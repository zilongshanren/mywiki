---
tags: [telemetry, analytics, game-design, indie, player-metrics]
date: 2026-04-19
sources: 1
---

# 独立游戏的游玩埋点与数据复盘

当游戏把 highscore / run 元数据上传到服务器时，开发者顺带得到一份**玩家行为分布**，能验证或推翻一系列设计假设。[[joost-van-dongen]] 在 Proun 发行三个月后整理出一百万条 highscore，是典型样本（见 [[sources/joostdevblog-proun-gameplay-stats]]）。

**埋点能回答什么问题：**

1. **模式使用分布**。Proun 的 Time Trial 在设计师眼中是最佳体验，实际只占 11% 场次，Championship 吃掉大头——**设计师偏好 ≠ 玩家行为**，埋点把这条差异量化。
2. **人数模式的 ROI**。四人分屏只占 0.085%，双人分屏 10%；键盘按键冲突让 3/4 人必须接手柄的硬约束是主因。后续工作室如果还要做 couch co-op，**投 4 人不如加深 2 人**。
3. **解锁内容是否被触达**。Proun 的 bonus 赛道挂在 Championship 外的 Time Trial / Single Race，导致最高难度场次数竟然**高于**一起解锁的奖励赛道——教训：**奖励必须塞进主玩家路径**，否则解锁约等于不存在。
4. **新手漏斗与留存 proxy**。Composition #1 比 #2 多得多，拆解为「第一关失败立刻重来」+「只试了第一关就弃游」——即 **首关退出率是最便宜的留存指标**。
5. **UGC 冷启动效应**。Proun 首周放出的 2 个 modder 赛道拿走绝大部分流量，后续赛道量级上不去——**UGC 投放节奏本身是设计问题**，不是「做好了再发」就行。

**埋点自身的工程教训：**

- Proun 服务器在发布头几天宕过机，丢了约十万条 highscore——**埋点管线的可用性和采集代码一样重要**，否则数据缺口会直接吞掉产品决策。
- 使用可弹性伸缩的托管（van Dongen 后来换到 Byte.nl）而不是便宜的 shared hosting（Hosting2Go 直接在流量大时关站）。

**局限**：这套方法只采集**上传到服务器的 run**，盗版/离线玩家不会出现在曲线上；只能反映「决定要传分数的玩家」的行为。对纯离线单机来说，需要额外的匿名遥测或 Steam API。

## 相关

- [[joost-van-dongen]]
- [[pc-gpu-driver-compat-qa]]
- [[easy-to-learn-hard-to-master]]

## Sources

- [[sources/joostdevblog-proun-gameplay-stats]]
