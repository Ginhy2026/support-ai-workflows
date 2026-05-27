# SupportMan Hermes Skill

`SupportMan` (`supportman`) 是 `support-triage` 的第二个版本，也是个人技术支持日常工作入口，用于处理海外支持、售前咨询、星火计划/项目线索、WhatsApp 截图、飞书截图、飞书邮件/消息和补充 SOP 资料。

它不会直接自动回复客户，而是帮助 Hermes 输出可复制的 Markdown：工作项分类、资料检索问题、适用性判断、客户回复草稿、中文内部说明、下一步动作、升级建议，以及是否具备后续知识沉淀价值。

`SupportMan` 和 `feishu-knowledge-capture` 是两个独立 skill。`SupportMan` 只做当前工作处理和沉淀价值判断；需要真正创建候选知识时，再单独调用 `feishu-knowledge-capture`。

## 文件结构

```text
supportman/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
└── references/
    ├── main-prompt.md
    ├── input-template.md
    ├── knowledge-sources.md
    ├── output-templates.md
    └── examples.md
```

## 核心能力

- 截图/聊天处理：读取 WhatsApp、飞书截图、飞书卡片、邮件截图或粘贴聊天中的可见事实。
- 日常分流：区分售前/咨询、星火计划/项目、排障、工作跟进、升级敏感。
- 资料检索：生成飞书知识问答问题，并判断飞书知识库、SOP、语雀、网页或粘贴正文是否适用于当前案子。
- 回复草稿：默认使用客户原语言，客户回复和中文内部说明分开输出。
- 下一步动作：拆成对客户、对内部、对知识沉淀三类。
- 沉淀价值判断：只判断是否值得后续沉淀，不在本 skill 里生成长篇正式知识。

## 使用方式

空调用获取输入模板：

```text
/supportman
```

处理截图或聊天：

```text
请使用 /supportman 分析这个 WhatsApp 截图。
```

处理售前或星火计划：

```text
请使用 /supportman 整理这个星火计划项目咨询，输出技术可行性、缺失信息、内部确认对象和沉淀建议。
```

二轮处理：

```text
请使用 /supportman 结合下面的飞书知识问答结果和 SOP，生成正式回复和内部说明。
```

## 维护入口

- 使用文档：`docs/supportman-usage-v1.md`
- 核心 workflow：`SKILL.md`
- 输入模板：`references/input-template.md`
- 输出模板：`references/output-templates.md`
- 飞书知识源规则：`references/knowledge-sources.md`
