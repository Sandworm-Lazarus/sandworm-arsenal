# Source watchlist

[Home](../README.md) · [Sources](../SOURCES.md) · [Review coverage](review-status.md)

These are observations at the pinned research revisions, not judgments about future releases. Follow the register's revision links for evidence.

| Source | Observation | Catalog treatment |
| --- | --- | --- |
| openai/skills | README says the repository is deprecated and points to openai/plugins | New selections use openai/plugins; legacy entries were not added |
| openai/plugins | Plugin examples can depend on host tools, shared references, and backends; no blanket root license was found | Inspect per-plugin/file scope; build-chatgpt-app has an Apache 2.0 file |
| vercel-labs/next-skills | The inspected tree has README/instruction files and no SKILL.md entries | Excluded from the skill count |
| vercel-labs/agent-skills | Selected React entries declare MIT; no root LICENSE was found | Keep link-only; resolve rights for entries without declarations |
| semgrep/skills | README identifies Beta and rule-derived material; LICENSE points to Semgrep Rules License v1.0 | Record the actual rules license, not an assumed MIT/Apache license |
| getsentry/skills | Primarily team workflows; security-review references have a separate CC BY-SA license | Record scoped licensing; identify organization-specific assumptions |
| Sentry triage-frontend-issues | Hard-coded organization/project and archive-only semantics | Reference example; not recommended as a generic drop-in triage skill |
| github/awesome-copilot | Community-created resources hosted in the GitHub organization | Community provenance; review individual entries independently |
| better-auth/skills | No root LICENSE found in the inspected tree | Link-only; resolve permission before redistributing |
| NVIDIA/skills | README and selected RAG entry frontmatter express license scope differently | Preserve scope questions and inspect notices before copying |
| haikow/claude-reverse-skills | No root LICENSE; partial MIT statements and forum provenance | Link-only study reference |
| gitleaks/gitleaks | README says feature-complete, security patches only, and points to Betterleaks | Record lifecycle; inspect the successor separately before choosing it |
| github/codeql | MIT applies to repository queries/libraries | Do not infer that the separately distributed CLI has identical terms |
| Orchestra AI Research skills | Several entries contain numeric performance claims and older library examples | Summaries describe the workflow without inheriting those benchmark claims |
| FlowiseAI/Flowise | GitHub metadata marked the repository archived in this research snapshot | Excluded from active toolbox additions |
| letta-ai/letta | README identifies letta-ai/letta-code as current source; archive branch is the retired V1 server | Tool selection points to current Letta Code |
| Firecrawl / CosyVoice | Older organization URLs redirect | Use firecrawl/firecrawl and QwenAudio/CosyVoice |
| Dify / FastGPT / MinerU / Open WebUI | LICENSE texts contain project-specific additional terms | Preserve custom labels and link to actual terms |
| n8n | Sustainable Use License and separate enterprise scope | Label as source-available/fair-code; do not assume MIT/Apache |
| Arize Phoenix | Root license is Elastic License 2.0 | Record ELv2, separately from the vendor's product descriptions |
| Unsloth / Langfuse / LiteLLM | Licensing varies across core, optional, or enterprise components | Inspect the files and deployment feature set before reuse |

## Before promoting an overview entry

Read its complete entry and required references/scripts, inspect permissions and outbound data, confirm dependencies and license scope, and run a bounded test in the target environment. Store reproducible evidence before adding a runtime-tested status.
