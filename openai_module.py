import openai
import os

def generate_content(art_data):
    api_key ="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"
    if not api_key:
        raise ValueError('OpenAI API key not provided.')
    client = openai.OpenAI(api_key=api_key)
    table_schema = {
        "name": "html_table",
        "schema": {
            "type": "object",
            "properties": {
                "columns": {
                    "type": "array",
                    "description": "List of columns in the HTML table",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["category", "description"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["columns"],
            "additionalProperties": False
        },
        "strict": True
    }
    input_messages = input=[
      {
        "role": "system",
        "content": "You are a skilled SEO content writer who is highly knowledgeable in traditional Indian arts."
      },
      {
        "role": "user",
        "content": "I have a online store called MeMeraki. MeMeraki.com is a  platform that helps traditional rural Indian artisans become digital creators. The platform offers online art and craft masterclasses, live classes, and an ecommerce marketplace for Indian heritage arts and crafts. We have customers in 40 countries. We cover 150+ artforms and 300+ artists."
      },
      {
        "role": "assistant",
        "content":  "That's incredible! MeMeraki is making a huge impact in preserving and promoting traditional Indian arts globally. What can I help you with? "
      },
      {
        "role": "user",
        "content": "I have a list of products in a collection. Use the information to generate an SEO-friendly HTML table containing descriptions for this collection. Follow the following structure. Your table should have the following rows - \n1. Origin\n2. History\n3. Famous Kerala Mural Paintings\n4. Technique\n5. Types/Styles\n6. Themes"
      },
      {
        "role": "assistant",
        "content": "Sure! Could you share the list of products? I'll help you organize or refine them for the collection page."
      },
      {
        "role": "user",
        "content": f"{art_data}"
      }
    ]
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=input_messages,
        response_format={
            "type": "json_schema",
            "json_schema": table_schema
        }
    )
    return completion.choices[0].message.content
