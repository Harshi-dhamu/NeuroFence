from model_loader.core import ModelLoader


class ModelService:
    def __init__(self):
        self.loader = None

    def load_model(self, model_path):
        self.loader = ModelLoader(model_path=model_path)

        return self.loader.load_safely()

    def validate_model(self):
        if not self.loader:
            raise RuntimeError("Model not loaded")

        return self.loader.validate_weights()

    def get_model_info(self):
        if not self.loader:
            raise RuntimeError("Model not loaded")

        return self.loader.get_model_info()