# NeuroFence - Model Loader Module

The `ModelLoader` module in NeuroFence provides a secure, robust pipeline for verifying, analyzing, and staging Large Language Models (LLMs) before execution. It ensures model files are valid, uncorrupted, safely sharded, and fit within available GPU/CPU memory bounds.

---

## Key Features

1. **Model Compatibility Analysis**
   * Validates structure and critical configuration keys (`hidden_size`, `num_hidden_layers`, `vocab_size`).
   * Estimates model parameter counts dynamically based on model architecture dimensions.

2. **Memory Projection Calculations**
   * Estimates memory consumption across multiple precisions (`float32`, `float16`, `bfloat16`, `int8`, `int4`).
   * Factors in memory overhead multipliers (default: `1.2x`) to predict total required VRAM/RAM.

3. **Corrupted Model Detection**
   * Scans model directories for missing, unreadable, zero-byte, or malformed configuration JSON files (`.safetensors`, `.bin`, `.pt`, `.json`, `.gguf`).

4. **Performance Metrics Tracking**
   * Tracks execution latency for directory scanning, configuration verification, and staging steps in milliseconds (`ms`).

5. **Large Model & Sharding Support**
   * Automatically detects sharded weights (e.g., `model-00001-of-00002.safetensors`) and computes shard counts.

6. **Validation Report Export**
   * Exports full model health, memory projections, and verification reports into structured JSON files.

7. **Metadata Caching**
   * Maintains an in-memory metadata cache to skip redundant disk scans when repeatedly querying the same model path.

8. **Resilient Edge-Case Handling**
   * Gracefully handles `None` paths, invalid non-dictionary configurations, missing files, and negative parameter inputs.

---

## Basic Usage Examples

### 1. Initializing and Scanning a Model Directory

```python
from model_loader.core import ModelLoader

# Initialize loader with target model directory
loader = ModelLoader("/path/to/llama-3-8b")

# Perform directory validation and caching scan
is_valid = loader.scan_model_directory()

if is_valid:
    print("Model directory validated successfully.")
else:
    print(f"Validation failed. Corrupted files: {loader.corrupted_files}")

# Populate raw configuration data
loader.metadata["raw_config"] = {
    "hidden_size": 4096,
    "num_hidden_layers": 32,
    "vocab_size": 32000,
    "intermediate_size": 11008
}

# Verify critical keys exist
if loader.verify_config_keys():
    # Calculate parameter estimation (~6.61B)
    params_b = loader.estimate_parameter_count()
    
    # Calculate memory requirements for float16
    memory_info = loader.get_memory_projection(precision="float16")
    print(f"Estimated Parameters: {params_b}B")
    print(f"Estimated VRAM Required: {memory_info['estimated_total_gb']} GB")

# Export report to JSON for audit logs
success = loader.export_validation_report("model_validation_summary.json")

# Retrieve tracked performance metrics
metrics = loader.get_performance_metrics()
print(f"Total scan & validation time: {metrics['total_execution_time_ms']} ms")