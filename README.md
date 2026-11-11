<p align="center"><img src="assets/banner.svg" alt="Sandworm Arsenal — AI engineering, agent systems, and cybersecurity" width="100%"></p>

<p align="center"><b>160 skill entries · 29 skill collections · 66 companion tools</b><br>Curated by <a href="https://github.com/Sandworm-Lazarus">Sandworm-Lazarus</a> · Source review: 11 November 2026</p>

<p align="center"><a href="https://github.com/Sandworm-Lazarus/sandworm-arsenal/actions/workflows/validate.yml">Validation workflow</a> · <a href="docs/review-status.md">Review coverage</a> · MIT for original material</p>

<p align="center"><a href="README.th.md">ภาษาไทย</a> · <a href="CATALOG.md">Browse the arsenal</a> · <a href="docs/starter-packs.md">Starter packs</a> · <a href="SOURCES.md">Sources &amp; licenses</a></p>

# Sandworm Arsenal

## Focused repositories

| Repository | Focus | Skills | Tools |
| --- | --- | ---: | ---: |
| [AI Toolbox](https://github.com/Sandworm-Lazarus/sandworm-ai-toolbox) | A directory of practical AI tools and frameworks, from personal agents and local inference to voice, documents, coding, and observability. | 0 | 48 |
| [Agent Skills](https://github.com/Sandworm-Lazarus/sandworm-agent-skills) | Focused agent workflows for context, memory, tool design, orchestration, browser use, and voice interfaces. | 13 | 18 |
| [Cyber Arsenal](https://github.com/Sandworm-Lazarus/sandworm-cyber-arsenal) | A focused security collection covering AppSec, agent and MCP security, reverse engineering, DFIR, detection, and supply-chain review. | 68 | 19 |
| [LLM Lab](https://github.com/Sandworm-Lazarus/sandworm-llm-lab) | A practical LLM engineering lab: model serving, quantization, RAG, evaluation, training, and experiment observability. | 49 | 15 |
| [Dev Playbooks](https://github.com/Sandworm-Lazarus/sandworm-dev-playbooks) | Developer workflows for debugging, cloud, frontend, coding agents, and evidence-backed reviews, with original playbooks and report templates. | 30 | 17 |

This repository is the collection hub. Skills have focused homes in the four subject collections; AI Toolbox is a cross-cutting directory. Tools can appear in multiple collections, so collection counts should not be added together.

A personal collection of useful **AI and cybersecurity agent skills**, with Thai annotations, pinned source links, and practical workflows. Built for people who want to understand what a skill does before adding it to their tools.

This repository contributes the curation, original summaries, three original playbooks, an offline catalog CLI, and the original Privacy Guard utility. Linked skills belong to their respective authors. Upstream skill code is not bundled here.

## Original tool: Privacy Guard

Mask email addresses and selected JSON fields before preparing agent context or application logs. The utility runs offline with Python 3.9+ and the standard library. It applies an explicit preprocessing policy with input limits and sanitized errors.

```bash
python3 scripts/privacy_guard.py json --sensitive-field customer_name < examples/privacy-input.json
python3 scripts/check_privacy_fixtures.py --check-report examples/privacy-guard-results.json
python3 -m unittest discover -s tests -v
```

See the [utility guide](docs/privacy-guard.md), [synthetic fixture results](examples/privacy-guard-results.json), and [development case study](docs/development-notes/2026-11-11-original-tools.md). This is a bounded email/field masking tool; other sensitive data requires an explicit field policy or a separately evaluated detector.

## Latest curation

[Five practical additions](docs/curation-notes/2026-11-11-mcp-typescript.md): MCP Inspector, Mastra, Vercel AI SDK, Presidio and Bruno. Includes three bounded trial tasks and an original synthetic privacy fixture. [Maintenance standard](docs/maintenance.md).

## AI tools beyond skills

Explore the **[AI toolbox guide](docs/ai-toolbox.md)**: 44 new projects covering personal agents, local inference, voice, browser automation, documents, memory, creative workflows, coding and model operations. The guide includes five original project directions and a comparison table.

## Choose your direction

| Track | What you can explore | Start here |
| --- | --- | --- |
| AI Engineering | Model serving, quantization, fine-tuning, RAG, evaluation | [AI lab pack](docs/starter-packs.md#ai-lab) |
| Agent / Context | Memory, context compression, tool design, human review | [Agent builder pack](docs/starter-packs.md#agent-builder) |
| AI Security | Prompt injection, MCP review, model provenance, trust boundaries | [Agent defense pack](docs/starter-packs.md#agent-defense) |
| Cyber | Code review, dependency risk, detection rules, CI security | [AppSec pack](docs/starter-packs.md#appsec) |
| Reverse / DFIR | Binary analysis, protocols, memory forensics | [Reverse & DFIR pack](docs/starter-packs.md#reverse-and-dfir) |
| Engineering | Debugging, verification, Postgres, browser testing, UI design | [Full catalog](CATALOG.md#engineering) |
| Cloud / DevOps | Workers, containers, Terraform, profiling | [Cloud pack](docs/starter-packs.md#cloud-and-containers) |
| Web / Frontend | React composition, accessibility, performance | [UI guide](docs/decision-guide.md) |

## A few places to begin

| Source | Why it is here |
| --- | --- |
| [Trail of Bits](https://github.com/trailofbits/skills) | Focused security review, finding verification, and rule authoring |
| [Hugging Face](https://github.com/huggingface/skills) | Local models, training, embeddings, and model workflows |
| [OWASP Secure Agent Playbook](https://github.com/OWASP/secure-agent-playbook) | Agent and MCP security review with supporting plays and templates |
| [SecSkills](https://github.com/trilwu/secskills) | Reverse engineering, DFIR, detection engineering, and extension review |
| [Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | Context, memory, and tool interface design |
| [AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Serving, quantization, evaluation, and fine-tuning workflows |

These are editorial starting points, not benchmark rankings or security endorsements. See the [complete source register](SOURCES.md) for the reviewed revisions and license notes.

## Original playbooks

Three concise workflows authored for this repository. Each includes required inputs, a procedure, an output contract, and a worked example. They are Markdown guides to give an agent as task context, not an automatic installer or a tested integration with every agent client.

| Playbook | Use it when you need to… |
| --- | --- |
| [Review an agent extension](playbooks/review-agent-extension.md) | Trace permissions, outbound data, hooks, and setup behavior before adoption |
| [Review a diff with evidence](playbooks/review-diff-with-evidence.md) | Separate verified findings from open questions and attach reproducible checks |
| [Compare models fairly](playbooks/compare-models.md) | Compare quality, latency, and cost using the same tasks and explicit assumptions |

Examples are illustrative. No live security certification or model benchmark is claimed.

## Search locally

The CLI uses Python 3.9+ and the standard library and performs no network requests.

```bash
git clone https://github.com/Sandworm-Lazarus/sandworm-arsenal.git
cd sandworm-arsenal
python3 scripts/arsenal.py search "memory"
python3 scripts/arsenal.py search "กฎ" --category "Cyber"
python3 scripts/arsenal.py check
```

On Windows, use `py -3` if `python3` is unavailable. Prefer browsing? Open [CATALOG.md](CATALOG.md). Want structured data? Use [catalog/arsenal.json](catalog/arsenal.json).

## Review coverage

| Scope | Entries | What was inspected |
| --- | ---: | --- |
| Entry-reviewed | 57 | Entry files and selected supporting files from the initial focused research |
| Entry-overview | 103 | Pinned identity, frontmatter, and opening excerpts; full bundles remain to review |
| Companion tools | 66 | README/source overviews and license evidence |

No upstream runtime tests are claimed. [Review coverage](docs/review-status.md) and [methodology](docs/methodology.md) explain the limits. Some packages need references, scripts, client-specific tools, or a complete plugin bundle.

## Put it to work

- Pick one of **[12 starter packs](docs/starter-packs.md)**, from an AI lab to game-server AppSec.
- Use the **[decision guide](docs/decision-guide.md)** to choose a skill or executable tool for a task.
- Explore **[66 companion tools](TOOLS.md)** for evaluation, SAST, SBOM, secrets, containers, and CI.
- Start a report from the **[five original templates](templates/README.md)**.
- Check **[watchlist notes](docs/watchlist.md)** for moved sources, license scopes, and platform-specific entries.
- See **[changes](CHANGELOG.md)** for the current expansion.

```bash
python3 scripts/arsenal.py search "MCP" --review entry-reviewed
python3 scripts/arsenal.py search "" --repo cloudflare/skills --json
python3 scripts/arsenal.py show 1
python3 scripts/arsenal.py stats
```

The validation workflow is configured for pushes and pull requests; see Actions for runner/execution status. Local checks cover catalog consistency, malformed input handling, deterministic collection generation, and the original Privacy Guard. The synthetic fixture report records script and fixture SHA-256 hashes. These checks do not execute linked upstream packages.

## Contribute and reuse

Suggest a useful source or correct a stale entry through a pull request. Include a pinned revision, a task it helps with, requirements, and license evidence; see [CONTRIBUTING.md](CONTRIBUTING.md).

Original repository material is [MIT licensed](LICENSE). External projects retain their own licenses. In particular, Trail of Bits uses CC BY-SA, and some other entries have scoped or unresolved license notes. Consult [attribution and reuse](docs/attribution.md) before copying upstream material.

Independent personal curation. No affiliation with the linked organizations.
