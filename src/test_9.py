import cloudinary
import cloudinary.uploader
import os

# --- 1. Configuration (REPLACE THESE) ---
# Get these values from your Cloudinary Dashboard
CLOUD_NAME = "deegtazog"
API_KEY = "519188851598325"
API_SECRET = "7tqHvk8FLdkejgAE1pPqbCigY7U"

# Local image path
LOCAL_IMAGE_PATH = "downloaded_image.jpeg" 

# --- 2. Cloudinary Setup ---
# Initialize the Cloudinary configuration once
cloudinary.config( 
    cloud_name = CLOUD_NAME, 
    api_key = API_KEY, 
    api_secret = API_SECRET,
    secure = True
)

# --- 3. Upload Function ---
def upload_image_cloudinary(image_path):
    """Uploads the local image file to Cloudinary and returns the public URL."""
    if not os.path.exists(image_path):
        print(f"❌ ERROR: Image file not found at path: {image_path}")
        return None

    print(f"\n🚀 Starting Cloudinary upload for: {os.path.basename(image_path)}...")

    try:
        # Use the uploader function provided by the SDK
        result = cloudinary.uploader.upload(image_path)
        
        public_url = result.get('secure_url')
        
        print(f"✅ Upload successful!")
        print(f"   Public Image URL: {public_url}")
        
        return public_url

    except Exception as e:
        print(f"❌ Cloudinary upload failed. Error: {e}")
        return None

# --- 4. Execution Block ---
if __name__ == "__main__":
    final_url = upload_image_cloudinary(LOCAL_IMAGE_PATH)
    
    if final_url:
        print(f"\n✨ FINAL RESULT: Cloudinary URL is {final_url}")
    else:
        print("\n🛑 Execution finished. Cloudinary upload failed.")
