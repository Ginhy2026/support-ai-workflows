# Lark Workflow

Use these commands as implementation guidance. Prefer dry-run or read-only steps until the personal document target is confirmed.

## Required Skills and Permissions

Use these local Lark skills when available:

- `lark-im` for selected chat search, message search, message listing, thread expansion, and resource download.
- `lark-doc` for creating personal case documents and updating the personal index document.
- `lark-wiki` for creating or moving case-note nodes under the personal Wiki parent.

Expected scopes include message search/read, chat read, docs create/update, and Wiki node create/move permissions for the current identity.

## Invocation Modes

Single-case manual capture:

```text
使用 feishu-knowledge-capture，把下面这段案例摘要沉淀成个人 case 文档。
使用 feishu-knowledge-capture，把下面这个已闭环案例整理成个人排障沉淀。
使用 feishu-knowledge-capture，把这个未闭环的新产品问题写入个人 Pending 线索。
```

For single-case mode:

- Source scope: `single-case`.
- Time window: not required unless source messages need to be fetched.
- Output mode: dry-run if target personal document group is missing; otherwise create/update case document plus optional index/archive.
- Case key: work-order ID if present, thread ID if present, source document node if present, otherwise fallback hash.

Selected chat capture:

```text
/飞书知识沉淀 获取今天群聊「xxx」里的关键信息并沉淀
/飞书知识沉淀 获取本周这些群聊：A、B、C，整理成个人 case 文档
/飞书知识沉淀 获取昨天 JSWO-202604220005 工单群内容并沉淀
```

Map the command to:

- Source scope: named chat, selected chats, explicit chat ID, explicit thread/message link, or visible work-order groups requested by the user.
- Time window: user-specified first; today in Asia/Shanghai when omitted.
- Output mode: personal case document plus optional personal index; `dry-run` reports only.
- Target: configured personal document group/Wiki parent and optional personal index document.

## Resolve Source Chat

When only a group name is known:

```powershell
lark-cli im +chat-search --query "PUDU T300法国JSWO-202604220005" --format json
```

Prefer a configured `chat_id` once known.

For visible work-order groups, search by the configured ticket pattern:

```powershell
lark-cli im +chat-search --query "JSWO-" --format json
```

Only enumerate chats visible to the current identity. For broad personal-visible requests, filter by configured technical-support keywords before case extraction.

## Fetch Messages

For a selected chat:

```powershell
lark-cli im +chat-messages-list --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --sort asc --page-size 50 --format json
```

For keyword filtering inside a selected chat:

```powershell
lark-cli im +messages-search --query "JSWO-" --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --page-all --format json
```

Useful filters include `JSWO-`, product names, `故障`, `报错`, `无法`, `异常`, `排查`, `解决`, `FAQ`, `SOP`, and configured robot/customer support terms.

## Expand Threads

If a result has `thread_id`, fetch the thread:

```powershell
lark-cli im +threads-messages-list --thread omt_xxx --sort asc --page-size 50 --format json
```

Keep the root message, replies, tool/bot summaries, and human follow-up together as one case.

## Image, Card, and File Evidence

Message listing may render images and files as placeholders. If the visible text is already present in message content or card text, use it. If the case requires the underlying image/file:

```powershell
lark-cli im +messages-resources-download --message-id om_xxx --type image --output .\tmp
```

If OCR or image reading is unavailable, mark `关键图片/卡片未读取` and put the case in `需补充` when the missing text blocks diagnosis.

## Reference Documents and Media

Before generating a case note, inspect any Feishu, Yuque, GitHub, web, SOP, or official manual links found in the source case.

For each reference:

- Resolve the title and readable content when the current identity has permission.
- Record the URL, source type, read status, and citation reason in the case note `参考资料` section.
- If the content is not readable, do not infer technical details from the title. Mark `读取状态：未读取` and preserve the link.
- If readable, extract only the key conclusion, steps, warnings, scope, and version boundaries needed for the current case.

## Parse JSWO Work-Order Group Names

Run:

```powershell
python feishu-knowledge-capture\scripts\parse_work_order_group.py "【新问题_进行中】PUDU T300法国JSWO-202604220005"
```

Use the parsed status/product/customer/work-order fields as metadata only. Closure still depends on message content.

## Create Personal Case Document

Create the document body from `references/templates.md`.

```powershell
lark-cli docs +create --api-version v2 --title "个人case沉淀：<标题>" --content "@case-note.md"
```

For long or multi-line content, always write the Markdown to a relative file first and pass it as `--content "@case-note.md"`. Do not pass multi-line content directly through PowerShell.

If the Wiki workflow requires a node under a parent, create or move the document into the personal Wiki parent with `lark-cli wiki +node-create` or the available Wiki shortcut for the configured space.

Do not create documents if the personal document group/Wiki parent is not configured. Output a dry-run case note instead.

## Update Personal Index

After the case document link is known, append or update one row in the optional personal index document:

```powershell
lark-cli docs +update --api-version v2 --doc "<personal index doc url or token>" --command append --content "@personal-index-row.md"
```

The index row must include only:

```text
关键词, 类型, 模块, 标题, 来源, 文档链接, 状态
```

Do not expand the personal index into an approval workflow, management console, or company review table.

For duplicate handling, search the personal index by case key, title, work-order ID, or source thread when possible. If a case note already exists and new material changes the answer, update the case note and append a compact `更新记录`.

## Archive to GitHub

After a personal case note is created or updated, save the generated Markdown to the repository archive when archive output is enabled. Do not archive full raw chat logs.

```powershell
python feishu-knowledge-capture\scripts\archive_snapshot.py `
  --candidate-key "workorder:JSWO-202604220005" `
  --type "故障" `
  --source-scope "personal-case" `
  --title "个人case沉淀：<标题>" `
  --feishu-doc-url "https://..." `
  --review-status "已沉淀" `
  --triggered-by "<user>" `
  --last-updated-by "<user or bot>" `
  --content-file ".\case-note.md"
```

Use the returned `latest_snapshot` and `latest_version` values in the run report when useful.

## Run Report Archive

For run reports, save a separate Markdown report only when archive output is enabled:

- `knowledge-archive/personal/YYYY-MM-DD/run-report.md`
