---
tags: [渲染, 纹理, ptex, gpu, 流送, 缓存, hyperion]
date: 2026-04-19
sources: 1
---

# Ptex 与 GPU 纹理流送

**Ptex**（Burley & Lacewell 2008）是 Disney Animation 的 per-face 纹理格式——每个 mesh face 独立存一张小纹理，省掉 UV unwrap。Disney Animation 管线 100% 以 Ptex 为纹理工作流基础。把这套东西搬到 GPU 做实时路径追踪预览，是 SIGGRAPH 2025 talk *A Texture Streaming Pipeline for Real-Time GPU Ray Tracing*（Lee, Zeichner & Li 2025）的主题。

## 设计约束

- **文件量级**：一部影片 tens of thousands 个 Ptex 文件。
- **目标体验**：零停顿、无 hitch，即使 GPU cache 被强制清空。
- **不依赖硬件纹理**：实现在 CUDA 里做，绕开 OpenGL/DX 的硬件 texturing，以原始内存块直接管理每个 face。
- **无预处理**：不做离线 atlas 或 MIP 预构建，CPU 侧 Ptex 数据原样流送。
- **小 GPU cache + 激进 LRU**：总显存占用很小，命中 cap 就用快速 LRU 驱逐。

## 为何不用 atlas

早期尝试（Kim et al. 2011、Pixar RTP）把 per-face 纹理 pack 成巨型 atlas，但：

- 相邻 atlas 位置在 mesh 拓扑上并不相邻，滤波时会跨 face 漏色。
- MIP 生成会把完全不相关的几何区域混进去。

Disney 新系统流送的是原始 Ptex face 数据，和 CPU 侧用的数据一模一样，彻底回避这个问题。

## 两个一代系统的教训

- **Joe Schutte 的 GPU Ptex 原型**：引入了 [cuckoo hash](https://en.wikipedia.org/wiki/Cuckoo_hashing)（Erlingsson 2006）做 key 查找，这个选择被二代沿用。
- **Moonray 的滤波经验**（Mark Lee 在 Lee et al. 2017 *Vectorized Production Path Tracing*）：Ptex 的跨 face 滤波巨难。结论是——在随机路径追踪里，**「点采样 + 两层 MIP 线性插值」已经够好**，不用真的跨 face 做各向异性滤波。Yining Karl Li 在 2018 年的博客也独立得到了同一结论。
- **Mythical Man-Month 第 11 章**：「Plan to throw one away, you will anyway」——二代写出来的系统比原型更紧凑更健壮，也印证了重建的价值。

## 打破的通行假设

- **「Ptex 在非相干访问下会慢」**：其实不是 Ptex 本身的属性，只是 Hyperion 的 sorted deferred shading（[[wavefront-path-tracing]]）刚好让 Ptex 读取相干，这使大家误以为 Ptex 一定需要相干。PBRT 的 Ptex 集成（Pharr 2018, Moana Island）其实也证伪过。
- **Disney 的 GPU 预览用 depth-first integrator**，二次 bounce 的 Ptex 访问完全非相干，照样能在多次反弹下保持交互帧率。

## 相关

- [[hyperion-renderer]]
- [[wavefront-path-tracing]]
- [[mipmap-generation-sampling]]
- [[yining-karl-li]]

## Sources

- [[sources/yiningkarlli-texture-streaming-siggraph2025]]
