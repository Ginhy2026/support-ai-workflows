---
name: pipeline
description: "全流程：补齐整理 → 费曼教学输出 → 报告 → GitHub 推送"
version: 2.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge, pipeline, digest, feynman, output]
---

# pipeline — 完整知识流水线

从已摄入的原始材料开始，一路处理到可教学输出。

## 何时触发

用户说"跑全流程"、"pipeline"、"完整整理"、"全部走一遍"、"从输入到输出"、"周日回顾"、"周报"。

## ⚠️ 不可违反的规则

**禁止调用 `skill_manage`。**

## Vault 路径

```bash
VAULT="${ESPACE_VAULT:-$HOME/Espace_Obsidian}"
```

## 执行流程（四步按顺序）

### 第 1 步：扫描现状

用 `terminal` 扫描 vault 目录结构：

```bash
cd "$VAULT"
echo "=== 原始材料 ==="
find 原始材料 -type f -name "*.md" | sort
echo "=== 摘要 ==="
find 知识库/摘要 -type f -name "*.md" | sort
echo "=== 概念 ==="
find 知识库/概念 -type f -name "*.md" | sort
echo "=== 教学输出 ==="
find 输出/教学 -type f -name "*.md" 2>/dev/null | sort
echo "=== 总览 ==="
echo "原始材料: $(find 原始材料 -type f | wc -l) 个文件"
echo "摘要:     $(find 知识库/摘要 -type f | wc -l) 个文件"
echo "概念:     $(find 知识库/概念 -type f | wc -l) 个文件"
echo "教学输出: $(find 输出/教学 -type f 2>/dev/null | wc -l) 个文件"
```

对比找出没有对应摘要的 raw 文件。

### 第 2 步：补齐缺失

对每个缺失的 raw 文件：
- `read_file` 读取内容
- `write_file` 生成摘要到 `知识库/摘要/<slug>-摘要.md`
- 提取 2-3 个概念，创建/更新 `知识库/概念/`
- 更新 `知识库/索引.md`

### 第 3 步：生成费曼教学输出（先检查是否已有）

**先检查** `$VAULT/输出/教学/` 下有没有最新材料的费曼文档：

```bash
ls "$VAULT/输出/教学/" 2>/dev/null
```

- **如果已有** → 跳过，在报告里注明"费曼输出已存在，如需重新生成请用 `/feynman`"
- **如果没有** → 执行生成（步骤见下）

保存到 `$VAULT/输出/教学/<slug>-费曼输出.md`

文档结构：

```markdown
---
title: "原标题 — 费曼输出"
基于: "原始材料/文章/<slug>.md"
创建日期: "今天"
类型: 教学输出
---

# 费曼输出: 原标题

## 🎯 一句话总结

## ❓ 核心问题

## 🔧 作者解法

## 💡 我学到了什么

## 🗣️ 如何讲给新人听

（用类比、生活例子让零基础的人听懂）

## 🤔 Q&A

**Q:** 你可能想问什么？
**A:** 提前回答

## 🔗 关键概念

## 📚 延伸阅读

## ✅ 行动项
```

### 第 4 步：完整性检查 + git push

```bash
cd "$VAULT"
git add -A
git commit -m "pipeline: 完整整理+费曼输出 $(date +%Y-%m-%d)"
git push
```

### 第 5 步：回复完整报告

回复格式：

```
📊 知识库完整报告
═══════════════════

📥 本周摄入: N 篇
🏷️ 概念: 新建 M 个，更新 N 个
✅ 完整性: X/Y 完整

📖 费曼输出已生成:
   📄 输出/教学/<slug>-费曼输出.md
   （可教给别人的版本）

📂 知识库总规模:
   • 原始材料: N 篇
   • 摘要: N 篇
   • 概念: N 个
   • 教学输出: N 个

🔄 已推送 GitHub，请同步 Obsidian

💡 想只看费曼输出本身，单独用 /feynman
```

## 验证清单

- [ ] 所有缺失摘要已补齐
- [ ] 生成了最新材料的费曼输出文档
- [ ] git add + commit + push 全部成功
- [ ] `输出/教学/` 下有新文件
- [ ] 未调用 `skill_manage`
