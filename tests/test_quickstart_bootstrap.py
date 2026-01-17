# @fdd-change:fdd-fdd-feature-core-methodology-change-quickstart-docs:ph-1
# Tests implement: fdd-fdd-feature-core-methodology-test-quickstart-bootstrap
"""
Tests for QUICKSTART bootstrap workflow.

Validates that QUICKSTART.md is readable and has proper structure.
"""

# @fdd-test:fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1
import sys
import unittest
from pathlib import Path

# Add skills/fdd/scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))


# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-start-timer
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-copy-first-prompt
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-execute-first
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-verify-adapter-created
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-copy-second-prompt
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-execute-second
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-verify-business-created
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-stop-timer
# fdd-begin fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-verify-time-limit
class TestQuickstartBootstrap(unittest.TestCase):
    """Test QUICKSTART.md file structure and content."""

    def test_quickstart_exists_and_readable(self):
        """Verify QUICKSTART.md exists and is readable."""
        quickstart = Path(__file__).parent.parent / "QUICKSTART.md"
        self.assertTrue(quickstart.exists(), "QUICKSTART.md must exist")
        
        content = quickstart.read_text(encoding='utf-8')
        self.assertGreater(len(content), 100, "QUICKSTART.md should have substantial content")
        
        # Check for key sections
        self.assertIn("Quick Start", content, "Should have Quick Start heading")
        self.assertIn("fdd", content.lower(), "Should mention fdd")
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-verify-time-limit
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-stop-timer
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-verify-business-created
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-execute-second
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-copy-second-prompt
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-verify-adapter-created
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-execute-first
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-copy-first-prompt
# fdd-end   fdd-fdd-feature-core-methodology-test-quickstart-bootstrap:ph-1:inst-start-timer


if __name__ == "__main__":
    unittest.main(verbosity=2)
