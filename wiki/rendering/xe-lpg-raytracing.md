---
tags: [raytracing, intel, xe-lpg, bvh, hardware-rt, igpu]
date: 2026-04-27
sources: 1
---

# Xe-LPG 硬件光线追踪

Meteor Lake iGPU（Xe-LPG 架构）的光线追踪加速单元（RTA）是 Intel 从 Arc 离散 GPU（[[xe-hpg-architecture]]）继承的硬件特性，代表了与 AMD RDNA 方案截然不同的设计哲学。

## 硬件架构

RTA 位于每个 Xe Core 内部，通过 Xe Core 内部互联与 XVE 和 L1 缓存通信。其核心职责是全程自主完成 [[bvh-traversal-hardware|BVH 遍历]]，通用 XVE 仅负责：
1. 发起光线（发送消息给 RTA）
2. 处理 hit/miss 着色器结果

在 RTA 执行遍历期间，XVE 处于低占用率状态——这与 RDNA 着色器程序全程保持活跃的行为形成对比。

## Restart Trail 遍历算法

Xe-LPG 不使用传统深度优先遍历（需要可变长度显式栈）。取而代之的是：

- **Restart trail**：29 个 3-bit 条目，记录 BVH 每层已访问的子节点数量，支持从根节点重启遍历并跳过已访问路径
- **Short stack**：4 条目，保存若干重启点，减少从根节点重启的频率

全部遍历状态占用不足 16 字节，可保存在 RTA 内部寄存器中，延迟远低于 RDNA 将遍历栈存于 LDS 的方案。代价是比深度优先搜索多约 16% 的遍历步骤，但 Intel 的研究表明此开销在实际场景中可以接受。

## 与 AMD RDNA 方案的对比

| 维度 | Intel Xe-LPG | AMD RDNA 2/3 |
|------|-------------|-------------|
| 遍历执行者 | 专用硬件 RTA | 着色器程序 + 部分固定功能 |
| 遍历状态位置 | RTA 内部寄存器 | LDS（本地数据共享） |
| 着色器生命周期 | 短暂（发出光线后退出） | 持续（等待 LDS/Texture 结果） |
| DXR 对应接口 | DXR 1.0 DispatchRays（原生）| DXR 1.1 RayQuery（内联，原生）|
| XVE 占用率 | 遍历期间极低 | 始终较高 |
| 线程启动开销 | 每 Xe Core 独立 dispatcher，>4100 万/s | 更少启动（着色器持续运行） |

RDNA 3 实测 Cyberpunk 2077 路径追踪着色器中，LDS 遍历栈操作有 46 周期等待，仅能通过线程级并行隐藏 10 周期。Intel 的寄存器方案可规避此延迟。

## 实测缓存表现

在 Cyberpunk 2077 路径追踪（7 FPS@2880×1800 + XeSS）和 3DMark Port Royal（8 FPS@2560×1440）测试中：

- 192 KB L1 缓存承担 >1 TB/s 内部带宽，命中率 87.9%
- 4 MB L2 有效拦截绝大多数 L1 miss；Port Royal 下 L2 miss 流量 46.2 GB/s，出现轻度 DRAM 带宽瓶颈（内存请求队列满载率 43.1%）
- RTA 和着色器的数据交换主要通过 L1 进行，L1 大容量是光追吞吐的关键支撑

## 实用价值争议

作者指出，iGPU 在无光追时已勉强维持 30 FPS，帧率余量不足以承担光追开销。相比而言，矩阵乘单元（XMX）用于 AI 超分辨率更有实际价值，而 Xe-LPG 恰恰省去了 XMX。

## Sources

- [[sources/chipsandcheese-meteor-lake-igpu-rt]]
