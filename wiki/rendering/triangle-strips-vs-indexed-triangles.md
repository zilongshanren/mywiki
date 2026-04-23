---
tags: [opengl, mesh, draw-call, vertex-buffer]
date: 2026-04-19
sources: 1
---

# 三角带 vs 索引三角形

在 2000 年前后，triangle strip（`GL_TRIANGLE_STRIP`）是画连续 mesh 的「最佳实践」：一条长度为 N 的带子只要 `N+2` 个顶点，而独立三角形需要 `3N` 个，vertex 数量直接缩水 66%。几何吞吐通常受顶点数限制，这是巨大的胜利。于是一代教程把「先尽量组 strip、剩下的用 free triangle」写成定式。

但到了索引化（`glDrawElements`）成为主流之后，Supnik 在 X-Plane 里得出一个反直觉的结论：**桌面 OpenGL 应用应该全部使用 indexed triangles，放弃 strip**。推导只需要几步算术：

**第一步，索引几乎总是值得开。** X-Plane 的顶点是 32 字节（XYZ + normal + 一组 UV，全 float），索引 4 字节——顶点比索引贵 8 倍。只要共享的顶点占比超过 1/8，indexed 就是纯赚。对于一个 2D 网格，相邻 strip 共享整条边，索引化带来的节省接近 2×，碾压索引本身的开销。绝大多数由建模师搭出来的网格属于这一类。

**第二步，一旦用了索引，strip 的光环就黯淡了。** 未索引时 strip 把**几何（顶点）**压到 1/3；索引时 strip 只把**索引列表**压到 1/3。在 X-Plane 的 32:4 比例下，这份节省只有当初的 1/8 重要。

**第三步，重启 primitive 会吃掉剩余那点好处。** 真实 mesh 里 strip 往往很短，要么对每条 strip 发一次 `glDrawElements`（CPU 侧 draw call 暴涨），要么依赖 `glMultiDrawElements` 或 `NV_primitive_restart`——前者驱动可能偷偷拆回独立调用，后者早年只 NVidia 支持，且每次 restart 还要占一个额外索引。**为了压一份放在 VRAM 里的 index buffer 而增加 CPU→GL 调用，是典型的方向搞反**。CPU 调用远比 index buffer 体积昂贵。

结论简单粗暴：任何有共享顶点的 mesh，X-Plane 都走 indexed triangles，整块 mesh 一次 `glDrawElements` 画完。代价是稍大的 index list，换来：单一代码路径、不依赖 multi-draw / restart 扩展、strip 化效果差的 mesh 也能跑满速。

**例外要认清**：`GL_POINTS`、每株都是独立 quad 的「树」这类几何完全无共享——此时索引是纯开销，关掉。嵌入式/移动端也要另算：PowerVR MBX（iPhone 1 代所用 ES 1.1 核心）是 tile-based renderer，分桶时把几何存成 native strip，**strip-order 的索引网格**能大幅提升；SGX 以后几何吞吐充裕，这个约束才松绑。这也是为什么 X-Plane 的 DSF scenery tool 仍会用 `tri_stripper` 生成 strip——只不过桌面端加载时又把它还原成 free triangles 再做索引化。

两条桌面 OpenGL 的可操作启发：

- **所有共享顶点的 mesh → indexed triangles**，一次 draw call 画完。参见 [[draw-call]]、[[opengl-draw-call-batching-sweet-spot]]。
- **不要为了节省 VRAM 里的 index buffer 去增加 CPU draw call**——优化应针对被流水线真实瓶颈住的资源。

## Sources

- [[sources/supnik-to-strip-or-not-to-strip]]
