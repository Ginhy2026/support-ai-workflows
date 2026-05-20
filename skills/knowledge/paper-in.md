---
name: paper-in
description: "摄入论文到知识库 — 从 arxiv 提取、摘要、概念，写入文件系统"
version: 1.1.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge, ingest, paper, arxiv, file-system]
---

# paper-in — 摄入论文

## 何时触发

用户说"摄入论文"、"收录论文"、"paper-in"，或发了 arxiv ID / 论文 URL。

在 CLI 中用 `/skill paper-in` 加载；在 Feishu/Telegram 网关中直接用 `/paper-in <arxiv-id>` 调用。（注意：`/skill paper-in` 在网关中会被识别为未知命令 `/skill`，不是加载 paper-in。）

## ⚠️ 不可违反的规则

**禁止调用 `skill_manage`。** 这个 skill 的目的是把论文内容写入知识库文件，不是创建或修改任何 Hermes skill。

正确做法：用 `write_file` 写入 `$VAULT/原始材料/论文/` 目录。
错误做法：用 `skill_manage` 创建任何 skill。如果发现自己想用 `skill_manage`，停下来，改用 `write_file`。

## Vault 路径

```bash
VAULT="${ESPACE_VAULT:-$HOME/Espace_Obsidian}"
```

## 执行流程

### 1. 获取论文
arxiv ID → 用 arxiv API 获取元数据（标题、作者、摘要、日期、分类）。
如果是其他 URL 的 PDF，用 `web_extract` 或 `curl` 提取。

### 2. 生成文件名
标题转小写 → 空格变连字符 → 截断 60 字符 → 存为 `<slug>`

### 3. 写原始材料文件
路径：`$VAULT/原始材料/论文/<slug>.md`

```markdown
---
title: "论文标题"
arxiv_id: "2503.12345"
作者: ["作者1"]
日期: "2025-03"
分类: ["cs.AI"]
收录: "今天日期"
类型: 论文
---

# 论文标题

> 作者列表 | 日期
> [arxiv](https://arxiv.org/abs/...)

## 官方摘要

## 关键贡献
```

### 4. 写摘要文件
路径：`$VAULT/知识库/摘要/<slug>-摘要.md`

### 5. 写/更新概念页
检查 `$VAULT/知识库/概念/`，已有则追加，没有则创建。

### 6. 更新索引
在 `$VAULT/知识库/索引.md` 的 `📝 摘要` 和 `🏷️ 概念` 下加一行。

### 7. git 提交
```bash
cd "$VAULT" && git add -A && git commit -m "收录(论文): 标题" && git push
```

### 8. 回复
```
✅ 已收录论文: 标题
📄 原始材料/论文/<slug>.md
📝 知识库/摘要/<slug>-摘要.md
🏷️ 概念: ...
📑 知识库/索引.md 已更新
🔄 已推送 GitHub，请手动同步 Obsidian
```

## 验证清单

- [ ] `write_file` 写入了 `$VAULT/原始材料/论文/`
- [ ] `write_file` 写入了 `$VAULT/知识库/摘要/`
- [ ] 索引已更新
- [ ] git push 成功
- [ ] **禁止出现：** `skill_manage`、`skill_view`、`skills_list`