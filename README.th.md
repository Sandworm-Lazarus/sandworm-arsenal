<p align="center"><img src="assets/banner.svg" alt="Sandworm Arsenal — คลังสกิล AI และ Cyber" width="100%"></p>

<p align="center"><b>160 สกิล · 29 คลังต้นทาง · 61 เครื่องมือประกอบ</b><br>คัดและเรียบเรียงโดย <a href="https://github.com/Sandworm-Lazarus">Sandworm-Lazarus</a> · ตรวจต้นทาง 11 พฤศจิกายน 2026</p>

<p align="center"><a href="README.md">English</a> · <a href="CATALOG.md">ดูสกิลทั้งหมด</a> · <a href="docs/starter-packs.md">ชุดเริ่มต้น</a> · <a href="SOURCES.md">ต้นทางและสิทธิ์ใช้งาน</a></p>

# Sandworm Arsenal

คลังสกิล **AI และ Cybersecurity** ที่คัดไว้ใช้เรียนรู้และต่อยอด มีคำอธิบายภาษาไทย ลิงก์ระบุ commit และหมายเหตุเรื่องเครื่องมือที่ต้องใช้ เพื่อให้เลือกได้ว่าสกิลไหนตรงกับงานของเรา

ผลงานของคลังนี้คือการคัดสรร สรุปข้อมูล จัดชุดเริ่มต้น เขียน playbook 3 ชุด และทำเครื่องมือค้นหารายการแบบออฟไลน์ สกิลที่ลิงก์ออกไปยังเป็นผลงานของผู้เขียนต้นทาง และไม่ได้คัดลอกโค้ดทั้งแพ็กมารวมไว้ที่นี่

## เครื่องมือ AI นอกเหนือจากสกิล

เพิ่ม [AI toolbox guide](docs/ai-toolbox.md) อีก 44 โครงการ ครอบคลุม Agent ส่วนตัว, local models, voice, browser automation, เอกสาร, memory, ภาพ, coding และ model operations พร้อมแนวทางทำโปรเจกต์ของตัวเอง 5 แบบ

## เลือกตามงาน

| หมวด | เหมาะกับอะไร | เริ่มจาก |
| --- | --- | --- |
| AI Engineering | รันโมเดล, quantize, fine-tune, RAG และวัดผล | [AI lab](docs/starter-packs.md#ai-lab) |
| Agent / Context | ออกแบบ memory, context, tools และจุดให้คนตัดสินใจ | [Agent builder](docs/starter-packs.md#agent-builder) |
| AI Security | ตรวจ prompt injection, MCP และสิทธิ์ของ Agent | [Agent defense](docs/starter-packs.md#agent-defense) |
| Cyber | รีวิวโค้ด, dependency, CI และกฎตรวจจับ | [AppSec](docs/starter-packs.md#appsec) |
| Reverse / DFIR | วิเคราะห์ binary, protocol และ memory image | [Reverse & DFIR](docs/starter-packs.md#reverse-and-dfir) |
| Engineering | Debug, Postgres, ทดสอบหน้าเว็บ และออกแบบ UI | [รายการทั้งหมด](CATALOG.md#engineering) |

## คู่มือที่เขียนขึ้นสำหรับคลังนี้

| Playbook | ผลลัพธ์ที่ต้องการ |
| --- | --- |
| [ตรวจ Agent extension ก่อนใช้](playbooks/review-agent-extension.md) | รายงานสิทธิ์ การส่งข้อมูล hooks และประเด็นที่ยังพิสูจน์ไม่ได้ |
| [รีวิว diff พร้อมหลักฐาน](playbooks/review-diff-with-evidence.md) | Finding ที่อ้างไฟล์ เงื่อนไขเกิดปัญหา และวิธีตรวจซ้ำได้ |
| [เปรียบเทียบโมเดลอย่างเป็นธรรม](playbooks/compare-models.md) | ตารางคุณภาพ ความเร็ว ต้นทุน และข้อจำกัดภายใต้เงื่อนไขเดียวกัน |

เปิดไฟล์แล้วส่งให้ Agent อ่านเป็นบริบทของงานได้ แต่คู่มือเหล่านี้ยังไม่ใช่ตัวติดตั้งสกิลอัตโนมัติ ตัวอย่างเป็นสถานการณ์จำลอง ไม่ใช่ผล benchmark หรือการรับรองความปลอดภัย

## ค้นหารายการบนเครื่อง

ใช้ Python standard library ไม่ติดตั้ง dependency และไม่ส่งข้อมูลออกจากเครื่อง

```bash
git clone https://github.com/Sandworm-Lazarus/sandworm-arsenal.git
cd sandworm-arsenal
python3 scripts/arsenal.py search "RAG"
python3 scripts/arsenal.py search "สิทธิ์" --category "AI Security"
python3 scripts/arsenal.py check
```

Windows ใช้ `py -3` แทน `python3` ได้ หรือเปิด [CATALOG.md](CATALOG.md) เพื่ออ่านบน GitHub โดยตรง

## ใช้งานให้ตรงโจทย์

- [12 ชุดเริ่มต้น](docs/starter-packs.md): AI lab, RAG, MLOps, Agent, AppSec, Cloud, auth, CI, fuzzing และเกมเซิร์ฟเวอร์
- [ตารางเลือกตามงาน](docs/decision-guide.md): เริ่มตรงไหน ใช้ skill หรือเครื่องมืออะไร และควรได้หลักฐานแบบใด
- [เครื่องมือประกอบ 61 ตัว](TOOLS.md): ประเมิน AI, ตรวจโค้ด, secrets, SBOM, container และ CI
- [แม่แบบรายงาน 5 แบบ](templates/README.md): finding, threat model, model evaluation, extension review และ detection rule
- [ข้อควรรู้ของต้นทาง](docs/watchlist.md): การย้าย repo, license และเงื่อนไขเฉพาะแพลตฟอร์ม

## ตรวจถึงระดับไหน

| ระดับ | จำนวน | ขอบเขต |
| --- | ---: | --- |
| Entry-reviewed | 57 | อ่าน entry และไฟล์ประกอบบางส่วนในรอบรีเสิร์ชแรก |
| Entry-overview | 103 | ตรวจตัวตนไฟล์ frontmatter และเนื้อหาช่วงต้น ยังไม่ได้อ่านครบทั้ง bundle |
| Companion tools | 61 | ตรวจภาพรวม README/source และหลักฐาน license |

ยังไม่ได้รันสกิลหรือเครื่องมือต้นทางจริง ดู [รายงาน coverage](docs/review-status.md) และ [วิธีคัดและตรวจ](docs/methodology.md) ได้ ทุก entry มีลิงก์ที่ตรึง commit และบันทึกระดับที่ตรวจไว้

ตั้ง workflow ให้ตรวจ catalog และ CLI เมื่อ push หรือเปิด pull request แล้ว ดูสถานะการรันจริงได้ใน Actions รอบนี้ตรวจในสภาพแวดล้อม local ผ่าน catalog checks และ 11 tests ส่วนคำสั่ง `check` รันแบบออฟไลน์ได้

```bash
python3 scripts/arsenal.py search "MCP" --review entry-reviewed
python3 scripts/arsenal.py search "" --repo cloudflare/skills --json
python3 scripts/arsenal.py show 1
python3 scripts/arsenal.py stats
```

## เครดิตและการต่อยอด

งานเขียนและโค้ดที่สร้างขึ้นสำหรับ repository นี้ใช้ [MIT License](LICENSE) ส่วนผลงานต้นทางใช้ license ของเจ้าของแต่ละแห่ง เช่น Trail of Bits ใช้ CC BY-SA และมีบางแพ็กที่ขอบเขตสิทธิ์ยังต้องตรวจเพิ่ม ดู [SOURCES.md](SOURCES.md) และ [แนวทางให้เครดิต](docs/attribution.md) ก่อนนำเนื้อหาต้นทางมาดัดแปลง

อยากเพิ่มสกิลหรือแก้ข้อมูล ส่ง pull request พร้อมต้นทางและหลักฐานตาม [แนวทางร่วมพัฒนา](CONTRIBUTING.md) ได้

คลังส่วนตัวอิสระ ไม่ได้สังกัดองค์กรที่อ้างถึง
