# Second-Brain Closed Loop

Use this contract whenever SupportMan handles PUDU work.

## Roles

| Component | Owns | Must not do |
|---|---|---|
| `supportman` | Handle current work, coordinate retrieval, draft replies, detect reusable feedback | Write formal knowledge or claim a candidate was saved |
| `second-brain-reader` | Read approved second-brain knowledge with paths and maturity warnings | Write back or promote knowledge |
| `feishu-knowledge-capture` | Turn user-approved feedback into a pending candidate | Modify formal knowledge |
| Codex + `obsidian-zhishi` | Review, promote, maintain, and publish formal knowledge | Promote without user review |

## Default Retrieval

For a PUDU support, pre-sales, project, or product question, SupportMan should naturally use both channels when available:

1. Search focused, relevant Feishu knowledge bases, documents, shared-drive items, and prior-message clues.
2. Query the approved second brain through `second-brain-reader`.
3. Read the exact matched sources before relying on them.
4. Report actual coverage and access failures.

Never describe keyword search as “searched everything I can see.” Never treat a missing second-brain result as proof that Feishu has no answer.

## Evidence Labels

- `正式飞书资料`: current company reference; still check applicability.
- `第二大脑正式知识`: reviewed personal knowledge; preserve status/confidence warnings.
- `历史线索`: message or prior-case clue; not a rule by itself.
- `客户事实`: current-case evidence.
- `内部推测`: model or human hypothesis; not customer-facing fact.

## Feedback Trigger

Produce a feedback handoff when at least one is true:

- a reusable solution or decision was verified;
- the user corrected a translation, rule, or response;
- current evidence contradicts or limits existing knowledge;
- repeated work exposed a missing checklist, FAQ, SOP, or boundary;
- the second brain had no answer for a question likely to recur.

Do not recommend capture for routine one-off work with no reusable learning.

## Compact Feedback Handoff

Keep this short enough to pass directly to `feishu-knowledge-capture`:

```markdown
## 第二大脑反馈建议
- 判断：不沉淀 / 待闭环后沉淀 / 建议创建候选
- 反馈类型：新知识 / 纠正 / 冲突 / 知识缺口 / 真实结果反馈
- 可复用结论：
- 来源与证据：
- 与现有知识的关系：
- 适用范围与例外：
- 仍需验证：
- 建议产物：FAQ / SOP / checklist / case / rule update / knowledge-gap
```

When the judgment is `建议创建候选`, ask:

```text
这次处理已经有可复用结论，要不要整理成第二大脑待审核候选？
```

When it is `待闭环后沉淀`, say what result or evidence should trigger a later capture. When the user agrees, invoke or hand off to `feishu-knowledge-capture`; do not expand the candidate inside SupportMan.
