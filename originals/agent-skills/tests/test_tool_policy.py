"""Synthetic offline decision tests; no authenticated users or executed tools."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "tool_policy.py"
SPEC = importlib.util.spec_from_file_location("tool_policy", SCRIPT)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)
NOW = "2030-01-01T00:00:00Z"
REQUEST = {"principal": "operator.demo", "action": "server.status", "resource": "game.demo"}


def fixture_inputs(case, fixture):
    default_policy = (ROOT / "examples" / fixture["policy_file"]).read_text(encoding="utf-8")
    policy_text = case.get("policy_text", default_policy)
    request_text = case.get("request_text", json.dumps(case.get("request", {})))
    return policy_text, request_text, case.get("now", fixture["now"])


class ToolPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = gate.load_json((ROOT / "examples" / "policy.json").read_text(encoding="utf-8"))

    def deny(self, policy=None, request=None, now=NOW, reason="INVALID_POLICY"):
        result = gate.evaluate(self.policy if policy is None else policy,
                               REQUEST if request is None else request, now)
        self.assertEqual(result, {"allowed": False, "reason": reason})

    def test_synthetic_expected_decisions(self):
        fixture = json.loads((ROOT / "examples" / "decision-fixtures.json").read_text(encoding="utf-8"))
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                policy_text, request_text, now = fixture_inputs(case, fixture)
                try:
                    result = gate.evaluate(gate.load_json(policy_text), gate.load_json(request_text), now)
                except gate.GateError as error:
                    result = {"allowed": False, "reason": str(error)}
                self.assertEqual(result, case["expected_decision"])

    def test_allow_is_deterministic_and_inputs_are_not_mutated(self):
        original = copy.deepcopy(self.policy)
        request = copy.deepcopy(REQUEST)
        expected = {"allowed": True, "reason": "ALLOW"}
        self.assertEqual(gate.evaluate(self.policy, request, NOW), expected)
        self.assertEqual(gate.evaluate(self.policy, request, NOW), expected)
        self.assertEqual(self.policy, original)
        self.assertEqual(request, REQUEST)

    def test_empty_grants_deny_by_default(self):
        self.deny(policy={"version": 1, "grants": []}, reason="NO_PRINCIPAL_GRANT")

    def test_exact_case_sensitive_identifiers_do_not_inherit_access(self):
        for key, value, reason in (("principal", "Operator.demo", "NO_PRINCIPAL_GRANT"),
                                   ("action", "Server.status", "ACTION_DENIED"),
                                   ("resource", "game.demo/child", "RESOURCE_DENIED")):
            with self.subTest(key=key):
                request = dict(REQUEST, **{key: value})
                self.deny(request=request, reason=reason)

    def test_no_cross_grant_action_resource_combination(self):
        policy = {"version": 1, "grants": [
            {"principal": "operator.demo", "actions": ["server.status"], "resources": ["game.other"]},
            {"principal": "operator.demo", "actions": ["config.write"], "resources": ["game.demo"]},
        ]}
        self.deny(policy=policy, reason="RESOURCE_DENIED")

    def test_expiry_is_exclusive_at_exact_second(self):
        request = dict(REQUEST, action="config.write")
        self.assertTrue(gate.evaluate(self.policy, request, "2030-01-01T00:59:59Z")["allowed"])
        self.deny(request=request, now="2030-01-01T01:00:00Z", reason="GRANT_EXPIRED")
        self.deny(request=request, now="2031-01-01T00:00:00Z", reason="GRANT_EXPIRED")

    def test_unexpired_matching_grant_wins_over_expired_match(self):
        base = {"principal": "operator.demo", "actions": ["server.status"], "resources": ["game.demo"]}
        policy = {"version": 1, "grants": [dict(base, expires_at="2029-01-01T00:00:00Z"), base]}
        self.assertTrue(gate.evaluate(policy, REQUEST, NOW)["allowed"])
        policy["grants"].reverse()
        self.assertTrue(gate.evaluate(policy, REQUEST, NOW)["allowed"])

    def test_every_grant_is_validated_before_allowing(self):
        self.policy["grants"].append({"principal": "unrelated.demo", "actions": ["*"], "resources": ["game.demo"]})
        self.deny()

    def test_unknown_policy_and_grant_fields_fail_closed(self):
        altered = copy.deepcopy(self.policy)
        altered["default_allow"] = True
        self.deny(policy=altered)
        altered = copy.deepcopy(self.policy)
        altered["grants"][0]["effect"] = "allow"
        self.deny(policy=altered)

    def test_malformed_policy_shapes_fail_closed(self):
        for policy in ([], {}, {"version": 1}, {"version": True, "grants": []},
                       {"version": 2, "grants": []}, {"version": 1, "grants": {}},
                       {"version": 1, "grants": [None]},
                       {"version": 1, "grants": [{"principal": "operator.demo"}]}):
            with self.subTest(policy=policy):
                self.deny(policy=policy)

    def test_invalid_patterns_unicode_and_unbounded_identifiers_are_rejected(self):
        for invalid in ("*", "game.*", "[ab]", "", " name", "ชื่อสมมติ", "x" * 129, None, True):
            with self.subTest(invalid=invalid):
                policy = copy.deepcopy(self.policy)
                policy["grants"][0]["resources"] = [invalid]
                self.deny(policy=policy)
                self.deny(request=dict(REQUEST, resource=invalid), reason="INVALID_REQUEST")

    def test_grant_collection_limits_and_duplicate_identifiers(self):
        for resources in ([], ["game.demo", "game.demo"], ["g" + str(i) for i in range(65)], "game.demo"):
            with self.subTest(resources=resources):
                policy = copy.deepcopy(self.policy)
                policy["grants"][0]["resources"] = resources
                self.deny(policy=policy)
        self.deny(policy={"version": 1, "grants": [self.policy["grants"][0]] * 257})

    def test_identifier_and_collection_boundaries_are_accepted(self):
        long_id = "x" * gate.MAX_ID_LENGTH
        grant = {"principal": long_id, "actions": ["a" + str(i) for i in range(64)],
                 "resources": ["r" + str(i) for i in range(64)]}
        policy = {"version": 1, "grants": [grant] * 256}
        request = {"principal": long_id, "action": "a63", "resource": "r63"}
        self.assertTrue(gate.evaluate(policy, request, NOW)["allowed"])

    def test_request_has_no_authority_to_add_approval_or_permissions(self):
        for request in ({}, [], dict(REQUEST, approved=True), dict(REQUEST, expires_at=NOW),
                        dict(REQUEST, roles=["admin"]), dict(REQUEST, payload="SYNTHETIC-SECRET")):
            with self.subTest(request=request):
                self.deny(request=request, reason="INVALID_REQUEST")

    def test_now_and_policy_dates_require_explicit_canonical_utc(self):
        invalid_dates = (None, "", "2030-1-1T00:00:00Z", "2030-01-01T00:00:00+00:00",
                         "2030-01-01T00:00:00.000Z", "2030-02-30T00:00:00Z",
                         "2030-01-01T00:00:60Z", "2030-01-01t00:00:00z")
        for value in invalid_dates:
            with self.subTest(date=value):
                self.deny(now=value, reason="INVALID_NOW")
                policy = copy.deepcopy(self.policy)
                policy["grants"][0]["expires_at"] = value
                self.deny(policy=policy)


class JSONInputTests(unittest.TestCase):
    def test_duplicate_keys_are_rejected_at_every_level(self):
        for text in ('{"version":1,"version":1,"grants":[]}',
                     '{"grants":[{"principal":"a","principal":"b"}]}',
                     '{"principal":"a","principal":"b"}'):
            with self.assertRaises(gate.GateError) as caught:
                gate.load_json(text)
            self.assertEqual(str(caught.exception), "INVALID_JSON")

    def test_malformed_and_unsupported_json_is_rejected(self):
        for text in ("", "{} {}", "{broken", "NaN", "Infinity", "1.0", "9" * 11, "\ud800"):
            with self.subTest(kind=len(text)):
                with self.assertRaises(gate.GateError):
                    gate.load_json(text)

    def test_byte_and_depth_budgets_are_enforced(self):
        self.assertEqual(gate.load_json("{}" + " " * (gate.MAX_BYTES - 2)), {})
        for text in ("{}" + " " * gate.MAX_BYTES, '"' + "ก" * gate.MAX_BYTES + '"',
                     "[" * (gate.MAX_DEPTH + 1) + "]" * (gate.MAX_DEPTH + 1)):
            with self.assertRaises(gate.GateError):
                gate.load_json(text)
        text = "[" * gate.MAX_DEPTH + "]" * gate.MAX_DEPTH
        self.assertIsInstance(gate.load_json(text), list)

    def test_quoted_brackets_do_not_consume_depth_budget(self):
        self.assertEqual(gate.load_json('"[[[{\\\"x\\\"}]]]"'), '[[[{"x"}]]]')


class ToolPolicyCLITests(unittest.TestCase):
    def command(self, policy_path=None, request_path=None, now=NOW, data=None, extra=()):
        command = [sys.executable, str(SCRIPT), "--policy", str(policy_path or ROOT / "examples" / "policy.json"),
                   "--now", now]
        if request_path is not None:
            command += ["--request", str(request_path)]
        return subprocess.run(command + list(extra), input=data, capture_output=True, timeout=10)

    def assert_decision(self, result, expected, status):
        self.assertEqual(result.returncode, status)
        self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(result.stderr, b"")
        self.assertNotIn(b"SYNTHETIC-SECRET", result.stdout)

    def test_quickstart_file_command(self):
        self.assert_decision(self.command(request_path=ROOT / "examples" / "request-allow.json"),
                             {"allowed": True, "reason": "ALLOW"}, 0)

    def test_stdin_and_denial_have_distinct_exit_status(self):
        self.assert_decision(self.command(data=json.dumps(REQUEST).encode()),
                             {"allowed": True, "reason": "ALLOW"}, 0)
        self.assert_decision(self.command(request_path=ROOT / "examples" / "request-deny.json"),
                             {"allowed": False, "reason": "ACTION_DENIED"}, 1)

    def test_every_fixture_has_matching_cli_decision_and_status(self):
        fixture = json.loads((ROOT / "examples" / "decision-fixtures.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            policy_path = Path(directory) / "policy.json"
            for case in fixture["cases"]:
                with self.subTest(case=case["id"]):
                    policy_text, request_text, now = fixture_inputs(case, fixture)
                    policy_path.write_text(policy_text, encoding="utf-8")
                    expected = case["expected_decision"]
                    status = 0 if expected["allowed"] else (2 if expected["reason"].startswith("INVALID_") else 1)
                    self.assert_decision(self.command(policy_path=policy_path, now=now,
                                                      data=request_text.encode()), expected, status)

    def test_invalid_input_never_echoes_supplied_payload(self):
        for raw in (b'{"SYNTHETIC-SECRET":', b'\xff', b'{"principal":"a","principal":"SYNTHETIC-SECRET"}',
                    json.dumps(dict(REQUEST, payload="SYNTHETIC-SECRET")).encode()):
            result = self.command(data=raw)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stdout)["allowed"])
            self.assertNotIn(b"SYNTHETIC-SECRET", result.stdout + result.stderr)
            self.assertNotIn(b"Traceback", result.stdout + result.stderr)

    def test_invalid_arguments_and_now_never_echo_values(self):
        self.assert_decision(self.command(data=b"{}", extra=("--SYNTHETIC-SECRET",)),
                             {"allowed": False, "reason": "INVALID_ARGUMENTS"}, 2)
        self.assert_decision(self.command(data=json.dumps(REQUEST).encode(), now="SYNTHETIC-SECRET"),
                             {"allowed": False, "reason": "INVALID_NOW"}, 2)

    def test_io_error_is_distinct_and_does_not_disclose_path(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.command(policy_path=Path(directory) / "SYNTHETIC-SECRET", data=b"{}")
        self.assert_decision(result, {"allowed": False, "reason": "IO_ERROR"}, 3)

    def test_output_is_byte_stable_for_identical_inputs(self):
        first = self.command(data=json.dumps(REQUEST).encode())
        second = self.command(data=json.dumps(REQUEST).encode())
        self.assertEqual(first.stdout, second.stdout)


if __name__ == "__main__":
    unittest.main()
