import os
import random


current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'data', 'overlay_text', 'ov_text.txt')

def get_text_overlay():
    """
    Reads lines from a file in a different directory, randomly selects one line,
    and returns it.

    Returns:
        str: A randomly selected line from the quotes file.
    """
    # 1. Define the path to the file in a different directory.
    # We use os.path.join and os.path.dirname to construct a path relative
    # to the current script's location. This makes the code more robust.
    # Assumes 'quotes.txt' is one directory up inside a 'data' folder.



    # 2. Read all lines from the file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # .strip() removes any leading/trailing whitespace, including newline characters (\n)
            # We filter out empty lines that might result from stripping.
            sentences = [line.strip() for line in file if line.strip()]

    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"Error: The file was not found at {file_path}")
        return "Quote file not found."

    except Exception as e:
        # Handle other potential file reading errors
        print(f"An error occurred while reading the file: {e}")
        return "Error reading quotes."

    # 3. Randomly select and return a sentence
    if sentences:
        return random.choice(sentences)
    else:
        return "The quotes file is empty."


