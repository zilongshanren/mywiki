---
tags: [source, 游戏引擎, ant-engine, ecs, framework-design]
date: 2026-04-19
sources: 1
---

# Ant 引擎的一些改进计划（云风 / blog.codingnow.com）

[[cloudwu|云风]] 发表于 2024 年 9 月 3 日的博客，作为 [[ant-engine|Ant 引擎]] 在他个人独立开发三个月后的阶段性反思。

## 摘要

云风离开阿里、独自开发游戏三个月后，以"唯一活跃用户"的身份回看 Ant 引擎，发现了不少缺憾。他现阶段不想大改引擎（想把精力放在 gameplay 上），但记下了几条重要改进方向：可视化编辑器对独立开发暂时不重要，美术可以用几何体代替，所以编辑器不维护了；引擎模块缺 API 文档只能读源码，而且并非每个模块设计都满意，于是他决定**额外做一个精简的游戏框架层**，按游戏需求把好模块浅封装、差模块做不侵入的改进；长期看希望按游戏类型做多套这样的框架，让底层实现可以放心裁剪。最后一点：希望把 ECS 框架**还原成更原始的面向数据设计**，避免添加太多的辅助模块。

## 关键要点

- 独立开发暴露引擎缺陷：无文档、模块设计参差不齐；
- 不正面改引擎，而是在上面加一层薄框架隔离：[[engine-thin-wrapper-per-genre]]；
- 按游戏类型做二次封装，让游戏代码免疫底层重构；
- ECS 回归原始面向数据设计：[[ecs-data-oriented-revert]]；
- 可视化编辑器对独立开发者优先级低，预制几何体 + demo 内嵌工具够用；
- 这篇是独立开发视角对 2024-01 开源公告的补充。

## 链接到的概念

- [[ant-engine]]
- [[ecs-data-oriented-revert]]
- [[engine-thin-wrapper-per-genre]]
- [[ecs]]
- [[modular-design]]
- [[interface-vs-implementation]]
- [[cognitive-load]]

## 原文

- 链接：<https://blog.codingnow.com/cat2/ant_engine/>
- 本地：`raw/articles/blog.codingnow.com/2024-09-03_yun-feng-de-blog.md`
