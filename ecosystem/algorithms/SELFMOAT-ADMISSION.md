# SELFMOAT Admission Algorithm

## Status

FORMALIZED AS A CONTROL ALGORITHM. This artifact defines control logic, not a claim that the entire SELFMOAT doctrine has been migrated.

## Contract

Given foreign state x:

1. Observe x.
2. Determine whether x is admitted into the current jurisdiction.
3. If observed(x) AND NOT admitted(x), mutation authorization MUST be refused.
4. Quarantine the proposed transition.
5. Emit an evidence/receipt event for the refusal if the runtime supports actuation.
6. Recontact external state before treating the refusal receipt as evidence of current external state.

## Core invariant

OBSERVE(x) ∧ ¬ADMITTED(x) → ¬AUTHORIZED_MUTATION(x)

## Non-equivalences

observation ≠ admission
observation ≠ authority
observation ≠ mutation
