---
tags: [shader, hlsl, ps1, 复古, interpolator, affine, 透视]
date: 2026-04-19
sources: 1
---

# `noperspective` 关键字与 Affine 纹理扭曲

现代 GPU 在把顶点属性（UV、颜色、任何 `TEXCOORD` 语义的数据）从三角形顶点插值到片元时，默认使用 **perspective-correct interpolation**——每个顶点属性先乘自己的 `1/w`、线性插值后再乘当前像素的 `w`，这样确保透视变换下的 UV 沿表面"贴实"而不是在屏幕空间线性铺开。**PS1 的硬件没做这一步**——它只做 affine（纯屏幕线性）插值，结果就是纹理在掠射角度下呈现著名的"拉扯扭曲"，也就是所谓 **affine texture warping**：三角形的一个边近一个边远时，UV 沿屏幕空间线性分布，造成斜面纹理看起来像被撕了一下。

## 用 `noperspective` 直接切换

HLSL（以及 D3D11 以来的主流 shading 语言）支持在 interpolator 变量前加 `noperspective` 关键字，**跳过** perspective-correct 插值。这让重现 PS1 affine warping 变得一行代码的事：

```hlsl
struct v2f
{
    float4 positionCS : SV_POSITION;           // clip space 位置
    noperspective float2 uv : TEXCOORD0;       // affine 插值
};
```

加了 `noperspective` 的 UV 在每个像素上直接用屏幕空间线性插值——三角形越倾斜、warping 越明显。不加就是现代默认。

这是 [[retro-rendering-techniques|PS1 retro 风格]] shader 里**最简洁**的 affine warp 实现。但它的缺点是 **on/off 二态**——不能平滑地在 affine 和 perspective 之间过渡。如果 asset（例如 Ilett 的 *Retro Shaders Pro*）要求把 warping 强度做成 0–1 滑杆，就需要**手动实现**：vertex 阶段不除 w、fragment 阶段按比例 `lerp` 两种插值结果，或者把 UV 和 `1/w` 都传进去然后在 fragment 里按需 undo division。Ilett 在他的 PSX shader 里选了后者——代码量更大但支持平滑过渡。

## Perspective-correct 插值的原理速回

理解 `noperspective` 的价值要先回到光栅化数学。三角形从 clip space 映射到屏幕时做了透视除法 `xy / w`。如果直接对 uv 做**屏幕线性插值**，远顶点的 UV 被过度采样（屏幕上离近顶点更近但 UV 却离近顶点很远）——结果就是纹理拉扯。正确做法：在 vertex 阶段把 uv 和 1 都乘以 `1/w`，片元阶段插值后再除以插值后的 `1/w` 恢复——这样插值是沿着 3D 空间的表面线性的，不是沿屏幕。`noperspective` 就是 opt-out 这套数学。

PS1 不做这一步的原因非常工程：**除法贵**。1994 年的硬件做不起每像素一次 `1 / interpolated_w`。现代 GPU 几乎每个 shader pipeline 都把它做进固定功能、零成本，所以默认就是 perspective-correct。

## 与其他 interpolator 修饰

HLSL 提供的 interpolator 修饰符不止 `noperspective`：

| 修饰符 | 作用 |
|---|---|
| `linear`（默认） | perspective-correct 线性 |
| `noperspective` | 跳过透视校正的线性插值 |
| `nointerpolation` | 不插值，片元拿第一个顶点（provoking vertex）的值——常用来传 per-triangle flat 数据 |
| `centroid` | 在 MSAA 时从 covered sample 的质心采，而不是像素中心——减少边缘 shimmering |
| `sample` | per-sample 插值，专供 per-sample shading |

几种可以组合，如 `noperspective centroid float2 uv : TEXCOORD0`。retro shader 一般只用 `noperspective`。

## 仅用于 "像素风" 吗

不完全。早年硬件限制的现代 artistic 还原固然是主要用途（PSX asset pack），但 `noperspective` 在一些图形研究里也用：

- **Debug / 可视化**：直接看屏幕空间插值的行为，和 perspective 结果对比做 sanity check。
- **屏幕空间贴花近似**：决定屏幕坐标时不想再做透视除法。
- **飞近时的快速 UV 线性假设**：近平面 mesh 上 affine ≈ perspective，用 `noperspective` 省一次硬件除法——在嵌入式或老手机 GPU 上有意义，现代桌面 GPU 上差异可忽略。

## 相关

- [[retro-rendering-techniques]] —— affine warping 作为 PSX 视觉特征之一
- [[fragment-shader]] —— 插值发生的前一阶段
- [[coordinate-spaces]] —— 为什么 `/w` 是透视的核心
- [[hlsl-derivation-correctness]] —— interpolator 的另一组修饰符家族

## Sources

- [[sources/danielilett-retro-shaders-pro-breakdown]]
