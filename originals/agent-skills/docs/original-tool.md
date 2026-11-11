# Original tool: Tool Policy Gate

This repository includes an original, offline authorization decision evaluator:
[scripts/tool_policy.py](../scripts/tool_policy.py). It turns agent/tool-security
review concepts into a small application policy that can be tested without an
LLM, cloud account or external dependency. It does not wrap or claim to implement
OPA, Cedar, MCP conformance, authentication or a tool executor.

## Quickstart

From the repository or bundle root, run this one command with synthetic inputs:

```bash
python3 scripts/tool_policy.py --policy examples/policy.json --request examples/request-allow.json --now 2030-01-01T00:00:00Z
```

It prints `{"allowed":true,"reason":"ALLOW"}` and exits `0`. Replace
`request-allow.json` with `request-deny.json` to see `ACTION_DENIED` and exit `1`.
Omit `--request` to read a UTF-8 JSON request from stdin. No input values or file
paths appear in the decision output or error diagnostics.

## Exact policy semantics

The policy must contain exactly `version` (integer `1`) and `grants` (a list).
Each grant contains exactly `principal`, `actions` and `resources`, with an
optional `expires_at`. For example:

```json
{
  "version": 1,
  "grants": [
    {
      "principal": "operator.demo",
      "actions": ["server.status"],
      "resources": ["game.demo"],
      "expires_at": "2030-01-01T01:00:00Z"
    }
  ]
}
```

The request contains exactly three strings:

```json
{"principal":"operator.demo","action":"server.status","resource":"game.demo"}
```

- Every identifier is matched **exactly and case-sensitively**. There are no
  wildcards, regular-expression permissions, prefix inheritance or role expansion.
  `game.demo` grants no access to `game.demo/child` or `Game.demo`.
- Identifiers contain 1–128 ASCII letters, digits, `_`, `.`, `:`, `/` or `-`,
  starting with a letter or digit. These are opaque identifiers, not filesystem
  paths; the gate performs no path normalization or resource lookup.
- A single grant must match the principal, action and resource together. It does
  not combine an action in one grant with a resource in another grant.
- At least one fully matching, unexpired grant allows the request. A matching
  grant without `expires_at` does not expire. Empty grants deny all requests.
  There are no explicit deny rules or rule-order overrides.
- `expires_at` and required `--now` use exactly `YYYY-MM-DDTHH:MM:SSZ` in UTC,
  without fractional seconds or offsets. A grant expires when `now >= expires_at`.
  Invalid dates or missing time input fail closed. The evaluator never reads the
  system clock, so a fixture has the same result whenever it is run.
- Every grant is validated before authorization. One invalid grant makes the
  whole policy invalid, even if another grant would have allowed the request.
  Unknown fields and versions are rejected rather than silently ignored.

## Caller enforcement and trust boundary

The principal must come from the caller's **authenticated server-side context**.
Do not accept the principal, policy, clock or resource binding from a model's
tool arguments or an untrusted client's claim. The evaluator does not establish
who owns an identifier: anyone able to replace the request principal with an
allowed identifier could obtain an allow decision. The JSON examples only
represent synthetic server-supplied context.

A production caller must maintain its policy in a trusted location, supply a
trusted UTC timestamp, bind the exact request to the operation it will perform,
and execute only after receiving `allowed: true`. Missing responses, parser
errors and nonzero exit statuses must not authorize execution. Reevaluate near
execution when expiry matters, and prevent changes between the checked resource
and the executed operation. Remote policy fetching, signatures, approvals,
replay prevention, permission revocation, audit persistence and tool side effects
remain separate caller responsibilities.

## Reason codes and exit statuses

Decision output is one compact JSON line with only `allowed` and `reason`.
The reason is a fixed code; requests, principals and arbitrary payloads are never
echoed. Reason precedence for a valid policy/request is principal → action →
resource → expiry. Invalid policy, request and time are checked in that order.

| Reason | Meaning | CLI status |
| --- | --- | --- |
| `ALLOW` | One grant matches and has not expired | `0` |
| `NO_PRINCIPAL_GRANT` | No grant for the exact principal | `1` |
| `ACTION_DENIED` | Principal has no grant for this action | `1` |
| `RESOURCE_DENIED` | No same-grant match for this resource | `1` |
| `GRANT_EXPIRED` | Every fully matching grant has expired | `1` |
| `INVALID_POLICY` | Invalid policy schema, identifiers or expiry | `2` |
| `INVALID_REQUEST` | Invalid request schema or identifiers | `2` |
| `INVALID_NOW` | Missing/invalid canonical UTC timestamp in the API | `2` |
| `INVALID_JSON` | Malformed, duplicate-key, unsupported or over-budget JSON | `2` |
| `INVALID_ARGUMENTS` | Missing/unknown CLI arguments | `2` |
| `IO_ERROR` | Cannot read an input file/stream | `3` |

A failed output write also exits `3`; no decision can be guaranteed on a broken
output stream. `--help` prints static help and exits `0` without an authorization
decision; do not treat its exit status as an allow decision.

## Python API

From the repository root:

```python
from scripts.tool_policy import GateError, evaluate, load_json

policy = load_json('{"version":1,"grants":[]}')
request = {"principal": "guest.demo", "action": "server.status", "resource": "game.demo"}
decision = evaluate(policy, request, "2030-01-01T00:00:00Z")
assert decision == {"allowed": False, "reason": "NO_PRINCIPAL_GRANT"}
```

`evaluate` accepts parsed JSON-shaped values and returns an invalid-input deny
decision instead of raising for schema failures. `load_json` raises `GateError`
with the fixed `INVALID_JSON` code on parse failures. Catch it and stop processing;
do not substitute a default-allow policy. `evaluate` does not mutate its inputs.

## Bounds and evidence

CLI documents and `load_json` are limited to **65,536 UTF-8 bytes** each and
**eight nested containers**. The strict loader rejects duplicate object keys at
any depth, multiple documents, non-finite numbers, floats and integers longer
than ten decimal digits. Policy version is the only supported numeric field.
The schema supports at most **256 grants**, with **1–64 unique actions** and
**1–64 unique resources** in each grant. Native API inputs have those structural
bounds; use `load_json` when the serialized byte/depth bounds are also needed.

Run synthetic tests:

```bash
python3 -m unittest discover -s tests -p 'test_tool_policy.py' -v
```

[Expected-decision fixtures](../examples/decision-fixtures.json) cover allowed
requests, cross-user/resource denial, wrong action, no prefix inheritance,
expiration boundaries, extra request authority and duplicate JSON keys. The
suite runs the same cases through the API and CLI, and also checks deterministic
output, malformed policies, budgets, sanitized errors and immutable inputs.
No real users, credentials, server operations or network services are involved.
These local checks do not establish a production authentication boundary, test
an upstream policy engine or claim GitHub-hosted CI success.
