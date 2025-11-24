
import classes as cl

from typing import Tuple
import json_writer as jw

from classes.chatbot.gemini import Gemini
from classes.chatbot.deepseek import Deepseek

# The user provides an input to Gemini.
# Gemini generates an output.
# DeepSeek evaluates Gemini's output to verify its reliability.
# If the output is reliable, it is returned to the user.
# If the output is not verified, DeepSeek generates a new output based on Gemini's output.
# The output is evaluated by Gemini.
# Gemini performs the same process as DeepSeek to verify the new output.
# Loop until the output is reliable. Note: to avoid infinite loops, a maximum number of iterations is 
# set to a predefined value. The main goal of this methodology is to leverage the strengths of both LLMs 
# to improve the reliability of the outputs provided to the user, in order to minimize the risk of misinformation.

class MethodChecker:
    def start_method(self, prompt: cl.Prompt):
        step = cl.Step()
        
        gemini_eval, gemini_response = Gemini().ask(prompt)
        prompt.bot_output_text = gemini_response
        prompt.bot_evaluation = gemini_eval
        step.chatbot_name = "Gemini"
        step.evaluate_step(gemini_eval) 

        print(f"Gemini response indicates the news is {'True' if gemini_eval else 'Fake'}")
        print(f"Response text: {gemini_response}")
        jw.write_json_to_file(step, prompt)
        
        deepseek_eval, deepseek_response = Deepseek().reply_to_gemini_output(prompt)
        prompt.bot_output_text = deepseek_response
        prompt.bot_evaluation = deepseek_eval
        print(f"Deepseek response indicates the news is {'True' if deepseek_eval else 'Fake'}")
        print(f"Response text: {deepseek_response}")
        jw.write_json_to_file(cl.Step(), prompt)
        
        if not deepseek_eval:
            step.next_step()
                    
        
        
        
