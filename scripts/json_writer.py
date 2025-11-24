import json as js
import os

from classes.method_step import Step
from classes.prompt import Prompt

import os
import json as js

def write_json_to_file(step: Step, prompt: Prompt) -> None:
    json_dir = "json"
    json_path = os.path.join(json_dir, "method_steps.json")

    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
        with open(json_path, "w") as f:
            f.write("{}")

    with open(json_path, "r") as f:
        try:
            data = js.load(f)
        except js.JSONDecodeError:
            data = {}

    method_step = {
        "News title": prompt.news.title,
        "chatbot_name": step.chatbot_name,
        "step_num": step.step_num,
        "step_evaluation": step.step_evaluation,
        "bot_output": prompt.bot_output_text
    }
    
    key = prompt.news.title

    if key in data:
        if not isinstance(data[key], list):
            data[key] = [data[key]]
        data[key].append(method_step)
    else:
        data[key] = [method_step]

    with open(json_path, "w") as f:
        js.dump(data, f, indent=4)

        
