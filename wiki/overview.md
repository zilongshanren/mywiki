---
tags: [overview, synthesis]
date: 2026-04-05
sources: 24
---

# 知识库综述

本知识库目前包含**五大主题**，覆盖从认知/设计哲学到物理硬件约束的全栈技术视角：

- **软件设计哲学**——[[john-ousterhout|John Ousterhout]] 的 *A Philosophy of Software Design*
- **编程语言基础**——[[sussman-abelson|Sussman & Abelson]] 的 SICP
- **计算机体系结构**——[[hennessy-patterson|Hennessy & Patterson]] 的 CAQA + CSAPP
- **游戏引擎架构**——[[jason-gregory|Jason Gregory]] 的 *Game Engine Architecture*
- **实时渲染**——*Real-Time Rendering* + [[jasper-flick|Jasper Flick]] 的 Custom SRP 实践

这些看似独立的主题共享一条贯穿的主线：**在"人的认知能力"和"物理硬件约束"之间，设计能长期演进的系统**。

## 主题一：复杂性是首要敌人（APoSD）

Ousterhout 开宗明义——**软件开发的最大限制是理解系统的能力，不是技术**。这把软件设计从"怎么写代码"翻转到"怎么管理认知负荷"。[[complexity|复杂性]]被精确定义为"任何使系统难以理解和修改的东西"——**读者视角**，不是写者视角。

复杂性以三种症状出现：**[[change-amplification|变更放大]]**、**[[cognitive-load|认知负荷]]**、**[[unknown-unknowns|未知的未知]]**。有两个根源：**[[dependencies|依赖]]**和**[[obscurity|模糊性]]**。**渐进累积**让[[zero-tolerance|零容忍]]成为唯一出路。

核心正面构造是 **[[deep-modules|深模块]]**（强大功能 + 简单接口），引擎是 **[[information-hiding|信息隐藏]]**。对立面是 **[[shallow-modules|浅模块]]** 及其病态形态 **[[classitis]]**。[[strategic-programming|战略编程]]是日常实践。

## 主题二：编程语言是思维的放大器（SICP）

SICP 用 Scheme 讲**思维**——**[[elements-of-programming|三要素]]**（原子、组合、抽象）。**[[procedural-abstraction|过程抽象]]**是 1985 年就已经强调的信息隐藏，和 APoSD 的理论完全一致——SICP 给出 what，APoSD 给出 how。

[[higher-order-functions|高阶函数]]把 [[lambda-calculus|Lambda 演算]] 的数学抽象带到工程中：函数作为一等公民。识别重复模式抽出高阶函数——"**代码重复是思维还没到位的信号**"。

**[[recursive-vs-iterative-process|递归语法 vs 递归过程]]** 让你理解代码的性能——[[tail-call-optimization|尾调用优化]]的语言支持分歧决定能不能用优雅的尾递归。**[[order-of-growth|增长阶]]** 是粗描述，常被**常数系数**和**缓存行为**打败。**[[probabilistic-algorithms|概率算法]]** 不是妥协，是精确解不可行时的合理工程选择。

## 主题三：物理硬件是最终约束（CAQA + CSAPP）

**[[amdahls-law|Amdahl 定律]]** 给出并行加速的残酷上界。**[[dennard-scaling|Dennard Scaling]]** 的崩塌（~2004）制造了 **[[power-wall|功耗墙]]**——频率免费提升的时代结束了。

**[[memory-hierarchy|存储层次]]** 跨越 5 个数量级延迟；一次 DRAM miss = 100 次 L1 hit。**[[locality-principle|局部性原理]]** 让 cache 有效；**[[aos-vs-soa|AoS vs SoA]]** 直接决定 cache 利用率——**Unity DOTS 的 10-100× 性能提升来自数据布局，不是代码更快**。

**CSAPP** 的信息系统视角：**[[bits-and-context|信息 = 比特 + 上下文]]**、**[[compilation-pipeline|编译四阶段]]**、**[[virtual-memory|虚拟内存]]**——这些底层抽象塑造了所有上层程序的性能特性。

## 主题四：游戏引擎融合所有这些约束

[[jason-gregory|Jason Gregory]] 的定义：游戏是**[[soft-real-time|软实时]]的、交互式的、基于智能体的计算机模拟**——每个词都限定引擎的必然设计。

**[[game-engine|引擎]]**存在的根本原因是**生存**（每个游戏都需要同样的基础设施）。**[[data-driven-architecture|数据驱动架构]]**是引擎与游戏专用软件的分水岭。**[[engine-layering|分层]]**是第一纪律。

**[[engine-evolution|引擎演化史]]**从 BSP Tree 到 Lumen/Nanite——**技术决定游戏设计**（BSP 的限制逼出第一代 FPS 的室内美学）。**[[unity-vs-unreal|Unity vs Unreal]]** 是两种哲学（工具 vs 框架）的对立，移动端 vs AAA 的分野。

## 主题五：渲染管线是游戏引擎的心脏

**[[rendering-pipeline|渲染管线]]** 四阶段（Application/Geometry/Rasterization/Pixel）是并行运行的 pipeline——**瓶颈决定帧率**。**[[tbdr-vs-imr|TBDR vs IMR]]** 是移动端和桌面端 GPU 架构的根本分野。

完整链路：
- Application 阶段：**[[draw-call|DrawCall]]**、**[[culling|Culling]]**、**[[batching|Batching]]** 的 CPU 决策。
- Geometry Processing：**[[mvp-transform|MVP 变换]]** 把顶点推过 **[[coordinate-spaces|一系列坐标空间]]**，**[[z-buffer|Z-Buffer]]** 解决隐面。
- Rasterization：**[[rasterization|三角形 → fragment]]**、**[[aliasing|走样]]** 的信号处理根源。
- Pixel Processing：**[[fragment-shader|片元着色]]**、**[[early-z-late-z|Early-Z]]**、**[[hsr-tbdr|HSR]]**、**[[overdraw|Overdraw]]**——每一层都是性能争夺战。

## 跨主题的关键连接

几条贯穿多个主题的线索值得注意：

**[[aos-vs-soa]] 贯穿 4 个主题**：CAQA（cache 理论）→ CSAPP（底层实现）→ GEA（ECS 设计）→ 游戏开发（DOTS 性能）。**同一个概念，从物理到工程到实践。**

**[[information-hiding]] 横跨 APoSD 和 SICP**：1985 年 Sussman/Abelson 的"过程即黑盒" = 2018 年 Ousterhout 的"信息隐藏"。**同一个洞察被两次独立发现**。

**[[amdahls-law]] 约束整个系统设计**：从 CAQA 的性能公式，到 DOTS 的数据并行重构，到 GPU/TPU 的专用化。

**[[soft-real-time|实时约束]] → [[rendering-pipeline|渲染管线设计]] → [[tbdr-vs-imr|GPU 架构分野]]**：所有渲染优化的起点。

**[[engine-evolution|技术债的历史周期]]** 与 [[tactical-programming]]/[[strategic-programming]] 形成对话——每代引擎架构都是对上代债务的偿还。

## 开放问题 / 张力

- **深度 vs SRP 的张力**：Ousterhout 和 Clean Code 在"类应该多大"上冲突；SICP 用过程抽象回避这个问题。
- **数据导向 vs 面向对象**：ECS/DOTS 的性能胜出 vs OOP 的灵活性——仍在演化。
- **[[probabilistic-algorithms|概率算法]] vs 确定算法**：工程选择而非技术选择。
- **[[power-wall|功耗墙]]的长期出路**：专用化（TPU）、能效（M1）、架构多样性（RISC-V）。
- **工具 vs 框架**：Unity vs Unreal 的哲学对立未解。

## 待补充的来源

- APoSD 第 6 章以后（Define Errors Out of Existence、Design It Twice）。
- RTR 第 7 章以后（Shading、Texturing、Lighting）。
- GEA 物理、动画、音频、AI 等核心系统章节。
- SICP 第 2 章（数据抽象）、第 3 章（状态、环境）。
- CAQA 流水线、ILP、多核章节。
- CSAPP 后续章节（机器表示、进程、并发）。
