# Configuration Example

Use this reference when setting up `feishu-knowledge-capture` for one person or for a team.

Do not commit private Feishu target URLs or tokens to a public repository. Prefer environment variables, a local untracked config file, or an automation prompt.

## Team Mode

Use team mode when multiple teammates should all write candidate knowledge into the same review pool.

Required target values:

```text
FEISHU_KNOWLEDGE_MODE=team
FEISHU_KNOWLEDGE_CANDIDATE_NODE_TOKEN=<待审核 wiki node token>
FEISHU_KNOWLEDGE_CANDIDATE_NODE_URL=<待审核 wiki url>
FEISHU_KNOWLEDGE_INDEX_DOC_TOKEN=<支持知识碎片候选池 docx token>
FEISHU_KNOWLEDGE_INDEX_DOC_URL=<支持知识碎片候选池 url>
```

Optional values:

```text
FEISHU_KNOWLEDGE_DEFAULT_TIMEZONE=Asia/Shanghai
FEISHU_KNOWLEDGE_SOURCE_PATTERNS=/support-triage,JSWO-
FEISHU_KNOWLEDGE_OWNER_FIELD=sender_name
```

With the current shared pool, the values are:

```text
FEISHU_KNOWLEDGE_CANDIDATE_NODE_TOKEN=QiPGwE9Y4iukxfkMh8YcXPKNnBd
FEISHU_KNOWLEDGE_CANDIDATE_NODE_URL=https://www.feishu.cn/wiki/QiPGwE9Y4iukxfkMh8YcXPKNnBd
FEISHU_KNOWLEDGE_INDEX_DOC_TOKEN=Xaf8dtkaboAsQ3xHzBtc1WD6n3e
FEISHU_KNOWLEDGE_INDEX_DOC_URL=https://www.feishu.cn/wiki/SarowXaTji5farkayOBcbYfqn2d
```

Only use these shared-pool values when the user explicitly wants all teammates to write into the same candidate pool and the current Feishu identity has write permission.

## Personal Mode

Use personal mode when each teammate keeps a private candidate pool.

```text
FEISHU_KNOWLEDGE_MODE=personal
FEISHU_KNOWLEDGE_CANDIDATE_NODE_TOKEN=<their own 待审核 node token>
FEISHU_KNOWLEDGE_INDEX_DOC_TOKEN=<their own index docx token>
```

## Source Discovery

For support-triage topic groups, resolve the source chat by configured chat name or chat ID.

For work-order groups, search visible chats by ticket pattern and parse names with `scripts/parse_work_order_group.py`.

Examples:

```powershell
lark-cli.cmd im +chat-search --query "JSWO-" --format json
python feishu-knowledge-capture\scripts\parse_work_order_group.py "【新问题_进行中】PUDU T300法国JSWO-202604220005"
```

If a teammate asks:

```text
@Pierre的飞书智能体 /飞书知识沉淀 获取今天我所有工单群内容并沉淀
```

Use these defaults:

- `owner`: Pierre or the invoking Feishu user.
- `time_window`: today from 00:00 to now in Asia/Shanghai.
- `source_scope`: visible groups containing `JSWO-` plus configured support-triage topic groups.
- `target`: team candidate node and shared index when `FEISHU_KNOWLEDGE_MODE=team`.

## Permission Requirements

The identity running the bot or automation must have:

- Read access to the source work-order groups.
- `im:chat:read` and message read/search scopes as needed.
- Write permission to the target candidate Wiki node.
- Write permission to the shared index document.

If the teammate can read their work-order groups but cannot write to the shared pool, ask the pool owner to grant edit permission to the teammate or to the bot.
