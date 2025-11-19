
from urllib import response
import scripts.classes as cl

from google import genai
from google.genai import types

geminiClient = genai.Client()

import os
from openai import OpenAI

deepSeekClient = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

def ask_to_bot(chatbot: cl.chatbot, prompt : cl.Prompt) -> str:
    
    step = cl.Step()
    
    while not step.step_evaluation:
        match chatbot.name:
            case "Gemini":
                step.step_evaluation = ask_gemini(prompt)
            case "Deepseek":
                step.step_evaluation = ask_deepseek(prompt)
    
    return "No chatbot found"

def ask_gemini(prompt: cl.Prompt) -> bool:
    response = geminiClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt.input,
        config=types.GenerateContentConfig(
            system_instruction="You are a fact-checking assistant. Your goal is to determine whether a given news headline is true or fake based on real-world information. \nAnswer clearly and briefly with 'True' or 'Fake' and a short explanation."
        )
    )
    
    if response.text is None:
        raise ValueError("No response from Gemini.")
    
    return evaluate_response(response.text)


def ask_deepseek(prompt: cl.Prompt) -> bool:
    response = deepSeekClient.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a fact-checking assistant. Your goal is to determine whether a given news headline is true or fake based on real-world information. Answer clearly and briefly with 'True' or 'Fake' and a short explanation."}, # System message to set the behavior of the assistant
            {"role": "user", "content": prompt.input} # User message with the news title,
        ],
        stream=False
    )
    
    if response.choices[0].message.content is None:
        raise ValueError("No response from Deepseek.")
    
    return evaluate_response(response.choices[0].message.content)

def evaluate_response(response: str) -> bool:
    text = response.strip().lower()

    if text.startswith("true"):
        return True

    if text.startswith("false") or text.startswith("fake"):
        return False
    
    raise ValueError("Response could not be evaluated as True or Fake.")