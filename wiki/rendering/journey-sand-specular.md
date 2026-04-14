---
tags: [渲染, shader, 高光, fresnel, blinn-phong, 风格化, unity]
date: 2026-04-14
sources: 1
---

# 《Journey》沙丘高光分解

thatgamecompany 的《Journey》里沙丘看起来会**流动**——一条大光斑随相机移动在沙面上拉开，边缘闪着柔光。Lead Engineer John Edwards 说过，团队当时**刻意把沙当作一种流体**来对待，而不是固体颗粒堆。[[alan-zucconi|Alan Zucconi]] 的 Journey Sand Shader 系列把这个效果拆成了三路高光——**rim lighting**、**ocean specular**、**glitter reflection**——这一页记录前两路。

## Rim Lighting：Fresnel 型轮廓光

Journey 的美学约束限制了每个场景使用的色彩数量。沙丘远处会失去立体感——多个 dune 只用几种颜色渲染，边界会糊成一片。解决方案是**给每条山脊加一圈柔和的 rim light**，用 Fresnel 的几何直觉：

$$I = (1 - N \cdot V)^{power} \cdot strength$$

- $N \cdot V$ 在正对相机时接近 1、在切线方向接近 0。
- $1 - N\cdot V$ 因此在轮廓处（法线几乎与视线垂直）最大。
- 取 power 是为了把"柔和过渡"收紧到"锐利窄带"——对 $[0, 1]$ 的值来说，指数越大、曲线越陡。

```hlsl
float3 RimLighting(float3 N, float3 V) {
    float rim = 1.0 - saturate(dot(N, V));
    rim = saturate(pow(rim, _TerrainRimPower) * _TerrainRimStrength);
    return rim * _TerrainRimColor;
}
```

这是「**廉价 Fresnel**」——真正的物理 Fresnel（Schlick 近似）需要 $F_0 + (1-F_0)(1-N\cdot V)^5$，但对风格化渲染只要 $(1 - N\cdot V)^p$ 这半个就够用。它的作用是**把轮廓线本身变成一条独立可控的光**。

## Ocean Specular：Blinn-Phong 大光斑

第二路高光是为了让沙"像水面"。水面在日落时会把一大条太阳映像拉成一条竖长的高光带——这是镜面反射在粗糙水面上的典型表现。相同的视觉效果完全可以用最经典的 **Blinn-Phong reflectance**：

$$I = (N \cdot H)^{power} \cdot strength, \qquad H = \frac{V + L}{\|V + L\|}$$

$H$ 是 $V$ 和 $L$ 的**半程向量**——几何直觉是"如果这条微表面朝向 $H$，它就把光直接反射到相机里"。$(N \cdot H)$ 衡量的是"宏观法线离这个理想微表面朝向有多近"。power 同样用来收紧高光锐度。

```hlsl
float3 OceanSpecular(float3 N, float3 L, float3 V) {
    float3 H = normalize(V + L);
    float NdotH = max(0, dot(N, H));
    float spec = pow(NdotH, _OceanSpecularPower) * _OceanSpecularStrength;
    return spec * _OceanSpecularColor;
}
```

Blinn-Phong 的历史脉络很整齐：Bùi Tường Phong 1973 年提出 Phong 模型用的是 $R \cdot V$（反射方向 vs 视线），James F. Blinn 1977 把它换成便宜的 $N \cdot H$——对绝大多数光照条件视觉上几乎一致，但更稳定、更便宜。现代 [[microfacet-brdf|微表面 BRDF]] 的 NDF 最早就是从 Blinn-Phong 的 $(N\cdot H)^p$ 泛化出来的。

## 合成：两路高光取 max

Journey 的两路 specular **不相加**——而是取 `max`：

```hlsl
float3 specularColor = saturate(max(rimColor, oceanColor));
float3 color = diffuseColor + specularColor;
```

这是一个风格化的选择：相加会让"轮廓处同时是 rim + ocean"的像素爆白；取 max 相当于"两条光永远只让最亮那条主导"，视觉上更干净。**艺术选择优先于能量守恒**——Journey 的整个美学都是往这个方向偏的。

## 第三路：glitter

Part 5 再加一条"沙粒闪烁"——用一张随机的 glitter normal map + 非常窄的镜面高光，让局部有少量极亮小点在相机移动时闪现。本页不详细展开；glitter 的难点是"时域稳定性"（在屏幕空间的采样不能产生 shimmer）和"能量守恒"（glitter 点不能把整块沙平均亮度拉上去）。

## 风格化渲染的普适技巧

这一系列说明了一个通用思路：**把真实材质拆成若干条解析项，每条用一个廉价模型单独调**。Rim 用 Fresnel 半式、Ocean 用 Blinn-Phong、Glitter 用随机 NDF，不追求任何一条物理自洽——但合起来通过美术参数调整可以达到"看起来是这种材质"的效果。这和完全走 [[physically-based-shading|PBR]] 骨架、让参数全部落在 albedo/roughness/metallic 上的思路相反，但在风格化项目里代价更低、可控性更强。

## 相关

- [[microfacet-brdf]] — Blinn-Phong 的物理化继承者
- [[physically-based-shading]] — 非风格化的路径
- [[shader-vector-math-primer]] — 半程向量 $H$、Fresnel 的几何直觉
- [[alan-zucconi]]

## Sources

- [[sources/alanzucconi-journey-sand-specular]]
