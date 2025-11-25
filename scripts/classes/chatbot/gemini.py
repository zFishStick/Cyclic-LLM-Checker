
from typing import Tuple
from classes.prompt import Prompt
import os

from google import genai
from google.genai import types

from ..util import evaluate_response

geminiClient = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

class Gemini:
    
    model = "gemini-2.5-flash"
    
    def ask(self, prompt: Prompt) -> Tuple[bool, str]:
        print("Asking Gemini...")
        response = geminiClient.models.generate_content(
            model=self.model,
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
    
    def evaluate_output(self, prev_output: str):
        response = geminiClient.models.generate_content(
            model=self.model,
            contents=f"Evaluate whether the following fact-checking reasoning is logically sound. Reply ONLY with 'Accept' or 'Reject' and a very short explanation.\n\n{prev_output}"
        )
        
        if response.text is None:
            raise ValueError("No response from Gemini (evaluate_output).")
        
        text = response.text.lower()
        accepted = text.startswith("accept")
        return accepted, response.text
    
    def rewrite_output(self, prev_output: str):
        response = geminiClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"The previous reasoning was rejected. Rewrite a better fact-checking analysis.\n\nPrevious reasoning:\n{prev_output}"
        )
        text = response.text
        
        if text is None:
            raise ValueError("No response from Gemini (rewrite_output).")
        
        return evaluate_response(text), text