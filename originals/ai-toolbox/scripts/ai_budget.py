#!/usr/bin/env python3
"""Estimate a fixed AI API workload from supplied USD/token prices, offline."""

import argparse
import json
import re
import sys
from decimal import Context, Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path

MAX_INPUT_BYTES = 65_536
MAX_NESTING = 8
MAX_COUNT = 1_000_000_000
MAX_DAYS = 3_660
MAX_RATE = Decimal("1000000")
MAX_BUDGET = Decimal("1000000000000")
MAX_DECIMAL_CHARACTERS = 32
DECIMAL_PATTERN = re.compile(r"(?:0|[1-9][0-9]*)(?:\.[0-9]{1,12})?\Z")
REQUIRED_FIELDS = frozenset((
    "schema_version", "input_tokens_per_request", "output_tokens_per_request",
    "requests_per_day", "days", "input_usd_per_million_tokens",
    "output_usd_per_million_tokens",
))
OPTIONAL_FIELDS = frozenset(("monthly_budget_usd", "price_basis"))


class InputError(ValueError):
    """A safe, fixed diagnostic for invalid workload input."""


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("duplicate JSON object keys are not allowed")
        result[key] = value
    return result


def _json_integer(text):
    if len(text.lstrip("-")) > 10:
        raise InputError("JSON integer exceeds the input digit limit")
    return int(text)


def _reject_float(_text):
    raise InputError("JSON fractions/exponents are not allowed; use decimal strings for USD values")


def _reject_constant(_text):
    raise InputError("non-finite JSON values are not allowed")


def _check_nesting(text):
    depth, quoted, escaped = 0, False, False
    for character in text:
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in "[{":
            depth += 1
            if depth > MAX_NESTING:
                raise InputError("JSON nesting exceeds the 8-level limit")
        elif character in "]}":
            depth -= 1


def parse_workload(raw):
    """Decode bounded UTF-8 bytes, rejecting duplicate keys and JSON floats."""
    if not isinstance(raw, bytes):
        raise InputError("input must be UTF-8 bytes")
    if len(raw) > MAX_INPUT_BYTES:
        raise InputError("input exceeds the 65536-byte limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        raise InputError("input must be valid UTF-8") from None
    _check_nesting(text)
    try:
        return json.loads(text, object_pairs_hook=_unique_object,
                          parse_int=_json_integer, parse_float=_reject_float,
                          parse_constant=_reject_constant)
    except (json.JSONDecodeError, RecursionError):
        raise InputError("input must be a valid, shallow JSON document") from None


def _count(data, field, minimum, maximum):
    value = data[field]
    if type(value) is not int or not minimum <= value <= maximum:
        raise InputError(f"{field} must be an integer from {minimum} to {maximum}")
    return value


def _usd(data, field, maximum):
    text = data[field]
    if (not isinstance(text, str) or len(text) > MAX_DECIMAL_CHARACTERS
            or not DECIMAL_PATTERN.fullmatch(text)):
        raise InputError(f"{field} must be a plain nonnegative decimal string with at most 12 fractional digits")
    value = Decimal(text)
    if not value.is_finite() or value > maximum:
        raise InputError(f"{field} exceeds the allowed USD limit")
    return value


def _decimal_text(value):
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def calculate_budget(data):
    """Return exact decimal costs and an exact whole-request budget floor."""
    if not isinstance(data, dict):
        raise InputError("workload must be a JSON object")
    if not REQUIRED_FIELDS.issubset(data):
        raise InputError("workload is missing required fields")
    if set(data) - REQUIRED_FIELDS - OPTIONAL_FIELDS:
        raise InputError("workload contains unknown fields")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise InputError("schema_version must be the integer 1")
    input_tokens = _count(data, "input_tokens_per_request", 0, MAX_COUNT)
    output_tokens = _count(data, "output_tokens_per_request", 0, MAX_COUNT)
    requests = _count(data, "requests_per_day", 0, MAX_COUNT)
    days = _count(data, "days", 1, MAX_DAYS)
    input_rate = _usd(data, "input_usd_per_million_tokens", MAX_RATE)
    output_rate = _usd(data, "output_usd_per_million_tokens", MAX_RATE)
    budget = _usd(data, "monthly_budget_usd", MAX_BUDGET) if "monthly_budget_usd" in data else None
    basis = data.get("price_basis", "user-supplied")
    if basis not in ("user-supplied", "synthetic-example"):
        raise InputError("price_basis must be user-supplied or synthetic-example")

    # Bounds keep every intermediate coefficient below 50 significant digits.
    # Precision 80 therefore retains all intermediate digits, independent of
    # the caller's Decimal context. USD rates divide by exactly 1,000,000 tokens.
    with localcontext(Context(prec=80, rounding=ROUND_HALF_UP)):
        input_cost = Decimal(input_tokens) * input_rate / Decimal(1_000_000)
        output_cost = Decimal(output_tokens) * output_rate / Decimal(1_000_000)
        request_cost = input_cost + output_cost
        daily_cost = request_cost * requests
        period_cost = daily_cost * days
        budget_result = None
        if budget is not None:
            maximum = None
            if request_cost:
                budget_numerator, budget_denominator = budget.as_integer_ratio()
                cost_numerator, cost_denominator = request_cost.as_integer_ratio()
                # Integer ratios avoid rounding a quotient across a floor boundary.
                maximum = str((budget_numerator * cost_denominator)
                              // (budget_denominator * cost_numerator))
            budget_result = {
                "amount_usd": _decimal_text(budget),
                "maximum_whole_requests": maximum,
                "request_limit": "unbounded" if request_cost == 0 else "finite",
                "modeled_period_within_budget": period_cost <= budget,
            }
        return {
            "schema_version": 1,
            "currency": "USD",
            "price_basis": basis,
            "prices_usd_per_million_tokens": {
                "input": _decimal_text(input_rate), "output": _decimal_text(output_rate),
            },
            "workload": {
                "input_tokens_per_request": input_tokens,
                "output_tokens_per_request": output_tokens,
                "requests_per_day": requests, "days": days,
                "total_requests": requests * days,
            },
            "cost_usd": {
                "input_per_request_exact": _decimal_text(input_cost),
                "output_per_request_exact": _decimal_text(output_cost),
                "per_request_exact": _decimal_text(request_cost),
                "daily_exact": _decimal_text(daily_cost),
                "period_exact": _decimal_text(period_cost),
                "daily_rounded_cents": format(daily_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f"),
                "period_rounded_cents": format(period_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f"),
            },
            "monthly_budget": budget_result,
        }


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, _message):
        self.exit(2, "error: invalid command line; use --help\n")


def main(argv=None):
    parser = SafeArgumentParser(description=__doc__)
    parser.add_argument("workload", help="UTF-8 JSON workload file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        if args.workload == "-":
            raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        else:
            with Path(args.workload).open("rb") as handle:
                raw = handle.read(MAX_INPUT_BYTES + 1)
        result = calculate_budget(parse_workload(raw))
    except InputError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except (OSError, ValueError):
        print("error: cannot read the workload file", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
