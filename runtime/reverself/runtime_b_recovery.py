#!/usr/bin/env python3
"""Recover and verify the receipted compiler output in a clean process."""

import hashlib
import json
import os
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen


REPOSITORY = "situaedmilly/ALTONUMBUSELF"
BRANCH = "morph-xi/selfmoat-proving"
OUTPUT_PATH = (
    "runtime/compilers/matter-compiler/outputs/"
    "MATTER-0001-SELFMOAT-C-OUTPUT.json"
)
RECEIPT_PATH = "evidence/morph-xiii/COMPILER-RECEIPT-001.json"
CONTRACT_PATH = "evidence/morph-xiii/COMPILER-RECONTACT-CONTRACT-001.json"
MAX_RESPONSE_BYTES = 262_144
ALLOWED_ENVIRONMENT = {
    "PATH",
    "PYTHONHASHSEED",
    "LC_CTYPE",
    "__CF_USER_TEXT_ENCODING",
}
OS_ADDED_ENVIRONMENT = {"LC_CTYPE", "__CF_USER_TEXT_ENCODING"}


def _fetch(url):
    request = Request(url, headers={"User-Agent": "ALTONUMBUSELF-Runtime-B/1.0"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"external read returned HTTP {response.status}")
        data = response.read(MAX_RESPONSE_BYTES + 1)
    if len(data) > MAX_RESPONSE_BYTES:
        raise RuntimeError("external response exceeded the configured byte bound")
    return data


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def recover():
    unexpected = set(os.environ) - ALLOWED_ENVIRONMENT
    if unexpected:
        raise RuntimeError(
            "Runtime B environment is not clean: "
            + ", ".join(sorted(unexpected))
        )

    started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    owner, repository = REPOSITORY.split("/", 1)
    branch_url = (
        f"https://api.github.com/repos/{owner}/{repository}/branches/"
        f"{quote(BRANCH, safe='')}"
    )
    branch_data = json.loads(
        _fetch(branch_url), object_pairs_hook=_reject_duplicate_keys
    )
    head = branch_data["commit"]["sha"]
    if (
        not isinstance(head, str)
        or len(head) != 40
        or any(char not in "0123456789abcdef" for char in head)
    ):
        raise RuntimeError("branch API returned an invalid commit SHA")

    def raw(path):
        encoded_path = quote(path, safe="/")
        return _fetch(
            f"https://raw.githubusercontent.com/{REPOSITORY}/{head}/{encoded_path}"
        )

    receipt_bytes = raw(RECEIPT_PATH)
    contract_bytes = raw(CONTRACT_PATH)
    output_bytes = raw(OUTPUT_PATH)
    receipt = json.loads(
        receipt_bytes, object_pairs_hook=_reject_duplicate_keys
    )
    contract = json.loads(
        contract_bytes, object_pairs_hook=_reject_duplicate_keys
    )
    output_sha256 = hashlib.sha256(output_bytes).hexdigest()
    output_git_blob = hashlib.sha1(
        f"blob {len(output_bytes)}\0".encode() + output_bytes
    ).hexdigest()
    subject = contract["subject"]
    matches = (
        subject["repository"] == REPOSITORY
        and subject["branch"] == BRANCH
        and subject["path"] == OUTPUT_PATH
        and receipt["observed_artifact"] == OUTPUT_PATH
        and receipt["observed_digest"] == output_sha256
        and subject["expected_sha256"] == output_sha256
        and subject["expected_byte_count"] == len(output_bytes)
        and subject["expected_git_blob"] == output_git_blob
        and receipt["lineage"]["observed_byte_count"] == len(output_bytes)
        and receipt["lineage"]["observed_git_blob"] == output_git_blob
        and receipt["lineage"]["receipt_hashes_itself"] is False
    )
    finished_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    result = {
        "runtime_id": f"RUNTIME-B-{os.getpid()}",
        "runtime_mode": "CLEAN_ENV_SUBPROCESS",
        "started_at": started_at,
        "finished_at": finished_at,
        "environment_keys": sorted(os.environ),
        "os_added_environment_keys": sorted(
            set(os.environ) & OS_ADDED_ENVIRONMENT
        ),
        "shared_conversation_memory_used": False,
        "external_repository_read_only": True,
        "repository": REPOSITORY,
        "branch": BRANCH,
        "branch_head": head,
        "receipt_path": RECEIPT_PATH,
        "receipt_id": receipt.get("receipt_id"),
        "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "contract_path": CONTRACT_PATH,
        "output_path": OUTPUT_PATH,
        "output_byte_count": len(output_bytes),
        "output_sha256": output_sha256,
        "output_git_blob": output_git_blob,
        "decision": "VERIFIED_MATCH" if matches else "REFUSED_MISMATCH",
        "matches_receipt": matches,
        "separate_machine": False,
        "separate_os_identity": False,
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if matches else 1


if __name__ == "__main__":
    sys.exit(recover())
