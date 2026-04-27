---
tags: [cpu, gpu, nvidia, arm, neoverse, hpc, interconnect]
date: 2026-04-27
sources: 1
---

# Grace Hopper（GH200）：Nvidia 的半成品 APU

GH200 是 Nvidia 将 CPU 与 GPU 封装为单一产品单元的首次高性能尝试：Grace CPU（72 颗 [[neoverse-v2-microarchitecture|Neoverse V2]] 核）+ H100 SXM 级 GPU，通过专有高带宽互联 **NVLink C2C** 相连。与 AMD 通过 Infinity Fabric 构建的 MI300A 真正集成 GPU（iGPU）不同，GH200 的 CPU 与 GPU 各有独立显存池，本质上是"封装在一起的离散 GPU"。

## 系统结构

- **Grace CPU**：72 颗 Neoverse V2，运行频率最高 3.44 GHz，置于 Nvidia Scalable Coherency Fabric（SCF）mesh 上；114 MB L3 共享缓存；480 GB LPDDR5X-6400（480 位总线，384 GB/s 理论带宽）。
- **H100 GPU**：132 SM 启用（144 SM 完整版），96 GB HBM3（12 控制器全开，6144 位总线，~4 TB/s 理论带宽）；软件侧作为 PCIe 设备暴露。
- **NVLink C2C**：900 GB/s 双向带宽（各向 450 GB/s），比 PCIe Gen 5 x16 高约一个数量级；支持硬件缓存一致性，HBM3 内存作为 NUMA 节点暴露给 CPU。

## 互联性能与局限

NVLink C2C 带宽优势明显，CPU 访问 HBM3 的带宽可媲美 Zen 4 双路配置的跨 socket 带宽。但延迟极差：CPU 访问 HBM3 约 800 ns，比访问本地 LPDDR5X 多出约 592 ns。相比之下，AMD Infinity Fabric 跨 socket 延迟仅约 120 ns 惩罚，Intel QPI 也更优。

实测中还出现了系统不响应（SSH 卡死、需重启）和 PCIe 报错等稳定性问题，体现了自研互联平台验证的难度。

## Neoverse V2 实现特异性

Grace 与 [[neoverse-v2-microarchitecture|Graviton 4]] 同用 Neoverse V2 核，但 Nvidia 的实现决策使 Grace 在常见 workload 中反而弱于 Graviton 4：

| 因素 | Grace | Graviton 4 |
|------|-------|------------|
| 频率 | 3.44 GHz | 2.8 GHz |
| L2 | 1 MB | 2 MB |
| L3 延迟 | ~125 周期（>38 ns）| ~68 周期（25 ns）|
| DRAM 延迟 | >200 ns（LPDDR5X）| ~114 ns（DDR5）|

较小的 L2 + 高延迟 L3 + 高延迟 LPDDR5X，使 Neoverse V2 的大后端无法充分吸收 L2 miss 代价。libx264 测试中 Grace 落后于 Graviton 4，证明"频率优势"被"延迟劣势"完全抵消。

这个案例本质上揭示了 ARM 授权模式的挑战：ARM 在仿真环境中评估核心，无法预知所有 implementer 的平台特性。Nvidia 选择了对并行计算优化但对通用 workload 不友好的内存配置。

## H100 GPU

GH200 中的 H100 是市售最高规格变体之一（完整 HBM 总线 + 更高功耗限制 900W）。VRAM 延迟由于更高频率从 330 ns 降至约 300 ns。软件侧兼容性不如独立 H100，OpenCL/NVLink C2C 均有测试失败/系统挂起报告。

关于 H100 本身的 GPU 架构，参见 [[h100-hopper-architecture]]。

## 竞争格局

GH200 代表 Nvidia 对 AMD MI300A（iGPU 真集成，赢得 El Capitan）的反制方案。Nvidia 通过 NVLink C2C 解决 CPU-GPU 通信带宽问题，同时保留了 HBM3 与 LPDDR5X 分离的灵活性（不限于 128 GB 的统一内存上限）。Isambard-AI 超算等已选择 GH200，两者在 HPC/AI 领域的竞争仍将持续。

## Sources

- [[sources/chipsandcheese-grace-hopper]]
