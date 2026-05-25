---
name: case-capture
description: Legacy optional helper for converting resolved or partially resolved robot support cases into structured candidate FAQ or SOP drafts. Prefer feishu-knowledge-capture for the main workflow because it supports single-case capture, batch Feishu capture, candidate pools, deduplication, maturity labels, and GitHub archives. Use this legacy skill only when the user explicitly asks for case-capture or needs a local Markdown-only draft.
---

# Case Capture

## Purpose

Use this legacy optional skill to transform support case material into a structured candidate FAQ or SOP draft. The output is for human review before entering any official knowledge base.

For the normal support workflow, prefer `support-triage` for current-case handling and `feishu-knowledge-capture` for single-case or batch knowledge capture. Do not treat `case-capture` as the default handoff path.

## Load References

- For copyable input fields, read `references/input-template.md`.
- For FAQ and SOP output structures, read `references/output-templates.md`.
- For a realistic example, read `references/examples.md` only when the user asks for an example or when validating the workflow.

## Workflow

1. Collect and normalize available source material:
   - customer issue or original message
   - product/model and module
   - Feishu knowledge-base answer
   - internal discussion or escalation notes
   - troubleshooting steps tried
   - final solution or current workaround
   - customer-facing reply
   - evidence such as logs, screenshots, videos, error codes, SN/version, or service records
2. Decide draft type:
   - FAQ: use for recurring questions, symptoms, known fixes, customer-facing support guidance, and short troubleshooting articles.
   - SOP: use for operational procedures, multi-step internal handling, escalation playbooks, installation/configuration processes, or cases requiring role ownership.
   - FAQ + SOP: use when the case needs both a customer-facing article and an internal handling procedure.
3. Do not directly publish or mark as formal knowledge. Always label the output as a candidate draft.
4. Separate facts, verified conclusions, assumptions, and missing information.
5. Mark information confidence for each important claim:
   - Verified: supported by final solution, reproduced result, official documentation, logs, or explicit technical confirmation.
   - Needs confirmation: plausible and supported by partial evidence, but not yet confirmed by final test or official source.
   - Preliminary judgment only: inferred from symptoms or discussion with weak evidence.
6. Include the required content:
   - fault symptom
   - applicable models/products/modules
   - cause or possible causes
   - troubleshooting steps
   - solution or workaround
   - customer reply template
   - internal notes
   - knowledge-base suitability
7. If source material is incomplete, produce a usable draft anyway and clearly list missing fields and review tasks.
8. Output Markdown only, optimized for copying into Feishu Docs, Yuque, GitHub, or a knowledge-base review workflow.

## Quality Rules

- Do not invent final causes or solutions.
- Do not convert uncertain internal discussion into verified knowledge.
- Do not expose internal blame, private customer details, phone numbers, personal names, or sensitive identifiers unless the user explicitly needs them for an internal draft.
- Prefer generic case patterns over one-off customer details when drafting FAQ/SOP content.
- Make customer-facing templates polite, conservative, and free of unsupported claims.
- Keep internal notes explicit about risks, prerequisites, rollback, and escalation criteria.
- If a case is too specific, stale, unresolved, or based only on speculation, mark it as not suitable for the formal knowledge base yet.

## Knowledge-Base Suitability

Recommend entry into a formal knowledge base only when most of these are true:

- The symptom is likely to recur for other customers or support teams.
- The applicable model/module is clear.
- The solution or workaround has been verified.
- The steps are reusable and not tied to one customer's private environment.
- The risk of misuse is low, or the SOP includes clear escalation limits.

Use these labels:

- Suitable: ready for review and likely worth publishing after human approval.
- Conditionally suitable: useful, but needs missing evidence, version scope, screenshots, or technical confirmation.
- Not suitable yet: unresolved, one-off, too speculative, or missing a verified solution.
