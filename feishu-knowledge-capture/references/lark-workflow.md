# Lark Workflow

Use these commands as implementation guidance. Prefer dry-run or read-only steps until target Wiki and index document are confirmed.

## Required Skills and Permissions

Use these local Lark skills when available:

- `lark-im` for chat search, message search, message listing, thread expansion, and resource download.
- `lark-doc` for creating candidate documents and updating the shared index document.
- `lark-wiki` for creating or moving candidate nodes under the target Wiki parent.

Expected scopes include message search/read, chat read, docs create/update, and Wiki node create/move permissions.

## Invocation Modes

Default automation:

```text
每天 18:30 自动沉淀今天 support-triage 话题聊天
```

Manual commands may request a different scope:

```text
/飞书知识沉淀 获取今天 support-triage 话题并沉淀
/飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
/飞书知识沉淀 获取昨天所有群聊中的技术支持问题并沉淀
/飞书知识沉淀 获取今天所有私聊中的工单问题并沉淀
/飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
```

Map the command to:

- Source scope: `support-triage`, `jswo-groups`, `all-group-chats`, `all-private-chats`, or `named-chat`.
- Time window: today by default; support yesterday, this week, and explicit date ranges.
- Output mode: Feishu write plus GitHub archive by default; `dry-run` reports only.
- Target: configured candidate Wiki node and shared index document.

## Resolve Source Chat

When only a group name is known:

```powershell
lark-cli im +chat-search --query "Gin的AI员工话题群" --format json
```

When the source group is a work-order group, search by stable parts:

```powershell
lark-cli im +chat-search --query "JSWO-202604220005" --format json
```

Prefer a configured `chat_id` once known.

For all JSWO work-order groups, search visible chats by the configured ticket pattern:

```powershell
lark-cli im +chat-search --query "JSWO-" --format json
```

For broad manual scopes, enumerate only chats visible to the current identity and then filter messages by technical-support signals. Do not process unrelated chats just because they are visible.

## Fetch Messages

For a daily run:

```powershell
lark-cli im +chat-messages-list --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --sort asc --page-size 50 --format json
```

For support-triage filtering across a chat:

```powershell
lark-cli im +messages-search --query "/support-triage" --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --page-all --format json
```

Also search for bot/user trigger phrases if configured:

```powershell
lark-cli im +messages-search --query "support-triage" --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --page-all --format json
```

For all-group or all-private manual runs, apply keyword filtering before case extraction. Useful filters include `/support-triage`, `support-triage`, `JSWO-`, product names, `故障`, `报错`, `无法`, `异常`, `排查`, `解决`, `FAQ`, `SOP`, and configured robot/customer support terms.

## Expand Threads

If a result has `thread_id`, fetch the thread:

```powershell
lark-cli im +threads-messages-list --thread omt_xxx --sort asc --page-size 50 --format json
```

Keep the root message, replies, support-triage response, and human follow-up together as one case.

## Image, Card, and File Evidence

Message listing renders images and files as placeholders. If the visible text is already present in message content or card text, use it. If the case requires the underlying image/file:

```powershell
lark-cli im +messages-resources-download --message-id om_xxx --type image --output .\tmp
```

If OCR or image reading is unavailable, mark `截图/卡片文本是否完整可读：否` and put the case in pending when the missing text blocks diagnosis.

## Parse JSWO Work-Order Group Names

Run:

```powershell
python feishu-knowledge-capture\scripts\parse_work_order_group.py "【新问题_进行中】PUDU T300法国JSWO-202604220005"
```

Use the parsed status/product/customer/work-order fields as metadata only. Closure still depends on message content.

## Create Candidate Document

Create the document body from `references/templates.md`.

```powershell
lark-cli docs +create --api-version v2 --title "候选故障知识：<标题>" --content "@candidate.xml"
```

For long or multi-line content, always write the XML or Markdown to a relative file first and pass it as `--content "@candidate.xml"` or `--content "@candidate.md"`. Do not pass multi-line content directly through PowerShell; some `lark-cli` versions only receive the first line and create a blank-looking document.

If the Wiki workflow requires a node under a parent, create or move the document into the target Wiki candidate parent with `lark-cli wiki +node-create` or the available Wiki shortcut for the configured space.

Do not create documents if the target Wiki or index document is not configured. Output a dry-run report instead.

## Update Shared Index

Before writing, fetch the shared index and search by candidate key:

```powershell
lark-cli.cmd docs +fetch --api-version v2 --doc "<index doc url or token>" --doc-format xml --scope keyword --keyword "thread:omt_xxx" --format json
```

If the key is found, do not create a new candidate page. Either skip it or update the existing page with an `更新记录` section according to `references/review-rules.md`.

Append one row per new candidate to the shared index document:

```powershell
lark-cli docs +update --api-version v2 --doc "<index doc url or token>" --command append --content "@index-row.md"
```

The index row must include:

- Unique key
- Date
- Type
- Product/module
- Work-order ID
- Source thread
- Title
- Source group
- Owner
- Candidate document link
- GitHub archive snapshot path
- Current version number
- Last updated time
- Recent change summary
- Review status

## GitHub Markdown Archive

After a Feishu candidate is created or updated, save the generated candidate Markdown to the repository archive. Do not archive full raw chat logs.

```powershell
python feishu-knowledge-capture\scripts\archive_snapshot.py `
  --root knowledge-archive `
  --candidate-key "workorder:JSWO-202604220005" `
  --type "故障" `
  --source-scope "JSWO工单群" `
  --title "候选故障知识：<标题>" `
  --feishu-doc-url "https://www.feishu.cn/wiki/xxx" `
  --review-status "待审核" `
  --content-file ".\candidate.md"
```

Use the returned `latest_snapshot` and `latest_version` values in the shared index row or update report.

For run reports, save a separate Markdown report under:

- `knowledge-archive/support-triage/YYYY-MM-DD/run-report.md` for default automation.
- `knowledge-archive/manual-runs/YYYY-MM-DD-operator-<name>/run-report.md` for broad manual runs when an operator name is known.

## Daily Report

Report both writes and non-writes. Include:

- Source chats and time range
- Messages read
- Cases recognized
- Candidate pages created
- Candidate pages updated
- Pending cases
- Skipped duplicates
- GitHub archive snapshots
- Permission or configuration failures
