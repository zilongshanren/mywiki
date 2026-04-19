---
tags: [人物, 作者]
date: 2026-04-19
sources: 5
---

# Sebastiano Mandalà

意大利程序员、[Svelto.ECS](https://github.com/sebas77/Svelto.ECS) 的作者与维护者，职业生涯长期在 Freejam（*Robocraft*、*Robocraft 2*）做游戏工程。在博客 *Seba's Lab* 上系统地写 ECS 设计、模块化、控制反转与 Svelto 内部实现。

与 Unity DOTS ECS 的 archetype 路线不同，Svelto 选择了**群组（Group / GroupCompound）**内存布局，并强调 ECS 只是"以 ECS 为中心的多范式应用"里的一层，不主张把整个引擎都塞进 ECS。他对 DOTS ECS 1.0 的评价一贯直接：赞 idiomatic for each、unmanaged components，批 ISystem、ECB、archetype 陷阱。

## 代表作与贡献

- [[svelto-ecs]] — 平台无关的 C# ECS 框架，兼容 Unity / .NET / SDL / Stride
- 把*依赖倒置*、Hollywood Principle 提炼成 [[ecs-abstraction-layers]] 方法论
- [[svelto-filters-api]] — 用 filter 取代 event / publisher-consumer
- [[svelto-on-dots]] — 把 DOTS ECS 当作"ECS 写的引擎库"而非游戏框架
- [[ecs-on-gpu-computesharp]] — 用 ComputeSharp 把 ECS 系统直接跑在 GPU 上

## Sources

- [[sources/sebaslab-ecs-abstraction-layers]]
- [[sources/sebaslab-svelto-filters-api]]
- [[sources/sebaslab-survival-mini-example]]
- [[sources/sebaslab-svelto-on-dots-update]]
- [[sources/sebaslab-ecs-on-gpu-computesharp]]
