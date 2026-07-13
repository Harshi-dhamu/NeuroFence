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
        Forward hook callback.
        """

        def hook(module, inputs, output):

            activation = extract_tensor(output)

            if activation is None:
                return

            self.activations[layer_name] = create_activation_record(
                layer_name=layer_name,
                module=module,
                activation=activation,
            )

        return hook

    def register_hooks(self, model):

        self.activations.clear()

        for name, module in model.named_modules():

            if name == "":
                continue

            handle = module.register_forward_hook(
                self._hook_fn(name)
            )

            self.handles.append(handle)

    def remove_hooks(self):

        for handle in self.handles:
            handle.remove()

        self.handles.clear()