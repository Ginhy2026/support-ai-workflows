# Lark Workflow

Use these commands as implementation guidance. Prefer dry-run or read-only steps until target Wiki and index document are confirmed.

## Required Skills and Permissions

Use these local Lark skills when available:

- `lark-im` for chat search, message search, message listing, thread expansion, and resource download.
- `lark-doc` for creating candidate documents and updating the shared index document.
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

- Source scope: existing Feishu candidate Wiki node and shared index document.
- Time window: not required unless the user asks to inspect recent writes only.
- Output mode: update existing Feishu pages/index plus GitHub archive when enabled.
- Candidate key: use the existing key from the index/page; never invent a new key for cleanup.

Single-case manual capture:

```text
使用 feishu-knowledge-capture，把下面这个 support-triage 输出和最终方案沉淀成候选知识。
使用 feishu-knowledge-capture，把这个未闭环的新产品问题写入 Pending 候选池。
Use $feishu-knowledge-capture to turn this support-triage output and final solution into a candidate fault article.
```

For single-case mode:

- Source scope: `single-case`.
- Time window: not required unless source messages need to be fetched.
- Output mode: dry-run if target Wiki/index is missing; otherwise candidate write plus GitHub archive.
- Candidate key: work-order ID if present, thread ID if present, otherwise fallback hash.

If the input is a `support-triage` output, parse its knowledge-capture section automatically:

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

If the same input also contains a human-written final answer or numbered troubleshooting manual, use that final answer as the main candidate body. The support-triage output is metadata and supporting context, not the structure to blindly follow.

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

Scope-only commands such as `沉淀今天所有工单群` are not report-generation commands. They must run the case-capture pipeline: discover source chats, group messages into cases, decide closure/maturity, and write per-case candidate FAQ/fault/SOP/Pending records. A work-order summary may appear only in the final run report, not as the candidate page body.

Leader pilot commands:

```text
@Leader的飞书智能体 /skill install https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
@Leader的飞书智能体 /skill update https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
@Leader的飞书智能体 使用 feishu-knowledge-capture，候选目录写入：https://www.feishu.cn/wiki/QiPGwE9Y4iukxfkMh8YcXPKNnBd ，统一索引文档写入：https://www.feishu.cn/wiki/SarowXaTji5farkayOBcbYfqn2d ，GitHub归档写入 Ginhy2026/support-ai-workflows 的 knowledge-archive。
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

For wide work-order scopes, split by stable case boundaries before generating any candidate:

- Prefer explicit work-order IDs such as `JSWO-`, `DLSGD-`, or `DBWO-`.
- If no work-order ID exists, use Feishu thread/topic boundaries.
- If neither exists, group by one product/module plus one coherent symptom.
- Do not merge unrelated work orders into a single `工单总结报告` candidate page.

## Image, Card, and File Evidence

Message listing renders images and files as placeholders. If the visible text is already present in message content or card text, use it. If the case requires the underlying image/file:

```powershell
lark-cli im +messages-resources-download --message-id om_xxx --type image --output .\tmp
```

If OCR or image reading is unavailable, mark `截图/卡片文本是否完整可读：否` and put the case in pending when the missing text blocks diagnosis.

## Reference Documents and Media

Before generating a candidate, inspect any Feishu, Yuque, GitHub, web, SOP, or official manual links found in the source case.

For each reference:

- Resolve the title and readable content when the current identity has permission.
- Record the URL, maturity (`M0`-`M4`), applicability (`A0`-`A3`), read status, and citation reason in the candidate `参考资料` section.
- If the content is not readable, do not infer technical details from the title. Mark `是否已读取：否` and preserve the link.
- If readable, extract only the key conclusion, steps, warnings, scope, and version boundaries needed for the current case.
- If the reference contains key images or tables, attempt to fetch or insert only the relevant media. If this is not possible, keep a note such as `图片未复制，仅可从原文查看：<section>`.

When a reference is `M4 正式知识` and `A3 直接适用`, default to an index/case-application record instead of creating a duplicate long-form candidate page. Create a supplemental candidate only when the current case adds a new boundary, exception, customer wording, or local workaround.

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

Do not create documents if the target Wiki or index document is not configured. Output a dry-run report instead.

The target Wiki parent must be the review/candidate child node, such as `候选知识碎片/待审核`. Do not write generated content to the root/landing page of the candidate pool, such as `候选知识碎片`. If the provided target looks like a landing page, root directory, or documentation page, stop before any `docs +update`/`wiki +node-create` write and ask for the `待审核` node plus the shared index document.

Before writing, fetch or resolve the target node title when practical. Reject targets whose title is only `候选知识碎片`, `知识碎片`, `候选池`, or other pool/root names unless the user explicitly requested maintenance of that landing page.

## Preflight Feishu Write Targets

When both a candidate node and shared index document are configured, the runner must verify them with read-only commands before deciding to skip Feishu writes.

Preflight checks:

- Resolve the candidate Wiki node token or URL and confirm the current identity can read it.
- Confirm the candidate node title/path is the review area, for example `待审核`, not the root `候选知识碎片` landing page.
- Fetch the shared index with the document URL or docx token accepted by `docs +fetch`.
- Search each generated candidate key in the shared index before creating or updating pages.

Example target probe:

```powershell
lark-cli.cmd wiki spaces get_node --params "{\"token\":\"<candidate_node_token>\"}" --format json
```

If the installed CLI exposes a different Wiki read shortcut, use the local shortcut, but the report must still include the command/tool name, target token, and resulting title or error.

Example index probe and dedupe search:

```powershell
lark-cli.cmd docs +fetch --api-version v2 --doc "<index doc url or docx token>" --doc-format xml --scope keyword --keyword "workorder:JSWO-202604220005" --format json
```

Preflight outcomes:

- `preflight_ok`: continue to `docs +create`, `wiki +node-create`, and index `docs +update`.
- `preflight_failed`: stop Feishu writes, optionally archive generated Markdown as fallback evidence, and return `dry-run` with the failed command, target, and error.
- `preflight_not_attempted`: treat as a skill execution error when targets were configured. Do not report the run as completed or as normal archive-only output.

Do not write "permission not confirmed", "dedupe not confirmed", or "target status unclear" unless the corresponding read-only preflight command was actually attempted and failed.

## Update Shared Index

Before writing, fetch the shared index and search by candidate key:

```powershell
lark-cli.cmd docs +fetch --api-version v2 --doc "<index doc url or token>" --doc-format xml --scope keyword --keyword "thread:omt_xxx" --format json
```

Use the index document URL or docx token for `docs +fetch`/`docs +update`. Do not pass a Wiki node token as `index_doc_token` unless `docs +fetch` has already proven that the CLI resolves it correctly. In config and reports, distinguish:

- `index_doc_token`: underlying docx token for Docs API writes.
- `index_wiki_node_token`: Wiki node token for navigation/copy links.
- `index_wiki_url`: human-facing Wiki URL.

If the key is found, do not create a new candidate page. Either skip it or update the existing page with an `更新记录` section according to `references/review-rules.md`.

For cleanup, if multiple pages exist for the same exact key, choose the canonical page first, mark duplicates obsolete, then update the index row to the canonical title/link/status. Prefer block-level replacement for one index row instead of overwriting the whole index document.

For JSWO groups, use `workorder:<JSWO-id>` as the dedupe key. Multiple users running the same work order must update or skip the existing candidate rather than creating duplicate pages.

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
- Support owner
- Department leader
- Product/service representative
- Trigger person
- Contributors
- Last updater
- Candidate document link
- GitHub archive snapshot path
- Current version number
- Last updated time
- Recent change summary
- Review status

## GitHub Markdown Archive

After a Feishu candidate is created or updated, save the generated candidate Markdown to the repository archive. Do not archive full raw chat logs.

Archive-only output is allowed only as an explicit dry-run or safety fallback. It must not be reported as a completed Feishu knowledge capture. If Feishu writes were skipped, the final report must say `dry-run/archive-only`, list that no `docs +create`, `wiki +node-create`, or `docs +update` write happened, and identify the blocker such as missing configuration or a failed preflight command. When targets are configured, "unverified target" or "unresolved dedupe check" is acceptable only if the attempted preflight command and error are included.

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
- Feishu write status: `completed`, `partial`, `dry-run`, or `archive-only`
- Feishu preflight status: `preflight_ok`, `preflight_failed`, or `preflight_not_attempted`
- Candidate target token/title and index doc token used
- Explicit note when local Markdown was generated but Feishu writes were not executed
- Permission or configuration failures
