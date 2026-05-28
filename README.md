# support-ai-workflows

Shared Hermes/Codex skills and workflows for AI-assisted technical support.

## Included Skills

### SupportMan (`supportman`)

`SupportMan` is the v2 of `support-triage` and the daily technical-support work assistant. It helps overseas support teams process WhatsApp screenshots, Feishu screenshots, Feishu email/messages, pasted customer conversations, pre-sales questions, Spark-plan/星火计划 requests, internal follow-ups, and robot troubleshooting cases. It supports first-pass handling, Feishu knowledge-base search guidance, supplemental SOP/Yuque/Feishu/web reference handling, source applicability judgment, customer reply drafts, internal notes, next actions, escalation notes, and knowledge-capture-worthiness decisions. It is independent from `feishu-knowledge-capture`; that separate skill is only an optional next step when the user explicitly wants to create candidate knowledge.

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

`feishu-knowledge-capture` is an independent knowledge-capture skill. It can turn single support cases, JSWO work-order groups, manually requested Feishu chat scopes, or pasted summaries from other workflows into candidate Feishu Wiki knowledge drafts. It writes candidate FAQ/fault/SOP/Pending entries, appends an entry to a shared index document such as `支持知识碎片候选池`, labels maturity (`M0`-`M4`), and can archive Markdown snapshots to GitHub for version history.

Core scope:

- Capture one pasted case or case summary when explicitly invoked.
- Batch-read configured support-related topic threads when explicitly invoked.
- Treat one topic thread or one work order as one case.
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

Usage doc:

```text
docs/feishu-knowledge-capture-usage.md
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
Use $feishu-knowledge-capture to collect today's configured support threads and write candidate knowledge drafts to Feishu Wiki.
Use $feishu-knowledge-capture to turn this closed case summary and final solution into a candidate fault/FAQ/SOP/Pending entry.
```

`SupportMan` and `feishu-knowledge-capture` are maintained as separate skills. If another skill already produced a useful case summary, pass that summary in as source material; `feishu-knowledge-capture` should still apply its own Feishu candidate review, dedupe, and archive rules.

Manual Feishu knowledge capture examples:

```text
Use $feishu-knowledge-capture to collect today's JSWO work-order groups and archive candidate drafts.
Use $feishu-knowledge-capture to collect yesterday's technical-support discussions from all visible group chats.
Use $feishu-knowledge-capture to run a leader pilot on one JSWO group and record support owner, leader, and service representative roles.
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
2. Run `$supportman` without Feishu knowledge-base results for first-pass handling.
3. Let the skill generate multiple Feishu search queries by model, module, symptom, error code, customer phrase, and Chinese synonyms.
4. Paste Feishu answers or supplemental SOP/Yuque/Feishu/web references back into Hermes.
5. If Feishu CLI search is not ready, run `$feishu-cli-setup` or manually search Feishu with the generated queries.
6. Run `$supportman` again to judge source applicability, produce executable troubleshooting steps, draft the customer reply, and decide whether the material has later knowledge-capture value.
7. When the case is closed or worth tracking and the user explicitly wants to write candidate knowledge, run the independent `$feishu-knowledge-capture` skill in single-case or batch mode.

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
