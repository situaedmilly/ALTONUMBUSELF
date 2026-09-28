# MORPH-XII: Single-Specimen SELFMOAT Actuation

## Scope

MORPH-XII admits one transition for MATTER-0001 and SELFMOAT-TEST-001 case C:

- Repository: `situaedmilly/ALTONUMBUSELF`
- Branch: `morph-xi/selfmoat-proving`
- Target: `evidence/morph-xii/SELFMOAT-TEST-001-C.actuation.json`
- State change: target path `ABSENT` to `PRESENT`

The current user directive is the authority reference. The authenticated GitHub
write path is represented separately as capability; repository permission alone
does not grant authority. The fresh admission binds the current branch preimage,
authority, capability, compiler contract, validation report, observation plan,
and receipt plan. It admits no other path or Matter.

## Independent facts

The actuation artifact records the authorized case-C fixture values and the
actuation-time state. Its `execution` field is not execution evidence. Execution
is established only by observing the GitHub commit/tree that creates this exact
path. Observation is established only by a later GitHub read of the target
bytes. The receipt digest is computed from those returned bytes, not from the
write payload. Recontact is a distinct later read after the receipt has been
generated.

The fixture's `ACTUATABLE` result is decision-logic evidence only; it does not
supply current authority or admission.

## Commit and failure boundary

The first commit contains only the admitted actuation target. After independent
observation, receipt generation, and later recontact, a second bounded,
evidence-only commit records the decision, transition, validation, execution,
observation, receipt, recontact, and corresponding graph/registry facts.
No source SELFMOAT artifact, schema, compiler definition, migration gate, or
unrelated Matter is changed.

On a head, target, digest, or scope mismatch, stop without repair. Preserve a
refusal/quarantine record and report the exact commit/path needed for an
authorized rollback. Do not replace the target with another artifact.

The ecosystem migration gate remains CLOSED. REALISELF remains FALSE unless
its existing predicate independently evaluates true.
