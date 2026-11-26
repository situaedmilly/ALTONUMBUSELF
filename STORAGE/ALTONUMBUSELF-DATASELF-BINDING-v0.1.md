# ALTONUMBUSELF → OURDATASELFBASE Memory Binding Contract

**Contract ID:** ALTONUMBUSELF-DATASELF-BINDING-001  
**Version:** 0.1.0  
**State:** PROPOSED / SOURCE-CUSTODIED / NOT_ADMITTED  
**Consumer instance:** `ALTONUMBUSELF`  
**Consumer class:** `MEMORY_STORAGE`  
**Canonical data estate:** `OURDATASELFBASE`  
**Authority parent:** `OURSELF-OS`

## 1. Purpose

Define the boundary by which ALTONUMBUSELF memory objects may be represented in the OURDATASELFBASE canonical data model. This contract binds identity, byte integrity, lineage, custody claims, and admission references. It does not deploy a storage adapter, provision a database, migrate memory, or grant write authority.

ALTONUMBUSELF remains the memory object and continuity model. OURDATASELFBASE remains the canonical data custody and persistence architecture. Neither repository is itself a live canonical payload store.

## 2. Governing source contracts

This contract is subordinate to, and must be interpreted with, the following source-custodied contracts in `situaedmilly/OURSELF-DATABASE-ESTATE`:

- `CONTRACTS/SOVEREIGN-DATA-ENVELOPE-v1.md` (OURDATASELFBASE-ENVELOPE-001)
- `CONTRACTS/SOVEREIGN-DATA-TRANSITION-JOURNAL-v1.md`
- `REGISTRY/runtime-storage-adapters.v1.json` (OURDATASELFBASE-RUNTIME-STORAGE-001)
- `RUNTIME/ADMISSION-GATES.md`

The data envelope's exact-byte SHA-256, immutable payload, append-only transition, and non-interchangeable verification states are mandatory. This contract does not supersede those rules.

## 3. Identity binding

A memory object binding MUST preserve these identities as separate fields:

| Identity | Meaning |
|---|---|
| `memory_reality_id` | The governed OURSELF memory reality |
| `memory_instance_id` | The exact ALTONUMBUSELF instance |
| `memory_object_id` | Stable identity of the memory object |
| `payload_content_key` | `sha256:` key computed over exact payload bytes |
| `data_envelope_id` | Identity of the OURDATASELFBASE envelope |
| `storage_adapter_id` | Exact adapter registration used for persistence |
| `runtime_id` | Exact runtime that performed the operation |
| `custodian_id` | Named operational custodian |
| `authority_ref` | Authority decision scoped to the exact operation |
| `admission_ref` | Admission decision scoped to the exact object, adapter, runtime, and operation |

A repository path, Git commit, branch, or blob SHA is source-custody evidence. It MUST NOT be substituted for a memory object ID, data envelope ID, adapter identity, runtime identity, or payload content key.

## 4. Object and payload rules

1. The canonical object class is `MEMORY_OBJECT`.
2. The payload is opaque byte content. Hash exact bytes before decoding, normalization, compression, or transformation.
3. `byte_count` MUST equal the exact payload byte length.
4. `content_key` MUST equal `sha256:` plus the lowercase SHA-256 digest.
5. Existing memory payloads MUST NOT be overwritten or rewritten in place.
6. A correction or transformation creates a successor object/envelope with explicit predecessor lineage and a new digest.
7. Prompt caches, model context windows, vector indexes, and runtime-local state remain derived or volatile unless separately enveloped and admitted.
8. A projection MUST identify canonical inputs and a deterministic rebuild procedure. It is never canonical authority.

## 5. Persistence and transition sequence

A future admitted persistence operation MUST execute this sequence:

1. Observe the source memory object and its current identity.
2. Read exact payload bytes without mutation.
3. Compute SHA-256 and byte count over those exact bytes.
4. Construct a schema-valid OURDATASELFBASE envelope with explicit reality, instance, jurisdiction, lineage, authority, custody, and verification fields.
5. Obtain a fresh admission decision for the exact object, payload digest, adapter, runtime, and operation.
6. Publish immutable content using an admitted adapter's no-replace semantics.
7. Read back the published bytes and independently recompute digest and byte count.
8. Append the corresponding hash-linked transition journal entry.
9. Record a receipt binding the source object, envelope, payload digest, adapter, runtime, authority, admission, and readback observation.
10. Recontact from a later runtime/session and compare exact digest before declaring continuity.

No step may be inferred from a preceding step. In particular, schema validity is not authorization; authorization is not admission; admission is not persistence; persistence is not recontact; recontact is not independent witness.

## 6. Adapter and runtime boundary

The current OURDATASELFBASE registry reports:

- `NODE-POSIX-FILESYSTEM-CAS`: `CONFORMANCE_TESTED_NOT_ADMITTED`, durability ceiling `D1_PROCESS_CRASH`.
- `S3-COMPATIBLE-OBJECT-CAS`: `CONTRACT_ONLY`.
- `CLOUDFLARE-EDGE-R2-CAS`: `CONTRACT_ONLY`.
- `GITHUB-SOURCE-CUSTODY`: source custody only, not canonical payload storage.
- `IN-MEMORY-CACHE`: cache only, never canonical persistence.

The target OURSELFPIMAC PostgreSQL runtime is recorded as `NOT_PROVISIONED` / `NOT_ADMITTED`. Therefore this contract selects no production adapter and makes no live database, endpoint, or storage availability claim.

An adapter may be used for canonical persistence only after its exact registration, runtime identity, durability evidence, jurisdiction, custody, authority, and admission gates are satisfied. Conformance tests alone do not grant admission.

## 7. Required failure behavior

Fail closed when any of the following is true:

- payload bytes or object identity are ambiguous;
- digest or byte count differs;
- schema version is unknown or required envelope fields are absent;
- authority, admission, jurisdiction, adapter, runtime, or custodian is unresolved;
- adapter is not admitted for the exact scope;
- immutable no-replace publication cannot be guaranteed;
- readback or journal lineage fails;
- witness or independence is claimed without supporting evidence.

On failure, preserve source bytes, do not publish a canonical transition, and record a bounded failure observation without promoting it to an admission receipt.

## 8. Current implementation state

| Capability | State |
|---|---|
| Memory object model | Source-custodied in ALTONUMBUSELF |
| DATASELF envelope contract | Source-custodied |
| Adapter registry | Declared target matrix |
| POSIX CAS | Conformance-tested, not admitted |
| PostgreSQL target | Not provisioned, not admitted |
| ALTONUMBUSELF binding | Proposed by this contract |
| Memory migration | Not performed |
| Canonical write authority | Not granted |
| Production cutover | Not performed |
| Independent witness | Not established |

## 9. Promotion criteria

This contract may be promoted beyond PROPOSED only after:

1. the exact memory schema and object identity contract are cross-checked;
2. a concrete adapter registration is selected and admitted;
3. runtime and host identities are freshly observed;
4. custody, jurisdiction, key handling, and authority are established;
5. exact-byte publish/readback and append-only journal tests pass;
6. later-runtime recontact succeeds;
7. an independent evaluator verifies evidence and scope;
8. the named authority records a scoped admission decision.

Until then, the binding is a design contract only. It does not make ALTONUMBUSELF globally admitted, canonical, or REALISELF.

## 10. Rollback and preservation

This change is additive source documentation. Rollback consists of reverting the single contract commit or closing its review without merge. No existing memory payload, envelope, journal, registry, adapter registration, key, or runtime state is changed by this contract.
