# AI toolbox field guide

[Home](../README.md) · [All tools](../TOOLS.md) · [Source register](../SOURCES.md)

This round adds **44 tools and frameworks**, bringing the register to **61 tools from 90 total source repositories**, alongside the existing 160 skill entries. Links below point to the inspected revisions. Research covers README overviews and license evidence; no upstream package was installed or executed.

## Explore by capability

| Direction | Projects to inspect | ใช้ทำอะไร |
| --- | --- | --- |
| Personal agents | [Hermes Agent](https://github.com/NousResearch/hermes-agent/tree/60f81635c28e825a233f7bb25ed93a2579d5b547) · [Letta Code](https://github.com/letta-ai/letta-code/tree/ad308cd3cb8486afa0bb8ad624c690b828339ea7) | Agent ส่วนตัวที่มี memory, skills และ messaging channels |
| Agent frameworks | [LangGraph](https://github.com/langchain-ai/langgraph/tree/5ea88ecbcdb9fde713c3abd58850a5b7beaa24ec) · [Pydantic AI](https://github.com/pydantic/pydantic-ai/tree/f5c460d46ad9d03200371751d3d89f3ea58433de) · [Agno](https://github.com/agno-agi/agno/tree/0b88f303e1ebd58a92677652fdeaddd7e7618362) · [CrewAI](https://github.com/crewAIInc/crewAI/tree/4254a835b1e5433d123e201928612bc692edbc3e) | ประกอบ Agent logic, state และ workflows ด้วยโค้ด |
| Visual workflows | [Dify](https://github.com/langgenius/dify/tree/8a43387fe4934506f4168943556ad03362d82ad9) · [n8n](https://github.com/n8n-io/n8n/tree/004dea2c9d8ab1b2d28de977073911a41d7ba167) · [FastGPT](https://github.com/labring/FastGPT/tree/ce796cea84abb5a3708a51c2a5851cbf9d7d6441) | ต่อบริการและสร้าง AI workflows ผ่าน canvas |
| Local inference | [Ollama](https://github.com/ollama/ollama/tree/8a89b76cc7359805e48357ba7e5b99e845a4c211) · [llama.cpp](https://github.com/ggml-org/llama.cpp/tree/f3b407ca1bfeeecebf9e9ef19fcd6eed565bd70a) · [vLLM](https://github.com/vllm-project/vllm/tree/bafa5c6c30b8397e64fb6a73740b9ebe71a18f05) · [SGLang](https://github.com/sgl-project/sglang/tree/5fbfcc7170235064125d23feac4b64e5dbe41414) | รันโมเดลบนเครื่องหรือ GPU server และให้บริการ API |
| Chat workspaces | [Open WebUI](https://github.com/open-webui/open-webui/tree/b0e6098e940942281d9c83f3529ea117287a3a22) · [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm/tree/728586d76c843ed25cb7a27c7403f4b79bd960c8) | หน้าแชตและ document workspace แบบ self-host |
| Agent memory | [Mem0](https://github.com/mem0ai/mem0/tree/f1791daa86d469249c9b002f62644d58a1eb96a0) · [Graphiti](https://github.com/getzep/graphiti/tree/ebef986a0b2360211b65751c111cacb4a7d790eb) | เก็บความจำหรือ facts/relations ที่มีเวลาและที่มา |
| Browser automation | [Browser Use](https://github.com/browser-use/browser-use/tree/7fdd63c03fd342aab4fe44507c77c3221ffd43c6) · [Stagehand](https://github.com/browserbase/stagehand/tree/c8e096cb83b6c06ad73e49583fb79a87e78bdd3c) · [Skyvern](https://github.com/Skyvern-AI/skyvern/tree/26d2722b0fc9c7f3246389bdf7385ef18862b242) | ให้ Agent ใช้ browser และดึงข้อมูลตาม schema |
| Document ingestion | [Docling](https://github.com/docling-project/docling/tree/da1eda8a6b4ef62691eee6e72ced4891a30e654c) · [MarkItDown](https://github.com/microsoft/markitdown/tree/ed178952a6672abdfd35b5f9e76a80b6cefc086e) · [MinerU](https://github.com/opendatalab/MinerU/tree/06c3481e9bf534e8d57a3f980e1f4c3cbd79f745) · [Crawl4AI](https://github.com/unclecode/crawl4ai/tree/cae74b203a33994f7e13b9052c3b0d5c93daa0e6) · [Firecrawl](https://github.com/firecrawl/firecrawl/tree/32fa6f6273daecc9675d41dc2dab44c61e8cc500) | เปลี่ยนเอกสารหรือเว็บเป็น context ที่ค้นและอ้างอิงได้ |
| RAG & vector search | [LlamaIndex](https://github.com/run-llama/llama_index/tree/18088d8f070c9212ac4a941b13f759bf417e3031) · [RAGFlow](https://github.com/infiniflow/ragflow/tree/5268b33a39a948931ea285a7fce8ec50461f359b) · [Qdrant](https://github.com/qdrant/qdrant/tree/222b2e44ab1c3f17e8246396ead6558e45041df7) | ต่อ ingestion, retrieval และ vector storage |
| Voice & audio | [LiveKit Agents](https://github.com/livekit/agents/tree/065deca6364096ce0cb79fd41dc1d3e53c64850e) · [Pipecat](https://github.com/pipecat-ai/pipecat/tree/caff2b489bfbee73be0f75e9de7601490205873d) · [faster-whisper](https://github.com/SYSTRAN/faster-whisper/tree/3ec025c4b7526e3fa121e527724ac43afa275a95) · [CosyVoice](https://github.com/QwenAudio/CosyVoice/tree/074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc) | สร้าง voice pipelines, transcription และ TTS |
| Image workflows | [ComfyUI](https://github.com/Comfy-Org/ComfyUI/tree/4d64a8bc072b81c9b47321789b4d83fb7348ae2a) · [Diffusers](https://github.com/huggingface/diffusers/tree/f598e6e6a99528858b962c1399c45b59a6c25484) | ประกอบ image/video pipelines และปรับ generation workflow |
| Coding agents | [OpenCode](https://github.com/anomalyco/opencode/tree/070b980c0b17487dcb94f381cc2eb03953dadb86) · [Aider](https://github.com/Aider-AI/aider/tree/5dc9490bb35f9729ef2c95d00a19ccd30c26339c) · [OpenHands](https://github.com/OpenHands/OpenHands/tree/7b5aa9eb60bdef7d832743c12cabd537b44b8a41) | ทำงานกับ codebase, terminal และ coding automations |
| Training & fine-tuning | [Unsloth](https://github.com/unslothai/unsloth/tree/1f68ed5ea316969676fef6b988a5bc81f504eb37) · [LlamaFactory](https://github.com/hiyouga/LlamaFactory/tree/42b2a546a339b514fd8b88d63959be8fbe297485) | ทดลอง fine-tuning และจัด model/dataset configs |
| Observability | [Langfuse](https://github.com/langfuse/langfuse/tree/47a70342f1736561dfa157a654d011aac29db79d) · [Phoenix](https://github.com/Arize-ai/phoenix/tree/7fa410bda0483fa1e1c694f8bc11501fea2960b9) | ดู traces, prompt versions, experiments และต้นทุน |
| Model gateways | [LiteLLM](https://github.com/BerriAI/litellm/tree/3616014548d40020f508566620c5cd8745721f3c) | รวมหลาย model providers ผ่าน gateway/SDK |
| AI evaluation | [DeepEval](https://github.com/confident-ai/deepeval/tree/0ca198b4640277100efc28b5a862a0170d449c91) · [Ragas](https://github.com/vibrantlabsai/ragas/tree/298b68274234c060deacab3cf5fb52aa3a20e885) | วัดคำตอบ, retrieval และ Agent trajectories |

## Five project directions

These are original project proposals, not prebuilt integrations or measured deployment recipes. Validate each connection and data boundary in a small prototype.

### Personal agent workstation

Start with [Hermes Agent](https://github.com/NousResearch/hermes-agent/tree/60f81635c28e825a233f7bb25ed93a2579d5b547) and [LiteLLM](https://github.com/BerriAI/litellm/tree/3616014548d40020f508566620c5cd8745721f3c).

ใช้ Agent ที่เรียก model APIs แล้วจัด provider routes ตามงาน

**Proof to collect:** One synthetic task, tool permission inventory, bounded retries, sanitized run log. Frameworks can use external models; this does not promise a particular VPS capacity.

### Voice bridge lab

Start with [Pipecat](https://github.com/pipecat-ai/pipecat/tree/caff2b489bfbee73be0f75e9de7601490205873d) and [faster-whisper](https://github.com/SYSTRAN/faster-whisper/tree/3ec025c4b7526e3fa121e527724ac43afa275a95).

ต่อเสียงเข้า → transcription → LLM → TTS แล้ววัดประสบการณ์สนทนา

**Proof to collect:** Thai audio fixtures, word-error samples, first-audio and turn latency, interruption handling. Choose a TTS provider/model with verified Thai support; CosyVoice language coverage is not assumed.

### Document research assistant

Start with [Docling](https://github.com/docling-project/docling/tree/da1eda8a6b4ef62691eee6e72ced4891a30e654c) and [Qdrant](https://github.com/qdrant/qdrant/tree/222b2e44ab1c3f17e8246396ead6558e45041df7).

นำเอกสารเข้า index แล้วให้ Agent ค้นและตอบพร้อมตำแหน่งอ้างอิง

**Proof to collect:** Parsed text/table fixtures, source locators, golden queries and retrieval evaluation. Add Ragas or DeepEval after defining acceptance criteria.

### Model operations dashboard

Start with [LiteLLM](https://github.com/BerriAI/litellm/tree/3616014548d40020f508566620c5cd8745721f3c) and [Langfuse](https://github.com/langfuse/langfuse/tree/47a70342f1736561dfa157a654d011aac29db79d).

รวม provider calls แล้วแสดง cost, latency และ failure traces

**Proof to collect:** Test provider failures, budget accounting, redaction and retention. A gateway does not change provider entitlements.

### Game-development research desk

Start with [OpenCode](https://github.com/anomalyco/opencode/tree/070b980c0b17487dcb94f381cc2eb03953dadb86) and [MarkItDown](https://github.com/microsoft/markitdown/tree/ed178952a6672abdfd35b5f9e76a80b6cefc086e).

แปลงเอกสารเทคนิคเป็น context และใช้ coding agent ช่วยงานใน repository

**Proof to collect:** Versioned documents, scoped repository permissions, evidence-backed diffs and regression results. Preserve source licensing when building a public dataset.

## What to choose first

| Need | First pair to compare | Decision evidence |
| --- | --- | --- |
| Personal API-backed assistant | [Hermes Agent](https://github.com/NousResearch/hermes-agent/tree/60f81635c28e825a233f7bb25ed93a2579d5b547) / [Letta Code](https://github.com/letta-ai/letta-code/tree/ad308cd3cb8486afa0bb8ad624c690b828339ea7) | Channels, memory behavior, permissions and recovery |
| Browser tool in a TypeScript project | [Stagehand](https://github.com/browserbase/stagehand/tree/c8e096cb83b6c06ad73e49583fb79a87e78bdd3c) / [Browser Use](https://github.com/browser-use/browser-use/tree/7fdd63c03fd342aab4fe44507c77c3221ffd43c6) | Supported SDK, repeatable workflow and browser session handling |
| Local model experiments | [Ollama](https://github.com/ollama/ollama/tree/8a89b76cc7359805e48357ba7e5b99e845a4c211) / [llama.cpp](https://github.com/ggml-org/llama.cpp/tree/f3b407ca1bfeeecebf9e9ef19fcd6eed565bd70a) | Model/quant support and observed hardware requirements |
| Serving concurrent model requests | [vLLM](https://github.com/vllm-project/vllm/tree/bafa5c6c30b8397e64fb6a73740b9ebe71a18f05) / [SGLang](https://github.com/sgl-project/sglang/tree/5fbfcc7170235064125d23feac4b64e5dbe41414) | Same model, context, concurrency, throughput and tail latency |
| Documents with difficult layout | [Docling](https://github.com/docling-project/docling/tree/da1eda8a6b4ef62691eee6e72ced4891a30e654c) / [MinerU](https://github.com/opendatalab/MinerU/tree/06c3481e9bf534e8d57a3f980e1f4c3cbd79f745) | Reading order, tables, formulas, citation locations and license scope |
| Real-time voice application | [LiveKit Agents](https://github.com/livekit/agents/tree/065deca6364096ce0cb79fd41dc1d3e53c64850e) / [Pipecat](https://github.com/pipecat-ai/pipecat/tree/caff2b489bfbee73be0f75e9de7601490205873d) | Transport needs, turn-taking, provider compatibility and Thai voice fixtures |

## Source quality notes

- Flowise was excluded from active additions because the inspected GitHub metadata marks its repository archived.
- Letta selections use `letta-ai/letta-code`, the current source identified by the legacy repository README.
- Firecrawl and CosyVoice use their current canonical organizations.
- Dify, FastGPT, Open WebUI, MinerU, n8n, Phoenix and open-core packages need scoped license labels; source visibility alone does not establish unrestricted reuse.
- Core/library, model weights, plugins, optional enterprise features and hosted services can have different terms. Consult [source and license notes](../SOURCES.md).
- Stars, vendor performance claims and managed-platform benchmark scores are not reproduced as catalog quality scores.

## Search offline

```bash
python3 scripts/arsenal.py tools "memory"
python3 scripts/arsenal.py tools --group "Voice & audio"
python3 scripts/arsenal.py tools "" --group "Coding agents" --json
```
