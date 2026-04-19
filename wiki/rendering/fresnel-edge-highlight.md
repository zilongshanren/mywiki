---
tags: [shader, shadergraph, fresnel, rim-light, unity, 渲染]
date: 2026-04-19
sources: 1
---

# Fresnel 边缘光与 HDR 高亮

Fresnel 效应的物理根源是"掠射角下反射率升高"，但在实时渲染里更常被当作一个**廉价的边缘高光技巧**使用——不关心光学准确性，只要球形/曲面物体边缘亮起一圈就能让它从背景里跳出来。[[daniel-ilett|Daniel Ilett]] 的 Shader Graph Basics Part 7 把这件事做到了最精简：一个 `Fresnel Effect` 节点 + 一个 HDR 颜色 + Bloom 后处理，就是完整配方。

## Fresnel Effect 节点做什么

Shader Graph 内建的 `Fresnel Effect` 节点输出一个 `[0, 1]` 的浮点值，等价于 `pow(1 - dot(N, V), Power)`：法线和视线夹角越接近 90°（即视线掠过表面），值越接近 1。三个输入里 `Normal` 和 `View Vector` 正常情况下留空、自动取当前 fragment 的值，唯一需要调的是 `Power`——越大边缘越细。它可以嵌在 **Unlit 图**里用，不必走 Lit 的 PBR 路径，这是它成为"装饰性边缘光"首选的原因。

Lit Shader Graph 其实内部已经做了 Fresnel——它是[[physically-based-shading|PBR]] specular 的一部分，受 smoothness 调制——但那是和光源、环境光耦合的"真"Fresnel。Ilett 这里故意把它剥离出来、当纯粹的屏幕空间装饰用，两种用法不冲突。

## HDR 颜色 + Bloom = 真正的"发光"

单独乘一个普通颜色只能得到一圈亮色，看着不会"发光"。配方的另一半是把 Fresnel 乘一个 **HDR 颜色**：Shader Graph 的 `Color` 属性 Node Settings 里把 Mode 改成 HDR，就多出一个 Intensity 字段。底层做的是 `rgb * 2^intensity`——intensity = 3 就是每通道乘 8，结果远超 `[0, 1]` 范围。单是这样只会被硬裁剪成白色，必须配合 **Bloom 后处理**才能把"超过 1 的亮度"扩散成视觉上的辉光。这和 [[shader-graph-lighting-primer|Lit 图的 Emission 槽位]]是同一套公式，也是 [[pokemon-terastallize-shader]]、能量护盾、霓虹灯所有 Unity "发光"效果的唯一路径。

HDR 颜色选色器有一个看起来像 bug 的行为：关闭再打开，RGB 值和 Intensity 值会变化但合成颜色不变——因为 `(1, 1, 1, intensity=3)` 和 `(8, 8, 8, intensity=0)` 数学上相等，选色器内部做了一次重新分解。

## 局限：只在曲面上好看

Fresnel 的数学基于 `dot(N, V)`——同一个平面上所有像素的法线方向一致，Fresnel 值也几乎一致。结果是：球体、胶囊体、有机曲面上这套效果完美，但立方体的每个面内部亮度均匀、只在边缘棱处突变，看起来不像"发光"更像"整面渐变"。Ilett 明确提醒这点：这个 trick 是给曲面用的，立方体得换别的路子（例如 [[uv-manipulation-nodes|基于 UV 的边缘检测]]，见 Part 9 的 Edge Glow 做法）。

## 和 rim light 的关系

"Fresnel light" 和 "Rim light" 在实时渲染语境里几乎是同一个东西——都是 `1 - N·V` 的标量乘一个颜色。[[cel-shading-pipeline|Cel shading 管线]]第 3 步里 Ilett 用的就是这个公式，只是把输出切成硬阶（`smoothstep`）给卡通着色用。Part 7 的 Fresnel Highlight 则保留平滑过渡，配 HDR + Bloom 做写实或半写实的"高光提示"，两者共享底层数学但走不同的后处理阶段。

## 相关

- [[daniel-ilett]]
- [[shader-graph-lighting-primer]] — Lit 图里 Fresnel 被内建在 specular 里
- [[bloom-threshold-blur-composite]] — HDR 辉光生效的必要条件
- [[cel-shading-pipeline]] — 同一套 `1 - N·V` 公式用在卡通渲染里的版本
- [[normalised-blinn-phong-shader]]
- [[physically-based-shading]]
- [[uv-manipulation-nodes]] — 立方体边缘光的替代方案

## Sources

- [[sources/danielilett-shader-graph-custom-lighting]]
