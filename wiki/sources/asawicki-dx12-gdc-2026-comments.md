---
tags: [source, D3D12, GDC2026, Microsoft, 调试]
date: 2026-04-19
sources: 1
---

# DirectX 12 News from GDC 2026 - My Comments（Adam Sawicki）

[[adam-sawicki]] 2026 年 3 月 15 日在 GDC 2026 收尾后发的长篇评注。作者离开 AMD 加入 Plastic 后从 IHV 视角切换到应用端视角，说自己"终于可以 brutal honesty"评论 Microsoft 的公告——这篇是他回 GDC 的第一发。

## 摘要

按 Microsoft 在 GDC 2026（"GDC Festival of Gaming"）上的 DirectX 12 新特性分类逐项点评：

1. **主机级开发者工具下放 PC**：PIX 重大升级、DirectX Dump Files（.dxdmp）、PIX API（C++/C#/Python）、HLSL `DebugBreak()` 内建、PIX 事件透传驱动、2027 计划的"real-time on-chip shader debugging"
2. **ML for DirectX**：HLSL Long Vectors（提案 0026）、Linear Algebra Matrix（提案 0035，取代此前的 Cooperative Vectors preview）、全新的 **DirectX Compute Graph Compiler**（面向完整 ML 模型的图优化/算子融合/内存规划）
3. **Advanced Shader Delivery + Shader Compiler Plugin** + **Partial Graphics Programs**
4. **DirectStorage 1.4**：Zstandard 支持替代 GDeflate + Game Asset Conditioning Library
5. **DXR Tier 2.0 / SM 6.10**：CLAS、Cluster Template、Compressed1 position encoding、Partitioned TLAS、Indirect BLAS 构建

每条都带作者的主观评价，不回避 Microsoft 的历史包袱（DXR 文档碎、DirectSR 被悄悄砍、HLSL printf 一直不标准化、Render Pipeline Shaders 已经死了）。

## 关键要点

- **GDC 公告 ≠ 能马上用**：作者强调这些特性都是"ship when it's done"，本周没有任何东西真正可用
- **PIX Markers 终于透传驱动**——长期让 AMD/Intel 工具团队头疼的痛点解决，AGS 库的 workaround 可以退休
- **DebugBreak() 没带参数**是遗憾——Sawicki 公开请愿"哪怕一个 uint4 也好"
- **HLSL printf** 还是没标准化——Chris Bieneman（Microsoft 员工）2025 年底写的[那篇](https://www.abolishcrlf.org/2025/12/31/Printf.html)仍是非官方提案
- **四家 GPU 厂商同台站台**（AMD/Intel/Nvidia/Qualcomm）是重要信号——上一次这种场面是关于 Vulkan
- **Work Graphs 不是 ML 方案**——作者特意澄清，Work Graphs 服务渲染 compute，不做 operator fusion
- **DirectX Compute Graph Compiler 是全新一类工具**——编译整个 ML 模型而非单个 shader，直接对标 ONNX Runtime / TensorRT 这一层
- **DXR Tier 2** 用 CLAS/PTLAS 把加速结构扩到三层，解决"每帧 TLAS 重建"顽疾
- **Nvidia Streamline 是 Microsoft 没做的 API layer 机制的厂商版**——Sawicki 希望 Microsoft 能像 Vulkan 那样正式支持 layer 注入

## 链接到的概念

- [[pix-api-and-dxdmp]]
- [[dxr-tier-2-clas-ptlas]]
- [[advanced-shader-delivery]]
- [[hlsl-cooperative-vectors-tensor-cores]]
- [[d3d12-work-graphs]]
- [[adam-sawicki]]

## 原文

- 链接：<https://asawicki.info/news_1801_directx_12_news_from_gdc_2026_-_my_comments>
- 本地：`raw/articles/asawicki.info/2026-03-15_directx-12-news-from-gdc-2026-my-comments.md`
