# Lark Workflow

Use these commands as implementation guidance. Prefer dry-run or read-only steps until target Wiki and index document are confirmed.

## Required Skills and Permissions

Use these local Lark skills when available:

- `lark-im` for chat search, message search, message listing, thread expansion, and resource download.
- `lark-doc` for creating candidate documents and updating the shared index document.
- `lark-wiki` for creating or moving candidate nodes under the target Wiki parent.

Expected scopes include message search/read, chat read, docs create/update, and Wiki node create/move permissions.

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

Append one row per candidate to the shared index document:

```powershell
lark-cli docs +update --api-version v2 --doc "<index doc url or token>" --command append --content "@index-row.md"
```

The index row must include:

- Date
- Type
- Product/module
- Work-order ID
- Title
- Source group
- Owner
- Candidate document link
- Review status

## Daily Report

Report both writes and non-writes. Include:

- Source chats and time range
- Messages read
- Cases recognized
- Candidate pages created
- Pending cases
- Skipped duplicates
- Permission or configuration failures
