---
tags: [source, vector-field, bytecode-vm, sse, data-oriented, bitsquid, physics]
date: 2026-04-19
sources: 3
---

# A Data-Oriented, Data-Driven System for Vector Fields（Niklas Frykholm / Bitsquid，三部曲合并）

[[niklas-frykholm]] 2012 年 9–10 月的三篇连载（Part 1/2/3）。以"游戏里的风"为动机设计一套 vector field 子系统，核心贡献是一个**按指令外循环、按粒子内循环的大规模向量化字节码 VM**——让字节码跑到接近原生 SSE 代码的速度，进而把完整的数据驱动能力放回 C++ 引擎。

## 摘要

**Part 1 — 表示**：Frykholm 拒绝"把 3D 空间的风速数据存成网格"这种朴素做法（内存与更新成本都太高），改用函数式表达 `F(p, t)`。观察到同一帧里 `t` 固定，可以把时间维度从快速路径剥离——高层系统每帧一次做常数折叠与简化产出一个 `G(p)`，低层只管高速求值 `G(p)`。把 `G(p)` 建模为多个局部效应 `G_i(p)` 的叠加（全局风 + 爆炸 + 通风口 + 漩涡等等），再用每个效应自带的 AABB 与粒子群 AABB 做裁剪，得到一个与本帧相关的最小 `G'(p)`。

**Part 2 — 执行**：vector field 必须真正"数据驱动"，不能写死在 C++ 里。可选项只有两种：动态生成机器码（跨平台与沙箱成本高），或者字节码 VM。普通字节码慢 10×，原因全在"解码指令 + 跳转"两步。Frykholm 的反转：对同一条指令，内层循环遍历**所有粒子**再跑下一条，解码成本被摊销到上千个点上，最后跑到只比 native 慢 16%。为了控制本地变量的内存预算，临时寄存器不做"每粒子一个完整轨迹"——调用方给一块 scratch buffer，VM 用它切成 Vector4 通道、按分块（chunk）推进粒子。示例里 20000 个粒子一帧只花 0.4ms 单线程。

**Part 3 — 语言与物理接入**：bytecode 格式追求最简（`op/dst/arg1/arg2` 各 4 字节，不做 pack）；2-arity 指令按常量/寄存器组合展开出 4 变体，用代码膨胀换执行速度。编写语言用类 HLSL 的 DSL，带 `CHANNEL0/1` 输入输出声明；编译器用**递归下降（结构）+ shunting yard（表达式）**直接生成 bytecode，从 value stack 回收临时通道。常量走运行时 patch（一张 `(hash, offset)` patch 列表），让 gameplay 代码可以 `add(field, "whirl", {radius = 10})` 动态改参。物理接入部分有两个关键经验：**只对 awake actor 施加风力**（否则物理世界永不休眠），再额外提供 `wake_actors(aabb)` 给"突发爆炸"这类情况；旋转力矩用一个"把 drag 作用点抬到质心上方"的 hack 近似，不追求物理正确，追求视觉可信。

## 关键要点

- **外层指令循环 / 内层数据循环**：一次解码摊到千个粒子，字节码逼近 native SSE 速度
- **时间维度在 per-frame 层剥离**：高层把 `F(p,t)` 特化为 `G(p)`，低层快车道不看时间
- **叠加 + AABB 裁剪**：`G(p) = ΣG_i(p)`，按帧剔除无关效应后动态拼接 bytecode
- **Scratch buffer 切通道**：本地变量内存预算可预测，与粒子数解耦（按 chunk 分批）
- **HLSL 风 DSL + recursive descent + shunting yard** 直接生成 bytecode，不用 Lex/Yacc
- **常量 patch 机制**让同一段 bytecode 可被 gameplay 复用不同参数
- **物理接入**：只对 awake actor 施力；突发效应需显式 wake AABB；rotation 用 drag 抬高点的 hack
- 评论区有价值：用 noise 的解析梯度做 divergence-free flow field（wavelet turbulence），比多条独立 noise 输出"相关"得多

## 链接到的概念

- [[vector-field-bytecode-vm]]
- [[bytecode-everywhere]]
- [[aos-vs-soa]]
- [[data-driven-architecture]]

## 原文

- 链接（Part 1）：https://bitsquid.blogspot.com/2012/09/a-data-oriented-data-driven-system-for.html
- 链接（Part 2）：https://bitsquid.blogspot.com/2012/10/a-data-oriented-data-driven-system-for.html
- 链接（Part 3）：https://bitsquid.blogspot.com/2012/10/a-data-oriented-data-driven-system-for_17.html
- 本地：
  - `raw/articles/bitsquid.blogspot.com/2012-09-17_a-data-oriented-data-driven-system-for-vector-fields-part-1.md`
  - `raw/articles/bitsquid.blogspot.com/2012-10-02_a-data-oriented-data-driven-system-for-vector-fields-part-2.md`
  - `raw/articles/bitsquid.blogspot.com/2012-10-17_a-data-oriented-data-driven-system-for-vector-fields-part-3.md`
