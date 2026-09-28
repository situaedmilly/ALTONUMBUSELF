#!/usr/bin/env python3
"""Evaluate whether corroborating evidence has an independent boundary."""

from dataclasses import asdict, dataclass


def _endpoint_complete(endpoint):
    identifiers = (
        endpoint.identity_id,
        endpoint.channel_id,
        endpoint.runtime_id,
        endpoint.host_id,
        endpoint.subject,
        endpoint.sha256,
        endpoint.evidence_ref,
    )
    return (
        endpoint.identity_verified is True
        and all(isinstance(value, str) and value.strip() for value in identifiers)
        and len(endpoint.sha256) == 64
        and all(char in "0123456789abcdef" for char in endpoint.sha256)
    )


@dataclass(frozen=True)
class WitnessEndpoint:
    identity_id: str
    channel_id: str
    runtime_id: str
    host_id: str
    subject: str
    sha256: str
    evidence_ref: str
    identity_verified: bool


def evaluate_witness(subject, sha256, primary, witness):
    if witness is None:
        return {
            "decision": "BLOCKED",
            "reason": "No independently authenticated witness endpoint is available.",
            "independent_witness_verified": False,
            "evidence_ref": None,
        }
    if not _endpoint_complete(primary) or not _endpoint_complete(witness):
        return {
            "decision": "BLOCKED",
            "reason": "Both endpoints require verified identities, non-empty boundary identifiers, a SHA-256 digest, and durable evidence references.",
            "independent_witness_verified": False,
            "evidence_ref": witness.evidence_ref or None,
        }
    if (
        primary.identity_id == witness.identity_id
        or primary.channel_id == witness.channel_id
        or primary.runtime_id == witness.runtime_id
        or primary.host_id == witness.host_id
    ):
        return {
            "decision": "BLOCKED",
            "reason": "Identity, channel, runtime, and host must all be distinct.",
            "independent_witness_verified": False,
            "evidence_ref": witness.evidence_ref or None,
        }
    if witness.subject != subject or witness.sha256 != sha256:
        return {
            "decision": "REFUSED",
            "reason": "The witness endpoint does not corroborate the exact subject digest.",
            "independent_witness_verified": False,
            "evidence_ref": witness.evidence_ref or None,
        }
    if not witness.evidence_ref:
        return {
            "decision": "BLOCKED",
            "reason": "A successful comparison requires a durable witness evidence reference.",
            "independent_witness_verified": False,
            "evidence_ref": None,
        }
    return {
        "decision": "VERIFIED",
        "reason": "Distinct verified endpoints returned the exact same subject digest.",
        "independent_witness_verified": True,
        "evidence_ref": witness.evidence_ref,
        "successful_witness_claim": True,
    }


def decision_record(subject, sha256, primary, witness):
    result = evaluate_witness(subject, sha256, primary, witness)
    record = {
        "subject": subject,
        "sha256": sha256,
        "primary": asdict(primary),
        "witness": None if witness is None else asdict(witness),
        **result,
    }
    if result["decision"] != "VERIFIED":
        record["successful_witness_claim"] = False
    return record
