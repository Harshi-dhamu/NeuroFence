# Activation Tracker

Assigned Member: Akhina

This module is responsible for:

* Monitoring neuron activations
* Recording intermediate outputs
* Logging suspicious behavior

---

## Purpose

The Activation Tracker captures intermediate neural network activations during model inference. These activations can later be analyzed to identify unusual behavior, potential weight poisoning, or backdoor patterns.

## Responsibilities

* Register forward hooks
* Capture layer outputs
* Store activations
* Provide activation statistics
* Support anomaly detection modules

## Module Structure

```text
activation_tracker/
├── README.md
├── tracker.py
├── hooks.py
├── analyzer.py
├── utils.py
└── __init__.py
```

## Current Status

Implemented

- Package structure
- Forward hook registration
- Activation extraction
- Layer-wise activation storage
- Activation statistics
- Dormant neuron activity analysis
- Activation logger
- JSON export## Current Status

Completed

- Package structure
- Forward hook registration
- Activation extraction
- Layer-wise activation storage
- Activation statistics
- Dormant neuron activity analysis
- Activation logger
- JSON export
- NumPy export
- Visualization data preparation
- Layer activity scoring
- Activation comparison
- Comparison reporting
- Performance optimization
- Public API
- Tracker state management
- Single-call activation tracking
- Documentation

Status: ✅ Module Complete

## Public API

The `ActivationTracker` class provides the following methods:

- start_tracking()
- stop_tracking()
- track_activation(input_tensor)
- get_activations()
- get_activation_count()
- get_statistics()
- analyze_neuron_activity()
- get_layer_summary()
- get_neuron_data()
- get_heatmap_data()
- get_layer_scores()
- compare_with()
- generate_comparison_report()
- export_json()
- export_numpy()
- export_all()
- reset_tracker()
- is_tracking()


## Example

```python
import torch
import torch.nn as nn

from activation_tracker import ActivationTracker

model = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 2),
)

tracker = ActivationTracker(model)

tracker.track_activation(torch.randn(1, 4))

print(tracker.get_statistics())
```

## Integration

This module is designed to integrate with:

- Model Loader
- Detection Engine
- Reporting Module
- Desktop UI