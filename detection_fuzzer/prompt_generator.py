import random
from prompt_manager import get_all_prompts


def generate_prompt_batch(size):
    prompts = get_all_prompts()

    all_prompts = []

    for category in prompts.values():
        all_prompts.extend(category)

    return all_prompts[:size]


def shuffle_prompts():
    prompts = get_all_prompts()
    random.shuffle(prompts)
    return prompts


def select_random_prompts(count):
    prompts = get_all_prompts()
    return random.sample(prompts, min(count, len(prompts)))


def duplicate_prompts(times):
    prompts = get_all_prompts()
    return prompts * times


if __name__ == "__main__":
    print("Batch of 5 Prompts:")
    batch = generate_prompt_batch(5)

    for prompt in batch:
        print(prompt)
