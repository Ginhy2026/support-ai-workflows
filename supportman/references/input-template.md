# Input Template

## Empty Invocation Behavior

When the user enters only `/supportman`, `$supportman`, or an equivalent invocation without case details, output only this compact template:

```markdown
# 客户问题输入

## 客户原文
> 

## 客户语言
法语 / 英语 / 中文 / 未知：

## 工作来源和目标
- 来源：WhatsApp / 飞书截图 / 飞书消息 / 飞书邮件 / 售前咨询 / 星火计划 / 内部同事请求 / 其他
- 目标：客户回复 / 售前答疑 / 技术确认 / 资料检索 / 升级 / 跟进 / 知识沉淀

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

## 补充参考资料 / SOP
- 链接：飞书 / 语雀 / GitHub / 网页
- 正文摘录：
- 资料类型：官方 SOP / 历史案例 / 内部讨论 / 未验证经验
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

## 工作来源和目标
- 来源：WhatsApp / 飞书截图 / 飞书消息 / 飞书邮件 / 售前咨询 / 星火计划 / 内部同事请求 / 其他
- 目标：客户回复 / 售前答疑 / 技术确认 / 资料检索 / 升级 / 跟进 / 知识沉淀
- 期望输出：客户回复草稿 / 内部说明 / 检索问题 / 升级工单 / 下一步动作 / 沉淀判断

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

## 补充参考资料 / SOP
- 链接：
- 正文摘录：
- 资料类型：官方 SOP / 历史案例 / 内部讨论 / 未验证经验
- 希望重点参考的部分：
```

## Minimal Input

信息很少时也可以只提供：

```markdown
客户原文：

客户语言：

来源/目标：

产品/机型：

场景：

飞书知识问答结果：

补充 SOP/资料：
```

## Targeted Troubleshooting Info Template

Use this when the visible case is a troubleshooting issue but the first screenshot/message lacks key evidence:

```markdown
为了进一步确认问题，请客户补充：

1. 故障发生时间和频率：是每次任务结束都出现，还是偶发？
2. 完整视频：请拍到故障前 5-10 秒、故障发生过程、机器人提示音/屏幕/运动状态。
3. 近距离照片或截图：异常部件、错误码、屏幕提示、现场环境。
4. 机器人信息：SN、软件版本、地图/任务名称。
5. 最近变化：是否刚做过维修、更换部件、升级、移动设备、调整现场环境。
6. 已尝试的基础排查：是否重启机器人、重新执行任务、清洁相关部件、检查是否有异物或松动。
```

## Lightweight Consultation Info Template

Use this when the case is only a feature, usage, pre-sales, or Spark-plan/星火计划 consultation:

```markdown
为了更准确查询资料，请补充：

1. 产品/机型：
2. 使用场景：
3. 想确认的功能、限制或项目目标：
4. 相关客户/项目背景：
5. 如果和版本有关，请补充软件版本：
6. 如果是星火计划/项目推进，请补充希望验证的价值指标或试点目标：
```
