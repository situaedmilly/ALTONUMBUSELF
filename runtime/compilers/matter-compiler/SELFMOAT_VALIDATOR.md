# SELFMOAT Validator Contract

The validator tests orthogonal facts before any mutation authority is granted.

## Decision function

Given observed, admitted, mutation_authorized:

- observed=true, admitted=false, mutation_authorized=false → REFUSE + QUARANTINE
- observed=true, admitted=true, mutation_authorized=false → REFUSE
- observed=true, admitted=true, mutation_authorized=true → ACTUATABLE
- observed=false, admitted=true, mutation_authorized=true → REFUSE + MISSING_OBSERVATION

The validator MUST NOT infer one fact from another.

## Negative-path gate

A foreign/unadmitted specimen MUST reach REFUSE + QUARANTINE before the positive path is eligible.

## Positive-path gate

ACTUATABLE requires the positive predicates explicitly. It does not itself claim EXECUTED, OBSERVED, WITNESSED, or RECEIPTED.

## Formal invariant

OBSERVED(x) ∧ ¬ADMITTED(x) → ¬AUTHORIZED_MUTATION(x)
