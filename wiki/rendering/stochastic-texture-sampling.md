---
tags: [shader, 纹理, tiling, heitz-neyret, stochastic, unity, urp]
date: 2026-04-19
sources: 1
---

# 随机采样打散纹理平铺

**Stochastic texture sampling** 指的是用随机化的 UV 偏移采样同一张纹理多次并按权重混合，以**打散可见的 tiling 重复**。当地面、墙面、地形这类需要大面积覆盖的材质被小 texture 平铺时，人眼会在远处识别出重复的图案——尤其是带有显著特征点的贴图（石头、青草、泥土斑块）。标准解法是让每个着色点以不同的随机偏移采样，最终结果不再出现重复。

## 问题根源：tiling = 可识别的周期

Texture tiling 本身是效率需求——一张 512×512 的石头贴图平铺到 100×100 米的地面上，无需更高分辨率。但平铺的周期一旦进入视觉识别范围（远处看整面墙），原本「随机的石头纹路」就退化成「规则的瓦片」。这是一个**频域**问题：贴图空间是周期信号，屏幕空间呈现出强烈的低频峰值。

## 最朴素的方案：多次偏移采样

[[daniel-ilett|Daniel Ilett]] 的 Shader Toolbox **Stochastic Lit** 用的是「对每张贴图做 3 次不同偏移的采样，按某种权重混合」的写法——教程原话说这使得 shader 比 Default Lit 更贵，每张贴图 3 次采样。权重和偏移一般由一个每像素独立的 hash 决定：

```hlsl
// 伪码：概念示意
float2 offset1 = hash2(floor(uv * tileSize));
float2 offset2 = hash2(floor(uv * tileSize + float2(1, 0)));
float2 offset3 = hash2(floor(uv * tileSize + float2(0, 1)));

half4 s1 = tex2D(_Main, uv + offset1);
half4 s2 = tex2D(_Main, uv + offset2);
half4 s3 = tex2D(_Main, uv + offset3);

// 按 hash 权重混合
half4 result = s1 * w1 + s2 * w2 + s3 * w3;
```

关键是**三个偏移是相邻三点共享的**——每个 tile 生成一个偏移，三角形三顶点对应的相邻偏移被混合。这避免了每像素独立随机导致的噪点，也保证相邻像素混合结果连续。

## 为什么混合不会让图像变浑浊

朴素实现的直接问题是**三张带偏移的纹理相加会让对比度下降**——均值相加、方差稀释。因此「stochastic sampling」这个名字下有个分支专门解决这件事：

- **Heitz & Neyret, 2018, "High-Performance By-Example Noise using a Histogram-Preserving Blending Operator"**：提出保持直方图的混合操作——不是简单相加，而是先把每张样本做一次基于目标直方图的变换（通过预计算的查找表），相加后结果的直方图仍接近原图。这是当前「histogram-preserving stochastic tiling」的行业基线。
- **Heitz 的后续工作**关注把这套方法简化到运行时可接受的成本。

Ilett 的 Stochastic Lit 教程只说「3 次采样」没展开具体混合公式，大概率是简化版——可能只做了加权平均、没做 histogram preservation。对 albedo 纹理这种视觉容忍度较高的材质够用；对 detail / normal 可能会有肉眼可见的软化。

## 性价比权衡

每张贴图 3 次采样意味着 Default Lit 里的 5 张贴图（Albedo / Normal / MRO / Height / Emission）变成 15 次采样——bandwidth-bound 硬件上约 3× 成本。适用场景：

- **远处大面积平铺材质**——玩家不会停留在一个像素审视，3× 成本换掉可见的 tiling 非常划算。
- **独立 Hero 物体**——不需要，本来就不平铺。
- **移动端**——谨慎，bandwidth 和功耗都敏感。

## 与其他打散 tiling 的方法对比

- **UV offset shader**：同一张贴图用两种不同 UV scale 混合——简单但只能打散低频周期，高频特征依然看得出来。
- **Detail textures**：叠一张小 scale 的 detail 贴图——不解决主贴图的 tiling，只是在视觉上盖一层噪点。
- **[[triplanar-mapping|Triplanar mapping]]**：三个轴方向的投影融合——解决的是 UV unwrap 问题，但三个投影各自仍会有 tiling。Triplanar + Stochastic 可以组合。
- **[[terrain-splatmap-shader-graph|Splatmap blend]]**：多种不同材质按蒙版混合——视觉上多样但每种材质自己还是平铺的。
- **Large non-repeating texture + megatexture / VT**：终极方案，但美术和存储成本很高。

Stochastic sampling 的位置是：**中等成本、无需额外美术资产、视觉效果显著**。

## 相关

- [[sampler-filter-wrap-modes]]
- [[triplanar-mapping]] —— 打散 UV unwrap 问题的正交方案，可与 stochastic 组合
- [[texture-swizzle-nested-tiling]] —— 另一种纹理复用/打散策略
- [[two-texture-sampling-tricks]] —— 双纹理采样的一般性技巧
- [[terrain-splatmap-shader-graph]]
- [[daniel-ilett]]

## Sources

- [[sources/danielilett-toolbox-urp-stochastic-lit]]
