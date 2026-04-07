## [2026-04-05] ingest | Custom SRP 6.1.0

收录 Catlike Coding 的 Unity Custom SRP 6.1.0 教程（作者 Jasper Flick）。内容涉及 Camera Target Texture 修复和 Color LUT 调试可视化的实现。创建 5 篇渲染相关 wiki 页。

## [2026-04-05] ingest | APoSD Day 1 Introduction

收录 APoSD 第 1 章 Introduction 的学习笔记。核心观点：软件开发的最大限制是理解系统的能力，不是技术；复杂性是核心敌人；对抗它有消除与封装两条路；软件设计是持续过程。

## [2026-04-05] ingest | APoSD Day 2 复杂性的定义与症状

收录 APoSD 第 2 章的学习笔记。给出复杂性的精确定义（读者视角）、三症状（变更放大、认知负荷、未知的未知）、两根源（依赖、模糊性）、公式 C = Σ(cp × tp)。

## [2026-04-05] ingest | APoSD Day 3 战术 vs 战略编程

收录 APoSD 第 3 章的学习笔记。复杂性的复利性、零容忍纪律、战术龙卷风概念、10-20% 投资原则、Facebook/Google 对照。

## [2026-04-05] ingest | APoSD Day 4 深模块

收录 APoSD 第 4 章前半部分的学习笔记。深模块作为核心正面构造，Unix I/O 和 GC 作为标杆，接口=成本的重新定义，抽象的定义，浅模块的极端案例，与 Clean Code/GoF 的对比。

## [2026-04-05] ingest | APoSD Day 5 浅模块之罪 & Classitis

收录 APoSD 第 4 章后半部分的学习笔记。Classitis 作为系统性疾病，Java I/O vs Unix I/O 的对照，游戏开发中 Manager 癌症和事件系统滥用的典型。

## [2026-04-05] ingest | APoSD Day 6 信息隐藏

收录 APoSD 第 5 章的学习笔记。信息隐藏作为深模块的灵魂，`private` != 信息隐藏，信息泄漏红旗，后门泄漏，时序分解陷阱，「让类稍微大一点」的反直觉推论。

## [2026-04-05] update | 初次编译整个 wiki

从所有 raw 源初次编译出完整 wiki：35 篇概念/案例/人物/源摘要页，加上 overview、index、log。所有内容使用简体中文。目录结构：software-design、examples、game-development、rendering、people、sources。

## [2026-04-05] ingest | SICP Day 1-6

收录 SICP 前 6 天学习笔记：编程三要素、过程抽象、递归 vs 迭代、增长阶、概率素数判定、高阶函数。创建 wiki/programming-languages/ 下 14 篇概念页：elements-of-programming、substitution-model、applicative-vs-normal-order、environment、procedural-abstraction、lexical-scoping、closure、recursive-vs-iterative-process、tail-call-optimization、higher-order-functions、lambda-calculus、order-of-growth、fast-exponentiation、probabilistic-algorithms。发现与 APoSD information-hiding 的直接呼应。

## [2026-04-05] ingest | Real-Time Rendering Day 1-6

收录 RTR 前 6 天学习笔记：渲染管线架构、Application 阶段、Geometry Processing、Rasterization、Pixel Processing、一帧完整生命。创建 wiki/rendering/ 下 19 篇新概念页：rendering-pipeline、bottleneck-analysis、tbdr-vs-imr、draw-call、culling、batching、mvp-transform、coordinate-spaces、z-buffer、z-fighting、reversed-z、perspective-correct-interpolation、rasterization、aliasing、msaa-ssaa、triangle-primitives、fragment-shader、early-z-late-z、hsr-tbdr、alpha-blending、stencil-buffer、overdraw、deferred-rendering。

## [2026-04-05] ingest | Game Engine Architecture Day 1-2

收录 Jason Gregory 的 Game Engine Architecture 前 2 天学习笔记：引擎定义、三角度分析、引擎演化史（BSP → Lumen/Nanite）。创建 wiki/game-engines/ 下 6 篇概念页：game-engine、data-driven-architecture、soft-real-time、engine-layering、unity-vs-unreal、engine-evolution。

## [2026-04-05] ingest | Computer Architecture Day 1-2 & CSAPP Day 1

收录 CAQA 前 2 天与 CSAPP 第 1 天学习笔记：Amdahl 定律、Flynn 分类法、CPU 性能公式、存储层次、局部性原理、AoS vs SoA、Dennard Scaling 崩塌、功耗墙、MTTF 可靠性、信息=比特+上下文、编译四阶段、虚拟内存。创建 wiki/computer-systems/ 下 14 篇概念页。

## [2026-04-05] update | 大规模知识域扩展

从 7 源扩展到 24 源，wiki 文章从 47 扩展到 101 篇。新增 4 个概念类别（programming-languages、computer-systems、game-engines、rendering 大幅扩展）、3 位作者（sussman-abelson、hennessy-patterson、jason-gregory）。更新 index、overview 大幅重写以反映五大主题架构和跨主题连接。更新 ecs、rendering-api-depth 以引入新 sources。

## [2026-04-05] lint | Wiki 健康检查

健康度评分 A-。发现 28 项改进点，分布 6 类：低入链页面（7）、概念缺口（10）、缺失交叉引用（12）、数据缺口（7）、样式一致性（1）、待研究问题（6）。无坏链，无 frontmatter 缺失，无 index 遗漏，无孤儿页。报告见 output/reports/lint-report.md。

## [2026-04-05] query | 如何用这些内容提升品味

用户问如何用本 wiki 提升设计品味。基于 Ousterhout 的 Red Flag 训练、APoSD 各章的品味判断、SICP 的抽象模式、概率算法的工程哲学，综合出五条可执行的品味训练方法 + 30 天练习计划。归档为 wiki/meta/taste-development.md，更新 index。
