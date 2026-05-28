# Review Rules

These rules keep personal case notes useful, traceable, and honest about uncertainty.

## Closure and Confidence

Treat a case as ready for a reusable personal note only when at least one strong signal exists:

- A final cause, workaround, configuration, or handling path is stated by a human.
- The customer, support owner, product/service colleague, or source discussion confirms the issue was resolved.
- A referenced SOP/manual clearly applies to the current case.
- The case is not fully solved but contains a reusable signal worth keeping as Pending/线索.

Weak signals are not enough by themselves:

- A first-pass model answer only asks for more information.
- A screenshot or log is present but not readable.
- The group name says solved, but the message content does not show what solved it.
- A hypothesis is repeated without verification.

## Personal Status

Use status values to describe the personal note state:

- `待整理`: material was found but not yet turned into a complete note.
- `已沉淀`: a traceable case note exists.
- `需补充`: key evidence, cause, solution, or verification is missing.
- `可复用`: the note is clear enough for future reuse or manual submission.
- `已废弃`: duplicate, obsolete, or no longer useful.

Pending is required when the case is valuable but not closed enough for a stable FAQ/SOP/fault note. Clearly state why it cannot yet become stable knowledge.

## Deduplication

Before writing a new personal case note, compare deterministic keys first:

- `thread:<thread_id>` for a Feishu thread.
- `workorder:<JSWO-id>` for a work-order group.
- `node:<wiki_node_token>` for a source document node.
- `hash:<sha1(product|module|title|core_symptom)>` when no stable source ID exists.

Duplicate signals:

- Exact key exists + no new material information: skip writing and report `duplicate_skipped`.
- Exact key exists + new final cause, solution, verification, customer confirmation, or better evidence: update the existing case note and add `更新记录`.
- Similar title/symptom but different key: report `possible_duplicate`; do not merge automatically.
- No matching key: create a new personal case note and optional index row.

## Evidence Priority

Use this source priority when evidence conflicts:

1. Human-written final solution, verified troubleshooting manual, or reviewer correction.
2. Source Feishu messages and thread replies.
3. Readable screenshots, cards, logs, and files.
4. Formal or candidate reference documents.
5. Model-generated summary.

When a human final answer and a model summary disagree, prefer the human final answer and record the discrepancy in `判断过程` or `更新记录`.

## Reference Handling

When a case cites Feishu, Yuque, GitHub, web pages, SOPs, official manuals, or other reference documents:

- Record the reference title, URL, source type, read status, and why it was used.
- If the content is not readable, preserve the title/link and mark `读取状态：未读取`.
- If readable, extract only the key conclusion, steps, warnings, scope, and version boundaries needed for the current case.
- Do not copy an entire mature article into the case note.

## Privacy and Scope

- Process only material the current user provides or can see with their current Feishu identity.
- Do not claim access to company-wide chats or other people's private conversations.
- Redact private names, phone numbers, emails, chat handles, and unrelated conversation when they are not needed for technical traceability.
- Keep source traceability through group name, work-order ID, thread/message ID, and time range rather than raw full chat transcripts.

## Writing Boundaries

- This skill creates personal case notes, not formal company knowledge.
- Do not mark content as approved, published, or submitted unless the user explicitly says that happened.
- Do not implement automatic Spark-plan submission in this skill.
- Do not store raw full chat transcripts in GitHub archives.
