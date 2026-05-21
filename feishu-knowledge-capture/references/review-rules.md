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

Before writing a new candidate, compare against the shared index and obvious title/work-order matches.

Duplicate signals:

- Same work-order ID.
- Same source thread ID.
- Same product/module and highly similar symptom.
- Same FAQ question with equivalent answer.

If duplicate content exists, update the index/report with "possible duplicate" instead of creating another candidate page unless the user explicitly asks for a new page.

## Privacy and Safety

- Redact personal phone numbers, email addresses, private chat handles, and personal names unless internal traceability requires them.
- Prefer customer/region and work-order ID over private person names.
- Do not expose internal blame or unsupported defect claims.
- Keep source message IDs and links in internal sections only.

## Publishing Boundary

This skill only creates candidate drafts. Do not move pages into a formal Wiki category, remove the candidate warning, or mark content as approved unless a human reviewer explicitly says it has been approved.
