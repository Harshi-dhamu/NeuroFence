"""
test_loader.py - Automated Testing Suite for NeuroFence ModelLoader
Validates metadata calculations, configuration validation rules, 
memory profiling matrices, corrupted file detection, and performance tracking.
"""

import unittest
from unittest.mock import MagicMock, patch

from model_loader.core import ModelLoader

# Safely import SandboxSecurityError or define a fallback to keep tests robust
try:
    from model_loader.sandbox import SandboxSecurityError
except ImportError:

    class SandboxSecurityError(Exception):
        pass


class TestModelLoaderSuite(unittest.TestCase):
    """Encapsulates unit tests targeting the verification and staging pipeline."""

    def setUp(self):
        """Initializes a base ModelLoader instance pointed to a dummy directory path."""
        self.dummy_path = "/mock/path/to/llm-model"
        self.loader = ModelLoader(self.dummy_path)

    @patch("model_loader.core.check_directory_exists")
    def test_scan_directory_failure(self, mock_exists):
        """Ensures scanning gracefully aborts and returns False if the path does not exist."""
        mock_exists.return_value = False
        result = self.loader.scan_model_directory()
        self.assertFalse(result)
        self.assertFalse(self.loader.is_validated)

    def test_verify_config_keys_missing(self):
        """Validates that configuration verification fails if critical parameters are absent."""
        self.loader.metadata["raw_config"] = {
            "model_type": "llama",
            "vocab_size": 32000
            # Missing hidden_size and num_hidden_layers
        }
        result = self.loader.verify_config_keys()
        self.assertFalse(result)
        self.assertFalse(
            self.loader.metadata["verification_report"]["config_verified"]
        )

    def test_verify_config_keys_success(self):
        """Validates that configuration verification succeeds when all required keys are present."""
        self.loader.metadata["raw_config"] = {
            "model_type": "llama",
            "vocab_size": 32000,
            "hidden_size": 4096,
            "num_hidden_layers": 32,
        }
        result = self.loader.verify_config_keys()
        self.assertTrue(result)
        self.assertTrue(
            self.loader.metadata["verification_report"]["config_verified"]
        )

    def test_estimate_parameter_count_math(self):
        """Verifies dimension calculations map accurately for parameter estimation."""
        self.loader.metadata["raw_config"] = {
            "vocab_size": 32000,
            "hidden_size": 4096,
            "num_hidden_layers": 32,
            "intermediate_size": 11008,
        }
        # Math verification target: ~6.61 Billion
        estimated_b = self.loader.estimate_parameter_count()
        self.assertEqual(estimated_b, 6.61)

    @patch("model_loader.core.SandboxEnvironment")
    def test_load_safely_sandbox_security_breach(self, mock_sandbox_class):
        """Validates that runtime execution errors translate to an Intercepted summary profile."""
        self.loader.is_validated = True

        mock_sandbox_instance = MagicMock()
        mock_sandbox_instance.initialize_sandbox.return_value = True
        mock_sandbox_instance.execute_safely.side_effect = (
            SandboxSecurityError("Unsafe op detected")
        )
        mock_sandbox_class.return_value = mock_sandbox_instance

        response = self.loader.load_safely()
        self.assertEqual(response["status"], "Intercepted")

    def test_export_metadata_structure(self):
        """Day 3: Validates that metadata export generates the expected key structure."""
        self.loader.metadata["raw_config"] = {
            "vocab_size": 32000,
            "hidden_size": 4096,
            "num_hidden_layers": 32,
            "intermediate_size": 11008,
        }
        export_data = self.loader.export_metadata()

        self.assertIn("model_path", export_data)
        self.assertIn("is_validated", export_data)
        self.assertIn("verification_report", export_data)
        self.assertIn("memory_projection", export_data)
        self.assertIn("performance_metrics", export_data)

    @patch("os.path.getsize")
    @patch("os.walk")
    @patch("model_loader.core.check_directory_exists")
    def test_detect_corrupted_files(self, mock_exists, mock_walk, mock_getsize):
        """Day 4: Validates detection of empty or corrupted model files."""
        mock_exists.return_value = True
        mock_walk.return_value = [("/mock/path", [], ["model.safetensors", "config.json"])]
        mock_getsize.side_effect = [0, 1024]

        corrupted = self.loader.detect_corrupted_files()
        self.assertIn("model.safetensors", corrupted)
        self.assertTrue(self.loader.metadata["verification_report"]["corruption_detected"])

    def test_performance_metrics_tracking(self):
        """Day 5: Ensures performance metrics track latency correctly across stages."""
        self.loader.verify_config_keys()
        self.loader.load_safely()
        metrics = self.loader.get_performance_metrics()

        self.assertIn("scan_time_ms", metrics)
        self.assertIn("verification_time_ms", metrics)
        self.assertIn("load_time_ms", metrics)
        self.assertIn("total_execution_time_ms", metrics)
        self.assertGreaterEqual(metrics["total_execution_time_ms"], 0.0)


if __name__ == "__main__":
    unittest.main()