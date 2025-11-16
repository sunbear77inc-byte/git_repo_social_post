import requests
import json
import os
import mimetypes # New library needed for reliable type detection

# Your configuration variables (LOCAL_IMAGE_PATH, POSTIMAGE_UPLOAD_URL) should remain at the top

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
