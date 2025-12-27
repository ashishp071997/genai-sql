from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def generate_sql(question, prompt):
    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite",
        messages=[
            {
                "role": "user",
                "content": prompt.format(question=question)
            }
        ]
    )
    return response.choices[0].message.content.strip()
