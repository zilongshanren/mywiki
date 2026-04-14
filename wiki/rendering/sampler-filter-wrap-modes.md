---
tags: [shader, 纹理, 采样, gpu, 渲染]
date: 2026-04-14
sources: 2
---

# 采样器的 Filter / Wrap 模式

`Sample Texture 2D` 的 `Sampler State` 输入控制着 GPU 采样单元如何从纹理里取值。它只有两个维度——**如何在像素之间插值**（Filter Mode）和**UV 超出 `[0, 1]` 时怎么处理**（Wrap Mode），但名字里有几个容易混淆的陷阱。Cyan 在 UV-Based Nodes 里把它们单独列出来，值得记录。

## Filter Mode

- **Point**：最近邻，零插值。贴近像素看起来**硬边、马赛克**。做像素画、像素风 UI、Minecraft 风格方块必须用这个——线性插值会把像素画的灵魂模糊掉。
- **Linear**（纹理 Inspector 里叫 **Bilinear**）：相邻四像素 bilinear 混合，贴近时**模糊**。这是大多数普通纹理的默认。
- **Trilinear**：这个名字是最大的坑。它不是"3D 纹理的线性滤波"——2D 纹理一样可以用 trilinear。它的含义是"Linear + 在相邻 mipmap level 之间也做一次线性插值"：bilinear 负责 XY 两个轴、第三次线性插值负责**mipmap 轴**，三个轴合起来才叫 trilinear。好处是相机前后移动时不会看到 mipmap 级别切换时的"突跳"；代价是每次采样多读一次 mipmap 相邻 level。

Cyan 的补充："shader 里的 Linear 其实就是 bilinear——即使是 3D 纹理也是三个轴都线性插值，而 trilinear 名字里的第三次线性是额外的 mipmap 维度，和 3D 纹理毫无关系。"这条澄清值得贴在每一份新手文档上。

## Wrap Mode

- **Repeat**：UV 超出 `[0, 1]` 时按整数周期重复。这是让 `Tiling And Offset` 看起来"平铺"的唯一开关——见 [[uv-manipulation-nodes]]。
- **Clamp**：超出时把 UV 夹到边缘；边缘像素被**拉伸**。常见于天空盒贴图、ramp 贴图（不希望颜色回卷）。
- **Mirror**：每个整数边界镜像一次，得到不产生接缝的无缝平铺。适合有些对称模式的纹理。
- **Mirror Once**：镜像一次然后按 clamp 处理。Cyan 文中提到它，但实际用得不多。

## 和 mipmap 的耦合

Filter Mode 和 Wrap Mode 并不独立。例如带 mipmap 的纹理用 Repeat 模式时，UV 在 `0 → 1` 的跨越处**看起来**应该无缝，但如果 shader 在着色之前做了 `Fraction`（把坐标人为回绕），那么 GPU 的 mipmap 选择硬件依据**屏幕空间的导数**去估算采样密度——`Fraction` 的跳变让导数短时间失真，结果就是跳变边上出现一条糟糕的 seam。Cyan 提醒到这点，但没展开；解决方案通常是用 `tex2Dgrad` 显式传入导数，或者换成无 mipmap 的采样策略。

## 和 Sampler State 资源的解耦

Shader Graph 允许在 `Sample Texture 2D` 的 `Sampler(SS)` 输入上连一个独立的 Sampler State 资源。这是在**覆盖**纹理 Inspector 里的默认设置——例如同一张贴图既用 Linear+Repeat 做墙面、又想在另一个 material 里用 Point+Clamp 做像素风 UI，就可以通过两个不同 Sampler State 解耦，而不需要两张纹理资源。

## Metal 的具体落地

[[metal-texture-sampler|Metal 的 sampler]] 把这些概念系统地实现成两种形式：**host 侧的 `MTLSamplerState`**（填 `MTLSamplerDescriptor` 创建，用 `[[sampler(n)]]` 在 shader 里引用）和 **MSL 源码里的 `constexpr sampler`**（编译期构造，整个函数共享一份）。Metal 独有 `address::clamp_to_zero`——越界返回黑色或透明，OpenGL 里没有对应项；其余四种 address mode（clamp_to_edge / repeat / mirrored_repeat）和两种 filter（nearest / linear）都和上面讲的一致。因为 constexpr sampler 参数必须静态，运行时需要切换 sampler 配置就只能走 host 侧那条路。

## 相关

- [[uv-manipulation-nodes]]
- [[fragment-shader]]
- [[image-resampling-filters]]

## Sources

- [[sources/cyan-uv-based-nodes]]
- [[sources/metalbyexample-textures-and-samplers]]
