---
name: feishu-knowledge-capture
description: Capture personally selected Feishu support material, visible work-order groups, and pasted case summaries into high-quality personal case notes, with an optional lightweight personal index. Use when Codex needs to help an individual turn support discussions into reusable case documents without scanning company-wide chats or maintaining a company candidate-pool console.
---

# Feishu Knowledge Capture

## Purpose

Use this skill to help one person actively preserve useful support knowledge from material they can see or provide. The default output is one concrete case note under the user's personal Feishu document group or Wiki parent, plus an optional lightweight personal index entry.

This is not a company-wide chat crawler, formal knowledge publisher, or management console. The skill should prioritize the quality, evidence, and future usefulness of each case document. The index is only a finding and status aid.

## Composing With Other Skills

This skill stays focused on Feishu knowledge capture. If another support workflow such as `supportman` has already produced a useful case summary, paste or link that output as source material and extract only the facts, evidence, final solution, current state, and missing information needed for the personal case note.

## Load References

- For Feishu IM, Docs, Wiki, and personal-index commands, read `references/lark-workflow.md`.
- For personal case note and lightweight index templates, read `references/templates.md`.
- For review status, confidence, closure, deduplication, and privacy rules, read `references/review-rules.md`.
- For personal target configuration and usage examples, read `references/config.example.md`.
- For JSWO group-name parsing, run or inspect `scripts/parse_work_order_group.py`.
- For deterministic case keys, run or inspect `scripts/candidate_key.py`.
- For GitHub Markdown archive snapshots, run or inspect `scripts/archive_snapshot.py` when archive output is enabled.

## Configuration Needed

Before writing to Feishu, obtain or ask the user for these values:

- Source material: pasted case text, selected chat names/IDs, selected work-order groups, or explicit message/thread links.
- Target personal Feishu document group, Wiki parent node, or folder for case notes.
- Optional personal index document URL/token.
- Time window, defaulting to today in Asia/Shanghai when the user does not specify one.
- Optional GitHub archive root, defaulting to `knowledge-archive/` in the repository.

If the personal write target is missing, complete source analysis and output a dry-run case note instead of guessing where to publish.

## Output Model

Default structure:

- One long-lived personal document group or Wiki parent.
- One case note document per useful case.
- One optional personal index list with only these fields: `关键词`, `类型`, `模块`, `标题`, `来源`, `文档链接`, `状态`.

Recommended status values:

- `待整理`: useful signal identified but not enough context yet.
- `已沉淀`: case note created with enough source traceability.
- `需补充`: important evidence, cause, solution, or verification is missing.
- `可复用`: the note is clean enough for future reuse or manual submission.
- `已废弃`: duplicate, obsolete, or no longer useful.

## Capture Modes

### Single-Case Mode

Use single-case mode when the user pastes one customer case, one internal discussion, one final solution, one work-order summary, or a summary produced by another workflow.

Accept inputs such as:

```text
使用 feishu-knowledge-capture，把下面这段案例摘要沉淀成个人 case 文档。
使用 feishu-knowledge-capture，把下面这个已闭环案例整理成个人排障沉淀。
使用 feishu-knowledge-capture，把这个还没闭环的新产品问题放入个人 Pending 线索。
```

For single-case mode:

- Do not fetch broad chat history unless the user provides a source link or explicitly asks.
- Normalize the pasted material into one case.
- If final cause, solution, or verification is missing, generate a Pending/线索 note rather than a high-confidence FAQ/SOP.
- If the case is closed enough, generate one personal case note that can contain FAQ, fault, and SOP sections as needed.
- Use `hash:<sha1(product|module|title|core_symptom)>` as the fallback case key when no thread ID or work-order ID exists.

### Selected Chat Mode

Use selected chat mode when the user names one or more Feishu groups/chats or work-order groups.

Accept inputs such as:

```text
/飞书知识沉淀 获取今天群聊「xxx」里的关键信息并沉淀
/飞书知识沉淀 获取本周这些群聊：A、B、C，整理成个人 case 文档
/飞书知识沉淀 获取昨天 JSWO-202604220005 工单群内容并沉淀
```

Interpret the command into:

- Source scope: explicitly named chats, explicit chat IDs, explicit message/thread links, or visible work-order groups requested by the user.
- Time window: user-specified first; default to today when omitted.
- Output mode: personal case documents plus optional personal index update; `dry-run` reports only when targets are missing.
- Target: configured personal document group/Wiki parent and optional personal index.

### Personal Visible Group Mode

Use this only when the user explicitly asks to process their own visible groups, such as `获取我可见的工单群`.

Rules:

- Process only the current identity's visible chats.
- Prefer configured keywords, explicit group names, or ticket patterns such as `JSWO-`.
- Do not claim access to all company chats or other people's private conversations.
- Filter by technical-support signals before case extraction.
- Redact unrelated personal conversation and administrative chatter.

## Source Handling

### Time Window

- If the user says today, yesterday, this week, a date, or a time range, use that exact window.
- If the user omits the window, default to today in Asia/Shanghai.
- If a case crosses the window boundary, include enough nearby thread context to make the case understandable when tools allow.

### Case Grouping

Treat one topic thread, one work-order group issue, or one coherent pasted problem as one case. Do not turn each message into a separate document.

For work-order groups, recognize names that contain IDs such as `JSWO-202604220005`, and use `scripts/parse_work_order_group.py` for metadata. The group status text is only a hint; closure depends on message evidence.

### Evidence Quality

Before writing a personal case note:

- Preserve source group/chat, message IDs or thread IDs, time range, participants when useful, and readable cards/images/files.
- Extract exact versions, thresholds, error codes, logs, robot models, country/region, and configuration values.
- If a screenshot, file, or card appears to contain key diagnosis or solution but cannot be read, mark it as unread evidence and lower confidence.
- Prefer human-written final solutions and verified steps over model-generated summaries.
- Keep customer-facing wording separate from internal facts when both are present.

## Personal Index

The personal index is intentionally lightweight. It is not an audit console.

Append or update one row per case note:

| 关键词 | 类型 | 模块 | 标题 | 来源 | 文档链接 | 状态 |
|---|---|---|---|---|---|---|

Field guidance:

- `关键词`: 3-8 searchable words, including product/model, symptom, error code, scenario, or customer region.
- `类型`: `故障`, `FAQ`, `SOP`, `故障+FAQ`, `线索/Pending`, or `其他`.
- `模块`: product, subsystem, service, feature, or `待确认`.
- `标题`: concise case title.
- `来源`: source chat/group, work-order ID, thread/message ID, and time window when available.
- `文档链接`: personal case note link.
- `状态`: one of `待整理`, `已沉淀`, `需补充`, `可复用`, `已废弃`.

## Deduplication

Use a stable key to avoid writing the same case repeatedly:

- `thread:<thread_id>` for a Feishu thread.
- `workorder:<JSWO-id>` for a work-order group.
- `node:<wiki_node_token>` for a source document node.
- `hash:<sha1(product|module|title|core_symptom)>` when no stable source ID exists.

If an existing personal case note has the same key, update that note only when new material information appears. If only a similar title exists but the key differs, report a possible duplicate for the user to decide.

## Writing Rules

- Create or update one personal case note per eligible case.
- Update the personal index only after the case note link is known.
- Never publish a personal note as formal company knowledge.
- Do not write to another person's private document area unless the configured target explicitly points there and the current identity has permission.
- Do not store raw full chat transcripts in GitHub archives. Archive only generated case Markdown, source identifiers, Feishu links, status, and minimal metadata.
- If write targets are missing or permissions fail, return a dry-run case note and a short configuration checklist.

## Report Format

Always end with a compact Markdown report:

```markdown
# 个人知识沉淀运行报告

- 运行时间：
- 来源范围：
- 时间范围：
- 个人文档组：
- 个人索引清单：

## 结果
| 指标 | 数量 |
|---|---:|
| 读取消息 |  |
| 识别 case |  |
| 新建 case 文档 |  |
| 更新 case 文档 |  |
| Pending/需补充 |  |
| 跳过重复 |  |

## 已沉淀
| 关键词 | 类型 | 模块 | 标题 | 来源 | 文档链接 | 状态 |
|---|---|---|---|---|---|---|

## 需补充
| 标题 | 来源 | 缺失信息 | 建议下一步 |
|---|---|---|---|
```
