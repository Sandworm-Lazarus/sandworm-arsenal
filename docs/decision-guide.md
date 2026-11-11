# Choose by task

[Home](../README.md) · [Starter packs](starter-packs.md) · [Tools](../TOOLS.md)

Start with the output you need. A skill supplies a workflow; an executable tool supplies observations. Use both when the task calls for measured evidence.

| งาน | Entry to inspect | Companion tool | หลักฐานที่ควรได้ |
| --- | --- | --- | --- |
| ตรวจ MCP config | [mcp-security-audit](https://github.com/github/awesome-copilot/blob/eaaffd5d020b756a2777a4b1b161d2bdc126d9a0/skills/mcp-security-audit/SKILL.md) | Skill Scanner / Agent Scan | Inventory ของ servers, pinned packages และ credential/data paths |
| ตรวจ diff | [differential-review](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/differential-review/skills/differential-review/SKILL.md) | Semgrep / CodeQL | Finding ที่ระบุ trigger, source/control/sink และ counterevidence |
| ตรวจ GitHub Actions | [gha-security-review](https://github.com/getsentry/skills/blob/e94f22214528d69899d09c627b3315ddc3544816/skills/gha-security-review/SKILL.md) | zizmor | Untrusted input ไปถึง privileged runner/credential ได้อย่างไร |
| ตรวจ dependency | [supply-chain-risk-auditor](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SKILL.md) | OSV-Scanner / Syft / Grype | SBOM หรือ lockfile revision, advisory และ reachability notes |
| ลดความเสี่ยง secrets | [secret-serialization](https://github.com/getsentry/skills/blob/e94f22214528d69899d09c627b3315ddc3544816/skills/secret-serialization/SKILL.md) | Gitleaks | แยก literal secrets จาก credential-holder/serialization sink |
| ทำ fuzzing | [harness-writing](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/testing-handbook-skills/skills/harness-writing/SKILL.md) | AFL++ / cargo-fuzz / Atheris | Reproducible crash artifact หรือ coverage gaps |
| เลือกโมเดล | [huggingface-community-evals](https://github.com/huggingface/skills/blob/25910b3d0ba31a2ba102f901cdc9e008c278a69c/skills/huggingface-community-evals/SKILL.md) | Inspect AI / Promptfoo | Fixed tasks, acceptance criteria, settings, latency และต้นทุน |
| ประเมิน AI defense | [prompt-injection-test](https://github.com/OWASP/secure-agent-playbook/blob/65d4efd2cd0b081d52101e9708792b944e4ddebb/plugins/ai-security-skills/skills/prompt-injection-test/SKILL.md) | PyRIT / garak | Test matrix, target scope, observed failures และ budget |
| เพิ่ม RAG quality | [qdrant-search-quality](https://github.com/qdrant/skills/blob/1d010729e5e573c4736cae520b47b1acce785c02/skills/qdrant-search-quality/SKILL.md) | Phoenix / Inspect AI | Golden queries, relevance labels, retrieval และ answer metrics แยกกัน |
| รันโมเดลบน GPU | [vllm](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/12-inference-serving/vllm/SKILL.md) | Runtime monitoring ตามระบบ | Exact model/quant/backend, peak VRAM และ workload-specific latency |
| ทดสอบ IaC | [terraform-test](https://github.com/hashicorp/agent-skills/blob/5e30fa5c867ba6777c37e4206babfd08049c396f/plugins/terraform/skills/terraform-test/SKILL.md) | Checkov / Trivy | Plan/mock results แยกจาก apply ที่สร้าง resource จริง |
| ปรับหน้าเว็บ | [web-design-guidelines](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/web-design-guidelines/SKILL.md) | Browser performance tools | Keyboard/responsive flow, screenshots และ trace ที่วัดจริง |

## Adoption sequence

1. Open the pinned entry and its source/license notes.
2. Read the full required bundle, especially for Overview selections.
3. Confirm runtime, credentials, external services, and cost.
4. Try one synthetic task in the intended environment.
5. Keep outputs, failures, versions, and checks in a [report template](../templates/README.md).
