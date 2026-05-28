# Feishu Knowledge Capture 使用文档

`feishu-knowledge-capture` 是独立的飞书知识沉淀 skill，用来把已闭环案例、JSWO 工单群、指定飞书群聊或手动粘贴的案例摘要整理成候选知识。

它和 `supportman` 分开维护：`supportman` 负责日常技术支持处理和沉淀价值判断；`feishu-knowledge-capture` 负责真正写入候选 Wiki、更新候选池索引，并按配置做 GitHub Markdown 归档。需要组合时，只把 `supportman` 的输出当作输入材料之一。

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

## 常用调用

单个案例沉淀：

```text
使用 feishu-knowledge-capture，把下面这个已闭环案例沉淀成候选排障知识。
```

未闭环线索进入 Pending：

```text
使用 feishu-knowledge-capture，把这个还没闭环的新产品问题放入 Pending 候选池。
```

JSWO 工单群批量沉淀：

```text
/飞书知识沉淀 获取今天所有 JSWO 工单群并沉淀
```

指定群聊沉淀：

```text
/飞书知识沉淀 获取群聊「PUDU T300法国JSWO-202604220005」并沉淀
```

组合使用其他 skill 输出：

```text
使用 feishu-knowledge-capture，把下面这份案例摘要和最终方案沉淀成候选 FAQ/排障知识。
```

## 维护边界

- 更新飞书沉淀流程、候选 Wiki、索引、归档、去重规则时，改 `feishu-knowledge-capture/`。
- 更新日常技术支持处理、客户回复、售前判断、知识检索问题生成时，改 `supportman/`。
- 不要把 `supportman` 的完整处理规则复制进 `feishu-knowledge-capture`；只保留必要的组合调用说明。
