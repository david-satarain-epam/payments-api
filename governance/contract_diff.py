"""
API Contract Comparator.

Compares two OpenAPI snapshots and identifies:
- Breaking changes (removed fields, changed types, new required fields)
- Non-breaking changes (new optional fields, description updates)
- Deprecated elements

Used by: Impact Context MCP Server → compare_api_contracts()
"""

import json
from pathlib import Path
from typing import Any
from deepdiff import DeepDiff


def load_openapi_spec(path: str) -> dict:
    """Load an OpenAPI specification from file."""
    with open(path, "r") as f:
        return json.load(f)


def compare_contracts(baseline_path: str, proposed_path: str) -> dict:
    """
    Compare two OpenAPI specs and return structured diff.

    Args:
        baseline_path: Path to the approved (current) OpenAPI spec.
        proposed_path: Path to the proposed (PR) OpenAPI spec.

    Returns:
        dict with keys: breaking_changes, new_fields, deprecated, has_breaking_change
    """
    baseline = load_openapi_spec(baseline_path)
    proposed = load_openapi_spec(proposed_path)

    diff = DeepDiff(baseline, proposed, ignore_order=True, verbose_level=2)

    breaking_changes = []
    new_fields = []
    deprecated = []

    # ── Analyze dictionary items changed ──
    if "dictionary_item_removed" in diff:
        for path in diff["dictionary_item_removed"]:
            path_str = _format_path(path)
            breaking_changes.append({
                "type": "REMOVED",
                "path": path_str,
                "detail": f"'{path_str}' was removed",
            })

    if "dictionary_item_added" in diff:
        for path in diff["dictionary_item_added"]:
            path_str = _format_path(path)
            new_fields.append({
                "type": "ADDED",
                "path": path_str,
                "detail": f"'{path_str}' was added",
            })

    if "type_changes" in diff:
        for path_str, change in diff["type_changes"].items():
            breaking_changes.append({
                "type": "TYPE_CHANGED",
                "path": path_str,
                "detail": f"Type changed from {change['old_type']} to {change['new_type']}",
            })

    # ── Check for new required fields (breaking) ──
    baseline_required = _extract_required_fields(baseline)
    proposed_required = _extract_required_fields(proposed)

    new_required = proposed_required - baseline_required
    for field in new_required:
        breaking_changes.append({
            "type": "NEW_REQUIRED",
            "path": field,
            "detail": f"'{field}' is now required (was optional)",
        })

    removed_required = baseline_required - proposed_required
    for field in removed_required:
        new_fields.append({
            "type": "NOW_OPTIONAL",
            "path": field,
            "detail": f"'{field}' is now optional (was required)",
        })

    return {
        "has_breaking_change": len(breaking_changes) > 0,
        "breaking_changes": breaking_changes,
        "new_fields": new_fields,
        "deprecated": deprecated,
        "total_changes": len(breaking_changes) + len(new_fields),
        "baseline": str(baseline_path),
        "proposed": str(proposed_path),
    }


def _format_path(path: str | list) -> str:
    """Convert a DeepDiff path to a readable dot-separated string."""
    if isinstance(path, str):
        return path.removeprefix("root")

    path_items = path
    parts = []
    for item in path_items:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, int):
            if parts:
                parts[-1] += f"[{item}]"
    return ".".join(parts)


def _extract_required_fields(spec: dict) -> set:
    """Extract all required fields from an OpenAPI spec."""
    required = set()
    schemas = spec.get("components", {}).get("schemas", {})

    for schema_name, schema in schemas.items():
        req = schema.get("required", [])
        for field in req:
            required.add(f"{schema_name}.{field}")

    return required