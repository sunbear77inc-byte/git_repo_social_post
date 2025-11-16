import requests
import json
import os

# --- Configuration ---

# 🛑 1. Image File Path to Upload
# Since you were running in ~/git_repo_social_post/src/ and the file was 1.jpg, 
# we'll use a relative path for simplicity, assuming the script is run there.
LOCAL_IMAGE_PATH = "downloaded_image.jpeg" 

# PostImage API Endpoint for JSON responses
POSTIMAGE_UPLOAD_URL = "https://postimages.org/json/uploader" 

# --- Image Upload Function ---

def upload_image_postimage(image_path):
    """
    Uploads the local image file to PostImage using the keyless anonymous method 
    and returns the public URL.
    """
    if not os.path.exists(image_path):
        # Check if the file exists before attempting to open it
        print(f"❌ ERROR: Image file not found at path: {image_path}")
        # Try a different path if the local one fails (e.g., the absolute path you used before)
        # Fallback_path = "/home/wlsbase/git_repo_social_post/src/1.jpg"
        # if os.path.exists(Fallback_path):
        #     image_path = Fallback_path
        # else:
        return None

    print(f"\n🚀 Starting PostImage upload for: {os.path.basename(image_path)}...")

    # Open the file in read-binary mode ('rb') for the upload
    # 'files' is a dictionary where the key ('upload') is the expected form field name
    files = {
        'upload': open(image_path, 'rb') 
    }
    
    # Required data for PostImage anonymous upload
    data = {
        'numfiles': '1',
        'session_id': '0'
    }

    public_url = None
    try:
        # Send the POST request
        response = requests.post(POSTIMAGE_UPLOAD_URL, files=files, data=data)
        response.raise_for_status() # Raise error for bad HTTP status codes

        result = response.json()

        # Parse the JSON response to find the public URL
        if result.get('status') == 'OK' and 'hash' in result:
            image_data = result['hash']
            # The 'url' key contains the viewer link which is public and stable
            public_url = image_data.get('url')
            
            print(f"✅ Upload successful!")
            print(f"   Public Viewer URL: {public_url}")
        else:
            print("❌ Upload Failed. Received error response:")
            print(json.dumps(result, indent=4))

    except requests.exceptions.RequestException as e:
        print(f"❌ Network or API error during upload: {e}")
        
    finally:
        # Crucial: ensure the file stream is closed
        files['upload'].close()
        
    return public_url

# --- Execution Block ---

if __name__ == "__main__":
    # Call the function and get the URL
    final_url = upload_image_postimage(LOCAL_IMAGE_PATH)
    
    if final_url:
        print(f"\n✨ FINAL URL: {final_url}")
    else:
        print("\n🛑 Image upload failed. Check the error messages above.")
