
from scripts.json_writer import write_json_to_file


def test_write_json_to_file():
    data = {
        "name": "Test Chatbot",
        "steps": [
            {"step": 1, "evaluation": "True"},
            {"step": 2, "evaluation": "False"}
        ]
    }
    write_json_to_file(data)