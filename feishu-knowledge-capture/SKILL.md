---
name: feishu-knowledge-capture
description: Capture support-triage Feishu topic threads, JSWO work-order groups, and manually requested Feishu chat scopes into candidate Feishu Wiki knowledge drafts and GitHub Markdown archives. Use when Codex needs to collect resolved support-triage cases, extract FAQ/fault/SOP knowledge from Feishu messages, run daily knowledge capture, process all visible group/private chats with safeguards, prepare a shared candidate knowledge pool, update a Feishu Wiki or index document, or archive candidate knowledge snapshots for version history.
---

# Feishu Knowledge Capture

## Purpose

Use this skill to turn Feishu support-triage threads, work-order group discussions, and explicitly requested chat scopes into candidate knowledge drafts for human review. It is the batch capture layer after `support-triage` and `case-capture`: collect source messages, group them into cases, classify whether they are suitable for knowledge capture, write candidate drafts to Feishu Wiki, update a shared index, and optionally archive Markdown snapshots to GitHub for version history.

The default automated source is the user's configured support-triage topic group. JSWO work-order groups and broad chat scopes are supported for manual or configured runs, but generated knowledge must still be treated as a candidate draft until reviewed.

## Load References

- For Feishu IM, Docs, Wiki, and index-update commands, read `references/lark-workflow.md`.
- For candidate FAQ, fault, SOP, pending, and index templates, read `references/templates.md`.
- For review status, confidence, closure, deduplication, and privacy rules, read `references/review-rules.md`.
- For personal/team target configuration and teammate usage examples, read `references/config.example.md`.
- For JSWO group-name parsing, run or inspect `scripts/parse_work_order_group.py`.
- For deterministic candidate keys, run or inspect `scripts/candidate_key.py`.
- For GitHub Markdown archive snapshots, run or inspect `scripts/archive_snapshot.py`.

## Configuration Needed

Before writing to Feishu, obtain or ask the user for these values:

- Source chat names or chat IDs.
- Target Feishu Wiki space or parent node for `候选知识碎片/待审核`.
- Shared index document URL or token, such as `支持知识碎片候选池`.
- Run window, defaulting to today in Asia/Shanghai for daily automation.
- Optional GitHub archive root, defaulting to `knowledge-archive/` in the repository.

If any target write location is missing, complete source analysis and output a dry-run report instead of guessing where to publish.

For team use, prefer a local config or environment variables instead of hardcoding internal Feishu URLs in a public repository. If a teammate asks `/飞书知识沉淀 获取今天我所有工单群内容并沉淀`, load the configured team target and write to the shared candidate pool.

## Source Selection

### Default Automation

Daily automation should process only configured support-triage related topic threads unless the automation prompt explicitly enables more sources:

- messages containing `/support-triage`
- messages mentioning Gin or the support-triage bot and asking for triage
- bot replies produced by the support-triage workflow
- threads in a group tagged or named `Support-triage`

Treat one topic thread as one case. Do not turn each individual message into a separate candidate document.

### Manual Source Scopes

Manual invocations may request a wider scope. Support these source phrases:

```text
/飞书知识沉淀 获取今天 support-triage 话题并沉淀
/飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
/飞书知识沉淀 获取昨天所有群聊中的技术支持问题并沉淀
/飞书知识沉淀 获取今天所有私聊中的工单问题并沉淀
/飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
```

Interpret the command into:

- Source scope: `support-triage`, `jswo-groups`, `all-group-chats`, `all-private-chats`, or `named-chat`.
- Time window: today by default; also support yesterday, this week, and explicit date ranges.
- Output mode: default is Feishu candidate write plus GitHub archive; `dry-run` only reports.
- Target: configured candidate Wiki node and shared index document.

For `all-group-chats` and `all-private-chats`, first filter by technical-support signals such as `/support-triage`, `JSWO-`, robot/product names, error/fault words, troubleshooting language, FAQ wording, or configured keywords. Do not summarize unrelated chatter, administrative messages, or personal conversation.

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
- Target: the configured team candidate Wiki node and shared index document.
- Output policy: candidate drafts only, pending report for unresolved cases.

Do not write to another person's private candidate pool unless the configured target explicitly points there and the current identity has permission.

## Workflow

1. Resolve source chats:
   - Use Feishu chat search when only names are known.
   - Prefer explicit `chat_id` when configured.
2. Fetch messages for the configured run window.
3. Filter sources:
   - First version: keep only support-triage related messages and their threads.
   - Company extension: keep configured work-order groups that match JSWO or configured ticket patterns.
4. Expand each thread:
   - Collect root message, replies, visible text from screenshots/cards when available, bot answer, human follow-up, and closure evidence.
   - If image or card content cannot be read, record it as missing evidence.
5. Normalize each case:
   - Source group, message IDs, thread ID, sender names, timestamps, product/module, customer/region, language, work-order ID when present.
6. Generate a deterministic candidate key:
   - Support-triage thread: `thread:<thread_id>`.
   - JSWO work-order group: `workorder:<JSWO-id>`.
   - Fallback when both are missing: `hash:<sha1(product|module|title|core_symptom)>`.
   - Use `scripts/candidate_key.py` for consistent key generation.
7. Read the shared index before writing:
   - Search for the candidate key first.
   - If the key exists and there is no material new information, skip creating a new page and report `duplicate_skipped`.
   - If the key exists and there is new resolution, append an `更新记录` section to the existing candidate page and update the index row/report instead of creating a new page.
   - If only a similar title/symptom exists but the key differs, do not auto-merge. Report `possible_duplicate` for human review.
8. Decide case state:
   - Closed enough for candidate knowledge: has final action, cause, workaround, verified result, customer confirmation, or explicit case closure.
   - Pending: still in troubleshooting, missing root cause, missing final answer, or only has first-pass triage.
9. Classify output:
   - Fault: abnormal robot behavior, error, failure, navigation issue, hardware/software/cloud fault, or troubleshooting case.
   - FAQ: recurring question, product difference, configuration, policy, usage, or short "how to" answer.
   - SOP: reusable internal handling procedure, escalation playbook, or multi-role workflow.
   - Pending: useful signal but not ready for candidate knowledge.
10. Generate Markdown or XML using `references/templates.md`.
11. Write to Feishu:
   - Create one candidate document or Wiki node per eligible case.
   - Append one row to the shared index document, including the unique key.
   - Never overwrite formal knowledge pages.
12. Archive to GitHub when enabled:
   - Save only the structured candidate Markdown and necessary metadata, not full raw chat logs.
   - New cases become `v001.md`; updated cases become `v002.md`, `v003.md`, and so on.
   - Store snapshots below `knowledge-archive/` following `references/templates.md`.
13. Return a daily report with collected message count, candidate documents, archive snapshots, pending cases, duplicate skips, possible duplicates, write links, and review tasks.

## Quality Rules

- Do not publish any output as formal knowledge. Always mark it as `候选草稿，需人工审核`.
- Do not invent final causes, solutions, verification results, or customer confirmations.
- Keep source traceability: include source chat, message ID, thread ID, date, and owner when available.
- Redact private customer details, phone numbers, personal names, and sensitive identifiers unless the target is explicitly internal and access-controlled.
- For all private-chat and broad all-chat scans, redact names, phone numbers, emails, private handles, and personal conversation by default.
- Prefer reusable patterns over one-off customer details.
- If source material is unresolved or incomplete, produce a pending record rather than a candidate knowledge draft.
- When content came from screenshots or cards, state whether the text was fully readable.
- Do not archive raw chat transcripts to GitHub. Archive only the generated candidate Markdown, source identifiers, Feishu links, and review metadata.

## Output Report

Always end with a compact Markdown report:

```markdown
# 知识沉淀日报

## 1. 采集范围
- 来源群：
- 时间范围：
- 来源范围：support-triage / JSWO工单群 / 所有群聊 / 所有私聊 / 指定群

## 2. 处理结果
- 读取消息：
- 识别 case：
- 生成候选故障：
- 生成候选 FAQ：
- 生成候选 SOP：
- 待补充/待闭环：
- 跳过：
- GitHub 归档：

## 3. 已写入候选区
| 类型 | 标题 | 工单号 | 来源 | 飞书链接 | GitHub 版本 | 审核状态 |
|---|---|---|---|---|---|---|

## 4. 待补充
| 标题/线索 | 缺失信息 | 建议动作 |
|---|---|---|
```
