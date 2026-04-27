---
tags: [gpu, nvidia, ray-tracing, dlss, rendering, ada-lovelace, rtx4000]
date: 2026-04-27
sources: 1
---

# Nvidia Ada Lovelace 架构（RTX 4000）

Ada Lovelace 是 Nvidia 第三代 RTX 架构（2022），继 Turing 和 Ampere 之后进一步强化光线追踪与 AI 超采样能力。顶级 AD102 die 集成 761 亿晶体管（GA102 的约 2.7 倍），SM 数从 82 增至 128（AD102 全开为 144），boost 时钟提升至 2.52 GHz，整卡 TDP 450W。

## 光线追踪：三角形吞吐量倍增

Ada Lovelace 相比 Ampere 再次将三角形求交速率翻倍（Turing→Ampere 已翻倍一次）。这一选择背后有明确的架构逻辑：

GPU 的 BVH 结构倾向于**胖 BVH**——减少树层级、增大 leaf 节点的三角形数量。这样可以减少指针追逐（降低缓存延迟压力），代价是更多算术运算。而 GPU 恰好具有高计算吞吐、高缓存延迟的特性，胖 BVH 正好扬长避短。提高三角形吞吐量使得 BVH 可以做得更胖，进一步减少 BVH 遍历的内存访问依赖。

## Shader Execution Reordering（SER）

SER 是 Ada Lovelace 的重要新特性，目的是在光线追踪时对工作进行重排序以提高 SM 的并行效率。Nvidia 将其类比为 CPU 的乱序执行，但实际机制更可能是：

- 更深的内存流水线队列，增加访问合并机会（与 Turing 的 texture unit 重排序扩展路线一致）
- 或者是 Volta 独立线程调度的延伸：识别来自不同 warp 中分叉部分的相同指令，动态组合成新 warp

无论如何，SER 本质上仍属于 warp 级别的工作组织优化，并非真正的指令级乱序。

## DLSS 3：帧生成

DLSS 3 在 DLSS 2 超分辨率的基础上新增**帧插值**（Frame Generation）：利用光流估算像素运动，用 ML 模型在两帧之间合成一整个新帧，帧率理论上可以超越仅靠降分辨率所能达到的上限。

帧生成依赖大量张量计算：Ada Lovelace 每 SM 的 FP16 tensor 吞吐量是 FP32 向量的 **16 倍**（Ampere 是 8 倍），使得实时推理合成完整帧成为可能。帧生成完全绕过游戏引擎的 CPU 处理循环，理论上可以突破 CPU 瓶颈——但代价是引入额外延迟（插值帧在后一真实帧已就绪时才呈现）。

DLSS 3 仅支持 Lovelace 显卡，原因在于前代卡没有足够的张量算力驱动完整帧合成。

## 光栅化扩容

RTX 4090 相比 3090 的理论 FP32 吞吐量翻倍，但在 Assassin's Creed Valhalla（无 DLSS/RT）测试中实际提升约 50%，符合预期（应用并非全程计算绑定，且内存带宽未同步翻倍）。AD102 使用 384-bit GDDR6X，并引入传言规模达 **96 MB 的 L2 缓存**以弥补带宽增速慢于计算增速的差距。

## AMD RDNA 3 预告

同期 AMD 尚未公布 RX 7000 详情，但 LLVM patch 泄露了 RDNA 3 的方向：

- 新增 LDS 专用指令加速 BVH 遍历栈操作（AMD 用 LDS 存储遍历栈）
- 引入 **VOPD**（Vector Operation Dual）：双发射同一 SIMD 周期内两个 vector 操作，以廉价方式将 FP32 吞吐量翻倍，但有寄存器 bank 和操作类型的限制

## 相关

- [[gpu-latency-hiding]]
- [[gcn-wave-occupancy]]
- [[gpu-memory-hierarchy-latency]]
- [[cdna2-mi200-architecture]]

## Sources

- [[sources/chipsandcheese-rtx4090-ada-lovelace]]
- [[sources/chipsandcheese-arc-a770]]
