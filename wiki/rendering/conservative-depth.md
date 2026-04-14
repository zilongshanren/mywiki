---
tags: [渲染, 深度测试, 着色器]
date: 2026-04-14
sources: 1
---

# Conservative Depth（保守深度输出）

pixel shader 只要写了 `SV_Depth`（HLSL）或 `gl_FragDepth`（GLSL），GPU 就无法在 shading 前判断 fragment 的最终深度——**[[early-z-late-z|Early-Z]] 因此被迫关掉**。代价很大：被遮挡的像素不能提前剔除，整个 shader 都会先跑完。

**Conservative Depth** 是 D3D11 / OpenGL 4.2 引入的补丁：让 shader 作者告诉 GPU「我写的深度只会比默认 rasterizer 深度**更大**（或更小）」，这样硬件仍然可以**用保守边界跑 Early-Z**——因为即便 shader 改深度，结果也不会跨越测试阈值。

## 语义与声明

- **HLSL**：`SV_DepthGreaterEqual` / `SV_DepthLessEqual` 作为 pixel shader 输出语义。前者承诺只增不减，后者反之。
- **GLSL**：`layout(depth_greater) out float gl_FragDepth;` / `layout(depth_less)` / `layout(depth_unchanged)`。
- 语义是**向驱动作出的承诺**：如果 shader 里的 `SV_DepthGreaterEqual` 实际写了比 rasterized depth 更**小**的值，行为未定义（画面闪烁 / 深度错乱）。

## 什么时候能用

- **Depth sprite**：billboard 圆球 shader 写出球心偏移过的深度——深度只会比 flat quad 的 rasterized depth 更**深**，所以用 `SV_DepthGreaterEqual` 合法。
- **高度 / parallax 映射**：同理，通常只会让深度「更深」。
- **impostors / 体渲染入口**：只要方向单调就能用。

如果 shader 写的深度方向不可预测，Conservative Depth 用不了，只能回到 Late-Z。

## 姐妹语义：`[earlydepthstencil]`

同样是 Early-Z 救援，另一条路针对**写 UAV 的 pixel shader**——默认情况下 UAV 写入会让驱动禁用 Early-Z（因为如果 fragment 最终被深度测试丢弃，UAV side effect 也应该一并撤销，而 Early-Z 没写入历史）。在 HLSL 里加 `[earlydepthstencil]` 属性到 pixel shader 上，就**强制** GPU 在 shader 执行前跑 depth / stencil test；如果 fail，UAV 写入也被跳过。**这是一个 opt-in 承诺**：作者必须确认这个 fragment 的所有 side effect 都应该受 depth / stencil test 控制。

两个机制同时存在的原因是：它们都是「默认关 Early-Z 的极端操作」的**精细化恢复通道**。Conservative Depth 恢复了**深度输出**场景的 Early-Z；`[earlydepthstencil]` 恢复了**UAV 写入**场景的 Early-Z。

## 相关

- [[early-z-late-z]]
- [[z-buffer]]
- [[fragment-shader]]

## Sources

- [[sources/interplay-depth-testing]]
