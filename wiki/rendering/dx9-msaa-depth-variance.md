---
tags: [渲染, DirectX9, MSAA, 深度缓冲, 方差, 阴影]
date: 2026-04-27
sources: 1
---

# DX9 MSAA 深度 Resolve 的方差补偿

DirectX 9 不允许直接读取 MSAA 深度缓冲的独立采样点，只能将多样本 resolve（平均）到 R32F 渲染目标。这导致物体边界处的深度值变成多个 MSAA 样本的插值，用于 SSAO、软粒子、深度雾等效果时产生明显的"幽灵边缘"（ghost edges）。

[[angelo-pesce]] 将方差阴影贴图（VSM）的统计思路迁移到这个问题：同时记录深度的均值和方差，用方差偏移来近似最小深度（前景优先），显著改善边缘质量。

## 问题根源

在 DX9 下的标准做法：

1. 写深度到 MSAA R32F 颜色目标（无法直接采样硬件深度）
2. Resolve 时 GPU 对 N 个 MSAA 样本取均值
3. 深度相关效果采样这个均值深度

物体边界处 N 个样本来自前景和背景，均值落在两者之间——既非前景深度也非背景深度——导致深度雾、SSAO 等产生半透明错误轮廓。

## 方差补偿方案

借鉴 VSM（Donnelly & Lauritzen 2006）的核心思想：用两个统计量描述一批深度采样，而非只用均值。

**存储格式**：将深度写入 16bit ARGB（或 RGBA16F）目标，R 通道存 depth，G 通道存 depth²（用于计算方差）。Resolve 时两个通道独立平均，得到 E[d] 和 E[d²]，方差 Var[d] = E[d²] - E[d]²。

**使用方式**：
- **前景优先**：用 `E[d] - k * sqrt(Var[d])` 近似最小深度（前景样本），k 为可调参数
- **双端模式**：同时用 +k 和 -k 计算两个深度端点，再对深度效果（如雾）分别求值后平均，比单端更物理正确

**效果**：边界处的幽灵轮廓大幅减少，在 JPEG 压缩后仍可见改善，更精细区域效果尤为显著。

## 元技术的价值

这篇文章真正要传达的不是具体实现（Pesce 自称是几小时内写的原型），而是 VSM 论文所代表的**统计元技术**：

- 只要能存储和传递均值 + 方差，就可以还原出原始样本分布的部分信息
- 这一思路可应用于任何"只能访问聚合结果（均值）但实际需要某种极值"的场景
- 其他应用：法线 mipmap 的方差驱动 gloss（见 [[normalmap-mipmap-aliasing]]），moment shadow mapping（见 [[moment-shadow-mapping]]）

## DX9 的替代方案

Aras Pranckevičius（aras-p.info）记录了 INTZ 格式：利用硬件扩展直接将 DX9 深度缓冲作为纹理采样，无需额外 R32F pass。但 MSAA 深度的逐样本访问在 DX9 下仍无官方支持。

## 相关

- [[moment-shadow-mapping]]
- [[msaa-ssaa]]
- [[z-buffer]]
- [[depth-aware-gaussian-blur]]
- [[normalmap-mipmap-aliasing]] — 同为方差统计元技术的另一应用
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-dx9-depth-resolve]]
