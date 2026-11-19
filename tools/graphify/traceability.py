"""Resolve curated feature, change, and test references at an immutable Git commit."""

import re
from collections.abc import Callable

FEATURE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
TEST_PATH = re.compile(r"tests/test_[a-z0-9_]+\.py")
TEST_LINE = re.compile(r"(?:async )?def (?:test_[a-z0-9_]+|smoke)\(")


def validate_features(features: object, source_files: list[str]) -> None:
    if not isinstance(features, list) or not 1 <= len(features) <= 32:
        raise ValueError("Features must be a nonempty list of at most 32 entries")
    if "CHANGELOG.md" not in source_files:
        raise ValueError("Feature traceability requires CHANGELOG.md")
    ids = set()
    for feature in features:
        if not isinstance(feature, dict) or set(feature) != {"id", "label", "document", "change", "tests"}:
            raise ValueError("Invalid feature record")
        identity = feature["id"]
        if not isinstance(identity, str) or len(identity) > 80 or not FEATURE_ID.fullmatch(identity):
            raise ValueError("Invalid feature identifier")
        if identity in ids:
            raise ValueError("Duplicate feature identifier: " + identity)
        ids.add(identity)
        label, change = feature["label"], feature["change"]
        if (
            not isinstance(label, str) or not 0 < len(label.strip()) <= 120 or not label.isprintable()
            or not isinstance(change, str) or not change.startswith("- ") or len(change) > 500
            or not change.isprintable()
        ):
            raise ValueError("Invalid feature label or changelog entry: " + identity)
        if feature["document"] not in source_files:
            raise ValueError("Feature documentation must appear in source_files: " + identity)
        tests = feature["tests"]
        if not isinstance(tests, list) or not 1 <= len(tests) <= 12:
            raise ValueError("Feature must cite between 1 and 12 tests: " + identity)
        references = set()
        for test in tests:
            if not isinstance(test, dict) or set(test) != {"path", "line"}:
                raise ValueError("Invalid test reference for " + identity)
            path, line = test["path"], test["line"]
            if (
                not isinstance(path, str) or not TEST_PATH.fullmatch(path)
                or not isinstance(line, str) or len(line) > 240 or not line.isprintable()
                or not TEST_LINE.match(line)
            ):
                raise ValueError("Expected a test declaration from tests/test_*.py")
            if (path, line) in references:
                raise ValueError("Duplicate test reference for " + identity)
            references.add((path, line))


def resolve_features(features: list[dict], read_source: Callable[[str], str]) -> list[dict]:
    cache: dict[str, list[str]] = {}

    def locate(path: str, target: str) -> dict:
        if path not in cache:
            cache[path] = read_source(path).splitlines()
        matches = [i for i, line in enumerate(cache[path], 1) if line.strip() == target]
        if len(matches) != 1:
            raise ValueError(f"Expected one pinned source match in {path}: {target}")
        return {"path": path, "line": matches[0], "text": target}

    return [
        {
            **feature,
            "change": locate("CHANGELOG.md", feature["change"]),
            "tests": [locate(test["path"], test["line"]) for test in feature["tests"]],
        }
        for feature in sorted(features, key=lambda feature: feature["id"])
    ]
