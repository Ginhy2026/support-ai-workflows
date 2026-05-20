---
name: media-in
description: "摄入音视频/图片到知识库 — 转文字、描述、保存到文件系统"
version: 1.1.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge, ingest, media, file-system]
---

# media-in — 摄入媒体

## 何时触发

用户说"摄入音频"、"保存图片"、"media-in"，或发了媒体链接。

在 CLI 中用 `/skill media-in` 加载；在 Feishu/Telegram 网关中直接用 `/media-in <url>` 调用。

## ⚠️ 不可违反的规则

**禁止调用 `skill_manage`。** 目标是写入知识库文件系统，不是创建 Hermes skill。

## Vault 路径

```bash
VAULT="${ESPACE_VAULT:-$HOME/Espace_Obsidian}"
```

## 执行流程

### 1. 识别媒体类型
- 图片 URL（.jpg/.png/.gif）→ `vision_analyze` 获取详细描述
- 音频 URL（.mp3/.wav/.m4a）→ 用 STT 转录文字
- YouTube/B站视频 → 用 yt-dlp 下载字幕或转录
- **抖音 Douyin 视频** → 极为强力的反爬虫（JS obfuscation + signed cookies），`yt-dlp` 无法获取基本信息除非提供 fresh cookies。不建议直接尝试提取文字；建议用户自行提供视频描述或用 `web-in` 搜索同主题文字内容替代

### 2. 生成文件名
标题/描述转小写 → 空格变连字符 → 截断 60 字符 → `<slug>`

### 3. 写原始材料文件
路径：`$VAULT/原始材料/媒体/<slug>.md`

```markdown
---
title: "媒体标题或描述"
来源: "原始 URL"
类型: 图片|音频|视频
收录: "今天日期"
---

# 媒体标题

> 来源: [链接](来源)

## 转录/描述内容
```

### 4. 写摘要文件
路径：`$VAULT/知识库/摘要/<slug>-摘要.md`

### 5. 更新概念页
提取核心概念，更新 `$VAULT/知识库/概念/`。

### 6. 更新索引
在 `$VAULT/知识库/索引.md` 的对应 section 下加一行。

### 7. git 提交
```bash
cd "$VAULT" && git add -A && git commit -m "收录(媒体): 标题" && git push
```

### 8. 回复
```
✅ 已收录媒体: 标题
📄 原始材料/媒体/<slug>.md
📝 知识库/摘要/<slug>-摘要.md
🔄 已推送 GitHub，请手动同步 Obsidian
```

## 验证清单

- [ ] `write_file` 写入了 `$VAULT/原始材料/媒体/`
- [ ] `write_file` 写入了 `$VAULT/知识库/摘要/`
- [ ] 索引已更新
- [ ] git push 成功
- [ ] **禁止出现：** `skill_manage`