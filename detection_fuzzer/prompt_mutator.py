import random
import base64


def add_prefix(prompt, prefix="[TEST] "):
    return prefix + prompt


def add_suffix(prompt, suffix=" [END]"):
    return prompt + suffix


def encode_prompt(prompt):
    return base64.b64encode(prompt.encode()).decode()


def random_mutation(prompt):
    mutations = [
        lambda p: add_prefix(p),
        lambda p: add_suffix(p),
        lambda p: p.upper(),
        lambda p: p.lower(),
        lambda p: encode_prompt(p)
    ]
    return random.choice(mutations)(prompt)
if __name__ == "__main__":
    sample_prompt = "What is Artificial Intelligence?"

    print("Original Prompt:")
    print(sample_prompt)

    print("\nWith Prefix:")
    print(add_prefix(sample_prompt))

    print("\nWith Suffix:")
    print(add_suffix(sample_prompt))

    print("\nEncoded Prompt:")
    print(encode_prompt(sample_prompt))

    print("\nRandom Mutation:")
    print(random_mutation(sample_prompt))