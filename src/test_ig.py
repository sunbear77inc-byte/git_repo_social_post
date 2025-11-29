import requests
import json
import time
from typing import Optional

# --- Configuration ---
# You can update this to the current version if needed.
API_VERSION = "v24.0" 
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


HEADERS = {
    # Spoofs the request to look like it's coming from a mobile browser (iPhone 13 on iOS 15)
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}







def publish_instagram_media(
    ig_user_id: str,
    access_token: str,
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
        container_endpoint = f"{BASE_URL}/{ig_user_id}/media"
        params = {
            'image_url': media_url,
            'caption': caption,
            'access_token': access_token
        }
    elif media_type.upper() == "VIDEO":
        # For videos, we use 'video_url' and must also include the 'media_type' parameter
        container_endpoint = f"{BASE_URL}/{ig_user_id}/media"
        params = {
            'video_url': media_url,
            'caption': caption,
            'media_type': 'VIDEO',
            'access_token': access_token
        }
    else:
        print("ERROR: Invalid media_type specified. Must be 'IMAGE' or 'VIDEO'.")
        return headers=HEADERSNone

    try:
        container_response = requests.post(container_endpoint, data=params, headers=HEADERS)
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
        check_params = {'fields': 'status_code', 'access_token': access_token}
        
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


    # 2. Publish Media
    print("2. Publishing Media...")
    publish_endpoint = f"{BASE_URL}/{ig_user_id}/media_publish"
    publish_params = {
        'creation_id': container_id,
        'access_token': access_token
    }

    try:
        publish_response = requests.post(publish_endpoint, data=publish_params, headers=HEADERS)
        publish_response.raise_for_status()
        publish_data = publish_response.json()
        
        media_id = publish_data.get('id')
        if not media_id:
            print(f"ERROR: Failed to get media ID. Response: {publish_data}")
            return None
            
        print(f"   -> SUCCESS! Media Post ID: {media_id}")
        return media_id

    except requests.exceptions.RequestException as e:
        print(f"ERROR during media publishing: {e}")
        return None


# ====================================================================
#                               MAIN EXECUTION BLOCK
# ====================================================================

if __name__ == "__main__":
    # --- ⚠️ IMPORTANT: REPLACE THESE WITH YOUR ACTUAL VALUES ⚠️ ---
    
    # 1. Instagram User ID (The ID of the Business/Creator account)
    INSTAGRAM_USER_ID = "17841478078172531"
    
    # 2. User Access Token (Must have 'instagram_content_publish' permission)
    USER_ACCESS_TOKEN = "EAAMgKdh8ZCJsBP3ktyJqS5C04FaYxQGzsq46A6iCfYI8nBrvf3JXA6hKhbW3waW023TxdipZAbLISLPRewMdgjTnpCowGAfwtvLun3giXAGBQZAzfQ4oEX7ZBo2TH4qOpBDmta2fJIJj0JicyBZCLkYMhxraV7ltRMvW4bPoTVqy8c95xksxpjhRziZBZBY"
    
    # 3. Publicly accessible URL for your media file (IMAGE or VIDEO)
    # This example URL is a placeholder and may not work.
    MEDIA_FILE_URL = "https://res.cloudinary.com/deegtazog/image/upload/v1764130734/my_new_directory/hcj3myytc5xntupk6ydk.jpg"
    
    # 4. Caption for the post
    POST_CAPTION = "Check out this amazing post from my API script! #Python #InstagramAPI"

    # 5. Type of media ('IMAGE' or 'VIDEO')
    MEDIA_TYPE = "IMAGE" # Change to "VIDEO" if posting a video

    # -------------------------------------------------------------------
    
    if INSTAGRAM_USER_ID == "YOUR_IG_USER_ID_HERE" or USER_ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        print("\n--- 🛑 SETUP ERROR 🛑 ---")
        print("Please replace INSTAGRAM_USER_ID and USER_ACCESS_TOKEN with your actual credentials.")
        print("------------------------\n")
    else:
        # Call the function to attempt the publish
        post_id = publish_instagram_media(
            ig_user_id=INSTAGRAM_USER_ID,
            access_token=USER_ACCESS_TOKEN,
            media_url=MEDIA_FILE_URL,
            caption=POST_CAPTION,
            media_type=MEDIA_TYPE
        )
        
        if post_id:
            print("\n✅ Publishing process completed successfully.")
        else:
            print("\n❌ Publishing process failed.")
