---
tags: [source, unreal-engine, cpp, roguelike, sample-project, data-oriented-design]
date: 2026-04-19
sources: 1
---

# Project Orion: Co-op Action Roguelike Sample in Unreal Engine（Tom Looman）

[[tom-looman]] 2026 年 2 月的文章，介绍自己维护的 UE5 合作 Roguelike 开源示例项目 "Project Orion"（GitHub：tomlooman/ActionRoguelike），设计参照 Risk of Rain 2。

## 摘要

Project Orion 是一份可下载的 UE5 C++ 示例项目，最初服务于 Tom 的 UE5 课程，之后持续演进。代码主要讲 Gameplay Framework 如何在 C++ 中落地：一套仿 GAS 的 "Action System"（Action / ActionEffect / Attribute）驱动玩家与怪物的能力与 Buff，近战战斗用 BT + AnimMontage + AnimNotifyState 的组合把命中检测拆到动画段上。最值得参考的是性能实践部分：Data-Oriented 的投射物与金币（`URogueProjectileSubsystem` + `URoguePickupSubsystem`，后者用单个 `InstancedStaticMeshComponent` 渲染千枚金币）、Actor 对象池（`URogueActorPoolingSubsystem`）、Significance Manager 按重要度分桶节流 AI 动画 VFX、Animation Budget Allocator 把总动画帧时间压在阈值内。实验性特性通过 `ActionRoguelike.h` 里的 `#define` 开关启用，方便切换研究。项目还带一套世界状态存档框架，Tom 另有专门博客展开。

## 关键要点

- Action / ActionEffect / Attribute 三件套是项目的核心 Ability 框架，与 GAS 思路一致
- 近战的命中判定由 `RogueAnimNotifyState_Melee` 在 AnimNotify 生命周期内做 `OverlapMultiByChannel` 并广播事件
- 投射物和金币提供 Actor-based 与 DoD struct-array 两种实现对比，后者才能跑上千实体
- `URogueActorPoolingSubsystem` 在 load screen 预生成，避开 Spawn / GC / 内存碎片开销
- Significance Manager 与 Animation Budget Allocator 都是 UE 自带、面向 CPU/动画节流的官方方案

## 链接到的概念

- [[project-orion-action-roguelike]]
- [[tom-looman]]

## 原文

- 链接：<https://tomlooman.com/unreal-engine-sample-game-action-roguelike>
- 本地：`raw/articles/tomlooman.com/2026-02-27_project-orion-co-op-action-roguelike-sample-in-unreal-engine.md`
