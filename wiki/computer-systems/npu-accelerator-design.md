---
tags: [cpu, npu, accelerator, ai, machine-learning, intel, movidius, meteor-lake]
date: 2026-04-27
sources: 1
---

# NPU 加速器设计

NPU（Neural Processing Unit，神经处理单元）是专为机器学习推断优化的片上加速器，以大规模 MAC（乘累加）阵列为核心，在低功耗条件下提供高 INT8/FP16 吞吐量。Intel Meteor Lake 集成的 NPU 3720 是客户端 SoC 中最具代表性的实现之一。

## 设计哲学

加速器设计的本质是"以灵活性换效率"：通过将硬件紧密匹配特定计算模式（矩阵乘法、卷积），获得比通用 GPU 或 CPU 更好的单瓦特性能。代价是对不支持的操作（如 FP64、某些激活函数）束手无策，且软件移植成本高昂。

## Intel NPU 3720 架构

NPU 3720 基于 Movidius 的 Myriad 平台（Intel 2016 年收购），其架构层次：

**控制层**：两枚 LEON SPARC 微控制器——LeonRT 处理主机命令，LeonNN 调度 NCE 任务。LEON 核心有独立 L1 缓存并运行 RTOS。

**计算层**：两个 Neural Compute Engine（NCE）tile，每 tile 含 512 个 MAC Processing Engine（MPE），每 MPE 支持 4 INT8 MAC/cycle，全 NPU 峰值 4096 INT8 MAC/cycle，合计 9.5 TOPS @ 1.16 GHz。FP16 以半速执行。

**DSP 层**：SHAVE（Streaming Hybrid Architecture Vector Engine）核心处理无法映射到 MAC 阵列的操作，如激活函数、数据类型转换，以及 FP32 计算（约 50 GFLOPS）。但不支持 FP64，这是实际使用中的主要障碍之一。

**内存层**：每 NCE 有 2 MB 软件管理 SRAM（scratchpad），需编译器显式调度数据搬运。另有约 128 KB 快速本地存储（延迟 ~16 ns）。整个 NPU 通过 IOMMU 接入 Meteor Lake 的 Scalable Fabric，与 iGPU 共享 LPDDR5。

## Scratchpad vs 缓存

NPU 采用 scratchpad 而非传统缓存，是有意为之的权衡：

- **优势**：无 tag 比较开销，无缓存一致性协议，访问延迟确定性强，单位面积存储密度更高
- **代价**：编译器或运行时必须显式管理数据搬运，软件复杂度大幅提升

相同思路也见于 GPU 的 Local Memory（OpenCL）和 Shared Memory（CUDA），以及各类 DSP 的本地 RAM。[[cuda-memory-hierarchy]] 中的 shared memory 是最广为人知的变体。

## 性能实测（Meteor Lake NPU 3720）

Intel Core Ultra 7 155H 实测：

| 场景 | NPU | iGPU（Arc Graphics） | RX 6900 XT |
|------|-----|---------------------|-----------|
| FP16 MatMul 实测 | 1.35 TFLOPS（理论 4.7） | 更高（FP32） | 远高 |
| Stable Diffusion 1.5（it/s） | ~0.85 | iGPU FP32 快 62% | 快 6.7× |

DMA 带宽约 10 GB/s，明显弱于 iGPU 的 19 GB/s，在大模型场景下成为瓶颈。

## 软件生态挑战

硬件设计之外，软件栈是 NPU 落地的最大障碍。Intel OpenVINO 需要为每款 NPU 编译专属模型图（IR），不支持 FP64 导致 Stable Diffusion UNET 无法直接编译；ONNX DirectML 路径同样需要特殊处理（NPU 不是 DXGI 设备）。这些障碍对普通消费者而言几乎不可逾越。

GPU 的通用计算生态经历了十余年（CUDA 自 2007 年）才达到今天的成熟度；NPU 软件栈的成熟尚需时日。

## 与"AI PC"营销的落差

Meteor Lake 发布时的"AI PC"定义被媒体广泛引用，但从实测看：iGPU 在绝大多数 ML 工作负载上既快又更通用；离散 GPU 更是完全不在一个量级。NPU 的真实价值在于**持续低功耗推断**（如实时摄像头处理、语音唤醒），而非取代 GPU 成为通用 AI 计算平台。

## Sources

- [[sources/chipsandcheese-meteor-lake-npu]]
