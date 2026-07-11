import random
from loader import load_prompts


def get_all_prompts():
    """Return all prompts."""
    return load_prompts()


def get_prompt_count():
    """Return total number of prompts."""
    prompts = load_prompts()
    return len(prompts) if prompts else 0


def get_random_prompt():
    """Return one random prompt."""

    prompts = load_prompts()

    if prompts:
        all_prompts = []

        for category in prompts.values():
            all_prompts.extend(category)

        return random.choice(all_prompts)

    return None


def get_prompts_by_category(category):
    """Return prompts of a specific category."""
    prompts = load_prompts()
    if prompts:
        return [p for p in prompts if p.get("category") == category]
    return []


if __name__ == "__main__":
    print("Total Prompts:", get_prompt_count())
    print("\nRandom Prompt:")
    print(get_random_prompt())

    # print("\nJailbreak Prompts:")
    # print(get_prompts_by_category("jailbreak"))