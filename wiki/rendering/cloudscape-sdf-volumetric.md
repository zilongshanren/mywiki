---
tags: [渲染, 体积云, SDF, raymarching, dcs]
date: 2026-04-19
sources: 1
---

# SDF 驱动的 Cloudscape

飞行模拟器里的体积云不只要漂亮——飞机在云中狗斗时要求**空间一致性**（从不同高度/角度看同一朵云要长得一样）。[[sources/thomas-poulet-dcs-frame|DCS 2.7]] 给出的解法是把云的「宏观分布」和「微观细节」**分层用 SDF 驱动**。

## 两张 SDF 合成 cloudscape

- **水平 SDF**：一张大型 signed distance field，勾出云的平面分布，带有一种 barrel 畸变（[[thomas-poulet]] 猜是为了在地平线上贴合地球曲率的视觉）。
- **垂直 SDF**：一张描述云在不同海拔上分布的 SDF。

两张合起来定义了天空中「哪里有云」—— 也就是一个 3D 云空间 SDF。两张图更像是**低频查询表**而不是每帧重算，[[thomas-poulet]] 在采样里没抓到它们被实时生成。

## 加细节的 raymarch

有了 cloudscape SDF，raymarcher 就可以沿视线 step：
1. 用 cloudscape SDF 做**粗形状**驱动，跳过空气区域。
2. 在云体内采样另一组 **cloud density 纹理**做形状调制。
3. 对高频细节用一张 **128³ 的 Perlin-Worley 3D 噪声**加纹理扰动。
4. 结果和前面 light-resolve 阶段算出的屏幕颜色做 alpha blend。

整体结构和 Guerrilla Games 在 *Horizon Zero Dawn* / Nubis 里公开的方法非常相像（三层密度 + Perlin-Worley）——所不同的是 DCS 用了**外层 SDF 来决定云体本体在哪里**，而不是让密度场自己定义存在区域。这让艺术家可以 offline 编辑 SDF 来快速改大尺度气象。

## 关键启示

- **SDF 作为「区域管理器」**：跟 [[sdf-ray-marched-shadows|SDF 阴影]]、[[sparse-shadows-cone-tracing|sparse cone-trace]] 一样，SDF 在这里是 **空间存在性查询** 的廉价代理，让真正昂贵的 raymarch 可以大幅跳过。
- **分层合成**：宏观（SDF）+ 中观（密度纹理）+ 微观（3D 噪声）是体积云的通用公式，关键是**每一层用哪种数据结构**，和 [[volumetric-fog-froxels|froxel fog]] 的 spatial/temporal decomposition 一脉相承。

## Sources

- [[sources/thomas-poulet-dcs-frame]]
