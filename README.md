## AI Mockup Generator (OpenAI)

This project uses OpenAI's image editing API (`gpt-image-1`) to generate realistic room mockups by compositing artwork onto interior backgrounds. It automates what would otherwise be a manual, time-consuming design process.

## How It Works
The final script takes a set of n artworks as input and uses OpenAI's `gpt-image-1` model to generate suitable room backgrounds and place the artwork appropriately. 

room_plus_final_mockup.py
<br>
This file contains the final pipeline of generating room images from a random input of artworks, followed by making the final mockups by imposing the artworks on the room images(random selection of both rooms and artworks).

artroom_generator.py
<br>
Works in a similar way as room_plus_final_mockup.py does but is restricted to only room image generation and not the final mockup(imposing artwork in room image).

prototype_openai.py
<br>
Uses OpenAI's gpt-image-1 model to generate a complete room mockup from a given artwork image. The script provides only the artwork as input, and the model creates a realistic interior background where the artwork is naturally placed, resulting in a photorealistic and visually appealing mockup.

prototype_gemini_1.py
<br>
An initial prototype using Google's Gemini API. Accepts an artwork and prompt to generate AI-enhanced room mockups. Focuses on exploring generative outputs.

prototype_gemini_2.py
<br>
An improved version of the first Gemini prototype. This script takes both the artwork (as the first image) and a background setup (as the second image) as inputs, then uses prompt-based generation to place the artwork realistically within the scene. It applies more refined prompt engineering and layout logic to produce visually accurate and aesthetically pleasing results.

## Setup Instructions

1. **Install dependencies**
   bash
   pip install openai python-dotenv

2. **Set your OpenAI API key**  
   Create a .env file in the root directory:
   
   OPENAI_API_KEY=your_openai_api_key
 

3. **Run the script**
   bash
   cd prototypes
   python prototype_openai.py

4. **Output**  
   The final mockup will be saved in the output directory.
