# Starter packs

[Home](../README.md) · [ภาษาไทย](../README.th.md) · [Full catalog](../CATALOG.md)

These are suggested reading paths, not bulk installation bundles. All upstream selections are source-reviewed only. Use the reviewed link to inspect the complete package and its own setup instructions.

## AI lab

วางการทดลองรันโมเดลและวัดผล

| Entry | ใช้ทำอะไร |
| --- | --- |
| [huggingface-local-models](https://github.com/huggingface/skills/blob/25910b3d0ba31a2ba102f901cdc9e008c278a69c/skills/huggingface-local-models/SKILL.md) | ค้น GGUF, เลือก quant และตั้ง local serving ด้วย llama.cpp |
| [vllm](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/12-inference-serving/vllm/SKILL.md) | วาง serving API, batching, quantization และ tensor parallelism |
| [gguf](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/10-optimization/gguf/SKILL.md) | วางการแปลงและ quantize โมเดลสำหรับ llama.cpp |
| [lm-evaluation-harness](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/11-evaluation/lm-evaluation-harness/SKILL.md) | ออกแบบรัน benchmark โมเดลด้วย harness แทนตัดสินจากความรู้สึก |
| [llm-cost-optimizer](https://github.com/alirezarezvani/claude-skills/blob/9ca476d8401f8750f92f4a7b31ec68efaa61ab02/engineering/llm-cost-optimizer/skills/llm-cost-optimizer/SKILL.md) | วาง model routing, caching, token limit และการเก็บต้นทุนต่อ feature |

เริ่มจากโมเดลหนึ่งตัว งานที่มีเกณฑ์ผ่านชัดเจน และข้อจำกัด hardware ที่ทราบ อย่าเริ่ม GPU job แบบมีค่าใช้จ่ายจากการอ่านคู่มือเพียงอย่างเดียว

คู่มือประกอบของคลัง: [เปิด playbook](../playbooks/compare-models.md)

## Agent builder

ออกแบบ Agent ที่จัดการบริบทและใช้เครื่องมือได้ตรงงาน

| Entry | ใช้ทำอะไร |
| --- | --- |
| [context-compression](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/9ff0c99108b36d3b886defd825d8ac1f47dba374/skills/context-compression/SKILL.md) | ออกแบบสรุปบริบทที่รักษา decision, files และงานค้าง |
| [memory-systems](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/9ff0c99108b36d3b886defd825d8ac1f47dba374/skills/memory-systems/SKILL.md) | ออกแบบความจำข้าม session, entity/time validity และ retrieval |
| [tool-design](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/9ff0c99108b36d3b886defd825d8ac1f47dba374/skills/tool-design/SKILL.md) | ออกแบบชื่อ schema, result และ error ของ tool ให้ Agent ใช้ถูก |
| [langgraph-human-in-the-loop](https://github.com/langchain-ai/langchain-skills/blob/126c384d8552dcb476b226c244172186cc3f4328/config/skills/langgraph-human-in-the-loop/SKILL.md) | วาง interrupt/resume และ workflow ที่รับการตัดสินใจจากคน |
| [mcp-builder](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/mcp-builder/SKILL.md) | ออกแบบ MCP server และเครื่องมือที่ต่อกับ API ภายนอก |

เริ่มจาก tool เดียวและข้อมูลจำลอง ตรวจ output/error schema แล้วค่อยเพิ่ม memory และการทำงานหลายขั้น

คู่มือประกอบของคลัง: [เปิด playbook](../playbooks/review-agent-extension.md)

## Agent defense

ตรวจขอบเขตสิทธิ์และเส้นทางข้อมูลของระบบ Agent

| Entry | ใช้ทำอะไร |
| --- | --- |
| [vetting-agent-extensions](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-core/skills/vetting-agent-extensions/SKILL.md) | ตรวจข้อความ config, hooks และสิ่งที่เริ่มทำงานเมื่อใช้ skill/plugin/MCP |
| [agent-security](https://github.com/UnitOneAI/SecuritySkills/blob/70bc259bb01abb3015ad2ad859ad5253cbf0bcab/skills/ai-security/agent-security/SKILL.md) | ทบทวนสิทธิ์ Agent, trust boundary, audit trail และ rollback |
| [mcp-server-review](https://github.com/OWASP/secure-agent-playbook/blob/65d4efd2cd0b081d52101e9708792b944e4ddebb/plugins/ai-security-skills/skills/mcp-server-review/SKILL.md) | ตรวจ transport/auth, tool permissions และข้อมูลที่ MCP เปิดเผย |
| [prompt-injection-test](https://github.com/OWASP/secure-agent-playbook/blob/65d4efd2cd0b081d52101e9708792b944e4ddebb/plugins/ai-security-skills/skills/prompt-injection-test/SKILL.md) | จัด test matrix ตามจุดรับข้อมูลและประเภทการโจมตี prompt |
| [multi-agentic-threat-model](https://github.com/OWASP/secure-agent-playbook/blob/65d4efd2cd0b081d52101e9708792b944e4ddebb/plugins/ai-security-skills/skills/multi-agentic-threat-model/SKILL.md) | ทำ threat model ของระบบหลาย Agent ตามชั้นสถาปัตยกรรม |

ทำ inventory ของ tools และ trust boundaries ก่อน วางชุดทดสอบในสภาพแวดล้อมที่คุณมีสิทธิ์ทดสอบ

คู่มือประกอบของคลัง: [เปิด playbook](../playbooks/review-agent-extension.md)

## AppSec

รีวิวการแก้โค้ดและทวนผลตรวจ

| Entry | ใช้ทำอะไร |
| --- | --- |
| [differential-review](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/differential-review/skills/differential-review/SKILL.md) | ตรวจความเสี่ยงที่เกิดจาก diff และผลกระทบต่อผู้เรียกใช้ |
| [agentic-actions-auditor](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SKILL.md) | ตรวจ GitHub Actions ที่เรียก AI และเส้นทางข้อมูลจาก PR/issue |
| [supply-chain-risk-auditor](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SKILL.md) | ตรวจ dependency, advisory, ผู้ดูแลแพ็กเกจ และ install scripts |
| [fp-check](https://github.com/trailofbits/skills/blob/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/fp-check/skills/fp-check/SKILL.md) | ตรวจซ้ำว่ารายงานช่องโหว่มีหลักฐานจริงหรือเป็น false positive |
| [api-security](https://github.com/UnitOneAI/SecuritySkills/blob/70bc259bb01abb3015ad2ad859ad5253cbf0bcab/skills/appsec/api-security/SKILL.md) | ตรวจ API เรื่องสิทธิ์เข้าถึง object/function, auth และการใช้ทรัพยากร |

เลือก diff หนึ่งชุด ไล่ caller และเงื่อนไขเกิดปัญหา แยก finding ที่พิสูจน์ได้ออกจากเรื่องที่ต้องตรวจเพิ่ม

คู่มือประกอบของคลัง: [เปิด playbook](../playbooks/review-diff-with-evidence.md)

## Reverse and DFIR

วิเคราะห์ artifact และเก็บหลักฐานที่ตรวจซ้ำได้

| Entry | ใช้ทำอะไร |
| --- | --- |
| [analyzing-binaries](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-core/skills/analyzing-binaries/SKILL.md) | วิเคราะห์ executable โดยเริ่ม triage ก่อนเลือกจุด decompile |
| [reversing-network-protocols](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-core/skills/reversing-network-protocols/SKILL.md) | เทียบ packet capture กับ client เพื่อกู้ framing และ field ของ protocol |
| [writing-sigma-rules](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-defense/skills/writing-sigma-rules/SKILL.md) | ออกแบบ Sigma rules, ลด noise และแปลงกฎข้าม SIEM |
| [analyzing-memory-images](https://github.com/trilwu/secskills/blob/ca53957bcd8e3b83b5d4d190bb3ad008a4f15c84/secskills-defense/skills/analyzing-memory-images/SKILL.md) | วิเคราะห์ RAM dump เพื่อเรียงหลักฐาน process, network และ injection |

ใช้ binary, packet capture หรือ memory image ที่มีสิทธิ์วิเคราะห์ เก็บ hash ของหลักฐานและแยกข้อสังเกตออกจากข้อสันนิษฐาน

คู่มือประกอบของคลัง: [เปิด playbook](../playbooks/review-diff-with-evidence.md)
