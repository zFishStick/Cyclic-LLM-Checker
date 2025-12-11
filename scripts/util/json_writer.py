
from ..classes.method_step import Step
from ..classes.prompt import Prompt

import os
import json as js

def write_json_to_file(step: Step, prompt: Prompt) -> None:
    # Always write to the project root-level json directory (not scripts/json)
    # __file__ is in scripts/util/, so we go up 3 levels to reach project root
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_dir = os.path.join(root_dir, "json")
    json_path = os.path.join(json_dir, "method_steps.json")

    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
        
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                content = f.read()
                if not content.strip():
                    with open(json_path, "w") as f:
                        f.write("[]")
            except js.JSONDecodeError:
                with open(json_path, "w") as f:
                    f.write("[]")

    if not os.path.exists(json_path):
        with open(json_path, "w") as f:
            f.write("[]")

    # Carica l'intero file come lista di notizie
    with open(json_path, "r") as f:
        try:
            data = js.load(f)
        except js.JSONDecodeError:
            data = []

    existing_entry = next((item for item in data if item["News title"] == prompt.news.title), None)

    method_step = {
        "chatbot_name": step.chatbot_name,
        "step_num": step.step_num,
        "step_evaluation_news": step.step_evaluation_news,
        "step_evaluation_chatbot": step.step_evaluation_chatbot,
        "bot_output": prompt.bot_output_text
    }

    if existing_entry:
        # Backfill is_fake if missing
        if "is_fake" not in existing_entry:
            existing_entry["is_fake"] = bool(prompt.news.fake)
        existing_entry["Steps"].append(method_step)
    else:
        new_entry = {
            "News title": prompt.news.title,
            "is_fake": bool(prompt.news.fake),
            "Steps": [method_step]
        }
        data.append(new_entry)

    with open(json_path, "w") as f:
        js.dump(data, f, indent=4)


        
