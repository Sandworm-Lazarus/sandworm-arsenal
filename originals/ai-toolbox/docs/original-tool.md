# AI API Workload Budget Calculator

An original Sandworm-Lazarus utility that turns a fixed token workload and supplied
prices into inspectable arithmetic. It runs offline with Python 3.9+ and the standard
library. It does not fetch prices, contact a provider, select a model, or measure
model quality.

The implementation, tests and synthetic fixtures are original project material
under the repository's MIT license. No upstream tool package is bundled.

## Run the synthetic example

From the repository root:

```bash
python3 scripts/ai_budget.py examples/workload.json
python3 -m unittest discover -s tests -p 'test_ai_budget.py' -v
```

Use `-` as the input path to read UTF-8 JSON from standard input. Success writes
one deterministic JSON document to stdout and exits `0`. Invalid input or an
unreadable file writes a fixed diagnostic to stderr, emits no result, and exits
`2`. Diagnostics do not repeat input values, supplied file paths or raw parser
exceptions. There are no dependencies or network operations.

[workload.json](../examples/workload.json) uses **invented arithmetic prices**:
USD 2 per million input tokens and USD 8 per million output tokens. These are not
current provider quotes. Its 1,000 input tokens plus 500 output tokens cost
USD 0.006 per request, USD 0.60 for 100 requests/day, and USD 18 for 30 days. A
USD 12 envelope buys 2,000 whole requests. The complete expected result is in
[workload.expected.json](../examples/workload.expected.json).

## Input contract

The root must be an object. All fields below are required except the last two;
unknown fields and duplicate object keys are rejected.

| Field | Type and unit | Accepted range |
| --- | --- | --- |
| `schema_version` | Integer | Exactly `1` |
| `input_tokens_per_request` | Integer tokens/request | 0 to 1,000,000,000 |
| `output_tokens_per_request` | Integer tokens/request | 0 to 1,000,000,000 |
| `requests_per_day` | Integer requests/day | 0 to 1,000,000,000 |
| `days` | Integer days in the modeled period | 1 to 3,660 |
| `input_usd_per_million_tokens` | Decimal string, USD per 1,000,000 input tokens | 0 to 1,000,000 |
| `output_usd_per_million_tokens` | Decimal string, USD per 1,000,000 output tokens | 0 to 1,000,000 |
| `monthly_budget_usd` | Optional decimal string, USD | 0 to 1,000,000,000,000 |
| `price_basis` | Optional string | `user-supplied` (default) or `synthetic-example` |

USD strings use ordinary decimal notation such as `"0"`, `"2.00"` or
`"0.000000000001"`. At most 12 fractional digits and 32 characters are accepted.
Signs, exponent notation, surrounding whitespace, leading zeroes such as
`"00.5"`, NaN and infinity are rejected. Integer fields reject booleans and
floating-point values, including `1.0`. The raw document limit is 65,536 bytes;
JSON integer literals are limited to ten digits. Nesting is limited to eight
levels, independently of the host Python recursion limit.

The optional monthly budget is **one flat supplied envelope**. It is not prorated,
renewed or converted into a calendar month. `days` defines the modeled period;
set it to the number of days you want to model for that month. The affordable
request count is a **total**, not requests/day. The period comparison asks whether
the entire selected period fits inside that same envelope.

## Arithmetic and output

```text
input cost/request  = input tokens/request  × input USD/million  ÷ 1,000,000
output cost/request = output tokens/request × output USD/million ÷ 1,000,000
daily cost          = (input cost/request + output cost/request) × requests/day
period cost         = daily cost × days
affordable requests = floor(budget USD ÷ exact cost/request)
```

Costs and supplied rates are returned as plain decimal strings. Fields ending
in `_exact` preserve all digits; no intermediate cost is rounded. The bounded
inputs need fewer than 50 significant coefficient digits, and calculations use an
independent Decimal context with precision 80. Cents display fields use two
decimal places and `ROUND_HALF_UP`. They do not feed affordability calculations.
The whole-request floor uses exact integer ratios, avoiding division-rounding
errors at a budget boundary.

`maximum_whole_requests` is a decimal **integer string**, preserving large counts
for JSON consumers. With positive cost and a zero budget it is `"0"`. With zero
per-request cost it is `null` and `request_limit` is `"unbounded"`, even when the
budget is zero. This means only that this arithmetic model imposes no spending
limit; it is not a claim about provider quotas. If no budget is supplied,
`monthly_budget` is `null`. Zero planned requests produce zero daily/period cost
while affordability still uses the per-request cost.

## Scope and limits

These are estimates from the supplied counts and rates, not an invoice or a model
recommendation. Actual usage may differ. The model excludes cached/batch pricing,
reasoning or hidden billable tokens, retries, tool charges, media, storage, minimum
charges, discounts, taxes and exchange rates. It assumes the same input/output
counts for every request and the same daily request count. Supply verified prices
and measured counts for a real workload; keep those assumptions with your result.

The tests demonstrate arithmetic, schema boundaries and deterministic local CLI
behavior. They do not demonstrate provider billing accuracy or model performance.
