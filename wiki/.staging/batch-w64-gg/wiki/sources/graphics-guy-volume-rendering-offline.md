---
tags: [source, 渲染, 体积渲染, pbrt]
date: 2026-04-19
sources: 1
---

# Volume Rendering in Offline Renderer（A Graphics Guy's Note）

[[graphics-guy-notes]] 2016 年 11 月的文章，补齐 PBRT 第二版体积渲染章节里跳过的数学推导。

## 摘要

文章先把离线渲染里光与体积的四种相互作用（absorption / emission / out-scattering / in-scattering）讲清楚，给出各自的微分方程。重点在 in-scattering：PBRT 把微分式 $\frac{dL_o}{dt} = -\sigma_t L_i + S$ 和积分式 $L_i = \int T_r S dt$ 同时列出，但没写如何推导。作者用方向反转 + 一阶线性 ODE 标准解法，用 $L(\infty)=0$ 定积分常数，给出从微分式到积分式的完整步骤。顺带对比实时方案（粒子系统 billboard）和离线方案的取舍——实时普遍有偏但对雾/烟够用，离线统一处理所有体积现象的代价是更重的 Monte Carlo 积分。

## 关键要点

- 微观角度看，雾、水、光柱都是同一类：粒子与光线相互作用。
- Attenuation = absorption + out-scattering，两者工程上合并为 $\sigma_t$。
- Beam transmittance $T_r = e^{-\int \sigma_t dt}$ 是离线体积渲染的核心量。
- In-scattering 方程的积分形式：沿路所有内散射源 $S(p(t))$ 各自乘以对应段 $T_r$ 后累加。
- 实时方案多为有偏 billboard；offline 一套积分打天下，代价是 MC 方差高。

## 链接到的概念

- [[volume-rendering-offline]]
- [[path-tracing-basics]]
- [[sss-practical-implementation]]
- [[spectral-rendering]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/volume_rendering_in_offline_renderer/
- 本地：`raw/articles/agraphicsguynotes.com/2016-11-10_volume-rendering-in-offline-renderer.md`
