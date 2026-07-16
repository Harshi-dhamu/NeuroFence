"""
logger.py

Utilities for exporting activation data.
"""

from pathlib import Path
import json
import numpy as np


class ActivationLogger:
    """
    Handles exporting activation data.
    """

    @staticmethod
    def export_statistics(statistics, output_file):
        """
        Export activation statistics to JSON.
        """

        output_path = Path(output_file)

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(statistics, file, indent=4)

    @staticmethod
    def export_numpy(activations, output_directory):
        """
        Save each layer activation as a NumPy file.
        """

        output_dir = Path(output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        for layer_name, info in activations.items():

            tensor = info["activation"]

            filename = layer_name.replace(".", "_") + ".npy"

            np.save(
                output_dir / filename,
                tensor.numpy(),
            )