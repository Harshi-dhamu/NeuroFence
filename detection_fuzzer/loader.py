import json
import os


def load_prompts():
    """
    Load prompts from prompts/prompts.json
    Returns a Python dictionary containing all prompts.
    """

    try:
        current_dir = os.path.dirname(__file__)
        prompt_file = os.path.join(current_dir, "prompts", "prompts.json")

        with open(prompt_file, "r", encoding="utf-8") as file:
            prompts = json.load(file)

        return prompts

    except FileNotFoundError:
        print("Error: prompts.json file not found.")
        return None

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None


if __name__ == "__main__":
    data = load_prompts()

    if data:
        print("Prompts loaded successfully!")
        print(data)