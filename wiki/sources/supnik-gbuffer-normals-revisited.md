---
tags: [source, 渲染, 延迟渲染, g-buffer, 法线编码, 精度]
date: 2026-04-19
sources: 1
---

# G-Buffer Normals, Revisited（Ben Supnik / hacksoflife）

[[ben-supnik|Supnik]] 2011-02-04 的 G-Buffer 法线精度续篇，接 [[sources/supnik-gbuffer-format]]——他在上一篇里预感「normal map goblin」会冒出来，几周后果然踩到了。

## 摘要

X-Plane 10 初版 G-Buffer（见 [[xplane-gbuffer-format]]）把眼空间法线存成 **RG16F 的 XY + shader 里 `sqrt(1-xy²)` 重建 Z**。日常几何上看着还行——Baron 58 飞机的机身、发动机舱在夕阳侧光下光照正常。但在**机翼前缘灯**这个 case 里翻车：翼面法线朝上、灯沿翼展方向，**法线与光方向几乎正交**，attenuation 曲线进入陡峭区段，2×16F 的精度偏差被放大成肉眼可见的**条带**（linear space 下尤其明显——见 [[linear-lighting-pipeline]]）。临时验证：切到完整 XYZ（多烧一个 16F 通道），条带消失；但多一个通道在 MRT 预算下负担不起。真正的修法是 SebH 之前推荐过的 [Aras 的 Compact Normal Storage 综述](https://aras-p.info/texts/CompactNormalStorage.html)——Supnik 选了其中的 **Lambert azimuthal equal-area projection**：仅用 2 通道但**等面积**投影到单位球，解码误差在球面上均匀分布（不像朴素 XY 投影那样在赤道精度稀烂）。副作用是 Lambert 天然能表达整个球面（唯一不可表达点 `(0,0,-1)` 在艺术资产上不现实），所以「负 eye-space Z」这种原先要 hand-wave 的边缘 case 也顺带消失。评论区补注：Crytek best-fit normals（BFN）用 **8 bit × 3 通道 + 查表**达到稳定 8 bit specular，比 Lambert 2 通道更省带宽但需要 3D LUT；它也完全绕开了负 Z 问题。

## 关键要点

- **问题场景**：法线 ⊥ 光方向时，2 通道 XY + 重建 Z 的精度误差落到 attenuation 陡峭段 → 条带。
- 临时验证：完整 XYZ 消除条带，但 MRT 通道预算不允许。
- **最终方案**：Lambert azimuthal equal-area projection——2 通道、等面积、解码误差球面上均匀分布。
- **副产品**：Lambert 能表达整个球面（除 `(0,0,-1)`），负 eye-space Z 不再是特例。
- **评论区对照**：CryTek Best-Fit Normals = 8 bit × 3 通道 + LUT，稳定 specular，也无负 Z 问题，但需 LUT 查找；可存于世界空间或眼空间。
- **历史上下文**：现代引擎多用 **octahedral encoding**，与 Lambert 同属「area-preserving 2 通道编码」家族但算术更省。

## 链接到的概念

- [[compact-normal-encoding]]
- [[xplane-gbuffer-format]]
- [[deferred-rendering]]
- [[tangent-space-normal-mapping]]
- [[color-banding]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/02/g-buffer-normals-revisited.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-02-04_g-buffer-normals-revisited.md`
