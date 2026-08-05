"""
test_loader.py - Automated Testing Suite for NeuroFence ModelLoader
Validates metadata calculations, configuration validation rules, 
memory profiling matrices, corrupted file detection, performance tracking,
large sharded model handling, and validation report exporting.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from model_loader.core import ModelLoader

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

        self.assertIn("validation_status", export_data)
        self.assertIn("target_model_path", export_data)
        self.assertIn("memory_requirements", export_data)
        self.assertIn("performance_latency", export_data)

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

    @patch("os.walk")
    @patch("model_loader.core.check_directory_exists")
    def test_detect_model_shards(self, mock_exists, mock_walk):
        """Day 6: Validates identification of sharded model files."""
        mock_exists.return_value = True
        mock_walk.return_value = [(
            "/mock/path", 
            [], 
            ["model-00001-of-00002.safetensors", "model-00002-of-00002.safetensors"]
        )]

        shards = self.loader.detect_model_shards()
        self.assertEqual(len(shards), 2)
        self.assertTrue(self.loader.is_sharded)

    @patch("builtins.open")
    def test_export_validation_report(self, mock_open):
        """Day 7: Validates report generation and export execution."""
        report = self.loader.generate_validation_report()
        self.assertIn("validation_status", report)
        self.assertIn("verification_checks", report)

        success = self.loader.export_validation_report("test_report.json")
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()