---
tags: [source, rendering, graphics-api, dx12, metal, mantle, opengl]
date: 2026-04-27
sources: 1
---

# Rate my API（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2014 年 6 月的文章，在 Metal / Mantle / DirectX 12 / AZDO 同时涌现的节点，用"有用 × 易用 / 成本"框架逐一评估各图形 API 的实际价值。

## 摘要

文章提出评估 API 的三要素：**Working**（真实部署）、**Useful**（覆盖目标市场）、**Easy**（是否需要重写整个引擎）。用此框架逐一分析：

- **OpenGL + AZDO**：技术上是工程奇迹（绕过驱动多线程限制，把 resource binding 卸载到 GPU 端），但 AAA 场景下价值有限——主平台是主机，而 DX12 即将到来；AZDO 最适合 CG 软件（多平台、NVidia 主导）
- **Mantle**：设计合理，但仅覆盖 Windows + AMD，市场太小；如果一开始就包含 PS4 layer 会更有价值；最终 AMD 凭借 Frostbite/EA 支持勉强站稳，但终究难以持续
- **DirectX 12**：DX11 奠定了良好基础（Compute Shader、Tessellation），唯一大问题是多线程驱动合约设计导致命令生成反而变慢；DX12 解决此问题，且覆盖 Xbox One，是 AAA 的最优解
- **Metal**：Apple 版 Mantle，技术合理，iOS 市场够大，值得 AAA mobile 团队投入单独后端

结论：**学 AZDO，玩 Mantle，用 DX 发货**；独立游戏用 bgfx 等抽象层；如果平台够大（iOS/Xbox）接受厂商专属 API。

## 关键要点

- API 选型三问：它能工作吗？它在我的目标市场有用吗？改造成本多高？
- AZDO 的本质：把 CPU 设置资源的工作转移到 GPU 端的间接表，绕过驱动多线程瓶颈
- DX11 多线程慢的根本原因：API 合约要求驱动承诺某些不必要的语义，导致命令录制无法快速并行
- Mantle 的悲剧：太小的市场（Win + AMD only），DX12 降临后价值归零
- GCN 架构公开文档（shader 反汇编可见）对图形研究社区的价值
- 平台市场规模决定专属 API 是否值得：Linux-only API 不够大，iOS / Xbox 够大

## 链接到的概念

- [[rendering/graphics-api-history]]
- [[rendering/mantle-api]]
- [[rendering/dx11-driver-overhead]]
- [[rendering/metal-api-overview]]
- [[rendering/draw-call]]
- [[rendering/bindless-rendering]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/06/rate-my-api.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-06-03_rate-my-api.md`
