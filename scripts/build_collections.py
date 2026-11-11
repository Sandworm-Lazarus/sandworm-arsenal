import argparse
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

HUB=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Generate focused collections into a separate review directory.')
parser.add_argument('--output-root', type=Path, default=HUB.parent/'generated-collections')
args=parser.parse_args()
OUT=args.output_root.resolve()
data=json.loads((HUB/'catalog/arsenal.json').read_text())
checkout_revision='11d5960a326750d5838078e36cf38b85af677262'
privacy_collections={'sandworm-cyber-arsenal','sandworm-dev-playbooks'}
privacy_files=('scripts/privacy_guard.py','tests/test_privacy_guard.py','docs/privacy-guard.md','examples/privacy-fixtures.json')
privacy_report_files=('scripts/check_privacy_fixtures.py','examples/privacy-guard-results.json')
privacy_extra_files=('examples/privacy-input.json','docs/development-notes/2026-11-11-original-tools.md')

def optional_bundle(paths, trigger_paths=None):
    """Allow an absent bundle during assembly, but never publish a partial one."""
    present=[(HUB/path).is_file() for path in paths]
    triggered=any((HUB/path).exists() for path in (trigger_paths or paths))
    if triggered and not all(present):
        missing=', '.join(path for path,exists in zip(paths,present) if not exists)
        raise SystemExit(f'Incomplete optional bundle; missing: {missing}')
    return all(present)

has_privacy_guard=optional_bundle(privacy_files,privacy_files[:3])
has_privacy_report=optional_bundle(privacy_report_files)
if has_privacy_report and not has_privacy_guard:
    raise SystemExit('The privacy fixture report requires the complete privacy guard bundle.')

def validation_workflow(include_privacy=False, include_report=False):
    workflow=f'''name: Validate collection

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  catalog:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Check out collection
        uses: actions/checkout@{checkout_revision} # v4, reviewed 2026-11-11
        with:
          persist-credentials: false
      - name: Validate catalog and generated documents
        run: python3 scripts/arsenal.py check
'''
    if include_privacy:
        workflow+='''      - name: Run original privacy guard tests
        run: python3 -m unittest discover -s tests -p 'test_privacy_guard.py' -v
'''
    if include_report:
        workflow+='''      - name: Verify synthetic privacy fixture report
        run: python3 scripts/check_privacy_fixtures.py --check-report examples/privacy-guard-results.json
'''
    return workflow

toolbox_groups={'Personal agents','Agent frameworks','Visual workflows','Local inference','Chat workspaces','Agent memory','Browser automation','Document ingestion','RAG & vector search','Voice & audio','Image workflows','Coding agents','Training & fine-tuning','Observability','Model gateways','MCP development','AI application SDKs','Privacy & data handling'}
new_evals={'confident-ai/deepeval','vibrantlabsai/ragas'}
security_groups={'Skill review','Secrets','Containers / IaC','Supply chain','CI security','Code analysis','MCP development','Privacy & data handling'}
security_evals={'NVIDIA/SkillEvaluator','microsoft/PyRIT','NVIDIA/garak','promptfoo/promptfoo','UKGovernmentBEIS/inspect_ai'}
cyber_tools={t['repo'] for t in data['tools'] if t['group'] in security_groups or t['repo'] in security_evals}
ai_tools={t['repo'] for t in data['tools'] if t['group'] in toolbox_groups or t['repo'] in new_evals}
specs=[
dict(name='sandworm-ai-toolbox',title='AI Toolbox',categories=[],groups=None,tool_repos=ai_tools,color='#d5ee8c',tagline='AGENTS / MODELS / VOICE / AUTOMATION',
     about='A directory of practical AI tools and frameworks, from personal agents and local inference to voice, documents, coding, and observability.',
     thai='คลังเครื่องมือ AI สำหรับเลือกและเปรียบเทียบตามงาน ตั้งแต่ Agent, local models, voice, browser, เอกสาร ไปจนถึง model operations',
     paths=[('Build a personal assistant',['Personal agents','Agent memory']),('Run models',['Local inference','Model gateways']),('Use documents and the web',['Document ingestion','Browser automation','RAG & vector search']),('Create voice or visual workflows',['Voice & audio','Image workflows'])]),
dict(name='sandworm-agent-skills',title='Agent Skills',categories=['Agent / Context'],groups={'Personal agents','Agent frameworks','Agent memory','Browser automation','Voice & audio','MCP development','AI application SDKs'},color='#baa4ed',tagline='CONTEXT / MEMORY / TOOLS / WORKFLOWS',
     about='Focused agent workflows for context, memory, tool design, orchestration, browser use, and voice interfaces.',
     thai='ชุดสกิลและเครื่องมือสำหรับออกแบบ Agent: context, memory, tools, orchestration, browser และช่องทางเสียง',
     paths=[('Design the agent',['Agent frameworks']),('Preserve useful context',['Agent memory']),('Choose a personal harness',['Personal agents']),('Connect browser or voice',['Browser automation','Voice & audio']),('Inspect MCP and TypeScript apps',['MCP development','AI application SDKs'])]),
dict(name='sandworm-cyber-arsenal',title='Cyber Arsenal',categories=['Cyber','AI Security','Reverse / DFIR'],groups=None,tool_repos=cyber_tools,color='#ed9876',tagline='APPSEC / AI SECURITY / DFIR / SUPPLY CHAIN',
     about='A focused security collection covering AppSec, agent and MCP security, reverse engineering, DFIR, detection, and supply-chain review.',
     thai='คลัง Cyber ที่รวม AppSec, AI/MCP security, reverse engineering, DFIR, detection และ supply-chain review',
     paths=[('Review code',['Code analysis']),('Review agents and MCP',['Skill review','AI evaluation']),('Inspect supply chain',['Supply chain','Secrets']),('Review CI and infrastructure',['CI security','Containers / IaC']),('Inspect MCP and privacy',['MCP development','Privacy & data handling'])]),
dict(name='sandworm-llm-lab',title='LLM Lab',categories=['AI Engineering'],groups={'Local inference','RAG & vector search','Training & fine-tuning','Observability','Model gateways','AI application SDKs'},extra_tools=new_evals,color='#87d4d4',tagline='INFERENCE / RAG / EVALUATION / TRAINING',
     about='A practical LLM engineering lab: model serving, quantization, RAG, evaluation, training, and experiment observability.',
     thai='ห้องทดลอง LLM สำหรับ serving, quantization, RAG, evaluation, fine-tuning และติดตามผลการทดลอง',
     paths=[('Choose a serving runtime',['Local inference']),('Build retrieval',['RAG & vector search']),('Evaluate and observe',['AI evaluation','Observability']),('Train and route models',['Training & fine-tuning','Model gateways']),('Integrate an application',['AI application SDKs'])]),
dict(name='sandworm-dev-playbooks',title='Dev Playbooks',categories=['Engineering','Cloud / DevOps','Web / Frontend'],groups={'Visual workflows','Chat workspaces','Document ingestion','Image workflows','Coding agents','API testing','AI application SDKs'},color='#edca7c',tagline='DEBUGGING / CLOUD / WEB / EVIDENCE',
     about='Developer workflows for debugging, cloud, frontend, coding agents, and evidence-backed reviews, with original playbooks and report templates.',
     thai='คู่มือทำงานสำหรับนักพัฒนา: debugging, cloud, frontend, coding agents พร้อม playbook และแม่แบบรายงานที่เขียนขึ้นเอง',
     paths=[('Work on a codebase',['Coding agents']),('Build repeatable workflows',['Visual workflows']),('Prepare technical context',['Document ingestion','Chat workspaces']),('Explore creative workflows',['Image workflows']),('Test APIs and AI endpoints',['API testing','AI application SDKs'])]),
]

script=(HUB/'scripts/arsenal.py').read_text()
script=script.replace('See the [AI toolbox guide](docs/ai-toolbox.md) for task-oriented combinations.','See [start here](docs/start-here.md) for task-oriented selections.')

summary=[]
for spec in specs:
    root=OUT/spec['name']
    for d in ('assets','catalog','scripts','docs','.github/workflows'):(root/d).mkdir(parents=True,exist_ok=True)
    include_privacy=has_privacy_guard and spec['name'] in privacy_collections
    include_report=has_privacy_report and include_privacy
    privacy_extras=tuple(path for path in privacy_extra_files if include_privacy and (HUB/path).is_file())
    for filename in (privacy_files if include_privacy else ())+(privacy_report_files if include_report else ())+privacy_extras:
        destination=root/filename
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(HUB/filename,destination)
    (root/'.github/workflows/validate.yml').write_text(validation_workflow(include_privacy,include_report))
    subset=copy.deepcopy(data)
    subset['skills']=[s for s in subset['skills'] if s['category'] in spec['categories']]
    if spec.get('groups') is None:
        subset['tools']=[t for t in subset['tools'] if t['repo'] in spec['tool_repos']]
    else:
        subset['tools']=[t for t in subset['tools'] if t['group'] in spec['groups'] or t['repo'] in spec.get('extra_tools',set())]
    repos={s['repo'] for s in subset['skills']}|{t['repo'] for t in subset['tools']}
    subset['sources']=[s for s in subset['sources'] if s['repo'] in repos]
    subset['evidence']=[e for e in subset['evidence'] if e['repo'] in repos]
    subset['snapshot']=data['snapshot']+'-'+spec['name']
    subset['scope']=f"Focused collection: {len(subset['skills'])} skill entries and {len(subset['tools'])} tools. Original review levels retained. No upstream runtime testing."
    subset['collection']={'name':spec['name'],'hub':'https://github.com/Sandworm-Lazarus/sandworm-arsenal','source_snapshot':data['snapshot']}
    (root/'catalog/arsenal.json').write_text(json.dumps(subset,ensure_ascii=False,indent=2)+'\n')
    (root/'scripts/arsenal.py').write_text(script)
    for filename in ('LICENSE','.gitignore'):shutil.copyfile(HUB/filename,root/filename)
    title=spec['title'].upper()
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280" role="img" aria-labelledby="title desc">
<title id="title">Sandworm {spec['title']}</title><desc id="desc">{spec['about']}</desc>
<rect width="1200" height="280" rx="20" fill="#121b21"/>
<path d="M850 0v280M920 0v280M990 0v280M1060 0v280M1130 0v280M815 70h385M815 140h385M815 210h385" stroke="#29363c"/>
<rect x="48" y="42" width="7" height="20" rx="3" fill="{spec['color']}"/>
<text x="72" y="59" fill="{spec['color']}" font-family="monospace" font-size="17" letter-spacing="3">SANDWORM COLLECTIONS</text>
<text x="46" y="151" fill="#f3f1e7" font-family="Arial,sans-serif" font-size="65" font-weight="700" letter-spacing="-2">{title}</text>
<text x="49" y="211" fill="{spec['color']}" font-family="Arial,sans-serif" font-size="20">{spec['tagline']}</text>
<circle cx="1060" cy="140" r="58" fill="none" stroke="{spec['color']}" stroke-width="19"/>
<circle cx="1060" cy="140" r="18" fill="{spec['color']}"/>
</svg>'''
    (root/'assets/banner.svg').write_text(svg)
    has_skills=bool(subset['skills'])
    nav=('[Skills](CATALOG.md) · ' if has_skills else '')+'[Tools](TOOLS.md) · [Start here](docs/start-here.md) · [Sources](SOURCES.md)'
    commands=['python3 scripts/arsenal.py tools "" --json','python3 scripts/arsenal.py stats','python3 scripts/arsenal.py check']
    if has_skills:commands.insert(0,'python3 scripts/arsenal.py search "" --json')
    collection_metrics=(f"{len(subset['skills'])} skill entries · {len(subset['tools'])} tools · {len(subset['sources'])} source repositories" if has_skills else f"{len(subset['tools'])} AI tools · {len({t['group'] for t in subset['tools']})} categories · {len(subset['sources'])} source repositories")
    shared=f'''<p align="center"><img src="assets/banner.svg" alt="Sandworm {spec['title']}" width="100%"></p>

<p align="center"><b>{collection_metrics}</b></p>

'''
    readme=shared+f'''# Sandworm {spec['title']}

{spec['about']}

{spec['thai']}

[ภาษาไทย](README.th.md) · {nav} · [Collection hub](https://github.com/Sandworm-Lazarus/sandworm-arsenal)

## What is inside

'''
    if has_skills:
        readme+='| Track | Entries |\n| --- | ---: |\n'
        for cat in spec['categories']:readme+=f"| {cat} | {sum(s['category']==cat for s in subset['skills'])} |\n"
        readme+='\n'
    readme+='| Tool category | Projects |\n| --- | ---: |\n'
    for group in dict.fromkeys(t['group'] for t in subset['tools']):
        readme+=f"| {group} | {sum(t['group']==group for t in subset['tools'])} |\n"
    readme+=f'''
## Use the collection

Browse the pinned source links and use the task paths in [Start here](docs/start-here.md). The offline CLI requires Python 3.9+ and no third-party dependencies.

```bash
git clone https://github.com/Sandworm-Lazarus/{spec['name']}.git
cd {spec['name']}
'''+ '\n'.join(commands)+'''
```

On Windows, use `py -3` if `python3` is unavailable.

## Evidence and reuse

Entry and Overview labels retain the inspection scope from the original research. Tool records are README overviews. No upstream installation, runtime certification, or benchmark result is claimed. [Review coverage](docs/review-status.md) records this collection's counts.

Original summaries, artwork, CLI and guides are [MIT licensed](LICENSE). Linked projects retain their own licenses; inspect [source/license notes](SOURCES.md) before copying or deploying external packages. This collection contains original curation and links, not upstream bundles.

## Related collections

'''
    for sibling in specs:
        if sibling['name']!=spec['name']:readme+=f"- [{sibling['title']}](https://github.com/Sandworm-Lazarus/{sibling['name']})\n"
    readme+='\nSelections overlap where tools support multiple tasks. Do not add collection counts together to infer a unique total.\n'
    if spec['name']=='sandworm-dev-playbooks':
        for folder in ('playbooks','templates'):shutil.copytree(HUB/folder,root/folder,dirs_exist_ok=True)
        readme+='\n## Original working materials\n\n- [Three original playbooks](playbooks/review-agent-extension.md) for extension review, evidence-backed diffs and model comparison.\n- [Five report templates](templates/README.md) for findings, threat models, model evals, extension reviews and detection rules.\n'
    if include_privacy:
        readme+='''
## Original utility: privacy guard

Use the local Python [privacy guard](docs/privacy-guard.md) to apply explicit field policies and text masking to synthetic text or JSON. It uses the standard library and makes no network requests. Read the documented coverage and limits before using its output.

```bash
printf '%s\\n' '{"customer_name":"Synthetic Person","message":"Email nina@example.invalid"}' | python3 scripts/privacy_guard.py json --sensitive-field customer_name
python3 -m unittest discover -s tests -p 'test_privacy_guard.py' -v
```

The [synthetic privacy fixtures](examples/privacy-fixtures.json) describe acceptance cases; they are not a Presidio or general PII-detection benchmark.
'''
        if 'docs/development-notes/2026-11-11-original-tools.md' in privacy_extras:
            readme+='\nRead the [original-tool development case study](docs/development-notes/2026-11-11-original-tools.md) for implementation decisions and verification evidence.\n'
        if include_report:
            readme+='\nReproduce the committed fixture report with `python3 scripts/check_privacy_fixtures.py --check-report examples/privacy-guard-results.json`.\n'
    if not has_skills:
        readme=readme.replace('Entry and Overview labels retain the inspection scope from the original research. Tool records are README overviews.', 'Tool records retain the README and license-overview scope from the original research.')
    (root/'README.md').write_text(readme)
    thai=shared+f'''# Sandworm {spec['title']}

{spec['thai']}

[English](README.md) · {nav} · [หน้ารวมทุกคลัง](https://github.com/Sandworm-Lazarus/sandworm-arsenal)

คลังนี้มีสกิล {len(subset['skills'])} entries และเครื่องมือ {len(subset['tools'])} ตัว พร้อมลิงก์ที่ตรึง commit และคำอธิบายการใช้งาน อ่าน [เส้นทางเริ่มต้น](docs/start-here.md) เพื่อเลือกตามโจทย์

## ค้นหาและตรวจข้อมูล

ใช้ Python 3.9+ โดยไม่ต้องติดตั้ง dependencies เพิ่ม

```bash
'''+ '\n'.join(commands)+'''
```

## ระดับการตรวจ

Entry หมายถึงเคยอ่านไฟล์ entry ในงานรีเสิร์ชต้นทาง ส่วน Overview หมายถึงตรวจ frontmatter และเนื้อหาช่วงต้น เครื่องมือเป็นการตรวจภาพรวม README ไม่ได้รันทดสอบแพ็กเกจต้นทาง ดู [coverage](docs/review-status.md) ของคลังนี้ได้

งานคัดสรรและคู่มือของเราใช้ [MIT](LICENSE) ส่วนผลงานภายนอกใช้ license ของเจ้าของตาม [SOURCES.md](SOURCES.md) การอยู่ในคลังไม่ได้แปลว่าเป็นผลงานที่เราเขียนทั้งหมด

เครื่องมือบางตัวอยู่ได้มากกว่าหนึ่งคลังตามบริบทการใช้งาน จึงไม่ควรนำจำนวนจากทุก repo มาบวกเป็นจำนวนโครงการไม่ซ้ำ
'''
    if not has_skills:
        thai=thai.replace(f"คลังนี้มีสกิล 0 entries และเครื่องมือ {len(subset['tools'])} ตัว", f"คลังนี้รวมเครื่องมือ AI {len(subset['tools'])} ตัว")
    if include_privacy:
        thai+='''
## เครื่องมือที่พัฒนาเอง: privacy guard

ใช้ [privacy guard](docs/privacy-guard.md) เพื่อใช้นโยบายปิดบัง field ที่ระบุและข้อความสังเคราะห์แบบ local ด้วย Python standard library โดยไม่มี network requests อ่านขอบเขตและข้อจำกัดในคู่มือก่อนนำผลไปใช้

```bash
printf '%s\\n' '{"customer_name":"Synthetic Person","message":"Email nina@example.invalid"}' | python3 scripts/privacy_guard.py json --sensitive-field customer_name
python3 -m unittest discover -s tests -p 'test_privacy_guard.py' -v
```

[ชุดข้อมูลสังเคราะห์](examples/privacy-fixtures.json) เป็นกรณีทดสอบตามนโยบาย ไม่ใช่ผล benchmark ของ Presidio หรือการรับรองว่าค้นพบ PII ครบ
'''
        if 'docs/development-notes/2026-11-11-original-tools.md' in privacy_extras:
            thai+='\nอ่าน [กรณีศึกษาการพัฒนาเครื่องมือของเรา](docs/development-notes/2026-11-11-original-tools.md) สำหรับเหตุผลการออกแบบและหลักฐานการตรวจสอบ\n'
    (root/'README.th.md').write_text(thai)
    start=[f"# Start here: {spec['title']}",'','[Home](../README.md) · [Tools](../TOOLS.md) · [Sources](../SOURCES.md)','','Select a task, inspect the complete pinned package, then try a bounded synthetic fixture. These are reading paths and prototype ideas, not tested integrations.','']
    for label,groups in spec['paths']:
        chosen=[t for t in subset['tools'] if t['group'] in groups][:6]
        if not chosen:continue
        start += [f'## {label}','','| Project | ใช้ทำอะไร | Evidence to collect |','| --- | --- | --- |']
        for t in chosen:
            start.append(f"| [{t['name']}]({t['url']}) | {t['purpose']} | Version, configuration, one task result, failure behavior and data/permission boundaries |")
        start+=['']
    if has_skills:
        start+=['## Skill starting points','','| Entry | Task | Review |','| --- | --- | --- |']
        for cat in spec['categories']:
            for s in [s for s in subset['skills'] if s['category']==cat][:3]:
                start.append(f"| [{s['name']}]({s['url']}) | {s['purpose']} | {s['review_level']} |")
    if spec['name'] in privacy_collections:
        (root/'examples').mkdir(exist_ok=True)
        shutil.copyfile(HUB/'examples/privacy-fixtures.json',root/'examples/privacy-fixtures.json')
        if include_privacy:
            start += ['', '## Original privacy guard', '',
                      'Run the original [local privacy utility](privacy-guard.md) against the [synthetic policy fixtures](../examples/privacy-fixtures.json). Record its documented field policy, input budgets and masking limits. These cases do not establish general PII-detection coverage or Presidio behavior.', '']
        else:
            start += ['', '## Synthetic privacy trial', '',
                      'Use the original [privacy policy fixtures](../examples/privacy-fixtures.json) to define expected masking behavior in a prototype. Include Thai text, explicit sensitive fields, benign version numbers, already masked values and empty input. These are proposed acceptance criteria; configure your own adapter and recognizers and record observed results before claiming support.', '']
    (root/'docs/start-here.md').write_text('\n'.join(start)+'\n')
    (root/'docs/methodology.md').write_text(f'''# Methodology

This focused collection derives from the `{data['snapshot']}` research snapshot in the Sandworm Arsenal hub. It contains {len(subset['skills'])} skill entries and {len(subset['tools'])} tools from {len(subset['sources'])} repositories. Stable entry IDs, pinned revisions, blob identities and scope labels are retained.

`entry-reviewed` records an entry-file read with selected supporting evidence. `entry-overview` records frontmatter and an opening excerpt. `readme-overview` records introductory tool README/license inspection. None means that every bundled file was reviewed or that external code was executed.

The local `check` validates catalog consistency, pinned-link structure, generated pages, SVG syntax and local file links. It does not contact external services, certify package behavior or reproduce benchmark claims.

Before adoption, read the complete relevant bundle, confirm dependencies, permissions, outbound data and license scope, and run a small fixture in the intended environment. Retain successes and failures with exact versions and commands.
''')
    (root/'docs/attribution.md').write_text('''# Attribution

Original curation, summaries, guides, artwork and CLI are by Sandworm-Lazarus under the repository MIT license. Linked skills and tools remain the work of their listed upstream authors. No external bundle is included or relicensed.

Read the exact source/license links in [SOURCES.md](../SOURCES.md), including per-file and enterprise scopes. Library licenses do not automatically cover model weights, datasets, plugins or hosted services. Listing does not imply affiliation or endorsement.
''')
    (root/'CONTRIBUTING.md').write_text('''# Contributing

Add sources that fit this collection's purpose. Record canonical repository, immutable revision, entry/blob identity, requirements, a concrete task and license evidence in `catalog/arsenal.json`. Keep Entry and Overview status consistent with the actual inspection; do not add runtime claims without reproducible evidence.

Regenerate and validate after edits:

```bash
python3 scripts/arsenal.py render
python3 scripts/arsenal.py check
```

Use original summaries and pinned links. Do not copy upstream bundles or include private data and credentials. Propose changes to the shared catalog/CLI in the collection hub when they affect multiple repositories.
''')
    subprocess.run([sys.executable,str(root/'scripts/arsenal.py'),'render'],check=True,capture_output=True)
    subprocess.run([sys.executable,str(root/'scripts/arsenal.py'),'check'],check=True,capture_output=True)
    # Exercise both data paths with the focused inventories.
    output=subprocess.run([sys.executable,str(root/'scripts/arsenal.py'),'tools','','--json'],check=True,capture_output=True,text=True)
    assert len(json.loads(output.stdout))==len(subset['tools'])
    if has_skills:
        output=subprocess.run([sys.executable,str(root/'scripts/arsenal.py'),'show',str(subset['skills'][0]['id'])],check=True,capture_output=True,text=True)
        assert json.loads(output.stdout)['id']==subset['skills'][0]['id']
    summary.append(dict(name=spec['name'],title=spec['title'],skills=len(subset['skills']),tools=len(subset['tools']),sources=len(subset['sources']),description=spec['about'],path=str(root)))

# Each skill has exactly one focused home; toolbox is a cross-cutting directory.
all_ids=[]
for spec in specs:
    subset=json.loads((OUT/spec['name']/'catalog/arsenal.json').read_text())
    all_ids += [s['id'] for s in subset['skills']]
assert sorted(all_ids)==sorted(s['id'] for s in data['skills'])
assert len(all_ids)==len(set(all_ids))
(OUT/'collections-manifest.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
