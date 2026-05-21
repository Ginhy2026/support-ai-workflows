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

## Privacy and Safety

- Redact personal phone numbers, email addresses, private chat handles, and personal names unless internal traceability requires them.
- Prefer customer/region and work-order ID over private person names.
- Do not expose internal blame or unsupported defect claims.
- Keep source message IDs and links in internal sections only.

## Publishing Boundary

This skill only creates candidate drafts. Do not move pages into a formal Wiki category, remove the candidate warning, or mark content as approved unless a human reviewer explicitly says it has been approved.
