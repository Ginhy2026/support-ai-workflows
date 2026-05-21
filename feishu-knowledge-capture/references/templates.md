# Candidate Knowledge Templates

Use these templates for Feishu Docs or Wiki candidate pages. Keep the status line unchanged until a human reviewer approves the content.

## Fault Candidate

```markdown
# 候选故障知识：<标题>

> 状态：候选草稿，需人工审核后再进入正式知识库。

## 1. 基本信息
- 类型：故障
- 工单号：
- 来源群：
- 来源 thread/message：
- 负责人/同事：
- 产品/机型：
- 模块：
- 客户/地区：
- 创建日期：

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
- 已验证：
- 待确认：
- 仅初步判断：

## 10. 审核
- 审核状态：待审核
- 发布建议：适合 / 条件适合 / 暂不适合
- 发布前需补充：
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

## 4. 注意事项

## 5. 来源与可信度
- 来源群：
- 来源 thread/message：
- 工单号：
- 负责人/同事：
- 截图/卡片文本是否完整可读：
- 可信度：已验证 / 待确认 / 仅初步判断

## 6. 审核
- 审核状态：待审核
- 发布建议：适合 / 条件适合 / 暂不适合
- 发布前需补充：
```

## SOP Candidate

```markdown
# 候选 SOP：<标题>

> 状态：候选草稿，需人工审核后再进入正式知识库或流程库。

## 1. 适用场景

## 2. 触发条件

## 3. 角色分工

## 4. 处理流程
1.
2.
3.

## 5. 排查步骤
| 步骤 | 操作 | 预期结果 | 升级条件 |
|---|---|---|---|

## 6. 解决方案/回退方案

## 7. 客户回复模板

## 8. 内部注意事项

## 9. 来源与审核
- 来源群：
- 来源 thread/message：
- 工单号：
- 负责人/同事：
- 审核状态：待审核
- 发布前需补充：
```

## Pending Record

Use this in the daily report, not as a full Wiki page unless the user asks for a pending queue.

```markdown
| 标题/线索 | 来源 | 工单号 | 缺失信息 | 建议动作 |
|---|---|---|---|---|
```

## Shared Index Row

Append one row per generated candidate document.

```markdown
| 日期 | 类型 | 产品/模块 | 工单号 | 标题 | 来源群 | 负责人/同事 | 候选文档链接 | 审核状态 |
|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | 故障/FAQ/SOP/待补充 |  |  |  |  |  |  | 待审核 |
```
