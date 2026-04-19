---
tags: [人物, 作者, 渲染, 全局光照, 研究]
date: 2026-04-19
sources: 2
---

# Alexander Sannikov

**Alexander Sannikov**，**Grinding Gear Games**（新西兰，《流放之路 Path of Exile》开发商）资深图形程序员。2023-2024 年提出 **[[radiance-cascades|Radiance Cascades]]** 全局光照算法，是这一波 2D/3D 实时 GI 研究里最具标志性的名字——把朴素的"cast N random rays"从 **per-pixel 随机** 变成 **结构化级联 + bilinear merge**，引发了 Graphics Programming Discord 和 shadertoy 社区的连锁创作潮。

## 贡献

- **[[penumbra-hypothesis|半影假设]]**：阴影半影需要的 linear 分辨率与 angular 分辨率**反比**——近光源要多探针少方向、远光源要少探针多方向。这个直觉虽然朴素，但此前没有被变成算法。
- **Radiance Cascades 算法**：把半影假设落地为级联纹理数据结构 + bilinear merge。相邻级联空间 1/4、角度 4×；合并时用 bilinear 插值把**有限方向**转换为**连续方向采样**，得到无噪声 GI。
- **Path of Exile 2 渲染**：传闻 RC 会进入 PoE 2 的实时照明管线，是该算法少见的 production 证据（截至 2024）。

## 影响

RC 在 2024 年是 Graphics Programming Discord 最活跃的讨论主题之一。衍生作品包括：

- **Yaazarai**（[[alex-yaazarai]]）的两部分 GameMaker 教程，把算法传到 GM 社区。
- **Mytino** 的 voxel + 物理派生实现（把 RC 扩到 3D）。
- **Fad** 的 shadertoy 带 skybox 积分的变体。
- **tmpvar** 的 interactive playground（可拖拽探针感受 linear/angular 反比）。

## 风格

他的原论文没有走标准 SIGGRAPH 渠道，直接在 Discord 社区和 arXiv 上传播。这种"非学术、非工业"的发表路径——先开源 + 演示 + 社区迭代——在现代图形程序圈越来越常见，是 shadertoy 文化进一步外扩的结果。

## 相关

- [[radiance-cascades]]
- [[penumbra-hypothesis]]
- [[alex-yaazarai]]
- [[instant-radiosity-vpl]] —— 一种早期的替代 GI 方案

## Sources

- [[sources/yaazarai-radiance-cascades]]
- [[sources/yaazarai-radiance-cascades-2]]
