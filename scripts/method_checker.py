
import classes as cl

import json_writer as jw

from classes.chatbot.gemini import Gemini
from classes.chatbot.deepseek import Deepseek

def _refresh_response(prompt: cl.Prompt):
    """Rebuild prompt.response to reflect current bot_output_text for evaluation steps."""
    if prompt.news.text:
        prompt.response = (
            f"A friend talked me about this news: '{prompt.news.title}' "
            f"with the following description: {prompt.news.text}. "
            f"He replied with this statement: '{prompt.bot_output_text}'. "
            f"Is his statement true or fake? Explain briefly why." )
    elif prompt.news.url:
        prompt.response = (
            f"A friend talked me about this news: '{prompt.news.title}' "
            f"accessible at: {prompt.news.url}. "
            f"He replied with this statement: '{prompt.bot_output_text}'. "
            f"Is his statement true or fake? Explain briefly why." )
    else:
        prompt.response = (
            f"He replied with this statement: '{prompt.bot_output_text}'. "
            f"Is his statement true or fake? Explain briefly why." )

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
        print("Gemini output: " + gemini_text)
        print("-----")
        prompt.bot_output_text = gemini_text
        prompt.bot_evaluation = gemini_eval
        _refresh_response(prompt)

        # Pass the prompt (not raw text) so Deepseek can read prompt.response
        ds_accept, ds_eval_text = Deepseek().evaluate_output(prompt)
        step.next_step()
        step.chatbot_name = "Deepseek"
        step.set_chatbot_agreement(ds_accept)
        step.set_news_evaluation(gemini_eval if ds_accept else None)
        prompt.bot_output_text = ds_eval_text
        prompt.bot_evaluation = ds_accept
        _refresh_response(prompt)
        jw.write_json_to_file(step, prompt)

        print(f"[STEP 1][DeepSeek evaluate] Accept={ds_accept}")
        print("DeepSeek evaluation: " + ds_eval_text)
        print("-----")

        if ds_accept:
            return (gemini_eval, gemini_text)

        prompt.bot_evaluation = ds_accept
        prompt.bot_output_text = ds_eval_text
        _refresh_response(prompt)
        last_output = gemini_text
        last_eval = gemini_eval

        while steps < self.step_limit:
            steps += 1

            # Deepseek rewrites using current prompt context
            ds_new_eval, ds_new_text = Deepseek().rewrite_output(prompt)
            step.next_step()
            step.chatbot_name = "Deepseek"
            step.set_news_evaluation(ds_new_eval)
            step.set_chatbot_agreement(None)
            prompt.bot_output_text = ds_new_text
            prompt.bot_evaluation = ds_new_eval
            _refresh_response(prompt)
            jw.write_json_to_file(step, prompt)

            print(f"[LOOP][DeepSeek rewrite] Eval={ds_new_eval}")
            print("DeepSeek rewrite: " + ds_new_text)
            print("-----")

            g_accept, g_accept_text = Gemini().evaluate_output(prompt)
            step.next_step()
            step.chatbot_name = "Gemini"
            step.set_chatbot_agreement(g_accept)
            step.set_news_evaluation(ds_new_eval if g_accept else None)
            prompt.bot_output_text = g_accept_text
            prompt.bot_evaluation = g_accept
            _refresh_response(prompt)
            jw.write_json_to_file(step, prompt)

            print(f"[LOOP][Gemini evaluate] Accept={g_accept}")
            print("Gemini evaluation: " + g_accept_text)
            print("-----")
            
            if g_accept:
                return (ds_new_eval, ds_new_text)

            # Update last_output for next rewrite cycle
            last_output = ds_new_text
            last_eval = ds_new_eval
        print("Step limit reached, final output may not be fully verified.")
        return (last_eval, last_output)

                
            