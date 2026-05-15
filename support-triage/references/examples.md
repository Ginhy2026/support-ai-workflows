# Examples

## Example 1: First-Pass, English Customer

### Input

```markdown
客户原文：
Hi, our robot cannot return to the charging dock. It stops about 30 cm before the dock and says positioning failed. We cleaned the dock area but it still happens.

客户语言：英语
客户背景：海外餐厅客户，晚高峰影响运营
产品/机型：配送机器人
问题发生场景：完成配送任务后自动回充失败
图片/日志/错误码：提示 positioning failed，无日志
我的初步判断：可能是充电桩附近定位或地图问题
飞书知识问答返回结果：
```

### Output

```markdown
# 技术支持分诊 - 首轮

## 1. 问题类型判断
- 类型：充电/回充 + 定位导航
- 紧急程度：中高，已影响门店运营
- 是否涉及安全风险：暂未体现

## 2. 一句话问题摘要
配送机器人完成任务后无法自动回到充电桩，在距离充电桩约 30 cm 处停止并提示 positioning failed。

## 3. 涉及产品/模块
- 产品/机型：配送机器人
- 模块：自动回充、定位、地图、充电桩环境
- 关联信息：客户已清理充电桩周边，但问题仍存在

## 4. 可能原因排序
1. 充电桩附近定位特征不足、环境变化或反光/遮挡导致定位失败。
2. 地图中充电桩点位或回充路径与现场实际位置不一致。
3. 机器人定位传感器、底盘回充动作或充电桩识别存在异常。

## 5. 需要客户补充的信息
- 机器人 SN、软件版本、地图名称。
- 问题是每次发生还是偶发。
- 充电桩周边 1-2 米环境照片和机器人停止位置视频。
- 最近是否移动过充电桩、更新过地图、改动过现场布置。
- App/后台是否有更完整的错误日志或错误码。

## 6. 建议问飞书知识问答的问题
1. 配送机器人自动回充时在充电桩前约 30 cm 停止并提示 positioning failed，常见原因和排查步骤是什么？
2. 配送机器人充电桩附近定位失败时，如何检查充电桩点位、地图、现场环境和传感器状态？
3. 如果清理充电桩周边后仍无法回充，哪些日志、照片或视频需要收集并升级给技术支持？

## 7. 是否需要内部升级
- 判断：建议先收集信息；如高频复现或客户运营受影响明显，建议升级。
- 理由：涉及回充和定位，可能需要地图/日志确认。
- 建议升级对象/方向：导航定位或机器人技术支持团队。

## 8. 给客户的初步回复草稿
Thank you for the details. We recommend checking a few points first:

- Please confirm whether the charging dock has been moved recently or whether the layout around the dock has changed.
- Please keep about 1-2 meters around the dock clear and avoid reflective or moving objects near the docking area.
- Please try restarting the robot and sending it back to the dock again.

If the issue persists, could you please send us the robot SN, software version, a short video showing where the robot stops, and photos of the charging dock area? We will check further with the technical team.

## 9. 是否建议后续沉淀为 FAQ
- 判断：建议沉淀。
- 建议 FAQ 主题：机器人自动回充失败并提示定位失败的排查方法。
- 沉淀价值：高频场景，适合标准化信息收集和初步排查。
```

## Example 2: Second-Pass, French Customer

### Input

```markdown
客户原文：
Bonjour, le robot affiche E203 apres la mise a jour et ne demarre plus les taches.

客户语言：法语
客户背景：法国酒店客户
产品/机型：配送机器人
问题发生场景：升级后无法启动任务
图片/日志/错误码：E203
我的初步判断：可能和版本升级后任务模块初始化失败有关
飞书知识问答返回结果：
E203 通常表示任务服务初始化失败或配置未同步。建议检查网络连接、重新登录账号、同步配置；若升级后持续出现，需收集 SN、版本号、升级时间、日志并升级研发确认。
```

### Output

```markdown
# 技术支持分诊 - 二轮

## 1. 飞书答案整理
- 与本案直接相关的结论：E203 通常与任务服务初始化失败或配置未同步有关。
- 推荐操作：检查网络连接、重新登录账号、同步配置。
- 注意事项：如果升级后持续出现，需要收集 SN、版本号、升级时间和日志。
- 与客户场景不完全匹配或仍需确认的点：需要确认客户是否已经完成配置同步，以及 E203 是否每次启动任务都出现。

## 2. 最终技术判断
- 判断：该问题可能与升级后任务服务配置未同步或初始化异常有关。
- 依据：错误码 E203 与飞书知识问答中的任务服务初始化/配置同步说明匹配。
- 仍不确定的信息：机器人 SN、版本号、升级时间、网络状态、同步配置结果、完整日志。

## 3. 给客户的正式回复草稿
Bonjour, merci pour votre retour.

Le code E203 peut etre lie a l'initialisation du service de taches ou a une configuration qui n'a pas encore ete synchronisee apres la mise a jour. Nous vous recommandons de verifier d'abord les points suivants :

1. Verifier que le robot est bien connecte au reseau.
2. Vous deconnecter puis vous reconnecter au compte de gestion.
3. Relancer la synchronisation de la configuration, puis essayer de demarrer une tache a nouveau.

Si le code E203 apparait toujours apres ces verifications, merci de nous envoyer le numero de serie du robot, la version logicielle actuelle, l'heure approximative de la mise a jour et les journaux disponibles. Nous ferons une verification plus approfondie avec l'equipe technique.

## 4. 中文内部说明
- 客户问题：法国酒店客户反馈机器人升级后显示 E203，无法启动任务。
- 已核对资料：飞书知识问答说明 E203 通常为任务服务初始化失败或配置未同步。
- 建议处理：先让客户确认网络、重新登录账号、同步配置；若仍复现则收集 SN、版本号、升级时间和日志。
- 风险/注意事项：升级后持续出现可能需要研发确认任务服务初始化或配置下发状态。

## 5. 内部升级工单描述
暂不立即升级；建议客户完成基础排查后，如仍复现再升级。

**标题：** 法国酒店客户配送机器人升级后 E203，无法启动任务

**客户/项目背景：** 法国酒店客户，升级后影响任务启动。

**产品/机型：** 配送机器人

**问题现象：** 升级后显示 E203，无法启动任务。

**已收集信息：** 错误码 E203；缺少 SN、版本号、升级时间、日志。

**已尝试/建议的排查：** 检查网络、重新登录账号、同步配置。

**飞书知识问答参考：** E203 通常表示任务服务初始化失败或配置未同步；升级后持续出现需收集信息并升级研发。

**需要支持团队确认的问题：** 若排查后仍复现，需确认配置同步状态和任务服务初始化日志。

**紧急程度和影响：** 中高，客户无法启动任务。

## 6. FAQ 草稿
**问题：** 机器人升级后显示 E203，无法启动任务，如何处理？

**适用产品/模块：** 配送机器人；任务服务、配置同步、升级后检查。

**典型现象：** 升级后启动任务失败，界面显示 E203。

**可能原因：** 任务服务初始化失败；配置未同步；网络或账号状态导致配置未正常下发。

**处理步骤：**
1. 检查机器人网络连接。
2. 重新登录管理账号。
3. 同步配置后重新启动任务。
4. 如仍失败，收集 SN、版本号、升级时间和日志。

**需要升级的条件：** 基础排查后仍持续复现，或多个机器人升级后同时出现 E203。

**资料来源/备注：** 基于飞书知识问答返回结果，需后续结合实际日志验证。
```
