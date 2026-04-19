---
tags: [source, shader, urp, hlsl, vertex-shader, tessellation, 教程]
date: 2026-04-19
sources: 1
---

# Vertex Shaders & Tessellation | Unity Shader Code Basics 05（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Shader Code Basics* 第 5 篇，在 URP + HLSL 环境里讲 **vertex displacement**（用 sin 波动海平面）和 **tessellation**（hull / domain shader 动态细分网格）。是本系列（以及 Ilett 的 Shader Graph 系列未覆盖——SG 的 tessellation 只在 HDRP）里第一次正式写 hull + domain 管线。

## 摘要

Vertex shader 不只是做 object → clip 的坐标变换，任何中间空间都能插入位移计算。做 wave 效果在 *world space* 做最合理——相邻同材质 mesh 可以 tile、共享 `sin(x+z)` 输入不产生 seams。公式：`waveHeight = sin(posWS.x + posWS.z + _Time.y * _WaveSpeed) * _WaveHeight`，叠到 posWS.y 再 `TransformWorldToHClip`。这样做 low-poly plane 会出现"锯齿状浪头"——每个三角形的三个顶点决定了 wave 的采样分辨率。

解法有两条：（a）用高多边形 mesh（多占内存、可能 LOD 系统切换）或（b）**tessellation**——让 GPU 在顶点 shader 之后、光栅化之前动态插入新顶点。tessellation 管线有三个阶段：**hull shader**（你写，接 patch 决定每边 / 中心细分数）→ **tessellation primitive generator**（固定功能，按 factor 在归一化参考域上生成 barycentric 坐标）→ **domain shader**（你写，拿 barycentric + 原 patch 控制点插值新顶点数据、可再做 displacement）。

文章循序渐进：先写最基础的 `Waves` shader（world-space sin displacement）；再复制成 `TessellatedWaves` 加入完整 tess 管线——`appdata` → `vert`（输出 `tessControlPoint`，含 `positionWS : INTERNALTESSPOS` 和 uv）→ `hull` 函数（5 个 attribute：`domain("tri")` / `outputcontrolpoints(3)` / `outputtopology("triangle_cw")` / `partitioning("integer")` / `patchconstantfunc("patchConstantFunc")`）→ `patchConstantFunc`（per-patch 跑一次，填 `tessFactors { edge[3]:SV_TessFactor; inside:SV_InsideTessFactor; }`）→ `domain("tri")` 函数（per 新顶点跑，用 `SV_DomainLocation` 重心坐标对 3 个控制点做加权插值，**再**做 sin wave displacement，最后输出 `t2f`）→ `frag(t2f)`。注册方式：`#pragma hull hull` + `#pragma domain domain`。距离淡出机制：patch constant 函数里用每条边中点到相机的距离 `saturate(1 - (dist - start) / (end - start))` 作为系数乘 `_TessellationAmount`——近处高细分、远处回到 1。

## 关键要点

- **vertex displacement 空间选择**：world space 可 tile、object space 不可，但 object space 做局部变形（角色弯腰）更自然。
- **Low-poly + wave = 锯齿**：信号的最高频（sin 波的波长）低于 mesh 的 Nyquist（顶点间距）就会失真；tessellation 是上采样。
- **tessellation 三阶段**：hull（你写 factor）/ tessellator（固定生成 barycentric）/ domain（你写真实数据）。
- **hull shader 5 attribute**：`domain("tri"|"quad"|"isoline")` / `outputcontrolpoints(N)` / `outputtopology("triangle_cw"|"triangle_ccw"|"line")` / `partitioning("integer"|"fractional_even"|"fractional_odd"|"pow2")` / `patchconstantfunc(name)`。
- **patch constant function**：per-patch 一次，填 `SV_TessFactor`（三角形三条边各一个）+ `SV_InsideTessFactor`（中间一个）。
- **domain shader**：用 `SV_DomainLocation`（三个 barycentric 权重）对控制点做加权求和。**这里**做 displacement 而不是 vert 里——vert 阶段数据量少（patch 级）。
- **partitioning 模式**：`integer` 严格整数（均匀间距）、`fractional_even/odd` 允许非均匀但支持 smooth 过渡、`pow2` 据作者测试在他硬件上等于 `integer`。
- **LOD 不如 tessellation**：LOD 要两份 mesh 占内存；tessellation 只需要低模 + GPU 细分；但硬件上限 64、代价随数量线性上涨。
- **tess factor 为 0 会整个 patch 消失**——距离淡出公式末尾的 `max(·, 1)` 是防止网格空洞。
- **tessellation 在 URP 支持**：只是 Shader Graph 不支持——必须手写 HLSL。

## 链接到的概念

- [[hull-domain-tessellation-urp]]
- [[tessellation-fur-rendering]]
- [[shaderlab-hlsl-basics]]
- [[coordinate-spaces]]
- [[vertex-shader]]

## 原文

- 链接：<https://danielilett.com/2026-01-03-tut10-05-vertex-waves/>
- 本地：`raw/articles/danielilett.com/2026-01-03_vertex-shaders-tessellation-unity-shader-code-basics-05.md`
