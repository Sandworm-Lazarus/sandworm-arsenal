# Original work and upstream attribution

Each collection must provide useful authored functionality, a reproducible example, meaningful tests, and an explanation of what was measured. Original work is maintained here and distributed to its focused repository by `scripts/build_collections.py`.

| Repository | Authored functionality | Evidence |
| --- | --- | --- |
| sandworm-arsenal | Catalog CLI, schema validator, focused generator, Privacy Guard, and original-project verification | Hub tests, generator regressions, privacy fixture report, `scripts/check_originals.py` |
| sandworm-ai-toolbox | AI Workload Budget Calculator | Synthetic workload and exact Decimal calculation tests |
| sandworm-agent-skills | Tool Policy Gate | Explicit allow/deny, resource, expiry and malformed-policy fixtures |
| sandworm-cyber-arsenal | Privacy Guard and Detection Lab | Privacy report and expected-vs-observed synthetic alerts |
| sandworm-llm-lab | Recorded Answer Evaluator | Original Thai/English cases, recorded predictions, metric and abstention tests |
| sandworm-dev-playbooks | Privacy Guard and Evidence Manifest Checker | File hashes, safe-path and result-metadata checks |

The [project register](originals/manifest.json) identifies the standalone source bundles. Each bundle documents its own input contract and limits. These are original implementations and fixtures under this repository's MIT license.

## What the catalog contributes

The 160 linked skills and 66 upstream tools remain their authors' work. Our contribution is the curation, Thai summaries, requirements/license notes, pinned source register, original guides, authored code, and local evidence. Original-tool tests do not change upstream `runtime_tested` flags.

When adapting an upstream implementation, retain its authorship and applicable license/notices, record the upstream revision and describe the actual modifications. A new name, translated README, or relocated file does not establish original authorship. Do not relabel third-party bundles as entirely authored here.

## Completion standard

1. State a practical problem and expose a runnable entry point.
2. Include fabricated or properly licensed fixtures and expected behavior.
3. Test important success, failure, boundary and misuse cases.
4. Record exact validation scope; distinguish local tests from hosted CI and model/provider execution.
5. Preserve upstream credit and license scope when adapting external work.
6. Publish only after checking the relevant tests and the current remote head.

The public profile links these projects as authored tools alongside curated resources. Other repositories keep their own project purpose and privacy requirements; this register does not make claims about ownership of their assets or private source.
