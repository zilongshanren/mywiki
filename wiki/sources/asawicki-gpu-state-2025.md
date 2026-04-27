---
tags: [source, rendering, d3d12, gpu, hardware, steam-survey, dx12-features]
date: 2026-04-27
sources: 1
---

# State of GPU Hardware (End of Year 2025)（Adam Sawicki / asawicki.info）

[[adam-sawicki]] 博客发表于 2026 年 1 月（以 2025 年 11 月 Steam 硬件调查数据为基准），由客座作者 Dmytro "Boolka" Bulatov 撰写，系统梳理 D3D12 各项新特性在真实玩家硬件上的支持率，并给出不同类型游戏的最低硬件要求建议。

## 摘要

文章结合两个公开数据源——Steam 硬件调查（GPU 市场占有率）和 D3d12infoDB（各 GPU 架构对 D3D12 特性的支持情况）——分析了 2025 年底 D3D12 开发者在选择最低硬件要求时的实际处境。作者将所有主流 GPU 架构按厂商（AMD/Nvidia/Intel/Qualcomm）列出累积市场份额与每档新增特性，给出以下核心结论：Shader Model 6.5 几乎无需任何取舍即可设为基准；SM 6.6（Bindless）只需放弃约 2% 的旧卡；DXR 与 Mesh Shader 的硬件支持已分别达到约 87% 和 96%（仅限有活跃驱动支持的 GPU）；Enhanced Barriers 覆盖率接近 98%；Work Graphs 在有驱动支持的 GPU 中达 74%。同时，文章分析了 DRAM 短缺（OpenAI 购买了全球 40% DRAM 产能）对消费级 GPU 价格带来的系统性压力。

## 关键要点

- **数据来源**：Steam 硬件调查（2025 年 11 月）+ D3d12infoDB；由于部分 GPU 无法映射到架构，约 12% 市场份额存在不确定性
- **SM 6.5 可无条件基准化**：覆盖率接近普适，成本几乎为零
- **SM 6.6（完全 Bindless）**：只需放弃 Nvidia Kepler + Intel Gen 9/9.5（合计 <2% 份额），对底层渲染开发者强烈推荐
- **DXR**：有活跃驱动支持的 GPU 中 86.62% 支持；GTX 16xx 系列支持 Mesh Shader 但不支持 DXR；Turing 20 系以上才有完整 DXR
- **Mesh Shader**：95.95% 覆盖率（活跃驱动），可视为几乎普适的优化选项
- **Enhanced Barriers**：97.62% 覆盖，唯一缺失是 Intel Xe（纯集显架构），可近似无条件采用
- **VRS**：只在高分辨率渲染场景有价值；若使用 Upscaler 则需慎重（CoD 强制禁用 VRS + Upscaler 共存）
- **Sampler Feedback**：实际应用案例极少（仅见 HL2 RTX demo），手动实现 streaming 仍是主流
- **Work Graphs**：活跃驱动 GPU 中 74.1% 支持，目前只有 UE5 Nanite 有出货案例
- **GPU Upload Heaps**：依赖 ReBAR 启用状态，无法仅凭 GPU 型号推断，应作为可选优化
- **DRAM 危机**：OpenAI 囤积全球 40% DRAM 产能 → DDR5 价格三倍 → Micron 砍消费品牌 → Nvidia 削减 RTX 50 系产能，消费级 GPU 价格上行趋势确定
- **最低要求建议示例**：面向画质竞争游戏可要求 RDNA2 / Turing 20+（获得 DXR + Mesh Shader）；面向广泛受众则 RDNA1 / Turing 16 仍是平衡点

## 链接到的概念

- [[directx12-api-overview]]
- [[d3d12-work-graphs]]
- [[meshlets-and-mesh-shaders]]
- [[bindless-rendering]]
- [[simplified-pipeline-barriers]]
- [[shader-ir-pipeline]]
- [[gpu-driver-support-lifecycle]]
- [[pc-gpu-driver-compat-qa]]
- [[rdna2-architecture]]
- [[rdna4-architecture]]
- [[blackwell-gb202-architecture]]

## 原文

- 链接：https://asawicki.info/articles/state_of_gpu_hardware_2025.php
- 本地：`raw/articles/asawicki.info/2026-01-01_state-of-gpu-hardware-end-of-year-2025.md`
