from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

image_path = './gemini_single_images/test.jpg'
image1 = Image.open(image_path)

image_path = './gemini_single_images/bgm.jpg'
image2 = Image.open(image_path)

# client = genai.Client("api-key")
client = genai.Client(api_key="AIzaSyBB33BVATAEMo5l7NgjDAs1mdvRkQ6FHZs")

text_input = "Create an image using these two images, put the painting in image1 on the wall of image2. Make small variations to make the colors look better and brighter, do not alter the furniture"
response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=[text_input, image1,image2],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        temperature=0.2,  #0.2,0,5
        top_p=0.5,
        top_k=75,
        max_output_tokens=2048,
        candidate_count=1
    )
)

generated_image = None
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        image_bytes = part.inline_data.data
        generated_image = Image.open(BytesIO(image_bytes))
        break  # assuming only one image part

if generated_image is None:
    print("No image found in response!")
else:
    generated_image.show()
    base_name = './gemini_single_images/test'
    output_image_path = f"{base_name}_updated.jpg"
    generated_image.save(output_image_path)
    print(f"Generated image saved at: {output_image_path}")
