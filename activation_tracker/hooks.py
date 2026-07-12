"""
hooks.py

Forward hook management for capturing intermediate activations.
"""

from typing import Dict, Any
import torch


class HookManager:
    """
    Registers forward hooks on model layers and stores activations.
    """

    def __init__(self):
        self.handles = []
        self.activations: Dict[str, Any] = {}

    def _hook_fn(self, layer_name):
        """
        Returns a hook function for a specific layer.
        """

        def hook(module, inputs, output):
            if isinstance(output, torch.Tensor):
                self.activations[layer_name] = output.detach().cpu()

        return hook

    def register_hooks(self, model):
        """
        Register forward hooks on supported layers.
        """

        self.activations.clear()

        for name, module in model.named_modules():
            # Skip the top-level model itself
            if name == "":
                continue

            handle = module.register_forward_hook(
                self._hook_fn(name)
            )
            self.handles.append(handle)

    def remove_hooks(self):
        """
        Remove every registered hook.
        """

        for handle in self.handles:
            handle.remove()

        self.handles.clear()