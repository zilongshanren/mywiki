---
tags: [source, 游戏设计, factorio, automation, simulation, mod-api]
date: 2026-04-19
sources: 1
---

# 异星工厂 2.0 太空时代通关复盘（云风 / blog.codingnow.com）

[[cloudwu|云风]] 发表于 2024 年 11 月 29 日的长文，在肝完 *Factorio: Space Age* 300 小时通关后写下的系统复盘。对做同类游戏的人来说，是一篇直接可用的设计样书。

## 摘要

云风从核心系统改进和新玩法两个维度总结 2.0。核心系统方面：**太空平台用单一枢纽取代无人机 + 多箱物流**（回答了他自己几版都没做好的"上帝视角交互"问题）；**流体系统 2.0 去掉了智能拦截，让玩家自己处理混道**，这看似退步其实把行为变确定、扩展了玩法；**信号控制增强**——线不消耗实体、可选择运算器、读取爪子/储存箱/核电站温度、用信号换配方——本质是把游戏状态进一步暴露给 Mod / 玩家自己的自动化；**机器多了回收箱**以容纳换配方残留。新玩法方面：五个风格迥异星球（新地 - 无限水 + 污染防守 / 雷神 - 副产品处理 / 祝融 - 液体原料 + 撼地虫 / 句芒 - 变质时效 / 玄冥 - 热能处理），太空物流成本设计把跨星球经营变成必须。云风明确赞许的核心哲学：**官方扩展本身就是一个 Mod，核心系统围绕 Mod API 进化而非不断堆内容**——这是异星工厂最独特的地方。

## 关键要点

- 太空平台唯一枢纽模型：[[single-hub-logistics-model]]；
- 流体系统去智能拦截换确定性：延续 [[determinism-vs-smart-ai-gameplay]] 的立场；
- 信号控制增强让外部确定性逻辑替代游戏内 AI；
- 品质系统：无液体品质是"神来之笔"，强制长生产链规划；
- 官方扩展以 Mod 形式实现：[[mod-first-engine-evolution]]；
- 云风 2022 曾自己实现过 1.0 的流体系统（引用自家旧文 `fluid_system.html`），对这些改动有一手判断；
- 他在自己的游戏里改过三四版单枢纽 / 液体管道系统都不满意，Space Age 把他卡住的地方都处理掉了。

## 链接到的概念

- [[single-hub-logistics-model]]
- [[determinism-vs-smart-ai-gameplay]]
- [[mod-first-engine-evolution]]
- [[game-engine-vfs]]
- [[worker-task-dispatch-priority]]

## 原文

- 链接：<https://blog.codingnow.com/2024/11/>
- 本地：`raw/articles/blog.codingnow.com/2024-11-29_yun-feng-de-blog.md`
