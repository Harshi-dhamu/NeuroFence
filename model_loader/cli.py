"""
cli.py - Command-Line Interface for NeuroFence Model Loader
Provides terminal-accessible auditing, validation, and footprint analysis commands.
"""

import argparse
import sys
import os
import json
from .core import ModelLoader


def render_summary_dashboard(summary: dict) -> None:
    """Formats and prints the model inspection report directly to stdout."""
    identity = summary.get("model_identity", {})
    arch = summary.get("architecture_details", {})
    tensors = summary.get("tensor_properties", {})
    tokenizer = summary.get("tokenizer_properties", {})
    security = summary.get("security_status", {})
    hardware = summary.get("hardware_projections", {})

    print("\n" + "=" * 65)
    print(f" NEUROFENCE MODEL AUDIT REPORT: {identity.get('name', 'Unknown')}")
    print("=" * 65)
    
    print("\n [1] ARCHITECTURE & STORAGE")
    print(f"  -> Path         : {identity.get('local_path')}")
    print(f"  -> Architecture : {arch.get('architecture')}")
    print(f"  -> Layers       : {arch.get('layers_count')}")
    print(f"  -> Hidden Size  : {arch.get('hidden_size')}")
    print(f"  -> Format       : {tensors.get('framework')}")
    print(f"  -> Parameters   : {tensors.get('parameter_count_b')} Billion")
    print(f"  -> Disk Size    : {tensors.get('disk_storage_gb')} GB")

    print("\n [2] TOKENIZER PROPERTIES")
    print(f"  -> Config Found : {tokenizer.get('has_tokenizer_config')}")
    print(f"  -> Class        : {tokenizer.get('tokenizer_class')}")
    print(f"  -> Vocab Size   : {tokenizer.get('vocabulary_size')}")

    print("\n [3] SECURITY & INTEGRITY CHECKS")
    checks = security.get("checks_passed", {})
    for check, passed in checks.items():
        status_icon = "[✔] PASS" if passed else "[✘] FAIL"
        print(f"  -> {check:<20} : {status_icon}")
    
    overall_status = "[✔] VALIDATED" if security.get("is_structurally_validated") else "[✘] UNVALIDATED"
    print(f"  -> Overall Status    : {overall_status}")

    print("\n [4] HARDWARE MEMORY PROJECTIONS (VRAM/RAM)")
    print(f"  -> FP32 Precision    : {hardware.get('fp32_precision_gb', 0.0):>6.2f} GB")
    print(f"  -> FP16 Precision    : {hardware.get('fp16_precision_gb', 0.0):>6.2f} GB")
    print(f"  -> INT8 Quantized    : {hardware.get('int8_quantized_gb', 0.0):>6.2f} GB")
    print(f"  -> INT4 Quantized    : {hardware.get('int4_quantized_gb', 0.0):>6.2f} GB")
    print("=" * 65 + "\n")


def main():
    """Main CLI entrypoint parser."""
    parser = argparse.ArgumentParser(
        prog="neurofence",
        description="NeuroFence: Safe local Hugging Face model verification and profiling toolkit."
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'scan' command
    scan_parser = subparsers.add_parser("scan", help="Scan and audit a local model directory.")
    scan_parser.add_argument("model_path", type=str, help="Path to the target Hugging Face model directory.")
    scan_parser.add_argument("--json", action="store_true", help="Output audit summary as raw JSON.")

    args = parser.parse_args()

    if args.command == "scan":
        target_path = os.path.abspath(args.model_path)
        loader = ModelLoader(target_path)
        loader.validate_weights()
        summary = loader.generate_model_summary()

        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            render_summary_dashboard(summary)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()