# Review Rules

## Closure Signals

Treat a case as closed enough for candidate knowledge only when at least one strong signal exists:

- A final cause, fix, workaround, or recommended handling is explicitly stated.
- A customer, service owner, or technical owner confirms the result.
- The work order is closed, solved, verified, or moved out of active troubleshooting.
- The support-triage second-pass output includes a final technical judgment and a reusable FAQ draft.

Weak signals are not enough by themselves:

- The group name says `进行中`.
- A first-pass support-triage answer only asks for more information.
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

## Deduplication

Before writing a new candidate, read the shared index and compare deterministic keys first. This is mandatory for every run, including manual reruns and scheduled automations.

### Candidate Key

Use exactly one of these keys:

- `thread:<thread_id>` for support-triage topic threads.
- `workorder:<JSWO-id>` for JSWO work-order groups.
- `hash:<sha1>` only when no thread ID or work-order ID exists.

For fallback hashes, normalize the concatenation of product, module, title, and core symptom. Use lowercase ASCII where possible, trim whitespace, collapse repeated spaces, and compute SHA-1.

Use `scripts/candidate_key.py` when available instead of hand-building keys.

Duplicate signals:

- Same work-order ID.
- Same source thread ID.
- Same product/module and highly similar symptom.
- Same FAQ question with equivalent answer.

### Write Decision

- Exact key exists + no material new information: skip creating a page and report `duplicate_skipped`.
- Exact key exists + new final cause, solution, verification, or customer confirmation: update the existing candidate page by appending `更新记录`, then update/report the existing index entry.
- Different key + very similar title/symptom: do not merge automatically. Report `possible_duplicate` with both links/titles for human review.
- No matching key: create a new candidate page and append a new index row.

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

Do not update the candidate as a final answer when the new material is only a screenshot, progress reminder, repeated question, unsupported hypothesis, or personal conversation.

For every new or updated candidate, also create a GitHub Markdown snapshot when archive output is enabled:

- New candidate: `v001.md`.
- Updated candidate: next version such as `v002.md`.
- The Feishu candidate page keeps only the latest content plus a compact `更新记录`.
- GitHub is the source for full Markdown version history and diff review.

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
