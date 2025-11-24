
from typing import Tuple
from classes.prompt import Prompt
import os

from google import genai
from google.genai import types

from ..util import evaluate_response

geminiClient = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

class Gemini:
    def ask(self, prompt: Prompt) -> Tuple[bool, str]:
        print("Asking Gemini...")
        response = geminiClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt.input,
            config=types.GenerateContentConfig(
                system_instruction="You are a fact-checking assistant. Your goal is to determine whether a given news headline is true or fake based on real-world information. \nAnswer clearly and briefly with 'True' or 'Fake' and a short explanation."
            )
        )
        
        if response.text is None:
            raise ValueError("No response from Gemini.")
        
        prompt.bot_output_text = response.text
        prompt.bot_evaluation = evaluate_response(response.text)
        
        return (prompt.bot_evaluation, response.text)