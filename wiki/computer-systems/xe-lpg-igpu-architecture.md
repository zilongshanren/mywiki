---
tags: [gpu, intel, xe-lpg, igpu, meteor-lake, microarchitecture]
date: 2026-04-27
sources: 2
---

# Xe-LPG iGPU 架构

Xe-LPG（Low Power Graphics）是 Intel 用于 Meteor Lake 集成 GPU 的架构，是 Xe-HPG（Arc A770 等离散 GPU 所用架构）的 iGPU 衍生版本，去除了矩阵乘单元（XMX）。

## 系统集成

Meteor Lake 放弃了自 Sandy Bridge 起沿用的"iGPU 共享 CPU L3 缓存"设计。iGPU 作为独立 tile（TSMC 5nm）通过 Scalable Fabric 连接，跨 die 延迟约 10 ns。好处是 iGPU 能有针对性地构建自己的缓存层级，不再与 CPU 缓存争用；代价是每次 CPU-GPU 数据交换都要越过 die 边界。参见 [[meteor-lake-chiplet-architecture]]。

## 计算架构

Core Ultra 7 155H 的 iGPU 配置为 8 个 Xe Core，分两个 Render Slice，最高频率 2.25 GHz，峰值 4.5 TFLOPS FP32。

每个 Xe Core 包含 16 个 Vector Engine（XVE），每个 XVE 有两个执行端口：
- Port 0：FP32/FP16 主数学运算
- Port 1：整数、特殊函数、FP64 等

与 Xe-HPG 相比，Xe-LPG 缺少 Port 2（矩阵乘单元 XMX）。每个 XVE 可同时持有最多 8 个线程。

**静态寄存器分配**是 Intel 与 AMD/NV 的关键区别：每个线程固定占用 128 个寄存器，不论实际使用多少。因此 GPU 占用率（occupancy）不受寄存器文件容量限制，而 AMD RDNA 3 每 SIMD 最多 16 线程、实际占用率随每线程寄存器用量下降。

**成对 XVE 锁步**：配对的两个 XVE 必须执行同一指令，导致即使连续对齐的 SIMD16 组内出现分支方向不同，也会触发分支发散惩罚。

## 缓存层级

| 层级 | 容量 | 说明 |
|------|------|------|
| L1 数据缓存 | 192 KB（实用 160 KB） | 每 Xe Core 私有；可部分用作 SLM |
| Texture Cache | ~32 KB | 独立只读；与 AMD/NV 统一缓存不同 |
| L2 | 4 MB | 全 GPU 共享；与 RTX 3070 相同容量 |

AMD Phoenix（Radeon 780M）L1 总量为 256 KB 共享，容量更大但为共享设计；Meteor Lake L1 虽每 Xe Core 较小，但 8 个 Xe Core 的私有 L1 总量相当可观。

## 光线追踪

Xe-LPG 从 Xe-HPG 继承了硬件光线追踪加速单元（RTA），详见 [[xe-lpg-raytracing]]。RTA 坐落于每个 Xe Core 内部，负责全程 BVH 遍历，通过 restart trail + short stack 将遍历状态保存在寄存器中，延迟低于 AMD 基于 LDS 的遍历栈方案。

## 与 AMD Phoenix 的对比

AMD Radeon 780M 在计算吞吐和缓存带宽上略占优势，但 Meteor Lake 在缓存容量上更具优势（4 MB L2 vs Phoenix 更小的 L2）。两者 DRAM 带宽基本持平，但 Meteor Lake 使用更快的 LPDDR5，在大数据传输时略有优势。参见 [[amd-phoenix-soc]]。

## Sources

- [[sources/chipsandcheese-meteor-lake-igpu]]
- [[sources/chipsandcheese-meteor-lake-igpu-rt]]
