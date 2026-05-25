# Examples

## Example 1: First Pass With No Mature Reference

### Input

```markdown
客户原文：
Hi, our robot cannot return to the charging dock. It stops about 30 cm before the dock and says positioning failed. We cleaned the dock area but it still happens.

客户语言：英语
客户背景：海外餐厅客户，晚高峰影响运营
产品/机型：配送机器人
问题发生场景：完成配送任务后自动回充失败
图片/日志/错误码：提示 positioning failed，无日志
飞书知识问答返回结果：
```

### Output Shape

```markdown
# 技术支持分诊 - 首轮

## 1. 问题类型判断
- 类型：排障类，回充/定位相关
- 紧急程度：中高，影响运营
- 是否涉及安全风险：暂未体现

## 2. 一句话问题摘要
配送机器人完成任务后无法自动回到充电桩，在距离充电桩约 30 cm 处停止并提示 positioning failed。

## 3. 涉及产品/模块
- 产品/机型：配送机器人
- 模块：自动回充、定位、地图、充电桩环境

## 4. 资料检索结果与适用性判断
| 来源/检索词 | 适用性 | 可用信息 | 仍需确认 |
|---|---|---|---|
| 配送机器人 回充 30cm positioning failed 排查步骤 | 未检索 | 可作为飞书检索词 | 需要知识库或日志验证 |
| 配送机器人 充电桩附近 定位失败 地图 点位 | 未检索 | 可作为飞书检索词 | 需要知识库或地图信息验证 |

## 5. 缺失信息
### 必须补充
- 机器人 SN、软件版本、地图名称。
- 问题是每次发生还是偶发。
- 充电桩周边 1-2 米环境照片和机器人停止位置视频。
- 最近是否移动过充电桩、更新过地图、改动过现场布置。

### 可选补充
- App/后台是否有更完整的错误日志或错误码。

## 6. 可执行排查步骤
> 当前没有成熟资料支撑，只给通用、低风险检查。

1. 确认充电桩位置近期是否移动，周边是否有反光、遮挡或临时物品。
2. 保持充电桩周边 1-2 米环境稳定并重新尝试回充。
3. 重启机器人后再次执行回充测试，并记录停止位置和屏幕提示。

## 7. 建议问飞书知识问答的问题
1. 配送机器人自动回充时在充电桩前约 30 cm 停止并提示 positioning failed，常见原因和排查步骤是什么？
2. 配送机器人充电桩附近定位失败时，如何检查充电桩点位、地图、现场环境和传感器状态？
3. 如果清理充电桩周边后仍无法回充，哪些日志、照片或视频需要收集并升级给技术支持？

## 8. 给客户的初步回复草稿
Thank you for the details. We recommend checking a few basic points first:

1. Please confirm whether the charging dock has been moved recently or whether the layout around the dock has changed.
2. Please keep about 1-2 meters around the dock clear and avoid reflective or moving objects near the docking area.
3. Please restart the robot and try sending it back to the dock again.

If the issue persists, could you please send us the robot SN, software version, a short video showing where the robot stops, and photos of the charging dock area? We will verify the next steps after checking this information.

## 9. 是否需要内部升级
- 判断：先收集信息；若高频复现或运营影响明显，建议升级。
- 理由：涉及回充和定位，可能需要地图/日志确认。

## 10. 是否建议交给 case-capture 沉淀
- 判断：暂不建议，缺少确认资料和最终解决方案。
- 建议沉淀方向：闭环后可沉淀“自动回充失败并提示 positioning failed 的排查信息收集”。
```

## Example 2: Second Pass With SOP Reference

### Input

```markdown
客户原文：
Bonjour, la station d'eau reste bleue et ne passe pas au vert. Le robot CC1 ne detecte pas le reservoir pendant le changement d'eau. Nous avons deja mis a jour le robot et reconnecte la station.

客户语言：法语
产品/机型：CC1 + 移动水站
飞书知识问答返回结果：
蓝灯常亮可能表示基座和固定式工作站电路连接正常，但移动水箱未和基座建立连接。可能与水路传感器接口接触不良有关。

补充 SOP/资料：
【water tank】l'erreur1003：移动水箱连接处进水导致接触不良。排查步骤包括测水箱对接模组电阻 4kΩ/3kΩ/2kΩ，短接基座金属 Pin 看是否闪红灯，检查基座 Pin 针和水箱电极脏污/磨损，必要时拆检水箱/基座对接模组和测基座 Pin 间约 2.2V 电压。
```

### Output Shape

```markdown
# 技术支持分诊 - 二轮

## 1. 资料整理
- 飞书知识库结果：蓝灯常亮与移动水箱未和基座建立连接相关，方向指向接口接触或通信问题。
- 补充 SOP/外部资料：1003 SOP 给出水箱对接模组、电极、基座 Pin、电压和内部进水腐蚀检查步骤。
- 与本案直接相关的结论：客户现象“蓝灯不变绿 + CC1 无法检测储水器”与 SOP 症状高度匹配。
- 推荐操作：先做外观和清洁检查，再由合格技术人员执行电阻、短接和电压测试。
- 注意事项：短接、拆机、测电压和换件需由合格技术人员执行。

## 2. 资料适用性判断
| 来源 | 适用性 | 匹配点 | 不匹配/仍需确认 |
|---|---|---|---|
| 飞书知识库蓝灯说明 | 直接相关 | 蓝灯不变绿、移动水箱未连接、接口接触问题 | 需确认是否同时出现 1003 |
| 1003 SOP | 直接相关 | 移动水站/水箱检测失败、接触不良、排查步骤明确 | 需客户提供 1003 报错截图或完整视频 |

## 3. 缺失信息
### 必须补充
- 报错 1003 的界面截图或完整换水流程视频。
- 故障是否每次换水都出现。
- 基座 Pin 针和水箱电极的近距离照片。

### 可选补充
- 机器人和水站 SN。
- 故障首次出现时间和最近是否清洁/移动/维修过水站。

## 4. 可执行排查步骤
1. 先检查并清洁基座 Pin 针和水箱电极，确认无脏污、磨损、氧化或水迹。
2. 确认水箱和基座完全对齐并重新执行换水流程，拍摄完整视频。
3. 由合格技术人员测量水箱对接模组电阻是否为 4kΩ / 3kΩ / 2kΩ 之一，误差 ±5%。
4. 由合格技术人员短接基座金属 Pin：若闪红灯，基座初步正常；若仍蓝灯，优先检查基座对接模组。
5. 如仍异常，由合格技术人员测基座 Pin 间电压是否约 2.2V，并拆检水箱/基座对接模组是否进水、腐蚀或连接器松脱。

## 5. 简要技术判断
- 根因方向：移动水箱/基座对接接口接触不良、进水腐蚀或对接模组异常。
- 置信度：高
- 依据：客户现象与飞书蓝灯说明和 1003 SOP 排查路径匹配；软件升级和重新连接未解决，硬件接口方向更优先。
- 仍不确定的信息：是否有 1003 截图、具体故障件在水箱侧还是基座侧。

## 6. 给客户的正式回复草稿
Bonjour, merci pour votre retour detaille.

D'apres le symptome de la station qui reste bleue et ne passe pas au vert, nous recommandons de verifier en priorite la zone de connexion entre le reservoir mobile et le socle.

1. Veuillez verifier et nettoyer delicatement les contacts du socle et du reservoir avec un chiffon sec et non pelucheux.
2. Veuillez confirmer que le reservoir est bien positionne et completement en contact avec le connecteur du socle, puis refaire un essai de changement d'eau.
3. Si le probleme persiste, merci de nous envoyer une video complete de l'operation de docking/changement d'eau, ainsi qu'une photo claire des contacts du socle et du reservoir.

Pour les controles electriques ou le demontage du module de connexion, merci de les faire realiser par un technicien qualifie. Ces controles permettront de confirmer si le probleme vient du reservoir, du socle ou du module de connexion.

Cordialement,

## 7. 中文内部说明
- 客户问题：CC1 移动水站蓝灯不变绿，机器人换水时无法检测储水器。
- 已核对资料：飞书蓝灯说明 + 1003 SOP，均指向水箱/基座对接接口接触或通信问题。
- 建议处理：先让客户清洁和拍摄完整视频；电阻/短接/电压/拆检由合格技术人员执行。
- 风险/注意事项：不要直接对客户承诺更换件；需通过测试区分水箱侧和基座侧。

## 8. 内部升级工单描述
暂不立即升级；如客户按 SOP 完成检查后仍无法确认故障点，或更换水箱/基座后仍异常，再升级。

## 9. 是否建议交给 case-capture 沉淀
- 判断：建议在案例闭环后交给 `$case-capture`。
- 建议沉淀方向：CC1 移动水站蓝灯不变绿/1003 的标准排查 SOP。
```
