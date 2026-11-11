# Tool Policy Gate

Original offline Python code that decides whether one principal may invoke one
action on one resource. It adapts agent-security guidance into a runnable,
deny-by-default policy gate with exact allowlists, expiry and synthetic tests.

Run from this bundle's root (or the generated repository root):

```bash
python3 scripts/tool_policy.py --policy examples/policy.json --request examples/request-allow.json --now 2030-01-01T00:00:00Z
```

Expected output: `{"allowed":true,"reason":"ALLOW"}` with exit status `0`.

The gate never executes tools or authenticates identities. A trusted server must
supply the principal and enforce the decision before invoking the requested tool.

- [Policy, API, limits and enforcement contract](docs/original-tool.md)
- [Machine-checkable synthetic decisions](examples/decision-fixtures.json)
- Tests: `python3 -m unittest discover -s tests -p 'test_tool_policy.py' -v`

Python 3.9+ standard library only. No model, API, network or third-party runtime.
