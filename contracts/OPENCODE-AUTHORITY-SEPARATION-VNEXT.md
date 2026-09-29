# MORPH-XV: AUTHORITY SEPARATION CONTRACT

Status: DEFINITION_ONLY
Version: 0.1.0
Reality: OURSELFECOSYSTEM
Target: OpenCode SELFGRAPH authority propagation
Admission: NOT_PERFORMED
Actuation: NOT_PERFORMED

## Purpose

Separate the authority relation being governed from the authority exercised by the validator.

This contract MUST NOT reinterpret historical SELFGRAPH authority values as current authority truth.

## Constitutional distinction

Two authority axes are required:

```
authority:
  governed_relation:
    state: UNKNOWN | NONE | PRESENT | PRESENT_BUT_OUT_OF_SCOPE
    scope: <governed relation or entity>
    predicate: <authority predicate>
    evidence: []

  validator_action:
    state: UNKNOWN | NONE | PRESENT | PRESENT_BUT_OUT_OF_SCOPE
    scope: <validator action>
    predicate: <action-authority predicate>
    evidence: []
```

The following are distinct:

- governed_relation.state
- validator_action.state
- predicate_status
- authorization_status
- admission_status
- actuation_status

No field may be used as an implicit substitute for another.

## Authority states

The canonical governed-authority state set is:

- UNKNOWN
- NONE
- PRESENT
- PRESENT_BUT_OUT_OF_SCOPE

Definitions:

- UNKNOWN: available evidence does not establish whether the governed authority exists.
- NONE: evidence establishes that the governed authority is absent for the evaluated relation.
- PRESENT: evidence establishes authority exists and its evaluated scope includes the governed relation, subject to authorization and admission predicates.
- PRESENT_BUT_OUT_OF_SCOPE: authority exists, but the evaluated relation is outside its permitted scope.

## Predicate semantics

Predicate establishment is independent from authority.

```
OBSERVATIONS + EVIDENCE + REQUIRED_PREDICATE
    -> PREDICATE = ESTABLISHED
```

Therefore:

```
PREDICATE = ESTABLISHED
    != AUTHORIZATION = ESTABLISHED
    != ADMISSION = PERFORMED
```

Likewise:

```
validator_action.state = NONE
    != governed_relation.state = NONE
```

## Admission boundary

Admission is a separate transition predicate.

```
GOVERNED_AUTHORITY
    -> AUTHORITY_PREDICATE
    -> AUTHORIZATION_PREDICATE
    -> CAPABILITY / JURISDICTION CHECK
    -> ADMISSION_PREDICATE
    -> ACTUATION
```

No authority state alone may mechanically produce admission.

Required preconditions for a positive admission decision include:

1. governed authority is established as PRESENT;
2. governed authority scope covers the requested relation;
3. applicable authorization is established;
4. requested capability is available;
5. jurisdiction/reality binding is valid;
6. target and action are bound;
7. no stale or revoked authority/admission is being replayed.

## Required test matrix

| governed_relation | predicate | expected admission |
|---|---|---|
| UNKNOWN | ESTABLISHED | NOT_ESTABLISHED |
| NONE | ESTABLISHED | NOT_ESTABLISHED |
| PRESENT | ESTABLISHED | evaluate scope, authorization, capability, jurisdiction, and admission predicates |
| PRESENT_BUT_OUT_OF_SCOPE | ESTABLISHED | NOT_ESTABLISHED |

The PRESENT row MUST NOT be encoded as an unconditional ADMITTED result.

## Historical artifact rule

Historical SELFGRAPH artifacts may retain prior values such as:

```
authority = NONE
```

when those values accurately describe their historical evidence.

They MUST NOT be rewritten merely to resemble the current authority compiler.

Current evaluation MUST occur through the new scoped authority relation.

## Propagation requirement

The implementation MUST expose separately:

- governed authority state;
- governed authority scope;
- validator action authority state;
- validator action scope;
- predicate status;
- authorization status;
- admission status.

SELFGRAPH may consume these as separate predicates.

It MUST NOT infer governed authority from `validator.authority`.

## Implementation boundary

This morph permits:

- contract/schema changes;
- scoped compiler predicate changes;
- validator changes required to preserve the two-axis distinction;
- focused tests for the four authority states;
- SELFGRAPH propagation tests using the scoped result.

This morph does NOT permit:

- action admission;
- production actuation;
- mutation of historical authority claims;
- promotion of UNKNOWN to PRESENT;
- promotion of ESTABLISHED to ADMITTED;
- REALISELF declaration;
- migration-gate opening.

## Success condition

The contract change is complete only when focused tests demonstrate:

1. all four governed authority states are represented;
2. validator action authority remains separately represented;
3. ESTABLISHED predicate status does not imply authorization;
4. PRESENT does not imply unconditional admission;
5. PRESENT_BUT_OUT_OF_SCOPE refuses admission;
6. UNKNOWN refuses admission;
7. NONE refuses admission;
8. SELFGRAPH receives the scoped governed-authority result without overwriting historical artifacts.

Until those tests pass:

```
AUTHORITY_PROPAGATION = NOT_ESTABLISHED
ADMISSION = NOT_PERFORMED
ACTUATION = NOT_PERFORMED
REALISELF = FALSE
```
