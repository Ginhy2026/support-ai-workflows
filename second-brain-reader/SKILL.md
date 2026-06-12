---
name: second-brain-reader
description: Read and answer from an approved, AI-readable GitHub publication of an Obsidian second brain. Use directly or as SupportMan's formal personal-knowledge channel when handling work, answering “according to my second brain”, finding relevant SOPs/checklists/cases, citing repository paths, identifying knowledge gaps, or assessing draft/review/stale/conflicted knowledge without reading or modifying the full Obsidian source vault.
---

# Second Brain Reader

Use only the configured AI publication repository. Treat it as read-only generated knowledge.

## Configuration

Obtain the approved repository from configuration or the user:

```text
SECOND_BRAIN_AI_REPO=<owner/repository>
```

For this user's current setup, the approved repository is:

```text
Ginhy2026/second-brain-ai-knowledge
```

Never substitute the full Obsidian source repository or candidate intake repository.

## Read Workflow

1. Verify that the configured repository is accessible.
2. Read `AGENTS.md`.
3. Read `.ai/manifest.json` or `AI_INDEX.md`.
4. Select only notes relevant to the question; do not scan or summarize the whole repository by default.
5. Read the selected note bodies before relying on them.
6. Cite every repository-backed conclusion with actual file paths.

If repository search is available, search titles, tags, domain, type, and likely Chinese/English synonyms. Confirm matches by reading the exact files.

## Trust Rules

- Prefer `active` over `review` or `draft`.
- Prefer `verified`, then `derived`, then `draft`.
- Warn when knowledge is review, draft, derived, stale, conflicted, or overdue.
- Treat missing linked files as unavailable.
- Show contradictions instead of silently choosing one.
- Never claim to have read a path whose contents were not retrieved.

## Answer Contract

Separate repository-backed knowledge from general reasoning:

```markdown
## 结论

## 第二大脑依据

## 风险与信息缺口

## 下一步建议

## 参考知识
- `actual/repository/path.md`
```

When the repository lacks sufficient evidence, say:

```text
当前第二大脑中没有足够依据。
```

Then ask focused questions or propose a knowledge candidate.

## SupportMan Handoff

When called during a SupportMan workflow, return a compact retrieval result that SupportMan can combine with Feishu and current-case evidence:

```markdown
## 第二大脑检索结果
- 实际读取路径：
- 可用结论：
- 状态与风险：
- 与当前问题的匹配度：
- 知识缺口或冲突：
```

Report a gap or conflict as feedback only. SupportMan decides whether to suggest preservation; `feishu-knowledge-capture` creates a pending candidate only after user confirmation.

## Write Boundary

- Never modify the AI publication repository.
- Never request or access the full Obsidian source repository for normal retrieval.
- Never promote a candidate into formal knowledge.
- When new knowledge or a correction appears, use the separate candidate-submission workflow or return a dry-run candidate.
- Do not claim “长期知识已更新” after merely proposing a candidate.

Read `references/verification.md` when configuring access or validating a new agent connection.
