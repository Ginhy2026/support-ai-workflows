# Knowledge Sources

## Primary Feishu Knowledge Base

Use this PUDU Feishu knowledge-base page as the preferred internal reference source when the runtime environment has permission to access it:

```text
https://pudutech.feishu.cn/wiki/ZXWUw8OBniPEzqkYbymc2E6AnJe?from=from_copylink
```

## Access Rules

- If the page content is accessible in the current environment, use it to inform issue classification, possible causes, troubleshooting steps, escalation criteria, and customer reply drafts.
- If Feishu document search is available, search the knowledge base by product/model, module, symptom, error code, and customer phrases before drafting technical conclusions.
- If the page requires login or is not accessible, do not claim to have checked it.
- If inaccessible, ask the user to paste the relevant Feishu knowledge-base answer or search result into the case input.
- Treat copied Feishu knowledge-base content as internal reference material. Do not paste internal-only wording directly into customer replies.
- If the knowledge-base content conflicts with customer evidence, explain the mismatch in the internal section and keep the customer reply conservative.

## Search Utility

This repository includes helper scripts that use official Feishu Open APIs and read credentials only from environment variables:

```text
tools/feishu_read_wiki.py
tools/feishu_search_docs.py
```

Use `feishu_search_docs.py` when the user wants the agent to find relevant articles from symptoms. It wraps the official `lark-cli drive +search` command, which uses the Search v2 `doc_wiki/search` API and a user login token.

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
## 知识库参考
- 来源：PUDU 飞书知识库
- 与本案相关的内容：
- 仍需确认的点：
```

When the page is not accessible:

```markdown
## 知识库参考
- 状态：当前无法直接访问飞书知识库链接
- 建议：请将相关飞书知识问答结果或页面内容粘贴到输入中，以便进行二轮整理
```
