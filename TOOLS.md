# Companion tools

[Home](README.md) · [Skill catalog](CATALOG.md) · [Sources and licenses](SOURCES.md)

These are executable tools and frameworks, counted separately from agent skills. Their README/source overviews were inspected; this repository has not installed or run them. Links point to the recorded revision.

**66 tools and frameworks in 26 groups.** See the [AI toolbox guide](docs/ai-toolbox.md) for task-oriented combinations.

| Group | Tools |
| --- | ---: |
| [Skill review](#skill-review) | 2 |
| [AI evaluation](#ai-evaluation) | 7 |
| [Secrets](#secrets) | 1 |
| [Containers / IaC](#containers-iac) | 2 |
| [Supply chain](#supply-chain) | 4 |
| [CI security](#ci-security) | 1 |
| [Code analysis](#code-analysis) | 2 |
| [Personal agents](#personal-agents) | 2 |
| [Agent frameworks](#agent-frameworks) | 5 |
| [Visual workflows](#visual-workflows) | 3 |
| [Local inference](#local-inference) | 4 |
| [Chat workspaces](#chat-workspaces) | 2 |
| [Agent memory](#agent-memory) | 2 |
| [Browser automation](#browser-automation) | 3 |
| [Document ingestion](#document-ingestion) | 5 |
| [RAG & vector search](#rag-vector-search) | 3 |
| [Voice & audio](#voice-audio) | 4 |
| [Image workflows](#image-workflows) | 2 |
| [Coding agents](#coding-agents) | 3 |
| [Training & fine-tuning](#training-fine-tuning) | 2 |
| [Observability](#observability) | 2 |
| [Model gateways](#model-gateways) | 1 |
| [MCP development](#mcp-development) | 1 |
| [AI application SDKs](#ai-application-sdks) | 1 |
| [Privacy & data handling](#privacy-data-handling) | 1 |
| [API testing](#api-testing) | 1 |

<a id="skill-review"></a>

## Skill review

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [skill-scanner](https://github.com/cisco-ai-defense/skill-scanner/tree/c558c421157c546ec417cf23778ce81a3a8f35fd) | ตรวจ pattern, AST/dataflow และเนื้อหา skill | Skill directory และ scanner dependencies. แยก static, optional LLM/cloud และ runtime evidence |
| [agent-scan](https://github.com/snyk/agent-scan/tree/59def8c624f9d7bef4d49992a4da5e68f83f4e75) | ตรวจความเสี่ยง Agent/MCP configuration และ components | MCP config, scanner และ service access ตามโหมด. บางโหมดเริ่ม server หรือส่ง content ไป API; ตรวจ data flow |

<a id="ai-evaluation"></a>

## AI evaluation

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator/tree/194f7f975e9dbcf5bc795a7de1147e960ea9a40a) | ตรวจโครงสร้างและประเมินผลมี/ไม่มี skill | Skill package, eval tasks และ model/runtime. Experimental; live evaluation อาจมีค่าใช้จ่าย |
| [PyRIT](https://github.com/microsoft/PyRIT/tree/3b70c3c98f2b07b2f0e435d926de3d44a8bd2ec6) | ประเมิน security/safety ของระบบ generative AI อย่างเป็นระบบ | Python และ model/application target ที่ได้รับอนุญาต. การทดสอบสร้างหลาย model calls; กำหนดงบและเก็บผลทั้งสำเร็จและล้มเหลว |
| [garak](https://github.com/NVIDIA/garak/tree/892779207cbc38f65a738ef9cbdfbc1e83aa0b55) | ใช้ probes สำรวจ failure modes ของ LLM application | Python, model connector และ probe configuration. ผลขึ้นกับ probes และ detector; ไม่ใช้สรุปว่าปลอดภัยครอบคลุมทุกกรณี |
| [promptfoo](https://github.com/promptfoo/promptfoo/tree/b3603fab85bb331da98a8b68ca442e1f4af7e368) | ทำ regression eval และเปรียบเทียบ prompts, Agents และ RAG | Node/CLI, provider access และ test cases. API calls มีต้นทุน; ตรวจ cloud/red-team mode และการส่งข้อมูลก่อนใช้ |
| [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai/tree/67873ea965f2d5acd46b2327ea17aecff30026c1) | สร้างและรัน model evaluations ที่มี tasks, solvers และ scorers | Python/uv และ model provider หรือ local backend. แยก scorer quality, task revision และ tool permissions ในรายงาน |
| [DeepEval](https://github.com/confident-ai/deepeval/tree/0ca198b4640277100efc28b5a862a0170d449c91) | เขียน eval สำหรับ outputs, RAG และ Agent/tool trajectories | Python, task fixtures และ judge/model backend ตาม metric. LLM judges มีต้นทุนและความคลาดเคลื่อน; รักษา acceptance checks ที่ตรวจได้อิสระ |
| [Ragas](https://github.com/vibrantlabsai/ragas/tree/298b68274234c060deacab3cf5fb52aa3a20e885) | วัดคุณภาพ LLM/RAG และสร้าง test sets จากข้อมูลตัวอย่าง | Python, dataset และ LLM/embedding backend ตาม metric. Synthetic tests และ judge scores ต้องตรวจ bias/coverage ก่อนตัดสินระบบจริง |

<a id="secrets"></a>

## Secrets

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [gitleaks](https://github.com/gitleaks/gitleaks/tree/5f6ec56cfa6f8c67648d863582c7ae2f206d5c1c) | ค้น credential patterns ใน repository และ files | CLI และ target files/history. README ระบุ feature-complete และรับ security patches; ผู้ดูแลชี้ไป Betterleaks |

<a id="containers-iac"></a>

## Containers / IaC

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [trivy](https://github.com/aquasecurity/trivy/tree/0e40f8178a375c68aeca146e4dc4e89ff1009587) | ตรวจ vulnerabilities, misconfiguration, secrets และ SBOM | CLI, image/files และ vulnerability database. ฐานข้อมูลและ coverage เปลี่ยนได้; finding ต้องทวน reachability และ false positives |
| [checkov](https://github.com/bridgecrewio/checkov/tree/c7f1a45fac5712d4cbaef22946109e20a41a1cef) | ตรวจ IaC, container และ dependency configuration ก่อน deploy | Python/CLI และ Terraform/Kubernetes/Docker/config files. ตรวจการเรียก API, external modules และ cloud features ตามโหมด |

<a id="supply-chain"></a>

## Supply chain

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [syft](https://github.com/anchore/syft/tree/a0c0d3890a9d79421c403e8fcadec50a2e55bf21) | สร้าง SBOM จาก container images และ filesystems | CLI และ image/filesystem. เป็น inventory; ใช้ scanner เช่น Grype เพิ่มเพื่อตรวจ vulnerability |
| [grype](https://github.com/anchore/grype/tree/cd1f23eb50dfb52647090158f453c7359172591f) | ตรวจ known vulnerabilities จาก images, filesystems หรือ SBOM | CLI, artifact/SBOM และ vulnerability database. จับคู่ package/CVE ไม่เท่ากับยืนยัน exploitability |
| [osv-scanner](https://github.com/google/osv-scanner/tree/7de3a036f48e34cdb3a1d396143b11dbba34be52) | จับคู่ dependencies กับข้อมูลช่องโหว่ OSV | CLI, lockfiles/source และ database access ตามโหมด. ต้องระบุ artifact และ database revision เพื่ออธิบายผลที่เปลี่ยนตามเวลา |
| [scorecard](https://github.com/ossf/scorecard/tree/5a951604a5ff7d99b7222139ba522237c58228af) | ตรวจสัญญาณ security hygiene ของ open-source repository | Repository metadata และ API access ตาม checks. Score เป็น hygiene indicators ไม่ใช่การรับรองว่าโค้ดไม่มีช่องโหว่ |

<a id="ci-security"></a>

## CI security

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [zizmor](https://github.com/zizmorcore/zizmor/tree/33ece2d3d6c60f3d669b8a69e095f60d8a980c0b) | ตรวจ CI/CD config รวม GitHub Actions และ permission risks | Workflow/config files และ CLI. Static analysis; ต้องทวน reusable actions และบริบท runner เพิ่ม |

<a id="code-analysis"></a>

## Code analysis

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [codeql](https://github.com/github/codeql/tree/ccc03491fc436578bfeecb7e75305d4d64e02118) | ใช้ query libraries และ checks สำหรับ semantic security analysis | CodeQL CLI/database และ toolchain ตามภาษา. MIT ใน repo นี้ครอบคลุม queries/libraries; CLI มีเงื่อนไขแยก |
| [semgrep](https://github.com/semgrep/semgrep/tree/06d9993409f6698f78f6956cd39d968e7f4d7b6a) | ค้น pattern และ taint flows ด้วย static analysis | CLI และ rulesets ตาม engine/edition. Engine, rules และ Pro features ใช้เงื่อนไขต่างกัน; ตรวจ license และ telemetry |

<a id="personal-agents"></a>

## Personal agents

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent/tree/60f81635c28e825a233f7bb25ed93a2579d5b547) | Agent ส่วนตัวที่ใช้ tools, memory, skills และ messaging gateways | Python/runtime, model provider และ integrations ที่เลือก. เหมาะศึกษา Agent บน VPS ที่เรียกโมเดลผ่าน API; ตรวจสิทธิ์ terminal, persistence และ channel secrets |
| [Letta Code](https://github.com/letta-ai/letta-code/tree/ad308cd3cb8486afa0bb8ad624c690b828339ea7) | สร้าง stateful agent harness ที่มี memory, skills, channels และ scheduling | Node/CLI และ provider/host configuration ตาม mode. ใช้ source ปัจจุบันแทน retired V1 server ใน letta-ai/letta; ตรวจเงื่อนไข remote/cloud features |

<a id="agent-frameworks"></a>

## Agent frameworks

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [LangGraph](https://github.com/langchain-ai/langgraph/tree/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec) | สร้าง stateful workflow ที่มี durable execution และจุดให้คนตรวจ | Python หรือ JS/TS counterpart, state store และ model provider. เป็น orchestration layer; ต้องกำหนด retry, checkpoint และ tool policy เองตามระบบ |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai/tree/f5c460d46ad9d03200371751d3d89f3ea58433de) | สร้าง typed Agents, tool calls และ structured outputs ใน Python | Python, Pydantic และ model/provider ที่รองรับ. Typed schema ไม่รับรองความถูกต้องเชิงเนื้อหา; แยก SDK จาก hosted Logfire/Gateway |
| [Agno](https://github.com/agno-agi/agno/tree/0b88f303e1ebd58a92677652fdeaddd7e7618362) | สร้าง Agent teams/workflows และให้บริการผ่าน API/MCP ด้วย AgentOS | Python, storage/runtime และ model credentials ตามการ deploy. แยก framework, AgentOS และ platform/UI features ก่อนเลือก stack |
| [CrewAI](https://github.com/crewAIInc/crewAI/tree/4254a835b1e5433d123e201928612bc692edbc3e) | จัด role-based agent collaboration และ event-driven Flows | Python และ model/tool integrations. แยก open framework จาก AMP/control-plane features; วัดประโยชน์ของหลาย Agent ด้วยงานจริง |
| [Mastra](https://github.com/mastra-ai/mastra/tree/59a60e42d5985980d1a36cf0bcddeead09283703) | สร้าง Agents, graph workflows, memory และ MCP integrations บน TypeScript | Node/TypeScript, provider credentials และ storage ตาม feature. Apache core แยก ee directories; ทดลอง suspend/resume และ retry ด้วย task สังเคราะห์ |

<a id="visual-workflows"></a>

## Visual workflows

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Dify](https://github.com/langgenius/dify/tree/8a43387fe4934506f4168943556ad03362d82ad9) | สร้าง LLM apps, workflow และ RAG ผ่าน visual workspace | Docker Compose, backing services และ model/embedding endpoints. Modified Apache license มีข้อกำหนดเพิ่ม; อ่านเงื่อนไข multi-tenant และ branding ก่อนนำไปทำบริการ |
| [n8n](https://github.com/n8n-io/n8n/tree/004dea2c9d8ab1b2d28de977073911a41d7ba167) | ต่อ workflows ระหว่าง AI, webhooks, messaging และบริการอื่น | Node/Docker, persistent storage และ integration credentials. Sustainable Use License และ enterprise scope แยก; source-available ไม่เท่ากับ permissive license |
| [FastGPT](https://github.com/labring/FastGPT/tree/ce796cea84abb5a3708a51c2a5851cbf9d7d6441) | สร้าง knowledge-based chat และ visual AI workflows | Self-hosted platform services และ model/embedding providers. Custom FastGPT license เพิ่มเงื่อนไข SaaS/branding; ไม่ติดป้ายเป็น Apache แบบไม่มีเงื่อนไข |

<a id="local-inference"></a>

## Local inference

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Ollama](https://github.com/ollama/ollama/tree/8a89b76cc7359805e48357ba7e5b99e845a4c211) | จัดการและเรียกโมเดลผ่าน local runtime และ REST API | Model artifacts และ CPU/GPU/RAM ที่เหมาะกับโมเดล. เลือก local/cloud backend ให้ชัด; MIT ของ runtime ไม่ใช่สิทธิ์ของ model weights ทุกตัว |
| [llama.cpp](https://github.com/ggml-org/llama.cpp/tree/f3b407ca1bfeeecebf9e9ef19fcd6eed565bd70a) | รัน LLM/VLM และ quantized models บน hardware หลายชนิด | Binary/build backend และ model format ที่รองรับ. เหมาะสำรวจ CPU/GPU hybrid และ GGUF; วัด latency/VRAM กับโมเดลจริง |
| [vLLM](https://github.com/vllm-project/vllm/tree/bafa5c6c30b8397e64fb6a73740b9ebe71a18f05) | ให้บริการโมเดลด้วย batching, KV cache และ API server | Supported model/backend และ hardware/runtime ตามรุ่น. เหมาะเทียบ serving throughput; concurrency และ context มีผลต่อ memory และ latency |
| [SGLang](https://github.com/sgl-project/sglang/tree/5fbfcc7170235064125d23feac4b64e5dbe41414) | วาง inference serving สำหรับ LLM, multimodal และ agentic workloads | Model/backend และ hardware ที่ cookbook รองรับ. ตรวจ engine/model compatibility; ไม่ใช้ตัวเลขเร็วที่สุดจาก marketing เป็นผลทดสอบของคลัง |

<a id="chat-workspaces"></a>

## Chat workspaces

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Open WebUI](https://github.com/open-webui/open-webui/tree/b0e6098e940942281d9c83f3529ea117287a3a22) | สร้าง self-hosted chat UI ที่ต่อ local models หรือ compatible APIs | Python/Docker และ inference/embedding endpoints. Open WebUI License มีเงื่อนไข branding; offline mode ต้องตรวจ dependencies และ provider routes |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm/tree/728586d76c843ed25cb7a27c7403f4b79bd960c8) | ใช้ workspace chat, documents, RAG และ Agents บน desktop/server | Desktop/Docker หรือ Node stack และ model/embedding backend. Desktop กับ Docker มี feature scope ต่างกัน; ตรวจ ingestion และ outbound provider calls |

<a id="agent-memory"></a>

## Agent memory

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Mem0](https://github.com/mem0ai/mem0/tree/f1791daa86d469249c9b002f62644d58a1eb96a0) | เพิ่ม memory layer ที่แยก user/session/agent context | SDK, LLM/embedding backend และ memory store. README แยก managed benchmark จาก OSS SDK; อย่าโอนคะแนน managed มาอ้างเป็นผลของ self-host |
| [Graphiti](https://github.com/getzep/graphiti/tree/ebef986a0b2360211b65751c111cacb4a7d790eb) | เก็บ entities, relationships และ facts ที่มีช่วงเวลาความถูกต้อง | Graph backend และ LLM/embedding setup ตาม integration. เหมาะข้อมูลที่เปลี่ยนตามเวลา; ออกแบบ provenance, deletion และ tenant isolation |

<a id="browser-automation"></a>

## Browser automation

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Browser Use](https://github.com/browser-use/browser-use/tree/7fdd63c03fd342aab4fe44507c77c3221ffd43c6) | ให้ Agent โต้ตอบ browser จริงและอ่านผลผ่าน browser harness | Python/browser runtime และ LLM provider หรือ hosted service. Local library กับ Cloud เป็นคนละ deployment; session/cookies และ tool permissions ต้องตรงงาน |
| [Stagehand](https://github.com/browserbase/stagehand/tree/c8e096cb83b6c06ad73e49583fb79a87e78bdd3c) | ใช้ observe, act และ schema-based extraction ใน browser automation | JS/TS หรือ Python SDK, browser และ model provider. มี local browser และ hosted options; ตรวจ data path ของ page content และ screenshots |
| [Skyvern](https://github.com/Skyvern-AI/skyvern/tree/26d2722b0fc9c7f3246389bdf7385ef18862b242) | ทำ browser workflows ด้วย vision/LLM และ workflow builder | Browser runtime, app services และ model access. AGPL-3.0 ใน source; local/Cloud ไม่ควรถูกสมมติว่ามี feature parity |

<a id="document-ingestion"></a>

## Document ingestion

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Crawl4AI](https://github.com/unclecode/crawl4ai/tree/cae74b203a33994f7e13b9052c3b0d5c93daa0e6) | แปลงเว็บเป็น Markdown หรือ structured data สำหรับ Agent/RAG | Python/browser หรือ Docker; hosted API เป็นอีกตัวเลือก. แยก self-hosted crawler จาก Cloud endpoints; ตั้ง crawl scope และ budget |
| [Docling](https://github.com/docling-project/docling/tree/da1eda8a6b4ef62691eee6e72ced4891a30e654c) | แยก layout, tables, OCR และ export เอกสารเป็นข้อมูลสำหรับ AI | Python และ parser/OCR/model dependencies ตาม format. Model artifacts อาจมีสิทธิ์แยก; ตรวจ tables, reading order และ citation locators กับ fixture จริง |
| [MarkItDown](https://github.com/microsoft/markitdown/tree/ed178952a6672abdfd35b5f9e76a80b6cefc086e) | แปลงเอกสารหลายชนิดเป็น Markdown สำหรับ text-analysis pipelines | Python และ format-specific dependencies. Converter ใช้สิทธิ์ I/O ของ process; image captioning/audio บางงานอาจเรียกบริการภายนอก |
| [MinerU](https://github.com/opendatalab/MinerU/tree/06c3481e9bf534e8d57a3f980e1f4c3cbd79f745) | parse เอกสารซับซ้อน ตาราง สูตร และ scanned pages เป็น Markdown/JSON | Parser/runtime และ hardware/model backend ตาม mode. MinerU license เพิ่มเงื่อนไขจาก Apache; ตรวจ API รุ่นจริงและข้อกำหนดของ models |
| [Firecrawl](https://github.com/firecrawl/firecrawl/tree/32fa6f6273daecc9675d41dc2dab44c61e8cc500) | ค้น scrape crawl และแปลงเว็บ/เอกสารเป็น context สำหรับ Agent | Hosted API หรือ self-hosted services ตามการใช้งาน. ใช้ canonical firecrawl/firecrawl; AGPL source และ hosted features/terms ต้องตรวจแยก |

<a id="rag-vector-search"></a>

## RAG & vector search

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [LlamaIndex](https://github.com/run-llama/llama_index/tree/18088d8f070c9212ac4a941b13f759bf417e3031) | ประกอบ ingestion, retrieval และ agentic document workflows | Python core/integrations และ model/vector backends. README ระบุ focus ของบริษัทไป LlamaParse; แยก OSS framework จาก hosted parsing products |
| [RAGFlow](https://github.com/infiniflow/ragflow/tree/5268b33a39a948931ea285a7fce8ec50461f359b) | จัด document ingestion, retrieval และ agentic context workflows | Self-hosted service stack และ model/storage backends. ประเมินความต้องการ RAM/storage จาก deployment docs; ไม่อนุมานว่าเหมาะกับ VPS เล็กทุกเครื่อง |
| [Qdrant](https://github.com/qdrant/qdrant/tree/222b2e44ab1c3f17e8246396ead6558e45041df7) | เก็บและค้น vectors พร้อม payload filters เพื่อ semantic retrieval | Qdrant server/embedded option และ embedding model. Quickstart container ไม่ใช่ production security config; แยก auth, exposure และ tenant controls |

<a id="voice-audio"></a>

## Voice & audio

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [LiveKit Agents](https://github.com/livekit/agents/tree/065deca6364096ce0cb79fd41dc1d3e53c64850e) | สร้าง real-time voice/video Agents ที่เชื่อม STT, LLM และ TTS | Agents runtime, LiveKit transport และ speech/model providers. Framework ไม่ใช่เสียงไทยสำเร็จรูป; เลือก provider แล้ววัด turn latency และ interruptions |
| [Pipecat](https://github.com/pipecat-ai/pipecat/tree/caff2b489bfbee73be0f75e9de7601490205873d) | ประกอบ streaming voice/multimodal pipelines และ conversation flows | Python, transport และ STT/LLM/TTS components. ต่อ APIs ได้โดยไม่ host ทุกโมเดลเอง; วัด end-to-end latency แยกจากแต่ละ service |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper/tree/3ec025c4b7526e3fa121e527724ac43afa275a95) | ถอดเสียงด้วย Whisper ผ่าน CTranslate2 บน CPU/GPU | Python, model files และ CTranslate2-compatible runtime. Benchmark ใน README ผูก hardware/config; ต้องวัดคำผิดและ latency กับเสียงไทยจริง |
| [CosyVoice](https://github.com/QwenAudio/CosyVoice/tree/074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc) | สร้างเสียง TTS และศึกษาการ streaming/control ของ speech models | Python, checkpoint และ inference hardware/runtime ตามรุ่น. ย้ายจาก FunAudioLLM ไป QwenAudio; รายชื่อภาษาใน README ที่อ่านไม่ได้ยืนยันภาษาไทย |

<a id="image-workflows"></a>

## Image workflows

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [ComfyUI](https://github.com/Comfy-Org/ComfyUI/tree/4d64a8bc072b81c9b47321789b4d83fb7348ae2a) | ประกอบ image/video/audio generation ผ่าน node-graph workflows | Model artifacts และ compute ตาม workflow. GPL ของโปรแกรมแยกจาก model/custom-node licenses; custom nodes เป็น code ที่ต้องตรวจเอง |
| [Diffusers](https://github.com/huggingface/diffusers/tree/f598e6e6a99528858b962c1399c45b59a6c25484) | สร้าง diffusion pipelines และปรับ schedulers/models ใน Python | Python/PyTorch, model files และ compatible hardware. Library Apache-2.0 ไม่ได้ครอบคลุม model weights ทุกตัว; GPU/VRAM ขึ้นกับ pipeline |

<a id="coding-agents"></a>

## Coding agents

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [OpenHands](https://github.com/OpenHands/OpenHands/tree/7b5aa9eb60bdef7d832743c12cabd537b44b8a41) | จัด coding agents และ automations ผ่าน self-hosted Agent Canvas | App/runtime backend, model access และ sandbox ตาม setup. Agent สามารถเปลี่ยนไฟล์และเรียก tools; จำกัด repository/workspace ตามงาน |
| [Aider](https://github.com/Aider-AI/aider/tree/5dc9490bb35f9729ef2c95d00a19ccd30c26339c) | ทำ AI pair programming ใน terminal พร้อม repo map และ Git integration | Python, Git และ LLM provider/local endpoint. ตรวจ auto-commit/test behavior; model examples ใน README ไม่ใช่คำแนะนำรุ่นปัจจุบันของคลัง |
| [OpenCode](https://github.com/anomalyco/opencode/tree/070b980c0b17487dcb94f381cc2eb03953dadb86) | ใช้ coding agent แบบ terminal/desktop พร้อม build และ plan modes | CLI/desktop runtime และ provider configuration. MIT ของ client ไม่รับรองราคา โควตา หรือเงื่อนไขโมเดลของ provider |

<a id="training-fine-tuning"></a>

## Training & fine-tuning

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Unsloth](https://github.com/unslothai/unsloth/tree/1f68ed5ea316969676fef6b988a5bc81f504eb37) | รันและ fine-tune โมเดลด้วย core package และ optional UI/workflows | Model/dataset และ hardware/runtime ที่รองรับ. README แบ่ง Apache core กับ AGPL optional components; ตรวจ file scope และ model/dataset licenses |
| [LlamaFactory](https://github.com/hiyouga/LlamaFactory/tree/42b2a546a339b514fd8b88d63959be8fbe297485) | จัด fine-tuning ผ่าน CLI/Web UI พร้อม configs และ datasets | Python, supported model และ training hardware/backend. ประเมิน VRAM/compute จาก sequence length และวิธีฝึกจริง; ไม่รับรอง savings ที่ยังไม่วัด |

<a id="observability"></a>

## Observability

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Langfuse](https://github.com/langfuse/langfuse/tree/47a70342f1736561dfa157a654d011aac29db79d) | เก็บ traces, prompt versions, datasets และ Agent evaluations | SDK instrumentation และ Cloud/self-hosted stack. MIT สำหรับส่วนที่ระบุ; ee directories มีสิทธิ์แยก และ traces อาจมี prompts/ข้อมูลผู้ใช้ |
| [Phoenix](https://github.com/Arize-ai/phoenix/tree/7fa410bda0483fa1e1c694f8bc11501fea2960b9) | วิเคราะห์ LLM traces, retrieval evals, datasets และ experiments | Instrumentation และ local/container/cloud backend. Root LICENSE เป็น ELv2; ไม่ติดป้าย Apache/MIT และต้องตรวจข้อจำกัด hosted service |

<a id="model-gateways"></a>

## Model gateways

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [LiteLLM](https://github.com/BerriAI/litellm/tree/3616014548d40020f508566620c5cd8745721f3c) | รวม model providers ผ่าน SDK/proxy พร้อม cost/routing controls | Provider credentials และ SDK/proxy runtime ตาม mode. MIT scope แยก enterprise directory; gateway ไม่เพิ่มสิทธิ์หรือโควตาจาก model provider |

<a id="mcp-development"></a>

## MCP development

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector/tree/4d3464cb3a6dde609d7b5ac24c440b947eb40f23) | ตรวจและเรียก MCP servers ผ่าน web, CLI หรือ terminal interface | Node runtime ตาม engine ของ revision, MCP server/config และ connection credentials. เครื่องมืออาจเก็บ OAuth/env secrets; ตรวจ keychain หรือ encrypted storage เมื่อใช้ headless/VPS |

<a id="ai-application-sdks"></a>

## AI application SDKs

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Vercel AI SDK](https://github.com/vercel/ai/tree/70e45d5878494be4b66e325187f865951025059e) | ต่อ text/streaming, structured outputs, tools และ UI สำหรับแอป TypeScript | Node 22+ ตาม README ที่อ่าน, provider adapter หรือ gateway และ UI integration ตามงาน. String model ID อาจเลือก Vercel AI Gateway; adapter โดยตรงเป็นอีกเส้นทาง ต้องบันทึก provider/billing route |

<a id="privacy-data-handling"></a>

## Privacy & data handling

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Presidio](https://github.com/data-privacy-stack/presidio/tree/1d7005932261a4b676e045d16fa2965dbc4b4ba2) | ค้นและ de-identify ข้อมูล PII ใน text/images ก่อนนำไปใช้ต่อ | Python, NLP/recognizer dependencies และ anonymization policy ตามข้อมูล. ใช้ canonical community repository; ทดสอบข้อมูลภาษาไทยและ false negatives จริง การตรวจอัตโนมัติไม่รับรองว่าพบ PII ครบ |

<a id="api-testing"></a>

## API testing

| Tool | ใช้ทำอะไร | ต้องมี / ข้อจำกัด |
| --- | --- | --- |
| [Bruno](https://github.com/usebruno/bruno/tree/60d7517d0545ef82c032c10dcbb6a3c815d246cf) | เก็บ API request collections เป็นไฟล์และรันทดสอบผ่าน desktop/CLI | Desktop app หรือ CLI, API test environment และ credentials ที่แยกจาก collection. Collection อยู่ local และใช้ Git ได้; HTTP requests ยังติดต่อ API เป้าหมาย และ paid editions มี feature scope แยก |
