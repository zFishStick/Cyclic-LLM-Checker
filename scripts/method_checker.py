
import classes as cl

import os
from google import genai
from google.genai import types
from typing import Tuple
import json_writer as jw

# Retrieve API key from environment variable
geminiClient = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

import os
from openai import OpenAI

deepSeekClient = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

class MethodChecker:
    def ask_to_bot(self, chatbot: cl.Chatbot, prompt : cl.Prompt) -> Tuple[bool, str]:
        step = cl.Step()
        out = (False, "")
        
        #while not step.step_evaluation and step.step_num < 2:
        match chatbot.name:
            case "Gemini":
                step.chatbot_name = "Gemini"
                out = self.__ask_gemini(prompt)
                jw.write_json_to_file(step, prompt)
                
            case "Deepseek":
                step.chatbot_name = "Deepseek"
                out = self.__ask_deepseek(prompt)
                jw.write_json_to_file(step, prompt)
            
        step.next_step()
        step.evaluate_step(prompt.bot_output_text is not None)
            
                
        return out
    
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
        
        prompt.bot_output_text = response.text
        prompt.bot_evaluation = self.__evaluate_response(response.text)
        
        return (prompt.bot_evaluation, response.text)


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
        
        raise ValueError("Response could not be evaluated as True or Fake. Response: " + response)