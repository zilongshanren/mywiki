---
tags: [source, computer-systems, gpu, amd, rdna4, isa, llvm, compiler]
date: 2026-04-27
sources: 1
---

# Examining AMD's RDNA 4 Changes in LLVM（Chips and Cheese）

[[chester-lam]] 发表于 2024 年 1 月的文章，通过分析 LLVM 开源代码中 RDNA 4（GFX12）相关提交，提前预览下一代 AMD GPU 的 ISA 变化。

## 摘要

RDNA 4 在 LLVM 中以 gfx1200/gfx1201 标识，文章逐一梳理了四大 ISA 改动：（1）更细粒度的内存依赖等待指令，将 GCN 以来沿用的粗分类拆分为更精确的类别；（2）更灵活的缓存一致性控制，引入 4 位缓存策略字段取代原有三位 GLC/SLC/DLC，并分离时序 hint 与作用域控制；（3）强化矩阵运算，新增 FP8/BF8 支持与稀疏矩阵乘法指令（SWMMAC）；（4）更激进的指令预取机制，初始预取窗口从 8 KB 增至 32 KB，并引入数据侧软件预取。文章强调所有信息在产品发布前均属预发布，不排除有误。

## 关键要点

- 等待指令细化：减少因粗分类导致的伪依赖停顿，令线程可提前继续执行
- 缓存 scope 控制：新增 SE 级作用域，使同一 Shader Engine 内线程可通过 L1 传递数据（避免下沉到 L2）
- FP8/BF8 矩阵指令：跟进低精度 AI 推理趋势，与 Nvidia H100 对齐
- SWMMAC 稀疏矩阵：A 矩阵以压缩格式存储（半尺寸），理论上可获 2× 矩阵吞吐
- 指令预取：`s_prefetch_inst` 指令可将预取指向可能的跳转目标，有助大型着色器程序
- 数据预取：RDNA 4 首次引入 GPU 数据侧软件预取指令，CPU 化倾向明显

## 链接到的概念

- [[rdna4-architecture]]
- [[rdna3-architecture]]
- [[gcn-architecture]]
- [[gpu-latency-hiding]]
- [[compilation-pipeline]]

## 原文

- 链接：https://chipsandcheese.com/p/examining-amds-rdna-4-changes-in-llvm
- 本地：`raw/articles/chipsandcheese.com/2024-01-29_examining-amds-rdna-4-changes-in-llvm.md`
