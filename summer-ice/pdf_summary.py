from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def summarize_text(extracted_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Summarize this document:\n\n{extracted_text}"}
        ],
        temperature=0.5,
        max_tokens=500
    )
    summary = response.choices[0].message.content
    return summary
