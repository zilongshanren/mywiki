---
tags: [渲染, shader, 光谱, 颜色, 拟合]
date: 2026-04-14
sources: 1
---

# Branchless 波长到 RGB 拟合（Zucconi Rainbow）

把可见光 400–700 nm 的波长映射回屏幕 RGB，是光谱渲染和物理衍射 / 干涉效果着色器的共同子问题。GPU Gems 书里给出的经典做法是用三个**凸抛物线**（作者称之为 *bump*）分别拟合 R、G、B 三个分量的分布：

$$bump(x) = \max(0,\,1 - x^2)$$

然后把 R/G/B 分量写成 `bump` 在输入上的平移。好处是**完全没有分支**——在 shader 里非常廉价；代价是 GPU Gems 原始参数是作者手调的，拟合误差尤其体现在蓝紫段。

## Zucconi 的两步改进

[[alan-zucconi|Alan Zucconi]] 在 *Improving the Rainbow – Part 2* 里保留 `bump` 的结构，重新用 Python 数值拟合参数，得到的 `spectral_zucconi` 在视觉和数值上都显著优于 GPU Gems 原版，仍然是 branchless 的。核心是把三个 bump 的 `c`、`x`、`y` 偏置打包成 `float3`，一次 `saturate(1 - x*x - yoffset)` 就算完三通道：

```hlsl
inline fixed3 bump3y (fixed3 x, fixed3 yoffset) {
    float3 y = 1 - x * x;
    return saturate(y - yoffset);
}

fixed3 spectral_zucconi (float w) {
    fixed  x  = saturate((w - 400.0) / 300.0);
    const float3 cs = float3(3.54541723, 2.86670055, 2.29421995);
    const float3 xs = float3(0.69548916, 0.49416934, 0.28269708);
    const float3 ys = float3(0.02320775, 0.15936245, 0.53520021);
    return bump3y(cs * (x - xs), ys);
}
```

再进一步的 `spectral_zucconi6` 用**两组 bump 叠加**（共 6 条抛物线），专门改善紫/橙段的残差——精度更高，代价是多一组常量和一次 `bump3y` 调用。

## 为什么要坚持 branchless

在 shader 里 JET / Bruton / Spektre 等基于 `if` 的波长→颜色映射在 C# 里看起来简洁，但在 GPU 上分支会引入 warp divergence，性能不稳定。`bump` 方案用几次乘加取代所有条件——既不需要纹理 LUT，也不需要分支，单个像素成本固定，非常适合衍射光栅、薄膜干涉、油膜这类会在一个像素里对多条波长做并行叠加的效果。

## 和光谱渲染的关系

这个拟合并**不是**严格意义上的 CIE XYZ → sRGB 变换——它是对「把 400–700 nm 可见光谱可视化成一条彩虹」这个感知问题的快捷近似。真正的光谱渲染（见 [[spectral-rendering]]、[[hero-wavelength-spectral-sampling]]）要处理 MC 采样、CIE 色匹配函数、色彩空间变换，代价更高。Zucconi 拟合是 shader art 场景下的廉价平替，在 [[diffraction-grating-shader|CD-ROM 衍射光栅]] 和虹彩效果里被广泛使用。

## 相关

- [[spectral-rendering]] — 完整光谱渲染的背景
- [[hero-wavelength-spectral-sampling]] — MC 场景下的 wavelength 抽样
- [[diffraction-grating-shader]] — 使用本函数的典型着色器
- [[shader-vector-math-primer]]
- [[alan-zucconi]]

## Sources

- [[sources/alanzucconi-improving-rainbow-2]]
