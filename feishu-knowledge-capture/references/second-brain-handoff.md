# Second-Brain Handoff

Use this flow when the user wants a Feishu case, translation correction, support lesson, or work insight to become part of their Obsidian second brain.

## Role Boundary

This skill is a candidate submitter, not the formal Obsidian writer.

The allowed direction is:

```text
Feishu source
  -> dedicated GitHub intake repository / knowledge-intake/feishu/
  -> local review and promotion
  -> Obsidian formal knowledge
  -> generated AI publication repository
  -> Feishu agent reads
```

Never treat the Obsidian source repository or generated AI publication repository as an intake target.

## Candidate-Only Write Contract

When GitHub intake is explicitly enabled:

- Create one new Markdown file under `knowledge-intake/feishu/`.
- Use a unique file name such as `YYYY-MM-DD-topic-<short-key>.md`.
- Never overwrite, rename, move, or delete an existing file.
- Never edit formal notes, entry pages, README files, system files, or `.obsidian`.
- Set `candidate_status: pending`.
- Do not set `status: active` or `confidence: verified`.
- Preserve a traceable Feishu source link or source identifier.
- Include only the minimum evidence needed; do not archive full chat transcripts.
- Re-read the committed file and verify that no path outside the intake directory changed.
- Run `scripts/validate_second_brain_handoff.py` against the before/after commits. Report success only when it passes.
- Report “已创建待审核候选” only after verification.

## Candidate Template

```markdown
---
type: knowledge-candidate
candidate_status: pending
domain: pudu_robotics
candidate_kind: case
source: "<Feishu message, document, meeting, or work-order link/ID>"
captured_at: YYYY-MM-DD
sensitivity: internal
suggested_output: case
target_note: ""
---

# 候选：<主题>

## 候选结论

## 为什么值得沉淀

## 来源与证据

## 与现有知识的关系

## 适用范围与例外

## 建议产物

## 待确认问题
```

For a translation correction, also record:

- source text;
- previous translation;
- corrected translation;
- correction reason;
- product, language, and scenario;
- known exceptions;
- whether the correction was confirmed by a reviewer or official source.

## Review Cadence

- Submit candidates whenever useful work happens.
- Let the user review and promote candidates weekly.
- Mark urgent confirmed errors as `priority: urgent`, but still do not edit formal knowledge.

## Failure Behavior

If the configured GitHub target is the Obsidian source repository, the AI publication repository, or cannot be verified:

1. refuse the GitHub write;
2. return the candidate Markdown as a dry-run;
3. explain that a dedicated intake repository or Feishu candidate queue is required.

## Deterministic Verification

After creating a commit, run:

```text
python scripts/validate_second_brain_handoff.py <repository> --base <commit-before-write> --head <commit-after-write>
```

The verifier passes only when:

- at least one Markdown file was added;
- every changed path is a new file under `knowledge-intake/feishu/`;
- every file declares `type: knowledge-candidate`;
- every file declares `candidate_status: pending`;
- no file declares `status: active` or `confidence: verified`;
- no likely credential pattern is present.

If verification fails, do not claim that a candidate was successfully created.
