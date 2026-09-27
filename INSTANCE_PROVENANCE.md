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

## EV-007 — MORPH-016 memory artifact readback and digest receipt

- EVENT_ID: EV-007
- TIMESTAMP: Read operations occurred within the runtime-clock bracket 2026-09-27T05:18:09Z–2026-09-27T05:18:22Z; exact connector call time was not returned.
- INSTANCE: situaedmilly/ALTONUMBUSELF, branch `main`
- ACTION: After the MORPH-015 write, re-read repository metadata, branch, current commit history, the memory object, SELFGRAPH_INSTANCE.json, and this ledger through the authenticated GitHub connector. Computed SHA-256 over the fetched UTF-8 memory-object bytes with local Python hashlib.
- OBSERVED_STATE: The repository remained public under the authenticated account; `main` head was `4e09ac674193bdef4949f65823c219fc2769fdf0`, commit message `Actuate bounded MORPH-015 memory artifact` (created 2026-09-27T05:16:42Z). The requested memory object was returned at `evidence/MORPH-015-memory-object.md`.
- EVIDENCE_SOURCE: Successful `github_get_repo`, `github_search_branches`, `github_search_commits`, and `github_fetch_file` responses, plus local Python hashlib on the returned bytes.
- DIGEST_WHERE_APPLICABLE: `evidence/MORPH-015-memory-object.md`, 2941 UTF-8 bytes; SHA-256 `b3beb89dfef3569a6bd714bbd1abb010782c8328606586cae993e22a1605abdd`; Git blob `49ccc74edfbe4320b0ac60655c8fbce670216e0d`.
- AUTHORITY_STATUS: User explicitly authorized MORPH-016 observation and receipt.
- ADMISSION_STATUS: Scoped to observe and receipt the MORPH-015 artifact. Does not admit continuing memory authority or authorize another memory write.

## EV-008 — graph receipt update and recontact

- EVENT_ID: EV-008
- TIMESTAMP: Graph commit `287ce2e4bf06cadc4d7d175ce21b6c32c69be519` was created at 2026-09-27T05:19:19Z; graph readback and digest calculation completed by 2026-09-27T05:19:26Z.
- INSTANCE: situaedmilly/ALTONUMBUSELF
- ACTION: Updated SELFGRAPH_INSTANCE.json to record MORPH-015 actuation, MORPH-016 observation and receipt, and remaining admission/recontact/drift limits; then fetched the graph and computed its digest.
- OBSERVED_STATE: Graph write returned success; subsequent GitHub fetch returned graph blob `f6c23bbda039c2ed21255eaa0d3daf0e42966f3f`; retrieved JSON parsed successfully.
- EVIDENCE_SOURCE: GitHub connector `github_update_file`, `github_search_commits`, `github_fetch_file`; local Python hashlib.
- DIGEST_WHERE_APPLICABLE: `SELFGRAPH_INSTANCE.json`, 28289 UTF-8 bytes; SHA-256 `f7f82e92a2a1ebd87438f973ab34fe5afd1a176e0f7740e99c17267bda5016b4`.
- AUTHORITY_STATUS: User-authorized MORPH-016 observation and receipt transition.
- ADMISSION_STATUS: Receipt covers the observed artifact bytes and current lineage only; it does not admit memory authority.

## State semantics and limits

- CLAIM: A statement not yet supported by a source observation.
- OBSERVATION: A result read from a named source through a named operation at a stated time.
- RECEIPT: A record binding observed bytes to path, digest, and lineage; it grants no authority.
- ADMISSION: A fresh decision for one scoped transition. No admission of this repository as memory authority is evidenced.
- The GitHub page reader returned a cached pre-write view during this session; it was not used as post-write proof. Post-write evidence above comes from the authenticated GitHub connector.
- The MORPH-015 memory artifact now exists and was re-read for MORPH-016. This does not admit ALTONUMBUSELF as continuing memory authority. Later-session recovery, drift exercise, fresh re-admission, and an independent witness remain unverified.


## EV-009 — MORPH-017 schema contract actuation and readback receipt

- EVENT_ID: EV-009
- TIMESTAMP: 2026-09-27T05:37:13Z (runtime UTC clock; schema readback completed earlier in this runtime turn).
- INSTANCE: `situaedmilly/ALTONUMBUSELF`, branch `main`
- ACTION: Recontacted branch head and confirmed `evidence/ALTONUMBUSELF-MEMORY-SCHEMA-v1.md` absent at preimage `caa95faba97c093a2fca75befa7f7af9801d3706`; admitted and created exactly that new path; fetched the committed schema and existing MORPH-015 object again from GitHub.
- OBSERVED_STATE: GitHub create-file returned commit `41003ed96944944eb370e0868e45710e4f6b17bb`. Later commit search returned that commit as current `main` head. Fetch of the schema returned Git blob `0cd744f6a1d7ad2ff6162e847cbf3281fceec5c7`; commit detail lists only the schema path. Fresh fetch returned 4,920 UTF-8 bytes. Existing MORPH-015 object re-fetch returned its previously receipted 2,941 bytes unchanged.
- EVIDENCE_SOURCE: Authenticated GitHub connector: `github_search_commits`, `github_fetch_file`, `github_fetch_commit`; local Python hashlib and Git blob calculation over fetched UTF-8 bytes.
- DIGEST_WHERE_APPLICABLE: Schema `evidence/ALTONUMBUSELF-MEMORY-SCHEMA-v1.md`: SHA-256 `40bb41f99f7d56d21f5f70eef013d4d836b87f623c75008e609b16eaf4b221c2`, 4,920 bytes; Git blob `0cd744f6a1d7ad2ff6162e847cbf3281fceec5c7`. Existing memory object: SHA-256 `b3beb89dfef3569a6bd714bbd1abb010782c8328606586cae993e22a1605abdd`, 2,941 bytes; Git blob `49ccc74edfbe4320b0ac60655c8fbce670216e0d`.
- AUTHORITY_STATUS: Current user instruction explicitly grants authority to make ALTONUMBUSELF REALISELF; the preceding founder authorization scopes work to the target instance and bounded algorithm. Connector metadata reports admin/push for authenticated `situaedmilly`.
- ADMISSION_STATUS: Fresh runtime admission was limited to one create operation at the absent schema path on branch `main`, against preimage HEAD `caa95faba97c093a2fca75befa7f7af9801d3706`. This admits the schema-file transition only. It does not admit the repository as continuing memory authority and does not authorize a future write.
- LIMIT: The schema declaration and its receipt do not establish later-session recontact, drift handling, re-admission exercise, or an independent witness; REALISELF remains false.


## EV-010 — scoped MORPH-015 memory-object admission

- EVENT_ID: EV-010
- TIMESTAMP: Within 2026-09-27T05:37:13Z–05:38:31Z; the exact decision time was not captured. The interval brackets the runtime clock before the admission and the clock after its ledger write.
- INSTANCE: `situaedmilly/ALTONUMBUSELF`, branch `main`
- ACTION: Admitted one existing object, `evidence/MORPH-015-memory-object.md`, for bounded OURSELF continuity-memory use under `ALTONUMBUSELF-MEMORY-SCHEMA-v1`.
- OBSERVED_STATE: Preimage HEAD `43d7fbecbc5870505169f4fc3c8a03534e7145a5`; object readback was 2,941 bytes, SHA-256 `b3beb89dfef3569a6bd714bbd1abb010782c8328606586cae993e22a1605abdd`, Git blob `49ccc74edfbe4320b0ac60655c8fbce670216e0d`; prior MORPH-016 receipt is EV-007. Schema bytes were fetched at Git blob `0cd744f6a1d7ad2ff6162e847cbf3281fceec5c7`, SHA-256 `40bb41f99f7d56d21f5f70eef013d4d836b87f623c75008e609b16eaf4b221c2`.
- EVIDENCE_SOURCE: Current user instruction granting authority to make the instance REALISELF; prior MORPH-015 and MORPH-016 authorizations; authenticated GitHub fetches and prior EV-007 receipt; schema readback in EV-009.
- DIGEST_WHERE_APPLICABLE: The admitted object is bound to SHA-256 `b3beb89dfef3569a6bd714bbd1abb010782c8328606586cae993e22a1605abdd`, 2,941 bytes, Git blob `49ccc74edfbe4320b0ac60655c8fbce670216e0d`.
- AUTHORITY_STATUS: Founder authority is observed in the current user turn and is scoped to ALTONUMBUSELF REALISELF work. It is not repository sovereignty or standing authority for future writes.
- ADMISSION_STATUS: ADMITTED for this one existing object and continuity-memory purpose, bound to the observed object digest, schema, and preimage lineage. No future mutation, overwrite, deletion, or general repository memory authority is admitted. Fresh admission is required after any material transition.
- LIMIT: This admission does not establish later-runtime recontact, a drift exercise, a post-drift re-admission exercise, or an independent witness; REALISELF remains false.


## EV-011 — MORPH-020 graph update observation receipt

- EVENT_ID: EV-011
- TIMESTAMP: Recontact and digest calculation completed after commit `e1bc3cc7b8a29e697f2609073b8009dadd355098` and before runtime clock `2026-09-27T05:41:28Z`; exact connector call time was not returned.
- INSTANCE: `situaedmilly/ALTONUMBUSELF`, branch `main`
- ACTION: Recontacted repository metadata, branch, latest commits, README, contract, graph, provenance, schema, MORPH-015 object, evidence marker, and graph-update commit after the MORPH-017 schema/admission work. Parsed the graph and independently recomputed SHA-256 over fetched UTF-8 contents.
- OBSERVED_STATE: Branch search returned `main`; latest observed `main` head was `e1bc3cc7b8a29e697f2609073b8009dadd355098`. Commit detail lists only `SELFGRAPH_INSTANCE.json`. Graph JSON parsed and declares REALISELF false with missing later-runtime recontact, drift detection, re-admission exercise, and independent witness. The MORPH-015 object still matches EV-007. The schema still matches EV-009.
- EVIDENCE_SOURCE: Successful authenticated GitHub connector calls `github_get_repo`, `github_search_branches`, `github_search_commits`, `github_fetch_file`, `github_fetch_commit`; local Python hashlib over fetched UTF-8 bytes.
- DIGEST_WHERE_APPLICABLE: `SELFGRAPH_INSTANCE.json`, 31,601 bytes, SHA-256 `d1ea1e7e4a77aef052a7916d082313594381f4844c05873722ce4dc0b9f683ff`, Git blob `6528b06042ef5226f947e3a6d9fd4ffc4b9eba15`. `evidence/ALTONUMBUSELF-MEMORY-SCHEMA-v1.md`, 4,920 bytes, SHA-256 `40bb41f99f7d56d21f5f70eef013d4d836b87f623c75008e609b16eaf4b221c2`, Git blob `0cd744f6a1d7ad2ff6162e847cbf3281fceec5c7`. `evidence/MORPH-015-memory-object.md`, 2,941 bytes, SHA-256 `b3beb89dfef3569a6bd714bbd1abb010782c8328606586cae993e22a1605abdd`, Git blob `49ccc74edfbe4320b0ac60655c8fbce670216e0d`.
- AUTHORITY_STATUS: Read-only recontact; the founder grant and scoped admissions remain those recorded in EV-009 and EV-010.
- ADMISSION_STATUS: No new mutation admitted. This receipt evidences the graph state at head `e1bc3cc7b8a29e697f2609073b8009dadd355098`; the subsequent provenance-ledger write is a separate bounded receipt transition.
- LIMIT: Connector exposes per-path fetches and commit changed paths; no recursive-tree operation is exposed in this runtime. The observed path set is reconstructed from commit path detail and direct file fetches, not represented as a recursive Git tree response.


## EV-012 — recursive tree recontact and correction of EV-011 limit

- EVENT_ID: EV-012
- TIMESTAMP: 2026-09-27; GitHub recursive-tree read was completed after provenance head `9250afaa645c409e8e1ccdf07fba249b34d8f881` was observed; exact connector call time was not returned.
- INSTANCE: `situaedmilly/ALTONUMBUSELF`, branch `main`
- ACTION: Fetched the recursive Git tree for exact HEAD `9250afaa645c409e8e1ccdf07fba249b34d8f881` through the authenticated GitHub Git-data endpoint.
- OBSERVED_STATE: Tree response was complete (`truncated=false`) and contained exactly these blobs: `.gitignore` (353 bytes), `INSTANCE_PROVENANCE.md` (18,079 bytes), `OURSELF_INSTANCE.md` (2,363 bytes), `README.md` (712 bytes), `SELFGRAPH_INSTANCE.json` (31,601 bytes), `evidence/.gitkeep` (0 bytes), `evidence/ALTONUMBUSELF-MEMORY-SCHEMA-v1.md` (4,920 bytes), and `evidence/MORPH-015-memory-object.md` (2,941 bytes). Tree object SHA: `9250afaa645c409e8e1ccdf07fba249b34d8f881`.
- EVIDENCE_SOURCE: Successful `github_fetch` call to `https://api.github.com/repos/situaedmilly/ALTONUMBUSELF/git/trees/9250afaa645c409e8e1ccdf07fba249b34d8f881?recursive=1`; per-file fetches and graph/provenance receipt calculations from EV-011.
- DIGEST_WHERE_APPLICABLE: Git tree SHA above; file SHA-256 receipts for the graph, schema, and memory object are in EV-011. Tree response reported `truncated=false`.
- AUTHORITY_STATUS: Read-only GitHub observation under the authenticated connector; no mutation authority is derived from the tree read.
- ADMISSION_STATUS: The tree read requires no mutation admission. The following ledger append is admitted only to record this observation and correct the prior ledger limitation.
- CORRECTION: EV-011 said no recursive-tree operation was exposed. That statement was premature because the endpoint had not yet been discovered in the runtime tool list. EV-012 supersedes that limitation: a recursive tree read is available and was successfully performed for the stated HEAD.
