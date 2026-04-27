---
tags: [rendering, graphics-api, mantle, amd, history, low-level-api]
date: 2026-04-27
sources: 1
---

# AMD Mantle：低层图形 API 的先驱

Mantle 是 AMD 于 2013 年底发布的专有低层图形 API，首批合作伙伴为 EA/DICE（Frostbite 引擎）。它是 [[graphics-api-history|DX12 和 Vulkan 出现之前]] 第一个公开挑战 DX11 驱动模型的商业尝试。

## 背景：Mantle 为什么在 2013 年出现

2013 年 PS4 和 Xbox One 同时上市，两台主机均采用 AMD GCN GPU。这意味着 AMD 实际上垄断了次世代主机的 GPU 供货。Mantle 的战略逻辑：如果 API 与 PS4 的底层接口（libGNM）高度对齐，开发者在为主机写的渲染器上的投资可以直接在 PC 上复用——用对齐 API 打破"开发者不投入 → 用户不增长 → 开发者不投入"的恶性循环。

## DX11 的核心缺陷

[[angelo-pesce]] 在 2013 年的 "On Mantle" 一文中总结了 DX11 驱动开销的结构性根因：

1. **延迟状态提交**：硬件状态与 DX11 API 状态不是一一对应的，驱动必须等到 draw call 时才能把积累的 API 状态翻译成真正的硬件命令
2. **状态生命周期错乱**：DX11 允许更新对象（如 dynamic buffer），但驱动必须保留旧版本直到 GPU 完成使用，产生大量复制和 refcount 管理
3. **deferred context 限制**：跨线程对象可见性迫使驱动在命令缓冲中留"空洞"等待 immediate context 的顺序，实质上阻止了完全并行的命令录制

这三点解释了为什么 DX11 游戏的 CPU/driver 线程往往是单线程的性能瓶颈。

## Mantle 的真实价值

"百万 drawcall"的营销点被 Pesce 视为夸大：PC 引擎的资产管线已围绕数千 draw 优化多年，Mantle 能加速已有渲染，但无法让引擎突然改变思考世界的方式——资产不会为单一平台重做。

真正的价值有两处：
- **compute 调度暴露**：DX11 未充分暴露 GPU compute queue 的调度控制，更好的 compute/graphics 交错调度可能带来比 drawcall 数量更大的性能提升
- **倒逼效应**：NVIDIA 和 Microsoft 对 Mantle + Frostbite 的反应，直接加速了 D3D12（2015）和 Vulkan（2016）的诞生

## 历史评价

Mantle 本身的市场渗透率有限，NVIDIA 从未支持，EA/DICE 也逐渐将精力转向 Vulkan/DX12。但它作为"概念验证"完成了使命：证明低层 API 是可行且有价值的，并强迫微软和 Khronos 跟进。[[graphics-api-history]] 的现代低层 API 阶段（DX12/Vulkan/Metal）在很大程度上是 Mantle 思路的正式化。

## 相关

- [[graphics-api-history]]
- [[dx11-driver-overhead]]
- [[low-level-gpu-api]]
- [[deferred-rendering]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-on-mantle]]
