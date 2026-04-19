---
tags: [渲染, unreal, 性能优化, 移动端, 动态分辨率]
date: 2026-04-19
sources: 1
---

# UE4.18 之前的反应式动态分辨率

UE4.19 之后官方加入了带时域上采的 [dynamic resolution](https://docs.unrealengine.com/en-US/Engine/Rendering/DynamicResolution/index.html)，但 UE4.18 及更早是**完全没有**这个概念的。[[adrian-courreges|Adrian Courrèges]] 在 [[sources/adrian-ue4-optimized-post-effects|UE4 优化补丁集]]里给出了一个可移植到 4.18/4.19/4.20/4.21/4.22 的**反应式**（reactive）动态分辨率 hack，在 Switch 上被《Dragon Quest XI S》出货用过。

## 机制

本质上不动 `r.ScreenPercentage`，而是**在内部乘一个 factor**——所有 G-Buffer / 后处理 RT 按这个系数分配尺寸，backbuffer 尺寸不变。配套必须设 `r.SceneRenderTargetResizeMethod 2`，让 RT 始终按最大尺寸分配、只改 viewport，避免切换时反复分配造成 hitch。

判定依据是**上一帧的 GPU 耗时**（`GGPUFrameTime`，由 RHI 的两个 timestamp 填充）：

- 超过高阈值 `MaxFrameTimeMs`（60 FPS 目标下建议设 14~15 而不是 16，留裕度）→ 下一帧降分辨率。
- 低于低阈值 `MinFrameTimeMs` → 下一帧升分辨率。

升 / 降 factor 都取自预设的两档（`MinScreenPercentage` / `MaxScreenPercentage`）之间，最基础的补丁直接在两档之间跳。

## 反应式的固有缺陷

这套机制是**反应式**的——只能在 GPU 已经吃满之后才察觉，无法预判。所以：

- 阈值要保守——降要"狠"（一旦危险立刻大幅降）、升要"稳"（缓慢试探）。即便如此，遇到突发负载（炸开的粒子、切镜头）还是会掉帧。
- **和时域特性不兼容**——TAA / motion blur / SSR 在分辨率切换那一帧会有明显 ghost 或 flash。项目认真想用 UE4.19+ 的"动态分辨率 + 时域上采"是更正确的选择。

但对"能跑"高于"好看"的移植项目（典型是 PS4 → Switch 下移），这套基础补丁够用——文档里提到《DQ XI S》就是用它 + [[sources/adrian-ue4-optimized-post-effects|half-res SSAO]] + [[gather-bokeh-dof|GatherDOF]] 这"三件套"把 PS4 版硬塞进 Switch。

## 与通用"变分辨率"思路的关系

这是 [[dynamic-resolution-scaling]] 在 UE4 生态里的一次具体实例化——[[gameknife]] 2013 年给 gkEngine 的静态 0.75× + 锐化路径是"离线选好一个缩放、整帧下来"，而 UE4 这套是"按帧反馈调节"。锐化（CAS / NIS 思路）在 UE4 这条路径里由 TAA 上采兜底，不需要单独补。

## 相关

- [[dynamic-resolution-scaling]] — 通用思路、静态版本
- [[sources/adrian-ue4-optimized-post-effects]] — Courrèges 的补丁集原文
- [[gather-bokeh-dof]] — 同补丁集的另一个构件
- [[unreal-frame-breakdown]] — UE4 主管线参考
- [[temporal-antialiasing]] — 和时域特性的不兼容点
- [[adrian-courreges]]

## Sources

- [[sources/adrian-ue4-optimized-post-effects]]
