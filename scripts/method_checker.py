
import classes as cl

import os
from google import genai
from google.genai import types
from typing import Tuple

# Retrieve API key from environment variable
geminiClient = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

import os
from openai import OpenAI

deepSeekClient = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

class MethodChecker:
    def ask_to_bot(self, chatbot: cl.Chatbot, prompt : cl.Prompt) -> Tuple[bool, str]:
        response = ""
        step = cl.Step()
        
        # while not step.step_evaluation:
        match chatbot.name:
            case "Gemini":
                step.step_evaluation, response = self.__ask_gemini(prompt)
            case "Deepseek":
                step.step_evaluation, response = self.__ask_deepseek(prompt)
        
        return (step.step_evaluation, response)
    
    def __ask_gemini(self, prompt: cl.Prompt) -> Tuple[bool, str]:
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
        
        return (self.__evaluate_response(response.text), response.text)


    def __ask_deepseek(self, prompt: cl.Prompt) -> Tuple[bool, str]:
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
        
        return (self.__evaluate_response(response.choices[0].message.content), response.choices[0].message.content)

    def __evaluate_response(self, response: str) -> bool:
        text = response.strip().lower()

        if text.startswith("true") or text.startswith("real"):
            return True

        if text.startswith("false") or text.startswith("fake"):
            return False
        
        raise ValueError("Response could not be evaluated as True or Fake.")