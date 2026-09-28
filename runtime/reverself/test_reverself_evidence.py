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

    def test_explicit_false_witness_flag_is_not_an_affirmative_claim(self):
        findings = inspect_document("sample.json", {"witnessed": False})
        self.assertEqual(findings, [])


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
