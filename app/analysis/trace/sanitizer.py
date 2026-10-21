"""Only permit bounded diagnostic metadata, never arbitrary tool payloads."""

import json
import re

KEYS = frozenset({
    "file_path", "branch", "model", "attempt", "error_type", "processed", "total",
    "successful", "failed", "count", "details", "source_files", "selected_files",
    "read_successful_files", "workflow_status", "gap_count", "format",
    "input_tokens", "output_tokens", "total_tokens",
})


def safe_text(value, limit=500):
    value = str(value)
    value = re.sub(r"(?i)(bearer\s+)[^\s]+", r"\1[redacted]", value)
    value = re.sub(r"(?i)(token|api[_-]?key|password|secret)(\s*[=:]\s*)[^\s&]+",
                   r"\1\2[redacted]", value)
    value = re.sub(r"\b(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]+)",
                   "[redacted]", value)
    return value[:limit]


def safe_attributes(attributes):
    result = {}
    for key, value in (attributes or {}).items():
        if key not in KEYS:
            continue
        clean = value if isinstance(value, (int, float, bool)) else safe_text(value, 300)
        candidate = {**result, key: clean}
        if len(json.dumps(candidate, ensure_ascii=False).encode("utf-8")) <= 2600:
            result[key] = clean
    return result
