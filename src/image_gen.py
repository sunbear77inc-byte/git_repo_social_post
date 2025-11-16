import torch
from diffusers import StableDiffusionPipeline
import os
from utils.logger import initiate_image

# --- Configuration ---

# 1. Model Name: Using a standard, relatively small Stable Diffusion model (1.5)
# You can change this to 'runwayml/stable-diffusion-v1-5' for a slightly larger model,
# or 'stabilityai/stable-diffusion-2-1' for a newer version.
MODEL_ID = "runwayml/stable-diffusion-v1-5"  
MODEL_ID_1 = "stabilityai/stable-diffusion-2-1"
# --- Main Generation Function ---

def generate_and_save_image(prompt: str):
    """
    Loads the Stable Diffusion pipeline and generates an image from a prompt.
    """
    print(f"Loading model: {MODEL_ID}...")

    # Determine the device (GPU if available, otherwise CPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Check if GPU is available and recommended settings
    if device == "cuda":
        # Enable half-precision (fp16) for faster generation on most modern GPUs
        pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
        print("Model loaded with float16 for GPU acceleration.")
    else:
        # Use full precision for CPU
        pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID)
        print("Model loaded with full precision for CPU.")
    
    # Move the model to the determined device
    pipe.to(device)

    print("\n--- Generating Image ---")
    print(f"Prompt: '{prompt}'")
    
    # Generate the image
    # Note: Use num_inference_steps=50 for quality, but lower (e.g., 20) for speed
    image = pipe(
        prompt=prompt,
        num_inference_steps=50,
        guidance_scale=7.5
    ).images[0]

    image_name = str(initiate_image()) + '.jpg'
    print(f'this is the file name {image_name}')
    # Save the generated image
    image.save(image_name)
    
    print(f"\n✅ Success! Image saved to: {os.path.abspath(image_name)}")
    print("------------------------------------------")


