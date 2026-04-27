---
tags: [gpu, blackwell, igpu, nvidia, 缓存]
date: 2026-04-19
sources: 1
---

# GB10 iGPU：Blackwell 消费级变体

GB10 的核心卖点是把 48 SM、最高 2.55 GHz 的 Blackwell GPU 塞进 iGPU，基本对标 RTX 5070，只是功耗预算、cache 容量、显存带宽都被打了折。CPU 侧见 [[gb10-memory-subsystem]]。

## 不是 datacenter Blackwell

Nvidia 在 Hot Chips 2025 演讲里把 GB10 放在"从 rack-scale 到单卡到 iGPU 的同一架构延续"叙事里，但实际上 **GB10 的 SM 是 consumer Blackwell（compute capability 12.1），不是 B200/GB300 的 datacenter Blackwell（10.0）**。差异包括：
- L1/Shared Memory：GB10 = 128 KB/SM，datacenter = 256 KB/SM
- FP64 比率：GB10 = 1:64 FP32，datacenter 有强 FP64 单元
- 5th-gen Tensor Core 特性仅 datacenter 独占
- GB10 保留了硬件光追、消费级 SM 时钟更高

结果是为 datacenter 写的 CUDA kernel 搬到 GB10 上常常跑不起来。Chester 认为营销上叫"统一架构"对投资人好听，但技术受众需要的是精确。"GB10 用与 GB300 同一架构"就像说"Strix Halo RDNA3.5 与 MI300X 同一架构"。

## 两级缓存即终点

Blackwell GPU 侧延续两级缓存：
- 每 SM 私有 L1/Shared Memory 128 KB（两者共享同一块 SRAM）
- 24 MB 统一 L2 作为 last level cache

与 AMD 多级渐进容量（RDNA 的 L0/L1/L2/Infinity Cache 四层）不同，Nvidia 靠大一级 L2 拦住绝大多数 GPU 流量，系统侧互连只处理 DRAM 访问。Strix Halo 则把 GPU cache 放在 SLC 那一端，对 Infinity Fabric 造成近 1 TB/s 压力；两种风格各有取舍。

## SLC 在 GPU 侧几乎隐形

16 MB 的 SLC 比 24 MB GPU L2 还小，所以 GPU 延迟曲线看不出 SLC 台阶；并且 SLC 与 L2 不是 exclusive 关系，容量不叠加。SLC 的真实角色还是"引擎间数据共享"（CPU↔GPU 不经 DRAM）。

## L1 设计的优势

单 SM L1 在依赖数组访问中几乎追上 AMD 的标量 cache 延迟，同时容量更大（128 KB vs AMD 16 KB 标量 + L0 向量的总和）。Nvidia 的数组地址生成本就高效，所以改用 pointer dereference 时提速不多；AMD 则在 pointer 版本里才显出标量 cache 的真正低延迟——即"测法决定结论"的典型。

## Shared Memory 延迟

GB10 的 Shared Memory 依赖访问延迟 13 ns，略快于 B200（14.84 ns）。牺牲容量换速度在消费级变体里常见。Shared Memory 的角色见 [[cuda-memory-hierarchy]]。

## 指令缓存

每 SM 四个 sub-partition，每个 partition 配 32 KB L0 I$，足以 1 IPC 喂饱。四个 partition 共用 128 KB L1 I$，两 partition 争抢 L1I 时 per-partition 掉到 0.5 IPC。Blackwell 固定 16-byte 指令格式，让这个结构算得明白。

## 带宽

48 个 SM × 48 个 L1 实例，给 GPU 带来极高 L1 聚合带宽——Nemes Vulkan 测试里远超 Strix Halo。L2 也比 AMD 2 MB L2 容量大带宽高。写路径上，GPU 均用 write-through L1，所以写直接进 L2，GB10 L2 以半速处理写，写带宽接近 1 TB/s。

## 实际负载

- **FluidX3D**：FP32 / FP16S 赢 Strix Halo，FP16C 模式（转换要软件实现）反而输；Intel Arc B580 因为 456 GB/s GDDR6 在内存受限场景大幅领先两者
- **VkFFT**：GB10 最稳，Strix Halo 在各种配置里都未能超过 GB10，B580 高方差
- **FAHBench**：单精度下 GB10 通吃，因为 FAHBench 靠 local memory 把数据留在芯片上，成了算力题
- **游戏**：GB10 因为 Arm ISA + 大多数 PC 游戏只有 x86-64 二进制，翻译执行开销显著，Cyberpunk 2077 1080p medium 只到 50 FPS（Strix Halo ~90 FPS）

## SVM 支持

GB10 支持 OpenCL 的 coarse-grained SVM（不能同时在 CPU/GPU 双侧映射同一 buffer），但不像 Qualcomm/Arm iGPU 那样在底层偷偷做全 buffer 拷贝。实打实共享物理内存。

## 相关

- [[gb10-memory-subsystem]]
- [[cuda-memory-hierarchy]]
- [[gpu-latency-hiding]]
- [[memory-hierarchy]]

## Sources

- [[sources/chipsandcheese-gb10-gpu]]
- [[sources/chipsandcheese-blackwell-gb202]]
