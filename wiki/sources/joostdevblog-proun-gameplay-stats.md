---
tags: [source, game-development, telemetry, player-metrics, indie]
date: 2026-04-19
sources: 1
---

# One million races played! Proun's gameplay statistics（Joost van Dongen）

[[joost-van-dongen]] 发表于 2011 年 9 月的文章，晒出 Proun 上线三个月采集到的一百万条 highscore 数据，对应 [[indie-gameplay-telemetry]] 的一个具体样本。

## 摘要

Proun 联网提交 highscore，van Dongen 借此得到完整的游玩分布。**游戏模式**：Championship（成就/解锁主线）吃掉绝大多数场次；Time Trial 仅 11%，van Dongen 本人却认为这是最佳体验——设计师偏好与玩家行为偏差被数据明确化；**四人分屏仅占 0.085%**，远低于预期；双人分屏 10%，算健康。**难度与赛道**：最高难度 Speed of Light 占 7%，虽低但已属 hardcore 认证；怪的是最高难度的场次数**高于**同时解锁的奖励赛道 Improvisation #1 场次数——van Dongen 反思：奖励赛道没塞进 Championship 流程里，只有 Time Trial/Single Race 能玩，于是大多数玩家根本不点。Composition #1 远高于 #2，他归因于「第一关输了立刻重开」+「只玩了第一关就判断不合口味」。**用户赛道**：共 7 个 modder 作品，发行首周放出的 Archipelago 和 Extrude 吃掉绝大多数流量，后面加入的赛道几乎吃不到冷启动红利。

## 关键要点

- **奖励内容必须塞进主玩家路径**。Proun 把 bonus track 放在 Championship 之外，结果解锁了的人也没玩。
- **设计师「最优体验」不等于玩家实际玩的模式**——Time Trial 的 11% 是反证。
- **四人分屏的 ROI 在 PC 上接近零**（0.085%），即使游戏本身支持也几乎无人使用；键盘按键冲突导致 3/4 人必须接手柄是硬约束。
- **UGC 冷启动红利**：首周随游戏一起发布的 modder 赛道拿走大部分玩量，后续赛道即使更精良也难以追平——提示要把 UGC 投放节奏当作产品设计来规划。
- **第一关退出率 = 试玩门槛反馈**：Composition #1 / #2 的落差能当作用户留存的 hint。
- 数据本身不完美：server 宕机期丢了约十万条记录——**埋点稳定性本身是一等事**。

## 链接到的概念

- [[indie-gameplay-telemetry]]
- [[joost-van-dongen]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/09/one-million-races-played-prouns.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-09-26_one-million-races-played-proun-s-gameplay-statistics.md`
