"""
FDD Validator - Constants and Regex Patterns

All regular expressions and global constants used throughout the FDD validation system.
Extracted for easier maintenance and modification by both humans and AI agents.
"""

import re
from typing import Dict

# === PROJECT CONFIGURATION ===

PROJECT_CONFIG_FILENAME = ".fdd-config.json"

# === ARTIFACT STRUCTURE PATTERNS ===

SECTION_RE = re.compile(r"^###\s+Section\s+([A-Z0-9]+):\s+(.+?)\s*$")
HEADING_ID_RE = re.compile(r"^#{1,6}\s+([A-Z])\.\s+.*$")
SECTION_FEATURE_RE = re.compile(r"^##\s+([A-G])\.\s+(.+?)\s*$")
SECTION_BUSINESS_RE = re.compile(r"^##\s+(?:Section\s+)?([A-E])\s*[:.]\s*(.+)?$", re.IGNORECASE)

# === FDD ID PATTERNS ===

# Generic FDD ID
FDD_ANY_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+\b")

# Core artifact IDs
REQ_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-req-[a-z0-9-]+\b")
NFR_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-nfr-[a-z0-9-]+\b")
PRINCIPLE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-principle-[a-z0-9-]+\b")
CONSTRAINT_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-constraint-[a-z0-9-]+\b")
ACTOR_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-actor-[a-z0-9-]+\b")
CAPABILITY_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-capability-[a-z0-9-]+\b")
USECASE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-usecase-[a-z0-9-]+\b")

# Feature-specific IDs
FEATURE_FLOW_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-flow-[a-z0-9-]+\b")
FEATURE_ALGO_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-algo-[a-z0-9-]+\b")
FEATURE_STATE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-state-[a-z0-9-]+\b")
FEATURE_REQ_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-req-[a-z0-9-]+\b")
FEATURE_TEST_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-test-[a-z0-9-]+\b")

# ADR IDs
ADR_NUM_RE = re.compile(r"\bADR-(\d{4})\b")
FDD_ADR_NUM_RE = re.compile(r"\bfdd-[a-z0-9-]+-adr-(\d{4})\b")
ADR_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-adr-[a-z0-9-]+\b")
ADR_HEADING_RE = re.compile(r"^##\s+(ADR-(\d{4})):\s+(.+?)\s*$")

# Change IDs
CHANGE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-change-[a-z0-9-]+\b")

# === FDL (FDD Description Language) PATTERNS ===

FDL_STEP_LINE_RE = re.compile(r"^\s*(?:\d+\.|-)\s+\[[ xX]\]\s+-\s+`ph-\d+`\s+-\s+.+?\s+-\s+`inst-[a-z0-9-]+`\s*$")
FDL_SCOPE_ID_RE = re.compile(
    r"^\s*[-*]\s+\[[ xX]\]\s+\*\*ID\*\*:\s*`fdd-[a-z0-9-]+-feature-[a-z0-9-]+-(?:flow|algo|state|test)-[a-z0-9-]+`\s*$"
)
PHASE_TOKEN_RE = re.compile(r"\bph-(\d+)\b")

# === CHANGES (Implementation Plan) PATTERNS ===

CHANGES_HEADER_TITLE_RE = re.compile(r"^#\s+Implementation\s+Plan:\s+.+$", re.IGNORECASE)
CHANGE_HEADING_RE = re.compile(r"^##\s+Change\s+(\d+):\s+(.+?)\s*$")
CHANGE_STATUS_RE = re.compile(r"^(?:⏳\s+NOT_STARTED|🔄\s+IN_PROGRESS|✅\s+COMPLETED|📦\s+ARCHIVED)$")
CHANGE_PRIORITY_RE = re.compile(r"^(?:HIGH|MEDIUM|LOW)$")
CHANGE_TASK_LINE_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(\d+(?:\.\d+)+)\s+(.+?)\s*$")

# === CODE TRACEABILITY PATTERNS ===

# @fdd-* tags in code comments
FDD_TAG_CHANGE_RE = re.compile(r"@fdd-change:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_FLOW_RE = re.compile(r"@fdd-flow:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_ALGO_RE = re.compile(r"@fdd-algo:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_STATE_RE = re.compile(r"@fdd-state:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_REQ_RE = re.compile(r"@fdd-req:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_TEST_RE = re.compile(r"@fdd-test:(fdd-[a-z0-9-]+):ph-(\d+)")

# fdd-begin/fdd-end block markers
FDD_BEGIN_LINE_RE = re.compile(r"^\s*(?:#|//|<!--|/\*|\*)\s*(?:!no-fdd\s+)?fdd-begin\s+([^\s]+)")
FDD_END_LINE_RE = re.compile(r"^\s*(?:#|//|<!--|/\*|\*)\s*(?:!no-fdd\s+)?fdd-end\s+([^\s]+)")

# Unwrapped instruction tags (should be wrapped in fdd-begin/fdd-end)
UNWRAPPED_INST_TAG_RE = re.compile(r"(fdd-[a-z0-9-]+(?:-[a-z0-9-]+)*:ph-\d+:inst-[a-z0-9-]+)")

# Block exclusion markers (!no-fdd-begin/!no-fdd-end)
NO_FDD_BLOCK_BEGIN_RE = re.compile(r"^\s*(?:#|//|<!--|/\*|\*).*!no-fdd-begin")
NO_FDD_BLOCK_END_RE = re.compile(r"^\s*(?:#|//|<!--|/\*|\*).*!no-fdd-end")

# === SCOPE ID PATTERNS BY KIND ===

SCOPE_ID_BY_KIND_RE: Dict[str, re.Pattern] = {
    "flow": FEATURE_FLOW_ID_RE,
    "algo": FEATURE_ALGO_ID_RE,
    "state": FEATURE_STATE_ID_RE,
    "req": FEATURE_REQ_ID_RE,
    "test": FEATURE_TEST_ID_RE,
}

# === VALIDATION PATTERNS ===

PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX|TBA)\b", re.IGNORECASE)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
DISALLOWED_LINK_TOKEN_RE = re.compile(r"(@/|@DESIGN\.md|@BUSINESS\.md|@ADR\.md)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
BRACE_PLACEHOLDER_RE = re.compile(r"\{[A-Za-z0-9_-]+\}")
SIZE_HARD_LIMIT_RE = re.compile(r"Hard limit:\s*≤?\s*(\d+)\s*lines", re.IGNORECASE)
ID_LINE_RE = re.compile(r"\*\*ID\*\*:\s*(.+)$")

# ADR-specific patterns
ADR_DATE_RE = re.compile(r"\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})")
ADR_STATUS_RE = re.compile(r"\*\*Status\*\*:\s*(Proposed|Accepted|Deprecated|Superseded)")

# Status overview pattern
STATUS_OVERVIEW_RE = re.compile(
    r"\*\*Status Overview\*\*:\s*(\d+)\s+features\s+total\s*\(\s*(\d+)\s+completed,\s*(\d+)\s+in progress,\s*(\d+)\s+not started\s*\)"
)

# Feature heading pattern
FEATURE_HEADING_RE = re.compile(
    r"^###\s+(\d+)\.\s+\[(.+?)\]\((feature-[^)]+/)\)\s+([⏳🔄✅])\s+(CRITICAL|HIGH|MEDIUM|LOW)\s*$"
)

# Field header pattern
FIELD_HEADER_RE = re.compile(r"^\s*[-*]?\s*\*\*([^*]+)\*\*:\s*(.*)$")

# === KNOWN FIELD NAMES ===

KNOWN_FIELD_NAMES = {
    "Purpose",
    "Status",
    "Description",
    "References",
    "Implements",
    "Phases",
    "Testing Scenarios (FDL)",
    "Testing Scenarios",
    "Acceptance Criteria",
}
