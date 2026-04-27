---
tags: [source, hardware, qualcomm, adreno, gpu, igpu, snapdragon, laptop]
date: 2026-04-27
sources: 1
---

# Diving into Qualcomm's Upcoming Adreno X2 GPU with Eric Demers（George Cozma / Chips and Cheese）

[[george-cozma]] 于 2026 年 1 月对高通 GPU 团队负责人 Eric Demers 的专访，深入讲解 Adreno X2 的架构设计决策，涵盖 HPM、Wave64 双发射机制、API 支持路线图。

## 摘要

本文为采访形式，Eric Demers 亲自解释 Adreno X2 相对 X1 的关键变化。最核心的创新是 HPM（High-Performance Memory）：21 MB 片上 SRAM（X2-90），全局 crossbar 允许任意 Slice 访问整块 HPM，目标是将完整帧（QHD+ 分辨率）保持在片上完成渲染，彻底省去 color ROPs 和 Z-buffer 对 DRAM 的访问。HPM 最多 3 MB 可配置为 cache（cache tag 面积限制了上限，且超过该大小后命中率增益趋于平坦），其余为软件管理 scratchpad。

Wave128 被移除的原因：Wave64 分支预测效率更高（更小的分歧粒度），两路 Wave64 双发射维持 128 ALU 的实际吞吐不变。为支持双发射，寄存器文件从 96 KB 扩大到 128 KB（约 +30%）。Eric 表示双发射几乎全时运行，只在极端 GPR 压力下才受限。

API 路线：DX12.2（含 DX12 Ultimate 全特性）、原生 Vulkan 1.4（与移动端同源代码）、原生 OpenCL 3.0、SYCL（2026 Q1）。原生 API 实现是相对 X1 的重要改进——此前依赖 Windows 转发层。

## 关键要点

- HPM 全局 crossbar：物理分布在 Slice 内，逻辑可全局访问
- Cache vs scratchpad 比例：最多 3 MB cache，其余 scratchpad（tag 面积权衡）
- Wave128 → Wave64 双发射：效率更高，ALU 利用率不变，GPR 文件 +30%
- API：原生 Vulkan 1.4 + OpenCL 3.0（与移动版同源），SYCL 2026 Q1
- Eric Demers 在高通 GPU 团队工作 14 年，主导 X 系列架构

## 链接到的概念

- [[adreno-x2-igpu-architecture]]
- [[adreno-x1-igpu-architecture]]
- [[snapdragon-x2-elite-soc]]
- [[hsr-tbdr]]

## 原文

- 链接：https://chipsandcheese.com/p/diving-into-qualcomms-upcoming-adreno
- 本地：`raw/articles/chipsandcheese.com/2026-01-04_diving-into-qualcomm-s-upcoming-adreno-x2-gpu-with-eric-deme.md`
