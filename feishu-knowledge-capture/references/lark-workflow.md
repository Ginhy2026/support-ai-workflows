# Lark Workflow

Use these commands as implementation guidance. Prefer dry-run or read-only steps until target Wiki and candidate Base table are confirmed.

## Required Skills and Permissions

Use these local Lark skills when available:

- `lark-im` for chat search, message search, message listing, thread expansion, and resource download.
- `lark-doc` for creating candidate documents.
- `lark-base` for reading, creating, and updating shared candidate Base records and status views.
- `lark-wiki` for creating or moving candidate nodes under the target Wiki parent.

Expected scopes include message search/read, chat read, docs create/update, and Wiki node create/move permissions.

## Invocation Modes

Maintenance / cleanup:

```text
使用 feishu-knowledge-capture，清理候选池里重复的 T300 网络域 FAQ
使用 feishu-knowledge-capture，修正这个候选答案，并把重复文档标记废弃
使用 feishu-knowledge-capture，检查支持知识碎片候选池里是否有重复候选
```

For maintenance mode:

- Source scope: existing Feishu candidate Wiki node and shared candidate Base table.
- Time window: not required unless the user asks to inspect recent writes only.
- Output mode: update existing Feishu pages/Base records plus GitHub archive when enabled.
- Candidate key: use the existing key from the Base record/page; never invent a new key for cleanup.
- Blank-key records are repair targets. Derive the missing key from thread/work-order evidence when possible, otherwise use the fallback hash, then update the same row and canonical candidate page instead of creating another row.

Single-case manual capture:

```text
使用 feishu-knowledge-capture，把下面这个 supportman 输出和最终方案沉淀成候选知识。
使用 feishu-knowledge-capture，把这个未闭环的新产品问题写入 Pending 候选池。
Use $feishu-knowledge-capture to turn this supportman output and final solution into a candidate fault article.
```

For single-case mode:

- Source scope: `single-case`.
- Time window: not required unless source messages need to be fetched.
- Output mode: dry-run if target Wiki/Base table is missing; otherwise candidate write plus GitHub archive.
- Candidate key: work-order ID if present, thread ID if present, otherwise fallback hash.

If the input is a `supportman` output, parse its knowledge-capture section automatically:

```text
是否建议进入 feishu-knowledge-capture 候选池
- 判断：不沉淀 / 待闭环后沉淀 / 建议立即候选沉淀
- 理由：
- 建议沉淀类型：FAQ / SOP / 排障知识 / Pending
- 进入候选池前缺失：
```

Normalize English labels if present:

- `Not captured` -> `不沉淀`
- `Capture after closure` -> `待闭环后沉淀`
- `Candidate now` -> `建议立即候选沉淀`

Then apply `references/review-rules.md`:

- `不沉淀`: skipped report only.
- `待闭环后沉淀`: Pending, usually `M0` or `M1`.
- `建议立即候选沉淀`: FAQ/SOP/fault candidate, usually `M2`, unless closure evidence is still missing.

If the same input also contains a human-written final answer or numbered troubleshooting manual, use that final answer as the main candidate body. The supportman output is metadata and supporting context, not the structure to blindly follow.

Default automation:

```text
每天 18:30 自动沉淀今天 supportman 话题聊天
```

Manual commands may request a different scope:

```text
/飞书知识沉淀 获取今天 supportman 话题并沉淀
/飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
/飞书知识沉淀 获取昨天所有群聊中的技术支持问题并沉淀
/飞书知识沉淀 获取今天所有私聊中的工单问题并沉淀
/飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
```

Map the command to:

- Source scope: `supportman`, `jswo-groups`, `all-group-chats`, `all-private-chats`, or `named-chat`.
- Time window: today by default; support yesterday, this week, and explicit date ranges.
- Output mode: Feishu write plus GitHub archive by default; `dry-run` reports only.
- Target: configured candidate Wiki node and shared candidate Base table.

Leader pilot commands:

```text
@Leader的飞书智能体 /skill install https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
@Leader的飞书智能体 /skill update https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
@Leader的飞书智能体 使用 feishu-knowledge-capture，候选目录写入：https://www.feishu.cn/wiki/QiPGwE9Y4iukxfkMh8YcXPKNnBd ，统一候选 Base 写入：https://www.feishu.cn/base/YfRTb0oJUazkCAsL2jYcOCcRndh ，GitHub归档写入 Ginhy2026/support-ai-workflows 的 knowledge-archive。
候选 Base 表 ID：tblHMj8buOaGsmNY
@Leader的飞书智能体 /飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
@Leader的飞书智能体 /飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
```

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

For SupportMan/supportman filtering across a chat, include the legacy `/support-triage` keyword during migration:

```powershell
lark-cli im +messages-search --query "/supportman" --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --page-all --format json
```

Also search for bot/user trigger phrases if configured:

```powershell
lark-cli im +messages-search --query "/support-triage" --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --page-all --format json
```

```powershell
lark-cli im +messages-search --query "supportman" --chat-id oc_xxx --start "2026-05-21T00:00:00+08:00" --end "2026-05-21T18:00:00+08:00" --page-all --format json
```

For all-group or all-private manual runs, apply keyword filtering before case extraction. Useful filters include `/supportman`, `/support-triage`, `SupportMan`, `supportman`, `JSWO-`, product names, `星火计划`, `售前`, `故障`, `报错`, `无法`, `异常`, `排查`, `解决`, `FAQ`, `SOP`, and configured robot/customer support terms.

## Expand Threads

If a result has `thread_id`, fetch the thread:

```powershell
lark-cli im +threads-messages-list --thread omt_xxx --sort asc --page-size 50 --format json
```

Keep the root message, replies, supportman response, and human follow-up together as one case.

## Image, Card, and File Evidence

Message listing renders images and files as placeholders. If the visible text is already present in message content or card text, use it. If the case requires the underlying image/file:

```powershell
lark-cli im +messages-resources-download --message-id om_xxx --type image --output .\tmp
```

Image handling policy:

- Default to metadata-only for unrelated images. Do not download every image in a broad chat scan.
- Select up to 3 high-value images per case for reading/OCR by default. Prioritize images near messages containing error codes, `根因`, `解决方案`, `解决版本`, `升级`, `版本`, `阈值`, `参数`, `已解决`, or customer confirmation.
- If more than 3 images look important, read the 3 most likely to contain root cause or solution, then list the remaining unread images in `缺失信息` or `备注/风险提示`.
- When an image is read, extract exact values such as solve version, firmware/APK version, threshold percentage, current/voltage/resistance, port, error code, and pass/fail criteria.
- If OCR or image reading is unavailable, mark `截图/卡片文本是否完整可读：否` and `关键图片未读取`. Put the case in Pending or keep it low-confidence when the missing image may contain diagnosis or solution. Do not write `根因未明确` when an unread image likely contains the final answer.

Tradeoff: reading selected images costs more model time and tokens than text-only capture, but bounded selection avoids runaway cost. Full media copying is optional and should be reserved for images that directly support diagnosis, troubleshooting steps, customer reply, or review evidence.

## Reference Documents and Media

Before generating a candidate, inspect any Feishu, Yuque, GitHub, web, SOP, or official manual links found in the source case.

For each reference:

- Resolve the title and readable content when the current identity has permission.
- Record the URL, maturity (`M0`-`M4`), applicability (`A0`-`A3`), read status, and citation reason in the candidate `参考资料` section.
- Treat Feishu document cards as references even when the raw message export only exposes the card title. If the source text says `具体操作见如下文档`, `操作说明`, `参考文档`, `见链接`, `SOP`, or `手册`, search the visible card title with `drive +search`, preserve the best matched URL, and record whether the document was actually read.
- If a relevant document card exists but cannot be opened, keep its title/link in `参考资料` and write `读取状态：未读取`. Do not claim the operation document is missing.
- If the content is not readable, do not infer technical details from the title. Mark `是否已读取：否` and preserve the link.
- If readable, extract only the key conclusion, steps, warnings, scope, and version boundaries needed for the current case.
- If the reference contains key images or tables, attempt to fetch or insert only the relevant media. If this is not possible, keep a note such as `图片未复制，仅可从原文查看：<section>`.

When a reference is `M4 正式知识` and `A3 直接适用`, default to a Base case-application record instead of creating a duplicate long-form candidate page. Create a supplemental candidate only when the current case adds a new boundary, exception, customer wording, or local workaround.

## Parse JSWO Work-Order Group Names

Run:

```powershell
python feishu-knowledge-capture\scripts\parse_work_order_group.py "【新问题_进行中】PUDU T300法国JSWO-202604220005"
```

Use the parsed status/product/customer/work-order fields as metadata only. Closure still depends on message content.

## Resolve Work-Order Roles

Record role fields separately from the trigger person:

- `support_owner`: technical support owner.
- `leader`: support department leader.
- `service_representative`: product or middle-platform service representative.
- `triggered_by`: current invoking user.
- `contributors`: people who provided key evidence or solutions.
- `last_updated_by`: current writer identity for updates.

Resolve roles in this order:

1. Configured local role map or explicit command arguments.
2. Work-order source metadata, if available.
3. Group membership and message behavior.
4. `待确认`.

Do not set the trigger person as support owner unless supported by the role map or message evidence.

## Create Candidate Document

Create the document body from `references/templates.md`.

```powershell
lark-cli docs +create --api-version v2 --title "候选故障知识：<标题>" --content "@candidate.xml"
```

For long or multi-line content, always write the XML or Markdown to a relative file first and pass it as `--content "@candidate.xml"` or `--content "@candidate.md"`. Do not pass multi-line content directly through PowerShell; some `lark-cli` versions only receive the first line and create a blank-looking document.

If the Wiki workflow requires a node under a parent, create or move the document into the target Wiki candidate parent with `lark-cli wiki +node-create` or the available Wiki shortcut for the configured space.

Do not create documents if the target Wiki or candidate Base table is not configured. Output a dry-run report instead.

For updates, do not create a replacement page when an existing Base record already has `候选文档链接`. Read that page first, replace or append the candidate content according to `references/review-rules.md`, and preserve a compact `更新记录`. A console report or GitHub archive update without a Feishu candidate page update is not a successful Feishu write.

## Update Shared Candidate Base

Before writing, fetch the shared candidate Base and search by candidate key in the `唯一键` field:

```powershell
lark-cli.cmd base +record-search --base-token "<base token>" --table-id "<table id>" --json '{"keyword":"thread:omt_xxx","search_fields":["唯一键"],"select_fields":["唯一键","标题","候选文档链接","审核状态","GitHub归档路径"],"limit":10}' --format json
```

Compare returned `唯一键` values exactly. If the key is found, do not create a new candidate page. Either skip it or update the existing page with an `更新记录` section according to `references/review-rules.md`.

Before creating a new record, also search/read nearby records by title/source when the key was not found. If a matching row has blank `唯一键`, repair that existing row: set `唯一键`, keep or correct `候选文档链接`, update `来源 thread`, and write the latest GitHub archive path. This prevents second-run data from sitting outside the deterministic dedupe system.

Every record payload must include a non-empty `唯一键`. Validate the JSON payload before calling `+record-upsert`; if `唯一键` is null, empty, `-`, or a human-readable source/date string, stop and return `missing_candidate_key`.

```powershell
python feishu-knowledge-capture\scripts\validate_candidate_record.py .\candidate-base-record.json
```

Use `--allow-legacy` only while repairing older records that already have non-prefixed keys such as historical title slugs. Do not use legacy keys for new records; prefer migrating them to `thread:`, `workorder:`, `node:`, or `hash:` when the evidence is clear.

For cleanup, if multiple pages exist for the same exact key, choose the canonical page first, mark duplicates obsolete, then update the canonical Base record to the canonical title/link/status and mark duplicate records as `已废弃/重复`.

For JSWO groups, use `workorder:<JSWO-id>` as the dedupe key. Multiple users running the same work order must update or skip the existing candidate rather than creating duplicate pages.

Create one record per new candidate in the shared candidate Base table:

```powershell
lark-cli.cmd base +record-upsert --base-token "<base token>" --table-id "<table id>" --json @candidate-base-record.json
```

Update an existing record only when material information changes:

```powershell
lark-cli.cmd base +record-upsert --base-token "<base token>" --table-id "<table id>" --record-id "<record id>" --json @candidate-base-record.json
```

The Base record must include:

- `唯一键`
- `日期`
- `类型`
- `产品/模块`
- `工单号`
- `来源 thread`
- `标题`
- `来源群/来源渠道`
- `负责人/同事`
- `候选文档链接`
- `成熟度`
- `审核状态`
- `审核人`
- `发布目标`
- `公共文档链接`
- `最后更新时间`
- `GitHub归档路径`
- `备注/风险提示`

When setting up a new Base, create status views filtered by `审核状态`: `待审核`, `需补充`, `已通过待发布` (filter value `已通过`), `已发布`, and `已废弃/重复`.

After each write, verify both surfaces:

```powershell
lark-cli.cmd base +record-get --base-token "<base token>" --table-id "<table id>" --record-id "<record id>" --format json
```

Confirm that `唯一键`, `候选文档链接`, `GitHub归档路径`, and `最后更新时间` match the intended payload. Then open/read the candidate document link enough to confirm the latest source/evidence/update record is present. If either verification fails, report `write_incomplete` with the failing surface; do not say the candidate was updated.

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
  --support-owner "A" `
  --leader "B" `
  --service-representative "C" `
  --triggered-by "B" `
  --contributors "A,C" `
  --content-file ".\candidate.md"
```

Use the returned `latest_snapshot` value in the `GitHub归档路径` Base field and the update report.

For run reports, save a separate Markdown report under:

- `knowledge-archive/supportman/YYYY-MM-DD/run-report.md` for default automation.
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
