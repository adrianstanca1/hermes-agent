"""
Test for gateway-optimization-plan skill.
Validates that all 4 workstreams execute correctly and verify the expected outcomes.
"""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class GatewayOptimizationPlanTest(unittest.TestCase):
    """Test gateway optimization plan execution outcomes."""

    def test_gateway_is_running(self):
        """Verify gateway service is active and running."""
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "hermes-gateway.service"],
            capture_output=True,
            text=True,
            timeout=10
        )
        self.assertEqual(result.returncode, 0, "Gateway service should be active")
        self.assertEqual(result.stdout.strip(), "active")

    def test_telegram_connected(self):
        """Verify Telegram platform is connected."""
        gateway_state_path = Path.home() / ".hermes" / "gateway_state.json"
        self.assertTrue(gateway_state_path.exists(), "gateway_state.json should exist")
        
        state = json.loads(gateway_state_path.read_text())
        self.assertEqual(state.get("gateway_state"), "running")
        
        platforms = state.get("platforms", {})
        self.assertIn("telegram", platforms)
        self.assertEqual(platforms["telegram"].get("state"), "connected")

    def test_ollama_models_available(self):
        """Verify all 3 Ollama models are installed and loaded."""
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        self.assertEqual(result.returncode, 0)
        
        output = result.stdout
        expected_models = ["hermes3:latest", "llama3.1:8b", "gemma2:27b"]
        for model in expected_models:
            self.assertIn(model, output, f"Model {model} should be installed")

    def test_toolsets_enabled(self):
        """Verify core toolsets are enabled."""
        # These toolsets should be enabled from our optimization
        enabled_toolsets = ["browser", "terminal", "code_execution", 
                           "computer_use", "skills", "vision", "tts"]
        
        for toolset in enabled_toolsets:
            # Use hermes config get to check
            result = subprocess.run(
                ["hermes", "config", "get", "platform_toolsets"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # If config get fails, check if tool is listed as enabled in tools list
            tools_result = subprocess.run(
                ["hermes", "tools", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Toolsets with checkmarks are enabled
            self.assertIn(f"✓ enabled {toolset}", tools_result.stdout,
                         f"{toolset} should be enabled")

    def test_performance_configuration(self):
        """Verify performance tuning settings are applied."""
        config_path = Path.home() / ".hermes" / "config.yaml"
        self.assertTrue(config_path.exists())
        
        config_content = config_path.read_text()
        
        # Check key performance settings
        self.assertIn("agent.max_turns", config_content)
        self.assertIn("terminal.timeout", config_content)
        self.assertIn("compression.enabled", config_content)

    def test_ollama_env_optimized(self):
        """Verify Ollama environment is tuned for CPU-only."""
        env_path = Path.home() / ".hermes" / ".env"
        self.assertTrue(env_path.exists())
        
        env_content = env_path.read_text()
        
        # Check Ollama optimization env vars
        self.assertIn("OLLAMA_NUM_PARALLEL=1", env_content)
        self.assertIn("OLLAMA_MAX_LOADED_MODELS=1", env_content)

    def test_skill_created(self):
        """Verify the gateway optimization plan skill exists."""
        skill_path = Path.home() / ".hermes" / "skills" / "devops" / "gateway-optimization-plan" / "SKILL.md"
        self.assertTrue(skill_path.exists(), "gateway-optimization-plan skill should exist")
        
        content = skill_path.read_text()
        self.assertIn("---", content)  # YAML frontmatter start
        self.assertIn("name: gateway-optimization-plan", content)
        self.assertIn("description:", content)


if __name__ == "__main__":
    unittest.main()