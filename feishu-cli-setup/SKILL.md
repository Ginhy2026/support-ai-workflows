---
name: feishu-cli-setup
description: Check and guide Feishu/Lark CLI setup for document and wiki search. Use when the user or another support skill needs to verify lark-cli installation, Feishu OAuth login, token validity, search:docs:read permission, or Feishu knowledge-base search readiness. This skill diagnoses and provides commands only; it must not automatically install software, modify system configuration, save credentials, or share App Secrets.
---

# Feishu CLI Setup

## Purpose

Use this skill to help a teammate prepare local `lark-cli` access for Feishu document and wiki search. It is a setup and diagnostics companion for `support-triage`; it does not perform customer support triage itself.

## Load References

- For the step-by-step readiness checklist, read `references/checklist.md`.
- For copyable commands, read `references/commands.md`.
- For common failure modes and remedies, read `references/troubleshooting.md`.

## Safety Rules

- Do not automatically install `lark-cli`, change shell policy, modify PATH, or edit system configuration.
- Do not ask users to paste App Secrets into chat.
- Prefer user OAuth login through `lark-cli auth login --domain search --recommend`.
- Use read-only checks only: version checks, auth status, scope checks, and search tests.
- If a command would require browser confirmation, tell the user what will happen and let them complete the browser authorization.
- If setup cannot be completed, provide manual fallback search queries for Feishu.

## Workflow

1. Check whether Node.js exists:
   - Run or instruct: `node --version`.
   - If missing, tell the user to install Node.js before installing `lark-cli`.
2. Check whether `lark-cli` exists:
   - Prefer `lark-cli --version`.
   - On Windows, if PowerShell blocks `lark-cli.ps1`, use `lark-cli.cmd --version`.
3. Check login state:
   - Run or instruct: `lark-cli auth status`.
   - Confirm identity is `user`, `tokenStatus` is `valid`, and scopes include `search:docs:read`.
4. Check search permission:
   - Run or instruct: `lark-cli auth check --scope "search:docs:read"`.
5. Run a test search:
   - Run or instruct: `lark-cli drive +search --query "CT4" --doc-types wiki,docx --page-size 10 --format json`.
   - Optionally test the repository wrapper: `python tools\feishu_search_docs.py "CT4" --type wiki --type docx --count 5`.
6. Output a fixed Markdown diagnostic report with current status, next steps, and acceptance commands.

## Output Format

Always output Markdown with these sections:

```markdown
# 飞书 CLI 检查报告

## 1. 当前状态
| 检查项 | 状态 | 说明 |
|---|---|---|
| Node.js | 通过 / 未通过 / 未检查 |  |
| lark-cli | 通过 / 未通过 / 未检查 |  |
| 飞书登录 | 通过 / 未通过 / 未检查 |  |
| token 有效性 | 通过 / 未通过 / 未检查 |  |
| search:docs:read 权限 | 通过 / 未通过 / 未检查 |  |
| 测试搜索 | 通过 / 未通过 / 未检查 |  |

## 2. 下一步操作
- 

## 3. 验收测试命令
```

Acceptance commands:

```powershell
lark-cli auth check --scope "search:docs:read"
lark-cli drive +search --query "CT4" --doc-types wiki,docx --page-size 10 --format json
python tools\feishu_search_docs.py "CT4" --type wiki --type docx --count 5
```

Continue the report with:

```markdown
## 4. support-triage 使用建议
- 如果检查通过：`support-triage` 可以优先使用飞书 CLI 搜索知识库。
- 如果检查未通过：`support-triage` 仍可输出建议检索词，由用户手动复制到飞书知识问答。
```

## Success Criteria

Setup is considered ready when all are true:

- `lark-cli auth status` shows a valid user token.
- `lark-cli auth check --scope "search:docs:read"` returns `ok: true`.
- `lark-cli drive +search --query "CT4" --doc-types wiki,docx --page-size 10 --format json` returns without permission errors.
- The repository wrapper `tools/feishu_search_docs.py` can return search results or a clean zero-result response.
