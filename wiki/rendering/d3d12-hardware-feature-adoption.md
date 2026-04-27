---
tags: [d3d12, gpu, hardware, steam-survey, feature-support, minimum-requirements]
date: 2026-04-27
sources: 1
---

# D3D12 硬件特性采用率（2025 年底）

每隔几年就有一道现实的问题摆在自研引擎开发者面前：**新 GPU 特性的硬件覆盖率到底够不够用？** 2025 年底，答案比许多人预想的要乐观。

## 数据方法论

两个公开来源交叉使用：Steam 硬件调查（每月更新，统计 Steam 用户 GPU 型号分布）和 D3d12infoDB（社区驱动，按架构记录各特性支持等级）。方法是先将 Steam 调查中的 GPU 型号手动映射到架构，再聚合 D3d12infoDB 的特性数据，得到"架构 × 特性"矩阵。

两组数据叠加后仍有约 12% 的不确定区间——部分 GPU 名称无法确定架构（如"AMD Radeon Graphics"）、一些 GPU 市场份额低于 Steam 调查的上榜阈值、D3d12infoDB 缺乏老旧架构的记录。

另一个校准因素是受众偏差：画质导向游戏的玩家群体会向新/高端硬件漂移；简单 indie 游戏则向旧/低端漂移。Steam 调查是所有 Steam 用户的混合样本，未必代表具体游戏的目标受众。

## 各特性覆盖率概况（2025 年 11 月数据）

以下数据均指**有活跃驱动支持**的 GPU 子集：

- **Shader Model 6.5 及以下**：近乎普适，可无条件要求
- **SM 6.6（完全 Bindless / Dynamic Resources）**：只需放弃 Kepler + Gen 9/9.5（合计 < 2%），强烈推荐底层渲染开发者直接上
- **SM 6.7**：放弃 AMD GCN3（0.05%），额外特性较少，成本接近零
- **SM 6.8**（含 Work Graph 前提）：需放弃全部 Intel 和 Qualcomm GPU（约 5%）
- **DXR**：86.62%——注意 GTX 16xx（Turing 16）有 Mesh Shader 但**没有**硬件 DXR
- **Mesh Shader**：95.95%——实际上比 DXR 更普及，可作为优化选项安全使用
- **Enhanced Barriers**：97.62%——唯一缺失的是 Intel Xe（集显），可近似无条件采用
- **VRS Tier 2**：有价值但条件多——高分辨率时效果好，与 Upscaler 共存问题多
- **Work Graphs**：74.1%——技术新，案例少（UE5 Nanite 是少数出货例子）
- **Sampler Feedback**：支持率可观，但实际游戏应用几乎为零；手动流式方案更灵活

## 最低要求选取思路

从架构表由低往高扫描，找到"净收益大于受众损失"的切割点：

- **轻量 indie**：RDNA1 / Turing 16 起步，获得 Mesh Shader + Enhanced Barriers，同时覆盖绝大多数潜在玩家
- **画质竞争型**：RDNA2 / Turing 20 起步，直接获得 DXR + Mesh Shader + SM 6.6 + Conservative Rasterization Tier 3；目标受众硬件偏新，损失不大
- **前沿技术展示**：可考虑要求 Ampere / RDNA3 以获得 Work Graphs，但需接受放弃 Pascal 带来的 > 6% 缺口

特性之间存在"包含关系"：要求 DXR 就等于免费得到 Mesh Shader（所有 DXR 硬件均支持 Mesh Shader）；要求 SM 6.8 就等于已经有了 Enhanced Barriers。这种传递性可以简化决策。

## 驱动支持与 EOL 风险

不是所有在 Steam 上出现的 GPU 都还有活跃驱动更新：

| 厂商 | 最老受支持架构 |
|------|--------------|
| AMD  | RDNA1（GCN 4 已有信号进入独立驱动分支） |
| Nvidia | Turing |
| Intel | Xe（Xe-HPG / Xe-LPG 长期预期不明朗） |
| Qualcomm | X1 |

AMD 已为 RDNA1/2 建立独立驱动分支，暗示主线驱动最终会放弃这两代；若对应[[gpu-driver-support-lifecycle]]中 GCN 被砍的节奏，游戏开发周期 3–5 年内可能需要重新评估。Nvidia 刚刚砍掉 Maxwell/Pascal/Volta，Turing 短期安全。Intel 的退出时间线最难预测。

## 2025–2026 的 DRAM 市场背景

消费级 GPU 的未来更受宏观因素压制：仅三家公司控制 93% 的 DRAM 产能，AI 需求爆发后 OpenAI 一次性锁定全球 40% DRAM 输出；DDR5 价格在短时间内翻三倍，Micron 宣布退出消费品牌，Nvidia 计划在 2026 年初削减 RTX 50 系产能。这意味着高 VRAM GPU 将越来越稀缺，Sampler Feedback Streaming 这类节省 VRAM 的方案长期价值上升，而 DXR 所需的大量 VRAM（加速结构）成本也随之上涨。

## 相关

- [[directx12-api-overview]]
- [[d3d12-work-graphs]]
- [[meshlets-and-mesh-shaders]]
- [[bindless-rendering]]
- [[simplified-pipeline-barriers]]
- [[gpu-driver-support-lifecycle]]
- [[pc-gpu-driver-compat-qa]]
- [[rdna2-architecture]]
- [[blackwell-gb202-architecture]]

## Sources

- [[sources/asawicki-gpu-state-2025]]
