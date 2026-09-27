# INSTANCE_PROVENANCE — Observation Ledger

This ledger separates CLAIM, OBSERVATION, RECEIPT, and ADMISSION. Entries are limited to tool results observed in this runtime. Timestamps are UTC; when an exact event time was not returned, that limitation is stated. The ledger does not grant authority. It cannot stably include a digest of its own final bytes; its final SHA-256 is reported outside the file.

## EV-001 — prior command-host network boundary

- EVENT_ID: EV-001
- TIMESTAMP: 2026-09-27; exact command time was not captured.
- INSTANCE: ALTONUMBUSELF
- ACTION: Attempted `git clone https://github.com/situaedmilly/ALTONUMBUSELF.git /home/selfadmin/ourself-instances/ALTONUMBUSELF`.
- OBSERVED_STATE: Clone exited 128 with `Could not resolve host: github.com`; read-only follow-up found the destination absent.
- EVIDENCE_SOURCE: Prior command output and follow-up in this conversation.
- DIGEST_WHERE_APPLICABLE: Not applicable.
- AUTHORITY_STATUS: Earlier user request covered a local clone; this failed command did not mutate GitHub.
- ADMISSION_STATUS: No remote admission implied.
- INTERPRETATION: NETWORK_UNREACHABILITY for that command-host transport path and time. This is not GITHUB_NONEXISTENCE.

## EV-002 — authenticated GitHub jurisdiction

- EVENT_ID: EV-002
- TIMESTAMP: 2026-09-27T05:02:32Z (runtime clock near discovery).
- INSTANCE: GitHub connector / situaedmilly
- ACTION: Read authenticated login, organization list, accessible repositories, and target repository metadata.
- OBSERVED_STATE: Connector login `situaedmilly` (account id 208099411); organization list empty; accessible list and metadata include public `situaedmilly/ALTONUMBUSELF` (repository id 1358892817), default branch `main`, not archived, with returned admin/maintain/push permissions.
- EVIDENCE_SOURCE: Successful GitHub connector calls `github_get_user_login`, `github_list_user_orgs`, `github_list_repositories`, `github_get_repo`.
- DIGEST_WHERE_APPLICABLE: Not applicable.
- AUTHORITY_STATUS: Authenticated login and repository permission metadata observed through connector.
- ADMISSION_STATUS: Does not admit memory authority or future mutation.

## EV-003 — pre-actuation repository lineage and content

- EVENT_ID: EV-003
- TIMESTAMP: 2026-09-27T05:02:32Z (runtime clock near discovery).
- INSTANCE: situaedmilly/ALTONUMBUSELF
- ACTION: Read default branch, commit search/detail, README, and requested path availability.
- OBSERVED_STATE: Branch `main`; initial commit `d6e19691984fac5c7baf38b25f13a16704a9ca88`, message `Initial commit`, created 2026-09-06T07:27:33Z. Its observed changed paths are `.gitignore` and `README.md`. README bytes decoded as UTF-8 were `# ALTONUMBUSELF\n/path/to/OURCLOUDSELF\n`. Fetches of `OURSELF_INSTANCE.md`, `SELFGRAPH_INSTANCE.json`, `INSTANCE_PROVENANCE.md`, and `evidence/.gitkeep` returned 404.
- EVIDENCE_SOURCE: Successful GitHub connector calls `github_search_branches`, `github_search_commits`, `github_fetch_commit`, and `github_fetch_file`.
- DIGEST_WHERE_APPLICABLE: Initial README Git blob SHA `c14f1eb6d254ed9b754ff5d0de6bc20d5fb91ac3` (Git blob identifier, not SHA-256).
- AUTHORITY_STATUS: Read-only observation.
- ADMISSION_STATUS: Not applicable.

## EV-004 — scoped artifact actuation

- EVENT_ID: EV-004
- TIMESTAMP: Commit times 2026-09-27T05:05:14Z through 2026-09-27T05:07:16Z; all returned by GitHub commit search.
- INSTANCE: situaedmilly/ALTONUMBUSELF, branch `main`
- ACTION: Updated README while retaining the original heading and literal path; created `OURSELF_INSTANCE.md`, `SELFGRAPH_INSTANCE.json`, `INSTANCE_PROVENANCE.md`, `evidence/.gitkeep`; then updated SELFGRAPH_INSTANCE.json to record observed operation/recontact status.
- OBSERVED_STATE: Each connector write returned success. Commit SHAs in observed order: `ed167a2f117c516c100289972198edcf5fdaead8`, `1af7e1d8ada07316f53e2566998344c7ff573dcb`, `35bc63d7a44974197057b8954e35f6e693933649`, `a147c4b745b4084a3958ad730b9b6556eb2687ba`, `7972fcb63c8cb39921bd4b6708e346add35d9000`, `16ad5e0bd38698141654acf2dd8fb7f811b847bd`.
- EVIDENCE_SOURCE: Successful GitHub connector create/update-file results and subsequent commit search/detail.
- DIGEST_WHERE_APPLICABLE: GitHub returned commit SHAs above; SHA-256 is recorded in EV-005 for readback bytes.
- AUTHORITY_STATUS: User explicitly authorized these named evidence artifacts in the target repository. The connector reported admin/push permission and the file writes succeeded.
- ADMISSION_STATUS: This bounded artifact-writing authorization is not admission of ALTONUMBUSELF as memory authority and does not authorize later memory writes.

## EV-005 — post-actuation recontact and artifact receipt

- EVENT_ID: EV-005
- TIMESTAMP: 2026-09-27T05:07:57Z (runtime clock immediately before this ledger update; connector reads occurred shortly before).
- INSTANCE: situaedmilly/ALTONUMBUSELF
- ACTION: Re-read repository metadata, branch, recent commits, README, contract, graph, ledger, evidence marker, and .gitignore through GitHub connector; fetched commit details for all six observed changes.
- OBSERVED_STATE: Default branch `main`; latest observed head before this ledger update `16ad5e0bd38698141654acf2dd8fb7f811b847bd`. Per-commit changed paths were observed as follows: initial `.gitignore`, `README.md`; then `README.md`; `OURSELF_INSTANCE.md`; `SELFGRAPH_INSTANCE.json`; `INSTANCE_PROVENANCE.md`; `evidence/.gitkeep`; and finally `SELFGRAPH_INSTANCE.json`. The resulting observed path set is `.gitignore`, `README.md`, `OURSELF_INSTANCE.md`, `SELFGRAPH_INSTANCE.json`, `INSTANCE_PROVENANCE.md`, `evidence/.gitkeep`. This is reconstructed from fetched commit changed-path lists and successful path reads, not a recursive-tree API response.
- EVIDENCE_SOURCE: GitHub connector calls `github_get_repo`, `github_search_branches`, `github_search_commits`, `github_fetch_commit`, `github_fetch_file`.
- DIGEST_WHERE_APPLICABLE: SHA-256 of fetched UTF-8 bytes: `README.md` 712 bytes, `2f8e0a892816806cdbb9ff127cc31addbee04e101e05594f1125c70228f8558e`; `OURSELF_INSTANCE.md` 2363 bytes, `375d5129b67148a6bdb36dbef78c2cba756a5983a6f56be0069d5c4549da536`; `SELFGRAPH_INSTANCE.json` 27051 bytes, `d224c2c9009327e251dfeb637e604354035dadcd27fc638ddf9220b593e5e455`; `evidence/.gitkeep` 0 bytes, `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; `.gitignore` 353 bytes, `63afe166951a7eea420b168273d1b9c8a872149406eb7324620548cebadad011`. The ledger SHA-256 is reported externally to avoid self-reference.
- AUTHORITY_STATUS: Readback is observation only.
- ADMISSION_STATUS: No memory-authority admission. Current-session recontact is observed; later-session recontact is not.

## EV-006 — graph timestamp precision correction

- EVENT_ID: EV-006
- TIMESTAMP: 2026-09-27; exact read time not returned, after commit `6af3c06353f0141db07284269fab7b8ac82521c8` (created 2026-09-27T05:09:39Z).
- INSTANCE: situaedmilly/ALTONUMBUSELF
- ACTION: Corrected SELFGRAPH_INSTANCE.json to distinguish the commit creation timestamp from the unreturned connector read time; re-fetched the graph and computed SHA-256 from returned UTF-8 bytes.
- OBSERVED_STATE: Connector reported latest commit `6af3c06353f0141db07284269fab7b8ac82521c8`; fetched graph blob `349829779ca9d31a374ec64cc7de4a6a33dd4f8c`; JSON parsed successfully.
- EVIDENCE_SOURCE: GitHub connector `github_search_commits`, `github_fetch_file`; local Python hashlib over fetched content.
- DIGEST_WHERE_APPLICABLE: SELFGRAPH_INSTANCE.json 27275 bytes, SHA-256 `8c424724cbf31cc8854719f22679fe073b609b305ae675802b9a81c497f3c09a`.
- AUTHORITY_STATUS: User-authorized scope for the named instance graph and ledger.
- ADMISSION_STATUS: Does not admit memory authority or authorize a future transition.

## State semantics and limits

- CLAIM: A statement not yet supported by a source observation.
- OBSERVATION: A result read from a named source through a named operation at a stated time.
- RECEIPT: A record binding observed bytes to path, digest, and lineage; it grants no authority.
- ADMISSION: A fresh decision for one scoped transition. No admission of this repository as memory authority is evidenced.
- The GitHub page reader returned a cached pre-write view during this session; it was not used as post-write proof. Post-write evidence above comes from the authenticated GitHub connector.
- No separate persistent memory object, later-session recovery, drift exercise, fresh re-admission exercise, or independent witness is established by these events.
