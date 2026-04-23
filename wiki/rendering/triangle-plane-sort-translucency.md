---
tags: [rendering, transparency, sorting, alpha-blending]
date: 2026-04-19
sources: 1
---

# 基于三角形平面划分的半透明排序

Supnik 2011 年在研究 AMD 的 OIT（顺序无关透明）演示后，放弃了把 X-Plane 的整个后端改造为链表式 deep framebuffer 的想法，转而思考一条更朴素的路径：**如果网格的三角形互不相交，是否总能为任意视角求出一个正确的前后绘制顺序？**

他给出的归纳是：任意两个不相交（除边/角以外）的单面三角形 A、B，只会落在三种情形之一：
- B 完全落在 A 平面的一侧 —— A 的朝向决定两者先后；
- A 完全落在 B 平面的一侧 —— 对称地由 B 决定；
- A、B 分别落在彼此平面的同一侧 —— 两者互不遮挡，任取顺序皆可，且若真相互背对其中至少一个必然背剔除。

关键前提是**三角形必须单面**：一个三角形对观察向量 V 可见，意味着其背面只对 –V 可见，这让我们能对两个相反视角解耦出两套排序。由此可以把「按视角排序」的逐帧成本，换成一个关于三角形对的二元关系，再由其生成整张网格的排序。

他本人承认这只是工程直觉而非证明，并担心结果是否严格构成 strict weak ordering。实践中这个方案的边界也清楚：动画变形可能打破假设、不同对象之间还需要额外的全局顺序。X-Plane 之所以敢这样做，是因为其典型半透明负载（窗户）重叠很轻，[[alpha-blending]] 排序误差不会暴露。

该思路与 [[alpha-blending-front-to-back]] 的「按面元深度排序」是不同层次：前者是**拓扑层面的预排序**，后者是运行时的深度比较。也可视作 Supnik 面对 [[order-independent-transparency]] 硬件方案时选择的「先解决小问题」（[[cheat-by-solving-less]]）立场。

## Sources

- [[sources/supnik-order-correct-translucency]]
