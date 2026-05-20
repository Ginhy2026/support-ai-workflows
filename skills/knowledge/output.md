---
name: output
description: "输出呈现知识 — 回顾报告、图表生成、问答归档、完整性检查"
version: 1.1.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge, output, review, diagram, qa]
---

# output — 知识输出

## 何时触发

用户说"输出"、"回顾"、"生成图表"、"output"、"出报告"、"检查"。

在 CLI 中用 `/skill output` 加载；在 Feishu/Telegram 网关中直接用 `/output <类型>` 调用。

## ⚠️ 不可违反的规则

**禁止调用 `skill_manage`。** 目标是输出知识到群聊和文件系统，不是创建 Hermes skill。

## Vault 路径

```bash
VAULT="${ESPACE_VAULT:-$HOME/Espace_Obsidian}"
```

## 输出类型

### 回顾报告
扫描最近 7 天变更，直接回复到群：

```
🧠 知识回顾 (最近7天)
═══════════════════
📥 新摄入: N 篇
🏷️ 新概念: N 个
🔗 关联发现: ...
📊 热度排行: ...
```

### 图表
用 `architecture-diagram` 或 `excalidraw` 生成概念示意图，保存到 `输出/图表/`。

### 问答归档
将有长期参考价值的问答保存到 `输出/问答归档/<slug>.md`。

### 检查报告
```
📋 健康报告
═══════════
📂 总览: N 个文件
✅ 完整性: N/M
❌ 缺失摘要: N 个
❌ 孤立页面: N 个
💡 建议: 运行 /skill digest 补齐
```

## 验证清单

- [ ] 回复直接显示在群聊中
- [ ] 如果写了文件，已 git push
- [ ] **禁止出现：** `skill_manage`