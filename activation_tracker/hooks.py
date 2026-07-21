"""
Forward hook management.
"""

from typing import Any, Dict

from .utils import (
    extract_tensor,
    create_activation_record,
)


class HookManager:
    """
    Manages forward hooks for activation tracking.
    """

    def __init__(self):
        self.handles = []
        self.activations: Dict[str, Dict[str, Any]] = {}

    def _hook_fn(self, layer_name):
        """
        Create a forward hook callback for a specific layer.
        """

        def hook(module, inputs, output):

            activation = extract_tensor(output)

            if activation is None:
                return

            # Performance optimization:
            # Detach from computation graph and store on CPU.
            activation = activation.detach().cpu()

            self.activations[layer_name] = {
                "layer_type": module.__class__.__name__,
                "activation": activation,
            }

        return hook

    def register_hooks(self, model):
        """
        Register forward hooks for all model layers.
        """

        # Clear previous activations before a new tracking session.
        self.activations.clear()

        for name, module in model.named_modules():

            if name == "":
                continue

            handle = module.register_forward_hook(
                self._hook_fn(name)
            )

            self.handles.append(handle)

    def remove_hooks(self):
        """
        Remove all registered forward hooks.
        """

        for handle in self.handles:
            handle.remove()

        self.handles.clear()

    def clear_activations(self):
        """
        Clear stored activation data.
        """

        self.activations.clear()

    def get_activations(self):
        """
        Return stored activations.
        """

        return self.activations