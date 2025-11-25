
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
                {"role": "system", "content":
                    "You are a fact-checking assistant. Your goal is to determine whether a given news headline is true or fake based on real-world information. Answer clearly and briefly with 'True' or 'Fake' and a short explanation."
                },
                {"role": "user", "content": prompt.input}
            ],
            stream=False
        )

        text = response.choices[0].message.content
        if text is None:
            raise ValueError("No response from DeepSeek.")
        
        return evaluate_response(text), text

    def evaluate_output(self, prev_output: str):
        response = deepSeekClient.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content":
                    "Evaluate whether the following fact-checking reasoning is logically sound and factually correct. "
                    "Reply ONLY with 'Accept' or 'Reject' and a very short explanation."
                },
                {"role": "user", "content": prev_output}
            ],
            stream=False
        )

        text = response.choices[0].message.content
        if text is None:
            raise ValueError("No response from DeepSeek (evaluate_output).")

        text_lower = text.lower()
        
        if text_lower.startswith("accept"):
            return True, text
        if text_lower.startswith("reject"):
            return False, text

        raise ValueError("DeepSeek evaluate_output did not return Accept or Reject:\n" + text)

    def rewrite_output(self, prev_output: str):
        response = deepSeekClient.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content":
                    "Rewrite the following fact-checking reasoning to make it more accurate, reliable, and factual."
                },
                {"role": "user", "content":
                    f"The previous reasoning was rejected. Rewrite a better fact-checking analysis.\n\nPrevious reasoning:\n{prev_output}"
                }
            ],
            stream=False
        )

        text = response.choices[0].message.content
        if text is None:
            raise ValueError("No response from DeepSeek (rewrite_output).")

        return evaluate_response(text), text
