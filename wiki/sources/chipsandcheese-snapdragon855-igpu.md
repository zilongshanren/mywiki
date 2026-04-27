---
tags: [source, rendering, gpu, qualcomm, adreno, mobile, snapdragon, tiled-rendering]
date: 2026-04-27
sources: 1
---

# Inside the Snapdragon 855's iGPU（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 5 月的文章，对 Snapdragon 855 内置的 Adreno 640 GPU 进行微基准测试，重点分析其在极度受限的功耗与面积预算下如何提升算力。

## 摘要

Adreno 640 是 Adreno 530（Snapdragon 821）的继任，从 Samsung 14 nm 升级至 TSMC 7 nm，同时大幅调整架构。核心改动：将 4 个 Shader Processor（SP）扩展为 6 个，但将三个 SP 编为一组共享 Local Memory 与内存接口，仅执行单元与 Texture Cache 保持 SP 私有；向量宽度从 wave32/wave64 激进跃升至 wave128（128×32 位），以减少前端开销并提升吞吐；时钟频率从 653 MHz 降至 585 MHz。缓存层次维持 1 KB L1 Texture Cache（只读）+ 128 KB L2，Local Memory 64 KB 全局共享（每组 32 KB）。Tiled Rendering（GMEM 1 MB）使光栅化场景带宽极低，3DMark Slingshot 下 GPU 内存带宽不超过 10 GB/s。但 wave128 的高度宽向量在分支发散场景下代价巨大，FluidX3D 等通用计算场景 Adreno 640 甚至不及 Adreno 530；Adreno 730 后来重新缩回 wave64 并恢复 SP 私有 Local Memory。

## 关键要点

- Adreno 640：6 SP，wave128 向量宽度，585 MHz，TSMC 7 nm
- 三个 SP 共享 Local Memory（32 KB）+ 内存接口，仅 Texture Cache（1 KB）与执行单元私有
- FP32 执行单元：每 SP 128 lane；FP16 与 FP32 同速（不像 Adreno 530 或 730 的 2× FP16）
- 整数性能弱：基础 INT ADD 半速，INT64 再减半；新增 INT8 硬件支持
- L1 Texture Cache 1 KB 只读；L2 128 KB 共享，与 Adreno 530 相同容量
- GMEM 1 MB 支撑 Tiled Rendering，光栅化内存带宽 <10 GB/s，表现优异
- wave128 在通用计算（FluidX3D）上性能下降；Adreno 730 回退至 wave64
- 3DMark Slingshot Extreme：着色器利用率 ~90%，ALU 30-40%，纹理管道压力大

## 链接到的概念

- [[rendering/adreno-640-architecture]]
- [[rendering/tiled-rendering]]
- [[computer-systems/qualcomm-kryo-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/inside-the-snapdragon-855s-igpu
- 本地：`raw/articles/chipsandcheese.com/2024-05-01_inside-the-snapdragon-855s-igpu.md`
