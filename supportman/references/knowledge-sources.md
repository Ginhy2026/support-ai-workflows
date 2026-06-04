# Knowledge Sources

## Primary Feishu Reference Scope

Use this PUDU Feishu knowledge-base page as the preferred formal internal reference source when the runtime environment has permission to access it:

```text
https://pudutech.feishu.cn/wiki/ZXWUw8OBniPEzqkYbymc2E6AnJe?from=from_copylink
```

Also search the broader Feishu scope that is visible to the current user when the case needs prior-case lookup or the primary page has no direct answer:

```text
All accessible knowledge bases:
https://pudutech.feishu.cn/wiki/?wiki_all_space_view_source=space_sidebar

User-visible cloud documents / shared drive:
https://pudutech.feishu.cn/drive/shared/

Relevant personal Feishu message history:
Search with user identity only when the runtime has permission and the case terms are specific enough.
```

These URLs are entry points, not proof that their contents were read. Treat them as search scopes. Only cite or rely on a specific wiki page, document, file, or message after its title and content/snippet are available in the current context.

## Source Search Order

1. User-provided pasted reference content or readable direct links that are explicitly relevant to the case.
2. Formal Feishu knowledge-base/wiki results, especially approved SOPs, official troubleshooting articles, and reviewed historical cases.
3. User-visible Feishu cloud documents and shared drive results, including docs, docx, sheets, files, and wiki-backed documents when their snippets or fetched content match the case.
4. Relevant personal Feishu message history, used only as historical case clues, owner/context discovery, or evidence that a similar issue was discussed before.
5. Customer evidence from screenshots, chats, attachments, error codes, logs, and videos.
6. The user's preliminary judgment.
7. Model inference, only as an internal hypothesis.

## Access Rules

- If the page content is accessible in the current environment, use it to inform issue classification, possible causes, troubleshooting steps, escalation criteria, and customer reply drafts.
- If Feishu document search is available, search across accessible wiki spaces, cloud documents, and shared-drive-visible documents by product/model, module, symptom, error code, customer phrases, and Chinese synonyms before drafting technical conclusions.
- If Feishu message search is available and relevant, search personal message history with specific query variants. Do not run broad searches over private chats when the case lacks enough specific terms.
- If any page, document, wiki space, shared-drive item, or chat result requires login or is not accessible, do not claim to have checked it.
- If inaccessible, ask the user to paste the relevant Feishu knowledge-base answer, document snippet, shared-drive result, or message search result into the case input.
- Treat copied Feishu knowledge-base content as internal reference material. Do not paste internal-only wording directly into customer replies.
- If the knowledge-base content conflicts with customer evidence, explain the mismatch in the internal section and keep the customer reply conservative.
- Treat personal chat records as private and low-maturity evidence. Do not expose private sender names, chat names, customer names, or internal discussion details in customer-facing replies.

## Feishu Source Types

| Source type | How to search or read | Evidence maturity | How to use |
|---|---|---|---|
| Formal wiki / knowledge base | `tools/feishu_search_docs.py` with `--type wiki`, or `lark-cli drive +search --as user --doc-types wiki`, then fetch readable documents | Usually `M3/M4` if approved | Use for troubleshooting steps and stronger internal judgment when applicability is high. |
| Cloud docs / shared drive | Search visible `docx`, `doc`, `wiki`, `sheet`, and `file` results through Drive search; inspect or fetch exact URLs before relying on them | Usually `M1-M4`, depending on author/review status | Use after rating applicability and maturity; do not assume shared-drive visibility means approved SOP status. |
| All wiki spaces | Use `lark-cli wiki +space-list --as user` only to orient available spaces; use Drive search for keyword retrieval across wiki content | Depends on each result | Prefer spaces that look official, product-owned, or support-owned; still rate each page individually. |
| Personal message history | Use `lark-cli im +messages-search --as user` with specific terms, sender/time filters when useful, then inspect returned message context | Usually `M0/M1` | Use to find prior owners, similar symptoms, links, or closure clues. Do not use as a customer-facing standard answer by itself. |

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

## Maturity And Applicability

Keep source maturity separate from case applicability:

### Source maturity

- `M0 原始线索`: raw customer message, screenshot, chat fragment, or unverified observation.
- `M1 初步判断`: triage analysis or discussion hypothesis without closure.
- `M2 候选草稿`: candidate FAQ/SOP/fault article with a handling path, but not reviewed or fully verified.
- `M3 已审核候选`: human-reviewed candidate suitable for internal reference, with scope or boundary notes.
- `M4 正式知识`: approved formal knowledge-base article, standard SOP, or official technical note.

### Case applicability

- `A3 直接适用`: model, module, symptom/error code, scenario, and steps match the current case.
- `A2 部分适用`: symptom or module is similar, but model/version/scenario differs.
- `A1 背景参考`: useful for mechanism/context only; not enough for customer-facing steps.
- `A0 不适用`: conflicts with the current case or key conditions do not match.

Use mature and applicable sources differently:

- `M3/M4 + A3`: may support clear troubleshooting steps and higher-confidence judgment.
- `M2 + A3` or `M3/M4 + A2`: may guide the response, but keep wording conservative and list mismatches.
- `M0/M1` or `A1/A0`: do not use as a standard answer; use only for low-risk checks, missing information, or escalation direction.

## No Mature Reference Behavior

If no directly relevant or mature reference is available:

- Do not write a long speculative root-cause section.
- Keep possible causes short and low-confidence, or omit them if they add no value.
- Provide only common, low-risk checks: confirm connections, clean accessible contacts, restart, confirm versions, retry the task, collect complete video, screenshot error codes, and gather logs/SN.
- Generate high-quality Feishu search questions and ask the user to paste any matching result for second-pass processing.
- If the case may recur, recommend `待闭环后沉淀` and explain what final cause, solution, and verification would be needed before later knowledge capture.

## Search Utility

This repository includes helper scripts that use official Feishu Open APIs and read credentials only from environment variables:

```text
tools/feishu_read_wiki.py
tools/feishu_search_docs.py
```

Use `feishu_search_docs.py` when the user wants the agent to find relevant articles from symptoms. It wraps the official `lark-cli drive +search` command, which uses the Search v2 `doc_wiki/search` API and a user login token. This search can cover user-visible wiki pages, cloud documents, and shared-drive-visible resources when the selected document types include them.

For troubleshooting cases, run or propose several query variants instead of only one. Combine:

- Product/model: `CC1`, `CC1 Pro`, module name.
- Symptom: visible issue, abnormal behavior, exact customer phrase.
- Error code: `1003`, log text, screen prompt.
- Chinese synonyms: `移动水站`, `移动水箱`, `对接底座`, `指示灯蓝色`, `不变绿`, `无法检测储水器`.
- Expected answer type: `排查步骤`, `SOP`, `故障案例`, `解决方案`.

```powershell
python tools\feishu_search_docs.py "CC1 清洁机器人 异常噪音" --type wiki --type docx --type doc
python tools\feishu_search_docs.py "CC1 清洁机器人 异常噪音 SOP 故障案例" --type wiki --type docx --type doc --type file
```

To search broader user-visible cloud documents and shared-drive-visible items directly:

```powershell
lark-cli drive +search --as user --query "CC1 异常噪音 SOP 故障案例" --doc-types wiki,docx,doc,file,sheet --page-size 10 --format json
```

To orient all accessible wiki spaces before deciding where a result belongs:

```powershell
lark-cli wiki +space-list --as user --page-all --format json
```

To search personal Feishu message history for prior-case clues, use user identity and narrow terms:

```powershell
lark-cli im +messages-search --as user --query "CC1 异常噪音" --page-size 10 --format json
lark-cli im +messages-search --as user --query "CC1 噪音 清洁模块" --page-size 10 --format json
```

Personal message search should be targeted. Prefer exact product/model, symptom, error code, customer phrase, country/customer alias, or teammate keyword. If the query returns a likely prior case, inspect only the relevant message context and any linked document before using it.

If search is not authenticated or search fails during `supportman`, call `$feishu-cli-setup` to diagnose the local CLI. The setup skill will check Node.js, `lark-cli`, login state, token validity, `search:docs:read`, and a test search. For message-history search, also check whether `search:message` is authorized.

Manual commands:

```powershell
lark-cli auth login --domain search --recommend
lark-cli auth check --scope "search:docs:read"
lark-cli auth check --scope "search:message"
```

Direct CLI example:

```powershell
lark-cli drive +search --as user --query "CC1 异常噪音" --doc-types wiki,docx --page-size 10 --format json
```

If document/wiki search returns `No permission`, the Feishu app or current user token likely needs `search:docs:read`, then the app must be republished/approved and the user must log in again. If message search fails, the current user token or app scopes may not allow cross-chat message search. If setup cannot be completed, keep the normal fallback: output exact search queries for the user to copy into Feishu knowledge search, cloud document search, shared drive search, or Feishu message search manually.

## Broad Search Query Plan

For a normal troubleshooting first pass, run or propose at least these query groups:

1. Formal knowledge/wiki: product + module + symptom/error + `SOP` / `故障案例` / `排查步骤`.
2. Cloud documents/shared drive: product + symptom + scenario + likely component names.
3. Personal chat history: product + exact error/customer phrase, then product + Chinese synonym, limited to the most specific terms.
4. Direct links supplied by the user: inspect or fetch the exact URL before relying on it.

For pre-sales or scenario consultation, replace error terms with capability, limitation, configuration, scenario, region, and product-version terms.

For Spark-plan/星火计划 or new-product issues, broaden beyond SOP terms and search for project names, prototype names, scenario names, internal owner names supplied by the user, and similar feature keywords.

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
