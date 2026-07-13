"""
hooks.py

Forward hook management for capturing intermediate activations.
"""

from typing import Dict, Any

import torch
import torch.nn as nn


class HookManager:
    """
    Registers forward hooks on selected neural network layers.
    """

    SUPPORTED_LAYERS = (
        nn.Linear,
        nn.Conv1d,
        nn.Conv2d,
        nn.Conv3d,
        nn.ReLU,
        nn.GELU,
        nn.Sigmoid,
        nn.Tanh,
        nn.BatchNorm1d,
        nn.BatchNorm2d,
        nn.LayerNorm,
    )

    def __init__(self):
        self.handles = []
        self.activations: Dict[str, Dict[str, Any]] = {}

    def _hook_fn(self, layer_name: str):
        """
        Create a hook function for a specific layer.
        """

        def hook(module, inputs, output):
            if not isinstance(output, torch.Tensor):
                return

            self.activations[layer_name] = {
                "layer_type": module.__class__.__name__,
                "shape": tuple(output.shape),
                "dtype": str(output.dtype),
                "activation": output.detach().cpu(),
            }

        return hook

    def register_hooks(self, model):
        """
        Register hooks only on supported layer types.
        """

        self.activations.clear()

        for name, module in model.named_modules():
            if name == "":
                continue

            if isinstance(module, self.SUPPORTED_LAYERS):
                handle = module.register_forward_hook(
                    self._hook_fn(name)
                )
                self.handles.append(handle)

    def remove_hooks(self):
        """
        Remove all registered hooks.
        """

        for handle in self.handles:
            handle.remove()

        self.handles.clear()