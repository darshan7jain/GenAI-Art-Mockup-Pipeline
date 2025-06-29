import json
import base64
import os
from openai import OpenAI

def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Function to open image safely using full path
    def open_image(filename):
        return open(os.path.join(script_dir, filename), "rb")

    # Prompt describing how to combine the images
    prompt = (
        "Place the painting given as Memeraki2.png (1st image) onto the wall in BackGround2.jpg. "
        "Do not change a single pixel in Memeraki2.png (1st Image)."
    )

    # Call the API to edit the image
    result = client.images.edit(
        model="gpt-image-1",
        image=[
            open_image("Memeraki2.png"),
            open_image("BackGround2.jpg"),
        ],
        prompt=prompt
    )

    # Decode the result and save the new image
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    output_path = os.path.join(script_dir, "result3.png")
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    main()
