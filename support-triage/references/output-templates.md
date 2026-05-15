# Output Templates

## First-Pass Output

Use when no Feishu knowledge-base result is provided.

```markdown
# 技术支持分诊 - 首轮

## 1. 问题类型判断
- 类型：
- 紧急程度：
- 是否涉及安全风险：

## 2. 一句话问题摘要

## 3. 涉及产品/模块
- 产品/机型：
- 模块：
- 关联信息：

## 4. 可能原因排序
1. 
2. 
3. 

## 5. 需要客户补充的信息
- 

## 6. 建议问飞书知识问答的问题
1. 
2. 
3. 

## 7. 是否需要内部升级
- 判断：
- 理由：
- 建议升级对象/方向：

## 8. 给客户的初步回复草稿
> 使用客户原语言


## 9. 是否建议后续沉淀为 FAQ
- 判断：
- 建议 FAQ 主题：
- 沉淀价值：
```

## Screenshot Or Chat First-Pass Output

Use when the user provides a WhatsApp/Feishu screenshot, video screenshot, or short pasted chat instead of a filled form.

```markdown
# 技术支持分诊 - 截图/聊天首轮

## 1. 从截图/聊天中提取到的信息
- 客户语言：
- 客户/项目：
- 产品/机型：
- 可见现象：
- 客户诉求：
- 已知历史：

## 2. 问题形态判断
- 形态：咨询类 / 排障类 / 升级敏感类
- 理由：
- 是否需要完整输入模板：是 / 否

## 3. 一句话问题摘要

## 4. 当前可以直接问飞书知识问答的问题
1. 
2. 
3. 

## 5. 需要客户补充的信息
> 咨询类只列最少必要信息；排障类列针对性排障信息。

- 

## 6. 是否需要内部升级
- 判断：
- 理由：

## 7. 给客户的初步回复草稿
> 使用客户原语言；排障类可包含基础排查和补充信息请求。


## 8. 是否建议后续沉淀为 FAQ
- 判断：
- 建议 FAQ 主题：
```

## Second-Pass Output

Use when Feishu knowledge-base result is provided.

```markdown
# 技术支持分诊 - 二轮

## 1. 飞书答案整理
- 与本案直接相关的结论：
- 推荐操作：
- 注意事项：
- 与客户场景不完全匹配或仍需确认的点：

## 2. 最终技术判断
- 判断：
- 依据：
- 仍不确定的信息：

## 3. 给客户的正式回复草稿
> 使用客户原语言


## 4. 中文内部说明
- 客户问题：
- 已核对资料：
- 建议处理：
- 风险/注意事项：

## 5. 内部升级工单描述
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

## 6. FAQ 草稿
> 如不适合沉淀，写“不建议沉淀”，并说明原因。

**问题：**

**适用产品/模块：**

**典型现象：**

**可能原因：**

**处理步骤：**

**需要升级的条件：**

**资料来源/备注：**
```

## Customer Reply Tone Snippets

English:

```markdown
Thank you for the details. We recommend checking the following points first:

If the issue persists after these checks, please send us the robot SN, software version, error message, and a short video or log screenshot. We will verify further with the technical team.
```

French:

```markdown
Merci pour ces informations. Nous recommandons de verifier d'abord les points suivants :

Si le probleme persiste apres ces verifications, merci de nous envoyer le numero de serie du robot, la version logicielle, le message d'erreur et, si possible, une courte video ou une capture des journaux. Nous ferons une verification plus approfondie avec l'equipe technique.
```

Chinese:

```markdown
感谢反馈。建议先按以下方向做基础确认：

如果检查后问题仍然存在，请补充机器人 SN、软件版本、错误提示截图以及相关日志/视频，我们会进一步和技术团队确认。
```
