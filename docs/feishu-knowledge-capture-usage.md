# Feishu Knowledge Capture 使用文档

`feishu-knowledge-capture` 是独立的个人知识沉淀 skill，用来把你主动选择的飞书群聊、JSWO 工单群、消息链接或手动粘贴的案例材料整理成高质量个人 case 文档。

它和 `supportman` 分开维护：`supportman` 负责日常技术支持处理和沉淀价值判断；`feishu-knowledge-capture` 负责把值得保留的材料写成个人 case 文档，并可选更新个人索引清单。需要组合时，只把 `supportman` 的输出当作输入材料之一。

## 安装和更新

首次安装：

```text
@你的飞书智能体 /skill install https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
```

已安装后更新：

```text
@你的飞书智能体 /skill update https://github.com/Ginhy2026/support-ai-workflows/tree/main/feishu-knowledge-capture
```

正式维护统一使用 `main/feishu-knowledge-capture` 这个地址。

## 默认产物

- 一个个人沉淀文档组或个人 Wiki 父节点。
- 每个 case 一个独立文档。
- 一个可选个人索引清单。

个人索引清单只保留：

```text
关键词, 类型, 模块, 标题, 来源, 文档链接, 状态
```

## 常用调用

指定群聊沉淀：

```text
/飞书知识沉淀 获取今天群聊「xxx」里的关键信息并沉淀
```

多群本周沉淀：

```text
/飞书知识沉淀 获取本周这些群聊：A、B、C，整理成个人 case 文档
```

单个案例沉淀：

```text
使用 feishu-knowledge-capture，把下面这段案例摘要沉淀成个人 case 文档。
```

未闭环线索：

```text
使用 feishu-knowledge-capture，把这个还没闭环的新产品问题写成个人 Pending 线索。
```

交给 Obsidian 第二大脑审核：

```text
把这次纠正整理成第二大脑待审核候选。只写入专用候选区，不要修改正式知识。
```

推荐节奏是工作发生时随时创建候选，每周集中审核一次。明确且严重的错误可以当天建议审核，但飞书智能体仍不直接修改正式知识。

只有候选仓库写入并通过验证后，飞书智能体才能回答“已创建待审核候选”。没有候选仓库写权限时，应回答“已生成待审核候选草稿，请交给 Codex 导入”，并在聊天中返回完整候选 Markdown。

读取经过审核的第二大脑正式知识时，安装并使用独立的 `second-brain-reader`。它只读取 AI 发布仓库、引用实际路径，并在知识不足时明确说明；不要用候选沉淀 Skill 代替正式知识检索。

可见工单群：

```text
/飞书知识沉淀 获取我可见的 JSWO 工单群中今天的关键信息并沉淀
```

## 使用边界

- 只处理你主动提供或当前身份可见的材料。
- 不默认扫描公司所有群聊，也不读取其他人的私聊。
- 文档质量优先，索引只做定位和状态追踪。
- 暂不自动投稿星火计划；单篇 case 文档后续可由你人工加工或投稿。
- 不直接修改 Obsidian 源仓库、正式知识、入口页或 AI 发布仓库；需要交给第二大脑时，只创建待审核候选。

## 维护边界

- 更新个人沉淀流程、case 文档模板、索引字段、去重规则时，改 `feishu-knowledge-capture/`。
- 更新日常技术支持处理、客户回复、售前判断、知识检索问题生成时，改 `supportman/`。
- 不要把 `supportman` 的完整处理规则复制进 `feishu-knowledge-capture`；只保留必要的组合调用说明。
