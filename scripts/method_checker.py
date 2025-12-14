
from . import classes as cl

import scripts.util.json_writer as jw

from .classes.chatbot.gemini import Gemini
from .classes.chatbot.deepseek import Deepseek

from .classes.util import text_similarity

def _refresh_response(prompt: cl.Prompt):
        
    question_suffix = (
        f"He analyzed it and replied with this statement: '{prompt.bot_output_text}'. "
        f"Do you agree with his assessment? "
        f"Answer 'True' if his analysis is correct and you agree, "
        f"or 'False' if his reasoning is flawed or the conclusion is wrong. "
        f"Explain briefly why."
    )

    if prompt.news.text:
        prompt.response = (
            f"A friend talked to me about this news: '{prompt.news.title}' "
            f"with the following description: {prompt.news.text}. "
            f"{question_suffix}"
        )
    elif prompt.news.url:
        prompt.response = (
            f"A friend talked to me about this news: '{prompt.news.title}' "
            f"accessible at: {prompt.news.url}. "
            f"{question_suffix}"
        )
    else:
        prompt.response = (
            f"He replied with this statement: '{prompt.bot_output_text}'. "
            f"Is his statement correct regarding the facts? "
            f"Answer 'True' if you agree, or 'False' otherwise. Explain briefly why."
        )

class MethodChecker:
    def __init__(self, step_limit: int = 10, similarity_threshold: float = 0.8):
        self.step_limit = step_limit
        self.similarity_threshold = similarity_threshold

    def start_method(self, prompt: cl.Prompt):
        
        step = cl.Step()
        gemini = Gemini()
        deepseek = Deepseek()

        # === STEP 0: Gemini initial ===
        current_label, current_explanation = gemini.ask(prompt)
        prompt.bot_evaluation = current_label
        prompt.bot_output_text = current_explanation
        _refresh_response(prompt)

        step.chatbot_name = "Gemini"
        step.set_news_evaluation(current_label)
        step.set_chatbot_agreement(None)
        jw.write_json_to_file(step, prompt)

        print(f"[STEP 0][Gemini] Label={current_label}")
        print("Explanation:", current_explanation)
        print("-----")

        # === STEP 1: DeepSeek evaluate ===
        ds_accept, ds_eval_text = deepseek.evaluate_output(prompt)

        step.next_step()
        step.chatbot_name = "Deepseek"
        step.set_chatbot_agreement(ds_accept)
        step.set_news_evaluation(current_label if ds_accept else None)
        jw.write_json_to_file(step, prompt)

        print(f"[STEP 1][DeepSeek evaluate] Accept={ds_accept}")
        print("DeepSeek evaluation:", ds_eval_text)
        print("-----")

        if ds_accept:
            return current_label, current_explanation

        # Check limite immediato
        if step.step_num >= self.step_limit:
            print("Step limit reached after Step 1.")
            return current_label, current_explanation

        # Inizializzo variabili per il loop
        last_explanation = current_explanation
        consecutive_similar_count = 0

        # === LOOP ===
        while True:
            
            # -------------------------------------------------
            # 1. DeepSeek Rewrite
            # -------------------------------------------------
            _, ds_rewrite = deepseek.rewrite_output(prompt)
            current_explanation = ds_rewrite
            prompt.bot_output_text = current_explanation
            _refresh_response(prompt)

            # Similarity Check
            if text_similarity(current_explanation, last_explanation) > self.similarity_threshold:
                consecutive_similar_count += 1
                if consecutive_similar_count >= 1:
                    print("[STOP] DeepSeek stopped for repetition")
                    return current_label, current_explanation
            else:
                consecutive_similar_count = 0
            
            last_explanation = current_explanation 

            step.next_step()
            step.chatbot_name = "Deepseek"
            step.set_chatbot_agreement(None)
            step.set_news_evaluation(current_label)
            jw.write_json_to_file(step, prompt)
            print("[LOOP][DeepSeek rewrite]", current_explanation)
            print("-----")

            # Check Limit
            if step.step_num >= self.step_limit:
                break

            # -------------------------------------------------
            # 2. Gemini Evaluate
            # -------------------------------------------------
            g_accept, g_eval_text = gemini.evaluate_output(prompt)
            
            step.next_step()
            step.chatbot_name = "Gemini"
            step.set_chatbot_agreement(g_accept)
            step.set_news_evaluation(current_label if g_accept else None)
            jw.write_json_to_file(step, prompt)
            print(f"[LOOP][Gemini evaluate] Accept={g_accept}")
            print("Gemini evaluation:", g_eval_text)
            print("-----")

            if g_accept:
                return current_label, current_explanation
            
            # Check Limit
            if step.step_num >= self.step_limit:
                break

            # -------------------------------------------------
            # 3. Gemini Rewrite
            # -------------------------------------------------
            _, g_rewrite = gemini.rewrite_output(prompt)
            current_explanation = g_rewrite
            prompt.bot_output_text = current_explanation
            _refresh_response(prompt)

            # Similarity Check
            if text_similarity(current_explanation, last_explanation) > self.similarity_threshold:
                consecutive_similar_count += 1
                if consecutive_similar_count >= 1:
                    print("[STOP] Gemini stopped for repetition")
                    return current_label, current_explanation
            else:
                consecutive_similar_count = 0
            
            # IMPORTANTE: Aggiorniamo last_explanation
            last_explanation = current_explanation

            step.next_step()
            step.chatbot_name = "Gemini"
            step.set_chatbot_agreement(None)
            step.set_news_evaluation(current_label)
            jw.write_json_to_file(step, prompt)
            print("[LOOP][Gemini rewrite]", current_explanation)
            print("-----")

            # Check Limit
            if step.step_num >= self.step_limit:
                break

            # -------------------------------------------------
            # 4. DeepSeek Evaluate
            # -------------------------------------------------
            ds_accept, ds_eval_text = deepseek.evaluate_output(prompt)
            
            step.next_step()
            step.chatbot_name = "Deepseek"
            step.set_chatbot_agreement(ds_accept)
            step.set_news_evaluation(current_label if ds_accept else None)
            jw.write_json_to_file(step, prompt)
            print(f"[LOOP][DeepSeek evaluate] Accept={ds_accept}")
            print("DeepSeek evaluation:", ds_eval_text)
            print("-----")

            if ds_accept:
                return current_label, current_explanation

            # Check Limit
            if step.step_num >= self.step_limit:
                break

        print("Step limit reached without acceptance.")
        return current_label, current_explanation
