# support-triage Skill 使用文档 v1.1

本文档用于帮助海外技术支持同事在 Hermes / 飞书智能体中安装和使用 `support-triage` skill，并说明如何配合 `feishu-cli-setup` 打通飞书知识库检索。

## 1. 这个 skill 是做什么的

`support-triage` 用于处理海外客户通过 WhatsApp、飞书邮箱、飞书消息发来的机器人技术问题。

它不会直接替你自动回复客户，而是帮助你完成：

- 判断客户问题是咨询、排障，还是需要内部升级
- 从 WhatsApp 截图、聊天记录、邮件中提取关键信息
- 归纳客户问题
- 生成适合复制到飞书知识问答的问题
- 在本机已配置 `lark-cli` 时，辅助检索飞书知识库资料
- 生成客户回复草稿，默认使用客户原语言
- 生成中文内部说明
- 生成内部升级工单描述
- 判断是否适合沉淀成 FAQ

支持客户语言：

- 法语
- 英语
- 中文

## 2. 适合使用的场景

可以在以下场景使用：

- 客户发来 WhatsApp 聊天截图
- 客户发来机器人故障视频或视频截图
- 客户通过邮件描述技术问题
- 客户咨询机器人功能、配置、限制或使用方法
- 客户反馈机器人异常、报错、噪音、无法执行任务、无法充电、屏幕异常、刮水组件偏移等
- 你需要把客户原始描述整理成飞书知识问答检索问题
- 你需要给客户写法语/英语/中文回复草稿
- 你需要判断是否要升级给内部技术团队

## 3. 基本使用方式

### 3.1 空调用，先生成输入模板

如果你还没有整理客户信息，可以直接输入：

```text
/support-triage
```

或：

```text
$support-triage
```

智能体应先返回一个精简输入模板，让你补充：

- 客户原文
- 客户语言
- 客户背景
- 产品/机型
- 问题发生场景
- 图片/日志/错误码
- 初步判断
- 飞书知识问答结果

### 3.2 直接发送 WhatsApp 截图或聊天记录

你也可以直接把 WhatsApp 截图、飞书聊天记录、邮件内容发给智能体，并输入：

```text
请使用 /support-triage 分析这个客户问题。
```

这时 skill 会先判断问题类型：

- 咨询类：功能、配置、使用方法、兼容性、限制等
- 排障类：异常声音、报错、任务失败、无法启动、无法充电、屏幕异常、硬件偏移等
- 升级敏感类：同一机器人反复故障、客户情绪激烈、安全风险、严重影响运营、重点客户等

### 3.3 咨询类问题

如果客户只是问功能或使用方法，skill 不会默认要求 SN、故障时间、视频、日志。

它会直接输出：

- 问题摘要
- 适合问飞书知识问答的问题
- 必要时要求补充产品/版本
- 给客户的初步回复草稿

### 3.4 排障类问题

如果客户反馈故障，skill 会输出：

- 问题类型判断
- 已知事实
- 假设与推断（内部）
- 缺失关键信息
- 需要客户补充的信息
- 建议问飞书知识问答的问题
- 是否需要内部升级
- 给客户的初步回复草稿

注意：`假设与推断（内部）` 只用于内部判断，不应直接复制给客户。

### 3.5 第二轮处理：补充飞书知识问答结果

第一轮输出后，把“建议问飞书知识问答的问题”复制到飞书知识问答。

拿到飞书知识问答结果后，再发给智能体：

```text
请使用 /support-triage 结合下面的飞书知识问答结果，生成正式客户回复和内部说明。

飞书知识问答结果：
...
```

第二轮会输出：

- 对飞书答案的整理
- 最终技术判断
- 给客户的正式回复草稿
- 中文内部说明
- 内部升级工单描述
- FAQ 草稿

### 3.6 飞书知识库自动检索

如果本机已经打通飞书 CLI，`support-triage` 可以优先使用飞书知识库检索结果来辅助判断。

推荐检索链路：

```text
support-triage
→ 生成产品/模块/现象/错误码关键词
→ 通过 lark-cli 搜索飞书 Wiki / Docx
→ 结合搜索结果输出分诊和客户回复草稿
```

如果 CLI 没有配置好，`support-triage` 不会停止工作，而是会：

- 提示调用 `$feishu-cli-setup` 检查本机配置
- 输出建议检索词，方便手动复制到飞书知识问答
- 避免把未检索到的知识库内容当成已验证依据

可以手动测试：

```powershell
lark-cli auth check --scope "search:docs:read"
lark-cli drive +search --query "CT4" --doc-types wiki,docx --page-size 10 --format json
python tools\feishu_search_docs.py "CT4" --type wiki --type docx --count 5
```

## 4. 推荐输入示例

### 4.1 WhatsApp 截图场景

```text
请使用 /support-triage 分析这个 WhatsApp 截图。
客户是法国经销商，机器人型号是 CC1。
```

然后附上截图。

### 4.2 客户原文场景

```markdown
请使用 /support-triage 处理下面这个客户问题。

客户原文：
Bonjour, le robot fait un bruit anormal à la fin de la tâche. Est-ce que vous savez d'où vient le problème ?

客户语言：法语
客户背景：法国经销商
产品/机型：CC1
问题发生场景：清洁任务结束阶段
图片/日志/错误码：客户发了 6 秒视频，暂无日志
我的初步判断：可能与清洁收尾或刮水组件有关
飞书知识问答返回结果：
```

### 4.3 二轮处理场景

```markdown
请使用 /support-triage 进行二轮处理。

客户原文：
...

首轮判断：
...

飞书知识问答返回结果：
...
```

## 5. 客户回复原则

使用输出中的客户回复草稿前，请注意：

- 不要承诺一定解决
- 不要承诺具体处理时限
- 不要把内部推断直接说给客户
- 不要把不确定内容说成确定根因
- 首轮回复尽量使用“我们会进一步确认下一步建议”
- 如果涉及安全风险，应建议客户暂停使用并保留现场信息

## 6. 飞书智能体如何安装

如果飞书智能体不能直接从 GitHub 拉取仓库，可以手动安装。

### 6.1 创建 skill

在飞书智能体的 skill 管理或配置入口中，新建一个 skill：

```text
skill name: support-triage
```

### 6.2 粘贴 SKILL.md

把本文档第 7 节中的 `SKILL.md` 全文复制到 skill 内容中。

如果飞书智能体只支持纯提示词，不支持 YAML frontmatter，也可以保留全文；如果它要求去掉元数据，可以去掉最上方这段：

```yaml
---
name: support-triage
description: ...
---
```

但建议优先保留，因为这段有助于智能体识别 skill 的名称和触发场景。

### 6.3 可选：安装 feishu-cli-setup

如果希望同事用飞书 CLI 自动检索知识库，建议同时安装 `feishu-cli-setup` skill。

新建另一个 skill：

```text
skill name: feishu-cli-setup
```

安装后可输入：

```text
/feishu-cli-setup
```

或：

```text
请使用 $feishu-cli-setup 检查本机飞书 CLI 是否可以搜索知识库。
```

这个 skill 会检查：

- Node.js 是否存在
- `lark-cli` 是否安装
- 飞书 CLI 是否已登录
- token 是否有效
- 是否具备 `search:docs:read`
- 是否能执行一次测试搜索

注意：`feishu-cli-setup` 不会自动安装软件、不会修改系统配置、不会保存凭证，只会给出检查结果和下一步命令。

### 6.4 测试安装

安装后，输入：

```text
/support-triage
```

期望结果：智能体返回一个精简输入模板。

再测试：

```text
请使用 /support-triage 分析这个客户问题：客户说 CC1 在清洁任务结束时有异常噪音，并且刚更换过 CT4。
```

期望结果：智能体应判断为排障类或升级敏感类，并输出假设与推断、缺失信息、知识库查询问题和客户回复草稿。

## 7. SKILL.md 全文

请将以下内容作为 `support-triage` 的 skill 内容。

````markdown
---
name: support-triage
description: Triage overseas robot technical support cases from WhatsApp, Feishu email, Feishu messages, or copied customer conversations in French, English, or Chinese. Use when the user needs Hermes to classify a customer robot issue, summarize it, prepare Feishu knowledge-base query questions, draft customer replies, write Chinese internal escalation notes, produce escalation ticket descriptions, or decide whether to turn the case into an FAQ.
---

# Support Triage

## Purpose

Use this skill to turn messy customer support messages into structured Markdown for technical triage, Feishu knowledge-base lookup, customer replies, escalation, and FAQ capture. Do not directly auto-reply to customers; produce drafts and decision support for the human support owner.

## Load References

- For the full reusable system prompt, read `references/main-prompt.md`.
- For Feishu knowledge-base source guidance, read `references/knowledge-sources.md`.
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
5. Before making technical judgments, use the linked PUDU Feishu knowledge base when the environment has access. If not accessible, say internally that the knowledge base could not be accessed and ask the user to paste the relevant Feishu knowledge-base result. Never claim to have read that link unless its contents are available in the current context.
6. If a Feishu API/search utility is available, search by product/model, module, symptom, error code, and key customer phrases before drafting technical conclusions. If `lark-cli` is missing, not logged in, lacks `search:docs:read`, or search fails, tell the user to run `$feishu-cli-setup` and include exact suggested search queries for manual Feishu lookup.
7. Preserve the customer's original language and infer it if not explicitly provided. Customer-facing drafts default to the customer's language. Internal notes default to Chinese.
8. Extract or infer: customer original text, customer language, customer background, product/model, scenario, images/logs/error codes, user's preliminary judgment, and Feishu answer if present.
9. Classify the issue type and affected product/module. Prefer conservative categories such as hardware, software/app, cloud/platform, network, map/navigation, task/dispatch, charging/power, account/permission, installation/configuration, operation guidance, bug/regression, or unknown.
10. Separate facts, assumptions, and missing information. Never present unsupported internal guesses as customer-facing conclusions.
11. For troubleshooting or escalation-sensitive first-pass output, include an internal "Hypotheses and Inferences" section with evidence and confidence. Keep this section out of the customer reply.
12. For second-pass output, organize the Feishu answer, produce the final technical judgment, draft the customer response in the customer's language, and create Chinese internal notes, escalation text, and FAQ draft when appropriate.
13. For first-pass output, generate a precise Feishu knowledge-base query question and an initial customer reply draft.

## Customer Reply Rules

- Be professional, polite, clear, and concise.
- Do not overpromise resolution time, replacement, compensation, root cause, or product defect unless the provided evidence supports it.
- Do not fabricate causes, policies, commands, firmware behavior, or troubleshooting steps.
- Use cautious wording for uncertain points: "we recommend checking first", "we need to confirm further", "this may be related to...", "il est possible que...", "we will verify with the technical team".
- Avoid promising a resolution plan, root cause, or timing in first-pass replies. Prefer "we will verify the next steps" over "we will come back with a resolution plan".
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

Primary reference source when accessible:

`https://pudutech.feishu.cn/wiki/ZXWUw8OBniPEzqkYbymc2E6AnJe?from=from_copylink`

Create one to three focused query questions. Each question should include product/model, module, symptom, scenario, exact error code/log phrase if available, recent changes, and expected answer type. Avoid vague questions like "how to fix this robot problem".

Good query pattern:

`[Product/model] in [scenario] shows [symptom/error]. What are the likely causes and recommended troubleshooting steps for [module]?`

When the customer language is not Chinese, still write Feishu query questions in clear Chinese by default unless the user asks otherwise, because internal knowledge is usually easier to retrieve in Chinese.
````

## 8. 维护建议

后续如果发现输出不符合预期，可以优先调整这些内容：

- 问题分流不准：修改 `Workflow` 第 2-3 条
- 客户回复太强硬或承诺过度：修改 `Customer Reply Rules`
- 飞书知识问答问题不够好：修改 `Feishu Knowledge-Base Query Guidance`
- 飞书 CLI 检索不可用：先使用 `$feishu-cli-setup` 检查 `lark-cli` 登录和 `search:docs:read`
- 排障报告缺少某个字段：修改 `Output Requirements`

建议每次修改后都用两个案例测试：

- 咨询类案例：客户只问某个功能怎么用
- 排障类案例：客户发 WhatsApp 截图或视频，描述机器人异常
