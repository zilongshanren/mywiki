---
tags: [渲染, 法线贴图, mipmap, 反走样, 材质, 高光, 遮蔽]
date: 2026-04-27
sources: 1
---

# 法线贴图 Mipmap 走样问题

法线贴图在图形管线中被广泛用于表达几何细节，但它有一个根本性缺陷：**作为表面导数（derivative measure），在 mipmap 缩小时趋向平坦**，导致高频细节在中远距离完全消失。这个问题在离线渲染中不突出（超采样可以化解），在实时渲染中却是一个长期被低估的视觉缺陷。

[[angelo-pesce]] 在 2012 年的博文中系统梳理了这一问题及实用的替代编码方式。

## 为何法线贴图不能自然 mipmap

法线贴图存储的是切线空间下的法线方向。GPU 的 mipmap 生成是对颜色通道做线性平均；将多个法线方向平均后，结果趋向 [0,0,1]（平坦表面法线）。换言之，**mipmap 平均不保留法线所隐含的照明贡献**。

标准 MSAA 没有帮助：MSAA 只增加深度/几何采样点，不增加着色点，法线贴图仍是每个 shading sample 一次查询。超采样（SSAA / 8× 或更高）在技术上可以缓解，但在实时场景中不可行。

核心矛盾是**预滤波与后滤波的不等价**：正确的流程是先对每个微法线计算照明再平均（后滤波）；mipmap 做的是先平均法线再计算照明（预滤波），两者对非线性光照函数是不等价的。

## 替代编码方案

### 遮蔽贴图（Occlusion Map）

遮蔽是在光照**之后**应用的乘性因子，因此 mipmap 的线性平均对最终结果仍然有意义。细节越尖锐（越细的凹陷），遮蔽值越大——这种编码天然适合皮肤毛孔、缝线、划痕等"表面凹陷型细节"。相比法线贴图，遮蔽贴图编码相同细节所需的纹素分辨率也更低。

### 高光指数贴图（Exponent / Gloss Map）

对于圆形高光形状（铆钉、汗珠、高光斑点），从远处观察时这些微小反射面的统计效果等同于**降低了 Phong exponent**（展宽了散射锥）。因此在 gloss map 里用较低的 exponent 来表达这些细节，比用法线贴图准确得多，且能正确在 mip 层级间过渡。

### LEAN / CLEAN：方差驱动的 Gloss Mipmap

Call of Duty: Black Ops 在 SIGGRAPH 2011 公开了一个优雅的工程化方案：**在生成 mipmap 时，计算当前 mip texel 覆盖的法线束的方差，用方差调低 gloss 量，写入 mip**。运行时零额外开销，仅 mipmap 生成阶段有额外计算。这是"预滤波 BRDF"的早期工业落地，LEAN（Linear Efficient Antialiased Normals）和 CLEAN 是对应的学术论文。

对于任意 BRDF，可以针对该 BRDF 推导最优的 gloss-to-variance 映射函数，而不必使用 Phong 的近似。

## 可变尺度材质

理想的材质在所有观察尺度下都应该正确表现：

- **近距离**：法线贴图 + 高 exponent，逐像素表达汗珠形状
- **中远距离**：降低 exponent（或查 gloss mip），法线贴图自然趋平
- **极远**：完全退化为材质基础 BRDF 参数

这可以通过 mip 层级间插值 gloss 参数来实现，与 [[mipmap-generation-sampling]] 里 LOD 系统协同。

## 对美术工作流的影响

法线贴图的 mipmap 失效有一个视觉副作用：美术往往会人为夸大细节（如放大毛孔、加粗睫毛），因为在观察距离下细节本应消失，但只有这样才"看得见"——这导致近看模型时细节比例严重失真，呈现塑料玩具质感。认识到这一问题后，可以改用遮蔽/gloss 贴图来表达细节，放弃对法线贴图过度依赖。

## 相关

- [[tangent-space-normal-mapping]]
- [[normal-map-blending]]
- [[mipmap-generation-sampling]]
- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[preintegrated-skin-shading]] — 皮肤渲染中的法线分层使用
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-normalmaps-everywhere]]
