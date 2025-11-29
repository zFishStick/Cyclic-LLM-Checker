
import classes as cl

import json_writer as jw

from classes.chatbot.gemini import Gemini
from classes.chatbot.deepseek import Deepseek

class MethodChecker:
    def __init__(self, step_limit: int = 6):
        self.step_limit = step_limit

    def start_method(self, prompt: cl.Prompt):
        steps = 0
        step = cl.Step()

        gemini_eval, gemini_text = Gemini().ask(prompt)
        step.chatbot_name = "Gemini"
        step.evaluate_step(gemini_eval)
        jw.write_json_to_file(step, prompt)
        print(f"[STEP 0][Gemini] Eval={gemini_eval}")
        print("Gemini output: " + gemini_text)
        print("-----")
        prompt.bot_output_text = gemini_text
        prompt.bot_evaluation = gemini_eval
        prompt.update_response()

        ds_accept, ds_eval_text = Deepseek().evaluate_output(prompt)
        step.next_step()
        step.chatbot_name = "Deepseek"
        step.evaluate_step(ds_accept)
        prompt.bot_output_text = ds_eval_text
        prompt.bot_evaluation = ds_accept
        jw.write_json_to_file(step, prompt)

        print(f"[STEP 1][DeepSeek evaluate] Accept={ds_accept}")
        print("DeepSeek evaluation: " + ds_eval_text)
        print("-----")

        if ds_accept:
            return (gemini_eval, gemini_text)

        prompt.bot_evaluation = ds_accept
        prompt.bot_output_text = ds_eval_text
        prompt.update_response()

        while steps < self.step_limit:

            steps += 1

            ds_new_eval, ds_new_text = Deepseek().rewrite_output(prompt)
            step.next_step()
            step.chatbot_name = "Deepseek"
            step.evaluate_step(ds_new_eval)
            prompt.bot_output_text = ds_new_text
            # prompt.bot_evaluation = ds_new_eval
            prompt.update_response()
            jw.write_json_to_file(step, prompt)

            print(f"[LOOP][DeepSeek rewrite] Eval={ds_new_eval}")
            print("DeepSeek rewrite: " + ds_new_text)
            print("-----")

            g_accept, g_accept_text = Gemini().evaluate_output(prompt)
            step.next_step()
            step.chatbot_name = "Gemini"
            step.evaluate_step(g_accept)
            prompt.bot_output_text = g_accept_text
            prompt.bot_evaluation = g_accept
            prompt.update_response()
            jw.write_json_to_file(step, prompt)

            print(f"[LOOP][Gemini evaluate] Accept={g_accept}")
            print("Gemini evaluation: " + g_accept_text)
            print("-----")

            if g_accept: # If Gemini accepts DeepSeek's rewrite
                return (ds_new_eval, ds_new_text)
            
            g_new_eval, g_new_text = Gemini().rewrite_output(prompt)
            step.next_step()
            step.chatbot_name = "Gemini"
            step.evaluate_step(g_new_eval)
            prompt.bot_output_text = g_new_text
            # prompt.bot_evaluation = g_new_eval
            prompt.update_response()
            jw.write_json_to_file(step, prompt)
            
            print(f"[LOOP][Gemini rewrite] Eval={g_new_eval}")
            print("Gemini rewrite: " + g_new_text)
            print("-----")

            ds_accept, ds_eval_text = Deepseek().evaluate_output(prompt)
            step.next_step()
            step.chatbot_name = "Deepseek"
            step.evaluate_step(ds_accept)
            prompt.bot_output_text = ds_eval_text
            prompt.bot_evaluation = ds_accept
            prompt.update_response()
            jw.write_json_to_file(step, prompt)
            
            print(f"[LOOP][DeepSeek evaluate] Accept={ds_accept}")
            print("DeepSeek evaluation: " + ds_eval_text)
            print("-----")
            
            if ds_accept: # If DeepSeek accepts Gemini's rewrite
                return (g_new_eval, g_new_text)
            
            last_output = ds_new_text
            last_eval = ds_new_eval

        print("Step limit reached, final output may not be fully verified.")
        return (last_eval, last_output)

                
            