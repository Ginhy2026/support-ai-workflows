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

Do not set `FEISHU_KNOWLEDGE_CANDIDATE_NODE_TOKEN` to the root `候选知识碎片` landing page. The root page is only an entrance and should never receive generated case content. If a teammate only has the root URL, run dry-run and ask for the `待审核` child node and index document.

Optional values:

```text
FEISHU_KNOWLEDGE_DEFAULT_TIMEZONE=Asia/Shanghai
FEISHU_KNOWLEDGE_SOURCE_PATTERNS=/support-triage,JSWO-
FEISHU_KNOWLEDGE_OWNER_FIELD=sender_name
FEISHU_KNOWLEDGE_ARCHIVE_ROOT=knowledge-archive
FEISHU_KNOWLEDGE_DEFAULT_AUTOMATION_SCOPE=support-triage
FEISHU_KNOWLEDGE_MANUAL_SCOPES=single-case,support-triage,jswo-groups,all-group-chats,all-private-chats,named-chat
FEISHU_KNOWLEDGE_ROLE_MAP_FILE=<local untracked role map path>
FEISHU_KNOWLEDGE_DEFAULT_LEADER=<leader name or open_id>
```

With the current shared pool, the values are:

```text
FEISHU_KNOWLEDGE_CANDIDATE_NODE_TOKEN=QiPGwE9Y4iukxfkMh8YcXPKNnBd
FEISHU_KNOWLEDGE_CANDIDATE_NODE_URL=https://www.feishu.cn/wiki/QiPGwE9Y4iukxfkMh8YcXPKNnBd
FEISHU_KNOWLEDGE_INDEX_DOC_TOKEN=Xaf8dtkaboAsQ3xHzBtc1WD6n3e
FEISHU_KNOWLEDGE_INDEX_DOC_URL=https://www.feishu.cn/wiki/SarowXaTji5farkayOBcbYfqn2d
```

Known non-target in this pool:

```text
FEISHU_KNOWLEDGE_ROOT_NODE_TOKEN=Ukb5wsoo3ihWWUkVMwzcSV6dn4b
FEISHU_KNOWLEDGE_ROOT_NODE_URL=https://pudutech.feishu.cn/wiki/Ukb5wsoo3ihWWUkVMwzcSV6dn4b
```

The root node above is the `候选知识碎片` landing page. It is useful for navigation or maintenance-only edits, but it must not be used as the candidate write target.

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
- `output`: case-level candidate/Pending records. Do not produce a single `工单总结报告` as the knowledge artifact.

## Automation and Manual Runs

Default scheduled automation should use:

```text
source_scope=support-triage
time_window=today
output=feishu+github-archive
```

Manual runs may override the source scope:

```text
source_scope=single-case
source_scope=jswo-groups
source_scope=all-group-chats
source_scope=all-private-chats
source_scope=named-chat:<chat name>
```

For `all-group-chats` and `all-private-chats`, the runner must filter by technical-support signals before generating candidates and must redact private conversation by default.

## Role Attribution

Use role attribution to separate work-order responsibility from the person who invokes the skill.

Recommended local role map shape:

```json
{
  "leaders": ["open_id_or_name_b"],
  "service_representatives": {
    "PUDU T300": ["open_id_or_name_c"],
    "KettyBot": ["open_id_or_name_d"]
  },
  "support_owners": {
    "JSWO-202604220005": "open_id_or_name_a"
  }
}
```

Resolution priority:

1. Explicit role map or configured values.
2. Work-order metadata from the source system, if available.
3. Group membership and message behavior.
4. `待确认` when the role cannot be determined reliably.

Track the invoking user separately as `触发人`; do not treat the invoking user as the work-order owner unless the role map or evidence supports it.

## GitHub Archive

Use GitHub Markdown archive snapshots for version history. The runner should create or update files under `FEISHU_KNOWLEDGE_ARCHIVE_ROOT` and commit them with the skill/repo workflow.

Do not store raw full chat transcripts in the archive. Store only generated candidate Markdown, minimal source identifiers, Feishu document links, review status, and run reports.

## Permission Requirements

The identity running the bot or automation must have:

- Read access to the source work-order groups.
- `im:chat:read` and message read/search scopes as needed.
- Write permission to the target candidate Wiki node.
- Write permission to the shared index document.
- GitHub push or repository write permission when Markdown archive snapshots are enabled.

If the teammate can read their work-order groups but cannot write to the shared pool, ask the pool owner to grant edit permission to the teammate or to the bot.
