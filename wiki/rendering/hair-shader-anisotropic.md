---
tags: [rendering, shader, hair, anisotropic, unity, brdf]
date: 2026-04-19
sources: 1
---

# 各向异性发丝着色（Hair Shader）

[[rune-skovbo-johansen]] 在 2025 年为普通 Unity sphere/capsule 写了一组三档头发着色器，完全不依赖特殊发丝网格或头发贴图。核心思路：**复用 Unity Standard BRDF**，在其之上做各向异性模拟——把表面近似为一簇沿 UV 的 V 方向排列的平行圆柱。

## 三个实现档位

1. **Full Multisample**：暴力方案。沿发丝方向的法线轴旋转出一个 180° 扇面内的 50 个采样法线，对每个采样运行完整 Standard BRDF，再按权重加权平均。贵但效果可靠。
2. **Specular Multisample**：只对与法线相关的点乘和 specular 项多采样（50 次），漫反射、菲涅尔等只算一次。与 Full 版几乎无差别，成本显著降低。
3. **Approximation**：完全不多采样，用解析公式去拟合多采样的输出。是作者"靠直觉+试错+对照"做出来的非物理近似，难以用几行数学说清楚。

## 权重函数

每个多采样点的权重 = 两个余弦的乘积（都 clamp 到 [0, 1]）：

- `cos(angleBetween(原始法线, 修改法线))`：从侧面看发丝簇时，面朝外的那部分不被其他发丝遮挡。
- `cos(angleBetween(修改法线, 视线))`：面朝相机的发丝在屏幕占比更大。

这两项相乘就足以模拟出"头发顺着长轴方向有沿高光线"的视觉效果，而不需要专门的 hair BRDF（Kajiya-Kay / Marschner）。

## 工程取舍

- 优点：直接兼容 Unity Surface/Standard shader 生态，放到任何资源商店里的角色上，只要发丝 UV 沿 V 方向就能用。
- 限制：波浪/卷发 UV 方向不严格垂直时会轻微失真。
- 作者坦言自己**看不懂大多数图形学论文**（包括专门的 hair rendering 论文），原因更多是文献书写风格问题。他的实现是"第一原理+实验"路径。

## 相关

- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[hybrid-hair-rendering]] — 另一种工业级的"mesh+shell"发丝方案
- [[tessellation-fur-rendering]]

## Sources

- [[sources/runevision-hair-and-atmosphere]]
