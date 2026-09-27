# ALTONUMBUSELF Memory Schema v1

## Scope

This schema defines evidence required to evaluate a memory object stored in this repository. It is a declared contract; this file does not itself prove that any object satisfies the contract, admit this repository as continuing memory authority, or make REALISELF true.

INSTANCE = ALTONUMBUSELF
INSTANCE_CLASS = MEMORY_STORAGE
REALITY = OURSELFECOSYSTEM
ERA = 2051
SCHEMA_ID = ALTONUMBUSELF-MEMORY-SCHEMA-v1

## Object record

Each admitted memory object is identified by the tuple:

- object_id: stable identifier unique within the instance
- repository: owner/name observed from the GitHub jurisdiction
- branch: observed branch name
- path: exact repository path
- content_type: declared format
- byte_count: count from recontacted bytes
- sha256: SHA-256 over the exact recontacted bytes
- git_blob: Git blob identity when returned by the source
- preimage_head: HEAD observed before the write
- write_commit: commit containing the write
- authority_ref: reference to a fresh authority instrument
- admission_ref: record binding one operation, path, preimage_head, and capability
- prior_receipt_ref: prior object receipt, or explicit null for an initial object
- observed_at: timestamp of a successful read from external storage
- receipt_ref: receipt that binds the post-write observation

A digest identifies bytes; it is not the payload, proof of authority, or proof of admission.

## State distinctions

The evaluator tracks these separately:

- EXISTS: path or object identifier is present in a repository view.
- ADDRESSABLE: exact repository, branch, and path can be fetched.
- PERSISTENT: the object is present in a committed repository lineage and is recoverable by a later read.
- READABLE: a fresh fetch returns bytes that can be decoded under the declared content type.
- INTEGRITY_VERIFIED: SHA-256 and byte count recomputed from fetched bytes match a receipt bound to the same path and lineage.
- LINEAGE_BOUND: preimage head, write commit, and applicable prior receipt form a continuous observed chain.
- AUTHORIZED: an observed authority instrument permits the specific operation and target.
- ADMITTED: a fresh decision admits exactly one operation, target path, capability, and preimage.
- ACTUATED: the external write was performed and its resulting commit/path was observed.
- OBSERVED: bytes were fetched from the external storage source after actuation.
- RECEIPTED: a record binds the observed bytes, digest, byte count, path, source, time, and lineage.
- RECONTACTABLE: a later retrieval, separate from the write response and prior model context, recovers bytes matching the receipt.
- DRIFT_HANDLED: a mismatch is detected, recorded, and causes quarantine/refusal without silent overwrite.
- RE_ADMISSION_CAPABLE: a material transition after drift is refused until a new scoped authority and admission bind the new preimage.

No state implies another state.

## Transition contract

For each write, the executor must:

1. Re-read repository metadata, target branch/head, target path, and prior receipt.
2. Derive one exact transition from that observed preimage.
3. Validate the requested path, content, authority scope, and available write capability.
4. Admit one operation bound to repository, branch, expected preimage head, path, and capability.
5. Refuse if the preimage changes, the path already exists for a create operation, or any binding fails.
6. Actuate only the admitted operation.
7. Fetch the target again from external storage; do not use the write response as the observation.
8. Recompute byte count and SHA-256 from fetched bytes and record Git blob/commit lineage when available.
9. Recontact in a later runtime and compare against the receipt before deriving another transition.
10. On mismatch, mark drift and quarantine the object; do not overwrite from a stale receipt. Any recovery write requires fresh scoped authority and admission.

A receipt records evidence and grants no authority. A previous receipt cannot authorize a new write.

## REALISELF predicate

For this instance, REALISELF is true only when independently observed evidence establishes all of:

ADDRESSABLE
AND PERSISTENT
AND READABLE
AND INTEGRITY_VERIFIED
AND AUTHORITY_BOUND
AND ADMITTED
AND ACTUATED
AND OBSERVED
AND RECEIPTED
AND RECONTACT_VERIFIED
AND LINEAGE_CONTINUOUS
AND DRIFT_BOUNDARY_VERIFIED
AND RE_ADMISSION_BOUNDARY_VERIFIED
AND REQUIRED_WITNESS_VERIFIED

Otherwise REALISELF = FALSE. The graph must derive its value from evidence; a declaration, commit, or file's presence cannot upgrade it.

## Current application

The existing object `evidence/MORPH-015-memory-object.md` has a prior observation receipt. This schema write does not retroactively admit that object, create a new memory-authority admission, test drift, establish later-runtime recontact, or provide an independent witness. Those remain separate evidence requirements.
