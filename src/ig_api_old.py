import requests
import json

# --- GLOBAL CONFIGURATION ---
# Configure these variables once
IG_USER_ID = "17841478078172531"
ACCESS_TOKEN = "EAAMgKdh8ZCJsBP3ktyJqS5C04FaYxQGzsq46A6iCfYI8nBrvf3JXA6hKhbW3waW023TxdipZAbLISLPRewMdgjTnpCowGAfwtvLun3giXAGBQZAzfQ4oEX7ZBo2TH4qOpBDmta2fJIJj0JicyBZCLkYMhxraV7ltRMvW4bPoTVqy8c95xksxpjhRziZBZBY"

def upload_to_ig(image_url, caption):
    """
    Uploads an image to Instagram using global auth credentials, 
    but specific URL and caption arguments.

    Args:
        image_url (str): Public URL of the image.
        caption (str): The text caption for the post.

    Returns:
        dict: The success response with the new Media ID, or an error dict.
    """
    base_url = "https://graph.facebook.com/v21.0"
    
    # --- Step 1: Create Media Container ---
    # Uses the arguments (image_url, caption) and global (ACCESS_TOKEN)
    container_url = f"{base_url}/{IG_USER_ID}/media"
    container_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    print("w about tosemd the ig\n\n\n") 
    try:
        container_res = requests.post(container_url, data=container_payload)
        container_data = container_res.json()
        
        # Check if container was created successfully
        if "id" not in container_data:
            return {
                "status": "error", 
                "message": "Failed to create container", 
                "raw": container_data
            }
            
        creation_id = container_data["id"]
        
        # --- Step 2: Publish Media ---
        publish_url = f"{base_url}/{IG_USER_ID}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": ACCESS_TOKEN
        }
        
        publish_res = requests.post(publish_url, data=publish_payload)
        publish_data = publish_res.json()
        
        if "id" in publish_data:
            return {"status": "success", "post_id": publish_data["id"]}
        else:
            return {
                "status": "error", 
                "message": "Failed to publish container", 
                "raw": publish_data
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

