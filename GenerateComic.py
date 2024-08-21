import requests
import io
from PIL import Image, ImageDraw, ImageFont
import os
import random


def GenerateComic(topic, style, target_lang='en'):
    # Initialize the InferenceClient with your model and token
    client = InferenceClient(
        # add Tokens Here...
    )

    # Initialize TranslateHelper
    translator = TranslateHelper()

    
    
    style_prompt = style_prompts.get(style, "funny story")

    # Combine the topic with the style prompt
    initial_prompt = "in 6 parts, each part divided by a blank line, narrate a story from a pov of a star which looks like an encyclopedia book. keep the sentences short.separate each phrase by a blank line "
    
    user_input = f"{topic} in {style_prompt}"
    prompt = initial_prompt + user_input

    # Define your message with the combined prompt
    messages = [
        {"role": "user", "content": prompt}
    ]

    # Generate the story in English
    story = ""
    for message in client.chat_completion(
        messages=messages,
        max_tokens=1000,  # Adjust the token limit as needed
        stream=True,
    ):
        story += message.choices[0].delta.content

    # Split the story into phrases
    phrases = story.strip().split("\n\n")

    # Directory to save images
    output_dir = os.path.join("C:\\Users\\Komal\\Desktop\\KKCODINGMAIN\\PROJECTS\\StarSketch\\templates", f"story_{random.randint(1, 100000)}")

    # Path to the comic font
    font_path = "C:\\Users\\Komal\\Desktop\\KKCODINGMAIN\\PROJECTS\\StarSketch\\font\\animeace2_reg.ttf"

    # Function to wrap text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = []

        for word in words:
            line_width, _ = font.getbbox(' '.join(line + [word]))[2:4]
            if line and line_width > max_width:
                lines.append(' '.join(line))
                line = [word]
            else:
                line.append(word)

        lines.append(' '.join(line))
        return lines

    # Generate and save images for each phrase with text overlay
    image_paths = []  # To store paths of images
    for i, phrase in enumerate(phrases):
        prompt = f"{phrase}, unique id {random.randint(1, 100000)}"
        response = query({"inputs": prompt})

        # Check if the response was successful
        if response and response.status_code == 200:
            image_bytes = response.content
            try:
                image = Image.open(io.BytesIO(image_bytes))

                # Create a white strip for text
                font_size = 16  # Smaller font size
                font = ImageFont.truetype(font_path, size=font_size)

                # Create the white strip
                text_width = image.width
                text_height = 100  # Height of the strip, adjust as needed
                white_strip = Image.new("RGB", (text_width, text_height), "white")

                # Translate the phrase to the target language for overlay
                translated_phrase = translator.lang_translate(phrase, target_lang)

                # Draw the translated text on the white strip
                draw = ImageDraw.Draw(white_strip)
                wrapped_text = wrap_text(translated_phrase, font, text_width - 20)  # 20 pixels margin

                # Calculate vertical position for the text
                y_text = 10  # Starting y position for text
                for line in wrapped_text:
                    text_bbox = draw.textbbox((0, y_text), line, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    position = ((white_strip.width - text_width) // 2, y_text)
                    draw.text(position, line, font=font, fill="black")  # Use black color for the text
                    y_text += text_bbox[3] - text_bbox[1] + 5  # Line height + padding

                # Create a new image with the white strip added on top
                new_image = Image.new("RGB", (image.width, image.height + text_height))
                new_image.paste(white_strip, (0, 0))  # Paste white strip on top
                new_image.paste(image, (0, text_height))  # Paste original image below the strip

                # Save the image
                image_path = os.path.join(output_dir, f"image_{i+1}.png")
                new_image.save(image_path)
                image_paths.append(image_path)  # Add image path to the list
                print(f"Saved image for phrase {i+1}: {image_path}")
            except Exception as e:
                print(f"Failed to process image for phrase {i+1}: {e}")
        else:
            print(f"Request failed with status code {response.status_code if response else 'Unknown'}")

    # Create a PDF from the images
    pdf_directory = "C:\\Users\\Komal\\Desktop\\KKCODINGMAIN\\PROJECTS\\StarSketch\\comicpdf"
    os.makedirs(pdf_directory, exist_ok=True)

    # Create a unique name for the PDF using a random unique ID
    unique_id = random.randint(100000, 999999)
    pdf_name = f"story_{unique_id}.pdf"
    pdf_path = os.path.join(pdf_directory, pdf_name)

    # Create a PDF from the images
    c = canvas.Canvas(pdf_path)
    for image_path in image_paths:
        img = Image.open(image_path)
        width, height = img.size
        c.setPageSize((width, height))
        c.drawImage(image_path, 0, 0, width, height)
        c.showPage()
    c.save()
    print(f"PDF created at {pdf_path}")
    return pdf_path
