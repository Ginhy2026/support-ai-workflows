# Knowledge Sources

## Primary Feishu Knowledge Base

Use this PUDU Feishu knowledge-base page as the preferred internal reference source when the runtime environment has permission to access it:

```text
https://pudutech.feishu.cn/wiki/ZXWUw8OBniPEzqkYbymc2E6AnJe?from=from_copylink
```

## Access Rules

- If the page content is accessible in the current environment, use it to inform issue classification, possible causes, troubleshooting steps, escalation criteria, and customer reply drafts.
- If Feishu document search is available, search the knowledge base by product/model, module, symptom, error code, customer phrases, and Chinese synonyms before drafting technical conclusions.
- If the page requires login or is not accessible, do not claim to have checked it.
- If inaccessible, ask the user to paste the relevant Feishu knowledge-base answer or search result into the case input.
- Treat copied Feishu knowledge-base content as internal reference material. Do not paste internal-only wording directly into customer replies.
- If the knowledge-base content conflicts with customer evidence, explain the mismatch in the internal section and keep the customer reply conservative.

## Supplemental References

The user may provide SOPs, Yuque articles, Feishu docs, GitHub Markdown, web pages, or pasted article text. Use them as supplemental evidence when the Feishu knowledge base is incomplete or when the user explicitly says the document is relevant.

- If the current environment can read the link, extract the title, applicable product/model, symptom/error code, troubleshooting steps, solution, and warnings.
- If the link cannot be read, ask the user to paste the article body or key paragraphs. Do not infer steps or root cause from an unread link.
- Supplemental references improve troubleshooting steps and customer replies, but they do not override customer evidence.
- Do not expose internal article titles, historical customer names, or internal-only notes in customer-facing replies unless the user explicitly asks and it is appropriate to share.

## Applicability Rating

Rate every search result or supplemental source before using it:

| Rating | Use it when | Output behavior |
|---|---|---|
| Directly relevant | Model, module, symptom/error code, scenario, and troubleshooting steps match the case. | Use it for executable steps and concise technical judgment. |
| Partially relevant | Some symptoms, module, or scenario match, but key details differ. | Mention the matching and non-matching points internally; use conservative customer wording. |
| Background only | It explains the module or general principle but lacks case-level steps. | Use only for context; do not turn it into a root cause. |
| Not applicable | Product, symptom, module, or scenario conflicts with the case. | Do not use it for conclusions. |

Prefer references with explicit applicable model, exact symptom or error code, repeatable troubleshooting steps, verified historical cases, or official SOP status.

## No Mature Reference Behavior

If no directly relevant or mature reference is available:

- Do not write a long speculative root-cause section.
- Keep possible causes short and low-confidence, or omit them if they add no value.
- Provide only common, low-risk checks: confirm connections, clean accessible contacts, restart, confirm versions, retry the task, collect complete video, screenshot error codes, and gather logs/SN.
- Generate high-quality Feishu search questions and ask the user to paste any matching result for second-pass processing.

## Search Utility

This repository includes helper scripts that use official Feishu Open APIs and read credentials only from environment variables:

```text
tools/feishu_read_wiki.py
tools/feishu_search_docs.py
```

Use `feishu_search_docs.py` when the user wants the agent to find relevant articles from symptoms. It wraps the official `lark-cli drive +search` command, which uses the Search v2 `doc_wiki/search` API and a user login token.

For troubleshooting cases, run or propose several query variants instead of only one. Combine:

- Product/model: `CC1`, `CC1 Pro`, module name.
- Symptom: visible issue, abnormal behavior, exact customer phrase.
- Error code: `1003`, log text, screen prompt.
- Chinese synonyms: `移动水站`, `移动水箱`, `对接底座`, `指示灯蓝色`, `不变绿`, `无法检测储水器`.
- Expected answer type: `排查步骤`, `SOP`, `故障案例`, `解决方案`.

```powershell
python tools\feishu_search_docs.py "CC1 清洁机器人 异常噪音" --type docx --type doc
```

If search is not authenticated or search fails during `support-triage`, call `$feishu-cli-setup` to diagnose the local CLI. The setup skill will check Node.js, `lark-cli`, login state, token validity, `search:docs:read`, and a test search.

Manual commands:

```powershell
lark-cli auth login --domain search --recommend
lark-cli auth check --scope "search:docs:read"
```

Direct CLI example:

```powershell
lark-cli drive +search --query "CC1 异常噪音" --doc-types wiki,docx --page-size 10 --format json
```

If the API returns `No permission`, the Feishu app or current user token likely needs `search:docs:read`, then the app must be republished/approved and the user must log in again. If setup cannot be completed, keep the normal fallback: output exact search queries for the user to copy into Feishu knowledge search manually.

## How To Reference It In Output

When the knowledge-base content is available:

```markdown
## 资料检索结果与适用性判断
| 来源 | 适用性 | 可用结论/步骤 | 不能直接套用或仍需确认 |
|---|---|---|---|
| PUDU 飞书知识库 / SOP / 补充链接 | 直接相关 / 部分相关 / 仅背景参考 / 不适用 |  |  |
```

When the page is not accessible:

```markdown
## 知识库参考
- 状态：当前无法直接访问飞书知识库链接
- 建议：请将相关飞书知识问答结果或页面内容粘贴到输入中，以便进行二轮整理
```
