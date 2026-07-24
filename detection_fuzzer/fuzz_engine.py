from prompt_manager import get_all_prompts


class FuzzEngine:
    def __init__(self):
        self.prompts = []
        self.current_index = 0

    def load_prompts(self):
        self.prompts = get_all_prompts()
        self.current_index = 0

    def prepare_scan(self):
        if not self.prompts:
            self.load_prompts()

    def get_next_prompt(self):
        if self.current_index < len(self.prompts):
            prompt = self.prompts[self.current_index]
            self.current_index += 1
            return prompt
        return None

    def reset_engine(self):
        self.current_index = 0


if __name__ == "__main__":
    engine = FuzzEngine()

    engine.prepare_scan()

    print("First Prompt:")
    print(engine.get_next_prompt())

    print("\nSecond Prompt:")
    print(engine.get_next_prompt())

    engine.reset_engine()

    print("\nAfter Reset:")
    print(engine.get_next_prompt())