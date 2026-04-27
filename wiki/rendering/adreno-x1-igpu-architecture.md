---
tags: [gpu, qualcomm, adreno, snapdragon, igpu, laptop, tiled-rendering, gmem, wave64]
date: 2026-04-27
sources: 1
---

# Adreno X1（Snapdragon X Elite）iGPU 架构

Adreno X1 是高通为 Snapdragon X Elite 笔记本平台开发的集成 GPU，官方营销名称"Adreno X1"，驱动内部型号 Adreno 741。它是 Snapdragon 8+ Gen 1 所用 [[adreno-640-architecture|Adreno 730]] 的扩展版本：更多 Shader Processor（SP）、更高主频（1.25–1.5 GHz vs 900 MHz），并在内存子系统上进行了显著改进。

## 执行单元结构

Adreno 的基本计算单元称为 **Shader Processor（SP）**，每个 SP 内含两个 **uSPTP**（Micro Shader Processor Texture Processor）。每个 uSPTP 对应 AMD RDNA 的 CU 级别，内含纹理单元和独立纹理缓存，自身再分为两个调度分区。这样一个 SP 在结构上类似 RDNA 的 WGP 或 NVIDIA Maxwell/Pascal 时代的 SM。

每个调度分区拥有 64-wide FP32 执行单元，支持 FP16 双速执行，8 个特殊函数单元处理反平方根等复杂操作。Adreno X1 采用 **wave64 或 wave128** 模式，宽向量有助于摊薄指令前端开销，但会加重分支发散惩罚，并对寄存器文件形成压力。每个 uSPTP 的寄存器文件容量提升至 192 KB（较 Adreno 730 的 64 KB 增加 50%），即每调度分区 96 KB，仍低于 AMD RDNA 3 iGPU 的单 CU 128 KB。

## 缓存层次

Adreno X1 形成四级缓存结构，这是 Adreno 系列的首次四级设计：

1. **L1 纹理缓存**：2 KB/uSPTP（所有代际中容量最小），延迟略高于竞品的大容量 L1
2. **集群缓存（Cluster Cache）**：128 KB，跨若干 uSPTP 共享，三个实例共 384 KB。与 AMD RDNA 的 L1 Cache 定位类似，但 Adreno X1 的集群缓存承载更多流量，因为计算访问会绕过纹理缓存直接访问这一层
3. **L2 缓存**：GPU 全局共享
4. **SLC（System Level Cache）**：6 MB，约 211 GB/s 带宽，在超出 L2 容量的大工作集场景提供帮助

计算访问（非纹理采样）**绕过** L1 直接访问集群缓存，这一特性与 AMD/Intel/NVIDIA 的通用 L1 设计截然不同。集群缓存延迟约 56–67 ns，与 AMD RDNA3 L1 延迟相当，但带宽远低于竞品——甚至低于 Adreno X1 自身的 L1 纹理缓存带宽（< 1 TB/s）。

DRAM 方面，128-bit LPDDR5X 内存控制器提供略优于 Intel Meteor Lake 和 AMD Phoenix 的带宽，这是高通在笔记本场景为数不多的竞争优势之一。

## GMEM：多用途片上存储

Adreno 的传统设计是为 **TBDR（Tile-Based Deferred Rendering）** 架构配备专用的片上 Tile Buffer，即 **GMEM**。Adreno X1 将 GMEM 扩展至 3 MB（Adreno 730 为 2 MB）。

GMEM 的独特价值在于**多用途复用**：当渲染管线不使用 Tiled Rendering 时（如 Compute、Raytracing），GMEM 可被重新分配为局部内存（Local Memory）或颜色/深度缓存。作为局部内存使用时，延迟仅略高于 AMD 和 Intel 将局部内存内嵌在 GPU core 中的方案，与 Adreno 730 基本相当。局部内存容量上限为 32 KB/kernel，全 GPU 最多同时分配 384 KB，超出后并行 workgroup 数量受限。

## 计算性能与短板

在 FP32 和 FP16 基础算力上，Adreno X1 与 Intel Meteor Lake 接近。AMD Phoenix 因高频宽向量+双发射，FP32 吞吐大幅领先。特殊函数（反平方根等）Meteor Lake 反而领先 Adreno X1。

明显弱点：
- **INT32 加法**性能异常低（Vulkan 下表现差于 OpenCL，原因不明）
- **INT64** 性能极差
- **FP64** 完全不支持
- FluidX3D 流体仿真基准表现极差，甚至不如十年前的 Intel HD 530

## 光线追踪与驱动

Adreno X1 继承自 Snapdragon 8 Gen 2 引入的硬件光追加速，但**不支持 DirectX 12 Ultimate**，光追仅可通过 Vulkan API 使用。这使绝大多数支持光追的 PC 游戏无法在 Adreno X1 上启用此功能。

驱动成熟度是 2024 年 Adreno X1 的核心短板：部分游戏无法启动，驱动更新后稳定性反而下降，无统一安装包，用户体验远落后于 AMD/Intel/NVIDIA 的驱动生态。

## Sources

- [[sources/chipsandcheese-sde-adreno]]
