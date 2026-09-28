#!/usr/bin/env python3
"""Read-only scanner for affirmative state claims lacking evidence links."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


DEFAULT_PATHS = (
    "SELFGRAPH_INSTANCE.json",
    "runtime/compilers/matter-compiler/MATTER-0001.json",
    "runtime/compilers/matter-compiler/outputs/MATTER-0001-SELFMOAT-C-OUTPUT.json",
    "evidence/REVERSELF-001-memory-recontact-receipt.json",
    "evidence/REVERSELF-002-boundary-evidence.json",
    "evidence/ALCHEMY-MORPH-017-transformation.json",
    "evidence/morph-xii/SELFMOAT-TEST-001-C.actuation.json",
    "evidence/morph-xii/EXECUTION-MORPH-XII-001.json",
    "evidence/morph-xii/OBSERVATION-MORPH-XII-001.json",
    "evidence/morph-xii/RECEIPT-MORPH-XII-001.json",
    "evidence/morph-xiii/COMPILER-EXECUTION-001.json",
    "evidence/morph-xiii/COMPILER-OBSERVATION-001.json",
    "evidence/morph-xiii/COMPILER-RECEIPT-001.json",
    "evidence/morph-xiii/RUNTIME-B-RECOVERY-001.json",
    "evidence/morph-xiii/drift/DRIFT-BASELINE-RECEIPT-001.json",
    "evidence/morph-xiii/drift/DRIFT-OBSERVATION-001.json",
    "evidence/morph-xiii/drift/DRIFT-REFUSAL-QUARANTINE-001.json",
)

_MISSING_WITNESS = {"BLOCKED", "MISSING", "NOT_WITNESSED"}
_WITNESS_FLAGS = {"witnessed", "independent_witness", "witness_verified"}


def _pointer_part(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def _finding(path, pointer, code, detail):
    return {
        "path": path,
        "json_pointer": pointer or "/",
        "code": code,
        "detail": detail,
    }


def _has_execution_proof(record):
    invocation = record.get("invocation")
    if not isinstance(invocation, dict):
        return False
    command = invocation.get("command")
    return (
        isinstance(command, list)
        and bool(command)
        and invocation.get("exit_code") == 0
        and invocation.get("result") in {"EXECUTED", "COMPILED"}
    )


def inspect_document(path, document):
    findings = []

    def visit(value, pointer):
        if isinstance(value, dict):
            kind = value.get("kind")
            state = value.get("state")
            if kind == "WITNESS" and isinstance(state, str) and state.upper() in _MISSING_WITNESS:
                findings.append(
                    _finding(
                        path,
                        pointer,
                        "WITNESS_LINK_ABSENT",
                        f"Witness node state is {state}; no independent witness is established.",
                    )
                )

            witness = value.get("witness")
            if isinstance(witness, dict):
                witness_state = witness.get("status")
                reference = witness.get("independent_witness_ref") or witness.get("witness_ref")
                if (
                    isinstance(witness_state, str)
                    and witness_state.upper() in _MISSING_WITNESS
                    and not reference
                ):
                    findings.append(
                        _finding(
                            path,
                            pointer + "/witness",
                            "WITNESS_LINK_ABSENT",
                            f"Witness status is {witness_state} and its reference is absent.",
                        )
                    )

            channel_witness = value.get("independent_channel_witness")
            if isinstance(channel_witness, dict) and (
                channel_witness.get("same_runtime") is True
                or channel_witness.get("same_identity") is True
            ):
                findings.append(
                    _finding(
                        path,
                        pointer + "/independent_channel_witness",
                        "WITNESS_NOT_INDEPENDENT",
                        "The record identifies shared runtime or identity; channel agreement is not independent witnessing.",
                    )
                )

            for key, child in value.items():
                child_pointer = pointer + "/" + _pointer_part(key)
                normalized = key.lower()
                if normalized in _WITNESS_FLAGS and child is True:
                    findings.append(
                        _finding(
                            path,
                            child_pointer,
                            "AFFIRMATIVE_WITNESS_CLAIM",
                            "An affirmative witness flag requires a separately addressable independent witness record.",
                        )
                    )
                elif normalized == "realiself" and child is True:
                    findings.append(
                        _finding(
                            path,
                            child_pointer,
                            "AFFIRMATIVE_REALISELF_CLAIM",
                            "A true predicate declaration is not evidence that every required condition was independently established.",
                        )
                    )
                elif normalized in {"execution", "executed"} and child is True:
                    if not _has_execution_proof(value):
                        findings.append(
                            _finding(
                                path,
                                child_pointer,
                                "EXECUTION_CLAIM_WITHOUT_PROCESS_PROOF",
                                "Execution is asserted without a same-record command, successful process result, and exit code.",
                            )
                        )
                visit(child, child_pointer)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, pointer + "/" + str(index))

    visit(document, "")
    return findings


def _strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"non-standard JSON constant: {value}")


def _git_blob(raw):
    header = b"blob " + str(len(raw)).encode("ascii") + bytes([0])
    return hashlib.sha1(header + raw).hexdigest()


def scan_paths(root, paths, source_commit):
    root = Path(root).resolve()
    scanner_path = Path(__file__).resolve()
    scanner_raw = scanner_path.read_bytes()
    scanned = []
    findings = []
    for relative in paths:
        source = (root / relative).resolve()
        if root not in source.parents:
            raise ValueError(f"scan path escapes repository root: {relative}")
        raw = source.read_bytes()
        if source_commit:
            committed = subprocess.check_output(
                ["git", "-C", str(root), "show", f"{source_commit}:{relative}"]
            )
            if committed != raw:
                raise ValueError(f"scan input differs from source commit: {relative}")
        document = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
        scanned.append(
            {
                "path": relative,
                "byte_count": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "git_blob": _git_blob(raw),
            }
        )
        findings.extend(inspect_document(relative, document))
    findings.sort(key=lambda item: (item["path"], item["json_pointer"], item["code"]))
    return {
        "scanner": "runtime/reverself/no_unwitnessed_claims.py",
        "scanner_artifact": {
            "sha256": hashlib.sha256(scanner_raw).hexdigest(),
            "git_blob": _git_blob(scanner_raw),
        },
        "source_commit": source_commit,
        "scanned_files": scanned,
        "finding_count": len(findings),
        "findings": findings,
        "decision": (
            "NO_UNWITNESSED_STATE_CLAIMS"
            if not findings
            else "BLOCKED_UNWITNESSED_STATE_CLAIMS_PRESENT"
        ),
        "mutated_inputs": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--commit", help="Require every input to match this committed preimage.")
    parser.add_argument("--paths", nargs="+", default=DEFAULT_PATHS)
    args = parser.parse_args()
    commit = args.commit
    if commit is None:
        commit = subprocess.check_output(
            ["git", "-C", str(args.root), "rev-parse", "HEAD"], text=True
        ).strip()
    report = scan_paths(args.root, args.paths, commit)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
