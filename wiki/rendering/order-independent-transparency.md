---
tags: [rendering, transparency, oit, compute]
date: 2026-04-19
sources: 1
---

# 顺序无关透明（OIT）

OIT（Order-Independent Transparency）指不依赖几何体提交顺序即可得到正确合成结果的半透明渲染方案。Supnik 在 2011 年考察 AMD HD5800 系列的实时 OIT 演示时，最初期待的是「`glEnable(GL_MAGIC_OIT_EXT)` 即开即用」式 API，但实际的硬件实现要求**应用层重写后端**：片元不再直接写入 framebuffer，而是通过 compute-shader 风格的原子操作，写入一张「深」framebuffer——每个像素位置维护一条链表的表头，全部片元落在一个通用存储里；随后用一个后处理 pass 遍历每个像素的链表（bucket），在 GPU 上对该像素的所有片元深度排序再合成。

这种 per-pixel linked-list OIT 的代价有两方面：一是需要 GLSL 里暴露 atomic counter 等 compute 能力；二是原本依赖标准光栅后端的老应用很难平滑迁移。Supnik 因此列出了备选路径：depth peeling（逐 pass 剥离离视点最近的一层）、以及更激进的「累加+平均」blend 替代——这些不追求绝对正确，但可以无痛嵌入现有 OpenGL 管线。对于 X-Plane 这种半透明面覆盖稀薄（典型场景是机舱窗户）的应用，他最终更倾向于 [[triangle-plane-sort-translucency]] 这样的拓扑预排序，而非付出硬件 OIT 的改造代价。

更广阔的 OIT 研究还有 weighted blended OIT、moment-based OIT（参见 [[moment-shadow-mapping]] 的矩方法思想在透明域的变体）等近似法；而要彻底摆脱顺序依赖又接受更高带宽，per-pixel linked-list 仍是参照系。

## Sources

- [[sources/supnik-order-correct-translucency]]
