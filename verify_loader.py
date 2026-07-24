"""
verify_loader.py - Real-World End-to-End Integration Tester
Generates simulated local model states to strictly execute and test
the multi-stage validation engine, memory calculation matrix, and logging channels.
"""

import os
import json
import shutil
from model_loader.core import ModelLoader

def create_mock_model(model_dir: str, include_tokenizer: bool = True, break_config: bool = False):
    """Helper method to provision a mock local Hugging Face folder structure."""
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)
    os.makedirs(model_dir, exist_ok=True)

    # 1. Generate config.json payload
    config_data = {
        "architectures": ["LlamaForCausalLM"],
        "model_type": "llama",
        "vocab_size": 32000,
        "hidden_size": 4096,
        "num_hidden_layers": 32,
        "num_attention_heads": 32,
        "intermediate_size": 11008
    }
    
    # Simulate a corrupted configuration file missing crucial keys if requested
    if break_config:
        config_data.pop("hidden_size")
        config_data.pop("num_hidden_layers")

    with open(os.path.join(model_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    # 2. Generate tokenizer infrastructure files
    if include_tokenizer:
        tokenizer_config = {"tokenizer_class": "LlamaTokenizer", "model_max_length": 2048}
        with open(os.path.join(model_dir, "tokenizer_config.json"), "w", encoding="utf-8") as f:
            json.dump(tokenizer_config, f, indent=2)
        
        with open(os.path.join(model_dir, "tokenizer.json"), "w", encoding="utf-8") as f:
            f.write('{"mock_matrix": "token_embeddings"}')

    # 3. Generate mock weight splits (simulating non-empty weights)
    with open(os.path.join(model_dir, "model-00001-of-00002.safetensors"), "wb") as f:
        f.write(b"MOCK_WEIGHTS_PART_A_" * 1024)  # Small dummy non-empty byte stream
    with open(os.path.join(model_dir, "model-00002-of-00002.safetensors"), "wb") as f:
        f.write(b"MOCK_WEIGHTS_PART_B_" * 1024)

def run_integration_suite():
    """Orchestrates test vectors against the validation engine."""
    print("=" * 60)
    print("NEUROFENCE MODEL LOADER INTEGRATION SUITE")
    print("=" * 60)

    good_model_path = "mock_llama_7b_valid"
    bad_model_path = "mock_llama_7b_corrupted"

    try:
        # ---- TEST CASE 1: VALID LLM RUNTIME PROFILE ----
        print("\n[+] Test Case 1: Processing a structurally valid local model...")
        create_mock_model(good_model_path, include_tokenizer=True, break_config=False)
        
        loader = ModelLoader(good_model_path)
        
        # Execute validation lifecycle
        is_valid = loader.validate_weights()
        print(f" -> Validation Status: {'PASSED' if is_valid else 'FAILED'}")
        
        # Extract telemetry summary generated in Day 9
        summary = loader.generate_model_summary()
        print(f" -> Architecture Identity: {summary['architecture_details']['architecture']}")
        print(f" -> Estimated Parameters: {summary['tensor_properties']['parameter_count_b']} Billion")
        print(f" -> Project Runtime Memory (FP16): {summary['hardware_projections']['fp16_precision_gb']} GB")
        
        # Execute secure loading sandbox payload
        load_result = loader.load_safely()
        print(f" -> Sandbox Mounting Isolation: {load_result['status']}")

        # ---- TEST CASE 2: CORRUPTED STRUCTURAL LAYOUT ----
        print("\n[+] Test Case 2: Processing an invalid/corrupted structural model...")
        create_mock_model(bad_model_path, include_tokenizer=True, break_config=True)
        
        bad_loader = ModelLoader(bad_model_path)
        is_bad_valid = bad_loader.validate_weights()
        print(f" -> Validation Status: {'PASSED' if is_bad_valid else 'FAILED'}")
        
        bad_load_result = bad_loader.load_safely()
        print(f" -> Sandbox Mounting Isolation: {bad_load_result['status']} (Message: {bad_load_result['message']})")

        # ---- LOG INTERROGATION ----
        print("\n[+] Checking persistent audit trail ('loader.log')...")
        if os.path.exists("loader.log"):
            print(" -> 'loader.log' successfully generated. Last 5 lines of audit history:")
            print("-" * 60)
            with open("loader.log", "r", encoding="utf-8") as log_file:
                lines = log_file.readlines()
                for line in lines[-5:]:
                    print(line.strip())
            print("-" * 60)
        else:
            print(" -> [ERROR] Trace log file 'loader.log' was not created.")

    finally:
        # Cleanup mock temporary filesystem tracks
        print("\n[+] Deleting temporary mock directories...")
        for path in [good_model_path, bad_model_path]:
            if os.path.exists(path):
                shutil.rmtree(path)
        print("[+] Integration testing suite terminated cleanly.")

if __name__ == "__main__":
    run_integration_suite()