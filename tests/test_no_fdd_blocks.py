# @fdd-test:fdd-fdd-feature-core-methodology-test-no-fdd-block-exclusion:ph-1
"""
Test !no-fdd-begin/!no-fdd-end block exclusion mechanism.

Validates that content between !no-fdd-begin and !no-fdd-end markers
is properly excluded from FDD validation and traceability scanning.
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

import fdd


class TestNoFddBlockExclusion(unittest.TestCase):
    """Test !no-fdd-begin/!no-fdd-end exclusion blocks."""

    def test_excluded_block_ignores_fdd_tags(self):
        """Verify that FDD tags inside !no-fdd-begin/!no-fdd-end blocks are ignored."""
        text = """
# Normal code
# fdd-begin fdd-test-feature-x-flow-y:ph-1:inst-real
real_implementation()
# fdd-end   fdd-test-feature-x-flow-y:ph-1:inst-real

# <!-- !no-fdd-begin -->
# Example code (should be ignored):
# fdd-begin fdd-example-feature-z-flow-w:ph-1:inst-example
example_code()
# fdd-end   fdd-example-feature-z-flow-w:ph-1:inst-example
# <!-- !no-fdd-end -->
"""
        paired_tags = fdd._paired_inst_tags_in_text(text)
        
        # Should only find the real tag, not the example
        self.assertIn("fdd-test-feature-x-flow-y:ph-1:inst-real", paired_tags)
        self.assertNotIn("fdd-example-feature-z-flow-w:ph-1:inst-example", paired_tags)

    def test_excluded_block_ignores_unwrapped_tags(self):
        """Verify that unwrapped instruction tags in excluded blocks are ignored."""
        text = """
# Normal code with real tag
# fdd-test-feature-a-algo-b:ph-1:inst-real-tag

# <!-- !no-fdd-begin -->
# Example: fdd-example-feature-c-algo-d:ph-1:inst-example-tag
# <!-- !no-fdd-end -->
"""
        unwrapped = fdd._unwrapped_inst_tag_hits_in_text(text)
        tags = [hit["tag"] for hit in unwrapped]
        
        self.assertIn("fdd-test-feature-a-algo-b:ph-1:inst-real-tag", tags)
        self.assertNotIn("fdd-example-feature-c-algo-d:ph-1:inst-example-tag", tags)

    def test_excluded_block_ignores_scope_tags(self):
        """Verify that @fdd-* tags in excluded blocks are ignored."""
        text = """
# @fdd-change:fdd-real-feature-x-change-y:ph-1

# <!-- !no-fdd-begin -->
# Example in docs:
# @fdd-change:fdd-example-feature-z-change-w:ph-1
# <!-- !no-fdd-end -->
"""
        hits = fdd._code_tag_hits(text)
        
        change_ids = [rid for rid, _ in hits["change"]]
        self.assertIn("fdd-real-feature-x-change-y", change_ids)
        self.assertNotIn("fdd-example-feature-z-change-w", change_ids)

    def test_excluded_block_prevents_empty_block_error(self):
        """Verify that empty blocks inside excluded zones don't trigger errors."""
        text = """
# Real implementation
# fdd-begin fdd-test-feature-x-flow-y:ph-1:inst-real
real_code()
# fdd-end   fdd-test-feature-x-flow-y:ph-1:inst-real

# <!-- !no-fdd-begin -->
# Example (intentionally empty for illustration):
# fdd-begin fdd-example-feature-z-flow-w:ph-1:inst-empty-example
# fdd-end   fdd-example-feature-z-flow-w:ph-1:inst-empty-example
# <!-- !no-fdd-end -->
"""
        issues = fdd._empty_fdd_tag_blocks_in_text(text)
        
        # Should not report empty_block for the example
        empty_tags = [issue["tag"] for issue in issues if issue["type"] == "empty_block"]
        self.assertNotIn("fdd-example-feature-z-flow-w:ph-1:inst-empty-example", empty_tags)

    def test_nested_excluded_blocks_work(self):
        """Verify that nested !no-fdd-begin/!no-fdd-end blocks work correctly."""
        text = """
# Real code
# @fdd-flow:fdd-real-feature-x-flow-y:ph-1

# <!-- !no-fdd-begin -->
# Outer example block
# @fdd-flow:fdd-example-outer-feature-a-flow-b:ph-1

# <!-- !no-fdd-begin -->
# Inner nested example
# @fdd-flow:fdd-example-inner-feature-c-flow-d:ph-1
# <!-- !no-fdd-end -->

# More outer example
# @fdd-flow:fdd-example-outer2-feature-e-flow-f:ph-1
# <!-- !no-fdd-end -->
"""
        hits = fdd._code_tag_hits(text)
        flow_ids = [rid for rid, _ in hits["flow"]]
        
        self.assertIn("fdd-real-feature-x-flow-y", flow_ids)
        self.assertNotIn("fdd-example-outer-feature-a-flow-b", flow_ids)
        self.assertNotIn("fdd-example-inner-feature-c-flow-d", flow_ids)
        self.assertNotIn("fdd-example-outer2-feature-e-flow-f", flow_ids)

    def test_excluded_block_works_in_markdown(self):
        """Verify exclusion works with HTML comment syntax in markdown."""
        text = """
Real content here.

<!-- fdd-begin fdd-test-feature-x-flow-y:ph-1:inst-real -->
Real implementation
<!-- fdd-end   fdd-test-feature-x-flow-y:ph-1:inst-real -->

<!-- !no-fdd-begin -->
## Example Section

```rust
// fdd-begin fdd-example-feature-z-algo-w:ph-1:inst-example
example_rust_code();
// fdd-end   fdd-example-feature-z-algo-w:ph-1:inst-example
```
<!-- !no-fdd-end -->
"""
        paired_tags = fdd._paired_inst_tags_in_text(text)
        
        self.assertIn("fdd-test-feature-x-flow-y:ph-1:inst-real", paired_tags)
        self.assertNotIn("fdd-example-feature-z-algo-w:ph-1:inst-example", paired_tags)

    def test_unmatched_no_fdd_begin_does_not_crash(self):
        """Verify that unmatched !no-fdd-begin doesn't cause crashes."""
        text = """
# Real code
# fdd-begin fdd-test-feature-x-flow-y:ph-1:inst-real
real_code()
# fdd-end   fdd-test-feature-x-flow-y:ph-1:inst-real

# <!-- !no-fdd-begin -->
# Example without closing marker
# fdd-begin fdd-example-feature-z-flow-w:ph-1:inst-orphan
example()
# fdd-end   fdd-example-feature-z-flow-w:ph-1:inst-orphan
"""
        # Should not crash, and should exclude everything after !no-fdd-begin
        paired_tags = fdd._paired_inst_tags_in_text(text)
        
        self.assertIn("fdd-test-feature-x-flow-y:ph-1:inst-real", paired_tags)
        # Orphan should NOT be found (no closing !no-fdd-end means it's excluded to EOF)
        self.assertNotIn("fdd-example-feature-z-flow-w:ph-1:inst-orphan", paired_tags)


if __name__ == "__main__":
    unittest.main()
