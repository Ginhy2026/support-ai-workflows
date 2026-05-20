---
name: web-in
description: "从URL抓取网页内容，写入知识库文件系统（原始材料/文章/），生成摘要和概念页，提交到GitHub"
version: 1.2.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge, ingest, web, obsidian, file-system]
---

# web-in — 摄入网页到知识库

## 何时触发

用户在对话中说"摄入网页"、"收录网页"、"web-in"，或者发了一个网址并说要保存到知识库。

在 CLI 中用 `/skill web-in` 加载；在 Feishu/Telegram 等网关中直接用 `/<skill-name>` 调用（注意：`/skill web-in` 在网关中会被识别为未知命令 `/skill`，而不是加载 web-in skill）。

## ⚠️ 不可违反的规则

**禁止调用 `skill_manage`。** 这个 skill 的目的是把网页内容写入知识库文件，不是创建或修改任何 Hermes skill。

正确做法：用 `write_file` 写入 `$VAULT/原始材料/文章/` 目录。
错误做法：用 `skill_manage` 创建任何 skill。

如果你发现自己正在考虑调用 `skill_manage`，停下来，改用 `write_file`。

## Vault 路径

```bash
VAULT="${ESPACE_VAULT:-$HOME/Espace_Obsidian}"
```

## 特殊情况处理

### 视频平台 / 强反爬网站

如果 URL 来自视频平台（**抖音 Douyin**、B站、YouTube 等）或遇到 strong anti-crawler（返回仅为 JS obfuscation VM 代码，无 visible HTML text）：

**不要浪费大量工具调用反复尝试。** 抖音 Douyin 的 anti-crawler 极其严格：
- `curl` / `requests` 返回的 HTML 不含任何 visible text，仅含 obfuscated JavaScript VM
- Douyin API 需要 signed cookies
- `yt-dlp` 也需要 fresh cookies 才能获取 metadata
- 最多尝试 2 种方法，如果都失败，立即进入 fallback 流程

### Fallback 策略

1. **识别主题**：从用户消息中的 URL 描述提取视频标题、作者、关键词（用户分享时通常会附带标题文字）
2. **搜索同主题文字内容**：用 `curl` 或 GitHub API 搜索相关关键词，找到 text-based 文章替代
3. **收录文字文章**：将找到的同主题文字文章作为主要来源，原始视频 URL 在元数据中作为关联来源记录
4. **标记关联视频**：在原始材料文件的开头用 `> 关联视频: [标题](URL)` 注明

只有在找不到任何可提取的文字内容时，才应告知用户并建议使用 `media-in` 或自行查找文字版。

## 执行流程

### 1. 获取网页
用 `web_extract` 或 `curl` 提取标题、作者、日期、正文、图片。

**第一步先判断平台类型：** 如果 URL 明显是视频/图片平台（douyin.com, bilibili.com, youtube.com 等），直接跳到「特殊情况处理 > 视频平台」流程。

### 2. 生成文件名
标题转小写 → 空格变连字符 → 截断 60 字符 → 存为变量 `<slug>`

### 3. 写原始材料文件
路径：`$VAULT/原始材料/文章/<slug>.md`

内容格式：
```markdown
---
title: "页面原标题"
网址: "https://..."
作者: "作者"
日期: "发布日期"
收录: "今天日期"
类型: 文章
---

# 页面原标题

> 来源: [链接](网址)
> 作者: 作者 | 日期: 日期

正文...
```

### 4. 写摘要文件
路径：`$VAULT/知识库/摘要/<slug>-摘要.md`

### 5. 写/更新概念页（必须执行）

**此步骤不可跳过。** 扫描正文提取 2-5 个核心概念。

对每个概念：
- 已有文件 → 用 `patch` 追加来源信息，更新 `更新日期`
- 无此文件 → 用 `write_file` 创建新页面到 `$VAULT/知识库/概念/<概念名>.md`

概念页格式：
```markdown
---
title: "概念名"
创建日期: "今天"
更新日期: "今天"
类型: 概念
---

# 概念名

## 定义

## 来源
本信息来自 [[文章slug]]
```
完成后检查：`ls "$VAULT/知识库/概念/"` 确认有新增文件。

### 6. 更新索引
在 `$VAULT/知识库/索引.md` 的 `📝 摘要` 和 `🏷️ 概念` 下加一行。

### 7. git 提交并推送（必须执行全部三行）

```bash
cd "$VAULT"
git add -A
git commit -m "收录(网页): 标题"
git push          # ← 不要省略这步！只 commit 不 push 的话知识库不会更新
```

执行后用 `git status` 确认工作区干净，没有未推送的 commit。

### 8. 回复
```
✅ 已收录: 标题
📄 原始材料/文章/<slug>.md
📝 知识库/摘要/<slug>-摘要.md
🏷️ 概念: ...
📑 知识库/索引.md 已更新
🔄 已推送 GitHub
```

## 验证清单（执行完毕后逐条检查）

- [ ] `write_file` 写入了 `$VAULT/原始材料/文章/` 下的文件
- [ ] `write_file` 写入了 `$VAULT/知识库/摘要/` 下的文件
- [ ] `write_file` 或 `patch` 写入/更新了 `$VAULT/知识库/概念/` 下的文件
- [ ] 索引 `$VAULT/知识库/索引.md` 已更新
- [ ] `git add / commit / push` 全部成功
- [ ] `git status` 显示工作区干净
- [ ] **未调用：** `skill_manage`、`skill_view`、`skills_list`
