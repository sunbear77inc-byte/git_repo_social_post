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

# --- 2. Cloudinary Setup ---

# Initialize the Cloudinary configuration once
cloudinary.config( 
    cloud_name = CLOUD_NAME, 
    api_key = API_KEY, 
    api_secret = API_SECRET,
    secure = True
)

# --- 3. The Core Function ---

def up_load_image_2_cloudinary(image_path, folder_name="my_new_directory"):
    """
    Uploads a single image to Cloudinary and returns the permanent web address (secure URL).
    
    Args:
        image_path (str): The local path to the image file.
        folder_name (str): The specific folder name on Cloudinary.

    Returns:
        str: The permanent secure URL of the uploaded image, or None if failed.
    """
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

# --- 4. Main Execution Loop ---

if __name__ == "__main__":
    
    # 1. Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        print(f"🛑 Error: Folder '{UPLOAD_FOLDER}' not found. Please create it and add images.")
    else:
        # 2. Get a list of all files in the folder
        all_files = os.listdir(UPLOAD_FOLDER)
        
        # Filter for common image extensions (optional, but good practice)
        image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        uploaded_urls = []
        
        print(f"\n--- Starting Upload of {len(image_files)} Images ---")
        
        for filename in image_files:
            # Construct the full local path
            full_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Call the upload function
            url = up_load_image_2_cloudinary(full_path)
            
            if url:
                uploaded_urls.append(url)
        
        # 3. Print final results
        print("\n--- Upload Summary ---")
        if uploaded_urls:
            print(f"✨ Successfully uploaded {len(uploaded_urls)} images.")
            for url in uploaded_urls:
                print(f"- {url}")
        else:
            print("🛑 No images were uploaded.")
