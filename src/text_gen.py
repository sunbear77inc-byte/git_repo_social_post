from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

IMAGE_FOLDER = "../data/created_images"


def draw_centered_wrapped_text(
    draw,
    image_size,
    text,
    font,
    fill=(255, 192, 0),
    margin=40,
    align="center",
):
    """
    Draws multi-line wrapped text centered in the image and constrained to margins.
    Includes a solid black background box for better readability.
    """
    image_width, image_height = image_size
    max_text_width = image_width - (margin * 2)

    # --- Wrap text to fit width ---
    lines = []
    words = text.split()

    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        test_width = bbox[2] - bbox[0]

        if test_width <= max_text_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # --- Calculate total text block height ---
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        height = bbox[3] - bbox[1]
        line_heights.append(height)

    # The line spacing is 6 pixels.
    line_spacing = 6
    total_text_height = sum(line_heights) + (len(lines) - 1) * line_spacing

    # --- START OF NEW CODE: DRAW BLACK BACKGROUND BOX ---
    
    # 1. Define Padding
    padding = 15 # Padding around the text block inside the black box
    
    # 2. Calculate Vertical Box Coordinates
    y_start_text = (image_height - total_text_height) / 2
    
    y_start_box = y_start_text - padding
    y_end_box = y_start_text + total_text_height + padding
    
    # 3. Calculate Horizontal Box Coordinates (based on image width and margin)
    x_start_box = margin - padding
    x_end_box = image_width - margin + padding
    
    # 4. Draw the Black Rectangle
    draw.rectangle(
        [(x_start_box, y_start_box), (x_end_box, y_end_box)], 
        fill="black"
    )

    # --- END OF NEW CODE: DRAW BLACK BACKGROUND BOX ---

    # Set the starting Y coordinate for the actual text (must be y_start_text)
    y = y_start_text
    current_line_y = y # Use a separate variable for iteration

    # --- Draw each line ---
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = line_heights[i] # Use pre-calculated height
        
        # Center horizontally
        x = (image_width - line_width) / 2

        draw.text((x, current_line_y), line, fill=fill, font=font, align=align)

        current_line_y += line_height + line_spacing # advance line position


def draw_text(text,image_name):
    # ... (rest of the draw_text function remains unchanged) ...
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    # --- Load image ---
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # --- Load font ---
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        12
    )

    # --- Draw wrapped centered text ---
    draw_centered_wrapped_text(
        draw=draw,
        image_size=img.size,
        text=text,
        font=font,
        fill=(255, 192, 0),
        margin=50
    )

    # --- Save output ---
    img.save(image_path)
    print("✅ Saved: output_wrapped_centered.jpg")
