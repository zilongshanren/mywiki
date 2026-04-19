---
tags: [渲染, 体积雾, raymarching, urp, unity, 噪声]
date: 2026-04-19
sources: 1
---

# URP 体积雾 Raymarch 实现

基于 [[urp-scriptable-render-pass|URP 自定义 Pass]]、每个雾体是一个 world-space 球形 volume、对每个屏幕像素沿 view ray 对球体内部做离散累积——这是 Steven Sell 在 `UnityURPVolumetricFog` 仓库里给出的教科书式实现。Oakleaff 的 [[volumetric-fog-raymarch-shadows]] 是同一条路线的 GameMaker 版本；Sell 这一版把 **1/4 分辨率 render 目标、ray-sphere 双 cast、3D 多层噪声、adaptive step、shadow 累积、多种 fade** 整合进了一张 URP 渲染管线。

## 工作流：register + per-volume render + composite

- `FogVolume` 组件挂在 GameObject 上，`Start` 时向静态列表注册、`OnDestroy` 时注销。`Apply(propertyBlock)` 把自己的参数塞进 MPB。
- `VolumetricFogPass.Execute` foreach 所有活着的 volume，每次 `volume.Apply(MPB)` → 画一次全屏 quad 到 **quarter-size offscreen buffer**。
- 全部画完再把这张 buffer **additive blend** 回主相机。

1/4 分辨率 buffer 的动机和 [[volumetric-cloud-quarter-res-upsample]] 同源——fog 本身就是低频、柔软的效果，分辨率损失几乎不可感；fragment 数量砍到 1/16。

## Sphere volume 的双 raycast

fragment shader 先对球体做两次 `RaySphereIntersection`：

- 第一次从相机位置沿 view ray 正向，拿到"进入点"。如果命中距离 > 场景深度（这一像素前面有遮挡物），早退出返回透明。
- 第二次从"远端开外"反向沿 -ray，拿到"离开点"。进入点 → 离开点就是 raymarch 的起止区间。

相机在球内的情况（`distance(camera, center) < radius`）单独处理：进入点就是相机、只做一次反向 cast 拿离开点。这套有三种可能的走向（前方命中 / 内部 / 外部 miss），用一个 `RaySphereHit` struct 打包返回，`Thickness` 字段归一化到 `[0, 1]` 表示"在这条射线上 volume 还剩多厚"，可以直接用来做 fade。

## Raymarch 循环的六步

对 50 步的循环，每步做：

1. **前进**：`distanceMarched += currStepSize`，当前位置 = 进入点 + rayDir * distanceMarched。
2. **Fade 计算**：三种 fade 相乘——edge（距离球心超过 `radius - _FogFadeEdge` 就开始淡）、height（`y` 超过 `_FogMaxY - _FogFadeY` 就开始淡）、proximity（离相机太近就淡，避免糊住前景）。
3. **双重噪声采样**：一张 3D 纹理 `CloudVolume64` 在四个通道里打包了不同频率的噪声（`.r` Simplex 大形状、`.gba` 不同尺度的 Worley 细节）。采样两次：大尺度 + 小尺度，按权重混合——得到"billowing 主云团 + 飘动细雾"。
4. **Adaptive step back**：第一次遇到 `fog > 0.1` 时，把步长砍到 0.2×、回退一点、标记 `takingSmallSteps=1`——让相机附近的雾有足够采样密度，远处的稀疏采样不被等权对待。和 Horizon Zero Dawn 的 adaptive step 思想一致，但和云不同的是**不会再切回大步**：fog 关心的就是近端浓度。
5. **阴影采样**：`MainLightShadow(TransformWorldToShadowCoord(pos), ...)` 拿 directional shadow，累积到 `shadowAccumulation`。
6. **累加**：`fog *= fades`，`accumulation += fog * currStepSize`。

起始位置加一个 **hash-based random 偏移**（`Hash13(pos * 1337 * sin(_Time.y))`）打散固定步长带来的 banding（和 [[volumetric-fog-raymarch-shadows|Oakleaff 用 Blue Noise]] 同理——把低频条纹换成高频噪点，让后续的 blur / temporal 更容易收拾）。

## Stylized accumulation 而不是物理正确

物理上"累积粒子密度 → 最终 alpha"是 [[volumetric-fog-froxels|GPU Pro 6 那套]]的标准做法。Sell 刻意偏离：`totalAccumulation = saturate(accumulation / distanceMarched) * density`——不是粒子数而是**"沿射线平均遇到多少雾 / 最大可能遇到的雾"**。

物理做法的问题：相机从高处俯视时，物理 accumulator 看不到"脚下一团雾"（射线穿过的雾短），玩家期望却是"低洼处应该有雾团"。提高粒子密度来补救会在远处产生"密度热点"。stylized 公式强行把分布 normalize 到 `[0, 1]`，保证视觉均匀。这是典型的"正确但不好看 → 不正确但好看"的艺术向取舍。

## Lighting 的尘肺方案

- `dotRaySun` 决定"射线是不是冲着太阳"，用来把 `lightColor` 和 `fogColor` 在"正面色"和"侧逆光色"之间插值——对着太阳方向的雾更暖更亮。
- `totalShadow` 由 `shadowAccumulation / distanceMarched` 得到；`_ShadowReverseStrength` 一般压得比 `_ShadowStrength` 小，避免低太阳角时阴影被雾"拉成很长"。
- 最终颜色 `= fogColor.rgb * max(totalLighting, ambientLighting) * totalShadow`，alpha 由 `totalAccumulation * fogAlpha` 给出。

## 和 Froxel / 低分辨率 raymarch 的家族

三条路线的定位：

- **per-fragment raymarch**（本文、Oakleaff）：每像素独立 raymarch，适合单个 volume 或业余引擎，实现简单、扩展性差。
- **Quarter-res + temporal**（Sell 体积云）：raymarch 还是 per-fragment，但通过分辨率 + jitter + history 把成本压到 1/16。
- **[[volumetric-fog-froxels|Froxel]]**：全场景 compute，3D 纹理缓存 + 多光源 in-scattering。AAA 首选。

本文是"middle ground"：结构上 per-volume、全分辨率可配置，但用 1/4 buffer 当粗糙的 temporal 近似。

## 作者自留的两个扩展坑

- **任意形状 volume**：不再用 sphere SDF，而是在 fog pass 前先渲 mesh 的 front-face/back-face depth 到 `.r/.g` 通道，fragment 直接读 depth 代替 `RaySphereHit`。Sell 的 depth-based fog 已经做了，但 volumetric 版本还没合并。
- **Light-source bloom in fog**：对点光源的贡献在 raymarch 里逐步采样会产生"光穿过雾就等亮度"的错觉，Sell 的方案是另一个 `LightSourceTexturePass` 把光源 mesh 渲到独立 buffer，然后类似 bloom 一样以当前 fog buffer 为 mask 糊上去。

## 相关

- [[urp-scriptable-render-pass]]
- [[volumetric-fog-raymarch-shadows]] — 同主题 GameMaker 版本
- [[volumetric-fog-froxels]] — AAA 的 compute 路线
- [[volumetric-cloud-quarter-res-upsample]] — Sell 在云上的 temporal upsample
- [[volumetric-raymarching-intro]]
- [[raymarching-intro]]
- [[steven-sell]]

## Sources

- [[sources/vertexfragment-urp-volumetric-fog]]
