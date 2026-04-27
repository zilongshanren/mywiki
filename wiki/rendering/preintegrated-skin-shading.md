---
tags: [渲染, 次表面散射, 皮肤渲染, 预积分, 实时渲染]
date: 2026-04-27
sources: 1
---

# 预积分皮肤着色（Preintegrated Skin Shading）

预积分皮肤着色由 Eric Penner（SIGGRAPH 2011）提出，是一种把皮肤次表面散射（Subsurface Scattering, SSS）压缩到**一张二维查找表（LUT）**里、在实时渲染里零额外开销使用的技术。[[angelo-pesce]] 在配合 Penner 准备 SIGGRAPH 演讲期间，独立用 Mathematica 推导了该积分的解析近似，形成对这一技术的配套理论补充。

## 核心思想

皮肤的次表面散射行为取决于**剪切点邻域的散射轮廓**。当不考虑阴影造成的光照不连续（另行处理）时，邻域可以用**表面曲率**来近似——曲率越大，散射效果越明显（鼻尖 vs 脸颊）。

具体做法：

1. 取 Jensen 的多层高斯 SSS 模型（d'Eon & Luebke 2007 的系数组）作为散射剖面（diffusion profile）。
2. 在**同曲率的圆柱截面**（一维圆弧）上，对散射剖面与 Lambert 余弦项做预积分。
3. 积分结果以 **(NdotL, 曲率半径)** 为两个轴，写入一张二维 LUT。

运行时着色器只需查这张 LUT，避免了实时卷积。

## 数学细节（Pesce 近似）

散射函数是六个高斯之和：

$$
S(x) = \sum_{i=1}^{6} w_i \cdot G(x, \sigma_i)
$$

预积分的漫反射系数为：

$$
D(\theta, r) = \frac{\int_{-\pi}^{\pi} \text{max}(0, \cos(\theta + x)) \cdot S(|2r \sin(x/2)|)\, dx}{\int_{-\pi}^{\pi} S(|2r \sin(x/2)|)\, dx}
$$

其中 $\theta$ 是表面法线与光源夹角，$r$ 是曲率半径。对于大曲率（$r \to \infty$），$D$ 退化为 Lambert 余弦。

Pesce 选用了一个有 6 个自由参数的参数化函数，通过 Mathematica 的 `NonlinearModelFit`（底层调用 `NMinimize`，因模型含 `Max`/`Clip` 非光滑项）拟合样本，得到可在 shader 中直接计算的近似式，从而**消灭 LUT 查询**，纯代数计算还原着色结果。

## 实现注意事项

- 高斯系数使用 d'Eon & Luebke 2007 的 RGB 三通道权重；R 通道散射最宽（皮肤暗红调的来源），B 通道最窄。
- 曲率可从**屏幕空间法线梯度**或**顶点曲率贴图**中估计；实时场景中粗略估算即可，误差对视觉影响可接受。
- 对阴影边缘（光照不连续处），需要额外的「窄散射 pass」或 SSS bitmask 补充——Penner 原文有专门讨论。
- 若预积分 LUT 不可用（内存/带宽受限），Pesce 的解析近似是等价替代。

## 背景：Mathematica 作为图形原型工具

[[angelo-pesce]] 在这篇文章中还用 Mathematica 演示了**用计算机代数系统加速图形研究**的范式：符号推导 → 数值采样 → 参数拟合 → 可视化验证，整个流程在一个 notebook 里完成。`NonlinearModelFit`、`SphericalPlot3D`、`ListPlot3D` 等 Mathematica 函数可以把本来要写几百行 C++ 的数学原型压缩到几十行。

## 相关

- [[physically-based-shading]] — SSS 是 PBR 的次表面传输分支
- [[spherical-harmonics]] — 另一种球面信号的低维表示手段
- [[microfacet-brdf]] — 镜面反射侧，与 SSS 共同构成完整皮肤着色模型
- [[angelo-pesce]]
- [[c0de517e-skin-rendering-horrors]] — Pesce 2011 皮肤渲染三大错误的实践总结，涵盖 SSS ramp、AO 混合、高光形状等 hack
- [[skin-rendering-practice]] — 皮肤渲染实践方法论（注意细节、参考资料、tonemapping、尺度、完整光照）

## Sources

- [[sources/c0de517e-mathematica-skin-rendering]]
- [[sources/c0de517e-skin-rendering-horrors]]
- [[sources/c0de517e-mathematica-skin-addendum]]
- [[sources/c0de517e-skin-rules-2]]
