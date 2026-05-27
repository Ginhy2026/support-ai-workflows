---
name: feishu-knowledge-capture
description: Capture single support cases, supportman outputs, Feishu topic threads, JSWO work-order groups, and manually requested Feishu chat scopes into candidate Feishu Wiki knowledge drafts, shared Feishu Base records, and GitHub Markdown archives. Use when Codex needs to convert one resolved or pending support case into candidate FAQ/fault/SOP/Pending knowledge, collect supportman cases in batch, extract reusable knowledge from Feishu messages, run daily knowledge capture, prepare a shared candidate knowledge pool, update a Feishu Wiki or candidate Base table, or archive candidate knowledge snapshots for version history.
---

# Feishu Knowledge Capture

## Purpose

Use this skill to turn one support case or many Feishu support discussions into candidate knowledge drafts for human review. It is the unified knowledge-capture layer after `supportman`: collect source material, group it into cases, classify whether it is suitable for knowledge capture, write candidate drafts to Feishu Wiki, update the shared candidate Base table, and optionally archive Markdown snapshots to GitHub for version history.

The default automated source is the user's configured supportman topic group. Single-case manual capture, JSWO work-order groups, and broad chat scopes are supported for manual or configured runs, but generated knowledge must still be treated as a candidate draft until reviewed.

## Load References

- For Feishu IM, Docs, Wiki, and index-update commands, read `references/lark-workflow.md`.
- For candidate FAQ, fault, SOP, pending, and index templates, read `references/templates.md`.
- For review status, confidence, closure, deduplication, and privacy rules, read `references/review-rules.md`.
- For personal/team target configuration and teammate usage examples, read `references/config.example.md`.
- For JSWO group-name parsing, run or inspect `scripts/parse_work_order_group.py`.
- For deterministic candidate keys, run or inspect `scripts/candidate_key.py`.
- For pre-write Base payload validation, run `scripts/validate_candidate_record.py`.
- For GitHub Markdown archive snapshots, run or inspect `scripts/archive_snapshot.py`.

## Configuration Needed

Before writing to Feishu, obtain or ask the user for these values:

- Source chat names or chat IDs.
- Target Feishu Wiki space or parent node for `候选知识碎片/待审核`.
- Shared candidate Base URL/token and table ID, such as `支持知识碎片候选池`.
- Run window, defaulting to today in Asia/Shanghai for daily automation.
- Optional GitHub archive root, defaulting to `knowledge-archive/` in the repository.
- Optional role mapping for support owners, department leaders, and product/service representatives.

If any target write location is missing, complete source analysis and output a dry-run report instead of guessing where to publish.

For team use, prefer a local config or environment variables instead of hardcoding internal Feishu URLs in a public repository. If a teammate asks `/飞书知识沉淀 获取今天我所有工单群内容并沉淀`, load the configured team target and write candidate documents plus one normalized record per case to the shared candidate Base table.

## Shared Candidate Base Schema

The shared candidate pool is a Feishu Base table, not a free-form index document. Every automation and manual run must write records using this exact field contract:

| Field | Type | Required behavior |
|---|---|---|
| 唯一键 | text | Stable dedupe key: `thread:<thread_id>`, `workorder:<JSWO-id>`, `node:<wiki_node_token>`, or fallback `hash:<sha1>`. |
| 日期 | text | Source date or creation date, `YYYY-MM-DD` when known; otherwise `待确认`. |
| 类型 | single select | One of `故障`, `FAQ`, `SOP`, `故障+FAQ`, `故障/SOP`, `待确认`. |
| 产品/模块 | text | Product, model, module, or subsystem. |
| 工单号 | text | JSWO or other work-order ID; leave blank if unavailable. |
| 来源 thread | text | Thread ID, message ID, source node token, or `待确认`. |
| 标题 | text | Candidate title. |
| 来源群/来源渠道 | text | Feishu group, private chat, topic group, Wiki candidate folder, or manual source. |
| 负责人/同事 | text | Primary support teammate or `待确认`; do not use this as the dedupe key. |
| 候选文档链接 | text | Feishu Wiki/Doc candidate link. |
| 成熟度 | single select | One of `M0 原始线索`, `M1 初步判断`, `M2 候选草稿`, `M3 已审核候选`, `M4 正式知识`, `待确认`. |
| 审核状态 | single select | One of `待审核`, `需补充`, `已通过`, `已发布`, `不沉淀`, `已废弃/重复`, `待确认`. |
| 审核人 | text | Reviewer name/open_id when known. |
| 发布目标 | text | Target official Wiki/category when approved, if known. |
| 公共文档链接 | text | Published/formal knowledge link after approval. |
| 最后更新时间 | text | `YYYY-MM-DD HH:mm` or a clear date note. |
| GitHub归档路径 | text | Snapshot path such as `knowledge-archive/.../v001.md`. |
| 备注/风险提示 | text | Missing evidence, migration notes, duplicate/obsolete explanation, or risk boundary. |

Create these status views when setting up a new Base table: `待审核`, `需补充`, `已通过待发布`, `已发布`, and `已废弃/重复`. Filter `已通过待发布` by `审核状态=已通过`; filter the others by the matching `审核状态` value.

### Base Write Invariants

These rules are hard gates for every Feishu write:

- `唯一键` is mandatory and must be non-empty. If the runner cannot derive `thread:<id>`, `workorder:<id>`, `node:<token>`, or `hash:<sha1>`, stop and return a dry-run error instead of writing a Base record.
- `来源 thread` is traceability metadata only. Never put a chat name/date such as `法国HMI群 | 2026-05-19` in `唯一键`; generate a fallback `hash:<sha1>` when no stable thread or work-order ID exists.
- When creating or updating a Base record, copy the same `candidate_key` into the candidate document body, GitHub archive frontmatter, and Base `唯一键` field. Do not let the report-only value diverge from the Feishu write payload.
- If an existing Base record has the same key, update that record and its canonical candidate page. Do not create a parallel record, and do not return a console-only update as success.
- If a record has `候选文档链接`, the linked candidate document is the canonical page unless a maintenance run marks it obsolete. Read it before deciding whether to update, skip, or repair.
- If a Base row is missing `唯一键` but has a candidate link/title/source, treat it as a repair target: derive the key, update the existing row, and update or split the linked candidate page before adding new rows.

## Capture Modes

### Maintenance Mode

Use maintenance mode when the user asks to clean the candidate pool, fix a wrong answer, merge duplicates, mark obsolete drafts, or repair the shared Base table. This mode maintains existing candidate knowledge; it does not collect new source chats by default.

Accept inputs such as:

```text
清理候选池里重复的 T300 网络域 FAQ
修正这个候选答案，并把重复文档标记废弃
检查支持知识碎片候选池里是否有重复候选
把同一 thread/workorder 的重复候选合并到一个主文档
```

For maintenance mode:

- Read the shared Base records and candidate pages before writing.
- Choose one canonical page per exact key (`thread:<id>` or `workorder:<JSWO-id>`).
- Correct the canonical page when the existing answer conflicts with newer evidence or human review.
- Mark duplicate or empty pages as obsolete with a link to the canonical page; do not delete them unless the user explicitly requests deletion.
- Update the shared Base record to point to the canonical page and record the correction/update time.
- If GitHub archive is enabled, create the next archive version for the corrected canonical candidate.
- Return a cleanup report listing canonical pages, obsolete pages, corrected facts, and any remaining possible duplicates.

### Single-Case Mode

Use single-case mode when the user pastes one customer case, one `supportman` output, one internal discussion, one final solution, or one work-order summary. This mode replaces the default recommendation to use `case-capture`.

Accept inputs such as:

```text
Use $feishu-knowledge-capture to turn this supportman output and final solution into a candidate knowledge draft.
使用 feishu-knowledge-capture，把下面这个已闭环案例沉淀成候选排障知识。
使用 feishu-knowledge-capture，把这个还没闭环的新产品问题放入 Pending 候选池。
```

For single-case mode:

- Do not fetch broad chat history unless the user provides a source link or explicitly asks.
- Normalize the pasted material into one case.
- If the input is a `supportman` output, parse its knowledge-capture section automatically instead of asking the user to fill a separate intake template.
- If final cause, solution, or verification is missing, generate a Pending record rather than a high-confidence FAQ/SOP.
- If the case is closed enough, generate one or more candidate drafts: FAQ, fault troubleshooting article, or SOP.
- Use `hash:<sha1(product|module|title|core_symptom)>` as the fallback candidate key when no thread ID or work-order ID exists.

### supportman Handoff Parsing

When the pasted material contains a `supportman` knowledge-capture decision, extract these fields when present:

```text
是否建议进入 feishu-knowledge-capture 候选池
- 判断：不沉淀 / 待闭环后沉淀 / 建议立即候选沉淀
- 理由：
- 建议沉淀类型：FAQ / SOP / 排障知识 / Pending
- 进入候选池前缺失：
```

Also accept English equivalents:

- `Not captured` -> `不沉淀`.
- `Capture after closure` -> `待闭环后沉淀`.
- `Candidate now` -> `建议立即候选沉淀`.

Map the decision to action:

- `不沉淀`: do not create a candidate page; include the case in the run report as skipped.
- `待闭环后沉淀`: create or update a Pending record with maturity `M0` or `M1`.
- `建议立即候选沉淀`: create or update a candidate FAQ, SOP, or fault/troubleshooting article with default maturity `M2`.

If the supportman output says `建议立即候选沉淀` but still lacks final cause, solution, or verification, prefer Pending or a low-confidence fault draft and clearly list missing evidence. Do not turn triage-only hypotheses into final knowledge.

### Batch Mode

Use batch mode for configured supportman topic groups, JSWO work-order groups, named chats, or broader Feishu scopes.

## Source Selection

### Default Automation

Daily automation should process only configured SupportMan/supportman related topic threads unless the automation prompt explicitly enables more sources. Treat `support-triage` as the legacy name for the same source family:

- messages containing `/supportman`
- legacy messages containing `/support-triage`
- messages mentioning Gin, SupportMan, supportman, or the legacy support-triage bot and asking for support handling
- bot replies produced by the SupportMan/supportman workflow
- threads in a group tagged or named `SupportMan`, `supportman`, or legacy `support-triage`

Treat one topic thread as one case. Do not turn each individual message into a separate candidate document.

### Manual Source Scopes

Manual invocations may request a wider scope. Support these source phrases:

```text
/飞书知识沉淀 获取今天 supportman 话题并沉淀
/飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
/飞书知识沉淀 获取昨天所有群聊中的技术支持问题并沉淀
/飞书知识沉淀 获取今天所有私聊中的工单问题并沉淀
/飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
```

Interpret the command into:

- Source scope: `supportman`, `jswo-groups`, `all-group-chats`, `all-private-chats`, or `named-chat`.
- Time window: today by default; also support yesterday, this week, and explicit date ranges.
- Output mode: default is Feishu candidate write plus GitHub archive; `dry-run` only reports.
- Target: configured candidate Wiki node and shared candidate Base table.

For `all-group-chats` and `all-private-chats`, first filter by technical-support signals such as `/supportman`, `/support-triage`, `SupportMan`, `supportman`, `JSWO-`, robot/product names, error/fault words, troubleshooting language, FAQ wording, pre-sales/Spark-plan wording, or configured keywords. Do not summarize unrelated chatter, administrative messages, or personal conversation.

### JSWO Work-Order Groups

Also support configured JSWO work-order groups when the user enables them. Recognize group names that contain a work-order ID such as `JSWO-202604220005`, for example:

```text
【新问题_进行中】PUDU T300法国JSWO-202604220005
【已解决】KettyBot法国JSWO-202604220006
```

Use `scripts/parse_work_order_group.py` to extract status, product/customer text, and work-order ID. The status text is a signal, not the final closure decision.

## Teammate Invocation

When a teammate uses this skill through a Feishu bot, support concise Chinese commands such as:

```text
@Pierre的飞书智能体 /飞书知识沉淀 获取今天我所有工单群内容并沉淀
@Pierre的飞书智能体 /飞书知识沉淀 获取本周 JSWO 工单群内容并沉淀
@Pierre的飞书智能体 /飞书知识沉淀 只处理已闭环工单
```

Interpret these as:

- Source owner: the invoking teammate unless specified otherwise.
- Source scope: all visible work-order groups for that teammate, especially groups whose names contain `JSWO-`.
- Target: the configured team candidate Wiki node and shared candidate Base table.
- Output policy: candidate drafts only, pending report for unresolved cases.

Do not write to another person's private candidate pool unless the configured target explicitly points there and the current identity has permission.

## Multi-User Work-Order Groups

Multiple teammates may run this skill in the same JSWO work-order group. Treat the work order, not the invoking person, as the deduplication unit:

- Use `workorder:<JSWO-id>` as the candidate key for JSWO groups.
- If A, B, and C run the skill on the same work order, create only one candidate page.
- If a later run adds a final cause, verified solution, product confirmation, or closure evidence, update the existing candidate and create the next GitHub archive version.
- If a later run has no material new information, skip writing and report `duplicate_skipped`.
- Record the trigger person and last updater for audit, but do not treat the trigger person as the work-order owner by default.

## Role Attribution

Record work-order responsibility by role:

- `技术支持负责人`: person mainly troubleshooting, replying to the customer, or driving the case.
- `部门 Leader`: technical support department leader in the group.
- `产品/中台服务代表`: product or middle-platform service representative for the involved product/service.
- `触发人`: person who invoked this skill for the current run.
- `贡献人`: people who provided final cause, solution, verification, customer confirmation, or other key evidence.
- `最后更新人`: person or bot identity that last updated the candidate.

Prefer explicit configuration or a local role mapping. If not available, infer roles from group membership and message behavior. If a role cannot be determined reliably, write `待确认` instead of guessing.

## Leader Pilot

For a department leader pilot, start with manual use before daily automation:

```text
@Leader的飞书智能体 /skill install https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
@Leader的飞书智能体 /skill update https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
@Leader的飞书智能体 使用 feishu-knowledge-capture，候选目录写入：https://www.feishu.cn/wiki/QiPGwE9Y4iukxfkMh8YcXPKNnBd ，统一候选 Base 写入：https://www.feishu.cn/base/YfRTb0oJUazkCAsL2jYcOCcRndh ，GitHub归档写入 Ginhy2026/support-ai-workflows 的 knowledge-archive。
@Leader的飞书智能体 /飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
@Leader的飞书智能体 /飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
```

After the manual run looks correct, daily automation may process the leader's visible JSWO groups and supportman topics at 18:30.

## Workflow

For maintenance mode, skip source chat collection and start from the shared Base/candidate pages. Follow `references/lark-workflow.md` and `references/review-rules.md` for canonical selection, correction, duplicate marking, and Base record repair.

1. Resolve source chats:
   - Use Feishu chat search when only names are known.
   - Prefer explicit `chat_id` when configured.
2. Fetch messages for the configured run window.
3. Filter sources:
   - First version: keep only supportman related messages and their threads.
   - Company extension: keep configured work-order groups that match JSWO or configured ticket patterns.
4. Expand each thread:
   - Collect root message, replies, visible text from screenshots/cards when available, bot answer, human follow-up, and closure evidence.
   - If image or card content cannot be read, record it as missing evidence.
   - Before summarizing a case, scan all collected text and readable image/card text for closure keywords such as `解决方案`, `解决版本`, `升级`, `固件`, `APK`, `版本`, `阈值`, `参数`, `已解决`, `fixed`, `workaround`, and `root cause`. Preserve exact versions, thresholds, measurements, and pass/fail criteria.
5. Normalize each case:
   - Source group, message IDs, thread ID, sender names, timestamps, product/module, customer/region, language, work-order ID, trigger person, support owner, department leader, product/service representative, contributors, and last updater when present.
6. Generate a deterministic candidate key:
   - supportman thread: `thread:<thread_id>`.
   - JSWO work-order group: `workorder:<JSWO-id>`.
   - Fallback when both are missing: `hash:<sha1(product|module|title|core_symptom)>`.
   - Use `scripts/candidate_key.py` for consistent key generation.
   - If the resulting key is blank or only repeats a source chat/date, stop the write and report `missing_candidate_key`.
7. Read the shared candidate Base before writing:
   - Search for the candidate key first.
   - If the key exists and there is no material new information, skip creating a new page and report `duplicate_skipped`.
   - If the key exists and there is new resolution, read the existing `候选文档链接`, update that existing candidate page with the latest full body plus an `更新记录` entry, then update the Base record/report instead of creating a new page.
   - If only a similar title/symptom exists but the key differs, do not auto-merge. Report `possible_duplicate` for human review.
   - Also search for blank-key records with the same title/source/candidate link. Repair the blank key and canonical link before inserting any new record.
8. Decide case state:
   - Closed enough for candidate knowledge: has final action, cause, workaround, verified result, customer confirmation, or explicit case closure.
   - Pending: still in troubleshooting, missing root cause, missing final answer, or only has first-pass triage.
9. Classify output:
   - Fault: abnormal robot behavior, error, failure, navigation issue, hardware/software/cloud fault, or troubleshooting case.
   - FAQ: recurring question, product difference, configuration, policy, usage, or short "how to" answer.
   - SOP: reusable internal handling procedure, escalation playbook, or multi-role workflow.
   - Pending: useful signal but not ready for candidate knowledge.
   - For single-case mode, this classification replaces the old separate `case-capture` flow.
10. Generate Markdown or XML using `references/templates.md`.
11. Write to Feishu:
   - Create one candidate document or Wiki node per eligible case.
   - Create or update one record in the shared candidate Base table, including the unique key.
   - Never overwrite formal knowledge pages.
   - After every create/update, read back the candidate page link and Base record. If the candidate page did not change, mark the result as `write_incomplete` instead of reporting success.
12. Archive to GitHub when enabled:
   - Save only the structured candidate Markdown and necessary metadata, not full raw chat logs.
   - New cases become `v001.md`; updated cases become `v002.md`, `v003.md`, and so on.
   - Store snapshots below `knowledge-archive/` following `references/templates.md`.
13. Return a daily report with collected message count, candidate documents, archive snapshots, pending cases, duplicate skips, possible duplicates, write links, and review tasks.

## Quality Rules

- Do not publish any output as formal knowledge. Always mark it as `候选草稿，需人工审核`.
- Do not invent final causes, solutions, verification results, or customer confirmations.
- Keep source traceability: include source chat, message ID, thread ID, date, and owner when available.
- Candidate pages must not collapse into only five short sections such as `故障现象/根因分析/状态/备注` unless the user explicitly asks for a brief note. Even concise candidates must include source traceability, evidence status, maturity, applicability, missing evidence, and update record.
- For each candidate, include a compact `来源证据索引` or `来源与可信度` section listing the source group/channel, thread or message IDs, message date/time when available, sender/role when safe, and whether each key source was text, screenshot, card, file, or reference document.
- If a source image/card may contain a root cause, solution, version, threshold, wiring, error screenshot, or troubleshooting step, read or OCR it before finalizing the candidate whenever tools allow. If it cannot be read, write `关键图片未读取` in the candidate and Base `备注/风险提示`, lower the maturity to `M0/M1` or Pending, and do not state that the root cause or solution is unknown merely because the text-only messages were incomplete.
- If a message says `具体操作见如下文档`, `参考文档`, `见链接`, `操作说明`, `SOP`, `手册`, or similar, treat the attached document card/link as key reference evidence. Preserve the title and URL in `参考资料` even if unread. If the card title is visible but the URL is not directly available, search by the exact title and record the matched URL or mark `链接待补充`.
- Do not write `详细操作文档待补充` when a source message already contains a document card or link. Instead write `参考文档已发现，读取状态：已读取/未读取`, then summarize only the parts that are readable.
- Preserve exact operational details from source evidence: firmware/APK versions, solve versions, thresholds, current/voltage/resistance values, percentages, port names, error codes, and date/time. Do not replace a concrete source statement such as `解决版本：0.4.18` with a generic phrase such as `后续版本修复`.
- Redact private customer details, phone numbers, personal names, and sensitive identifiers unless the target is explicitly internal and access-controlled.
- For all private-chat and broad all-chat scans, redact names, phone numbers, emails, private handles, and personal conversation by default.
- Prefer reusable patterns over one-off customer details.
- If source material is unresolved or incomplete, produce a pending record rather than a candidate knowledge draft.
- New products and new issues often start with immature material. This is normal; capture them as Pending or low-maturity candidates until final cause, solution, and verification become available.
- When content came from screenshots or cards, state whether the text was fully readable.
- Do not archive raw chat transcripts to GitHub. Archive only the generated candidate Markdown, source identifiers, Feishu links, and review metadata.
- Separate role ownership from invocation: `触发人` is audit metadata, while `技术支持负责人`, `部门 Leader`, and `产品/中台服务代表` describe the work-order roles.

## Output Report

Always end with a compact Markdown report:

```markdown
# 知识沉淀日报

## 1. 采集范围
- 来源群：
- 时间范围：
- 来源范围：supportman / JSWO工单群 / 所有群聊 / 所有私聊 / 指定群

## 2. 处理结果
- 读取消息：
- 识别 case：
- 生成候选故障：
- 生成候选 FAQ：
- 生成候选 SOP：
- 生成 Pending：
- 待补充/待闭环：
- 跳过：
- GitHub 归档：

## 3. 已写入候选 Base
| 唯一键 | 类型 | 标题 | 成熟度 | 审核状态 | 候选文档链接 | GitHub归档路径 |
|---|---|---|---|---|---|---|

## 4. 待补充
| 标题/线索 | 缺失信息 | 建议动作 |
|---|---|---|
```
