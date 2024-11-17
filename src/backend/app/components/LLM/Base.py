class BaseLLMComponent:
    def __init__(self):
        self.model_instance = None

    def build(self, **kwargs):
        raise NotImplementedError("You need to implement the build method.")

    def run(self, prompt):
        if self.model_instance is None:
            raise ValueError("LLM is not initialized. Call the build method first.")
        return self.model_instance(prompt)