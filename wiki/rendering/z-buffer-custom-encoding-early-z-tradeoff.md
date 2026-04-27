---
tags: [rendering, z-buffer, depth-buffer, early-z, performance]
date: 2026-04-27
sources: 1
---

# 自定义 Z 缓冲编码与 Early-Z 的根本矛盾

在标准透视投影下，深度精度按 1/z 曲线分布——靠近相机精度过剩，远处精度不足，近裁剪面稍微靠近一点就会让远处发生严重 z-fighting。这催生了对自定义深度编码的需求，典型方案有：对数 Z（log-Z）和眼空间线性浮点深度。

## 自定义编码的代价：非线性

无论哪种自定义方案，它们有一个共同特点：裁剪空间 Z 值在三角形内部是**非线性**的。硬件光栅器对 clip-space 坐标做线性插值，而自定义公式的中间值与线性插值结果不同，因此必须把编码计算移到 fragment shader 里，逐像素精确计算。

## Fragment Shader 写入 Z 意味着丢失 Early-Z

[[early-z-late-z|Early-Z]] 是 GPU 在 fragment shader 执行之前就做深度测试、剔除被遮挡像素的硬件优化。一旦 fragment shader 修改了 `gl_FragDepth`（或等价的输出），GPU 就无法再提前裁剪——必须等到 shader 运行完才知道最终深度值，Early-Z 优化彻底失效。

更糟的是，代价不只发生在需要写 Z 的那趟 pass：**所有做 Z 测试的物体**（即便不写 Z）同样要在 fragment shader 里重新计算自定义深度，才能与缓冲中的值比较。这意味着粒子、云层等填充率密集的效果会变得更昂贵。

## 唯一的出路：浮点深度 + Reversed-Z

[[reversed-z]] 把 near/far 编码反转，利用浮点数在 0.0 附近精度最高的特性，在原本精度浪费最大的地方获得最佳分辨率。配合 `ARB_clip_control`（D3D 的 NDC 约定），可以用标准线性插值保留 Early-Z，同时获得远优于 1/z 曲线的深度分布——这是唯一一种不破坏 Early-Z 的"更好分布"方案。

## X-Plane 的实际选择

X-Plane 因为需要同时处理驾驶舱（毫米级精度）和大世界（数百公里），采用**两段 Z pass** 而不是自定义编码：每段使用标准线性 Z，改变 near/far 裁剪面，并共享同一个 G-Buffer 和 shadow map，将额外开销降到最低。这是放弃精度分布优势、保留 Early-Z 的务实权衡。

## Sources

- [[sources/supnik-custom-z-buffer-early-z]]
