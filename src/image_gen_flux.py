import torch
# --- Import the appropriate pipeline class for FLUX ---
from diffusers import FluxPipeline # Assuming FluxPipeline is the correct class
import os
from utils.logger import initiate_image

# --- Configuration ---

# 1. Model Name: Using a placeholder for a FLUX model ID.
# Replace 'PLACEHOLDER/flux-model-large' with the actual model ID (e.g., 'microsoft/flux-s-v2').
#MODEL_ID = "black-forest-labs/FLUX.1-dev"
#MODEL_ID = "black-forest-labs/FLUX.1-schnell"
#MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
MODEL_ID = "Manojb/stable-diffusion-2-1-base"


# MODEL_ID_1 is not used, so it is commented out for clarity:
# MODEL_ID_1 = "stabilityai/stable-diffusion-2-1" 
# --- Main Generation Function ---


IMAGE_FOLDER = "../data/created_images"

def generate_and_save_image(prompt: str):
    """
    Loads the FLUX pipeline and generates an image from a prompt.
    """
    print(f"Loading model: {MODEL_ID}...")

    # Determine the device (GPU if available, otherwise CPU)
    # FLUX models benefit highly from 'cuda' and 'bfloat16'
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # --- Pipeline Loading Logic Modified for FLUX ---
    
    # FLUX models often use bfloat16 for optimal performance on newer GPUs (e.g., NVIDIA A100, H100)
    # If the GPU doesn't support bfloat16, you might need to revert to float16.
    
    if device == "cuda":
        # Using bfloat16 if available, otherwise fallback to float16
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        pipe = FluxPipeline.from_pretrained(MODEL_ID, torch_dtype=dtype, use_safetensors=True)
        print(f"Model loaded with {dtype} for GPU acceleration.")
    else:
        # Use full precision for CPU (CPU is typically very slow for these models)
        pipe = FluxPipeline.from_pretrained(MODEL_ID, use_safetensors=True)
        print("Model loaded with full precision for CPU.")

    # Move the model to the determined device
    pipe.to(device)

    print("\n--- Generating Image ---")
    print(f"Prompt: '{prompt}'")

    # --- Generation Call Modified for FLUX ---
    # The generation parameters for FLUX might differ from Stable Diffusion
    # You may need to consult the FLUX documentation for the best settings.
    image = pipe(
        prompt=prompt,
        # Default settings for FLUX are often different and may require specific sampling steps
        num_inference_steps=28, # A common setting for FLUX models
        guidance_scale=4.5      # A common setting for FLUX models
    ).images[0]
    
    # The rest of the saving logic remains the same
    
    # --- Start of required changes ---

    # 1. Create the directory if it doesn't exist
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
        print(f"Created directory: {IMAGE_FOLDER}")

    # 2. Generate the unique filename
    image_name = str(initiate_image()) + '.jpg'
    print(f'This is the file name: {image_name}')

    # 3. Construct the full path to save the file
    full_path = os.path.join(IMAGE_FOLDER, image_name)

    # 4. Save the generated image to the full path
    image.save(full_path)
    
    print(f"\n✅ Success! Image saved to: {os.path.abspath(full_path)}")
    # --- End of required changes ---
    
    print("------------------------------------------")

    return image_name
