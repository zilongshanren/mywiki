---
tags: [apple, igpu, gpu, apple-silicon, m2, bandwidth, opencl, metal]
date: 2026-04-27
sources: 1
---

# Apple M2 Pro iGPU

M2 Pro 是 Apple Silicon 产品线中面向专业笔记本（MacBook Pro 14/16 寸）的中高端 SoC，采用约 289 mm² 的单片硅，配备 **19 核 iGPU**。与消费级 PC 的集成显卡不同，M2 Pro 的 iGPU 定位于挑战低端独显，并在内存带宽设计上向主机芯片看齐。

## 缓存层次与延迟

M2 Pro iGPU 的两级缓存设计：
- **L1（数据缓存）**：8 KB，与 M1 相同，速度接近 AMD Phoenix 的 32 KB L1 向量缓存，但容量极小（2011 年前 AMD Terascale 级别）
- **纹理缓存**：24 KB（通过 `image1d_buffer_t` 访问），延迟接近 Nvidia Maxwell 架构
- **L2**：3 MB（比 M1 增长 50%，比 Phoenix 的 2 MB 多），带宽超过 1 TB/s；延迟与 Phoenix 相近，略高于 M1
- **系统级缓存**：~234 ns
- **DRAM**：>342 ns（128 MB 测试），远高于 AMD Phoenix；与较老的 Intel HD 530 接近

8 KB L1 数据缓存是明显弱点：需要频繁回退到 L2，增加功耗并影响计算着色器性能。

## 内存带宽

M2 Pro 使用 **256-bit LPDDR5** 内存总线，实测 DRAM 带宽超过 200 GB/s，是其最核心的竞争优势：
- 远超 AMD Phoenix（128-bit 总线）
- 接近老款 Radeon R9 390（512-bit GDDR5）
- L2 带宽超过 1 TB/s，超越部分旧款独显

但 AMD Phoenix 的 L2 带宽更高（RDNA 3 强调带宽优化）。对于 L2 命中率低的工作负载，M2 Pro 对 L2 带宽依赖更重。

CPU 侧也受益于同一内存总线，8 核可获约 125 GB/s 带宽（1 GB 测试延迟 116.5 ns，略高于 Ryzen 7950X 的 84 ns）。

## 计算性能

FP32 峰值吞吐约 6.5 TFLOPs，接近 AMD Phoenix（8.6 TFLOPs，但依赖难以喂饱的双发射机制）。

**FluidX3D（LBM 流体模拟）**：M2 Pro 大幅领先 Phoenix，得益于更宽的内存总线；接近 Radeon R9 390（同样宽总线），被更高带宽 GDDR6 的独显超越。

**本地内存（scratchpad）**：最大 32 KB 分配，延迟略慢于 8 KB L1 数据缓存（寻址直接但竞争延迟），不如近年 AMD/Nvidia 独显。

**全局内存 atomic 延迟**：58.57 ns，与 AMD RDNA 2 相当，优于旧款 Intel/AMD iGPU。

## 大尺寸 iGPU 的定位逻辑

M2 Pro 与 PS5 APU（298.4 mm²，20 核 GPU，256-bit GDDR6）的策略相似：将 GPU 与 CPU 集成以节省 PCIe 接口、主板布线和散热空间，共享内存控制器。对于 GPU 内存需求远大于 CPU 的场景（游戏主机、专业创意工作），这一方案有效。

M2 Pro 的独特之处在于：既实现了主机级别的高带宽，又保持了低于主机的内存延迟——Chester Lam 认为这是"出色的折衷"。

**局限**：最大内存 32 GB；单片 28/3 nm 硅芯片成本高（32 GB M2 Pro Mac Mini 售价 $1999）；PC 市场消费者偏好分开购买 CPU 和 GPU。

## 与 AMD Strix Halo 的预测

文章指出，M2 Pro 的高带宽方案在 PC 市场难以复制——AMD Strix Halo 若想做同类产品，面临成本、市场定位和规模经济挑战（Apple 有 Mac + iPhone 的出货量基础）。

## Sources

- [[sources/chipsandcheese-m2pro-igpu]]
