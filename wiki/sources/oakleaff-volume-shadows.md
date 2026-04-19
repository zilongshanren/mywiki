---
tags: [source, 渲染, 体积光, 阴影, raymarching, gamemaker]
date: 2026-04-19
sources: 1
---

# Volume Shadows（Oakleaff / GM Shaders Guest）

[[oakleaff|Oakleaff]] 2024 年 4 月 5 日在 [[xor-shader-artist|Xor]] 的 GM Shaders 上发的客座教程。完整拆解了一个**屏幕空间 raymarch 体积雾 + cascaded shadow map** 的 GameMaker 实现，demo 项目开源在 GitHub。

## 摘要

整个系统建立在**五个积木**之上：深度 buffer、3 级 cascaded shadow map、Perlin noise（雾密度）+ blue noise（抖动）、世界空间视锥远面四角（作 uniform 传给 VS）、全屏 fog pass。Vertex shader 用 4 个视锥角分别对应 quad 的 4 个顶点，让 view ray 通过插值 per-fragment 生成——但要记得 fragment 里重新归一化（线性插值破坏单位长度）。Fragment shader 对每像素做 `cSampleCount` 步 raymarch，每步三平面 Perlin 采 3 次得伪 3D 雾密度，同时在对应 cascade 上做 hard shadow test 累积。朴素实现有严重**带状 artifacts**——24 采样下远处 shadow 和近处 lit 交替成条纹；用 blue noise 抖动射线起点后，带状变成高频噪声，被后续 blur 吃掉。性能上的经济模式是**1/4 分辨率渲染 + Gaussian blur + additive blend**——把抖动和低采样的缺点全部掩盖。文末坦承：没有光散射积分（不是物理正确的 in-scattering）、shadow bias 粗糙、blue noise 可以 temporal 化配合 [[temporal-antialiasing|TAA]] 进一步降噪。

## 关键要点

- **五件套积木**：depth / cascade shadow / Perlin+blue noise / 视锥角 / fog pass——拆分清晰。
- **3 级 Cascaded Shadow Map**：把视锥按 z 切 3 段，每段 2048px shadow map；draw call 翻 3 倍但不爆贴图分辨率。
- **View ray per-fragment**：VS 传 4 个远面角到 quad 的 4 个顶点，插值出 view ray。**必须在 FS 中再 normalize**。
- **三平面 Perlin = 伪 3D 雾**：xy/xz/yz 三次 2D 采样做 3D 密度——每 raymarch 步 3 次 fetch，是最贵的部分。
- **Blue Noise 抖动起点**：朴素等间距采样产生带状 artifacts；blue noise 抖动把低频带改成高频噪声，便于 blur。
- **1/4 分辨率 + blur + additive**：经济版体积光的标准配方——牺牲细节换性能，blur 掩盖采样不足。
- **Shadow 算法与几何着色器无异**：体积 shadow 不需要额外 shadow map，复用同一张。
- **局限自省**：没有 in-scattering、bias 粗糙、快速移动时 blue noise 抖动可见——诚实的教程态度。
- **和 Froxel 方案对比**：[[volumetric-fog-froxels|Rise of the Tomb Raider]] 的 compute pipeline 是工业解法；per-pixel raymarch 是业余/中小项目的甜蜜点。

## 链接到的概念

- [[volumetric-fog-raymarch-shadows]]
- [[shadow-mapping-basics]]
- [[cached-shadowmaps]]
- [[volumetric-raymarching-intro]]
- [[volumetric-fog-froxels]]
- [[poisson-disk-sampling]]
- [[separable-gaussian-blur]]
- [[classic-shader-noise]]
- [[temporal-antialiasing]]
- [[oakleaff]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/volume-shadows
- 本地：`raw/articles/mini.gmshaders.com/2024-04-05_gm-shaders-guest-volume-shadows.md`
