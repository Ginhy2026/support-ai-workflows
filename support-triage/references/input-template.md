# Input Template

## Empty Invocation Behavior

When the user enters only `/support-triage`, `$support-triage`, or an equivalent invocation without case details, output only this compact template:

```markdown
# 客户问题输入

## 客户原文
> 

## 客户语言
法语 / 英语 / 中文 / 未知：

## 客户背景
- 国家/地区：
- 客户类型/项目：
- 紧急程度：

## 产品/机型

## 问题发生场景
- 发生时间：
- 发生地点：
- 操作/触发条件：
- 影响范围：

## 图片/日志/错误码
- 图片/视频：
- 日志：
- 错误码/提示语：
- 机器人 SN / 版本：

## 我的初步判断

## 飞书知识问答返回结果
> 首轮留空；二轮粘贴飞书知识问答结果。
```

Do not add explanation before or after the template unless the user explicitly asks.

## Full Intake Template

Use this when the user asks for a more complete intake form:

```markdown
# 客户问题输入

## 客户原文
> 粘贴 WhatsApp / 飞书邮箱 / 飞书消息原文

## 客户语言
法语 / 英语 / 中文 / 未知

## 客户背景
- 国家/地区：
- 客户类型：
- 项目/门店/场景：
- 紧急程度：
- 历史相关问题：

## 产品/机型

## 问题发生场景
- 发生时间：
- 发生地点：
- 操作步骤：
- 触发条件：
- 影响范围：

## 图片/日志/错误码
- 图片说明：
- 日志片段：
- 错误码/提示语：
- 机器人 SN / 版本信息：

## 我的初步判断

## 飞书知识问答返回结果
> 首轮处理时留空；二轮处理时粘贴知识问答结果。
```

## Minimal Input

信息很少时也可以只提供：

```markdown
客户原文：

客户语言：

产品/机型：

场景：

飞书知识问答结果：
```
