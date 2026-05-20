---
name: digest
description: "消化整理知识库 — 补齐摘要/概念、归类主题、检查完整性"
version: 1.1.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge, digest, organize, audit]
---

# digest — 消化整理

## 何时触发

用户说"整理"、"消化"、"补齐"、"digest"。

在 CLI 中用 `/skill digest` 加载；在 Feishu/Telegram 网关中直接用 `/digest` 调用。

## ⚠️ 不可违反的规则

**禁止调用 `skill_manage`。** 目标是扫描和补齐知识库文件，不是创建 Hermes skill。

## Vault 路径

```bash
VAULT="${ESPACE_VAULT:-$HOME/Espace_Obsidian}"
```

## 执行流程

### 1. 扫描缺失
用 `search_files` 或 `terminal` + `find` 对比 `原始材料/` 和 `知识库/摘要/`，列出：
- `原始材料/文章/` 中没有对应摘要的文件
- `原始材料/论文/` 中没有对应摘要的文件
- `原始材料/媒体/` 中没有对应摘要的文件

### 2. 补齐
对每个缺失的 raw 文件：
- 用 `read_file` 读取内容
- 用 `write_file` 写入对应摘要到 `知识库/摘要/`
- 提取概念，更新 `知识库/概念/`
- 更新 `知识库/索引.md`

### 3. 主题归类
扫描所有摘要和概念，按内容相关性归入 `知识库/主题/` 下的主题页。

### 4. 完整性检查
- 每个 raw 文件都有对应摘要？
- 概念页互相链接（`[[wikilinks]]`）？
- 索引是最新的？
- 有重复内容需要合并？
- 有超过 90 天未更新的旧内容？

### 5. git 提交
```bash
cd "$VAULT" && git add -A && git commit -m "整理: $(date +%Y-%m-%d)" && git push
```

### 6. 回复
```
📊 整理报告
═══════════

📥 未处理: N 个 → 已补齐 ✅
🏷️ 新建概念: N 个
📂 主题归类: 主题1, 主题2
✅ 完整性: N/N 完整
🔄 已推送 GitHub，请手动同步 Obsidian
```

## 验证清单

- [ ] 所有缺失摘要已补齐
- [ ] git push 成功
- [ ] **禁止出现：** `skill_manage`