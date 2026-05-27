# Review Rules

## Closure Signals

Treat a case as closed enough for candidate knowledge only when at least one strong signal exists:

- A final cause, fix, workaround, or recommended handling is explicitly stated.
- A customer, service owner, or technical owner confirms the result.
- The work order is closed, solved, verified, or moved out of active troubleshooting.
- The supportman second-pass output includes a final technical judgment, reusable troubleshooting steps, or a clear recommendation to enter the candidate pool.

Weak signals are not enough by themselves:

- The group name says `进行中`.
- A first-pass supportman answer only asks for more information.
- The discussion contains hypotheses but no final action.
- A screenshot shows an error, but no diagnosis or result is available.

## Suitability Labels

- `适合`: reusable symptom/question, clear scope, verified answer or fix, low risk of misuse.
- `条件适合`: useful but missing version scope, image evidence, confirmation, or reviewer approval.
- `暂不适合`: unresolved, one-off, speculative, sensitive, or missing final solution.

## Confidence Labels

- `已验证`: supported by final solution, official documentation, logs, reproduced result, or explicit technical confirmation.
- `待确认`: plausible and partly supported, but not validated by final result or official source.
- `仅初步判断`: inferred from symptoms or discussion with weak evidence.

## Maturity Labels

Use maturity labels to describe how reusable the candidate knowledge is. Maturity is about the knowledge item itself, not whether it applies to a future case.

- `M0 原始线索`: raw customer message, screenshot, work-order fragment, or unverified observation.
- `M1 初步判断`: supportman output or internal hypothesis, but no closure.
- `M2 候选草稿`: candidate FAQ/fault/SOP/Pending with a handling path, but not reviewed or fully verified.
- `M3 已审核候选`: human-reviewed candidate that can be used internally, with scope and boundary notes.
- `M4 正式知识`: approved official FAQ/SOP/fault article in the formal knowledge base.

Default maturity:

- Pending records are usually `M0` or `M1`.
- Newly generated candidate drafts are usually `M2`.
- Do not mark `M3` or `M4` unless a human reviewer explicitly approves it or the source is already formal knowledge.

## Applicability Labels

Use applicability labels to describe whether a source or prior candidate can be used for the current case:

- `A3 直接适用`: product/model, module, symptom/error code, scenario, and steps match.
- `A2 部分适用`: symptom or module is similar, but product/version/scenario differs.
- `A1 背景参考`: useful context only; not enough for operational or customer-facing steps.
- `A0 不适用`: conflicts with the case or key conditions do not match.

When writing a candidate, include known applicability boundaries and non-applicable scenarios. A high-maturity source can still be only `A2` or `A1` for a specific case.

## Candidate Type Quality Gates

FAQ is suitable when one question maps to one high-confidence standard answer with clear scope, non-applicable scenarios, and low risk of misuse.

SOP is suitable when the procedure is complete from trigger to closure, with roles, steps, expected results, exception branches, and escalation conditions.

Fault/troubleshooting knowledge is suitable when the symptom, troubleshooting logic, final cause or cause range, solution, and verification result are clear.

Pending is required when the case is valuable but not closed enough for a candidate FAQ/SOP/fault article.

If unread images, cards, or files may contain the final diagnosis, solution, solve version, thresholds, wiring, or error evidence, the case is not closed enough for a confident candidate. Keep it Pending or low-confidence until that media is read, and explicitly list the unread evidence.

## supportman Decision Mapping

When ingesting a `supportman` output, normalize its knowledge-capture decision before writing anything.

Accepted labels:

- `不沉淀` or `Not captured`
- `待闭环后沉淀` or `Capture after closure`
- `建议立即候选沉淀` or `Candidate now`

Action mapping:

| supportman decision | Feishu capture action | Default maturity |
|---|---|---|
| 不沉淀 / Not captured | Do not create a candidate page; report skipped with reason. | none |
| 待闭环后沉淀 / Capture after closure | Create or update Pending only. | M0 原始线索 or M1 初步判断 |
| 建议立即候选沉淀 / Candidate now | Create or update FAQ, SOP, or fault/troubleshooting candidate according to the suggested type and evidence. | M2 候选草稿 |

The `supportman` decision is an input signal, not proof of closure. If final cause, solution, verification, or scope is still missing, keep the output as Pending or low-confidence candidate content and list the missing evidence.

## Deduplication

Before writing a new candidate, read the shared candidate Base table and compare deterministic keys first. This is mandatory for every run, including manual reruns and scheduled automations.

### Candidate Key

Use exactly one of these keys:

- `thread:<thread_id>` for supportman topic threads.
- `workorder:<JSWO-id>` for JSWO work-order groups.
- `hash:<sha1>` only when no thread ID or work-order ID exists.

For fallback hashes, normalize the concatenation of product, module, title, and core symptom. Use lowercase ASCII where possible, trim whitespace, collapse repeated spaces, and compute SHA-1.

Use `scripts/candidate_key.py` when available instead of hand-building keys.

The key cannot be blank. It also cannot be a source label, date label, person name, or title slug unless it is wrapped as a fallback `hash:<sha1>`. If the source only provides a chat/date label, generate the fallback hash from the normalized case fields and keep the chat/date in `来源 thread` or `来源群/来源渠道`.

Older rows may contain non-prefixed title-slug keys from early runs. Treat those as legacy identifiers for matching and repair only; do not create new legacy keys. When the source thread/work-order/wiki node can be recovered, migrate the row to the prefixed key during maintenance.

Duplicate signals:

- Same work-order ID.
- Same source thread ID.
- Same product/module and highly similar symptom.
- Same FAQ question with equivalent answer.

### Write Decision

- Exact key exists + no material new information: skip creating a page and report `duplicate_skipped`.
- Exact key exists + new final cause, solution, verification, or customer confirmation: update the existing candidate page linked by `候选文档链接` with the latest candidate body and append `更新记录`, then update/report the existing Base record.
- Different key + very similar title/symptom: do not merge automatically. Report `possible_duplicate` with both links/titles for human review.
- No matching key: create a new candidate page and create a new Base record.
- Blank-key row + matching title/source/candidate link: repair that row by filling `唯一键`, updating the linked candidate page, and adding the archive path. Do not create a new row until the blank-key row is resolved or marked obsolete.

Never create a second candidate page for the same exact key unless the user explicitly asks for a new page.

### Multi-User Runs

When several teammates run the skill on the same JSWO work-order group, the work order remains the deduplication unit:

- Same `workorder:<JSWO-id>` means same candidate, regardless of whether A, B, C, a leader, or a service representative triggered the run.
- Trigger person changes are not material knowledge updates by themselves.
- If a later trigger contributes final cause, solution, verification, product confirmation, or closure evidence, update the existing page and create the next GitHub archive version.
- If no material new information exists, skip writing and report `duplicate_skipped`.

## Update and Versioning

When a candidate already exists, update the existing Feishu page only when new material information appears:

- Final cause, verified solution, workaround, rollback path, or customer confirmation.
- Work-order closure or explicit movement out of active troubleshooting.
- Evidence that changes the recommended answer, risk, applicable scope, or escalation condition.
- Maturity change, such as Pending becoming candidate draft, candidate draft being reviewed, or reviewed content becoming formal knowledge.

Do not update the candidate as a final answer when the new material is only a screenshot, progress reminder, repeated question, unsupported hypothesis, or personal conversation.

For every new or updated candidate, also create a GitHub Markdown snapshot when archive output is enabled:

- New candidate: `v001.md`.
- Updated candidate: next version such as `v002.md`.
- The Feishu candidate page keeps only the latest content plus a compact `更新记录`.
- GitHub is the source for full Markdown version history and diff review.

The Feishu candidate page, Base record, GitHub archive, and final run report must describe the same version. If only the console/run report or GitHub archive was updated, call it `write_incomplete`; do not claim the candidate document was updated.

## Human-Curated Final Answers

When the source contains a human-curated final answer, troubleshooting manual, numbered SOP, customer-ready reply, or reviewer correction, treat it as the primary source of truth for the candidate body.

- Preserve explicit numbered steps, measurement values, thresholds, pass/fail criteria, warnings, and customer reply wording unless they conflict with safety or privacy rules.
- Do not replace a concrete manual with a generic summary such as "replace module" or "check connection" when the source provides step-by-step diagnostics.
- If supportman output, knowledge-base search results, and a human final answer disagree, prefer the human final answer and record the discrepancy in `更新记录` or `内部注意事项`.
- If a value is operationally important, such as resistance, voltage, port, error code, or firmware version, copy it exactly and include units and tolerance where provided.
- Treat readable screenshots and cards containing labels such as `根因分析`, `解决方案`, `解决版本`, or `已解决` as human-curated final-answer evidence. Preserve their exact root-cause text, solve version, thresholds, and configuration values unless later evidence contradicts them.
- If the final answer is customer-facing but the candidate is internal, keep both: a reusable internal SOP section and a customer reply template section.
- When the manual is incomplete, keep the known steps and mark missing evidence explicitly instead of inventing the rest of the procedure.

## Reference Documents and Media

When a case cites Feishu, Yuque, GitHub, web pages, SOPs, official manuals, or other reference documents, preserve traceability in the candidate output.

- Always keep the original reference link in a `参考资料` section, even when key content is quoted or summarized elsewhere.
- Record the reference title, URL, maturity (`M0`-`M4`), applicability (`A0`-`A3`), whether the link was readable, and why it was used.
- A document card shared next to a solution message is evidence. If the message wording indicates that the document contains the operation method or final answer, the candidate must include the card title/link and read status; missing access should lower confidence, not erase the reference.
- If the link cannot be read, do not infer technical content from the title. Mark it as `未读取` and ask for pasted content or key paragraphs when needed.
- If the reference is readable, extract only the key conclusion, steps, warnings, scope, and version boundaries needed for the current case. Do not copy an entire mature article into a candidate.
- If the reference contains critical images, screenshots, tables, wiring diagrams, measurement diagrams, error screenshots, or port tables, attach the relevant media when the runtime can download or insert it.
- If media cannot be downloaded or inserted because of permission, tool, or format limits, keep the reference link and state where the image/table appears, such as `图片未复制，仅可从原文查看：第 3 节接线图`.
- Do not move all images by default. Only copy media that directly supports diagnosis, troubleshooting steps, customer reply, or review evidence.

### Mature Reference Decision Table

| Reference maturity and applicability | Default action |
|---|---|
| `M4 正式知识` + `A3 直接适用` | Do not create a duplicate long-form candidate. Create/update only an index or case-application record that links to the formal knowledge and explains why it applies. |
| `M4 正式知识` + new boundary, exception, customer wording, or local workaround | Create a supplemental candidate focused only on the new value, and cite the formal knowledge as the authority. |
| `M3 已审核候选` + `A3 直接适用` | Prefer updating/reusing the existing candidate or recording reuse. Do not duplicate content into a new page. |
| `M2` or lower | Candidate capture is allowed, but mark reference maturity, applicability, missing evidence, and review status. |

Content priority:

1. Human-curated final manual or final customer reply.
2. Mature formal reference document.
3. `supportman` output.
4. Similar historical case.
5. Model-generated summary.

If a mature document fully covers the issue, the candidate should summarize the current case fit: why the document applies, applicable conditions, differences, follow-up actions, and the link to the source. Do not duplicate the formal article body.

## Maintenance and Correction

Use maintenance rules when the user asks to clean an existing candidate pool, fix a wrong answer, merge duplicate candidates, or repair Base records.

- Exact same key (`thread:<id>` or `workorder:<JSWO-id>`): keep one canonical candidate page and mark all other pages as obsolete duplicates.
- Same title/question but different key: do not merge automatically. Report `possible_duplicate` unless a human reviewer confirms they are the same knowledge item.
- Wrong or misleading answer: correct the canonical page, add a compact update record, and update the shared Base record title/status if needed.
- Empty or partial page for an existing key: mark obsolete and link to the canonical page.
- Obsolete pages should be overwritten or prefixed with a clear notice such as `已废弃：重复候选，请以主文档为准`; do not delete pages unless explicitly requested.
- The Base table should point only to the canonical page for an exact key. If older records remain, mark them obsolete with `审核状态=已废弃/重复` or replace them with the canonical record.
- Corrections based on human review are material updates and should generate the next GitHub archive version when archive output is enabled.

## Role Attribution

Use role fields for traceability, but do not invent responsibility.

- `技术支持负责人`: person driving troubleshooting or customer response.
- `部门 Leader`: configured support leader or clearly identified leader in the group.
- `产品/中台服务代表`: product or middle-platform representative for the involved product/service.
- `触发人`: person who invoked the skill in this run.
- `贡献人`: people who added final cause, solution, verification, customer confirmation, or other key evidence.
- `最后更新人`: person or bot identity that updated the candidate.

Prefer explicit role maps or source-system metadata. Message behavior is a fallback signal. If evidence is insufficient, write `待确认`.

## Privacy and Safety

- Redact personal phone numbers, email addresses, private chat handles, and personal names unless internal traceability requires them.
- Prefer customer/region and work-order ID over private person names.
- Do not expose internal blame or unsupported defect claims.
- Keep source message IDs and links in internal sections only.
- For `all-group-chats`, keep only technical-support, fault, FAQ, SOP, robot/product, or work-order related content. Ignore casual, administrative, meeting, HR, and sales-only chatter.
- For `all-private-chats`, redact private names, phone numbers, emails, chat handles, personal comments, and unrelated conversation by default. Use source type and stable message IDs for traceability instead of full personal details.
- Do not write raw full chat transcripts to GitHub. Archive only generated candidate Markdown, source identifiers, Feishu links, review status, and other minimal metadata.

## Publishing Boundary

This skill only creates candidate drafts. Do not move pages into a formal Wiki category, remove the candidate warning, or mark content as approved unless a human reviewer explicitly says it has been approved.
