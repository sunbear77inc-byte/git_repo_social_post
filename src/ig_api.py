import requests
import json

# --- GLOBAL CONFIGURATION (Keep these outside the function) ---
IG_USER_ID = "17841478078172531" # Assume this is defined globally
ACCESS_TOKEN = "EAAMgKdh8ZCJsBP3ktyJqS5C04FaYxQGzsq46A6iCfYI8nBrvf3JXA6hKhbW3waW023TxdipZAbLISLPRewMdgjTnpCowGAfwtvLun3giXAGBQZAzfQ4oEX7ZBo2TH4qOpBDmta2fJIJj0JicyBZCLkYMhxraV7ltRMvW4bPoTVqy8c95xksxpjhRziZBZBY" # Assume this is defined globally


# Define the spoofed headers globally or just inside the function
# Using a common mobile User-Agent is the safest choice for social media APIs
HEADERS = {
    # Spoofs the request to look like it's coming from a mobile browser (iPhone 13 on iOS 15)
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}


def upload_to_ig(image_url, caption):
    """
    Uploads an image to Instagram, now using spoofed User-Agent headers.
    """
    base_url = "https://graph.facebook.com/v24.0"
    
    # --- Step 1: Create Media Container ---
    container_url = f"{base_url}/{IG_USER_ID}/media"
    container_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    
    print("Sending container request with spoofed headers...")
    try:
        # 🐛 FIX: Add the 'headers=HEADERS' argument here
        container_res = requests.post(container_url, data=container_payload, headers=HEADERS)
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
        
        # 🐛 FIX: Add the 'headers=HEADERS' argument here too
        publish_res = requests.post(publish_url, data=publish_payload, headers=HEADERS)
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
