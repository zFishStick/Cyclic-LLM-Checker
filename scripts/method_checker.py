
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
        # Gemini provides a news evaluation
        step.set_news_evaluation(gemini_eval)
        step.set_chatbot_agreement(None)
        jw.write_json_to_file(step, prompt)

        print(f"[STEP 0][Gemini] Eval={gemini_eval}")
        print(gemini_text)

        ds_accept, ds_eval_text = Deepseek().evaluate_output(gemini_text)
        step.next_step()
        step.chatbot_name = "Deepseek"
        # Deepseek evaluates Gemini's output -> chatbot agreement
        step.set_chatbot_agreement(ds_accept)
        # If Deepseek accepts, copy Gemini's news evaluation; else None
        step.set_news_evaluation(gemini_eval if ds_accept else None)
        prompt.bot_output_text = ds_eval_text
        jw.write_json_to_file(step, prompt)

        print(f"[STEP 1][DeepSeek evaluate] Accept={ds_accept}")
        print(ds_eval_text)

        if ds_accept:
            return (gemini_eval, gemini_text)

        last_output = gemini_text
        last_eval = gemini_eval

        while steps < self.step_limit:
            steps += 1

            ds_new_eval, ds_new_text = Deepseek().rewrite_output(last_output)
            step.next_step()
            step.chatbot_name = "Deepseek"
            # Deepseek proposes a new news evaluation
            step.set_news_evaluation(ds_new_eval)
            step.set_chatbot_agreement(None)
            prompt.bot_output_text = ds_new_text
            jw.write_json_to_file(step, prompt)

            print(f"[LOOP][DeepSeek rewrite] Eval={ds_new_eval}")
            print(ds_new_text)

            g_accept, g_accept_text = Gemini().evaluate_output(ds_new_text)
            step.next_step()
            step.chatbot_name = "Gemini"
            # Gemini evaluates Deepseek's output -> chatbot agreement
            step.set_chatbot_agreement(g_accept)
            # If Gemini accepts, copy Deepseek's news evaluation; else None
            step.set_news_evaluation(ds_new_eval if g_accept else None)
            prompt.bot_output_text = g_accept_text
            jw.write_json_to_file(step, prompt)

            print(f"[LOOP][Gemini evaluate] Accept={g_accept}")
            print(g_accept_text)

            if g_accept:
                return (ds_new_eval, ds_new_text)

            last_output = ds_new_text
            last_eval = ds_new_eval

        print("Step limit reached, final output may not be fully verified.")
        return (last_eval, last_output)

                
            