import json
import os
import base64
import random
from openai import OpenAI

# --- Configuration ---
DATASET_FILENAME = "usage_data.json"
PAINTINGS_PER_GROUP = 3
NUM_GROUPS = 10
TOTAL_IMAGES = NUM_GROUPS * PAINTINGS_PER_GROUP
OUTPUT_IMAGE_PREFIX = "room"

# Folder paths (make these environment variables or config params when sharing)
PAINTINGS_FOLDER = os.environ.get("PAINTINGS_FOLDER", "input_paintings")
ROOM_OUTPUTS_FOLDER = os.environ.get("ROOM_OUTPUTS_FOLDER", "room_output")
FINAL_OUTPUTS_FOLDER = os.environ.get("FINAL_OUTPUTS_FOLDER", "final_output")

os.makedirs(ROOM_OUTPUTS_FOLDER, exist_ok=True)
os.makedirs(FINAL_OUTPUTS_FOLDER, exist_ok=True)

# --- Initialize ---
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
painting_files = sorted([
    os.path.join(PAINTINGS_FOLDER, f) for f in os.listdir(PAINTINGS_FOLDER)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])[:TOTAL_IMAGES]

dataset = []
room_images = []
costs = []

qualities = ["high", "medium", "low"]
prices = [ .167, .042, 0.011]

prompts = [("Create an image of a study room designed to complement Mata ni Pachdi artworks. "
        "Room Type: Study Room. "
        "Style/Mood: Modern Heritage. "
        "Furniture: Colourful fabric sofa. "
        "Decor: Brass lamp with golden base, Afghan rug, books. "
        "Lighting: Golden hour sunlight with warm tones. "
        "Note: Only include one artwork in the image.") ,

        ("Generate a dining room designed around a single Mata ni Pachedi artwork."
        "Room Type: Dining Room." 
        "Furniture: Hand-carved Sheesham wood dining table, mismatched traditional chairs with printed seat cushions." 
        "Decor: Brass thali centerpiece with marigold flowers, clay water jug, kalamkari runner." 
        "Lighting: Warm overhead hanging lantern with patterned shadows. " 
        "Note: Artwork should be hung on a feature wall visible from every seat, grounding the room with spiritual richness."),

        ("Create a luxurious hallway designed to enhance the beauty of a Mata ni Pachedi artwork. "
         "Room Type: Hallway/Entryway. "
        "Style/Mood: Art Gallery Luxe with Ethnic Accents. "
        "Furniture: Narrow brass-inlaid console table. "
        "Decor: Lotus-shaped brass diya, marble elephant figurines, antique mirror. "
        "Lighting: Focused warm spotlight on the painting with ambient daylight. "
        "Note: Keep walls neutral to let the traditional artwork feel like a curated centerpiece."),
        
        ("Create an image of a calm corner room designed to enhance a Mata ni Pachedi artwork. "
        "Room Type: Art Lounge / Reading Nook. "
        "Style/Mood: Contemporary Ethnic. "
        "Furniture: Textured accent chair with tribal print, wave-carved console. "
        "Decor: Sculptural lamp, dried bamboo stalks, open books, neutral rug with soft textures. "
        "Lighting: Diffused daylight with muted warm tones. "
        "Note: Only one framed painting should be visible, acting as the centerpiece above the console."),

        ("Create an image of a nature-inspired gallery room featuring a single Mata ni Pachedi artwork. "
        "Room Type: Indoor Gallery Niche. "
        "Style/Mood: Earthy and Botanical. "
        "Furniture: Vintage wood console with sliding doors. "
        "Decor: Assorted potted plants (bamboo, fiddle leaf, cactus), terracotta pots, green foliage. "
        "Lighting: Natural indirect light with a rustic warm backdrop. "
        "Note: Place the artwork on a deep terracotta wall, giving it a temple-like visual sanctity."),

        ("Create an image of a rustic, soulful room built around a single traditional Indian painting. "
        "Room Type: Quiet Sitting Corner. "
        "Style/Mood: Rustic Vintage. "
        "Furniture: Distressed wooden chair and log-style stool. "
        "Decor: Tall glass vase with a single dried bloom, blue-textured wall finish. "
        "Lighting: Soft natural light with slight shadow play. "
        "Note: The artwork should be the only visual focus, framed above the chair for a poetic touch.")
        ]




# --- Process ---
for i in range(NUM_GROUPS):
    group = painting_files[i * PAINTINGS_PER_GROUP: (i + 1) * PAINTINGS_PER_GROUP]
    files = [open(img_path, "rb") for img_path in group]
    
    try:
        prompt = prompts[i % len(prompts)]
        quality = qualities[i % len(qualities)]
        price = prices[i % len(prices)]

        result = client.images.edit(
            model="gpt-image-1",
            image=files,
            prompt=prompt,
            size="1024x1024",
            quality=quality
        )

        image_bytes = base64.b64decode(result.data[0].b64_json)

        data = result.model_dump()
        image_tokens = int(data["usage"]["input_tokens_details"]["image_tokens"])
        text_tokens = int(data["usage"]["input_tokens_details"]["text_tokens"])
        cost_value = image_tokens * 1e-5 + text_tokens * 5e-6 + price

        output_filename = f"{OUTPUT_IMAGE_PREFIX}_{i+1}.jpg"
        output_path = os.path.join(ROOM_OUTPUTS_FOLDER, output_filename)
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        data["output_image"] = output_filename
        data["cost"] = round(cost_value, 5)

        dataset.append(data)
        costs.append(cost_value)
        room_images.append(output_path)

        print(f"Generated room {i+1} using paintings {i*3+1} to {(i+1)*3}")

    except Exception as e:
        print("Something went wrong:", e)
    finally:
        for f in files:
            f.close()

# --- Save Results ---
with open(DATASET_FILENAME, "w") as f:
    json.dump(dataset, f, indent=4)

print("Total cost:", round(sum(costs), 5))
print("\nAll paintings have been processed successfully.")
