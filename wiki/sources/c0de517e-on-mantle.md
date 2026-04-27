---
tags: [source, graphics-api, mantle, amd, dx11, low-level-api, history]
date: 2026-04-27
sources: 1
---

# On Mantle（c0de517e / Angelo Pesce）

[[angelo-pesce]] 发表于 2013 年 12 月的文章，深度分析 AMD Mantle API 的意义、局限以及对行业格局的影响。

## 摘要

文章分四个议题逐一展开。首先论证为什么 Mantle 是个好主意：AMD 当时已控制 PS4/Xbox One 两台次世代主机的 GPU，如果 Mantle 与 PS4 的 libGNM API 高度对齐，开发者就能把已有的主机渲染器投资直接复用到 PC，大幅降低采用门槛——这是绕过"鸡和蛋"问题的正确策略。其次解剖 DX11 的核心缺陷：延迟状态提交（driver 必须等到 draw call 才能将 API 状态转译成硬件位）、状态生命周期错乱（需要 buffer 复制 + refcount）、deferred context 的对象可见性迫使 driver 留"空洞"等待晚到的 immediate context 调用——这些决定了 DX11 的驱动是单线程的事实结构。第三部分质疑"百万 drawcall"营销点：PC 游戏引擎多年来在数千 draw 的约束下优化了资产管线，Mantle 只能提速现有渲染，而不能让引擎突然转向"用十万 draw 思考世界"的模式，因为资产不会为单一平台重做。最后预测 Mantle 的真实价值：对 NVIDIA 和 Microsoft 的"鲇鱼效应"——促成 DX12/Vulkan，比它自身的市场占有更重要。

## 关键要点

- DX11 驱动开销的根因：状态机模型 + 跨线程对象可见性，而非"API 设计差"本身
- 主机血统是 Mantle 采用率的关键：PS4 GCN + XB1 DX11ish + PC Mantle = 一套可组合的投资
- "百万 drawcall"被 Pesce 判定为主要是营销，资产管线不会为单平台重新制作
- 真正的潜力：compute 调度暴露（DX11 未充分暴露）、显存流式控制、GPU scheduling hint
- Mantle 对 NVIDIA/Microsoft 的倒逼效应才是最大遗产——Pesce 预言它将"催生更好的 DX 和驱动"（实际上是 D3D12 + Vulkan）
- 对 Steam Machine/Linux 持悲观态度：即便 Mantle 支持 Linux，仍要维护 OpenGL for NVIDIA，不降低成本

## 链接到的概念

- [[graphics-api-history]]
- [[low-level-gpu-api]]
- [[dx11-driver-overhead]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2013/12/on-mantle.html
- 本地：`raw/articles/c0de517e.blogspot.com/2013-12-01_on-mantle.md`
