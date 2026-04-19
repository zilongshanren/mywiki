---
tags: [ecs, game-engine, data-oriented-design, ant-engine]
date: 2026-04-19
sources: 1
---

# 把 ECS 回归面向数据的原始设计

[[cloudwu|云风]] 2024 年 9 月在独立开发三个月后，对 [[ant-engine|Ant 引擎]] ECS 的反思：希望让 ECS 框架还原成更原始的设计——**面向数据，避免添加太多的辅助模块**。

## 问题

Ant 引擎作为工作项目在六年迭代中，为方便团队协作，逐步在 ECS 之上堆了不少辅助模块：事件、消息、生命周期钩子、特定子系统的粘合层。这些模块当初是为了让系统代码写起来"更像 gameplay 语言"，但云风作为这个引擎唯一活跃用户时发现：这些辅助反而把 ECS 的本质——组件即数据、系统即对数据的无状态变换——掩盖了。每次他想改一个小行为，都要先翻清楚哪几层辅助在介入，这违背了他对 [[modular-design|模块化]] 与 [[information-hiding|信息隐藏]] 的长期品味。

## 立场

回到原始 ECS：组件是聚合数据（[[aos-vs-soa]] 向 SoA 倾斜），系统读写组件、按 query 遍历，不引入事件 bus、不引入"组件间通信"这种高阶构造。辅助设施如果确有必要，放到 gameplay 侧（见 [[engine-thin-wrapper-per-genre]]），而不是下沉到 ECS 核心。

这个主张延续了云风 [[type-safety-vs-simplicity|类型安全 vs 代码浅显]] 的倾向：宁可在上层用一点裸代码，也不要用一层抽象把底层规则隐藏起来。也呼应他在 [[ecs-particle-system-c]] 里的做法——粒子系统用 C 裸写属性数组，比 C++ 模板版本读起来更通透。

## 延伸

- [[data-driven-architecture]]
- [[cognitive-load|降低认知负担]]
- [[shallow-modules]] 的反面：辅助模块把一个本来浅显的 ECS query 变成深层依赖链

## Sources

- [[sources/cloudwu-ant-engine-improvement-plan]]
