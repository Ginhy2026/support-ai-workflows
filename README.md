# support-ai-workflows

Shared Hermes/Codex skills and workflows for AI-assisted technical support.

## Included Skills

### support-triage

`support-triage` helps overseas robot support teams process customer issues from WhatsApp, Feishu email, and Feishu messages. It supports first-pass triage, Feishu knowledge-base query generation, second-pass answer synthesis, customer reply drafts, internal escalation notes, and FAQ drafts.

Skill folder:

```text
support-triage/
```

### case-capture

`case-capture` converts customer issues, Feishu knowledge-base answers, internal discussions, troubleshooting notes, and final solutions into candidate FAQ or SOP drafts. It labels information confidence and whether the content is suitable for a formal knowledge base.

Skill folder:

```text
case-capture/
```

## Install

Copy the `support-triage` folder into your Hermes/Codex skills directory.

Typical Codex location:

```text
%USERPROFILE%\.codex\skills\support-triage
```

Then invoke it with:

```text
Use $support-triage to triage this customer robot issue.
```

For case capture:

```text
Use $case-capture to convert this resolved support case into a candidate FAQ or SOP draft.
```

Chinese example:

```text
请使用 $support-triage 处理下面这个客户机器人问题。
```

If you invoke it without case details, Hermes should return a compact intake form first:

```text
/support-triage
```

## Recommended Workflow

1. Paste the customer message and case background into Hermes.
2. Run `$support-triage` without Feishu knowledge-base results for first-pass triage.
3. Copy the generated Feishu knowledge-base query questions into Feishu.
4. Paste the Feishu answer back into Hermes.
5. Run `$support-triage` again to produce the formal customer reply, Chinese internal note, escalation ticket, and FAQ draft.

## Repository Layout

```text
.
├── README.md
├── case-capture/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── examples.md
│       ├── input-template.md
│       └── output-templates.md
└── support-triage/
    ├── SKILL.md
    ├── README.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── main-prompt.md
        ├── input-template.md
        ├── output-templates.md
        └── examples.md
```
