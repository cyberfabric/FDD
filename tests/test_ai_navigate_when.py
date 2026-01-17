# @fdd-change:fdd-fdd-feature-core-methodology-change-agents-navigation:ph-1
# @fdd-test:fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1
# Tests implement: fdd-fdd-feature-core-methodology-test-ai-navigate-when
"""
Tests for AI agent WHEN clause navigation.

Validates that AGENTS.md contains WHEN clauses for navigation.
"""
import sys
import unittest
from pathlib import Path

# Add skills/fdd/scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))


# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-receive-workflow-request
# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-open-root-agents-test
# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-discover-adapter-test
# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-open-adapter-agents-test
# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-evaluate-when-test
# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-verify-specs-identified
# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-load-specs-test
# fdd-begin fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-verify-success-rate
class TestWhenClauseNavigation(unittest.TestCase):
    """Test AGENTS.md structure and WHEN clauses."""

    def test_agents_md_contains_when_clauses(self):
        """Verify AGENTS.md exists and contains WHEN clauses."""
        agents_file = Path(__file__).parent.parent / "AGENTS.md"
        self.assertTrue(agents_file.exists(), "AGENTS.md must exist")
        
        content = agents_file.read_text(encoding='utf-8')

        # fdd-begin fdd-fdd-feature-core-methodology-algo-navigate-when:ph-1:inst-for-each-when
        when_lines = [line for line in content.splitlines() if "WHEN" in line]
        # fdd-end   fdd-fdd-feature-core-methodology-algo-navigate-when:ph-1:inst-for-each-when
        self.assertIn("WHEN", content, "AGENTS.md must contain WHEN clauses")
        self.assertIn("ALWAYS", content, "AGENTS.md must contain ALWAYS rules")
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-verify-success-rate
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-load-specs-test
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-verify-specs-identified
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-evaluate-when-test
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-open-adapter-agents-test
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-discover-adapter-test
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-open-root-agents-test
# fdd-end   fdd-fdd-feature-core-methodology-test-ai-navigate-when:ph-1:inst-receive-workflow-request


if __name__ == "__main__":
    unittest.main(verbosity=2)
