"""Offline arithmetic, input-boundary and CLI tests for the original calculator."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Inexact, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ai_budget.py"
SPEC = importlib.util.spec_from_file_location("ai_budget", SCRIPT)
ai_budget = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ai_budget)


def workload():
    return json.loads((ROOT / "examples" / "workload.json").read_text(encoding="utf-8"))


class BudgetMathTests(unittest.TestCase):
    def test_token_units_daily_and_period_costs(self):
        result = ai_budget.calculate_budget(workload())
        self.assertEqual(result["cost_usd"], {
            "input_per_request_exact": "0.002", "output_per_request_exact": "0.004",
            "per_request_exact": "0.006", "daily_exact": "0.6", "period_exact": "18",
            "daily_rounded_cents": "0.60", "period_rounded_cents": "18.00",
        })
        self.assertEqual(result["workload"]["total_requests"], 3000)
        self.assertEqual(result["monthly_budget"]["maximum_whole_requests"], "2000")
        self.assertFalse(result["monthly_budget"]["modeled_period_within_budget"])

    def test_affordability_floors_exactly_at_and_below_a_boundary(self):
        data = workload()
        data.update(input_tokens_per_request=100_000, output_tokens_per_request=0,
                    input_usd_per_million_tokens="3", output_usd_per_million_tokens="0")
        for budget, expected in (("0.9", "3"), ("0.899999999999", "2")):
            with self.subTest(budget=budget):
                data["monthly_budget_usd"] = budget
                result = ai_budget.calculate_budget(data)
                self.assertEqual(result["cost_usd"]["per_request_exact"], "0.3")
                self.assertEqual(result["monthly_budget"]["maximum_whole_requests"], expected)

    def test_subcent_costs_do_not_use_display_rounding_for_budget(self):
        data = workload()
        data.update(input_tokens_per_request=200, output_tokens_per_request=0,
                    requests_per_day=1, input_usd_per_million_tokens="2",
                    output_usd_per_million_tokens="0", monthly_budget_usd="0.01")
        result = ai_budget.calculate_budget(data)
        self.assertEqual(result["cost_usd"]["per_request_exact"], "0.0004")
        self.assertEqual(result["cost_usd"]["daily_rounded_cents"], "0.00")
        self.assertEqual(result["monthly_budget"]["maximum_whole_requests"], "25")

    def test_rounding_is_half_up_and_only_for_cents_display(self):
        data = workload()
        data.update(input_tokens_per_request=5000, output_tokens_per_request=0,
                    requests_per_day=1, days=3, input_usd_per_million_tokens="1")
        result = ai_budget.calculate_budget(data)
        self.assertEqual(result["cost_usd"]["daily_exact"], "0.005")
        self.assertEqual(result["cost_usd"]["period_exact"], "0.015")
        self.assertEqual(result["cost_usd"]["daily_rounded_cents"], "0.01")
        self.assertEqual(result["cost_usd"]["period_rounded_cents"], "0.02")

    def test_smallest_rate_and_large_affordability_remain_exact(self):
        data = workload()
        data.update(input_tokens_per_request=1, output_tokens_per_request=0,
                    input_usd_per_million_tokens="0.000000000001",
                    monthly_budget_usd="1000000000000")
        result = ai_budget.calculate_budget(data)
        self.assertEqual(result["cost_usd"]["per_request_exact"], "0.000000000000000001")
        self.assertEqual(result["monthly_budget"]["maximum_whole_requests"], "1" + "0" * 30)

    def test_maximum_inputs_ignore_callers_decimal_context(self):
        data = workload()
        data.update(input_tokens_per_request=ai_budget.MAX_COUNT,
                    output_tokens_per_request=ai_budget.MAX_COUNT,
                    requests_per_day=ai_budget.MAX_COUNT, days=ai_budget.MAX_DAYS,
                    input_usd_per_million_tokens="1000000",
                    output_usd_per_million_tokens="1000000")
        with localcontext() as context:
            context.prec = 2
            context.Emax = 3
            context.traps[Inexact] = True
            result = ai_budget.calculate_budget(data)
        expected_daily = 2 * ai_budget.MAX_COUNT * ai_budget.MAX_COUNT
        self.assertEqual(result["cost_usd"]["daily_exact"], str(expected_daily))
        self.assertEqual(result["cost_usd"]["period_exact"], str(expected_daily * ai_budget.MAX_DAYS))

    def test_large_counts_with_twelve_digit_rates_preserve_carry_and_budget_floor(self):
        data = workload()
        data.update(input_tokens_per_request=ai_budget.MAX_COUNT,
                    output_tokens_per_request=ai_budget.MAX_COUNT,
                    requests_per_day=ai_budget.MAX_COUNT, days=ai_budget.MAX_DAYS,
                    input_usd_per_million_tokens="999999.999999999999",
                    output_usd_per_million_tokens="0.000000000001",
                    monthly_budget_usd="999999999999.999999999999")
        result = ai_budget.calculate_budget(data)
        self.assertEqual(result["cost_usd"]["per_request_exact"], "1000000000")
        self.assertEqual(result["cost_usd"]["period_exact"], str(10 ** 18 * ai_budget.MAX_DAYS))
        self.assertEqual(result["monthly_budget"]["maximum_whole_requests"], "999")

    def test_zero_cost_missing_budget_and_zero_budget_are_distinct(self):
        data = workload()
        data["monthly_budget_usd"] = "0"
        self.assertEqual(ai_budget.calculate_budget(data)["monthly_budget"]["maximum_whole_requests"], "0")
        for change in ({"input_tokens_per_request": 0, "output_tokens_per_request": 0},
                       {"input_usd_per_million_tokens": "0", "output_usd_per_million_tokens": "0"}):
            with self.subTest(change=change):
                free = dict(data, **change)
                result = ai_budget.calculate_budget(free)
                self.assertEqual(result["monthly_budget"]["request_limit"], "unbounded")
                self.assertIsNone(result["monthly_budget"]["maximum_whole_requests"])
                self.assertTrue(result["monthly_budget"]["modeled_period_within_budget"])
        del data["monthly_budget_usd"]
        self.assertIsNone(ai_budget.calculate_budget(data)["monthly_budget"])

    def test_zero_planned_requests_preserves_finite_affordability(self):
        data = workload()
        data["requests_per_day"] = 0
        result = ai_budget.calculate_budget(data)
        self.assertEqual(result["cost_usd"]["period_exact"], "0")
        self.assertEqual(result["monthly_budget"]["request_limit"], "finite")
        self.assertEqual(result["monthly_budget"]["maximum_whole_requests"], "2000")


class BudgetInputTests(unittest.TestCase):
    def test_counts_require_bounded_integers_and_reject_booleans(self):
        for field in ("input_tokens_per_request", "output_tokens_per_request", "requests_per_day", "days"):
            maximum = ai_budget.MAX_DAYS if field == "days" else ai_budget.MAX_COUNT
            for value in (True, False, 1.0, "1", None, [], {}, -1, maximum + 1):
                with self.subTest(field=field, value=value):
                    data = workload()
                    data[field] = value
                    with self.assertRaises(ai_budget.InputError):
                        ai_budget.calculate_budget(data)
        data = workload()
        data["days"] = 0
        with self.assertRaises(ai_budget.InputError):
            ai_budget.calculate_budget(data)

    def test_decimal_values_have_strict_grammar_and_bounds(self):
        for field in ("input_usd_per_million_tokens", "output_usd_per_million_tokens", "monthly_budget_usd"):
            for value in (True, 1, 0.25, None, [], {}, "", " 1", "1 ", "+1", "-0", "-1",
                          "1e2", "1_000", "00.5", ".5", "1.", "NaN", "Infinity",
                          "0.0000000000001", "9" * 33):
                with self.subTest(field=field, value=value):
                    data = workload()
                    data[field] = value
                    with self.assertRaises(ai_budget.InputError):
                        ai_budget.calculate_budget(data)
            data = workload()
            data[field] = "1000000000000.000000000001" if field == "monthly_budget_usd" else "1000000.000000000001"
            with self.subTest(field=field, above_limit=True), self.assertRaises(ai_budget.InputError):
                ai_budget.calculate_budget(data)

    def test_root_required_unknown_and_version_fields(self):
        for value in (None, [], "workload", 1, True):
            with self.subTest(value=value), self.assertRaises(ai_budget.InputError):
                ai_budget.calculate_budget(value)
        for field in ai_budget.REQUIRED_FIELDS:
            data = workload()
            del data[field]
            with self.subTest(missing=field), self.assertRaises(ai_budget.InputError):
                ai_budget.calculate_budget(data)
        for change in ({"unknown": "private-marker"}, {"schema_version": True},
                       {"schema_version": 1.0}, {"schema_version": 2}, {"price_basis": []}):
            with self.subTest(change=change), self.assertRaises(ai_budget.InputError):
                ai_budget.calculate_budget(dict(workload(), **change))

    def test_parser_rejects_duplicates_floats_nonfinite_and_huge_integers(self):
        for raw in (b'{"days": 1, "days": 2}', b'{"nested":{"a":1,"a":2}}',
                    b'{"days":1.0}', b'{"days":1e2}', b'{"days":NaN}',
                    b'{"days":Infinity}', b'{"days":-Infinity}', b'{"days":12345678901}'):
            with self.subTest(raw=raw), self.assertRaises(ai_budget.InputError):
                ai_budget.parse_workload(raw)

    def test_input_size_encoding_syntax_and_nesting_are_bounded(self):
        at_limit = b"{}" + b" " * (ai_budget.MAX_INPUT_BYTES - 2)
        self.assertEqual(ai_budget.parse_workload(at_limit), {})
        for raw in (at_limit + b" ", b"\xff", b"not JSON", b"[" * 2000 + b"]" * 2000):
            with self.subTest(size=len(raw)), self.assertRaises(ai_budget.InputError):
                ai_budget.parse_workload(raw)
        self.assertEqual(ai_budget.parse_workload(b'{"text":"[[[[[[[[[[\\\"{"}'),
                         {"text": '[[[[[[[[[["{'})


class BudgetCliTests(unittest.TestCase):
    def test_file_and_stdin_match_committed_expected_output(self):
        expected = (ROOT / "examples" / "workload.expected.json").read_bytes()
        for argument, stdin in ((str(ROOT / "examples" / "workload.json"), None),
                                ("-", (ROOT / "examples" / "workload.json").read_bytes())):
            with self.subTest(argument=argument):
                result = subprocess.run([sys.executable, "-B", str(SCRIPT), argument],
                                        input=stdin, capture_output=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, b"")
                self.assertEqual(result.stdout, expected)

    def test_invalid_cli_input_has_nonzero_status_and_sanitized_errors(self):
        marker = "PRIVATE-MARKER-DO-NOT-ECHO"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / (marker + ".json")
            path.write_text('{"unknown":"' + marker + '"}', encoding="utf-8")
            for args in ([str(path)], [str(path) + ".missing"], ["--" + marker]):
                with self.subTest(args=args):
                    result = subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                                            capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertTrue(result.stderr.startswith("error: "))
                    self.assertNotIn(marker, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
        oversized = subprocess.run([sys.executable, "-B", str(SCRIPT), "-"],
                                   input=b" " * (ai_budget.MAX_INPUT_BYTES + 1), capture_output=True)
        self.assertEqual(oversized.returncode, 2)
        self.assertEqual(oversized.stdout, b"")


if __name__ == "__main__":
    unittest.main()
