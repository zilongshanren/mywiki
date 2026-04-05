---
tags: [软件设计, aposd, 哲学]
date: 2026-04-05
sources: 1
---

# 软件设计是持续过程

Ousterhout 在 APoSD 第一章里对瀑布模型的批判：

> "Software design is a continuous process that spans the entire lifecycle of a software system; this makes software design different from the design of physical systems such as buildings, ships, or bridges."

桥的设计图一旦确定，中途改「支柱数量」是灾难。但软件不一样——**可塑性（malleability）**是软件最特殊的属性。你可以中途重构核心架构，把同步系统改成异步，把单体拆成微服务。

## 自由的陷阱

> "Incremental development means that software design is never done. Design happens continuously over the life of a system: developers should always be thinking about design issues."

可塑性带来巨大自由，也带来陷阱：**因为「以后可以改」，我们倾向于现在不认真设计**。

瀑布模型试图在开始时做完所有设计，失败了——因为开始时你不可能理解所有含义。敏捷正确地识别到这点，把设计变成持续活动。但敏捷经常被滥用成「不设计」的借口——「反正会迭代，先做再说」。

Ousterhout 的立场：**增量开发不意味着不设计，而意味着持续设计**。每次写新功能，你在设计；每次 code review，你在设计；每次重构，你在设计。

## 对游戏开发的含义

- **里程碑之间的「清理时间」不是奢侈品，是维持系统健康的必要投入**。游戏项目常把里程碑间隙填满新功能，完全不留设计改进时间。结果是技术债越来越重，最后阶段开发速度急剧下降。
- **玩法验证的成功不等于代码设计的成功**。一个让玩家爽了的原型，可能建立在最糟糕的代码基础上。从原型转生产阶段的重设计，是项目技术质量的关键节点。

## 相关

- 操作化形式：[[strategic-programming]]
- 纪律：[[zero-tolerance]]
- 对立面：[[tactical-programming]]

## Sources

- [[sources/aposd-day01]]
