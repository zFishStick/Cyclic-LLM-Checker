
from typing import Tuple
from classes.prompt import Prompt

import os
from openai import OpenAI

from ..util import evaluate_response

deepSeekClient = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

class Deepseek:
    def ask(self, prompt: Prompt) -> Tuple[bool, str]:
        response = deepSeekClient.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant. Your goal is to determine whether a given news headline is true or fake based on real-world information. Answer clearly and briefly with 'True' or 'Fake' and a short explanation."},
                {"role": "user", "content": prompt.input}
            ],
            stream=False
        )
        
        if response.choices[0].message.content is None:
            raise ValueError("No response from Deepseek.")
        
        return (evaluate_response(response.choices[0].message.content), response.choices[0].message.content)
    
    def reply_to_gemini_output(self, prompt : Prompt) -> Tuple[bool, str]:
        response = deepSeekClient.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant. Your goal is to determine whether a given news headline is true or fake based on real-world information. Answer clearly and briefly with 'True' or 'Fake' and a short explanation."},
                {"role": "user", "content": prompt.response}
            ],
            stream=False
        )
        
        if response.choices[0].message.content is None:
            raise ValueError("No response from Deepseek.")
        
        return (evaluate_response(response.choices[0].message.content), response.choices[0].message.content)