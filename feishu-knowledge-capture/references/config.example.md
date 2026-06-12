# Configuration Example

Use this reference when setting up `feishu-knowledge-capture` for personal knowledge capture.

Do not commit private Feishu URLs or tokens to a public repository. Prefer environment variables, a local untracked config file, or an automation prompt.

## Default Personal Mode

Personal mode is the default. It writes case notes to a personal document group or Wiki parent and optionally updates one lightweight personal index.

Required target values:

```text
FEISHU_KNOWLEDGE_MODE=personal
FEISHU_KNOWLEDGE_PERSONAL_PARENT_TOKEN=<个人沉淀文档组或 Wiki 父节点 token>
FEISHU_KNOWLEDGE_PERSONAL_PARENT_URL=<个人沉淀文档组或 Wiki 父节点 url>
```

Optional values:

```text
FEISHU_KNOWLEDGE_PERSONAL_INDEX_DOC_TOKEN=<个人索引清单文档 token>
FEISHU_KNOWLEDGE_PERSONAL_INDEX_DOC_URL=<个人索引清单文档 url>
FEISHU_KNOWLEDGE_DEFAULT_TIMEZONE=Asia/Shanghai
FEISHU_KNOWLEDGE_SOURCE_PATTERNS=JSWO-,故障,报错,异常,排查,解决,FAQ,SOP
FEISHU_KNOWLEDGE_ARCHIVE_ROOT=knowledge-archive
FEISHU_KNOWLEDGE_DEFAULT_TIME_WINDOW=today
FEISHU_KNOWLEDGE_MANUAL_SCOPES=single-case,named-chat,selected-chats,visible-workorder-groups
```

Optional second-brain handoff values:

```text
FEISHU_SECOND_BRAIN_INTAKE_REPO=<dedicated intake repository; never the Obsidian source or AI publication repository>
FEISHU_SECOND_BRAIN_INTAKE_ROOT=knowledge-intake/feishu
```

If `FEISHU_SECOND_BRAIN_INTAKE_REPO` is missing or cannot be verified as a dedicated intake repository, return a dry-run candidate instead of writing to GitHub.

## Personal Index Fields

The personal index is a lightweight list, not a control console. Use exactly these fields:

```text
关键词, 类型, 模块, 标题, 来源, 文档链接, 状态
```

Recommended status values:

```text
待整理, 已沉淀, 需补充, 可复用, 已废弃
```

## Source Discovery

For named chats, resolve the source chat by configured chat name or chat ID:

```powershell
lark-cli.cmd im +chat-search --query "PUDU T300法国JSWO-202604220005" --format json
```

For work-order groups, search visible chats by ticket pattern and parse names with `scripts/parse_work_order_group.py`:

```powershell
lark-cli.cmd im +chat-search --query "JSWO-" --format json
python feishu-knowledge-capture\scripts\parse_work_order_group.py "【新问题_进行中】PUDU T300法国JSWO-202604220005"
```

Only process chats visible to the current identity. Do not imply access to company-wide or other people's private chats.

## Automation and Manual Runs

Manual runs should usually specify the source:

```text
source_scope=single-case
source_scope=named-chat:<chat name>
source_scope=selected-chats:<chat A>,<chat B>
source_scope=visible-workorder-groups
```

Time window rules:

```text
time_window=today
time_window=yesterday
time_window=this-week
time_window=2026-05-21
time_window=2026-05-21T00:00:00+08:00..2026-05-21T18:00:00+08:00
```

If the user omits the time window, use today in `Asia/Shanghai`.

## Optional Advanced Team Setup

Team or shared targets may be configured later, but they are not the default mode for this skill. When using a shared target, keep the same document-quality rules and do not turn the personal index into a large review console.

Example optional values:

```text
FEISHU_KNOWLEDGE_MODE=team
FEISHU_KNOWLEDGE_TEAM_PARENT_TOKEN=<team review parent token>
FEISHU_KNOWLEDGE_TEAM_INDEX_DOC_TOKEN=<team lightweight index token>
```

Only use team mode when the user explicitly asks for a shared target and the current identity has write permission.

## GitHub Archive

Use GitHub Markdown archive snapshots only for generated case notes and minimal metadata. Do not store raw full chat transcripts.

The optional `knowledge-archive/` is an audit snapshot, not formal Obsidian knowledge. The optional `knowledge-intake/feishu/` is a candidate handoff queue. Neither may point to or modify the Obsidian source repository.

## Permission Requirements

The identity running the bot or automation must have:

- Read access to the selected source chats or work-order groups.
- Message read/search scopes as needed.
- Write permission to the personal document group or Wiki parent.
- Write permission to the optional personal index document.
- GitHub push or repository write permission when Markdown archive snapshots are enabled.
