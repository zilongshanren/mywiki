---
tags: [人物, 作者, 中文博客, 游戏引擎]
date: 2026-04-14
sources: 9
---

# 云风（Cloud Wu）

云风（吴云洋），中国游戏引擎程序员，长期活跃于 blog.codingnow.com。早期在网易任职多年，主导过《大话西游》等 MMO 引擎与底层系统，后期创立 simplegame / ejoy，是开源 actor 模型游戏服务器框架 **skynet**（Lua/C 混合）以及 2D 游戏引擎 **ejoy2d** 的主要作者。

他的文章偏好用纯 C 写底层、用 Lua 做脚本层，反感 C++ 过度的 template 与 all-in-one 哲学，长期围绕模块化、接口设计、对象模型、资源管理、虚拟文件系统、内存管理、序列化、GC 这些朴素而核心的工程问题展开思辨。写作风格务实，多为边做边写的设计笔记，对中文游戏程序员社区影响较大。

## 主要工作

- 网易早期 MMO 引擎 / 大话西游系列
- skynet：面向游戏服务器的 Lua/C actor 框架
- ejoy2d：2D 游戏引擎
- 十余年的个人博客 blog.codingnow.com，系统性的工程思考输出
- Ant Engine：2017 年底开始研发、2024 年 1 月开源的移动端 3D 游戏引擎（Lua + C，ECS 架构）

## 关联概念

- 偏爱 C + Lua 混合编程的哲学，反对用 C++ 宏来"模拟"对象模型
- 从模块化 / 接口先行 / 生命期隔离出发设计底层
- 2024 年开始独立做游戏，开始系统性梳理 gameplay 上层架构：三层切分 + Object/Actor + 持久化驱动的数据设计
- 2024 下半年在自研游戏过程中反复验证一个立场：micro-management 类游戏里，确定性规则优于"智能 AI"，玩家需要可预测的物流/行为

## 相关

- [[modular-design]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[c-opaque-struct-modules]]
- [[c-interface-oop]]
- [[simple-cpp-mark-sweep-gc]]
- [[c-serialization-metadata]]
- [[game-engine-vfs]]
- [[malloc-wrapper-debug]]
- [[lua-design-philosophy]]
- [[c-tagged-union-dispatch]]
- [[game-resource-pack-format]]
- [[cpp-multi-paradigm-discipline]]
- [[go-goroutine-channels]]
- [[connection-multiplexer-gateway]]
- [[zeromq-messaging-patterns]]
- [[snapshot-diff-persistence]]
- [[lua-incremental-gc]]
- [[ant-engine]]
- [[ltask-scheduler]]
- [[mobile-energy-optimization]]
- [[async-offline-culling]]
- [[ecs-particle-system-c]]
- [[type-safety-vs-simplicity]]
- [[worker-task-dispatch-priority]]
- [[multi-target-pathfinding]]
- [[id-based-lifetime-with-kill-flag]]
- [[gameplay-layering-object-actor]]
- [[immediate-vs-retained-mode]]
- [[save-load-driven-data-design]]
- [[ecs-data-oriented-revert]]
- [[engine-thin-wrapper-per-genre]]
- [[determinism-vs-smart-ai-gameplay]]
- [[mod-first-engine-evolution]]
- [[single-hub-logistics-model]]
- [[agent-state-sync-broadcast]]
- [[sprite-batch-instance-draw]]
- [[soluna-2d-engine]]
- [[lua-class-pattern]]
- [[xlsx-text-versioning]]
- [[mysql-charset-migration]]

## Sources

- [[sources/cloudwu-c-module-interface]]
- [[sources/cloudwu-cpp-mark-sweep-gc]]
- [[sources/cloudwu-c-serialization-and-c-oop]]
- [[sources/cloudwu-game-engine-vfs]]
- [[sources/cloudwu-malloc-wrapper]]
- [[sources/cloudwu-masterminds-lua-chapter]]
- [[sources/cloudwu-c-tagged-union-dispatch]]
- [[sources/cloudwu-resource-pack-format]]
- [[sources/cloudwu-effective-cpp-comments]]
- [[sources/cloudwu-go-first-impressions]]
- [[sources/cloudwu-mmo-io-snapshot-diff]]
- [[sources/cloudwu-zeromq-patterns]]
- [[sources/cloudwu-lua-incremental-gc]]
- [[sources/cloudwu-ant-engine-open-source]]
- [[sources/cloudwu-vfs-new-ideas]]
- [[sources/cloudwu-ltask-rewrite]]
- [[sources/cloudwu-ant-engine-mobile-optimization]]
- [[sources/cloudwu-ecs-particle-system-c]]
- [[sources/cloudwu-worker-task-pathfinding]]
- [[sources/cloudwu-id-lifetime-kill-flag]]
- [[sources/cloudwu-gameplay-architecture]]
- [[sources/cloudwu-ant-engine-improvement-plan]]
- [[sources/cloudwu-game-reviews-determinism]]
- [[sources/cloudwu-factorio-space-age]]
- [[sources/cloudwu-state-sync-broadcast-optimization]]
- [[sources/cloudwu-soluna-2d-pipeline]]
- [[sources/cloudwu-game-engine-memory]]
- [[sources/cloudwu-lua-class-pattern]]
- [[sources/cloudwu-xlsx-version-control]]
- [[sources/cloudwu-mysql-gbk-utf8-migration]]
