import requests
import json
import os
import mimetypes 

# --- Configuration ---

# 🛑 1. Image File Path to Upload
# Update this path to where your image file is located (e.g., "1.jpg" or an absolute path)
LOCAL_IMAGE_PATH = "downloaded_image.jpeg" 

# 🛑 2. PostImage API Endpoint
POSTIMAGE_UPLOAD_URL = "https://postimages.org/json/uploader" 

# --- Image Upload Function ---

def upload_image_postimage(image_path):
    """
    Uploads the local image file to PostImage, enforcing MIME types for strict servers.
    """
    if not os.path.exists(image_path):
        print(f"❌ ERROR: Image file not found at path: {image_path}")
        return None

    print(f"\n🚀 Starting PostImage upload for: {os.path.basename(image_path)}...")

    # --- FIX APPLIED HERE: Detecting MIME type automatically ---
    filename = os.path.basename(image_path)
    
    # 1. Use mimetypes to reliably guess the Content-Type (e.g., 'image/jpeg')
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream' # Fallback for unknown types
        print(f"⚠️ Warning: Could not detect MIME type. Using generic: {mime_type}")
    else:
        print(f"   Detected MIME type: {mime_type}")

    file_stream = open(image_path, 'rb')
    
    # 2. Use the strict file tuple: (filename, file_object, content_type)
    files = {
        'upload': (filename, file_stream, mime_type) 
    }
    
    # --- END FIX ---
    
    data = {
        'numfiles': '1',
        'session_id': '0'
    }

    public_url = None
    try:
        response = requests.post(POSTIMAGE_UPLOAD_URL, files=files, data=data)
        response.raise_for_status() 

        result = response.json()

        if result.get('status') == 'OK' and 'hash' in result:
            public_url = result['hash'].get('url')
            print(f"✅ Upload successful!")
            print(f"   Public Viewer URL: {public_url}")
        else:
            print("❌ Upload Failed. Received error response:")
            print(json.dumps(result, indent=4))

    except requests.exceptions.RequestException as e:
        # A 400 error will be caught here
        print(f"❌ Network or API error during upload: {e}")
        
    finally:
        # Crucial: ensure the file stream is closed
        if 'file_stream' in locals() and not file_stream.closed:
             file_stream.close()
        
    return public_url

# -------------------------------------------------------------
# --- Execution Block (The 'main' part) ---
# -------------------------------------------------------------

if __name__ == "__main__":
    
    # Call the function to start the upload process
    final_url = upload_image_postimage(LOCAL_IMAGE_PATH)
    
    if final_url:
        print(f"\n✨ FINAL RESULT: Image uploaded successfully.")
        # Now you can use this URL for other purposes, like saving it to SQLite!
    else:
        print("\n🛑 Execution finished. Image upload failed.")
