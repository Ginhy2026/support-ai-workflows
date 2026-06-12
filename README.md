# support-ai-workflows

Shared Hermes/Codex skills and workflows for AI-assisted technical support.

## Included Skills

### SupportMan (`supportman`)

`SupportMan` is the daily front door for technical-support work and the front-end feedback sensor for the user's second brain. It handles WhatsApp/Feishu screenshots, emails, customer conversations, pre-sales questions, projects, follow-ups, and troubleshooting. For PUDU work it coordinates relevant user-visible Feishu search with the approved `second-brain-reader`, drafts natural customer replies, and surfaces a compact feedback handoff when work reveals reusable knowledge, a correction, conflict, or knowledge gap. It never writes formal knowledge.

Skill folder:

```text
supportman/
```

### case-capture (legacy / optional)

`case-capture` is retained for compatibility as a local Markdown-only draft helper. The recommended workflow now uses `feishu-knowledge-capture` for both single-case capture and batch Feishu knowledge capture.

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

`feishu-knowledge-capture` is the user-approved capture stage. It turns SupportMan feedback handoffs, selected Feishu chats, visible work-order groups, message links, or pasted case summaries into high-quality personal case notes or pending second-brain candidates. It never handles the current support request or modifies formal knowledge.

Core scope:

- Capture one pasted case or case summary when explicitly invoked.
- Read user-selected Feishu groups or visible work-order groups when explicitly invoked.
- Treat one topic thread or one work order as one case.
- Write one personal case note per useful case under the user's personal document group or Wiki parent.
- Keep the case note complete and traceable; keep the index intentionally lightweight.
- Never publish content as formal company knowledge without human review.

Personal capture scope:

- Recognize work-order group names containing ticket IDs such as `JSWO-202604220005`.
- Parse group names such as `【新问题_进行中】PUDU T300法国JSWO-202604220005`.
- Use message content, not only group status text, to decide whether a case is ready for a reusable note.
- Support selected chats, selected work-order groups, and pasted summaries.
- Store generated case Markdown versions under `knowledge-archive/` when archive output is enabled.
- Dedupe repeated personal runs by `thread:<id>`, `workorder:<JSWO-id>`, `node:<token>`, or fallback hash.

Skill folder:

```text
feishu-knowledge-capture/
```

Usage doc:

```text
docs/feishu-knowledge-capture-usage.md
```

### second-brain-reader

`second-brain-reader` reads approved formal knowledge from a separate GitHub AI publication repository, directly or as SupportMan's personal-knowledge channel. It cites actual repository paths, warns about draft/review/stale/conflicted knowledge, states knowledge gaps, and never writes back to the publication repository or full Obsidian vault.

Skill folder:

```text
second-brain-reader/
```

## Install

Copy the `supportman` folder into your Hermes/Codex skills directory.

Typical Codex location:

```text
%USERPROFILE%\.codex\skills\supportman
```

Then invoke it with:

```text
Use $supportman to handle this customer robot issue.
```

Legacy local Markdown-only case capture:

```text
Use $case-capture only when a legacy local Markdown-only FAQ/SOP draft is needed.
```

For Feishu CLI setup:

```text
Use $feishu-cli-setup to check lark-cli, Feishu login, search permission, and document search readiness.
```

For Feishu knowledge capture:

```text
/skill install https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
/skill update https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
Use $feishu-knowledge-capture to collect today's key information from Feishu group "xxx" and create personal case notes.
Use $feishu-knowledge-capture to turn this closed case summary and final solution into a personal case note.
```

`SupportMan`, `second-brain-reader`, and `feishu-knowledge-capture` are maintained as separate skills with a small handoff contract. SupportMan handles and detects; the reader retrieves; capture preserves only after user confirmation; Codex/Obsidian reviews and publishes formal knowledge.

Manual Feishu knowledge capture examples:

```text
/飞书知识沉淀 获取今天群聊「xxx」里的关键信息并沉淀
/飞书知识沉淀 获取本周这些群聊：A、B、C，整理成个人 case 文档
使用 feishu-knowledge-capture，把下面这段案例摘要沉淀成个人 case 文档
```

Chinese example:

```text
请使用 $supportman 处理下面这个客户机器人问题。
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

### Empty SupportMan Invocation

If you invoke it without case details, Hermes should return a compact intake form first:

```text
/supportman
```

## Recommended Workflow

1. Paste the customer message and case background into Hermes.
2. Run `$supportman`; for PUDU work it should search relevant Feishu sources and query the approved second brain when available.
3. Let SupportMan distinguish formal Feishu references, second-brain paths, historical clues, customer facts, and internal hypotheses.
4. If Feishu search is not ready, run `$feishu-cli-setup` or manually use the generated queries; if second-brain retrieval is unavailable, continue without inventing a result.
5. Use the natural customer reply draft and next actions to handle the current work.
6. When SupportMan surfaces a reusable feedback handoff, confirm preservation only if it is worth keeping.
7. After confirmation, run `$feishu-knowledge-capture` to create a pending candidate; Codex/Obsidian later reviews and publishes it.

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
└── supportman/
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
