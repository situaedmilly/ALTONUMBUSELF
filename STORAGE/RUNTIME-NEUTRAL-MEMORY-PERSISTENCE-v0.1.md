# ALTONUMBUSELF Runtime-Neutral Memory Persistence Contract v0.1

ALTONUMBUSELF is a memory reality and object model, not a storage engine. Memory objects are canonical only when their exact bytes are enveloped and persisted through an admitted OURDATASELFBASE adapter.

## Requirements

- Preserve the existing ALTONUMBUSELF identity, lineage, and reality boundaries.
- Store memory payloads as immutable content-addressed bytes.
- Keep memory identity, object identity, storage adapter identity, runtime identity, and custodian identity distinct.
- Append transitions to the canonical DATASELF journal; local memory indexes are projections.
- Rebuild indexes from admitted envelopes and journals.
- Permit runtime changes without changing memory object identity.
- Treat model context windows, prompt caches, vector indexes, and agent-local state as volatile or derived unless separately admitted.
- Do not equate synchronization with custody or replication with independent witnessing.
- Require exact read-back and later-runtime recontact before declaring continuity.

## Adapter binding

Each ALTONUMBUSELF storage binding references a DATASELF adapter registration and its exact admission scope. A storage migration creates a new versioned binding event; it does not rewrite historical memory lineage.

## Current state

This document defines the cross-runtime memory contract only. No ALTONUMBUSELF production adapter, migration, or global memory cutover is performed by this proposal.
