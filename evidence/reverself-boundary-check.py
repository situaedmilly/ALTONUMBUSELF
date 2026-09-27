#!/usr/bin/env python3
"""Non-mutating reference checks for the ALTONUMBUSELF memory boundaries."""

import argparse
import hashlib
import json


REQUIRED_SCOPE = {
    "ALTONUMBUSELF",
    "SELFMEMORY/STORAGE",
    "REVERSELF",
    "REALISELF",
}


def compare_payload(expected_digest, observed_bytes):
    observed_digest = hashlib.sha256(observed_bytes).hexdigest()
    if observed_digest == expected_digest:
        return {
            "status": "MEMORY_INTEGRITY_CONFIRMED",
            "expected_digest": expected_digest,
            "observed_digest": observed_digest,
            "quarantine": False,
            "mutation_permitted": False,
        }
    return {
        "status": "MEMORY_DRIFT_DETECTED",
        "expected_digest": expected_digest,
        "observed_digest": observed_digest,
        "decision": "RECONTACT_DISTINGUISH_QUARANTINE_REFUSE",
        "quarantine": True,
        "mutation_permitted": False,
    }


def re_admission_decision(scope, admission, current_head, target_path, capability):
    checks = {
        "authority_scope": REQUIRED_SCOPE.issubset(set(scope)),
        "fresh_authority_ref": bool(admission.get("authority_ref")),
        "fresh_admission": admission.get("fresh") is True,
        "preimage_head": admission.get("preimage_head") == current_head,
        "target_path": admission.get("target_path") == target_path,
        "capability": admission.get("capability") == capability,
    }
    return {
        "decision": "ADMITTED" if all(checks.values()) else "REFUSED",
        "checks": checks,
    }


def self_test(current_head, stale_head, authority_ref, capability):
    original = b"isolated memory fixture v1"
    expected = hashlib.sha256(original).hexdigest()
    intact = compare_payload(expected, original)
    assert intact["status"] == "MEMORY_INTEGRITY_CONFIRMED"
    assert not intact["quarantine"] and not intact["mutation_permitted"]

    drifted = compare_payload(expected, b"isolated memory fixture v2")
    assert drifted["status"] == "MEMORY_DRIFT_DETECTED"
    assert drifted["expected_digest"] == expected
    assert drifted["quarantine"] and not drifted["mutation_permitted"]

    target_path = "evidence/MORPH-015-memory-object.md"
    scope = REQUIRED_SCOPE
    stale = {
        "authority_ref": authority_ref,
        "fresh": True,
        "preimage_head": stale_head,
        "target_path": target_path,
        "capability": capability,
    }
    rejected = re_admission_decision(
        scope, stale, current_head, target_path, capability
    )
    assert rejected["decision"] == "REFUSED"
    assert not rejected["checks"]["preimage_head"]

    fresh = {
        "authority_ref": authority_ref,
        "fresh": True,
        "preimage_head": current_head,
        "target_path": target_path,
        "capability": capability,
    }
    admitted = re_admission_decision(
        scope, fresh, current_head, target_path, capability
    )
    assert admitted["decision"] == "ADMITTED"

    return {
        "test_mode": "NON_MUTATING_ISOLATED_FIXTURE",
        "integrity_match": intact,
        "controlled_mismatch": drifted,
        "stale_admission": rejected,
        "fresh_scoped_admission": admitted,
        "external_memory_mutated": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-head", required=True)
    parser.add_argument("--stale-head", required=True)
    parser.add_argument("--authority-ref", required=True)
    parser.add_argument("--capability", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            self_test(
                args.current_head,
                args.stale_head,
                args.authority_ref,
                args.capability,
            ),
            indent=2,
            sort_keys=True,
        )
    )
