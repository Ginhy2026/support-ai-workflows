# Output Templates

## First-Pass Output

Use when no Feishu knowledge-base result is provided.

```markdown
# 技术支持工作助手 - 首轮

## 1. 工作项类型判断
- 类型：售前/咨询类 / 星火计划/项目类 / 排障类 / 工作跟进类 / 升级敏感类
- 来源渠道：WhatsApp / 飞书截图 / 飞书消息 / 飞书邮件 / 复制文本 / 其他
- 紧急程度：
- 是否涉及安全风险：

## 2. 一句话问题摘要

## 3. 涉及产品/模块
- 产品/机型：
- 模块：
- 关联信息：

## 4. 双源检索结果与适用性判断
> 分别报告飞书资料与第二大脑的实际检索情况；无法自动检索时列出建议检索词，不要把未读取资料当作依据。

| 渠道 | 实际来源/路径或检索词 | 适用性 | 可用信息 | 仍需确认 |
|---|---|---|---|---|
| 飞书 / 第二大脑 / 客户事实 / 历史线索 |  | 直接相关 / 部分相关 / 仅背景参考 / 不适用 / 未检索 |  |  |

## 5. 缺失信息
### 必须补充
-

### 可选补充
-

## 6. 可执行排查步骤
> 有成熟 SOP 时按 Step 1/2/3 输出；无成熟资料时只列通用、低风险检查，不展开长篇猜测。

1.
2.
3.

## 7. 建议问飞书知识问答的问题
1.
2.
3.

## 8. 给客户的初步回复草稿
> 使用客户原语言；基于上面的缺失信息和排查步骤。


## 9. 下一步动作
### 对客户
-

### 对内部
-

### 对知识沉淀
-

## 10. 是否需要内部升级
- 判断：
- 理由：
- 建议升级对象/方向：

## 11. 第二大脑反馈建议
- 判断：不沉淀 / 待闭环后沉淀 / 建议创建候选
- 反馈类型：新知识 / 纠正 / 冲突 / 知识缺口 / 真实结果反馈
- 可复用结论：
- 来源与证据：
- 与现有知识的关系：
- 适用范围与例外：
- 仍需验证：
- 建议产物：FAQ / SOP / checklist / case / rule update / knowledge-gap
```

## Screenshot Or Chat First-Pass Output

Use when the user provides a WhatsApp screenshot, Feishu screenshot, Feishu card, video screenshot, email screenshot, or short pasted chat instead of a filled form.

```markdown
# 技术支持工作助手 - 截图/聊天首轮

## 1. 从截图/聊天中提取到的信息
- 客户语言：
- 客户/项目：
- 来源渠道：WhatsApp / 飞书截图 / 飞书消息 / 飞书邮件 / 复制文本 / 其他
- 产品/机型：
- 可见现象：
- 客户诉求：
- 已知历史：

## 2. 工作项形态判断
- 形态：售前/咨询类 / 星火计划/项目类 / 排障类 / 工作跟进类 / 升级敏感类
- 理由：
- 是否需要完整输入模板：是 / 否

## 3. 一句话问题摘要

## 4. 假设与推断（内部）
> 咨询类可省略；排障类/升级敏感类必须填写。不要把本节内容直接发给客户。
> 如果没有成熟资料和足够证据，本节保持简短；不要为了填满模板扩展无依据分析。

| 假设 | 依据 | 置信度 |
|---|---|---|
|  |  | 高 / 中 / 低 |

## 5. 双源检索结果与适用性判断
> 分别报告飞书资料与第二大脑的实际检索情况；如未检索，列出建议检索词。

| 渠道 | 实际来源/路径或检索词 | 适用性 | 可用信息 | 仍需确认 |
|---|---|---|---|---|
| 飞书 / 第二大脑 / 客户事实 / 历史线索 |  | 直接相关 / 部分相关 / 仅背景参考 / 不适用 / 未检索 |  |  |

## 6. 当前可以直接问飞书知识问答的问题
1.
2.
3.

## 7. 需要补充的信息
> 咨询类只列最少必要信息；排障类列针对性排障信息。

### 必须补充
-

### 可选补充
-

### 内部需要查询/确认
-

## 8. 可执行排查步骤
> 有成熟 SOP 时按 Step 1/2/3 输出；无成熟资料时只列通用、低风险检查。

1.
2.
3.

## 9. 给客户的初步回复草稿
> 使用客户原语言；排障类可包含基础排查和补充信息请求。
> 首轮不要承诺 root cause、resolution plan 或具体时限。


## 10. 下一步动作
### 对客户
-

### 对内部
-

### 对知识沉淀
-

## 11. 是否需要内部升级
- 判断：
- 理由：

## 12. 第二大脑反馈建议
- 判断：不沉淀 / 待闭环后沉淀 / 建议创建候选
- 反馈类型：新知识 / 纠正 / 冲突 / 知识缺口 / 真实结果反馈
- 可复用结论：
- 来源与证据：
- 与现有知识的关系：
- 适用范围与例外：
- 仍需验证：
- 建议产物：FAQ / SOP / checklist / case / rule update / knowledge-gap
```

## Second-Pass Output

Use when Feishu knowledge-base result, SOP content, Yuque article, Feishu doc, web page, or other supplemental reference is provided.

```markdown
# 技术支持工作助手 - 二轮

## 1. 资料整理
- 飞书知识库结果：
- 第二大脑知识路径：
- 补充 SOP/外部资料：
- 与本案直接相关的结论：
- 推荐操作：
- 注意事项：

## 2. 资料适用性判断
| 渠道 | 实际来源/路径 | 适用性 | 匹配点 | 不匹配/仍需确认 |
|---|---|---|---|---|
| 飞书 / 第二大脑 / 客户事实 / 历史线索 |  | 直接相关 / 部分相关 / 仅背景参考 / 不适用 |  |  |

## 3. 缺失信息
### 必须补充
-

### 可选补充
-

## 4. 可执行排查步骤
> 有成熟 SOP 时按 Step 1/2/3 输出；涉及万用表、短接、拆机、测电压、换件时注明由合格技术人员执行。

1.
2.
3.

## 5. 简要技术判断
- 根因方向：
- 置信度：高 / 中 / 低
- 依据：
- 仍不确定的信息：

## 6. 给客户的正式回复草稿
> 使用客户原语言；不暴露内部资料来源、历史案例细节或未验证推断。


## 7. 中文内部说明
- 客户问题：
- 已核对资料：
- 建议处理：
- 风险/注意事项：

## 8. 下一步动作
### 对客户
-

### 对内部
-

### 对知识沉淀
-

## 9. 内部升级工单描述
> 如不需要升级，写“暂不需要升级”，并说明原因。

**标题：**

**客户/项目背景：**

**产品/机型：**

**问题现象：**

**已收集信息：**

**已尝试/建议的排查：**

**飞书知识问答参考：**

**需要支持团队确认的问题：**

**紧急程度和影响：**

## 10. 第二大脑反馈建议
- 判断：不沉淀 / 待闭环后沉淀 / 建议创建候选
- 反馈类型：新知识 / 纠正 / 冲突 / 知识缺口 / 真实结果反馈
- 可复用结论：
- 来源与证据：
- 与现有知识的关系：
- 适用范围与例外：
- 仍需验证：
- 建议产物：FAQ / SOP / checklist / case / rule update / knowledge-gap

> 判断为“建议创建候选”时，自然询问用户是否交给 `$feishu-knowledge-capture`；不要在 SupportMan 内直接创建候选。
```

## Customer Reply Tone Snippets

English:

```markdown
Thanks for the details. Could you please check these points first?

If the issue is still there afterward, please send us the robot SN, software version, error message, and a short video or log screenshot. We'll check it further with the technical team.
```

French:

```markdown
Merci pour ces informations. Pourriez-vous d'abord verifier les points suivants ?

Si le probleme persiste ensuite, pourriez-vous nous envoyer le numero de serie du robot, la version logicielle, le message d'erreur et, si possible, une courte video ou une capture des journaux ? Nous verifierons cela avec l'equipe technique.
```

Chinese:

```markdown
收到，麻烦先帮忙确认下面几点：

如果检查后问题还在，请把机器人 SN、软件版本、错误提示截图以及相关日志或视频发给我们，我们再和技术团队进一步确认。
```
