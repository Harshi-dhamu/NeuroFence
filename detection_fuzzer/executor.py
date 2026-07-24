from loader import load_prompts


def execute_prompts():
    """
    Simulates running prompts and storing responses.
    """

    prompts = load_prompts()

    if not prompts:
        print("No prompts found.")
        return

    responses = []

    for category, prompt_list in prompts.items():
        if isinstance(prompt_list, list):
            for prompt in prompt_list:
                response = f"Executed: {prompt}"

                responses.append({
                    "category": category,
                    "prompt": prompt,
                    "response": response
                })

                print(f"[LOG] {category}: {prompt}")

    print("\nExecution completed.")
    return responses


if __name__ == "__main__":
    results = execute_prompts()

    print("\nResponses:")
    print(results)