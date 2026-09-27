# OURSELF Instance Contract

INSTANCE_NAME = ALTONUMBUSELF
INSTANCE_CLASS = MEMORY_STORAGE
REALITY = OURSELFECOSYSTEM
ERA = 2051

## State distinctions

- VALID: a claim or artifact meets its stated validation criteria.
- AUTHORIZED: a governing actor or instrument permits a specified operation on a specified target.
- ACTUATABLE: the required capability and path are available for that operation.
- EXECUTED: the operation was actually performed.
- OBSERVED: a state was directly read from its stated source at a stated time.
- WITNESSED: an observation was independently corroborated by a named witness or independent channel.
- RECEIPTED: a record binds an observation to evidence such as a digest and lineage.
- ADMITTED: a fresh, scoped decision accepts a specific transition for execution.
- REALISELF: the predicate in SELFGRAPH_INSTANCE.json is satisfied by independently observed evidence; declaration or file existence is insufficient.

These are distinct states. Evidence for one does not imply another.

## Identity and authority boundary

REMOTE_REPOSITORY
≠ LOCAL_REPOSITORY
≠ MEMORY_INSTANCE
≠ AUTHORITY
≠ RECEIPT
≠ REALISELF

The repository is evidence-bearing infrastructure. It does not become sovereign merely because it exists. The authenticated GitHub connector observed the repository under the account stated in the provenance ledger; that observation does not itself admit any future mutation.

## SELFMOAT

- Foreign state may be observed.
- Observation does not grant authority.
- Repository existence does not grant mutation authority.
- A proposed memory write does not equal an admitted memory write.
- A committed artifact does not equal an observed artifact until recontacted.
- A receipt must refer to observed state.
- A prior receipt does not automatically authorize a new transition.
- Every material transition requires fresh admission.

## Current status

DISCOVERED; evidence artifacts have been written and subsequently recontacted as recorded in INSTANCE_PROVENANCE.md. CONTRACT_ADMISSION = NOT_EVIDENCED. REALISELF = FALSE because the required predicate is not fully evidenced.

The previous command-host clone attempt failed because DNS resolution of github.com failed. That is a NETWORK_UNREACHABILITY observation for that transport path and time, not evidence that GitHub or this repository does not exist.
