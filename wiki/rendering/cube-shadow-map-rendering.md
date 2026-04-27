---
tags: [渲染, 阴影, cube-map, 点光源, 椭球光源, geometry-shader, esm, shadow-caching]
date: 2026-04-27
sources: 1
---

# Cube Shadow Map 渲染

**Cube shadow map** 是点光源（及类似全向发射光源）阴影的主流存储格式：将光源周围的深度信息存入一个 cubemap 的六个面，在着色时通过方向向量采样对应面完成遮挡比较。相比竞争方案（dual-paraboloid shadow map），cube map 提供更均匀的误差分布，并与 GPU 的 cubemap 采样硬件天然契合。

## 单 Draw Call 渲染六个面

DirectX 10+ 支持借助几何着色器（Geometry Shader）在一个 draw call 内完成 cube shadow map 的全部六个面。核心思路：顶点着色器处理每个顶点的位置，几何着色器对每个三角形循环六次，将变换后的图元输出到对应的 render target array 层。每次迭代包含视锥剔除和背面剔除以减少不必要的 primitive，最终流量写到 `SV_RenderTargetArrayIndex`。

然而，几何着色器的性能在不少 GPU（尤其 AMD GCN 初代）上明显低于预期，因为其动态输出特性阻碍了硬件流水线优化。Wolfgang Engel 提出的改进方案是将 viewProjection 矩阵的偏移计算前移到顶点着色器——每个顶点预计算三对变换结果（正/负 X、Y、Z 方向各一对），几何着色器只做轻量的「根据 face index 解包 + 剔除测试」，将最重的矩阵乘法从几何阶段卸载。

## 椭球光源的 Cube Map 存储

椭球光源（各方向有独立衰减系数的扩展点光源）同样可以直接复用 cube shadow map 存储，不需要特殊格式。方向衰减可以在着色 pass 中通过方向向量独立计算，shadow map 只负责遮挡判断，两者正交。这使得椭球光源可以被统一纳入点光源的阴影系统，无需额外管线分支。

## 阴影缓存（Shadow Caching）

每帧更新所有动态点光源的 cube shadow map 代价极高，缓存策略不可缺少。合理的缓存算法综合以下参数决定是否更新：

- **距相机距离**：远处阴影精度低，更新优先级低
- **屏幕覆盖面积**：屏幕像素占用小的阴影对视觉影响小
- **光照影响区域内是否有移动物体**：无动态遮挡体时可无限期复用

缓存 100 张 256×256×6 的 16-bit depth cube map 约占用 75 MB；内存不足时可按距离限制缓存容量，超出范围的 map 移出。

## Shadow Bias 与指数阴影映射（ESM）

传统的固定 bias 方案在 cube shadow map 上尤为棘手：随光源位置变化，场景与投影关系动态改变，手工选定的 bias 很快失效，既出现阴影痤疮（shadow acne），又容易 peter-panning。

Marco Salvi 提出的**指数阴影映射（ESM）**以指数函数近似二值深度比较：

```hlsl
float depth = tex2D(ShadowSampler, pos.xy).x;
shadow = saturate(2.0 - exp((pos.z - depth) * k));
```

指数近似天然平滑，不依赖场景相关的 bias 参数，且可以与硬件线性滤波叠加使用，以低 overhead 获得软化边缘。代价是在极端深度差异下可能出现「光渗透」（light bleeding），需要通过调节 k 参数或限制 ESM 的深度范围来控制。ESM 是 VSM（Variance Shadow Maps）的指数版本，参见 [[moment-shadow-mapping]] 的概率滤波家族。

## 半影软化

概率滤波方法（VSM / ESM / MSM）可以充分利用硬件双线性滤波，软化质量高，开销相对可控。对于屏幕空间软化，Engel 实现了一个可同时处理大量（16–32 个）软点光源阴影的屏幕空间 PCF 变体，利用 cube map 投影构建屏幕空间核，在不更新 shadow map 的前提下实现视觉上可接受的半影。

## 相关

- [[shadow-mapping-basics]] — 阴影贴图基础原理与 bias 详述
- [[cached-shadowmaps]] — 帧间相干性缓存策略
- [[moment-shadow-mapping]] — 概率滤波阴影（VSM / MSM / ESM 家族）
- [[cascaded-shadow-maps]] — 方向光阴影，与点光源阴影互补
- [[rendering/gpgpu-compute-simt-model]] — GS 性能问题与 compute 替代路径的背景

## Sources

- [[sources/humus-ellipsoid-light-shadow]]
