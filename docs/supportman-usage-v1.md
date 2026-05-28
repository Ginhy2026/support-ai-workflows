# SupportMan Skill 使用文档 v2.0

本文档用于帮助海外技术支持同事在 Hermes / 飞书智能体中安装和使用 `supportman`。`SupportMan` 是 `support-triage` 的第二个版本：它不再只是“故障分诊器”，而是个人技术支持日常工作入口，用来处理 WhatsApp 截图、飞书截图、售前咨询、星火计划/项目线索、客户故障和内部跟进。

注意：`SupportMan` 和 `feishu-knowledge-capture` 是两个独立 skill。二者只是有轻量关联：`SupportMan` 可以判断一个案例是否有沉淀价值；如果你后续明确要写入候选知识池，再单独调用 `feishu-knowledge-capture`。

## 1. 安装和更新

第一次安装：

```text
@你的飞书智能体 /skill install https://github.com/Ginhy2026/support-ai-workflows/tree/main/supportman
```

已安装后更新：

```text
@你的飞书智能体 /skill update https://github.com/Ginhy2026/support-ai-workflows/tree/main/supportman
```

验证入口：

```text
@你的飞书智能体 /supportman
```

正常情况下，智能体会返回一个精简输入模板。

如果旧版本已经安装过 `support-triage`，建议迁移到 `supportman`。历史对话、历史归档和旧文档中出现的 `support-triage` 可以理解为旧名称；新调用统一使用 `/supportman` 或 `$supportman`。

## 2. 它做什么

`SupportMan` 帮你把零散工作变成可执行 Markdown：

- 从 WhatsApp / 飞书截图中提取可见事实、客户诉求、产品信息和缺失证据。
- 判断工作项类型：售前/咨询、星火计划/项目、排障、工作跟进、升级敏感。
- 生成飞书知识问答检索问题，并判断资料是否适用于当前场景。
- 输出客户回复草稿，默认使用客户原语言。
- 输出中文内部说明、下一步动作、升级工单描述。
- 判断是否具备后续知识沉淀价值。

## 3. 基本用法

空调用，先拿模板：

```text
/supportman
```

直接处理截图：

```text
请使用 /supportman 分析这个 WhatsApp 截图。
```

处理飞书截图或内部同事请求：

```text
请使用 /supportman 整理这张飞书截图，告诉我该回复客户什么、内部还缺什么信息。
```

处理售前或星火计划：

```text
请使用 /supportman 处理这个星火计划项目咨询，先判断技术可行性、需要查哪些资料、下一步该找谁确认。
```

二轮处理：

```text
请使用 /supportman 结合下面的飞书知识问答结果和 SOP，生成正式客户回复、内部说明和沉淀判断。
```

## 4. 推荐输入

信息不完整也可以直接发，但推荐尽量包含：

```markdown
# 客户问题输入

## 客户原文

## 客户语言
法语 / 英语 / 中文 / 未知：

## 工作来源和目标
- 来源：WhatsApp / 飞书截图 / 飞书消息 / 飞书邮件 / 售前咨询 / 星火计划 / 内部同事请求 / 其他
- 目标：客户回复 / 售前答疑 / 技术确认 / 资料检索 / 升级 / 跟进 / 知识沉淀

## 客户背景
- 国家/地区：
- 客户类型/项目：
- 紧急程度：

## 产品/机型

## 场景和现象

## 图片/日志/错误码

## 我的初步判断

## 飞书知识问答返回结果
> 首轮留空；二轮粘贴飞书知识问答结果。

## 补充参考资料 / SOP
```

## 5. 工作项类型

售前/咨询类：客户问功能、配置、兼容性、限制、方案可行性。不要默认索要 SN、故障时间、日志，优先生成检索问题和答疑草稿。

星火计划/项目类：围绕试点项目、样板客户、方案验证、价值证明或跨团队推进。输出项目目标、已知事实、技术待确认点、价值验证指标、内部协作对象和下一步动作。

排障类：客户反馈异常声音、报错、任务失败、无法启动/充电/定位、硬件偏移、屏幕异常等。输出事实、内部假设、缺失信息、低风险排查步骤和客户回复草稿。

工作跟进类：信息不一定是故障，但需要整理当前状态、负责人、阻塞点、对客户/内部的下一步动作。

升级敏感类：安全风险、反复故障、重点客户、严重影响运营、跨团队阻塞或疑似硬件损坏。客户回复要稳，内部建议升级。

## 6. 输出结构

首轮输出会包含：

- 工作项类型判断
- 一句话摘要
- 涉及产品/模块
- 资料检索结果与适用性判断
- 缺失信息
- 可执行排查或确认步骤
- 建议问飞书知识问答的问题
- 客户回复草稿
- 下一步动作：对客户、对内部、对知识沉淀
- 是否需要升级
- 是否具备后续知识沉淀价值

二轮输出会额外整理飞书知识问答、SOP 或补充资料，并生成更正式的客户回复、内部说明和升级工单描述。

## 7. 飞书知识库检索

如果本机已配置 `lark-cli`，`SupportMan` 可以配合飞书文档搜索。未配置时，它仍会输出可复制到飞书知识问答的检索问题。

检查命令：

```powershell
lark-cli auth check --scope "search:docs:read"
lark-cli drive +search --query "CC1 异常噪音" --doc-types wiki,docx --page-size 10 --format json
python tools\feishu_search_docs.py "CC1 异常噪音" --type wiki --type docx --count 5
```

如果搜索不可用，先调用：

```text
/feishu-cli-setup
```

## 8. 可选知识沉淀关联

`SupportMan` 只判断是否值得沉淀，不默认生成长篇正式知识，也不直接写入候选池。`feishu-knowledge-capture` 是独立 skill；只有当你明确要把闭环案例或高价值线索写成候选知识时，才单独调用它。

判断标签：

- 不沉淀：一次性问题、复用价值低，或资料不足且看不出复用价值。
- 待闭环后沉淀：新产品、新问题、星火计划线索或资料不成熟，但有复用潜力。
- 建议立即候选沉淀：已有明确现象、处理步骤、结论或高复用价值。

交接示例：

```text
请使用 /feishu-knowledge-capture 把下面这个 SupportMan 输出和最终方案沉淀成候选排障知识。
```

`feishu-knowledge-capture` 可以把 `SupportMan` 输出作为参考材料之一，写入候选 Wiki/Base，并按配置做 GitHub Markdown 归档。

## 9. 常用示例

WhatsApp 截图：

```text
请使用 /supportman 分析这个 WhatsApp 截图。客户是法国经销商，机器人型号可能是 CC1。
```

售前咨询：

```text
请使用 /supportman 处理这个售前问题：客户想确认配送机器人能否在酒店夜间场景跨楼层配送，需要哪些前提条件？
```

星火计划：

```text
请使用 /supportman 整理这个星火计划项目线索：客户想做 T300 在商超后仓搬运的试点，请列出技术可行性、需要客户补充的信息、内部确认对象和沉淀价值。
```

二轮排障：

```text
请使用 /supportman 进行二轮处理。

客户原文：
...

飞书知识问答结果：
...

补充 SOP：
...
```

## 10. 维护建议

- 入口定位或分流不准：更新 `supportman/SKILL.md` 的 Workflow。
- 输入模板不够顺手：更新 `supportman/references/input-template.md`。
- 输出结构缺字段：更新 `supportman/references/output-templates.md`。
- 飞书知识检索规则变化：更新 `supportman/references/knowledge-sources.md`。
- 沉淀判断口径变化：先更新 SupportMan；只有独立沉淀流程本身变化时，才更新 `feishu-knowledge-capture`。
