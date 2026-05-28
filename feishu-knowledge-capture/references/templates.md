# Templates

Use these templates for personal Feishu Docs or Wiki case notes. The case document is the primary asset; the index is only a lightweight finding list.

## Personal Case Note

```markdown
# 个人case沉淀：<标题>

> 状态：个人沉淀草稿，需本人加工确认。

## 1. 基本信息
- 关键词：
- 类型：故障 / FAQ / SOP / 故障+FAQ / 线索/Pending / 其他
- 模块：
- 产品/机型：
- 来源：
- 时间范围：
- case key：
- 文档状态：待整理 / 已沉淀 / 需补充 / 可复用 / 已废弃

## 2. 背景
- 客户/地区：
- 使用场景：
- 触发原因：
- 已知限制：

## 3. 问题现象
- 用户或同事原始描述：
- 可观察现象：
- 影响范围：
- 错误码/日志/截图要点：

## 4. 关键信息
| 时间 | 发送人/来源 | 信息类型 | 事实摘录 | 读取状态 |
|---|---|---|---|---|
|  |  | 聊天/截图/卡片/文件/链接 |  | 已读取/未读取/待确认 |

## 5. 判断过程
- 已排除：
- 支持当前判断的证据：
- 仍然不确定：

## 6. 解决方案或当前状态
### 已验证方案

### 临时方案/绕行方式

### 当前状态

## 7. 缺失信息
- 缺失的日志/截图/版本/场景：
- 缺失会影响什么判断：
- 需要谁补充：

## 8. 下一步
- 对客户：
- 对内部：
- 对知识沉淀：

## 9. 参考资料
| 标题 | 链接 | 来源类型 | 读取状态 | 使用原因 |
|---|---|---|---|---|

## 10. 更新记录
| 时间 | 触发来源 | 变更摘要 | 新增证据 | 更新人 |
|---|---|---|---|---|
```

## Pending / Signal Note

Use this when the material is valuable but cannot yet become stable reusable knowledge.

```markdown
# 个人case线索：<标题>

> 状态：Pending/需补充。当前材料还不能沉淀成稳定知识。

## 1. 基本信息
- 关键词：
- 类型：线索/Pending
- 模块：
- 来源：
- 时间范围：
- case key：
- 文档状态：需补充

## 2. 现有事实

## 3. 为什么还不能成为稳定知识
- 未确认原因：
- 未验证方案：
- 缺少关键证据：
- 适用边界不清：

## 4. 建议补充
- 需要补充的信息：
- 建议询问对象：
- 建议下一次检查时间：

## 5. 后续沉淀方向
- 可能成为：故障 / FAQ / SOP / 其他
- 需要满足的闭环条件：

## 6. 来源与参考资料
| 标题/消息 | 链接或ID | 读取状态 | 备注 |
|---|---|---|---|

## 7. 更新记录
| 时间 | 触发来源 | 变更摘要 | 新增证据 | 更新人 |
|---|---|---|---|---|
```

## Personal Index Row

Append or update one row per case document.

```markdown
| 关键词 | 类型 | 模块 | 标题 | 来源 | 文档链接 | 状态 |
|---|---|---|---|---|---|---|
| T300, JSWO-202604220005, 定位异常 | 故障 | 导航/定位 | T300 法国现场定位异常排查 | PUDU T300法国JSWO-202604220005；2026-05-21；thread:omt_xxx | https://... | 已沉淀 |
```

## GitHub Archive Snapshot

Save one Markdown snapshot per case-note version when archive output is enabled. Do not include full raw chat logs.

```markdown
---
case_key: "workorder:JSWO-202604220005"
type: "故障"
version: "v001"
source: "personal-case"
title: "个人case沉淀：<标题>"
feishu_doc_url: "https://..."
status: "已沉淀"
triggered_by: ""
last_updated_by: ""
---

# 个人case沉淀：<标题>

<case note markdown body>
```

## Run Report

```markdown
# 个人知识沉淀运行报告

- 运行时间：
- 来源范围：
- 时间范围：
- 个人文档组：
- 个人索引清单：

## 结果
| 指标 | 数量 |
|---|---:|
| 读取消息 |  |
| 识别 case |  |
| 新建 case 文档 |  |
| 更新 case 文档 |  |
| Pending/需补充 |  |
| 跳过重复 |  |

## 已沉淀
| 关键词 | 类型 | 模块 | 标题 | 来源 | 文档链接 | 状态 |
|---|---|---|---|---|---|---|

## 需补充
| 标题 | 来源 | 缺失信息 | 建议下一步 |
|---|---|---|---|
```
