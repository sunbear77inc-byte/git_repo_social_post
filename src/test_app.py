from template_gen import get_prompt_words
from image_gen_flux import generate_and_save_image
from utils.logger import log_hello 
from cloudy_api import up_load_image_2_cloudinary
from ig_api import upload_to_ig
from new_ig import publish_instagram_media


print("about to get going")

prompt, filler_words = get_prompt_words()        
image_name = generate_and_save_image(prompt)
print(image_name)
caption = prompt
print("about to get cloudy going,{image_id}")
cloudy_url = up_load_image_2_cloudinary(image_name)
print(cloudy_url)

#upload_to_ig(cloudy_url,caption)
i#resulta = publish_instagram_media(cloudy_url,caption)

print("just sent to ig\n\n\n\n\n")
#print(resulta)
#log_new_sequance(image_id,prompt,Filler_words)
log_hello()



print(prompt)
print(filler_words)
