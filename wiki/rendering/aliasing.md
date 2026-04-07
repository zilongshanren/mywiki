---
tags: [渲染, 信号处理]
date: 2026-04-05
sources: 1
---

# 走样与反走样（Aliasing & Anti-aliasing）

**走样**是采样率不足的信号处理失真——欠采样导致的不真实视觉伪影（锯齿、闪烁）。

## "像素不是小方块"

关键认知：像素**不是面积采样**，它是**0.5 偏移处的点采样**。这就是为什么纯 point sampling 必然造成锯齿和闪烁——你是在高频信号（三角形边缘）上做低频采样。

## Nyquist 采样定理

要无失真重建信号，采样率必须 ≥ 信号最高频率的 2 倍。三角形边缘在视觉上是无限高频（离散突变），理论上永不满足 Nyquist——所以只能通过**低通滤波**削减高频。

## 反走样策略

反走样 = **采样前的低通滤波**。

| 技术 | 方法 | 成本 |
|---|---|---|
| **SSAA** | 多次完整 shader 执行 + 平均 | 高（2-16× fragment cost） |
| **MSAA** | 多次 coverage 测试 + 一次 shader + 混合 | 中（2-4× coverage） |
| **FXAA** | 后处理模糊边缘 | 极低 |
| **TAA** | 时间上累积多帧 jitter 采样 | 低（但 ghosting） |
| **DLSS** | AI 从低分辨率升采样 | 低（但需硬件支持） |

## MSAA 在 TBDR 上的特殊地位

TBDR 架构把 multisample 数据留在**片上内存**，写回时 resolve，成本几乎为零。详见 [[tbdr-vs-imr]]。

## 相关

- [[msaa-ssaa]]
- [[rasterization]]

## Sources

- [[sources/rtr-day04]]
