---
tags: [index]
date: 2026-04-05
sources: 24
---

# 知识库索引

本知识库涵盖**软件设计哲学 · 实时渲染 · 游戏引擎 · 计算机体系结构 · 编程语言基础**五大主题。入口页：[[overview]]。品味训练指南：[[taste-development]]。

## 软件设计（wiki/software-design/）

核心概念与框架，源自 John Ousterhout 的 APoSD。

| 文章 | 一句话描述 |
|---|---|
| [[complexity]] | 复杂性的定义与整体框架，软件设计的核心敌人 |
| [[change-amplification]] | 复杂性症状之一：改动需要触及多处 |
| [[cognitive-load]] | 复杂性症状之二：需要知道太多东西 |
| [[unknown-unknowns]] | 复杂性症状之三：不知道自己不知道（最危险） |
| [[dependencies]] | 复杂性根源之一：代码间的相互牵连 |
| [[obscurity]] | 复杂性根源之二：重要信息不显而易见 |
| [[red-flags]] | 识别设计问题的信号集合 |
| [[tactical-programming]] | 短视的「让它工作」心态 |
| [[strategic-programming]] | 投资心态，优秀设计恰好也能工作 |
| [[tactical-tornado]] | 外部化成本的高产出工程师 |
| [[zero-tolerance]] | 对复杂性增量的日常纪律 |
| [[continuous-design]] | 软件设计是持续过程，不是一次性活动 |
| [[modular-design]] | 模块化的真正目标是认知隔离 |
| [[deep-modules]] | 强大功能 + 简单接口的设计理想 |
| [[shallow-modules]] | 接口复杂度接近实现复杂度的反模式 |
| [[classitis]] | 「类越多越好」的系统性设计疾病 |
| [[interface-vs-implementation]] | 接口是成本，功能是收益 |
| [[abstraction]] | 省略不重要细节的简化视图 |
| [[false-abstraction]] | 省略了重要细节的「简洁」陷阱 |
| [[information-hiding]] | 把设计决策藏进实现——深模块的引擎 |
| [[information-leakage]] | 同一份知识分散在多个模块 |
| [[temporal-decomposition]] | 按时间顺序切模块的陷阱 |

## 编程语言基础（wiki/programming-languages/）

SICP 及 Lambda 演算传统的核心概念。

| 文章 | 一句话描述 |
|---|---|
| [[elements-of-programming]] | 编程语言的三要素：原子、组合、抽象 |
| [[substitution-model]] | 纯函数求值的思维工具 |
| [[applicative-vs-normal-order]] | 求值时机的两种设计选择 |
| [[environment]] | 名字→值的 frame chain |
| [[procedural-abstraction]] | 过程作为黑盒 |
| [[lexical-scoping]] | 代码结构决定作用域 |
| [[closure]] | 函数 + 定义时环境 |
| [[recursive-vs-iterative-process]] | 递归语法 vs 递归过程 |
| [[tail-call-optimization]] | 尾调用优化与语言设计分歧 |
| [[higher-order-functions]] | 函数作为一等公民 |
| [[lambda-calculus]] | 计算的通用数学模型 |
| [[order-of-growth]] | 算法增长阶的粗描述 |
| [[fast-exponentiation]] | 分治思想的经典例证 |
| [[probabilistic-algorithms]] | 用概率正确性换可行性 |

## 计算机体系结构与系统（wiki/computer-systems/）

CAQA + CSAPP 的底层视角。

| 文章 | 一句话描述 |
|---|---|
| [[amdahls-law]] | 并行加速的理论上界 |
| [[flynn-taxonomy]] | 指令流 × 数据流的架构分类 |
| [[cpu-performance-formula]] | CPU Time = IC × CPI / Clock Rate |
| [[latency-vs-throughput]] | 两种性能指标的权衡 |
| [[memory-hierarchy]] | 跨越 5 个数量级的存储分层 |
| [[locality-principle]] | 缓存层次的理论基础 |
| [[aos-vs-soa]] | 内存布局决定 cache 利用率 |
| [[cache-friendliness]] | 让代码与缓存对齐 |
| [[dennard-scaling]] | 晶体管缩放规律的崩塌 |
| [[power-wall]] | 频率停滞的物理原因 |
| [[mttf-reliability]] | 可靠性的量化指标 |
| [[bits-and-context]] | 信息 = 比特 + 上下文 |
| [[compilation-pipeline]] | C 编译的四阶段 |
| [[virtual-memory]] | 进程独立连续地址空间幻觉 |

## 游戏引擎（wiki/game-engines/）

Game Engine Architecture（Jason Gregory）的核心概念。

| 文章 | 一句话描述 |
|---|---|
| [[game-engine]] | 什么是游戏引擎 |
| [[data-driven-architecture]] | 引擎 vs 游戏专用软件的分水岭 |
| [[soft-real-time]] | 偶尔违反时限是可接受的 |
| [[engine-layering]] | 单向依赖是第一纪律 |
| [[unity-vs-unreal]] | 两种引擎设计哲学 |
| [[engine-evolution]] | 从 BSP 到 Lumen/Nanite |

## 实时渲染（wiki/rendering/）

Real-Time Rendering + Custom SRP 的渲染管线知识。

| 文章 | 一句话描述 |
|---|---|
| [[rendering-pipeline]] | 四阶段的瓶颈驱动并行系统 |
| [[bottleneck-analysis]] | 找瓶颈只优化瓶颈 |
| [[tbdr-vs-imr]] | 两种 GPU 架构对比 |
| [[draw-call]] | CPU 状态 setup 是主成本 |
| [[culling]] | 分层过滤的 CPU 剔除 |
| [[batching]] | 减少 DrawCall 或状态切换 |
| [[mvp-transform]] | 三矩阵变换链 |
| [[coordinate-spaces]] | Model/World/View/Clip/NDC/Screen |
| [[z-buffer]] | 每像素深度缓冲 |
| [[z-fighting]] | 深度精度不足的闪烁 |
| [[reversed-z]] | 利用 float 精度分布改善远平面 |
| [[perspective-correct-interpolation]] | 透视校正插值 |
| [[rasterization]] | 三角形 → fragment |
| [[aliasing]] | 走样与反走样 |
| [[msaa-ssaa]] | 两种超采样对比 |
| [[triangle-primitives]] | 三角形为什么是基本图元 |
| [[fragment-shader]] | 每 fragment 的着色 |
| [[early-z-late-z]] | 早期/晚期深度测试 |
| [[hsr-tbdr]] | TBDR 特有的精确隐面消除 |
| [[alpha-blending]] | 半透明混合的顺序依赖 |
| [[stencil-buffer]] | 8-bit 模板缓冲的低成本效果 |
| [[overdraw]] | 过度绘制的代价与对策 |
| [[deferred-rendering]] | G-Buffer + 统一光照 pass |
| [[custom-srp]] | Catlike Coding 教程系列 |
| [[scriptable-render-pipeline]] | Unity 的可编程渲染管线 |
| [[render-graph]] | SRP 的声明式编排系统 |
| [[color-lut]] | color grading 查找纹理 |
| [[debug-visualization]] | Rendering Debugger 集成 |

## 经典案例（wiki/examples/）

APoSD 中反复出现的标杆与反面案例。

| 文章 | 一句话描述 |
|---|---|
| [[unix-io]] | 5 个系统调用隐藏几十万行实现的深模块标杆 |
| [[java-io]] | 三件套 + 显式 buffering 的 classitis 病例 |
| [[garbage-collector]] | 接口为零的极限深模块 |

## 游戏开发（wiki/game-development/）

APoSD 框架在 Unity/游戏引擎开发中的应用。

| 文章 | 一句话描述 |
|---|---|
| [[unity-complexity-patterns]] | Unity 项目中的复杂性典型模式 |
| [[classitis-in-games]] | Manager 癌症与事件系统滥用 |
| [[resource-system-design]] | 资源系统的信息隐藏战场 |
| [[ecs]] | ECS 作为深模块与显式依赖的案例 |
| [[rendering-api-depth]] | 渲染 API 的浅 vs 深对照 |

## 人物（wiki/people/）

| 文章 | 一句话描述 |
|---|---|
| [[john-ousterhout]] | APoSD 作者，斯坦福 CS 教授 |
| [[jasper-flick]] | Catlike Coding 作者，Unity 教程作者 |
| [[jason-gregory]] | Naughty Dog 引擎工程师，GEA 作者 |
| [[sussman-abelson]] | SICP 作者，Scheme 发明人 |
| [[hennessy-patterson]] | CAQA 作者，RISC 图灵奖得主 |

## 源摘要（wiki/sources/）

| 源 | 一句话描述 |
|---|---|
| [[sources/custom-srp-6-1-0]] | Custom SRP 6.1.0 教程摘要 |
| [[sources/aposd-day01]] | APoSD Day 1：Introduction |
| [[sources/aposd-day02]] | APoSD Day 2：复杂性的定义与症状 |
| [[sources/aposd-day03]] | APoSD Day 3：战术 vs 战略编程 |
| [[sources/aposd-day04]] | APoSD Day 4：深模块 |
| [[sources/aposd-day05]] | APoSD Day 5：浅模块之罪与 Classitis |
| [[sources/aposd-day06]] | APoSD Day 6：信息隐藏 |
| [[sources/sicp-day01]] | SICP Day 1：编程的三要素 |
| [[sources/sicp-day02]] | SICP Day 2：过程即黑盒 |
| [[sources/sicp-day03]] | SICP Day 3：递归过程 vs 迭代过程 |
| [[sources/sicp-day04]] | SICP Day 4：增长阶与快速幂 |
| [[sources/sicp-day05]] | SICP Day 5：概率素数判定 |
| [[sources/sicp-day06]] | SICP Day 6：高阶函数 |
| [[sources/rtr-day01]] | RTR Day 1：渲染管线架构 |
| [[sources/rtr-day02]] | RTR Day 2：Application 阶段 |
| [[sources/rtr-day03]] | RTR Day 3：Geometry Processing |
| [[sources/rtr-day04]] | RTR Day 4：Rasterization |
| [[sources/rtr-day05]] | RTR Day 5：Pixel Processing |
| [[sources/rtr-day06]] | RTR Day 6：一帧的完整生命 |
| [[sources/gea-day01]] | GEA Day 1：引擎是什么 |
| [[sources/gea-day02]] | GEA Day 2：引擎演化史 |
| [[sources/caqa-day01]] | CAQA Day 1：量化方法 |
| [[sources/caqa-day02]] | CAQA Day 2：存储层次与可靠性 |
| [[sources/csapp-day01]] | CSAPP Day 1：信息是上下文中的比特 |

## 元（wiki/meta/）

| 文章 | 一句话描述 |
|---|---|
| [[taste-development]] | 基于 wiki 内容综合出的品味训练方法 |

## 特殊页面

- [[overview]] —— 综合叙事：把主题串起来
- [[log]] —— 所有操作的时间顺序记录
