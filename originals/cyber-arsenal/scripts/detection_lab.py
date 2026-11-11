"""Offline detection of denied-access and rejected-replay bursts in synthetic logs."""

import argparse
from collections import deque
from datetime import datetime
import json
from pathlib import Path
import re
import sys


MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_EVENTS = 10000
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class DetectionError(ValueError):
    """The input does not meet the documented event contract."""


def _identifier(value, field, index):
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise DetectionError(f"event {index}: {field} must be a nonempty string of at most 128 characters")


def validate_events(document):
    if not isinstance(document, dict) or type(document.get("schema_version")) is not int or document["schema_version"] != 1:
        raise DetectionError("input must be an object with schema_version 1")
    events = document.get("events")
    if not isinstance(events, list) or len(events) > MAX_EVENTS:
        raise DetectionError(f"events must be an array of at most {MAX_EVENTS} records")
    result, seen, previous = [], set(), None
    for index, event in enumerate(events, 1):
        if not isinstance(event, dict):
            raise DetectionError(f"event {index}: expected an object")
        for field in ("event_id", "actor", "timestamp", "action", "outcome"):
            if field not in event:
                raise DetectionError(f"event {index}: missing {field}")
        for field in ("event_id", "actor"):
            _identifier(event[field], field, index)
        if event["event_id"] in seen:
            raise DetectionError(f"event {index}: duplicate event_id")
        seen.add(event["event_id"])
        timestamp = event["timestamp"]
        if not isinstance(timestamp, str) or not TIMESTAMP.fullmatch(timestamp):
            raise DetectionError(f"event {index}: timestamp must use UTC YYYY-MM-DDTHH:MM:SSZ")
        try:
            instant = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as exc:
            raise DetectionError(f"event {index}: invalid timestamp") from exc
        if previous is not None and instant < previous:
            raise DetectionError(f"event {index}: events must be sorted by timestamp")
        previous = instant
        if event["action"] not in ("object_access", "replay_check"):
            raise DetectionError(f"event {index}: unsupported action")
        if event["outcome"] not in ("allowed", "denied"):
            raise DetectionError(f"event {index}: unsupported outcome")
        detail = "object_id" if event["action"] == "object_access" else "request_id"
        if detail not in event:
            raise DetectionError(f"event {index}: missing {detail}")
        _identifier(event[detail], detail, index)
        result.append((instant, event))
    return result


def detect(document, window_seconds=60, threshold=3):
    """Return deterministic alerts; the window includes both boundary seconds."""
    if type(window_seconds) is not int or not 1 <= window_seconds <= 86400:
        raise DetectionError("window_seconds must be an integer from 1 to 86400")
    if type(threshold) is not int or not 2 <= threshold <= 1000:
        raise DetectionError("threshold must be an integer from 2 to 1000")
    events = validate_events(document)  # Validate the whole batch before emitting alerts.
    windows, alerts = {}, []
    for instant, event in events:
        if event["outcome"] != "denied":
            continue
        if event["action"] == "object_access":
            rule, group = "denied_object_access_burst", {"actor": event["actor"]}
            key = (rule, event["actor"])
        else:
            rule = "rejected_replay_burst"
            group = {"actor": event["actor"], "request_id": event["request_id"]}
            key = (rule, event["actor"], event["request_id"])
        window = windows.setdefault(key, deque())
        while window and (instant - window[0][0]).total_seconds() > window_seconds:
            window.popleft()
        previous_count = len(window)
        window.append((instant, event))
        # Alert once on crossing the threshold. Rearm only after the window shrinks.
        if previous_count < threshold <= len(window):
            alert = {
                "rule": rule, "group": group, "count": len(window),
                "first_seen": window[0][1]["timestamp"], "last_seen": event["timestamp"],
                "event_ids": [item[1]["event_id"] for item in window],
            }
            if rule == "denied_object_access_burst":
                alert["object_ids"] = sorted({item[1]["object_id"] for item in window})
            alerts.append(alert)
    return {
        "schema_version": 1, "event_count": len(events), "window_seconds": window_seconds,
        "threshold": threshold, "alerts": alerts,
    }


def read_json(path):
    try:
        with Path(path).open("rb") as stream:
            raw = stream.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise DetectionError("input exceeds the 2 MiB budget")
        return json.loads(raw)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        if isinstance(exc, DetectionError):
            raise
        raise DetectionError("could not read valid JSON input") from exc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--window-seconds", default=60, type=int)
    parser.add_argument("--threshold", default=3, type=int)
    parser.add_argument("--expect", type=Path, help="Compare alerts with this expected JSON array")
    args = parser.parse_args(argv)
    try:
        report = detect(read_json(args.input), args.window_seconds, args.threshold)
        status = 0
        if args.expect is not None:
            expected = read_json(args.expect)
            if not isinstance(expected, list):
                raise DetectionError("expected alerts must be a JSON array")
            report["expectations_match"] = expected == report["alerts"]
            status = 0 if report["expectations_match"] else 1
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return status
    except DetectionError as exc:
        print(json.dumps({"error": str(exc), "status": "invalid_input"}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
