---
tags: [source, 独立开发, 游戏开发, soluna, cloudwu, 中文博客, 复盘]
date: 2026-04-19
sources: 1
---

# Deep Future 开发复盘（云风 / blog.codingnow.com）

[[cloudwu|云风]] 发表于 2025 年 10 月的长篇复盘，记录他在 7 周（含搬家、家庭意外中断 2 周）里用自研 [[soluna-2d-engine|soluna]] 引擎独立开发桌游数字化项目 *Deep Future* 的全过程与方法论总结。

## 摘要

2025 年 7 月底启动，8 月前两周主要在补 soluna 引擎：yoga 布局模块、文本排版、icon 混排、纯色矩形（用于可视化 box）、嵌套图层。其间两个小问题耗了大量时间：[Windows SetWindowText API 多线程死锁](https://blog.codingnow.com/2025/08/setwindowtext_deadlock.html)；以及放弃 20 多年来习惯的**预乘 alpha** 工作流——现代图片软件（GIMP 等）默认导出非预乘，坚持预乘只会让工作流多一步，不如顺着成熟工具改引擎默认。

游戏开发按桌游规则流程顺序（布局 → 开始 → 行动 → 结算 → 胜利）推进，每天完成一个可玩增量。用 Lua coroutine 实现状态机（几十行代码），用 setup 脚本做人工测试加速，而非自动化测试或存档路线。其间经历两次重构：advancement 结算（共享 action 结算）、星图（六边形网格）。搬家打断两周后回归，完成胜利结算、存档分离到独立服务（作为 bug 恢复工具）、文明卡与奇迹、多层主界面（用 table 描述结构）、键盘输入与自定义命名。

整个项目游戏侧约 13000 行代码，soluna 增加 5672 行。云风据此提炼出独立开发的几条方法论：**情绪是第一生产力**（按 gameplay 流程推进提供视觉反馈激励）、**拆任务是必需**、**越早重构越省事**、**代码量是对进度的可靠衡量**、**不要刻意做引擎**、**优化往后放**、**开源意外收益多**（网友补完胜利判定 / 英文本地化 / Linux/macOS 移植）。

## 关键要点

- 独立开发的核心敌人是热情耗尽，不是技术难题
- 按玩法流程推进 > 按系统分层推进，视觉反馈持续供能
- Lua coroutine 用几十行做出 gameplay 状态机
- 预乘 alpha 的工作流成本高于收益，顺手工具流程比"技术正确"重要
- Setup 脚本测试 > 自动化测试 / 存档方案
- 估时乘 2 的根源：很多功能要实现两遍（先快跑脚手架，再拆）
- 游戏核心代码 2 万行以内是独立开发的合适篇幅
- 开源带来跨平台志愿者、本地化志愿者、更仔细的自我审视

## 链接到的概念

- [[cloudwu]]
- [[soluna-2d-engine]]
- [[ltask-scheduler]]
- [[indie-game-dev-rhythm]]
- [[gameplay-architecture]]

## 原文

- 链接：https://blog.codingnow.com/2025/10/
- 本地：`raw/articles/blog.codingnow.com/2025-10-12_yun-feng-de-blog.md`
