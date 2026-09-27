# INSTANCE_PROVENANCE — Observation Ledger

This ledger distinguishes CLAIM, OBSERVATION, RECEIPT, and ADMISSION. It records observations available through this runtime and connector; it is not an authority grant. Times are UTC unless stated. Digests for the four requested remote text artifacts will be added only after separate GitHub readback. This file does not hash itself.

## Event EV-001 — prior command-host clone boundary

- EVENT_ID: EV-001
- TIMESTAMP: 2026-09-27 (the prior command output did not include a time)
- INSTANCE: ALTONUMBUSELF
- ACTION: Attempted `git clone https://github.com/situaedmilly/ALTONUMBUSELF.git /home/selfadmin/ourself-instances/ALTONUMBUSELF`
- OBSERVED_STATE: Clone exited 128 with `Could not resolve host: github.com`; follow-up found destination absent.
- EVIDENCE_SOURCE: Prior runtime command output and read-only follow-up in this conversation.
- DIGEST_WHERE_APPLICABLE: Not applicable.
- AUTHORITY_STATUS: User requested local clone in the earlier task; no remote mutation.
- ADMISSION_STATUS: No remote admission implied.
- INTERPRETATION: NETWORK_UNREACHABILITY for that command-host transport at that time; not proof of GitHub or repository nonexistence.

## Event EV-002 — authenticated GitHub jurisdiction discovery

- EVENT_ID: EV-002
- TIMESTAMP: 2026-09-27T05:02:32Z
- INSTANCE: GitHub connector / situaedmilly
- ACTION: Read authenticated login, organizations, accessible repository listing, and target repository metadata.
- OBSERVED_STATE: Login `situaedmilly` (account id 208099411); organizations list empty; accessible repository listing includes public `situaedmilly/ALTONUMBUSELF` (id 1358892817); metadata reports default branch `main`, not archived, and admin/maintain/push permissions.
- EVIDENCE_SOURCE: Successful GitHub connector responses `github_get_user_login`, `github_list_user_orgs`, `github_list_repositories`, `github_get_repo`.
- DIGEST_WHERE_APPLICABLE: Not applicable.
- AUTHORITY_STATUS: Connector-authenticated identity and repository permission metadata observed.
- ADMISSION_STATUS: No memory-authority admission implied.

## Event EV-003 — initial repository lineage and contents

- EVENT_ID: EV-003
- TIMESTAMP: 2026-09-27T05:02:32Z
- INSTANCE: situaedmilly/ALTONUMBUSELF
- ACTION: Read branch search, recent commit, commit detail, README, and tested absence of requested paths.
- OBSERVED_STATE: Branch `main`; initial/current observed commit `d6e19691984fac5c7baf38b25f13a16704a9ca88`, message `Initial commit`, created 2026-09-06T07:27:33Z. Commit diff lists `.gitignore` and `README.md`. README content was `# ALTONUMBUSELF\n/path/to/OURCLOUDSELF\n`. Fetch of OURSELF_INSTANCE.md, SELFGRAPH_INSTANCE.json, INSTANCE_PROVENANCE.md, and evidence/.gitkeep returned 404.
- EVIDENCE_SOURCE: Successful GitHub connector responses `github_search_branches`, `github_search_commits`, `github_fetch_commit`, `github_fetch_file`.
- DIGEST_WHERE_APPLICABLE: README Git blob SHA c14f1eb6d254ed9b754ff5d0de6bc20d5fb91ac3 (Git blob identifier, not SHA-256).
- AUTHORITY_STATUS: Existing repository metadata reported admin/push permission for authenticated login.
- ADMISSION_STATUS: Not applicable to read-only observation.

## Event EV-004 — requested artifact write and recontact

- EVENT_ID: EV-004
- TIMESTAMP: Pending; this event will be completed only from tool results after write and readback.
- INSTANCE: situaedmilly/ALTONUMBUSELF
- ACTION: Pending.
- OBSERVED_STATE: Pending.
- EVIDENCE_SOURCE: Pending.
- DIGEST_WHERE_APPLICABLE: Pending post-readback SHA-256 values and byte counts.
- AUTHORITY_STATUS: User explicitly authorized creation of the bounded requested instance artifacts in the target repository.
- ADMISSION_STATUS: This scoped artifact-writing authorization is not an admission of ALTONUMBUSELF as memory authority, and does not authorize future memory writes.

## State semantics

- CLAIM: A statement awaiting evidence.
- OBSERVATION: A fact returned by a specified read operation from a specified source and time.
- RECEIPT: A record binding an observation to bytes/digests and lineage; it does not grant authority.
- ADMISSION: A fresh, scoped authorization decision for one material transition; no such memory-authority admission is established here.
