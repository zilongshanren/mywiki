---
tags: [渲染, raymarching, 体积渲染, shader, sdf]
date: 2026-04-19
sources: 2
---

# 体积 Raymarching 的密度场与样本累积

[[volumetric-raymarching-intro|volumetric raymarch 入门]]关心的是「相机射线第一次碰到外壳」，属于 SDF (Signed Distance Field) raymarch 的自然延伸。真正的**体积渲染**（云、烟、火、光柱、等离子体）需要换一种思路：不是找第一个交点，而是**沿射线对体内光能做积分**。[[xor-shader-artist|Xor]] 的教程用 shader art 视角把这套思路拆成几个可组合的部件。

## 从 SDF 到 Density Field

核心替换：把 `distance(p)`（到最近表面的距离）换成 `density(p)`（局部体积密度）。raymarch 依然一步一步走，但**不再追求和表面相切**，而是希望**高密度区走小步（采样多）、低密度区走大步（快进）**。这是一个非物理但效率高的 heuristic：步长与密度倒数成正比。

Xor 的隧道例子：

```glsl
float volume(vec3 p) {
    return 3.5 - 0.25*length(p.xy) + 0.5*dot(sin(p), cos(p*0.618).yzx);
}
```

`length(p.xy)` 给一个无限圆柱；`dot(sin,cos)` 是廉价的 aperiodic [[dot-gyroid-noise|gyroid noise]]，给柱壁加扰动。

## 样本累积的两种模式

### 发光模式（additive）

每步都把颜色**除以距离/密度**累加——自然产生光衰减：

```glsl
for (float i = 0; i < STEPS; i++) {
    float d = volume(pos);
    pos += dir * d;
    col += LIGHT_COLOR / d;   // 近处贡献大、远处贡献小
}
col = tanh(BRIGHTNESS * col); // [[hyperbolic-tangent-shader|tanh tone-map]] 压回 [0,1]
```

注意：必须保证 `d > 0`；用 `abs(sum-2.0)` 让距离场**变空心**再加 passthrough 项是常用招数，保证 ray 能穿过表面而不卡死。

### 透明度混合模式（alpha blend）

像平常的 decal 一样从前往后 blend，但在体积采样序列上：

```glsl
color = mix(color, vec4(sample_rgb, 1.0), (1.0 - color.a) * sample_alpha);
if (color.a > 0.998) break;  // 已几乎不透明，提前退出
```

适合云、烟——这些东西不是光源，而是吸收/散射介质。

## 与其它技术的分野

- [[volumetric-fog-froxels|Froxel-based fog]]：用 compute shader 预计算整个视锥的 3D 光照纹理，fragment 只做三线性采样——全场景摊薄方案。
- **Per-fragment raymarch（本文）**：每像素独立循环，适合单体积物体（球、烟团、plasma）或 Shadertoy demo。
- [[volumetric-raymarching-intro|Analytic volumetric raycast]]：只处理能解析求交的外壳，与密度场的连续采样不兼容。

## 一个值得记住的小技巧

**死循环保险**：密度场常常会在某些退化位置返回 0（比如 `abs` 或 `mod` 的零点），造成 `pos += dir * 0` 无限循环或 NaN。两种防御：

- 在密度公式里加一个**小 passthrough**（Xor 的 `+ 0.1`）；
- 在颜色项里把 `col / d` 上方加 bias；
- 保证 `d >= some_epsilon` 的硬下限。

## 相关

- [[xor-shader-artist]]
- [[raymarching-intro]]
- [[volumetric-raymarching-intro]]
- [[dot-gyroid-noise]]
- [[hyperbolic-tangent-shader]]
- [[classic-shader-noise]]

## Sources

- [[sources/xor-volumetric-raymarching]]
- [[sources/xor-decoding-phosphor]]
