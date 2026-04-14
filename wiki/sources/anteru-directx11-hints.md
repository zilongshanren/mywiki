---
tags: [source, 渲染, DirectX11, 工程笔记]
date: 2026-04-14
sources: 1
---

# DirectX11 hints（Matthäus G. Chajdas / anteru.net）

[[matthaeus-chajdas]] 2010 年 3 月发表在 anteru.net 的一篇短工程笔记，记录他在 DirectX 11 刚铺开时趟过的几个坑，对象是「刚开始上手 DX11」的开发者。

## 摘要

文章按 tessellation、compute shader、HLSL 三块整理踩坑清单。tessellation 部分讲了 domain shader 必须写满 4 维 SV_Position、tessfactor 输入必须配套（边与内部细分必须相近，否则边界破洞），以及 topology 必须用 `PATCHLIST` 否则 ATI 驱动会冻死整机。compute shader 部分讲了 dispatch 后必须显式解绑 SRV 否则 debug layer 会持续报 hazard，以及 RW texture 的 `BindFlags` 必须同时打开 `SHADER_RESOURCE | UNORDERED_ACCESS`，HLSL register 槽位 `t/u/b` 要按顺序使用。HLSL 部分给了一个小招——直接写 `1.#INF` 拿无穷。文末作者抱怨当时的文档质量与驱动稳定性，并对 ATI 驱动「用户错误就死锁」表示不满。

## 关键要点

- **tessellation domain shader 必须写完整 4 维 SV_Position**，对应 `error X4577`。
- **`SV_TessFactor` 与 `SV_InsideTessFactor` 必须同时设置**，且数值不能差太远，否则边界 vertex valence 爆炸出现破洞。
- **tessellation 必须用 `D3D11_PRIMITIVE_TOPOLOGY_<N>_CONTROL_POINT_PATCHLIST`**——误用 `TRIANGLELIST` 会冻机直到 Windows 7 TDR 重置。
- **dispatch 后必须用 `CSSetShaderResources` 手动解绑 SRV**，否则后续 `OMSetRenderTargets` 会触发 `STATE_SETTING WARNING #9` / `#2097317` hazard 警告，驱动会强制将 slot 置 NULL。
- **RW Texture2D 的 BindFlags 必须 `SHADER_RESOURCE | UNORDERED_ACCESS`** 双开，并单独建 UAV。
- **HLSL register 顺序**：`tN` 给纹理 / structured buffer，`uN` 给 UAV，`bN` 给 cbuffer。
- **`float i = 1.#INF`** 是 HLSL 里取无穷的简便写法。
- **作者吐槽**：debug layer 虽好，但很多约束仍要 trial-and-error；CS 开发常常需要重启机器，tessellation 略好（驱动可重启）。

## 链接到的概念

- [[directx11-early-pitfalls]]
- [[rendering-pipeline]]
- [[gpu-hazard-tracking]]
- [[d3d12-resource-binding]]
- [[matthaeus-chajdas]]

## 原文

- 链接：https://anteru.net/blog/2010/directx11-hints
- 本地：`raw/articles/anteru.net/2010-03-01_directx11-hints.md`
