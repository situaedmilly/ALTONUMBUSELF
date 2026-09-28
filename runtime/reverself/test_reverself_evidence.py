import unittest

from independent_witness import WitnessEndpoint, evaluate_witness
from no_unwitnessed_claims import inspect_document


class NoUnwitnessedClaimsTests(unittest.TestCase):
    def test_unproven_execution_claim_is_reported(self):
        findings = inspect_document("sample.json", {"execution": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["EXECUTION_CLAIM_WITHOUT_PROCESS_PROOF"],
        )

    def test_process_proof_satisfies_execution_rule(self):
        findings = inspect_document(
            "sample.json",
            {
                "execution": True,
                "invocation": {
                    "command": ["python3", "task.py"],
                    "exit_code": 0,
                    "result": "EXECUTED",
                },
            },
        )
        self.assertEqual(findings, [])

    def test_missing_witness_link_is_reported_without_false_success(self):
        findings = inspect_document(
            "sample.json",
            {"witness": {"status": "NOT_WITNESSED", "independent_witness_ref": None}},
        )
        self.assertEqual([item["code"] for item in findings], ["WITNESS_LINK_ABSENT"])

    def test_shared_witness_boundary_is_not_independent(self):
        findings = inspect_document(
            "sample.json",
            {"independent_channel_witness": {"same_runtime": True}},
        )
        self.assertEqual([item["code"] for item in findings], ["WITNESS_NOT_INDEPENDENT"])

    def test_explicit_false_witness_flag_is_not_an_affirmative_claim(self):
        findings = inspect_document("sample.json", {"witnessed": False})
        self.assertEqual(findings, [])

    def test_affirmative_witness_claim_requires_a_link(self):
        findings = inspect_document("sample.json", {"witness_verified": True})
        self.assertEqual([item["code"] for item in findings], ["AFFIRMATIVE_WITNESS_CLAIM"])

    def test_affirmative_realiself_claim_is_reported(self):
        findings = inspect_document("sample.json", {"REALISELF": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["AFFIRMATIVE_REALISELF_CLAIM"],
        )

    def test_unproven_execution_claim_is_reported(self):
        findings = inspect_document("sample.json", {"executed": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["EXECUTION_CLAIM_WITHOUT_PROCESS_PROOF"],
        )

    def test_observed_and_observation_false_is_a_contradiction(self):
        findings = inspect_document(
            "sample.json",
            {"observed": True, "observation": False},
        )
        self.assertEqual(
            {item["code"] for item in findings},
            {
                "SEMANTIC_OBSERVATION_CONTRADICTION",
                "OBSERVED_WITHOUT_EXTERNAL_EVIDENCE",
            },
        )

    def test_undefined_temporal_label_does_not_hide_contradiction(self):
        findings = inspect_document(
            "sample.json",
            {
                "observed": True,
                "observation": False,
                "temporal_distinction": "different times",
                "observation_reference": "evidence/observation.json",
                "observation_source": "external HTTPS read",
                "observed_digest": "a" * 64,
            },
        )
        self.assertIn(
            "SEMANTIC_OBSERVATION_CONTRADICTION",
            {item["code"] for item in findings},
        )

    def test_unparseable_temporal_values_do_not_hide_contradiction(self):
        findings = inspect_document(
            "sample.json",
            {
                "subject": "sample-subject",
                "observed": True,
                "observation": False,
                "temporal_distinction": {
                    "kind": "DISTINCT_EVENT_TIMES",
                    "observed_at": "t1",
                    "observation_at": "t0",
                    "subject": "sample-subject",
                },
                "observation_reference": "evidence/observation.json",
                "observation_source": "external HTTPS read",
                "observed_digest": "a" * 64,
            },
        )
        self.assertIn(
            "SEMANTIC_OBSERVATION_CONTRADICTION",
            {item["code"] for item in findings},
        )

    def test_defined_distinct_event_times_can_separate_observation_states(self):
        findings = inspect_document(
            "sample.json",
            {
                "subject": "sample-subject",
                "observed": True,
                "observation": False,
                "temporal_distinction": {
                    "kind": "DISTINCT_EVENT_TIMES",
                    "observed_at": "2026-09-28T10:00:00Z",
                    "observation_at": "2026-09-28T10:01:00Z",
                    "subject": "sample-subject",
                },
                "observation_reference": "evidence/observation.json",
                "observation_source": "external HTTPS read",
                "observed_digest": "a" * 64,
            },
        )
        self.assertEqual(findings, [])

    def test_admission_requires_preimage(self):
        findings = inspect_document("sample.json", {"admitted": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["ADMISSION_WITHOUT_PREIMAGE"],
        )

    def test_authorization_requires_reference(self):
        findings = inspect_document("sample.json", {"authorized": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["AUTHORIZATION_WITHOUT_REFERENCE"],
        )

    def test_receipt_requires_observed_artifact(self):
        findings = inspect_document("sample.json", {"receipted": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["RECEIPT_WITHOUT_OBSERVED_ARTIFACT"],
        )

    def test_recontact_requires_persisted_subject(self):
        findings = inspect_document("sample.json", {"recontacted": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["RECONTACT_WITHOUT_PERSISTED_SUBJECT"],
        )

    def test_present_state_requires_realization_evidence(self):
        findings = inspect_document("sample.json", {"state": "PRESENT"})
        self.assertEqual(
            [item["code"] for item in findings],
            ["PRESENT_WITHOUT_REALIZATION_EVIDENCE"],
        )

    def test_affirmative_witness_requires_reference(self):
        findings = inspect_document("sample.json", {"witnessed": True})
        self.assertEqual(
            [item["code"] for item in findings],
            ["AFFIRMATIVE_WITNESS_CLAIM"],
        )


class IndependentWitnessTests(unittest.TestCase):
    def setUp(self):
        self.primary = WitnessEndpoint(
            "operator-a", "channel-a", "runtime-a", "host-a",
            "artifact.json", "a" * 64, "evidence/primary.json", True,
        )

    def test_unavailable_witness_is_blocked(self):
        result = evaluate_witness("artifact.json", "a" * 64, self.primary, None)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertFalse(result["independent_witness_verified"])

    def test_shared_identity_is_not_independent(self):
        witness = WitnessEndpoint(
            "operator-a", "channel-b", "runtime-b", "host-b",
            "artifact.json", "a" * 64, "evidence/witness.json", True,
        )
        result = evaluate_witness("artifact.json", "a" * 64, self.primary, witness)
        self.assertEqual(result["decision"], "BLOCKED")

    def test_digest_mismatch_is_refused(self):
        witness = WitnessEndpoint(
            "operator-b", "channel-b", "runtime-b", "host-b",
            "artifact.json", "b" * 64, "evidence/witness.json", True,
        )
        result = evaluate_witness("artifact.json", "a" * 64, self.primary, witness)
        self.assertEqual(result["decision"], "REFUSED")

    def test_incomplete_endpoint_is_blocked(self):
        witness = WitnessEndpoint(
            "", "channel-b", "runtime-b", "host-b",
            "artifact.json", "a" * 64, "evidence/witness.json", True,
        )
        result = evaluate_witness("artifact.json", "a" * 64, self.primary, witness)
        self.assertEqual(result["decision"], "BLOCKED")

    def test_fully_distinct_matching_endpoint_can_pass_in_fixture(self):
        witness = WitnessEndpoint(
            "operator-b", "channel-b", "runtime-b", "host-b",
            "artifact.json", "a" * 64, "evidence/witness.json", True,
        )
        result = evaluate_witness("artifact.json", "a" * 64, self.primary, witness)
        self.assertEqual(result["decision"], "VERIFIED")
        self.assertTrue(result["independent_witness_verified"])


if __name__ == "__main__":
    unittest.main()
