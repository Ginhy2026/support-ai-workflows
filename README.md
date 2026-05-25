# support-ai-workflows

Shared Hermes/Codex skills and workflows for AI-assisted technical support.

## Included Skills

### support-triage

`support-triage` helps overseas robot support teams process customer issues from WhatsApp, Feishu email, and Feishu messages. It supports first-pass triage, Feishu knowledge-base search guidance, supplemental SOP/Yuque/Feishu/web reference handling, source applicability judgment, customer reply drafts, internal escalation notes, and handoff decisions for FAQ/SOP capture.

Skill folder:

```text
support-triage/
```

### case-capture

`case-capture` converts customer issues, Feishu knowledge-base answers, internal discussions, troubleshooting notes, and final solutions into candidate FAQ or SOP drafts. It labels information confidence and whether the content is suitable for a formal knowledge base.

Skill folder:

```text
case-capture/
```

### feishu-cli-setup

`feishu-cli-setup` checks and guides local `lark-cli` readiness for Feishu document and wiki search. It verifies CLI installation, Feishu user login, token validity, `search:docs:read`, and a test search.

Skill folder:

```text
feishu-cli-setup/
```

### feishu-knowledge-capture

`feishu-knowledge-capture` collects support-triage Feishu topic threads and, when enabled, JSWO work-order group discussions or manually requested Feishu chat scopes into candidate Feishu Wiki knowledge drafts. It writes one candidate FAQ/fault/SOP page per reusable case, appends an entry to a shared index document such as `支持知识碎片候选池`, and can archive Markdown snapshots to GitHub for version history.

First-version scope:

- Read only support-triage related topic threads.
- Treat one topic thread as one case.
- Write only candidate drafts under a Feishu Wiki review area such as `候选知识碎片/待审核`.
- Never publish content as formal knowledge without human review.

Future company-wide scope:

- Recognize work-order group names containing ticket IDs such as `JSWO-202604220005`.
- Parse group names like `【新问题_进行中】PUDU T300法国JSWO-202604220005`.
- Use message content, not only group status text, to decide whether a case is closed enough for candidate knowledge.
- Support manual scopes such as all JSWO work-order groups, all visible group chats, all private chats, or a named chat with filtering and redaction safeguards.
- Store candidate Markdown versions under `knowledge-archive/` for GitHub-based diff and recovery.
- Dedupe multi-user runs in the same work-order group by `workorder:<JSWO-id>` and record roles separately: technical support owner, department leader, product/service representative, trigger person, contributors, and last updater.

Skill folder:

```text
feishu-knowledge-capture/
```

## Install

Copy the `support-triage` folder into your Hermes/Codex skills directory.

Typical Codex location:

```text
%USERPROFILE%\.codex\skills\support-triage
```

Then invoke it with:

```text
Use $support-triage to triage this customer robot issue.
```

For case capture:

```text
Use $case-capture to convert this resolved support case into a candidate FAQ or SOP draft.
```

For Feishu CLI setup:

```text
Use $feishu-cli-setup to check lark-cli, Feishu login, search permission, and document search readiness.
```

For Feishu knowledge capture:

```text
Use $feishu-knowledge-capture to collect today's support-triage threads and write candidate knowledge drafts to Feishu Wiki.
```

Manual Feishu knowledge capture examples:

```text
Use $feishu-knowledge-capture to collect today's JSWO work-order groups and archive candidate drafts.
Use $feishu-knowledge-capture to collect yesterday's technical-support discussions from all visible group chats.
Use $feishu-knowledge-capture to run a leader pilot on one JSWO group and record support owner, leader, and service representative roles.
```

Chinese example:

```text
请使用 $support-triage 处理下面这个客户机器人问题。
```

---

### knowledge — Knowledge Pipeline Skills

This suite of 7 skills forms a complete knowledge management pipeline: ingest → digest → output → push to GitHub. They work with an Obsidian vault at `$HOME/Espace_Obsidian`.

Invocation in Hermes (Feishu/Telegram): `/<skill-name>` (e.g. `/web-in`)

#### Skill Overview

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| **web-in** | Ingest web pages | URL | Raw article + summary + concept pages in vault |
| **paper-in** | Ingest academic papers | arXiv URL/ID | Raw paper + summary + concept pages in vault |
| **media-in** | Ingest video/audio content | Video/audio URL + description | Raw transcript or text summary in vault |
| **digest** | Digest unsorted raw materials | None (scans vault) | Summary + concept pages for all unprocessed entries |
| **feynman** | Generate teaching output | None (scans vault) | Feynman-style teaching notes in `输出/教学/` |
| **output** | Generate review/retrospective reports | None (scans vault) | Review reports in `输出/回顾/` |
| **pipeline** | Full end-to-end run | None | Digest → feynman → output → Health report → GitHub push |

#### File Structure in Vault

```
$HOME/Espace_Obsidian/
├── 原始材料/
│   ├── 文章/        ← web-in, paper-in write here
│   └── 视频/        ← media-in write here
├── 知识库/
│   ├── 摘要/        ← Summaries of ingested content
│   ├── 概念/        ← Concept pages (linked from summaries)
│   └── 索引.md      ← Central index, updated after every ingest
├── 输出/
│   ├── 教学/        ← feynman writes here
│   └── 回顾/        ← output writes here
└── README.md
```

#### Data Flow

```
External source (web/paper/media)
    │
    ▼
[web-in / paper-in / media-in]  ──►  raw material + summary + concept pages
    │
    ▼
[digest]  ──►  process backlog, fill missing summaries/concepts
    │
    ▼
[feynman / output]  ──►  generate teaching notes & review reports
    │
    ▼
[pipeline]  ──►  entire chain + health report + git commit & push to GitHub
```

#### Cron Automation

A scheduled cron job (`job_id: dc8e06cd9a7e`) runs `pipeline` every Sunday at 09:00, which automatically:
1. Scans all raw materials for unprocessed items
2. Fills in missing summaries and concept pages
3. Generates Feynman teaching notes
4. Creates a health report
5. Commits and pushes everything to `github.com/Ginhy2026/Espace_Obsidian`

#### For Codex: How to Read & Modify These Skills

Each skill is a standalone `.md` file in `skills/knowledge/`:
- YAML frontmatter: metadata (name, description, version)
- Body: trigger conditions, execution steps, file paths, format templates, verification checklist

To create a new skill (e.g., a Feishu knowledge capture skill):
1. Design the execution flow (what triggers it, what it reads, what it writes)
2. Define file paths and format templates in the vault
3. Include verification steps and anti-footgun rules (like "no skill_manage")
4. Add the skill to `~/.hermes/skills/knowledge/` as a SKILL.md

---

### case-capture

If you invoke it without case details, Hermes should return a compact intake form first:

```text
/support-triage
```

## Recommended Workflow

1. Paste the customer message and case background into Hermes.
2. Run `$support-triage` without Feishu knowledge-base results for first-pass triage.
3. Let the skill generate multiple Feishu search queries by model, module, symptom, error code, customer phrase, and Chinese synonyms.
4. Paste Feishu answers or supplemental SOP/Yuque/Feishu/web references back into Hermes.
5. If Feishu CLI search is not ready, run `$feishu-cli-setup` or manually search Feishu with the generated queries.
6. Run `$support-triage` again to judge source applicability, produce executable troubleshooting steps, draft the customer reply, and decide whether to hand off to `$case-capture`.

## Repository Layout

```text
.
├── README.md
├── case-capture/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── examples.md
│       ├── input-template.md
│       └── output-templates.md
├── feishu-cli-setup/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── checklist.md
│       ├── commands.md
│       └── troubleshooting.md
├── feishu-knowledge-capture/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── references/
│   │   ├── config.example.md
│   │   ├── lark-workflow.md
│   │   ├── review-rules.md
│   │   └── templates.md
│   └── scripts/
│       ├── archive_snapshot.py
│       ├── candidate_key.py
│       └── parse_work_order_group.py
├── knowledge-archive/          ← generated candidate Markdown versions when archive output is enabled
├── skills/
│   └── knowledge/
│       ├── web-in.md
│       ├── paper-in.md
│       ├── media-in.md
│       ├── digest.md
│       ├── feynman.md
│       ├── output.md
│       └── pipeline.md
└── support-triage/
    ├── SKILL.md
    ├── README.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── main-prompt.md
        ├── input-template.md
        ├── output-templates.md
        └── examples.md
```
