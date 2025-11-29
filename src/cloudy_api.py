
import cloudinary
import cloudinary.uploader
import os

# --- 1. Configuration (REPLACE API KEY/SECRET) ---

# Your Cloud Name is already set (deegtazog)
CLOUD_NAME = "deegtazog"
# 🛑 REPLACE with your actual Cloudinary API Key and Secret
API_KEY = "519188851598325"
API_SECRET = "7tqHvk8FLdkejgAE1pPqbCigY7U"

# The local folder containing images you want to upload
UPLOAD_FOLDER = "upload" 


IMAGE_FOLDER = "../data/created_images"


# --- 2. Cloudinary Setup ---

# Initialize the Cloudinary configuration once
cloudinary.config( 
    cloud_name = CLOUD_NAME, 
    api_key = API_KEY, 
    api_secret = API_SECRET,
    secure = True
)

# --- 3. The Core Function ---

def up_load_image_2_cloudinary(image_name, folder_name="my_new_directory"):
    """
    Uploads a single image to Cloudinary and returns the permanent web address (secure URL).
    
    Args:
        image_path (str): The local path to the image file.
        folder_name (str): The specific folder name on Cloudinary.

    Returns:
        str: The permanent secure URL of the uploaded image, or None if failed.
    """
    
    image_path = os.path.join(IMAGE_FOLDER, image_name)


    if not os.path.exists(image_path):
        print(f"❌ ERROR: Image file not found at path: {image_path}")
        return None

    print(f"🚀 Uploading {os.path.basename(image_path)}...")

    try:
        # Use the uploader function provided by the SDK
        result = cloudinary.uploader.upload(
            image_path,
            folder=folder_name,
            # public_id is optional; if omitted, Cloudinary uses the filename
        )
        
        # Cloudinary returns a dictionary; we extract the secure URL
        secure_url = result.get('secure_url')
        
        print(f"✅ Success! URL: {secure_url}")
        return secure_url

    except Exception as e:
        print(f"❌ Cloudinary upload failed for {os.path.basename(image_path)}. Error: {e}")
        return None



