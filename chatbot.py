from google import genai
from google.genai import types
from dotenv import load_dotenv

import os
from openai import OpenAI

load_dotenv() 

# Gemini API
client = genai.Client()

def chat_with_gemini(news_title: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"I read this news: '{news_title}'. Is this true or fake? Explain briefly why.",
        config=types.GenerateContentConfig(
            system_instruction="You are a fact-checking assistant. Your goal is to determine whether a given news headline is true or fake based on real-world information. Answer clearly with 'True' or 'Fake' and a short explanation."
        )
    )
    return (response.text or "").strip()

def chat_with_deepseek(news_title: str, news_truth_value: str) -> str:

    client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": f"A person said that the following news: '{news_title}' is {news_truth_value}, can you verify it?"
            }
        ]
    )
    return response.choices[0].message.content or ""