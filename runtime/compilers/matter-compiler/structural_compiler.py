#!/usr/bin/env python3
"""Bounded, deterministic structural compilation for small Matter JSON objects."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


MAX_INPUT_BYTES = 65_536
MAX_OUTPUT_BYTES = 131_072
MAX_NESTING_DEPTH = 8
REQUIRED_FIELDS = {
    "matter_id",
    "matter_type",
    "version",
    "jurisdiction",
    "semantic",
    "inputs",
    "outputs",
    "state",
    "invariants",
    "preconditions",
    "failure_states",
    "transitions",
    "algorithm",
    "formulas",
    "authority",
    "capability",
    "admission",
    "execution",
    "observation",
    "witness",
    "receipt",
    "lineage",
    "recontact",
    "dependencies",
}


class CompilationError(ValueError):
    """Raised when a source object is outside the compiler contract."""


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CompilationError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise CompilationError(f"non-standard JSON constant: {value}")


def _check_nesting(text):
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_NESTING_DEPTH:
                raise CompilationError(
                    f"JSON nesting exceeds {MAX_NESTING_DEPTH}"
                )
        elif char in "]}":
            depth -= 1
            if depth < 0:
                raise CompilationError("unbalanced JSON structure")
    if in_string or depth != 0:
        raise CompilationError("incomplete JSON structure")


def _require_string(value, label):
    if not isinstance(value, str) or not value:
        raise CompilationError(f"{label} must be a non-empty string")


def _require_object(value, label):
    if not isinstance(value, dict):
        raise CompilationError(f"{label} must be an object")


def _require_array(value, label):
    if not isinstance(value, list):
        raise CompilationError(f"{label} must be an array")


def _validate_matter(matter):
    _require_object(matter, "Matter")
    missing = REQUIRED_FIELDS - matter.keys()
    extra = matter.keys() - REQUIRED_FIELDS
    if missing:
        raise CompilationError(
            "missing Matter fields: " + ", ".join(sorted(missing))
        )
    if extra:
        raise CompilationError(
            "unexpected Matter fields: " + ", ".join(sorted(extra))
        )

    for field in ("matter_id", "matter_type", "version"):
        _require_string(matter[field], field)
    for field in (
        "jurisdiction",
        "semantic",
        "state",
        "authority",
        "capability",
        "admission",
        "execution",
        "observation",
        "witness",
        "receipt",
        "lineage",
        "recontact",
    ):
        _require_object(matter[field], field)
    for field in (
        "inputs",
        "outputs",
        "invariants",
        "preconditions",
        "failure_states",
        "transitions",
        "formulas",
        "dependencies",
    ):
        _require_array(matter[field], field)
    if not all(isinstance(item, str) for item in matter["invariants"]):
        raise CompilationError("invariants must contain only strings")
    if not all(isinstance(item, str) for item in matter["preconditions"]):
        raise CompilationError("preconditions must contain only strings")
    if not all(isinstance(item, str) for item in matter["formulas"]):
        raise CompilationError("formulas must contain only strings")
    if not all(isinstance(item, str) for item in matter["dependencies"]):
        raise CompilationError("dependencies must contain only strings")
    for field in ("inputs", "outputs", "failure_states", "transitions"):
        if not all(isinstance(item, dict) for item in matter[field]):
            raise CompilationError(f"{field} must contain only objects")
    if matter["algorithm"] is not None:
        _require_string(matter["algorithm"], "algorithm")
    for field, required in (
        ("jurisdiction", ("reality", "instance", "substrate")),
        ("semantic", ("definition", "semantic_type", "vocabulary_refs")),
    ):
        missing_nested = set(required) - matter[field].keys()
        if missing_nested:
            raise CompilationError(
                f"{field} missing fields: "
                + ", ".join(sorted(missing_nested))
            )
    for field in ("reality", "instance", "substrate"):
        _require_string(matter["jurisdiction"][field], f"jurisdiction.{field}")
    for field in ("definition", "semantic_type"):
        _require_string(matter["semantic"][field], f"semantic.{field}")
    _require_array(matter["semantic"]["vocabulary_refs"], "semantic.vocabulary_refs")
    if not all(isinstance(item, str) for item in matter["semantic"]["vocabulary_refs"]):
        raise CompilationError("semantic.vocabulary_refs must contain only strings")


def compile_matter(source_bytes):
    if len(source_bytes) > MAX_INPUT_BYTES:
        raise CompilationError(f"input exceeds {MAX_INPUT_BYTES} bytes")
    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CompilationError("input is not UTF-8") from error
    _check_nesting(source_text)
    try:
        matter = json.loads(
            source_text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise CompilationError(f"invalid JSON: {error.msg}") from error
    _validate_matter(matter)

    formulas = matter["formulas"]
    if not formulas:
        formula_status = "NO_FORMULAS_DECLARED"
    elif all(
        formula == "UNFORMALIZED" or formula.startswith("UNFORMALIZED:")
        for formula in formulas
    ):
        formula_status = "UNFORMALIZED"
    else:
        formula_status = "SOURCE_DECLARED_NOT_FORMALIZED"

    output = {
        "artifact_schema": "ourself.matter-compiler.structural-output.v1",
        "compiler": {
            "matter_id": "MATTER-0001",
            "version": "0.1.0",
            "mode": "STRUCTURAL_ONLY",
        },
        "source": {
            "matter_id": matter["matter_id"],
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
            "byte_count": len(source_bytes),
        },
        "structure": {
            "fields": sorted(matter),
            "input_count": len(matter["inputs"]),
            "output_count": len(matter["outputs"]),
            "transition_count": len(matter["transitions"]),
            "formula_count": len(formulas),
            "formula_status": formula_status,
        },
        "source_matter": matter,
        "claims": {
            "source_matter_executed": False,
            "external_state_mutated": False,
            "external_observation_performed": False,
            "formula_invented": False,
        },
    }
    output_bytes = (
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )
    if len(output_bytes) > MAX_OUTPUT_BYTES:
        raise CompilationError(f"output exceeds {MAX_OUTPUT_BYTES} bytes")
    return output_bytes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    source_bytes = args.input.read_bytes()
    output_bytes = compile_matter(source_bytes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as output_file:
        output_file.write(output_bytes)
    print(
        json.dumps(
            {
                "status": "COMPILED",
                "input_sha256": hashlib.sha256(source_bytes).hexdigest(),
                "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
                "output_byte_count": len(output_bytes),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
