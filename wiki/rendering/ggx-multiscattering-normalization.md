---
tags: [渲染, pbr, brdf, ggx, 能量守恒, 多次散射]
date: 2026-04-27
sources: 1
---

# GGX 多次散射归一化（GGX Multiscattering Normalization）

标准 GGX [[microfacet-brdf]] 只模拟光线与微表面的**单次散射**。被 masking-shadowing 项遮蔽的能量被直接丢弃，而不是让它在相邻 microfacet 间继续弹射。结果是：**粗糙金属在均匀光照下比理论值更暗**，且在高 roughness 下亮度随粗糙度非线性下降，参数不正交。

## 炉子测试（Furnace Test）

验证 BRDF 能量守恒的标准手段：将材质置于均匀辐射的白色环境中，设 f0=1（Fresnel 为 1，所有能量都反射）。理想情况下，物体应当消失（因为出射辐亮度 = 入射辐亮度）。标准 GGX 无法通过：高粗糙度下球体依然可见且偏暗，证明存在能量泄露。

## 解法对比

### Kulla/Conty（SIGGRAPH 2017）

Imageworks 的完整解法，在单次散射项之外添加一个补偿 lobe $f_{ms}$，其强度被设计成恰好补回 $1 - E(\mu_o)$ 的流失能量，同时正确模拟多次弹射引起的**色彩饱和度累积**（每次反射都经过 Fresnel，导致更高 roughness 时材质色彩更饱和）。这是物理上更准确的解，但参数化上 roughness 既影响亮度又影响饱和度。

[[stephen-hill]] 在「A Multi-Faceted Exploration」系列中发现了 Imageworks 原版推导的一个错误，修正后 $F_{ms}$ numerator 从 $F_{avg}$ 变为 $F_{avg}^2$。

### Pesce 2019「最无知近似法」

[[people/angelo-pesce]] 的方案从另一个方向出发：**只保证能量守恒，不模拟多次弹射的饱和度效应**。

做法是用 split-sum LUT 中已有的 directional albedo 值反向归一化 BRDF：

```glsl
// split-sum LUT 已给出 scale(roughness, NdotV) 和 bias(roughness, NdotV)
float normFactor = 1.0 / (bias + scale);  // bias/scale 均在 f0=1 条件下查询
brdfSpecular *= normFactor;
```

优势：
- **无需新纹理**：split-sum LUT 本就存在，只多一次 LUT 采样
- **参数正交**：roughness 只影响亮度分布，不影响饱和度，艺术家调参更直观
- **炉子测试通过**：f0=1 时任意 roughness 下球体消失

劣势：
- f0 的物理含义与 Kulla 方案不同（代表不同的 albedo）
- 不满足 BRDF 互易性（对实时渲染无影响）

若需要近似模拟饱和度，可进一步乘以 `1 + f0*(normFactor - 1)`，结果接近 Kulla，但仍不完全一致。

## 解析近似（去除 LUT 依赖）

归一化函数 `1/(bias + scale)` 形状极简，可用多项式拟合：

- 含 NdotV：`1 + 2*α²*NdotV`（α = roughness²）
- 不含 NdotV：`1 + α²`

后者更简单，引入的误差在粗糙大角度处稍大，但多数情况下视觉不可区分。

## 工程立场

两种解法都能量守恒，选哪种取决于参数化语义的取舍。Pesce 的论点：**渲染不是在追求物理正确，而是在追求对内容创作有益的工具**。如果「更正确的物理」使材质参数空间更复杂，对生产是净损失。

此思路与 [[pbr-approximation-stack]] 的整体性评估观点一致：不应在一个局部过度精化，而忽视其他层的误差。

## Sources

- [[sources/c0de517e-misunderstanding-multiscattering]]
