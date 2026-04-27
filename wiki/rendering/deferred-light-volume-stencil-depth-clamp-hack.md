---
tags: [deferred-rendering, stencil, depth-clamp, light-volume, opengl, x-plane]
date: 2026-04-19
sources: 1
---

# 延迟光源体积：stencil + 近/远剪裁面下的 depth clamp 技巧

延迟渲染里为了省 fill rate，把每个光源画成一个**包围体**——X-Plane 10 对点光源用立方体、对方向光（pyramid light）用四棱锥——然后用**双面 stencil** 把「包围体内部」的屏幕像素挑出来，只在这些像素上跑昂贵的光照 shader。这套手法本身来自公开资料：

- 背面 stencil = 深度失败时 increment（with wrap）
- 正面 stencil = 深度失败时 decrement（with wrap）
- 结果：只有落在**包围体内部几何**的像素 stencil 为奇 → 通过第二次 pass 的 stencil test。

细节上还有两条：只画背面避免相机在体积内时 front face 被剔除（与 Carmack's Reverse 的动机相同，见 [[stencil-buffer]]）；近剪裁面穿过体积前部不影响——前面本就不会有被光照到的几何。

[[ben-supnik]] 2011-12-13 处理的是一个更具体的问题：**当光源体积被远剪裁面切掉背面时会怎样**。

## 远剪裁切背面的两个灾难

想象飞机尾部一个朝后照射的金字塔方向光。远剪裁面很近时，金字塔的**底面**落在远剪裁面外，被 clip 掉——屏幕上只看到顶面和四个侧面：

1. **最终光照渲染**：背面缺失 → 体积后半段的屏幕覆盖丢失 → 光斑被垂直直线切掉（机身顶部有一条「光止于此」的硬边）。
2. **stencil 计数**：`increment/decrement` 不再配对 → 有几何横穿过远剪裁面时 stencil 值偏差 1 → 这个偏差污染**其他**覆盖同一屏幕区域的光源的 stencil 计数，它们的光也被错误剔除。

## 正解：`GL_ARB_depth_clamp`

[ARB_depth_clamp](https://www.opengl.org/registry/specs/ARB/depth_clamp.txt) 把越过近/远剪裁面的片段**夹到近/远面深度值**而不是 clip 掉。有它就万事大吉——stencil 计数一致、背面覆盖完整。

但 X-Plane 必须面对老驱动没有这个扩展的情况。

## 没有 depth clamp 的 hack：vertex-shader clip-space Z 夹紧

```glsl
gl_Position.z = clamp(gl_Position.z, gl_Position.w, -gl_Position.w);
// W 对标准 glFrustum 而言是负的
```

为什么只动 Z 不动 XY 就够？因为**裁剪空间是正交的**：XY 除以 W 后得光栅坐标（透视），Z 独立表示深度。只要等式在 frustum 变换**之后**改动 Z，屏幕位置 XY 就不受影响，体积的屏幕覆盖保持正确。

而且这一切发生在 vertex shader，fragment shader 不写 Z、不调用 `discard` → [[early-z-late-z|early-Z]] 和硬件 Z 压缩都还能用。

## 代价：Z 测试不再正确

片段的 Z 经过 clamp 后，在**插值时**会把整个三角形的 Z 往前拉（远端顶点被拉近 → 整个面相当于做了一个伪 polygon offset）。具体效果：体积与场景几何的 Z 相交判定错了，有时误把应该被光照的像素踢掉，有时反过来。于是——

> **不能**把 vertex-shader Z clamp 与 stencil depth-fail 测试合用，因为 stencil 依赖正确的 depth。

## X-Plane 10 的实际组合

Supnik 给出的三档生产路径：

| 场景 | 策略 |
|---|---|
| 「大」世界（远剪裁面很远） | 纯双面 stencil |
| 「小」世界 + 有 `GL_ARB_depth_clamp` | 双面 stencil + depth clamp |
| 「小」世界 + 无 depth clamp | 纯 vertex-shader Z clamp，跳过 stencil |

## 评论区争议

评论里有人建议「用 fragment shader 写 DEPTH 做真正的 Z clamp」（`SV_Depth`）。Supnik 的反驳是：写 DEPTH **杀掉 early-Z**，对 X-Plane 那种「小光源数万个、真正压力在 vertex bus 带宽」的场景反而更慢。真实瓶颈不一定是 shading——有时是 AGP/PCI-E bus 的顶点流量（见 [[agp-vs-vram-streaming]]），二次过一遍体积几何本身就够贵，不是加几条 shader 指令能补回来的。

这篇是 Supnik 「**光学答案要配工程 profile**」系列的好样板：教科书的 stencil 方案 → 硬件不支持时的降级 hack → 发现 hack 与 stencil 不兼容的妥协 → 最后还得追问一句「当前的 bottleneck 究竟是啥」。

## 相关
- [[stencil-buffer]]
- [[deferred-rendering]]
- [[early-z-late-z]]
- [[agp-vs-vram-streaming]] —— 当 bus 才是真瓶颈时所有 stencil trick 都可能得关掉
- [[xplane-deferred-pipeline-hacks]] —— 2012-11-16 Supnik 把本文描述的 stencil 优化**关掉**的工程决定：顶点带宽比 fill rate 更紧时 stencil 净亏损
- [[stencil-failure-modes-deferred-lighting]] — 同一系统中 bit 溢出与单 pass 视锥死角两类独立失效的分析

## Sources

- [[sources/supnik-stencil-deferred-lights-depth-clamp]]
