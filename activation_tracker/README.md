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
- JSON export
- NumPy export
- Visualization data preparation
- Layer activity scoring

Upcoming

- Activation comparison
- Performance optimization
- Public API