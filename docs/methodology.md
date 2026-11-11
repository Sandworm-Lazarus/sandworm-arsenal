# Review methodology

## Initial snapshot

Reviewed on 2026-11-11. The register covers 22 repositories: 19 skill sources and 3 evaluation tools. Research read 57 `SKILL.md` entry files and 12 supporting files. Supporting-file evidence is recorded in `catalog/arsenal.json`.

Each selected entry records a canonical repository, full commit SHA, file path, blob SHA, purpose, requirements, and a caution or use case. Repository metadata and entry contents were inspected through GitHub. The read-only research did not install skills, execute their helper code, start model jobs, or certify them for production.

## Expansion snapshot

The expansion adds 103 entry-overview inspections to the initial 57 entry-reviewed selections: 160 entries across 29 skill collections. Fourteen additional tools bring the companion-tool register to 17, for 46 source repositories in total. New entry overviews cover the recorded file identity, frontmatter, and opening excerpt; they do not claim a complete read of the entry, supporting files, or executable bundle. Source README/license overviews informed lifecycle and scope notes.

The initial `read: true` field is retained only for the original entry-reviewed selections. New overviews use `read: false` plus an explicit `review_level`. All upstream runtime statuses remain false.

## AI toolbox research

The toolbox round adds 44 executable tools/frameworks after inspecting canonical GitHub metadata, immutable README overviews, and license evidence. The complete register now contains 61 tools and 29 skill collections, for 90 source repositories. The 160 skill-entry records retain their previous scope labels.

Archived Flowise was excluded from active additions. Letta uses the current source named in its legacy README; moved Firecrawl/CosyVoice repositories use current canonical names. Custom and scoped licenses are recorded separately from GitHub's detected license badge. The project combinations in the toolbox guide are original proposals, not tested integrations.

## Selection criteria

- A recognizable task: the entry should help produce a concrete output.
- Inspectable procedure: steps, tools, references, or output expectations can be examined.
- Traceable origin: identify upstream owners, forks, and exact revisions.
- Visible requirements: describe credentials, hardware, services, and supporting files.
- Honest limits: separate author claims, source inspection, and observed execution.

Popularity and catalog size are not quality measurements. The recommendations are editorial judgments from source inspection, not a numeric benchmark.

## Status vocabulary

| Field or phrase | Meaning |
| --- | --- |
| `read: true` | The selected entry was read in this research snapshot |
| `runtime_tested: false` | No execution claim is made by this repository |
| Commit / blob SHA | Revision and file identity recorded for traceability |
| แนะนำเริ่ม | Editorial starting point for a relevant task |
| ตามแพลตฟอร์ม | Useful when using that platform |
| ตรวจสิทธิ์เพิ่ม | Resolve the license scope before copying material |
| เครื่องมือคัดคุณภาพ | Evaluation tool; not counted as a selected skill entry |

## Limits of the local check

`python3 scripts/arsenal.py check` checks IDs, duplicates, source references, SHA syntax, pinned URL consistency, required fields, source-review status, generated-document freshness, SVG XML, and local Markdown/HTML file targets. It runs offline. It does not re-fetch GitHub, check upstream link availability, verify every dependency, execute any third-party skill, or prove that a SHA refers to trusted code.

## Future runtime evidence

Before adding a tested label, record the host/client and version, exact package revision, permission scope, fixture, task prompt, expected outcome, observed output, tool logs, duration, and failures. Include cases where the skill should decline a task or mark evidence missing. Store only sanitized fixtures and logs. Failed and partial runs belong in the report too.

When upstream changes, add a new review date and revision only after rereading the affected files. Historical source-review claims should not silently follow a moving branch.
