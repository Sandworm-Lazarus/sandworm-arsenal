#!/usr/bin/env python3
"""Offline, deny-by-default tool authorization decisions; never execute tools."""

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Optional


MAX_BYTES = 65536
MAX_DEPTH = 8
MAX_GRANTS = 256
MAX_IDENTIFIERS = 64
MAX_ID_LENGTH = 128
_FIRST = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
_IDENTIFIER = _FIRST | frozenset("_.:/-")
_DIGITS = frozenset("0123456789")


class GateError(ValueError):
    """A fixed reason code, never a supplied identifier or payload."""


def _identifier(value: Any) -> bool:
    return (type(value) is str and 1 <= len(value) <= MAX_ID_LENGTH
            and value[0] in _FIRST and all(char in _IDENTIFIER for char in value))


def _timestamp(value: Any, reason: str) -> datetime:
    if (type(value) is not str or len(value) != 20
            or any(value[index] != char for index, char in
                   ((4, "-"), (7, "-"), (10, "T"), (13, ":"), (16, ":"), (19, "Z")))
            or any(char not in _DIGITS for index, char in enumerate(value)
                   if index not in (4, 7, 10, 13, 16, 19))):
        raise GateError(reason)
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        raise GateError(reason) from None


def _identifier_list(value: Any) -> bool:
    return (type(value) is list and 1 <= len(value) <= MAX_IDENTIFIERS
            and all(_identifier(item) for item in value)
            and len(set(value)) == len(value))


def _validate_policy(policy: Any) -> None:
    if (type(policy) is not dict or set(policy) != {"version", "grants"}
            or type(policy["version"]) is not int or policy["version"] != 1
            or type(policy["grants"]) is not list or len(policy["grants"]) > MAX_GRANTS):
        raise GateError("INVALID_POLICY")
    required = {"principal", "actions", "resources"}
    for grant in policy["grants"]:
        if (type(grant) is not dict or not required.issubset(grant)
                or set(grant) - required - {"expires_at"}
                or not _identifier(grant["principal"])
                or not _identifier_list(grant["actions"])
                or not _identifier_list(grant["resources"])):
            raise GateError("INVALID_POLICY")
        if "expires_at" in grant:
            _timestamp(grant["expires_at"], "INVALID_POLICY")


def evaluate(policy: Any, request: Any, now: str) -> dict:
    """Return {allowed: bool, reason: str}, validating every grant first.

    Identifiers match exactly and case-sensitively. The caller must obtain the
    principal from trusted authenticated server context. No authentication,
    signatures, execution, policy fetching, or system-clock access occurs here.
    """
    try:
        _validate_policy(policy)
        if (type(request) is not dict or set(request) != {"principal", "action", "resource"}
                or not all(_identifier(request[key]) for key in request)):
            raise GateError("INVALID_REQUEST")
        instant = _timestamp(now, "INVALID_NOW")
    except GateError as error:
        return {"allowed": False, "reason": str(error)}

    candidates = [grant for grant in policy["grants"]
                  if grant["principal"] == request["principal"]]
    if not candidates:
        return {"allowed": False, "reason": "NO_PRINCIPAL_GRANT"}
    candidates = [grant for grant in candidates if request["action"] in grant["actions"]]
    if not candidates:
        return {"allowed": False, "reason": "ACTION_DENIED"}
    candidates = [grant for grant in candidates if request["resource"] in grant["resources"]]
    if not candidates:
        return {"allowed": False, "reason": "RESOURCE_DENIED"}
    if all("expires_at" in grant
           and instant >= _timestamp(grant["expires_at"], "INVALID_POLICY")
           for grant in candidates):
        return {"allowed": False, "reason": "GRANT_EXPIRED"}
    return {"allowed": True, "reason": "ALLOW"}


def _reject_number(_value: str) -> None:
    raise GateError("INVALID_JSON")


def _parse_integer(value: str) -> int:
    if len(value.lstrip("-")) > 10:
        raise GateError("INVALID_JSON")
    return int(value)


def _unique_object(pairs: Any) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise GateError("INVALID_JSON")
        result[key] = value
    return result


def load_json(text: str) -> Any:
    """Strict bounded JSON parsing; duplicate keys and floats are unsupported."""
    if type(text) is not str or len(text) > MAX_BYTES:
        raise GateError("INVALID_JSON")
    try:
        if len(text.encode("utf-8")) > MAX_BYTES:
            raise GateError("INVALID_JSON")
    except UnicodeEncodeError:
        raise GateError("INVALID_JSON") from None
    level, quoted, escaped = 0, False, False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            level += 1
            if level > MAX_DEPTH:
                raise GateError("INVALID_JSON")
        elif char in "]}":
            level -= 1
    try:
        return json.loads(text, object_pairs_hook=_unique_object,
                          parse_constant=_reject_number, parse_float=_reject_number,
                          parse_int=_parse_integer)
    except GateError:
        raise
    except (ValueError, RecursionError, OverflowError):
        raise GateError("INVALID_JSON") from None


def _read_document(path: Optional[str]) -> Any:
    if path is None:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
    else:
        with open(path, "rb") as source:
            raw = source.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise GateError("INVALID_JSON")
    try:
        return load_json(raw.decode("utf-8"))
    except UnicodeDecodeError:
        raise GateError("INVALID_JSON") from None


class _Parser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        raise GateError("INVALID_ARGUMENTS")


def main(argv: Optional[list] = None) -> int:
    parser = _Parser(description=__doc__)
    parser.add_argument("--policy", required=True, metavar="PATH")
    parser.add_argument("--request", metavar="PATH", help="request JSON file; default stdin")
    parser.add_argument("--now", required=True, metavar="UTC", help="YYYY-MM-DDTHH:MM:SSZ")
    try:
        args = parser.parse_args(argv)
        policy = _read_document(args.policy)
        request = _read_document(args.request)
        result = evaluate(policy, request, args.now)
        status = 0 if result["allowed"] else (2 if result["reason"].startswith("INVALID_") else 1)
    except GateError as error:
        result, status = {"allowed": False, "reason": str(error)}, 2
    except OSError:
        result, status = {"allowed": False, "reason": "IO_ERROR"}, 3
    try:
        sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
        sys.stdout.flush()
    except OSError:
        try:
            sys.stdout.close()
        except OSError:
            pass
        return 3
    return status


if __name__ == "__main__":
    sys.exit(main())
