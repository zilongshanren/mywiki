---
tags: [rendering, frostbite, deferred-rendering, pbr, analysis, specular, ssao, dof]
date: 2026-04-27
sources: 1
---

# Frostbite / BF4 渲染技术分析（2013）

[[angelo-pesce]] 2013 年对 Battlefield 4 做的非正式技术评析，是 2013 年 PC 次世代渲染实践的一份实地记录。Frostbite 在当时是公认的技术质量标杆，这份分析的批评性视角使其对渲染工程师更有参考价值。

## 结构：从"问题"到"亮点"

Pesce 刻意先列问题，再谈优点——因为在"每个人都说它好"的前提下，值得思考的是可改进之处。

### 三个主要问题

**1. 镜头光晕滥用**
光晕效果本身工艺出色（稳定、支持遮挡衰减、混合了 screenspace + 粒子 + framebuffer readback），但密度过高。Pesce 的论点：一个技术效果如果不能有节制地使用，是艺术上的失败，而非技术胜利。

**2. Specular 过强 + Specular Aliasing**
几乎所有表面的高光都被拉满。更深的问题是缺乏 specular occlusion：没有遮挡的 cubemap 反射在室内光照中造成"deferred flatness"。Pesce 的核心论断：

> 如果你对某个光照或 BRDF 项没有 occlusion 来源，宁可不渲染那一项，或者做得很克制。

Planar reflection 在缺少 occlusion 的情况下尤为突出，建议"做不好就别做，扫进地毯"。

**3. 角色脸部着色**
SSS 效果做得有克制（避免了"蜡像感"），但缺少高频 specular 细节，normalmap 压缩可能造成低频失真（Pesce 猜测类似 L.A.Noire 的采集数据压缩问题）。

### 主要亮点

- **纹理质量**：几乎看不出 tiling，材质变化自然，推测使用了 distortion/blending tricks 隐藏拼接
- **SSAO 调校**：大半径 + 不随机化取样，避免了描边感；Pesce 倡导对非动态阴影的灯光使用方向性 AO
- **粒子与破坏**：小型实例物体的光照天然正确；布料/纸张/灰尘等"活动元素"极大地提升了世界的生动感
- **DOF**：sprite-based DOF（compute + append buffer），near plane bleeding 几乎不可见；bokeh 形状选择"catadioptric lens"被认为是艺术声明多于技术需求
- **Thin-wire AA**：Pesce 猜测存在，用于防止细杆和树枝 shimmer，但无法确认

## 方法论价值

文章展示了一种"渲染逆向工程"的工作方式：不使用 PIX/RenderDoc，只凭视觉观察推断实现路径，并注明哪些是猜测。这种方法的局限性（可能全错）和价值（训练渲染感知）是 Pesce 本人反复强调的。他写道他对所有主要作品都做类似的分析，通常不公开。

## 相关

- [[deferred-rendering]]
- [[ground-truth-ambient-occlusion]]
- [[pbr-practice]]
- [[specular-aliasing]]
- [[debug-visualization]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-bf4-graphics-review]]
