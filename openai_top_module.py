import openai
import os

def generate_content_top(art_data,artname):
    api_key ="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"
    if not api_key:
        raise ValueError('OpenAI API key not provided.')
    client = openai.OpenAI(api_key=api_key)
    top_products_schema = {
        "name": "products_html_table",
        "schema": {
            "type": "object",
            "properties": {
            "columns": {
                "type": "array",
                "description": "List of columns in the HTML table",
                "items": {
                "type": "object",
                "properties": {
                    "Name": {
                    "type": "string",
                    "description": "The name of the category in the table."
                    },
                    "Description": {
                    "type": "string",
                    "description": "A description corresponding to the category."
                    },
                    "Size (Inches)": {
                    "type": "string",
                    "description": "The name of the category in the table."
                    },
                    "Price (₹)": {
                    "type": "string",
                    "description": "A description corresponding to the category."
                    }
                    
                },
                "required": [
                    "Name",
                    "Description",
                    "Size (Inches)",
                    "Price (₹)"
                ],
                "additionalProperties": False
                }
            }
            },
            "required": [
            "columns"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
    products_input_messages = input=[
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
        "content": "I have a list of products in a collection. Use the information to generate an SEO-friendly HTML table containing descriptions for this collection. Follow the following structure. Your table should have the first 10 products as entires."
        },
        {
        "role": "assistant",
        "content": "Sure! Could you share the list of products? I'll help you organize or refine them for the collection page."
        },
        {
        "role": "user",
        "content": f"Collection Name : {artname} and Art Collection Products: {art_data}"
        }
    ]
    produts_completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=products_input_messages,
        response_format= {
            "type": "json_schema",
            "json_schema": top_products_schema
        }
    )

    return produts_completion.choices[0].message.content
