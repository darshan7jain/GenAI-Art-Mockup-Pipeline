import json
import os
import base64
import random
from openai import OpenAI

client = OpenAI("api-key")

# Setup folders
paintings_folder = "./openai_input_paintings"
room_outputs_folder = "./openai_room_output"
final_outputs_folder = "./openai_final_output"

os.makedirs(room_outputs_folder, exist_ok=True)
os.makedirs(final_outputs_folder, exist_ok=True)

# Get sorted list of 30 painting file paths
painting_files = sorted([
    os.path.join(paintings_folder, f) for f in os.listdir(paintings_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])[:30]

room_images = []
quality = ["high", "medium", "low"]
price = [0.167, 0.042, 0.011]

prompts = [
    "Create an image of a study room designed to complement Mata ni Pachdi artworks."
    "Room Type: Study Room. Style/Mood: Modern Heritage."
    "Furniture: Colourful fabric sofa. Decor: Brass lamp with golden base, Afghan rug, books."
    "Lighting: Golden hour sunlight with warm tones. Note: Only include one artwork in the image.",
    
    "Generate a dining room designed around a single Mata ni Pachedi artwork."
    "Room Type: Dining Room. Furniture: Hand-carved Sheesham wood dining table, mismatched traditional chairs with printed seat cushions."
    "Decor: Brass thali centerpiece with marigold flowers, clay water jug, kalamkari runner."
    "Lighting: Warm overhead hanging lantern with patterned shadows."
    "Note: Artwork should be hung on a feature wall visible from every seat, grounding the room with spiritual richness.",
    
    "Create a luxurious hallway designed to enhance the beauty of a Mata ni Pachedi artwork."
    "Room Type: Hallway/Entryway. Style/Mood: Art Gallery Luxe with Ethnic Accents."
    "Furniture: Narrow brass-inlaid console table. Decor: Lotus-shaped brass diya, marble elephant figurines, antique mirror."
    "Lighting: Focused warm spotlight on the painting with ambient daylight."
    "Note: Keep walls neutral to let the traditional artwork feel like a curated centerpiece.",
    
    "Create an image of a calm corner room designed to enhance a Mata ni Pachedi artwork."
    "Room Type: Art Lounge / Reading Nook. Style/Mood: Contemporary Ethnic."
    "Furniture: Textured accent chair with tribal print, wave-carved console."
    "Decor: Sculptural lamp, dried bamboo stalks, open books, neutral rug with soft textures."
    "Lighting: Diffused daylight with muted warm tones. Note: Only one framed painting should be visible, acting as the centerpiece above the console.",
    
    "Create an image of a nature-inspired gallery room featuring a single Mata ni Pachedi artwork."
    "Room Type: Indoor Gallery Niche. Style/Mood: Earthy and Botanical."
    "Furniture: Vintage wood console with sliding doors."
    "Decor: Assorted potted plants (bamboo, fiddle leaf, cactus), terracotta pots, green foliage."
    "Lighting: Natural indirect light with a rustic warm backdrop."
    "Note: Place the artwork on a deep terracotta wall, giving it a temple-like visual sanctity.",
    
    "Create an image of a rustic, soulful room built around a single traditional Indian painting."
    "Room Type: Quiet Sitting Corner. Style/Mood: Rustic Vintage."
    "Furniture: Distressed wooden chair and log-style stool."
    "Decor: Tall glass vase with a single dried bloom, blue-textured wall finish."
    "Lighting: Soft natural light with slight shadow play. Note: The artwork should be the only visual focus, framed above the chair for a poetic touch."
]

# cost = []

# STEP 1: -----Loop runs for 30 images-------
for i in range(30):
    group = painting_files[i * 3: (i + 1) * 3]
    images = [open(img_path, "rb") for img_path in group]

    try:
        result = client.images.edit(
            model="gpt-image-1",
            image=images,
            prompt=prompts[i % len(prompts)],
            size="1024x1024",
            quality=quality[i % 3]
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save room image
        room_path = os.path.join(room_outputs_folder, f"room_{i+1}.jpg")
        with open(room_path, "wb") as f:
            f.write(image_bytes)
        room_images.append(room_path)

        # Estimate cost
        # usage_data = json.loads(result.model_dump_json())
        # tokens = usage_data["input_tokens_details"]
        # temp_cost = (
        #     tokens["image_tokens"] * 1e-5 +
        #     tokens["text_tokens"] * 5e-6 +
        #     price[i % 3]
        # )
        # cost.append(temp_cost)

        print(f"Room {i+1} created using paintings {i*3+1}–{(i+1)*3}")
    except Exception as e:
        print(f"Failed at room {i+1}: {e}")
    finally:
        for img in images:
            img.close()

# print("\nEstimated cost:", cost)
# print("Total cost:", sum(cost))
print("Room generation complete.\n")

# STEP 2: Place each painting into a random room
for idx, painting_path in enumerate(painting_files):
    room_path = random.choice(room_images)

# ---------Use below lines of code if lesser than 30 outputs are needed like 10------------
# room_images = sorted([
#     os.path.join(room_outputs_folder, f) for f in os.listdir(room_outputs_folder)
#     if f.lower().endswith((".jpg", ".jpeg", ".png"))
# ])[:10]  
# for idx in range(30):
#     painting_path = painting_files[idx]
#     room_path = room_images[idx]

    try:
        result = client.images.edit(
            model="gpt-image-1",
            image=[
                open(painting_path, "rb"),
                open(room_path, "rb")
            ],
            prompt="Mask the painting image and realistically place it as artwork on the wall in the given room. Do not change anything else.",
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        output_path = os.path.join(final_outputs_folder, f"final_{idx+1}.jpg")
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        print(f"Painting {idx+1}/30 embedded into a room.")
    except Exception as e:
        print(f"Failed to embed painting {idx+1}: {e}")

print("\nAll paintings have been embedded into rooms.")
