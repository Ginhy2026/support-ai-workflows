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
FEISHU_KNOWLEDGE_BASE_TOKEN=<支持知识碎片候选池 base token>
FEISHU_KNOWLEDGE_BASE_TABLE_ID=tblHMj8buOaGsmNY
FEISHU_KNOWLEDGE_BASE_URL=<支持知识碎片候选池 base url>
```

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
FEISHU_KNOWLEDGE_BASE_TOKEN=YfRTb0oJUazkCAsL2jYcOCcRndh
FEISHU_KNOWLEDGE_BASE_URL=https://www.feishu.cn/base/YfRTb0oJUazkCAsL2jYcOCcRndh
FEISHU_KNOWLEDGE_BASE_TABLE_ID=<候选记录 table id>
```

Only use these shared-pool values when the user explicitly wants all teammates to write into the same candidate pool and the current Feishu identity has write permission.

## Personal Mode

Use personal mode when each teammate keeps a private candidate pool.

```text
FEISHU_KNOWLEDGE_MODE=personal
FEISHU_KNOWLEDGE_CANDIDATE_NODE_TOKEN=<their own 待审核 node token>
FEISHU_KNOWLEDGE_BASE_TOKEN=<their own candidate Base token>
FEISHU_KNOWLEDGE_BASE_TABLE_ID=<their own candidate table id>
```

## Candidate Base Schema

The shared pool uses one Feishu Base table with these fields:

```text
唯一键, 日期, 类型, 产品/模块, 工单号, 来源 thread, 标题, 来源群/来源渠道, 负责人/同事,
候选文档链接, 成熟度, 审核状态, 审核人, 发布目标, 公共文档链接, 最后更新时间,
GitHub归档路径, 备注/风险提示
```

`类型` is a single-select field with: `故障`, `FAQ`, `SOP`, `故障+FAQ`, `故障/SOP`, `待确认`.

`成熟度` is a single-select field with: `M0 原始线索`, `M1 初步判断`, `M2 候选草稿`, `M3 已审核候选`, `M4 正式知识`, `待确认`.

`审核状态` is a single-select field with: `待审核`, `需补充`, `已通过`, `已发布`, `不沉淀`, `已废弃/重复`, `待确认`.

Create status views filtered by `审核状态`: `待审核`, `需补充`, `已通过待发布` (filter value `已通过`), `已发布`, and `已废弃/重复`.

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
- `target`: team candidate node and shared candidate Base when `FEISHU_KNOWLEDGE_MODE=team`.

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

Use GitHub Markdown archive snapshots for version history. The runner should create or update files under `FEISHU_KNOWLEDGE_ARCHIVE_ROOT`, write the snapshot path back to the `GitHub归档路径` Base field, and commit the archive with the skill/repo workflow.

Do not store raw full chat transcripts in the archive. Store only generated candidate Markdown, minimal source identifiers, Feishu document links, review status, and run reports.

## Permission Requirements

The identity running the bot or automation must have:

- Read access to the source work-order groups.
- `im:chat:read` and message read/search scopes as needed.
- Write permission to the target candidate Wiki node.
- Write permission to the shared candidate Base table.
- GitHub push or repository write permission when Markdown archive snapshots are enabled.

If the teammate can read their work-order groups but cannot write to the shared pool, ask the pool owner to grant edit permission to the teammate or to the bot.
