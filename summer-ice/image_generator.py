from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_image(prompt):
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = image_response.data[0].url
    return image_url
