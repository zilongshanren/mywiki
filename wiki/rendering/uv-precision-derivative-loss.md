---
tags: [渲染, shader, 导数, 浮点精度, normal-mapping]
date: 2026-04-19
sources: 2
---

# Vertex-projected UV 的导数精度耗尽

[[ben-supnik|Supnik]] 在 X-Plane 地形系统里遇到过一个只在 GF 8800 上复现、在 HD 4870 上看不见的 bug：per-pixel 法线贴图的 tangent space 会出现**像素级噪声**，像撒了一把胡椒粒。

## 场景

X-Plane 的地形 tile 大到 300 × 300 km。为了让美术直接在「未做任何 UV 展开」的 mesh 上贴 bump map，tangent 基底不随顶点保存，而是在 **fragment shader 里从 UV 的 `dFdx` / `dFdy` 反推出来**（参见 [[tangent-free-normal-mapping]]）。

UV 又是 vertex shader 里从**世界空间顶点位置**投影出来的——一个 300 km 尺度的 mesh 投到几个单位的 UV 里，但若纹理被放大（tile rate 高），实际送给 fragment shader 的 UV 数字会相当大。

## 问题

当插值出的 UV 数值本身已经消耗掉了 fp32 的低位，**相邻像素间 UV 的差值**可能低于 fp 可以稳定表达的粒度——你本想得到 `du ≈ 一像素覆盖的纹理距离`，实际得到的是量化后的 0、噪声、或符号错的小数。

基于这个坏导数算出的 tangent / binormal 在每个像素独立抖动，投射到法线贴图采样上就是每个像素独立方向的光照错误：整片地形出现 per-pixel 高频噪点。

8800 与 4870 的差异大概源自两家在内部 interpolator 精度和差分器精度上的实现差异——**ATI 当时内部精度更高，暂时把 bug 藏住了**。但从原理上两家都是对的，不能指望硬件替你补救。

## 两条出路
Supnik 给出两条互补的 work-around：

1. **提高 UV 坐标本身的精度**：不要让 vertex shader 投影出的 UV 已经吞掉低位。例如把投影的 origin 拉近相机、或者拆成「低频 + 高频」两部分。
2. **不要用 `dFdx(UV)` 反推 tangent 基底**：在「vertex 投影生成 UV」这条 case 下，投影参数本身是**已知**的——直接把投影轴作为 tangent 基底传下去，绕开差分。

### 补充：算法式导数完全替换内建差分

Supnik 在 *Derivatives III*（2011-01）把这条路走到极致：既然出问题的 UV 总是在 vertex shader 里**按公式生成**的（世界坐标直接投影），那对应的公式本身就可微——**直接在 fragment shader 里算出解析的 `du/dx`、`du/dy`，彻底不调内建 `dFdx/dFdy`**。精度由你自己选的浮点路径决定，不再被两像素差分的量化阈值卡住。代价是 shader 里多算几行代数，但对「UV = f(position)」这类构造，公式本就在手边。

## 和「不连续 UV」的对比

这个问题和 [[texture2dgrad-explicit-derivatives]] 表面像——都是导数不可靠——但病根不同：

| | 不连续 UV | 精度耗尽 UV |
|---|---|---|
| 成因 | shader 里做 fract/swizzle 破坏连续性 | UV 数值过大，差值低于浮点精度 |
| 表现 | 缝隙处 1 条低 mip 艺术带 | 整个面高频噪点 |
| 修法 | `texture2DGradARB` 显式喂原始导数 | 改 UV 生成方式或绕开差分 |

两者共同的教训：**差分是一次数值测量，测量有噪声阈值**。当你的 UV 生成方式会让这个阈值变大，就不能指望硬件隐式差分。

## 相关

- [[tangent-free-normal-mapping]]
- [[texture2dgrad-explicit-derivatives]]
- [[huge-world-coordinate-precision]] — 同一个项目的另一个 fp32 精度问题
- [[ben-supnik]]

## Sources
- [[sources/supnik-running-out-of-derivative-res]]
- [[sources/supnik-derivatives-iii-ran-out-of-rez]]
