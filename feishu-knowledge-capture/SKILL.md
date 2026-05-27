---
name: feishu-knowledge-capture
description: Capture single support cases, support-triage outputs, Feishu topic threads, JSWO work-order groups, and manually requested Feishu chat scopes into candidate Feishu Wiki knowledge drafts and GitHub Markdown archives. Use when Codex needs to convert one resolved or pending support case into candidate FAQ/fault/SOP/Pending knowledge, collect support-triage cases in batch, extract reusable knowledge from Feishu messages, run daily knowledge capture, prepare a shared candidate knowledge pool, update a Feishu Wiki or index document, or archive candidate knowledge snapshots for version history.
---

# Feishu Knowledge Capture

## Purpose

Use this skill to turn one support case or many Feishu support discussions into candidate knowledge drafts for human review. It is the unified knowledge-capture layer after `support-triage`: collect source material, group it into cases, classify whether it is suitable for knowledge capture, write candidate drafts to Feishu Wiki, update a shared index, and optionally archive Markdown snapshots to GitHub for version history.

The default automated source is the user's configured support-triage topic group. Single-case manual capture, JSWO work-order groups, and broad chat scopes are supported for manual or configured runs, but generated knowledge must still be treated as a candidate draft until reviewed.

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
- Optional role mapping for support owners, department leaders, and product/service representatives.

If any target write location is missing, complete source analysis and output a dry-run report instead of guessing where to publish.

The configured candidate target must be the writable review area, usually the `待审核` child node under `候选知识碎片`. Never overwrite or append generated candidate/report content to the `候选知识碎片` root/landing page itself. If only a root/landing-page URL is provided, stop and output a dry-run report that asks for the `待审核` candidate node and shared index document.

The shared index update target must be a document URL or the underlying docx token accepted by `docs +fetch`/`docs +update`, not merely the Wiki node token that wraps that document. If both are available, keep both labels explicit: `index_doc_token` for Docs API writes and `index_wiki_node_token` for navigation.

When the candidate node and index document are configured, Feishu write preflight is mandatory before any archive-only fallback:

- Resolve or fetch the configured candidate node and verify that the current identity can access it, that its title is the review/candidate area, and that it is not the root/landing page.
- Fetch the shared index document through the Docs API using the document URL or `index_doc_token`, then search each candidate key before writing.
- If preflight succeeds, continue to Feishu candidate writes and index updates.
- If preflight fails, stop the Feishu write path and report the exact target, command, and error in a `dry-run` report. Local archive snapshots may be produced only as clearly labelled fallback evidence.
- Do not use vague reasons such as "permission not confirmed", "dedupe not confirmed", or "target status unclear" to silently skip Feishu writes. Those are tasks for the agent to verify with read-only preflight commands.

For team use, prefer a local config or environment variables instead of hardcoding internal Feishu URLs in a public repository. If a teammate asks `/飞书知识沉淀 获取今天我所有工单群内容并沉淀`, load the configured team target and write to the shared candidate pool.

## Capture Modes

### Maintenance Mode

Use maintenance mode when the user asks to clean the candidate pool, fix a wrong answer, merge duplicates, mark obsolete drafts, or repair the shared index. This mode maintains existing candidate knowledge; it does not collect new source chats by default.

Accept inputs such as:

```text
清理候选池里重复的 T300 网络域 FAQ
修正这个候选答案，并把重复文档标记废弃
检查支持知识碎片候选池里是否有重复候选
把同一 thread/workorder 的重复候选合并到一个主文档
```

For maintenance mode:

- Read the shared index and candidate pages before writing.
- Choose one canonical page per exact key (`thread:<id>` or `workorder:<JSWO-id>`).
- Correct the canonical page when the existing answer conflicts with newer evidence or human review.
- Mark duplicate or empty pages as obsolete with a link to the canonical page; do not delete them unless the user explicitly requests deletion.
- Update the shared index row to point to the canonical page and record the correction/update time.
- If GitHub archive is enabled, create the next archive version for the corrected canonical candidate.
- Return a cleanup report listing canonical pages, obsolete pages, corrected facts, and any remaining possible duplicates.

### Single-Case Mode

Use single-case mode when the user pastes one customer case, one `support-triage` output, one internal discussion, one final solution, or one work-order summary. This mode replaces the default recommendation to use `case-capture`.

Accept inputs such as:

```text
Use $feishu-knowledge-capture to turn this support-triage output and final solution into a candidate knowledge draft.
使用 feishu-knowledge-capture，把下面这个已闭环案例沉淀成候选排障知识。
使用 feishu-knowledge-capture，把这个还没闭环的新产品问题放入 Pending 候选池。
```

For single-case mode:

- Do not fetch broad chat history unless the user provides a source link or explicitly asks.
- Normalize the pasted material into one case.
- If the input is a `support-triage` output, parse its knowledge-capture section automatically instead of asking the user to fill a separate intake template.
- If final cause, solution, or verification is missing, generate a Pending record rather than a high-confidence FAQ/SOP.
- If the case is closed enough, generate one or more candidate drafts: FAQ, fault troubleshooting article, or SOP.
- Use `hash:<sha1(product|module|title|core_symptom)>` as the fallback candidate key when no thread ID or work-order ID exists.

### Support-Triage Handoff Parsing

When the pasted material contains a `support-triage` knowledge-capture decision, extract these fields when present:

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

If the support-triage output says `建议立即候选沉淀` but still lacks final cause, solution, or verification, prefer Pending or a low-confidence fault draft and clearly list missing evidence. Do not turn triage-only hypotheses into final knowledge.

### Batch Mode

Use batch mode for configured support-triage topic groups, JSWO work-order groups, named chats, or broader Feishu scopes.

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

When the user only scopes the run, for example "沉淀今天所有工单群" or "获取所有包含工单的群聊并沉淀", do not create a broad work-order summary report as the candidate content. Treat the command as a request to discover cases, group messages by work order or thread, classify each case, and write only case-level candidate FAQ/fault/SOP/Pending records. A compact run report is allowed at the end, but it is not a candidate knowledge page.

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
@Leader的飞书智能体 使用 feishu-knowledge-capture，候选目录写入：https://www.feishu.cn/wiki/QiPGwE9Y4iukxfkMh8YcXPKNnBd ，统一索引文档写入：https://www.feishu.cn/wiki/SarowXaTji5farkayOBcbYfqn2d ，GitHub归档写入 Ginhy2026/support-ai-workflows 的 knowledge-archive。
@Leader的飞书智能体 /飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
@Leader的飞书智能体 /飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
```

After the manual run looks correct, daily automation may process the leader's visible JSWO groups and support-triage topics at 18:30.

## Workflow

For maintenance mode, skip source chat collection and start from the shared index/candidate pages. Follow `references/lark-workflow.md` and `references/review-rules.md` for canonical selection, correction, duplicate marking, and index repair.

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
   - Source group, message IDs, thread ID, sender names, timestamps, product/module, customer/region, language, work-order ID, trigger person, support owner, department leader, product/service representative, contributors, and last updater when present.
   - For wide work-order scopes, split source material into one case per work-order ID, topic thread, or coherent issue. Never collapse many unrelated work orders into one candidate page.
6. Generate a deterministic candidate key:
   - Support-triage thread: `thread:<thread_id>`.
   - JSWO work-order group: `workorder:<JSWO-id>`.
   - Fallback when both are missing: `hash:<sha1(product|module|title|core_symptom)>`.
   - Use `scripts/candidate_key.py` for consistent key generation.
7. Preflight Feishu write targets:
   - Resolve the configured candidate Wiki node and reject root/landing-page targets before creating any document.
   - Fetch the shared index document through `docs +fetch` with the document URL or `index_doc_token`.
   - Search candidate keys in the index to prepare dedupe decisions.
   - If any configured target cannot be read or verified, return `dry-run` with the failed command/error. Do not silently create only local files.
8. Read the shared index before writing:
   - Search for the candidate key first.
   - If the key exists and there is no material new information, skip creating a new page and report `duplicate_skipped`.
   - If the key exists and there is new resolution, append an `更新记录` section to the existing candidate page and update the index row/report instead of creating a new page.
   - If only a similar title/symptom exists but the key differs, do not auto-merge. Report `possible_duplicate` for human review.
9. Decide case state:
   - Closed enough for candidate knowledge: has final action, cause, workaround, verified result, customer confirmation, or explicit case closure.
   - Pending: still in troubleshooting, missing root cause, missing final answer, or only has first-pass triage.
10. Classify output:
   - Fault: abnormal robot behavior, error, failure, navigation issue, hardware/software/cloud fault, or troubleshooting case.
   - FAQ: recurring question, product difference, configuration, policy, usage, or short "how to" answer.
   - SOP: reusable internal handling procedure, escalation playbook, or multi-role workflow.
   - Pending: useful signal but not ready for candidate knowledge.
   - For single-case mode, this classification replaces the old separate `case-capture` flow.
11. Generate Markdown or XML using `references/templates.md`.
12. Write to Feishu:
   - Create one candidate document or Wiki node per eligible case.
   - Append one row to the shared index document, including the unique key.
   - Never overwrite formal knowledge pages.
13. Archive to GitHub when enabled:
   - Archive is secondary evidence, not the primary write target.
   - Only claim `completed` when Feishu candidate pages and the shared index were created or updated.
   - If Feishu writes were skipped because preflight failed for permission, target validation, or deduplication checks, label the run `dry-run/archive-only` and list the failed command, target, and error.
   - Save only the structured candidate Markdown and necessary metadata, not full raw chat logs.
   - New cases become `v001.md`; updated cases become `v002.md`, `v003.md`, and so on.
   - Store snapshots below `knowledge-archive/` following `references/templates.md`.
14. Return a daily report with collected message count, candidate documents, archive snapshots, pending cases, duplicate skips, possible duplicates, write links, and review tasks.

## Quality Rules

- Do not publish any output as formal knowledge. Always mark it as `候选草稿，需人工审核`.
- Do not invent final causes, solutions, verification results, or customer confirmations.
- Keep source traceability: include source chat, message ID, thread ID, date, and owner when available.
- Redact private customer details, phone numbers, personal names, and sensitive identifiers unless the target is explicitly internal and access-controlled.
- For all private-chat and broad all-chat scans, redact names, phone numbers, emails, private handles, and personal conversation by default.
- Prefer reusable patterns over one-off customer details.
- Do not use a report title such as `工单总结报告`, `统计概览`, or `知识沉淀建议` as a candidate knowledge page unless the user explicitly asks for a report-only artifact. Candidate pages must be case-level FAQ/fault/SOP/Pending drafts with candidate keys, evidence, maturity, review status, and missing-information fields.
- If source material is unresolved or incomplete, produce a pending record rather than a candidate knowledge draft.
- New products and new issues often start with immature material. This is normal; capture them as Pending or low-maturity candidates until final cause, solution, and verification become available.
- When content came from screenshots or cards, state whether the text was fully readable.
- Do not archive raw chat transcripts to GitHub. Archive only the generated candidate Markdown, source identifiers, Feishu links, and review metadata.
- Do not report "沉淀完成" or "已归档至知识库" when only local Markdown files were created. Say "本地归档完成，飞书写入未执行" and include the missing permission/config/dedup step.
- If configured Feishu targets exist, the agent must try read-only target/index preflight before deciding that permission or dedupe is unavailable. A skipped write without attempted preflight is a skill execution error, not a successful archive-only run.
- Separate role ownership from invocation: `触发人` is audit metadata, while `技术支持负责人`, `部门 Leader`, and `产品/中台服务代表` describe the work-order roles.

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
- 生成 Pending：
- 待补充/待闭环：
- 跳过：
- GitHub 归档：
- 飞书写入状态：completed / partial / dry-run / archive-only
- Feishu preflight status：preflight_ok / preflight_failed / preflight_not_attempted
- Candidate 目标：
- Index doc token：

## 3. 已写入候选区
| 类型 | 标题 | 成熟度 | 工单号 | 来源 | 飞书链接 | GitHub 版本 | 审核状态 |
|---|---|---|---|---|---|---|---|

## 4. 待补充
| 标题/线索 | 缺失信息 | 建议动作 |
|---|---|---|
```
