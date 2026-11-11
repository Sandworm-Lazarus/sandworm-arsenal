# Original tool: detection lab

An offline Python 3.9+ utility for turning small, ordered JSON event batches into reproducible defensive alerts. Original Sandworm material under the repository MIT license. All shipped events are fabricated.

```bash
python3 scripts/detection_lab.py --input examples/events.json --expect examples/expected-alerts.json
python3 -m unittest discover -s tests -p 'test_detection_lab.py' -v
```

The first command compares observed alerts to the committed expected array. It emits three alerts and `expectations_match: true` for the shipped fixture. Exit codes: **0** valid input/expectations match, **1** expectations differ, **2** invalid input, configuration or unreadable JSON. The tool never sends network traffic, executes commands or changes input files.

## Detection contract

| Rule | Group | Eligible event | Default trigger |
| --- | --- | --- | --- |
| `denied_object_access_burst` | Actor | `object_access` with `denied` outcome | Three denied events within 60 seconds, across one or more object IDs |
| `rejected_replay_burst` | Actor and request ID | `replay_check` with `denied` outcome | Three rejected checks for the same request within 60 seconds |

Set `--window-seconds` from 1 to 86400 and `--threshold` from 2 to 1000. Both ends of the time window are included: events at 00, 30 and 60 seconds qualify; 00, 30 and 61 do not. An alert is emitted on the threshold crossing, not for every following event. A group rearms when old events expire and its count falls below the threshold before a new event is added. Allowed outcomes do not count or clear the window.

This is an original, intentionally narrow algorithm. It does not implement Sigma conversion, a SIEM, machine learning, a continuous stream processor or an assertion that an actor is malicious. Retries, permission misconfiguration and stale clients can cause legitimate bursts; review the included event IDs and object IDs before acting.

## Input and missing data

The JSON root contains `schema_version: 1` and an `events` array, capped at 10000 events and 2 MiB of input. Each event requires nonempty `event_id` and `actor` strings of at most 128 characters; `timestamp` in UTC `YYYY-MM-DDTHH:MM:SSZ`; an action from the table; and `outcome` equal to `allowed` or `denied`. Object events require `object_id`; replay events require `request_id`, with the same string bounds. Additional fields are ignored and are not copied into alerts.

Timestamps must represent real UTC dates and be globally nondecreasing. Equal timestamps retain input order. Duplicate event IDs, missing required fields, unknown actions/outcomes and unsorted events reject the entire batch before any alerts are produced. No timestamp, identity or field is silently invented.

```bash
python3 scripts/detection_lab.py --input examples/missing-data.json
```

The invalid fixture returns exit 2 and `event 1: missing object_id`.

## Expected versus observed fixtures

| Case in the shipped data | Expected result | Verification |
| --- | --- | --- |
| Actor A denied access at 00, 30 and 60 seconds | One alert, IDs `e01/e04/e05` | Exact alert-array comparison |
| Allowed access and actor B's separate denial | Neither contributes to actor A's count | Same comparison |
| Actor C rejected replay at 40, 70 and 100 seconds | One alert for `request-x` | Same comparison |
| Later actor A burst after expiration | A second actor A alert | Same comparison |
| Separate replay request IDs | No combined alert | Same comparison |
| Missing object ID | Reject batch, exit 2 | Invalid fixture and regression test |

Tests additionally cover a one-second-outside window, continuous-burst suppression, grouping, malformed timestamps and event ordering. The expected array remains independent input; the CLI compares it with newly calculated results. These finite cases establish the documented algorithm's behavior on these inputs, not coverage of all incidents or all log schemas.
