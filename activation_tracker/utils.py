"""
Utility functions for activation processing.
"""

from typing import Any, Dict, Optional

import torch


def extract_tensor(output) -> Optional[torch.Tensor]:
    """
    Extract the first tensor from a layer output.
    """

    if isinstance(output, torch.Tensor):
        return output.detach().cpu()

    if isinstance(output, (tuple, list)):
        for item in output:
            if isinstance(item, torch.Tensor):
                return item.detach().cpu()

    return None


def create_activation_record(
    layer_name: str,
    module,
    activation: torch.Tensor,
) -> Dict[str, Any]:
    """
    Create a standardized activation record.
    """

    return {
        "layer_name": layer_name,
        "layer_type": module.__class__.__name__,
        "shape": tuple(activation.shape),
        "dtype": str(activation.dtype),
        "activation": activation,
    }