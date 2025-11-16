from template_gen import get_prompt_words
from image_gen import generate_and_save_image
from utils.logger import log_hello 

print("about to get going")

prompt, filler_words = get_prompt_words()        
image_id = generate_and_save_image(prompt)
caption = prompt + "\n#quote\n\n"



#log_new_sequance(image_id,prompt,Filler_words)
log_hello()



print(prompt)
print(filler_words)
