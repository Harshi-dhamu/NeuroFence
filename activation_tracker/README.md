# Activation Tracker

**Assigned Member:** Akhina

The Activation Tracker module is responsible for:

- Monitoring neuron activations
- Recording intermediate neural network outputs
- Analyzing neuron activity
- Detecting potentially unusual activation behavior
- Preparing activation data for visualization
- Providing activation metrics for integration with other modules

---

## Purpose

The Activation Tracker captures intermediate neural network activations during model inference.

The captured activations can be analyzed to identify:

- Unusual neuron activity
- Dormant neurons
- Activation changes between inputs
- Potential anomalous behavior
- Possible weight poisoning or backdoor-related patterns

The module uses PyTorch forward hooks to capture intermediate layer outputs without modifying the model architecture.

---

## Responsibilities

- Register forward hooks
- Capture layer outputs
- Store activations
- Calculate activation statistics
- Analyze neuron activity
- Detect anomalous activation behavior
- Rank layers based on activity
- Generate heatmap-ready data
- Track activation history
- Analyze activation trends
- Filter layers
- Generate dashboard metrics
- Compare activation outputs
- Export activation statistics and data

---

## Module Structure

```text
activation_tracker/
├── README.md
├── tracker.py
├── hooks.py
├── analyzer.py
├── logger.py
├── utils.py
└── __init__.py

---

## Current Status

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
    - Normalized heatmap data
    - Layer activity scoring
    - Layer activity ranking
    - Activation comparison
    - Comparison reporting
    - Activation history tracking
    - Dead neuron analysis
    - Anomaly severity classification
    - Activation trend analysis
    - Layer filtering
    - Dashboard metrics
    - Tracker state management
    - Duplicate tracking protection
    - Single-call activation tracking
    - Public API
    - Documentation and integration examples

Status: ✅ Module Complete


## Dependencies

The Activation Tracker requires:
    - Python
    - PyTorch

The module operates on PyTorch models and tensors.

## Public API

The main class exposed by the module is:

            from activation_tracker import ActivationTracker

The ActivationTracker class provides the following interfaces.

---

## Core Integration APIs

These are the primary interfaces intended for integration with the rest of the NeuroFence application.

track_activation(input_tensor)

Performs a model forward pass while tracking intermediate activations.

Input:
    input_tensor

A PyTorch tensor compatible with the model's expected input.

Example:
    activations = tracker.track_activation(input_tensor)

Return:
    A dictionary containing activation information for tracked layers.

Example:

    {
        "0": {
            "layer_name": "0",
            "layer_type": "Linear",
            "shape": (1, 8),
            "dtype": "torch.float32",
            "activation": tensor(...)
        }
    }

get_statistics()

    Returns statistical information for the tracked activations.

Example:
    statistics = tracker.get_statistics()

Example return:

    {
        "0": {
            "layer_type": "Linear",
            "shape": (1, 8),
            "mean": 0.21,
            "variance": 0.34,
            "maximum": 1.52,
            "minimum": -1.21
        }
    }


detect_anomalies(threshold=1e-5)
Analyzes tracked activations to identify potentially unusual neuron activity.

Example:
    anomalies = tracker.detect_anomalies()

The returned dictionary contains layer-level activation and anomaly-related information.



## Activation Analysis APIs

analyze_neuron_activity(threshold=1e-5)
Analyzes active and dormant neurons for each tracked layer.

Example:
    activity = tracker.analyze_neuron_activity()

Example return:
    {
        "0": {
            "layer_type": "Linear",
            "total_neurons": 8,
            "active_neurons": 8,
            "dormant_neurons": 0,
            "activation_frequency": 1.0,
            "dormant_ratio": 0.0,
            "threshold": 1e-5
        }
    }

analyze_dead_neurons(threshold=1e-5)
Analyzes neurons that show little or no activation.

Example:
    dead_neurons = tracker.analyze_dead_neurons()

classify_anomaly_severity(threshold=1e-5)
    Classifies activation behavior into severity levels.

Example:
    severity = tracker.classify_anomaly_severity()

Possible severity levels include:
    -Normal
    -Low
    -Medium
    -High

get_layer_scores(threshold=1e-5)
    Calculates activity-related scores for each tracked layer.

    Example:
        scores = tracker.get_layer_scores()

rank_layers(threshold=1e-5)
    Ranks tracked layers according to their activity.

    Example:
        ranking = tracker.rank_layers()

    Example return:

    [
        {
            "layer_name": "0",
            "layer_type": "Linear",
            "activity_score": 1.0,
            "active_neurons": 8,
            "dormant_neurons": 0
        }
    ]




##  Visualization APIs

get_layer_summary()
    -Returns summary information for each tracked layer.

        summary = tracker.get_layer_summary()


get_neuron_data()
    -Returns neuron activation values prepared for visualization.

        neuron_data = tracker.get_neuron_data()


get_heatmap_data()
    -Returns activation data prepared for heatmap visualization.

        heatmap_data = tracker.get_heatmap_data()


get_normalized_heatmap_data()
    -Returns normalized activation data suitable for visualization.

        heatmap_data = tracker.get_normalized_heatmap_data()




## History and Trend Analysis

get_activation_history()
    -Returns stored activation history.

        history = tracker.get_activation_history()


analyze_activation_trends()
    -Analyzes activation changes across multiple inference runs.

        trends = tracker.analyze_activation_trends()

    Example:
        {
            "0": {
                "activity_scores": [1.0, 1.0, 1.0],
                "initial_activity": 1.0,
                "final_activity": 1.0,
                "change": 0.0,
                "trend": "stable"
            }
        }




## Layer Filtering

filter_layers(layer_names=None, layer_type=None)

Filters tracked activation data by layer name or layer type.

Filter by layer name:

        filtered = tracker.filter_layers(
            layer_names=["0", "2"]
        )

Filter by layer type:

        filtered = tracker.filter_layers(
            layer_type="Linear"
        )



##  Dashboard Integration

get_dashboard_metrics(threshold=1e-5)
    -Returns summary metrics for dashboard integration.

    Example:
        dashboard_metrics = tracker.get_dashboard_metrics()

    Example return:
        {
            "total_layers": 3,
            "total_neurons": 18,
            "active_neurons": 15,
            "dormant_neurons": 3,
            "overall_activity": 0.83,
            "overall_dormant_ratio": 0.17
        }

These metrics can be passed directly to the desktop Dashboard or IntegrationController.



## Activation Comparison

compare_with(other_activations)
    -Compares the current activation set with another activation set.

        comparison = tracker.compare_with(
            other_activations
        )

generate_comparison_report(other_activations)
    -Generates a summary report from activation comparison results.

        report = tracker.generate_comparison_report(
            other_activations
        )



## Tracker State Management

start_tracking()
    -Starts activation tracking and registers forward hooks.

        tracker.start_tracking()

stop_tracking()
    -Stops tracking and removes registered forward hooks.

            tracker.stop_tracking()

is_tracking()
    -Returns whether activation tracking is currently enabled.

            tracking = tracker.is_tracking()

        Example:
            True
            or:
            False

reset_tracker()
    -Clears stored activation data.

        tracker.reset_tracker()


get_activations()
    -Returns the currently stored activation data.

        activations = tracker.get_activations()

get_activation_count()
    -Returns the number of tracked layers.

        count = tracker.get_activation_count()

    Example:
        3



## Export APIs

export_statistics(output_file)
    -Exports activation statistics to JSON.

            tracker.export_statistics(
                "statistics.json"
            )

export_json(output_file)
    -Exports activation statistics to JSON.

            tracker.export_json(
                "statistics.json"
            )

export_numpy(output_directory)
    -Exports activation tensors as NumPy files.

            tracker.export_numpy(
                "activations"
            )


export_all(folder="activations")
    -Exports supported activation data formats.

            tracker.export_all(
                "activations"
            )



##  Integration Example

The Activation Tracker can be integrated into the NeuroFence application as follows:

        import torch
        from activation_tracker import ActivationTracker

        tracker = ActivationTracker(model)

        # Track model activations
        activations = tracker.track_activation(
            input_tensor
        )

        # Get activation statistics
        statistics = tracker.get_statistics()


        # Analyze neuron activity
        neuron_activity = tracker.analyze_neuron_activity()


        # Detect unusual activation behavior
        anomalies = tracker.detect_anomalies()


        # Get dashboard metrics
        dashboard_metrics = tracker.get_dashboard_metrics()

The returned dictionaries can be passed to the IntegrationController, Detection Engine, Dashboard, Reporting, History, and Export components.

Example Model

    A simple PyTorch model can be used to test the Activation Tracker:
            import torch
            import torch.nn as nn

            from activation_tracker import ActivationTracker


            model = nn.Sequential(
                nn.Linear(4, 8),
                nn.ReLU(),
                nn.Linear(8, 2),
            )


            tracker = ActivationTracker(model)


            input_tensor = torch.randn(1, 4)


            activations = tracker.track_activation(
                input_tensor
            )


            print(tracker.get_statistics())
            print(tracker.analyze_neuron_activity())
            print(tracker.get_dashboard_metrics())




## Error and Edge-Case Handling

The tracker has been tested for the following cases:

        -Empty activation data
        -Resetting the tracker
        -Stopping tracking before starting
        -Starting tracking multiple times
        -Empty layer filtering
        -Models with layers that do not return tensors
        -Activation tensors stored after detaching from the computation graph

Repeated calls to start_tracking() are protected against duplicate hook registration.

Activation tensors are detached from the computation graph and moved to CPU memory before being stored for analysis.


## Integration Notes

    The Activation Tracker does not require the desktop UI or IntegrationController to access its internal implementation.

The recommended integration points are:

        tracker.track_activation(input_tensor)
        tracker.get_statistics()
        tracker.detect_anomalies()

Additional analysis APIs can be used when required:

        tracker.analyze_neuron_activity()
        tracker.rank_layers()
        tracker.get_heatmap_data()
        tracker.analyze_activation_trends()
        tracker.get_dashboard_metrics()

## Module Status

    Activation Tracker: ✅ Complete
        -Phase 1: ✅ Complete
        -Phase 2: ✅ Complete
