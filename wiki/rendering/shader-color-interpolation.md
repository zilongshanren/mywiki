---
tags: [shader, 颜色, 数学, 混合, 渲染]
date: 2026-04-14
sources: 1
---

# Shader 颜色插值（lerp 与线性混合）

shader 里「在两种颜色之间过渡」这件事，背后是一个非常基础但常被搞错的数学公式：**线性插值**。写错了的话画面会变亮、变暗、或者出现第三种奇怪的颜色——所以值得把它从第一性原理推一遍。

## 错误版本：加法

一个直觉上的尝试是「随着 blend 从 0 到 1，把第二种颜色叠上去」：

```hlsl
col = _Color + _SecondaryColor * _Blend;
```

这实际上做的是 **把两束光照在同一个点上**——原色始终 100% 在场，副色按 `_Blend` 权重叠加。结果就是亮度持续增加，颜色从 `_Color` 移向 `_Color + _SecondaryColor`，而不是移向 `_SecondaryColor`。

## 正确版本：凸组合

想让 `_Blend = 0` 得到 `_Color`、`_Blend = 1` 得到 `_SecondaryColor`，必须让两个权重之和恒为 1：

```
col = _Color * (1 - _Blend) + _SecondaryColor * _Blend
```

这就是 **线性插值**（linear interpolation）的定义——一个 **凸组合**（convex combination）：两个权重非负且和为 1，确保结果落在原色与副色的连线上、不会超出这条线段。HLSL 直接提供一个内置函数 `lerp(a, b, t)` 封装这件事，GLSL 里叫 `mix(a, b, t)`；它们对向量分量逐一插值，所以 `fixed4 col = lerp(_Color, _Secondary, _Blend)` 一行就够了。

## 三种常见使用场景

1. **两种纯色过渡**：Inspector 里两个 ColorPicker + 一个 `Range(0,1)` slider。
2. **两张纹理之间过渡**：先分别 `tex2D` 两张贴图，再 `lerp` 两个结果。注意每张贴图可能有自己的 `_ST`，所以 tiling/offset 要放在 fragment shader 里各算一次 UV。
3. **纹理作为 blend mask**：`_Blend` 不是 uniform，而是从第三张灰度图读出来的——`blend = tex2D(_BlendTex, uv).r`，再拿这个标量去 `lerp`。这种 **mask-driven blending** 是地形 splat map、溶解效果、污渍贴花的基础。

## 色彩空间注意事项

`lerp` 是在当前采样值所在的数值空间做线性混合——如果 shader 输入是 sRGB 未解码的 8bit 值，就会遇到和 [[alpha-blending]] 一样的问题：中间过渡会出现非自然的暗带。Unity 的 **Linear Color Space** 项目里纹理采样会自动 sRGB→线性，`lerp` 的结果是物理意义下的线性混合，写回 framebuffer 时再 γ 编码。这也是「色彩插值应当在线性空间」的根本原因——参见 [[color-space]]。

## 相关

- [[alpha-blending]] — 同样是凸组合的权重选择
- [[color-space]] — 线性 vs sRGB 的插值差异
- [[procedural-checkerboard]] — 典型的「二值 0/1 mask 走 lerp」用法
- [[oklab-color-space]] — 感知均匀空间里的渐变更好看
- [[fragment-shader]]

## Sources

- [[sources/ronja-color-interpolation]]
