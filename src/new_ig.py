import requests
import json
import time
from typing import Optional

# --- Configuration ---
# You can update this to the current version if needed.
API_VERSION = "v24.0" 
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"
INSTAGRAM_USER_ID = "17841478078172531"
USER_ACCESS_TOKEN = "EAAMgKdh8ZCJsBP3ktyJqS5C04FaYxQGzsq46A6iCfYI8nBrvf3JXA6hKhbW3waW023TxdipZAbLISLPRewMdgjTnpCowGAfwtvLun3giXAGBQZAzfQ4oEX7ZBo2TH4qOpBDmta2fJIJj0JicyBZCLkYMhxraV7ltRMvW4bPoTVqy8c95xksxpjhRziZBZBY"


def publish_instagram_media(
    media_url: str,
    caption: str,
    media_type: str = "IMAGE"
) -> Optional[str]:
    """
    Publishes an image or video to an Instagram Business/Creator account 
    via the Instagram Graph API (2-step process).

    Args:
        ig_user_id: Your Instagram Business/Creator Account ID.
        access_token: Your User Access Token with 'instagram_content_publish' permission.
        media_url: The publicly accessible URL of the image or video file.
        caption: The caption text for the post.
        media_type: 'IMAGE' or 'VIDEO'. (Defaults to 'IMAGE')

    Returns:
        The ID of the newly created Instagram media object, or None on failure.
    """
    print(f"--- Starting {media_type} Post Process ---")

    # 1. Create Media Container
    print("1. Creating Media Container...")
    
    if media_type.upper() == "IMAGE":
        # For images, we use 'image_url' parameter
        container_endpoint = f"{BASE_URL}/{INSTAGRAM_USER_ID}/media"
        params = {
            'image_url': media_url,
            'caption': caption,
            'access_token': USER_ACCESS_TOKEN
        }
    elif media_type.upper() == "VIDEO":
        # For videos, we use 'video_url' and must also include the 'media_type' parameter
        container_endpoint = f"{BASE_URL}/{INSTAGRAM_USER_ID}/media"
        params = {
            'video_url': media_url,
            'caption': caption,
            'media_type': 'VIDEO',
            'access_token': USER_ACCESS_TOKEN
        }
    else:
        print("ERROR: Invalid media_type specified. Must be 'IMAGE' or 'VIDEO'.")
        return None

    try:
        container_response = requests.post(container_endpoint, data=params)
        container_response.raise_for_status() # Raise an exception for bad status codes
        container_data = container_response.json()
        
        container_id = container_data.get('id')
        if not container_id:
            print(f"ERROR: Failed to get container ID. Response: {container_data}")
            return None
        
        print(f"   -> Container ID created: {container_id}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR during container creation: {e}")
        return None

    # --- Video Specific Check (Wait for processing to complete) ---
    if media_type.upper() == "VIDEO":
        print("   -> Video uploaded. Polling status (up to 5 min) for processing...")
        # Instagram needs time to process videos. We must poll the status.
        
        status_endpoint = f"{BASE_URL}/{container_id}"
        check_params = {'fields': 'status_code', 'access_token': USER_ACCESS_TOKEN}
        
        # Max wait time (5 minutes)
        max_checks = 30
        for i in range(max_checks):
            time.sleep(10) # Wait 10 seconds between checks
            status_response = requests.get(status_endpoint, params=check_params)
            status_response.raise_for_status()
            status_code = status_response.json().get('status_code')

            if status_code == 'FINISHED':
                print("   -> Video processing is FINISHED. Ready to publish.")
                break
            elif status_code == 'ERROR':
                print(f"ERROR: Video processing failed. Check video requirements.")
                return None
            
            print(f"   -> Status Check {i+1}/{max_checks}: {status_code}...")
        else:
            print("ERROR: Video processing timed out.")
            return None
    

    DELAY_SECONDS = 9
    print(f"   -> Waiting {DELAY_SECONDS} seconds for media processing...")
    time.sleep(DELAY_SECONDS)

    publish_endpoint = f"{BASE_URL}/{INSTAGRAM_USER_ID}/media_publish"
    publish_params = {
        'creation_id': container_id,
        'access_token': USER_ACCESS_TOKEN
        } 

    try:
        publish_response = requests.post(publish_endpoint, data=publish_params)

        # Instead of just relying on the generic exception, check status code first
        if publish_response.status_code >= 400:
            print(f"!!! FATAL PUBLISH ERROR !!! HTTP Status Code {publish_response.status_code}")
            print("   -> Reading API Error Message:")
            try:
                # Print the detailed JSON error from the API
                publish_error_data = publish_response.json()
                print(json.dumps(publish_error_data, indent=4))
            except json.JSONDecodeError:
                # If API didn't return JSON, print the raw text
                print("   -> Raw Response Content:")
                print(publish_response.text)
            return None # Return None here because of the error
    
        # ... (If status code was 200, proceed to success logic below) ...
        publish_data = publish_response.json()
        media_id = publish_data.get('id')
        # ... (rest of success logic) ...
    
    except requests.exceptions.RequestException as e:
        # This catches non-HTTP errors like connection failure
        print(f"NETWORK/CONNECTION ERROR during media publishing: {e}")
        return None
    # 2. Publis
