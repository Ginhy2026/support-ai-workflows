# Candidate Knowledge Templates

Use these templates for Feishu Docs or Wiki candidate pages. Keep the status line unchanged until a human reviewer approves the content.

## Fault Candidate

```markdown
# 候选故障知识：<标题>

> 状态：候选草稿，需人工审核后再进入正式知识库。

## 1. 基本信息
- 类型：故障
- 唯一键：
- 工单号：
- 来源群：
- 来源 thread/message：
- 技术支持负责人：
- 部门 Leader：
- 产品/中台服务代表：
- 触发人：
- 贡献人：
- 最后更新人：
- 产品/机型：
- 模块：
- 客户/地区：
- 创建日期：
- 成熟度：M0 原始线索 / M1 初步判断 / M2 候选草稿 / M3 已审核候选 / M4 正式知识
- 适用性边界：
- 不适用场景：

## 2. 故障现象

## 3. 分析和排查
| 步骤 | 现象/证据 | 判断 | 可信度 |
|---|---|---|---|

## 4. 最终原因
| 结论 | 依据 | 可信度 |
|---|---|---|

## 5. 解决方案
### 已验证方案

### 临时方案

### 需要升级的条件

## 6. 验证结果/回访状态

## 7. 客户回复模板

## 8. 内部注意事项
- 风险：
- 前置条件：
- 不要对客户承诺：
- 需要保留的证据：

## 9. 来源与可信度
- 来源消息：
- 截图/卡片文本是否完整可读：
- 资料成熟度：
- 当前案例适用性：A3 直接适用 / A2 部分适用 / A1 背景参考 / A0 不适用
- 已验证：
- 待确认：
- 仅初步判断：

## 10. 审核
- 审核状态：待审核
- 发布建议：适合 / 条件适合 / 暂不适合
- 发布前需补充：
- 审核通过后目标成熟度：M3 已审核候选 / M4 正式知识

## 11. 更新记录
| 版本 | 时间 | 触发来源 | 变更摘要 | 新增证据 | 处理人/机器人 | 来源消息 |
|---|---|---|---|---|---|---|
| v001 | YYYY-MM-DD HH:mm | 自动/手动 | 初次创建候选知识 |  |  |  |
```

## FAQ Candidate

```markdown
# 候选 FAQ：<问题>

> 状态：候选草稿，需人工审核后再进入正式知识库。

## 1. 问题

## 2. 答案

## 3. 适用范围
- 产品/机型：
- 模块：
- 版本/配置限制：
- 不适用场景：
- 成熟度：M0 原始线索 / M1 初步判断 / M2 候选草稿 / M3 已审核候选 / M4 正式知识
- 适用性边界：

## 4. 注意事项

## 5. 来源与可信度
- 唯一键：
- 来源群：
- 来源 thread/message：
- 工单号：
- 技术支持负责人：
- 部门 Leader：
- 产品/中台服务代表：
- 触发人：
- 贡献人：
- 最后更新人：
- 截图/卡片文本是否完整可读：
- 资料成熟度：
- 当前案例适用性：A3 直接适用 / A2 部分适用 / A1 背景参考 / A0 不适用
- 可信度：已验证 / 待确认 / 仅初步判断

## 6. 审核
- 审核状态：待审核
- 发布建议：适合 / 条件适合 / 暂不适合
- 发布前需补充：
- 审核通过后目标成熟度：M3 已审核候选 / M4 正式知识

## 7. 更新记录
| 版本 | 时间 | 触发来源 | 变更摘要 | 新增证据 | 处理人/机器人 | 来源消息 |
|---|---|---|---|---|---|---|
| v001 | YYYY-MM-DD HH:mm | 自动/手动 | 初次创建候选 FAQ |  |  |  |
```

## SOP Candidate

```markdown
# 候选 SOP：<标题>

> 状态：候选草稿，需人工审核后再进入正式知识库或流程库。

## 1. 适用场景

## 2. 触发条件

## 3. 角色分工

## 4. 成熟度与适用边界
- 成熟度：M0 原始线索 / M1 初步判断 / M2 候选草稿 / M3 已审核候选 / M4 正式知识
- 适用产品/模块：
- 适用条件：
- 不适用场景：

## 5. 处理流程
1.
2.
3.

## 6. 排查步骤
| 步骤 | 操作 | 预期结果 | 升级条件 |
|---|---|---|---|

## 7. 解决方案/回退方案

## 8. 客户回复模板

## 9. 内部注意事项

## 10. 来源与审核
- 唯一键：
- 来源群：
- 来源 thread/message：
- 工单号：
- 技术支持负责人：
- 部门 Leader：
- 产品/中台服务代表：
- 触发人：
- 贡献人：
- 最后更新人：
- 当前案例适用性：A3 直接适用 / A2 部分适用 / A1 背景参考 / A0 不适用
- 审核状态：待审核
- 发布前需补充：
- 审核通过后目标成熟度：M3 已审核候选 / M4 正式知识

## 11. 更新记录
| 版本 | 时间 | 触发来源 | 变更摘要 | 新增证据 | 处理人/机器人 | 来源消息 |
|---|---|---|---|---|---|---|
| v001 | YYYY-MM-DD HH:mm | 自动/手动 | 初次创建候选 SOP |  |  |  |
```

## Pending Record

Use this in the daily report, not as a full Wiki page unless the user asks for a pending queue.

```markdown
| 标题/线索 | 来源 | 工单号 | 成熟度 | 当前结论 | 缺失信息 | 建议动作 |
|---|---|---|---|---|---|---|
```

## Shared Index Row

Append one row per generated candidate document.

```markdown
| 唯一键 | 日期 | 类型 | 成熟度 | 产品/模块 | 工单号 | 来源 thread | 标题 | 来源群 | 技术支持负责人 | 部门 Leader | 产品/中台服务代表 | 触发人 | 贡献人 | 最后更新人 | 候选文档链接 | GitHub归档 | 版本号 | 最后更新时间 | 最近变更摘要 | 审核状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| thread:omt_xxx | YYYY-MM-DD | 故障/FAQ/SOP/待补充 | M2 候选草稿 |  |  | omt_xxx |  |  | 待确认 | 待确认 | 待确认 |  |  |  |  | knowledge-archive/.../v001.md | v001 | YYYY-MM-DD HH:mm | 初次创建 | 待审核 |
```

## GitHub Archive Frontmatter

Save one Markdown snapshot per candidate version. Do not include full raw chat logs.

```markdown
---
candidate_key: "workorder:JSWO-202604220005"
type: "故障"
version: "v001"
source: "JSWO工单群"
title: "<标题>"
feishu_doc_url: "https://..."
created_at: "2026-05-22T18:30:00+08:00"
updated_at: "2026-05-22T18:30:00+08:00"
review_status: "待审核"
maturity: "M2 候选草稿"
applicability: ""
support_owner: "待确认"
leader: "待确认"
service_representative: "待确认"
triggered_by: ""
contributors: ""
last_updated_by: ""
---

# 候选故障知识：<标题>

<candidate markdown body>
```

## GitHub Archive Layout

```text
knowledge-archive/
  support-triage/
    YYYY-MM-DD/
      thread-omt_xxx/
        v001.md
        metadata.json
      run-report.md
  jswo/
    JSWO-202604220005/
      v001.md
      v002.md
      metadata.json
  manual-runs/
    YYYY-MM-DD/
      hash-xxx/
        v001.md
        metadata.json
      run-report.md
```

## Run Report Archive

```markdown
# 知识沉淀运行报告

- 运行时间：
- 触发方式：自动任务 / 手动调用
- 来源范围：support-triage / JSWO工单群 / 所有群聊 / 所有私聊 / 指定群
- 时间范围：
- 飞书候选目录：
- 飞书索引文档：

## 结果
| 指标 | 数量 |
|---|---:|
| 读取消息 |  |
| 识别 case |  |
| 新建候选 |  |
| 更新候选 |  |
| 跳过重复 |  |
| 待补充 |  |
| GitHub 快照 |  |

## 明细
| 唯一键 | 类型 | 标题 | 飞书链接 | GitHub版本 | 处理结果 |
|---|---|---|---|---|---|
```
