---
tags: [source, 渲染, 全局光照, GI, raymarching, radiance-cascades, gamemaker]
date: 2026-04-19
sources: 1
---

# Radiance Cascades Part 1（Yaazarai / GM Shaders Guest）

[[alex-yaazarai|Alex (Yaazarai)]] 2024 年 4 月 13 日在 [[xor-shader-artist|Xor]] 的 GM Shaders 发表的客座教程——**把 [[alexander-sannikov|Alexander Sannikov]] 的 Radiance Cascades 算法**翻译成可跑的 2D GameMaker 实现的第一部分，以概念和可视化为主。

## 摘要

[[radiance-cascades|Radiance Cascades]] 的核心是 **[[penumbra-hypothesis|半影假设]]**：阴影半影近光源处需要高 linear 分辨率（探针密集），远光源处需要高 angular 分辨率（射线密集）——两者反比。算法把这个反比直接编码为**级联纹理结构**：cascade 0 最多探针（16×16）最少射线（64）；cascade 3 最少探针（2×2）最多射线（4096）。**4× scaling** 让所有级联纹理尺寸相等，内存布局整齐。级联数上限由 `diagonal / interval0` 的 `log4` 决定，超过就有射线跑出屏幕、无贡献。射线从探针中心按均匀角度发射，每个 texel 存**一条特定方向射线**的 raymarch 结果（`alpha=0` 表示命中——有 radiance，`alpha=1` 表示未命中——可以从上级借光）。合并从最高级往 cascade 0 反向做：对每条射线找 cascade N+1 的 4 个最近邻探针、每个探针的 4 条同向射线，先平均 4 条射线再按当前探针相对位置做 **bilinear 插值**——这步是"用有限方向模拟无限方向"的数学出处。合并完的 cascade 0 通过每探针求平均降到探针分辨率，硬件双线性上采样得到 per-pixel GI。文末坦承算法仍在 Graphics Programming Discord 活跃演进，有 light leak 和非线性 attenuation 的已知问题。

## 关键要点

- **半影假设反比**：linear ↔ angular 分辨率反比；近光源要多探针少方向，远处反之。
- **级联 = 按距离段分工**：每级 cascade 负责一个特定**射线区间**（geometric sequence），从 cascade 0 的 `[0, interval0]` 到 cascade N 的 `[offset_N, offset_N + interval0 * 4^N]`。
- **恒定总射线数**：所有 cascade 纹理相同大小，`probe_count × ray_count = 常数`。这是 4× scaling 的直接结果。
- **Ray visibility term**：raymarch 结果的 alpha 0/1 决定是否合并——命中的射线本身已有 radiance，不再需要从上级借。
- **Bilinear merge = 连续方向积分**：有限射线方向通过空间插值变成角度域的积分，这是 "noiseless GI" 的关键。
- **Cascade 0 是最终 radiance field**：其它级联只是"供应链"。
- **Skybox 积分**合并到最高 angular 级联——天空盒 linear 分辨率近乎 0、angular 分辨率高（Part 2 会深入）。
- **仍在活跃研究**：light leak、非线性 attenuation、specular 支持都是 open problems。
- **评论区好问题**：view-dependent specular GI 是否可行？干涉图案为什么不反映波长？（答：这是几何光学算法，不是波动光学。）

## 链接到的概念

- [[radiance-cascades]]
- [[penumbra-hypothesis]]
- [[alexander-sannikov]]
- [[alex-yaazarai]]
- [[instant-radiosity-vpl]]
- [[jump-flooding-algorithm]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/radiance-cascades
- 本地：`raw/articles/mini.gmshaders.com/2024-04-13_gm-shaders-guest-radiance-cascades.md`
