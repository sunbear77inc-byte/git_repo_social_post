from template_gen import get_prompt_words
from image_gen import generate_and_save_image
from utils.logger import log_hello 
from cloudy_api import up_load_image_2_cloudinary
from ig_api import upload_to_ig



print("about to get going")

prompt, filler_words = get_prompt_words()        
image_name = generate_and_save_image(prompt)
print(image_name)
caption = prompt + "\n#quote\n\n"
print("about to get cloudy going,{image_id}")
cloudy_url = up_load_image_2_cloudinary(image_name)
print(cloudy_url)

upload_to_ig(cloudy_url,caption)
print("just sent to ig")

#log_new_sequance(image_id,prompt,Filler_words)
log_hello()



print(prompt)
print(filler_words)
