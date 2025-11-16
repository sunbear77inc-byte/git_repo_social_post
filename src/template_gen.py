import os
import re
import random

# load template
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = (os.path.dirname(script_dir))
template_path = os.path.join(project_root, "data", "templates", "template_01.txt")


def get_prompt_words():
    with open(template_path, "r") as f:
        template_text= f.read()

    # extract placeholders
    placeholders = re.findall(r"{(.*?)}", template_text)

    chosen_words = {}

    for placeholder in placeholders:
        filepath = os.path.join(project_root,"data", "words", f"{placeholder}.txt")
     
        if not os.path.exists(filepath):
            print(f"No file foun: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

            # This removed the empty strings and returns a list with only words
            word_list = [line for line in lines if line.strip()]

            if not word_list:
                print(f"Empty file: {filepath}")
                continue

            chosen_words[placeholder] = random.choice(word_list)


    #recreates template
    for placeholder, selected_word in chosen_words.items():
        template_text = template_text.replace(f"{{{placeholder}}}", selected_word)

#    filler_words_pairs = list(chosen_words))
    return template_text, chosen_words
