---
tags: [source, procedural-generation, dungeon-generation, doom, game-development]
date: 2026-04-27
sources: 1
---

# Level Generation in SLIGE（Boris The Brave）

[[people/boris-the-brave]] 发表于 2020 年 6 月的文章，深度解析 Doom 经典随机关卡生成器 SLIGE 的算法实现。

## 摘要

SLIGE 是 1990 年代初针对原版 Doom 开发的随机关卡生成器，由 David Chess 编写，代码为单文件 14000 行 ANSI C。Boris 通过阅读其开源代码，系统梳理了 SLIGE 的生成策略：以轴对齐矩形"房间"和"连接走廊"为基本单元，通过栈式的"任务（Quest）"系统提供锁钥结构，并用一次性随机化的"关卡参数（Level Settings）"保证全局风格一致性。SLIGE 的优先级不是追求最精美的平面图，而是精心调校的游戏性——通过运行时预算追踪确保每种难度下玩家的血量、护甲和弹药始终处于合理范围。

## 关键要点

- **房间 + 连接**：全部以轴对齐矩形实现，生成结果有明显的方块感，但矩形内部支持大量随机变体（凹槽、楼梯、电梯、秘密区域等）
- **Quest 系统**：栈式锁钥图；遇到分叉时当前 Quest 入栈、新 Quest 开始，新 Quest 结束后恢复旧 Quest——实现非线性但无环的关卡结构
- **Quest 分叉类型**：KEY / SWITCH / GATE / NULL 四类，分别在终点放置钥匙、开关、传送门或少量道具
- **难度预算**：每添加一个敌人就更新"玩家剩余资源估算"，血量/弹药低于阈值时才生成补给品，精确到各武器弹药量和不同难度设定
- **关卡参数（Level Settings）**：生成之初一次性随机化；固定全局后让每张地图有统一风格，同时形成自然的"适者生存"——被传播的 WAD 恰好是设定最好的那批
- 无抽象层，全部直接操作 Doom 的 linedef/sector 内存结构；BSP 树需事后由外部工具计算

## 链接到的概念

- [[game-development/slige-doom-level-gen]]
- [[dungeon-generation-algorithm]]
- [[game-development/procedural-dungeon-generation]]
- [[recursive-subdivision]]

## 原文

- 链接：https://www.boristhebrave.com/2020/06/24/level-generation-in-slige/
- 本地：`raw/articles/boristhebrave.com/2020-06-24_level-generation-in-slige-doom-level-generator.md`
