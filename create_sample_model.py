"""
create_sample_model.py - Generates a valid sample Hugging Face model directory 
for Day 13 Integration Testing.
"""

import os
import json


def create_valid_model_directory(directory_name="sample_valid_llama"):
    """Creates a mock model folder with valid config, tokenizer, and weight files."""
    model_dir = os.path.abspath(directory_name)
    os.makedirs(model_dir, exist_ok=True)

    # 1. Valid config.json with all required hyperparameter keys
    config_data = {
        "architectures": ["LlamaForCausalLM"],
        "model_type": "llama",
        "vocab_size": 32000,
        "hidden_size": 4096,
        "intermediate_size": 11008,
        "num_hidden_layers": 32,
        "num_attention_heads": 32,
        "torch_dtype": "float16",
    }
    with open(
        os.path.join(model_dir, "config.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(config_data, f, indent=2)

    # 2. Valid tokenizer_config.json
    tokenizer_config = {
        "tokenizer_class": "LlamaTokenizer",
        "bos_token": "<s>",
        "eos_token": "</s>",
        "unk_token": "<unk>",
    }
    with open(
        os.path.join(model_dir, "tokenizer_config.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(tokenizer_config, f, indent=2)

    # 3. Valid tokenizer.json vocabulary file
    tokenizer_data = {
        "version": "1.0",
        "truncation": None,
        "padding": None,
        "added_tokens": [],
        "normalizer": None,
        "model": {"type": "BPE", "vocab": {"<s>": 0, "</s>": 1, "<unk>": 2}},
    }
    with open(
        os.path.join(model_dir, "tokenizer.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(tokenizer_data, f, indent=2)

    # 4. Binary dummy weight file (Safetensors format)
    safetensors_path = os.path.join(
        model_dir, "model-00001-of-00001.safetensors"
    )
    with open(safetensors_path, "wb") as f:
        f.write(b"SIMULATED_HEADER_AND_TENSOR_DATA_FOR_NEUROFENCE_TESTING" * 100)

    print(f"\n[+] Successfully created sample model at: {model_dir}")
    print("    Contains: config.json, tokenizer_config.json, tokenizer.json, model-00001-of-00001.safetensors")


if __name__ == "__main__":
    create_valid_model_directory()