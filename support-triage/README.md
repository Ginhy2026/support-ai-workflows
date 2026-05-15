# support-triage Hermes Skill

`support-triage` 用于处理海外客户通过 WhatsApp、飞书邮箱、飞书消息发来的机器人技术问题。它不会直接自动回复客户，而是帮助 Hermes 完成分诊、归纳、飞书知识问答检索问题生成、客户回复草稿、内部升级说明和 FAQ 沉淀判断。

## 文件结构

```text
support-triage/
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

## 核心能力

- 首轮分诊：在没有飞书知识问答结果时，整理客户问题、判断类型、生成检索问题和初步客户回复。
- 二轮整理：在补充飞书知识问答结果后，整理答案、形成技术判断、生成正式客户回复和中文内部说明。
- 升级判断：识别是否需要内部升级，并生成升级工单描述。
- FAQ 沉淀：判断是否适合沉淀知识库，并生成 FAQ 草稿。
- 多语言回复：客户回复默认使用客户原语言，支持中文、英语、法语。

## 如何在 Hermes 中使用

1. 将整个 `support-triage` 文件夹放到 Hermes 可识别的 skills 目录。
2. 在 Hermes 中用类似下面的方式触发：

```text
Use $support-triage to triage this robot support case.
```

或中文：

```text
请使用 $support-triage 处理下面这个客户问题。
```

如果只输入下面这种空调用，skill 会先输出精简输入模板，方便你补充客户原文、语言、客户背景、产品/机型、场景、图片/日志/错误码等信息：

```text
/support-triage
```

3. 首轮处理时，粘贴客户原文、语言、产品/机型、场景、图片/日志/错误码说明和你的初步判断。飞书知识问答结果留空。
4. 将首轮输出中的“建议问飞书知识问答的问题”复制到飞书知识问答。
5. 把飞书知识问答返回结果补充给 Hermes，再次使用 `$support-triage` 进行二轮处理。
6. 复制二轮输出中的客户回复草稿、中文内部说明、升级工单描述或 FAQ 草稿到对应渠道。

## 推荐输入格式

使用 `references/input-template.md` 中的模板。信息不完整也可以使用，skill 会明确列出缺失信息。

## 输出格式

所有输出固定为 Markdown。首轮和二轮模板见 `references/output-templates.md`。

## 维护建议

- 如果公司内部有新的标准排查路径，优先更新 `references/output-templates.md` 或 `references/examples.md`。
- 如果客户回复口吻需要调整，更新 `references/main-prompt.md` 的客户回复边界和 `references/output-templates.md` 的语气片段。
- 如果 Hermes 的 skill 元数据规范变化，更新 `agents/openai.yaml`。
