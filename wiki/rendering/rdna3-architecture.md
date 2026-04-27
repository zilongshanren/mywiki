---
tags: [gpu, amd, rdna3, cache, compute, dual-issue, vopd, chiplet, memory-hierarchy]
date: 2026-04-27
sources: 1
---

# RDNA 3 架构

RDNA 3 是 AMD 第三代 RDNA 消费级 GPU 架构，首发产品为 Radeon 7900 XTX（2022 年底）。相比 [[rendering/rdna1-overclocking-navi10|RDNA 1/2]]，RDNA 3 的核心策略是在多个维度上同时扩展：更多 WGP、更大缓存、更高带宽，以及首次引入的 VOPD 双发射指令。物理实现上首次采用 chiplet 方案，主图形 die 使用 TSMC 5nm，Infinity Cache 和内存控制器移至独立的 6nm die。

## 存储层次

缓存容量在 RDNA 2 基础上全面升级：

| 层级 | RDNA 2 | RDNA 3 | 备注 |
|------|--------|--------|------|
| L0 向量缓存 | 16 KB/CU | 32 KB/CU | 翻倍 |
| L0 标量缓存 | 16 KB | 16 KB | 不变，延迟改善 |
| L1（共享） | 128 KB/shader array | 256 KB | 翻倍，16-way |
| L2（全局） | 4 MB，16-way | 6 MB，16-way | +50% 容量 |
| Infinity Cache | 128 MB（on-die） | 96 MB（on-chiplet） | 容量下降，延迟上升 |
| VRAM | 256-bit GDDR6 | 384-bit GDDR6 | 带宽大幅提升 |

尽管 Infinity Cache 容量下降、延迟上升，但 L2 命中率提升意味着访问 Infinity Cache 的频率降低，整体内存访问延迟可接受。VRAM 总带宽（384-bit）接近 Nvidia GA102，减少了对 Infinity Cache 的依赖。

## VOPD 双发射

RDNA 3 的 WGP 内新增 VOPD（Vector Operation Dual-dispatch）能力，允许将两条常见指令打包为单条 8-byte 指令并行执行：

- 支持范围有限：每条操作最多 2 源 + 1 目标，FMA（3 源操作数）不支持
- 寄存器 bank 约束：同位置操作数不能读同一 bank；目标寄存器不能同为奇数或同为偶数
- 实际效果：FP32 加法编译器可自动生成 VOPD；FMA 几乎无法双发射
- Wave64 模式下有机会不依赖编译器直接实现双发射

VOPD 的实际收益大部分来自 AMD 手工优化的 shader 路径，以及 wave64 模式。对通用 FP32 TFLOPs 的贡献被 AMD 谨慎地未列入官方宣传数字（61 TFLOPS 的 headline 是假设 VOPD 或 wave64 FMA @ 2.5 GHz）。

## LDS 延迟

RDNA 3 的 Local Data Share（LDS）延迟大幅改善，超越 Nvidia：

- 每 WGP 128 KB LDS（2×64 KB block，对应两个 CU）
- 延迟改善对光线追踪 BVH 遍历栈操作有直接收益（AMD GPU 在 RT 场景中 LDS 存储 BVH 栈）

## 计算吞吐

- FP32 FMA（含 VOPD）：约 61–62 TFLOPS（Nemes benchmark，全 WGP 负载）
- FP16 packed math（v_pk 指令）：翻倍，但 VOPD 不支持 packed FP16 双发射
- FP64：较 RDNA 2 下降一半（每 WGP 每周期 4 次，RDNA 2 为 8 次）
- INT32 乘法：极慢（RDNA 3 与 RDNA 2 相同，约为 FP32 四分之一速率）

## Chiplet 实现

7900 XTX 采用 MCM 封装：

- 主图形 die（5nm）：WGP、寄存器文件、L0/L1 缓存
- 内存控制器 die（6nm）：Infinity Cache、GDDR6 控制器

chiplet 代价是 Infinity Cache 访问延迟上升，以及更复杂的封装成本（需 interposer 级别的高带宽互联）。收益是主 die 面积更小，可使用更先进工艺。

## 与 Ada Lovelace 对比

AMD 和 Nvidia 在同一性能档位（7900 XTX vs RTX 4080）采用了截然不同的设计哲学：

- AMD：chiplet + 大带宽存储层次（384-bit VRAM + Infinity Cache）
- Nvidia：单大芯片（4nm）+ 超大 L2（72–96 MB），更简单的缓存层次

[[rendering/ada-lovelace-architecture|Ada Lovelace]] 在高 SM 占用时 VRAM 带宽略逊，但缓存层次更简单，L2 容量巨大，减少了对外部带宽的依赖。

## Sources

- [[sources/chipsandcheese-rdna3-architecture]]
