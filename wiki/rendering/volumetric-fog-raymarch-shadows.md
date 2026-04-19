---
tags: [渲染, 体积光, 阴影, raymarching, shadow-map, gamemaker]
date: 2026-04-19
sources: 1
---

# 体积雾 + 级联阴影：屏幕空间 Raymarch 实现

一个业余规格但完整的 **volumetric shadow** 实现需要把几个已知组件拼起来：屏幕空间深度、[[cached-shadowmaps|cascaded shadow map]]、世界空间视锥远面四角、Perlin 雾密度、Blue Noise 抖动。Oakleaff 在 GM Shaders 上写的 GameMaker 版本不是 AAA 规模，但把**"低分辨率 raymarch + blur + 加色"**这条经济路线讲得很透，对理解 [[volumetric-fog-froxels|Froxel 体积雾]]之前的"per-pixel raymarch 版本"很有帮助。

## 五块积木

1. **深度 buffer**：屏幕空间全分辨率，RGB pack 的深度，用来确定每条射线的终点（击中几何前就停步，不穿透场景）。
2. **阴影贴图**（cascaded）：把相机视锥沿 z 切成 3 段，每段一张 2048px shadow map。近处细节清晰、远处代价可控。这和 [[shadow-mapping-basics]] 的算法本身无区别，只是多做几张、在采样时按 world-space 位置挑对应的那张。
3. **噪声贴图**：Perlin 定义雾的 3D 密度场，Blue Noise 抖动射线起点（关键——见下文）。
4. **视锥远面四角**（世界空间）：CPU 侧算出来当 uniform 上传，vertex shader 读对应角插值得到**每像素 view ray**。
5. **全屏 fog pass**：以上拼起来跑在一个四边形上。

## Vertex shader：让 view ray 通过插值传下来

顶点着色器只有两件事：把 4 个屏幕角分别对应到世界空间的 4 个远面角，让 view ray 通过插值**per-fragment 生成**：

```glsl
int n = 0;
n += int(in_TextureCoord.x);
n += int(in_TextureCoord.y) * 2;
vec3 frustumPoint = uFrustumPoints[n];
v_vViewRay = normalize(frustumPoint - uCamPosition);
```

Fragment shader 必须 **renormalize** 这个 v_vViewRay——线性插值不保留单位长度，不归一化 fog 积分位置会错。这是个常见的坑。

## Fragment shader：raymarch + shadow sample

对每个像素：

1. 用 depth buffer + far-plane 距离还原像素的世界位置 `rayEndPosition`。
2. 从相机到 rayEndPosition 沿射线走 `cSampleCount`（通常 24–48）步，每步：
   - **三平面 Perlin 采样**：xy、xz、yz 三次读 noise 做伪 3D 雾密度（比真 3D 纹理便宜得多，但有各向异性）。每步 3 次 tex fetch 不便宜，这是整套最贵的部分。如果不需要雾有"形状"，这步可以省。
   - **Shadow map 采样**：`shadowCoord = uShadowMatrix * vec4(worldPos, 1)`，在对应 cascade 上做 hard shadow test。命中影子就给这一步加 shadow 权重。
3. 累积 `totalValue` 和 `shadowedSamples`，最后 `finalFog = totalValue * (1 - shadowedSamples / N)`。

## 为什么需要 Blue Noise 抖动

朴素做法是把 `[0, 1]` 均匀分成 N 份，每步按 `i/N` 取位置。问题：步长大时多数射线的采样点都错过了**细长的 shadow 区域**，结果是**带状 artifacts**——"远处在阴影里，近处有阳光，然后远远地又一条阴影带"。

[[poisson-disk-sampling|Blue Noise]] 抖动射线**起点**（`n = (1/N) * blueNoise + i/N`）把这种低频条纹打散成高频噪声，**噪声更容易被 blur 过滤掉**。

## 性能模式：1/4 分辨率 + 模糊 + additive blend

直接全分辨率 raymarching 贵到不能接受。Oakleaff 的组合拳：

1. 在 1/4 分辨率（宽高各 1/2）渲 fog → fragment 只有 1/4 数量。
2. 把 fog 渲到独立 emission surface，启用 texture filter **上采样**。
3. 两 pass [[separable-gaussian-blur|可分离 Gaussian blur]]（半径 5）把噪声糊掉。
4. 最终 **additive blend** 到主画面。

半分辨率 + blur 把 blue noise 抖动、带状误差、采样不足同时掩盖——一个典型的"低质量渲染 + 后处理救命"路线。代价是快速移动相机时可以看到 noise pattern 闪烁，**把 fog strength 砍半**能让抖动低于视觉阈值。

## 局限与进阶

- 没有光散射积分（Mie/Rayleigh phase）——这是纯累积，不是物理正确的 in-scattering。
- Shadow biasing 很粗糙，远 cascade 会有自遮挡。
- Blue noise 可以做 **temporal animation** + [[temporal-antialiasing|TAA]] history rectification，进一步降噪。
- 和 [[volumetric-fog-froxels|Froxel 方案]]相比，这是 per-pixel raymarch，没有 3D 纹理缓存，不适合大场景多光源。小型 2.5D/3D 游戏或 GameMaker 这类业余引擎，它是个甜蜜点。

## 相关

- [[volumetric-raymarching-intro]] —— raymarching 和体积着色的基础
- [[volumetric-fog-froxels]] —— 同主题的工业解法，用 3D 纹理代替 per-pixel raymarch
- [[shadow-mapping-basics]] —— shadow sample 的基础
- [[cached-shadowmaps]] —— cascade 跨帧缓存
- [[poisson-disk-sampling]] —— blue noise 抖动的姊妹技术
- [[separable-gaussian-blur]] —— 用来掩盖 1/4 分辨率的噪点
- [[temporal-antialiasing]] —— 进一步降噪的温和路径
- [[classic-shader-noise]] —— 本文用 Perlin 作为密度场

## Sources

- [[sources/oakleaff-volume-shadows]]
