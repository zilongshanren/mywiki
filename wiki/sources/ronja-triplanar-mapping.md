---
tags: [source, rendering, shader, unity, uv, 纹理]
date: 2026-04-14
sources: 1
---

# Triplanar Mapping（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 2018 年 5 月发表的系列第 010 篇，紧接 [[sources/ronja-planar-mapping|planar mapping]] 之后，用手写 vertex/fragment shader 讲清楚 triplanar 的每一个中间步骤。

## 摘要

文章把 triplanar 拆成可验证的四步。第一步在 fragment 里用 `worldPos.xy`、`worldPos.zy`、`worldPos.xz` 生成三套 UV，分别采样后简单平均 `(c1+c2+c3)/3`——结果是每个面都能看到三层叠加的模糊图案。第二步把世界法线作为权重引入：用 `mul(v.normal, (float3x3)unity_WorldToObject)` 把法线从 object 空间转到 world 空间（必须走**逆转置**矩阵才能在非均匀缩放下保持正交性，文章专门画图解释为什么不能直接乘 object-to-world）。第三步把法线取 `abs` 处理正反方向共享贴图、按分量加权三个投影，再除以 `weights.x+y+z` 归一化亮度——否则整体亮度会随法线方向波动。第四步加一个 `_Sharpness` 属性，用 `weights = pow(weights, _Sharpness)` 压低小权重，让三个轴之间的过渡更硬。文末坦白说 triplanar 在恰好 45° 的面上仍然会退化、对 normal map 需要额外处理、采样数翻三倍是硬成本。

## 关键要点

- Object-space 法线 → world-space 必须用 **逆转置矩阵**：`mul(v.normal, (float3x3)unity_WorldToObject)`（向量从左乘），否则非均匀缩放下法线不再正交。
- 权重计算：`abs(N) → pow(., _Sharpness) → 归一化为和为 1`，三步缺一不可。
- `abs` 的作用是让正反朝向共享同一张贴图；缺少它的话「朝下」的面会变黑。
- `_Sharpness` 越大 → 过渡越硬；`=1` 是自然软过渡，`=4` 起接近硬选。
- 缺点：采样数 ×3、45° 斜面退化、normal map 需要额外 reorient 才能 triplanar。

## 链接到的概念

- [[triplanar-mapping]]
- [[planar-mapping]]
- [[coordinate-spaces]]
- [[normal-map-blending]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/010-triplanar-mapping/>
- 本地：`raw/articles/ronja-tutorials.com/2018-05-11_triplanar-mapping.md`
