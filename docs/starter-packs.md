# Starter packs

[Home](../README.md) · [ภาษาไทย](../README.th.md) · [Full catalog](../CATALOG.md) · [Companion tools](../TOOLS.md)

Twelve task-oriented reading paths. These are selections, not bulk installers. Entry and Overview labels describe inspection scope; none claims upstream execution.

## AI lab

วางการทดลองรันโมเดลและวัดผล

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [huggingface-local-models](https://github.com/huggingface/skills/blob/25910b3d0ba31a2ba102f901cdc9e008c278a69c/skills/huggingface-local-models/SKILL.md) | ค้น GGUF, เลือก quant และตั้ง local serving ด้วย llama.cpp | Entry |
| [vllm](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/12-inference-serving/vllm/SKILL.md) | วาง serving API, batching, quantization และ tensor parallelism | Entry |
| [gguf](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/10-optimization/gguf/SKILL.md) | วางการแปลงและ quantize โมเดลสำหรับ llama.cpp | Entry |
| [lm-evaluation-harness](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/11-evaluation/lm-evaluation-harness/SKILL.md) | ออกแบบรัน benchmark โมเดลด้วย harness แทนตัดสินจากความรู้สึก | Entry |

เริ่มจากโมเดลหนึ่งตัว ชุดงานเล็ก และเกณฑ์ผ่านที่กำหนดก่อนรัน

Original workflow: [playbook](../playbooks/compare-models.md)

## Agent builder

ออกแบบ tools, context และ memory

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [agent-architecture](https://github.com/github/awesome-copilot/blob/eaaffd5d020b756a2777a4b1b161d2bdc126d9a0/skills/agent-architecture/SKILL.md) | ออกแบบหรือวิเคราะห์ architecture ของ Agent จาก requirements และ failure cases | Overview |
| [tool-design](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/9ff0c99108b36d3b886defd825d8ac1f47dba374/skills/tool-design/SKILL.md) | ออกแบบชื่อ schema, result และ error ของ tool ให้ Agent ใช้ถูก | Entry |
| [memory-systems](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/9ff0c99108b36d3b886defd825d8ac1f47dba374/skills/memory-systems/SKILL.md) | ออกแบบความจำข้าม session, entity/time validity และ retrieval | Entry |
| [mcp-builder](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/mcp-builder/SKILL.md) | ออกแบบ MCP server และเครื่องมือที่ต่อกับ API ภายนอก | Entry |

เริ่มจาก tool เดียวและ synthetic inputs แล้วตรวจ schema และ error behavior

Original workflow: [playbook](../playbooks/review-agent-extension.md)

## Agent defense

ตรวจ trust boundaries และ MCP

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [agentic-actions-auditor](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SKILL.md) | ตรวจ GitHub Actions ที่เรียก AI และเส้นทางข้อมูลจาก PR/issue | Entry |
| [agent-security](https://github.com/UnitOneAI/SecuritySkills/blob/70bc259bb01abb3015ad2ad859ad5253cbf0bcab/skills/ai-security/agent-security/SKILL.md) | ทบทวนสิทธิ์ Agent, trust boundary, audit trail และ rollback | Entry |
| [mcp-server-review](https://github.com/OWASP/secure-agent-playbook/blob/65d4efd2cd0b081d52101e9708792b944e4ddebb/plugins/ai-security-skills/skills/mcp-server-review/SKILL.md) | ตรวจ transport/auth, tool permissions และข้อมูลที่ MCP เปิดเผย | Entry |
| [mcp-security-audit](https://github.com/github/awesome-copilot/blob/eaaffd5d020b756a2777a4b1b161d2bdc126d9a0/skills/mcp-security-audit/SKILL.md) | ตรวจ MCP config เรื่อง credentials, shell command และ dependency selectors | Overview |

ทำ inventory ของสิทธิ์และข้อมูลที่เครื่องมือเข้าถึงก่อน

Original workflow: [playbook](../playbooks/review-agent-extension.md)

## AppSec

ตรวจ diff และทวน finding

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [differential-review](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/differential-review/skills/differential-review/SKILL.md) | ตรวจความเสี่ยงที่เกิดจาก diff และผลกระทบต่อผู้เรียกใช้ | Entry |
| [audit-context-building](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/audit-context-building/skills/audit-context-building/SKILL.md) | ทำความเข้าใจ assumptions, guarantees และ dependencies ก่อนเริ่ม audit | Overview |
| [fp-check](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/fp-check/skills/fp-check/SKILL.md) | ตรวจซ้ำว่ารายงานช่องโหว่มีหลักฐานจริงหรือเป็น false positive | Entry |
| [triage-finding](https://github.com/openai/plugins/blob/d420d13051bffe4543ed39e30fa46b87148e47dd/plugins/codex-security/skills/triage-finding/SKILL.md) | ทวน finding ที่มีอยู่จาก static evidence แล้วจัดสถานะและ proof gaps | Overview |

ไล่ source, control และ sink พร้อมตรวจ counterevidence

Original workflow: [playbook](../playbooks/review-diff-with-evidence.md)

## Reverse and DFIR

วิเคราะห์ binary, protocol และ memory evidence

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [analyzing-binaries](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-core/skills/analyzing-binaries/SKILL.md) | วิเคราะห์ executable โดยเริ่ม triage ก่อนเลือกจุด decompile | Entry |
| [reversing-network-protocols](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-core/skills/reversing-network-protocols/SKILL.md) | เทียบ packet capture กับ client เพื่อกู้ framing และ field ของ protocol | Entry |
| [analyzing-memory-images](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-defense/skills/analyzing-memory-images/SKILL.md) | วิเคราะห์ RAM dump เพื่อเรียงหลักฐาน process, network และ injection | Entry |
| [writing-sigma-rules](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-defense/skills/writing-sigma-rules/SKILL.md) | ออกแบบ Sigma rules, ลด noise และแปลงกฎข้าม SIEM | Entry |

ใช้ artifact ที่มีสิทธิ์วิเคราะห์ เก็บ hashes และแยก observation ออกจาก hypothesis

Original workflow: [playbook](../playbooks/review-diff-with-evidence.md)

## MLOps

เก็บ experiment และตาม LLM traces

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [huggingface-trackio](https://github.com/huggingface/skills/blob/25910b3d0ba31a2ba102f901cdc9e008c278a69c/skills/huggingface-trackio/SKILL.md) | เก็บ metrics, alerts และ dashboard ของ training experiments ด้วย Trackio | Overview |
| [mlflow](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/13-mlops/mlflow/SKILL.md) | เก็บ experiment parameters, metrics, artifacts และ model versions | Overview |
| [phoenix-observability](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/17-observability/phoenix/SKILL.md) | ทำ LLM tracing, datasets และ evaluation ด้วย Phoenix | Overview |
| [langsmith-observability](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/17-observability/langsmith/SKILL.md) | ติดตาม traces, latency, token usage และ regression eval ด้วย LangSmith | Overview |

กำหนด retention/privacy ของ prompts, metrics และ artifacts ก่อน sync dashboard

Original workflow: [playbook](../playbooks/compare-models.md)

## RAG and search

สำรวจข้อมูลและวัด retrieval

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [huggingface-datasets](https://github.com/huggingface/skills/blob/25910b3d0ba31a2ba102f901cdc9e008c278a69c/skills/huggingface-datasets/SKILL.md) | สำรวจ splits, rows, filters และ parquet ผ่าน Dataset Viewer API | Overview |
| [sentence-transformers](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/15-rag/sentence-transformers/SKILL.md) | สร้าง multilingual embeddings เพื่อ semantic search และ RAG | Overview |
| [faiss](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/15-rag/faiss/SKILL.md) | เลือก vector index และค้นหา similarity ด้วย FAISS บน CPU/GPU | Overview |
| [qdrant-search-quality](https://github.com/qdrant/skills/blob/1d010729e5e573c4736cae520b47b1acce785c02/skills/qdrant-search-quality/SKILL.md) | วินิจฉัย retrieval quality และเลือก hybrid search/reranking | Entry |

เตรียม golden queries และ relevance judgments แยก retrieval quality จากคำตอบสุดท้าย

Original workflow: [playbook](../playbooks/compare-models.md)

## Cloud and containers

พัฒนา edge runtime และทดสอบ infrastructure

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [workers-best-practices](https://github.com/cloudflare/skills/blob/cbf893b954222276bf1af57e5f23379231e0efb9/skills/workers-best-practices/SKILL.md) | ทบทวน runtime patterns, bindings, compatibility และ observability ของ Workers | Overview |
| [durable-objects](https://github.com/cloudflare/skills/blob/cbf893b954222276bf1af57e5f23379231e0efb9/skills/durable-objects/SKILL.md) | ออกแบบ persistent state และ coordination ด้วย Durable Objects | Overview |
| [multi-stage-dockerfile](https://github.com/github/awesome-copilot/blob/eaaffd5d020b756a2777a4b1b161d2bdc126d9a0/skills/multi-stage-dockerfile/SKILL.md) | ออกแบบ build/runtime stages และลดสิทธิ์ของ container image | Overview |
| [terraform-test](https://github.com/hashicorp/agent-skills/blob/5e30fa5c867ba6777c37e4206babfd08049c396f/plugins/terraform/skills/terraform-test/SKILL.md) | เขียน tftest พร้อม assertions, mocks และเลือก plan/apply ให้ตรงงาน | Overview |

แยก local/remote bindings; Terraform apply tests อาจสร้าง resource จริง

Original workflow: [playbook](../playbooks/review-diff-with-evidence.md)

## Authentication

สร้างและทบทวน auth flows

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [auth0](https://github.com/auth0/agent-skills/blob/6331cf05ef6bbc6999d7a7b98a583e7429ebe3f6/plugins/auth0/skills/auth0/SKILL.md) | ต่อ authentication, sessions, MFA, RBAC และ API protection ด้วย Auth0 | Overview |
| [better-auth-security-best-practices](https://github.com/better-auth/skills/blob/20c9e88a5c007461a703f1c213572b073196113e/security/SKILL.md) | ทบทวน secrets, rate limits, CSRF, trusted origins และ session cookies | Overview |
| [two-factor-authentication-best-practices](https://github.com/better-auth/skills/blob/20c9e88a5c007461a703f1c213572b073196113e/better-auth/twoFactor/SKILL.md) | ต่อ TOTP, backup codes และขั้นตอนลงชื่อเข้าใช้แบบสองปัจจัย | Overview |
| [api-security](https://github.com/UnitOneAI/SecuritySkills/blob/70bc259bb01abb3015ad2ad859ad5253cbf0bcab/skills/appsec/api-security/SKILL.md) | ตรวจ API เรื่องสิทธิ์เข้าถึง object/function, auth และการใช้ทรัพยากร | Entry |

เลือก provider ให้ตรงระบบ ตรวจ ownership/session/MFA และ migration behavior

Original workflow: [playbook](../playbooks/review-diff-with-evidence.md)

## CI and supply chain

ตรวจ workflows และ dependency integrity

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [gha-security-review](https://github.com/getsentry/skills/blob/e94f22214528d69899d09c627b3315ddc3544816/skills/gha-security-review/SKILL.md) | ตรวจเส้นทางโจมตีจากผู้ไม่มีสิทธิ์เขียน repo ใน GitHub Actions | Overview |
| [supply-chain-risk-auditor](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SKILL.md) | ตรวจ dependency, advisory, ผู้ดูแลแพ็กเกจ และ install scripts | Entry |
| [agent-supply-chain](https://github.com/github/awesome-copilot/blob/eaaffd5d020b756a2777a4b1b161d2bdc126d9a0/skills/agent-supply-chain/SKILL.md) | สร้างและตรวจ integrity manifest ของ plugin และ dependency ที่ตรึงรุ่น | Overview |
| [sarif-parsing](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/static-analysis/skills/sarif-parsing/SKILL.md) | อ่าน กรอง รวม และลดรายการซ้ำจากรายงาน SARIF ของเครื่องมือสแกน | Overview |

ใช้ Gitleaks, OSV-Scanner, zizmor และ Syft/Grype จาก TOOLS.md ประกอบตามโจทย์

Original workflow: [playbook](../playbooks/review-agent-extension.md)

## Fuzzing

ทำ harness และวัด coverage

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [harness-writing](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/testing-handbook-skills/skills/harness-writing/SKILL.md) | ออกแบบ fuzz harness ให้รับ structured input และทำซ้ำผลได้ | Overview |
| [address-sanitizer](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/testing-handbook-skills/skills/address-sanitizer/SKILL.md) | ตรวจ memory errors ด้วย AddressSanitizer ระหว่าง tests หรือ fuzzing | Overview |
| [aflpp](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/testing-handbook-skills/skills/aflpp/SKILL.md) | วาง AFL++ campaign หลาย core พร้อม corpus และ crash triage | Overview |
| [cargo-fuzz](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/testing-handbook-skills/skills/cargo-fuzz/SKILL.md) | สร้าง Rust fuzz target และตรวจ crash artifacts ด้วย cargo-fuzz | Overview |
| [coverage-analysis](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/testing-handbook-skills/skills/coverage-analysis/SKILL.md) | วัด code coverage เพื่อหาส่วนที่ fuzz campaign ยังเข้าไม่ถึง | Overview |

เริ่มจาก target เล็กและ deterministic harness ก่อนเพิ่ม core หรือเวลารัน

Original workflow: [playbook](../playbooks/review-diff-with-evidence.md)

## Game server AppSec

ทบทวน API, invariants และ database ของเกม

| Entry | ใช้ทำอะไร | Review |
| --- | --- | --- |
| [api-security](https://github.com/UnitOneAI/SecuritySkills/blob/70bc259bb01abb3015ad2ad859ad5253cbf0bcab/skills/appsec/api-security/SKILL.md) | ตรวจ API เรื่องสิทธิ์เข้าถึง object/function, auth และการใช้ทรัพยากร | Entry |
| [property-based-testing](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/property-based-testing/skills/property-based-testing/SKILL.md) | ออกแบบ invariant และสุ่มอินพุตเพื่อหา counterexample | Entry |
| [supabase-postgres-best-practices](https://github.com/supabase/agent-skills/blob/c9be0e931b7930f7d02126d04774d904c381e7d7/skills/supabase-postgres-best-practices/SKILL.md) | ทบทวน schema, query, indexes, RLS และ pgvector | Entry |
| [secret-serialization](https://github.com/getsentry/skills/blob/e94f22214528d69899d09c627b3315ddc3544816/skills/secret-serialization/SKILL.md) | ตามเส้นทาง credential ที่อาจรั่วผ่าน repr, JSON, logs และ telemetry | Overview |

กำหนด ownership, atomic transfer, non-negative balances, replay/idempotency และ server authority เป็น acceptance criteria

Original workflow: [playbook](../playbooks/review-diff-with-evidence.md)
