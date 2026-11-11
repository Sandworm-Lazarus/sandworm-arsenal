# MCP, TypeScript and privacy: five useful additions

[Home](../../README.md) · [All tools](../../TOOLS.md) · [Maintenance](../maintenance.md)

Research date: 2026-11-11. Scope: primary README and license overviews at the recorded revisions. These additions fill capability gaps rather than increase the skill-entry count. No upstream package or integration was executed.

| Project | Gap it fills | Before adoption |
| --- | --- | --- |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector/tree/4d3464cb3a6dde609d7b5ac24c440b947eb40f23) | ตรวจและเรียก MCP servers ผ่าน web, CLI หรือ terminal interface | เครื่องมืออาจเก็บ OAuth/env secrets; ตรวจ keychain หรือ encrypted storage เมื่อใช้ headless/VPS |
| [Mastra](https://github.com/mastra-ai/mastra/tree/59a60e42d5985980d1a36cf0bcddeead09283703) | สร้าง Agents, graph workflows, memory และ MCP integrations บน TypeScript | Apache core แยก ee directories; ทดลอง suspend/resume และ retry ด้วย task สังเคราะห์ |
| [Vercel AI SDK](https://github.com/vercel/ai/tree/70e45d5878494be4b66e325187f865951025059e) | ต่อ text/streaming, structured outputs, tools และ UI สำหรับแอป TypeScript | String model ID อาจเลือก Vercel AI Gateway; adapter โดยตรงเป็นอีกเส้นทาง ต้องบันทึก provider/billing route |
| [Presidio](https://github.com/data-privacy-stack/presidio/tree/1d7005932261a4b676e045d16fa2965dbc4b4ba2) | ค้นและ de-identify ข้อมูล PII ใน text/images ก่อนนำไปใช้ต่อ | ใช้ canonical community repository; ทดสอบข้อมูลภาษาไทยและ false negatives จริง การตรวจอัตโนมัติไม่รับรองว่าพบ PII ครบ |
| [Bruno](https://github.com/usebruno/bruno/tree/60d7517d0545ef82c032c10dcbb6a3c815d246cf) | เก็บ API request collections เป็นไฟล์และรันทดสอบผ่าน desktop/CLI | Collection อยู่ local และใช้ Git ได้; HTTP requests ยังติดต่อ API เป้าหมาย และ paid editions มี feature scope แยก |

## Three small trial tasks

### Inspect a minimal MCP server

Use MCP Inspector against a disposable local server with synthetic inputs. Inventory advertised tools, exercise one valid call and one invalid input, and record transport, errors, permissions and credentials storage. A responsive server is not evidence that authorization is correct. Read the Inspector revision-specific engine and secret-storage documentation first.

### Build a TypeScript AI endpoint

Compare Vercel AI SDK for provider/streaming/UI integration with Mastra for stateful Agent/workflow orchestration. Start with one read-only tool and a fixed task. Record the exact provider route, retry budget, schema-validation result, failure behavior and persistence assumptions. Gateway routing and direct provider adapters can have different billing/data paths.

### Evaluate a privacy preprocessing policy

Use the original [synthetic privacy cases](../../examples/privacy-fixtures.json) to define intended masking behavior. Treat recognizer coverage and language support as measurements. Include benign version numbers, already masked values, missing fields and Thai text. The fixture describes product expectations; it does not certify Presidio defaults. Keep private data out of the trial.

## Primary evidence

| Repository | README inspected | License scope |
| --- | --- | --- |
| modelcontextprotocol/inspector | [Pinned README](https://github.com/modelcontextprotocol/inspector/blob/4d3464cb3a6dde609d7b5ac24c440b947eb40f23/README.md) | [Apache-2.0 transition; retained MIT contributions; docs CC-BY-4.0](https://github.com/modelcontextprotocol/inspector/blob/4d3464cb3a6dde609d7b5ac24c440b947eb40f23/LICENSE) |
| mastra-ai/mastra | [Pinned README](https://github.com/mastra-ai/mastra/blob/59a60e42d5985980d1a36cf0bcddeead09283703/README.md) | [Apache-2.0 outside ee directories; separate enterprise terms](https://github.com/mastra-ai/mastra/blob/59a60e42d5985980d1a36cf0bcddeead09283703/LICENSE.md) |
| vercel/ai | [Pinned README](https://github.com/vercel/ai/blob/70e45d5878494be4b66e325187f865951025059e/packages/ai/README.md) | [Apache-2.0](https://github.com/vercel/ai/blob/70e45d5878494be4b66e325187f865951025059e/LICENSE) |
| data-privacy-stack/presidio | [Pinned README](https://github.com/data-privacy-stack/presidio/blob/1d7005932261a4b676e045d16fa2965dbc4b4ba2/README.MD) | [MIT](https://github.com/data-privacy-stack/presidio/blob/1d7005932261a4b676e045d16fa2965dbc4b4ba2/LICENSE) |
| usebruno/bruno | [Pinned README](https://github.com/usebruno/bruno/blob/60d7517d0545ef82c032c10dcbb6a3c815d246cf/readme.md) | [MIT source; commercial editions/features separate](https://github.com/usebruno/bruno/blob/60d7517d0545ef82c032c10dcbb6a3c815d246cf/license.md) |

Presidio now uses the Data Privacy Stack community repository. The Vercel repository README is a symlink; the recorded overview follows its in-repository target `packages/ai/README.md`. Package/library, enterprise features, hosted services and model-provider terms should be considered at their actual scopes.
