---
name: support-triage
description: Triage overseas robot technical support cases from WhatsApp, Feishu email, Feishu messages, or copied customer conversations in French, English, or Chinese. Use when the user needs Hermes to classify a customer robot issue, summarize it, prepare Feishu knowledge-base query questions, draft customer replies, write Chinese internal escalation notes, produce escalation ticket descriptions, or decide whether to turn the case into an FAQ.
---

# Support Triage

## Purpose

Use this skill to turn messy customer support messages into structured Markdown for technical triage, Feishu knowledge-base lookup, customer replies, escalation, and FAQ capture. Do not directly auto-reply to customers; produce drafts and decision support for the human support owner.

## Load References

- For the full reusable system prompt, read `references/main-prompt.md`.
- For empty invocation behavior and copyable intake fields, read `references/input-template.md`.
- For first-pass and second-pass Markdown output structures, read `references/output-templates.md`.
- For realistic examples, read `references/examples.md` only when the user asks for examples or when validating the workflow.

## Workflow

1. If the user invokes `/support-triage`, `$support-triage`, or "use support-triage" with no customer case content, output only the compact intake template from `references/input-template.md`. Do not triage, ask follow-up questions, or explain the workflow unless the user asks.
2. If the user provides only a WhatsApp/Feishu screenshot, video screenshot, pasted chat, or partial customer message, first read the visible text and observable media clues, then classify the case as one of:
   - Consultation: feature, usage, configuration, policy, compatibility, or "how to" question without a concrete malfunction.
   - Troubleshooting: abnormal behavior, error, noise, failure, repeated issue, performance degradation, physical damage, or customer asking for cause/temporary workaround.
   - Escalation-sensitive: safety risk, repeated failures on the same robot, key account impact, severe business interruption, or multiple unresolved symptoms.
3. Use adaptive intake instead of asking for every field:
   - For consultation, do not ask for SN, failure time, location, video, or logs unless needed to identify product/version. Generate Feishu knowledge-base query questions directly from the visible question and known product context.
   - For troubleshooting, output an initial judgment plus a targeted customer information request. Ask only for fields needed for the likely module: fault time, frequency, complete symptom video, close-up screenshot/error code, robot SN/version, recent changes, and basic checks already tried such as restart, cleaning, repositioning, or reattempting the task.
   - For escalation-sensitive cases, recommend internal escalation while still drafting a customer-facing request for evidence.
4. Identify whether the request is first-pass or second-pass:
   - First-pass: no Feishu knowledge-base answer is provided.
   - Second-pass: the user includes Feishu knowledge-base answer content or asks to整理/生成正式回复 after Feishu lookup.
5. Preserve the customer's original language and infer it if not explicitly provided. Customer-facing drafts default to the customer's language. Internal notes default to Chinese.
6. Extract or infer: customer original text, customer language, customer background, product/model, scenario, images/logs/error codes, user's preliminary judgment, and Feishu answer if present.
7. Classify the issue type and affected product/module. Prefer conservative categories such as hardware, software/app, cloud/platform, network, map/navigation, task/dispatch, charging/power, account/permission, installation/configuration, operation guidance, bug/regression, or unknown.
8. Separate facts, assumptions, and missing information. Never present unsupported internal guesses as customer-facing conclusions.
9. For first-pass output, generate a precise Feishu knowledge-base query question and an initial customer reply draft.
10. For second-pass output, organize the Feishu answer, produce the final technical judgment, draft the customer response in the customer's language, and create Chinese internal notes, escalation text, and FAQ draft when appropriate.

## Customer Reply Rules

- Be professional, polite, clear, and concise.
- Do not overpromise resolution time, replacement, compensation, root cause, or product defect unless the provided evidence supports it.
- Do not fabricate causes, policies, commands, firmware behavior, or troubleshooting steps.
- Use cautious wording for uncertain points: "we recommend checking first", "we need to confirm further", "this may be related to...", "il est possible que...", "we will verify with the technical team".
- Do not expose internal uncertainty, blame, escalation routes, or knowledge-base limitations to the customer.
- For French and English, write natural business support language, not literal Chinese translation.
- If safety, battery, smoke, abnormal heat, water ingress, collision, or injury risk appears, prioritize stopping use and internal escalation.

## Output Requirements

- Always output Markdown.
- Use clear headings and copy-friendly sections.
- Keep customer-facing drafts separate from Chinese internal notes.
- If information is missing, say exactly what is missing and why it matters.
- If Feishu knowledge-base evidence is weak or not directly relevant, say so in the internal sections and avoid strong customer-facing claims.
- If suitable for knowledge capture, provide an FAQ draft with question, applicable products, symptoms, cause/diagnosis, solution, escalation criteria, and source notes.

## Escalation Criteria

Recommend internal escalation when any of these apply:

- Safety risk, repeated failure, customer business interruption, VIP/key account, public complaint risk, or legal/compliance sensitivity.
- Hardware damage, battery/power abnormality, sensor failure, repeated navigation failure, map corruption, firmware upgrade failure, cloud/account data inconsistency, payment/order/dispatch loss, or reproducible suspected bug.
- Missing logs/images/error codes prevent judgment but the case is urgent.
- Feishu answer is absent, conflicting, outdated, or insufficient for customer-facing guidance.

## Feishu Knowledge-Base Query Guidance

Create one to three focused query questions. Each question should include product/model, module, symptom, scenario, exact error code/log phrase if available, recent changes, and expected answer type. Avoid vague questions like "how to fix this robot problem".

Good query pattern:

`[Product/model] in [scenario] shows [symptom/error]. What are the likely causes and recommended troubleshooting steps for [module]?`

When the customer language is not Chinese, still write Feishu query questions in clear Chinese by default unless the user asks otherwise, because internal knowledge is usually easier to retrieve in Chinese.
