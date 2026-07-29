import json
import os
import torch


class ModelLoader:

    def __init__(self, model_dir):
        self.model_dir = os.path.abspath(model_dir)
        self.config_path = os.path.join(self.model_dir, "config.json")
        # List of supported architecture types
        self.supported_architectures = [
            "llama",
            "gpt2",
            "bert",
            "mistral",
            "phi",
        ]

    def check_compatibility(self) -> dict:
        """Analyzes the model config to determine system hardware & architecture compatibility."""
        report = {
            "is_compatible": True,
            "architecture_supported": False,
            "dtype_supported": True,
            "model_type": "Unknown",
            "torch_dtype": "Unknown",
            "issues": [],
        }

        # 1. Verify config.json exists
        if not os.path.exists(self.config_path):
            report["is_compatible"] = False
            report["issues"].append("config.json not found in model directory.")
            return report

        # 2. Read config metadata
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            report["is_compatible"] = False
            report["issues"].append(f"Failed to parse config.json: {str(e)}")
            return report

        # 3. Check Architecture
        model_type = config.get("model_type", "").lower()
        report["model_type"] = model_type

        if model_type in self.supported_architectures:
            report["architecture_supported"] = True
        else:
            report["is_compatible"] = False
            report["issues"].append(
                f"Architecture '{model_type}' is not supported. Supported: {self.supported_architectures}"
            )

        # 4. Check Data Type / Hardware Compatibility
        torch_dtype = config.get("torch_dtype", "float32")
        report["torch_dtype"] = torch_dtype

        # e.g., bfloat16 requires CUDA or CPU with AVX-512 / modern PyTorch support
        if (
            "bfloat16" in str(torch_dtype).lower()
            and not torch.cuda.is_bf16_supported()
        ):
            report["dtype_supported"] = False
            report["issues"].append(
                "Warning: bfloat16 is requested but not optimally supported on this hardware."
            )

        return report