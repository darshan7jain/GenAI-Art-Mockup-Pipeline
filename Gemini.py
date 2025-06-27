from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

import PIL.Image

image = PIL.Image.open('./gemini_images/img.jpg')

client = genai.Client("api_key")

text_input = ('Create an image similar to this, please note-change the wall colour to dark green and the rug should be an afghanistani kilim, keep plants and other stuff as it is')

response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=[text_input, image],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT','IMAGE']
    )
)

for part in response.candidates[0].content.parts:
    if part.text:
        print("Text:", part.text)
    elif part.inline_data:
        generated_image_bytes = part.inline_data.data
        generated_image = Image.open(BytesIO(generated_image_bytes))
        generated_image.show()
        base_name = './gemini_images/img'
        output_image_path = f"{base_name}_updated.jpg"
        generated_image.save(output_image_path)

print(f"Generated image saved at : {output_image_path}")
