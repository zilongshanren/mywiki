---
tags: [source, 渲染, 抗锯齿, temporal]
date: 2026-04-14
sources: 1
---

# Temporal AA and the Quest for the Holy Trail（Emilio López Ros）

[[emilio-lopez-ros|Emilio López Ros]] 2022 年初发表的长篇 TAA tutorial。作者明确说是「写给未来的自己」的技术 deep-dive——用 Matt Pettineo 的 MSAAFilter demo 一步一步展示每个阶段的输入输出，从最朴素的 accumulation buffer 开始，每发现一个 artifact 就加一层 rectification，最后到现代 AAA 水平。社区里被广泛认为是当前最好的 TAA 入门。

## 摘要

文章开头梳理 CG aliasing 的各种来源：几何边缘、alpha test、镜面高光、高频法线、parallax、SSAO/SSR 这类低分辨率效果、dithering——并解释为什么 [[msaa-ssaa|MSAA]] 只能解决一小部分，以及为什么 [[temporal-antialiasing|TAA]] 用跨帧分散计算的方式成为现代事实标准。

然后进入 TAA 流水线的每一环：

1. **Jitter**：用 quasi-random（Halton 等）序列每帧把投影矩阵偏移一个 sub-pixel——典型范围是半个像素以内
2. **最简单的 Resolve**：`output = 0.1·current + 0.9·history`，静态相机下就够了
3. **Ghosting 与 Reprojection**：相机移动后要用深度 + 逆投影 + 上一帧 VP 把 UV 投回历史 buffer
4. **Motion Vectors**：动态物体需要额外的 [[motion-vectors|velocity buffer]]，VS 算两次位置、PS 做差
5. **Disocclusion & Rectification**（文章的重头戏）：[[taa-history-rectification|color clamping / depth / stencil / velocity rejection]]——作者推荐用**速度差向量的长度**（即帧间加速度）作为 velocity 失配度量，比 dot product 或 magnitude 差都更稳定
6. **Flicker 与 Tonemap Weighing**：luminance weighing 和 log weighing 两种把 outlier 压下去的方法
7. **Blurring**：Catmull-Rom bicubic（16→9→5 samples 的优化路线）解决重建模糊
8. **Texture Blurring**：negative mip bias 或者一个很漂亮的「**unjitter UV**」trick，通过 `ddx_fine`/`ddy_fine` 反向补偿 jitter 的 UV 偏移
9. **Edge Dilation**：velocity / depth / stencil 本身是 aliased 的，需要在 3×3 邻域取「最近深度」或「最大 magnitude」的那个 sample
10. **Transparency、Camera Cuts**：最后两个特例的工程 workaround

全文的底色是「**TAA 是 tradeoff**」——作者诚恳地回应评论区「我恨 TAA」的玩家，承认它确实糊、但现代渲染的帧预算 + 物理 BRDF + 大量随机采样的组合下别无选择。

## 关键要点

- **jitter 要加到两帧的计算里**：velocity 写入时要显式减去两帧的 jitter，否则 reprojection 把 jitter 放大
- **color clamping 是保底**：无论再加什么高级 rejection，clamping 都要在。其他方法是**精化**而不是替代
- **速度差向量长度作为失配度量**：对比 dot product / magnitude 差都更稳定——是作者原创的小贡献
- **unjitter UV**：作者从 Martin Sobek 学到的小 trick，用 derivatives 在 texture space 反抵消 jitter，比 negative mip bias 副作用小
- **Catmull-Rom 重建**：TAA 保留锐度的关键。9-sample 是 UE4 版，5-sample 是 CoD 版
- **responsive AA**：UE4 给特定 VFX 提供 per-pixel 降低 history 权重的 knob，牺牲 stability 换响应
- **alpha 的痛点**：透明物体默认不写 motion vectors——要么写 blended velocity，要么放弃 history
- **camera cut 只能 hack**：fade out/in、临时回退到 FXAA、或者用更快的 convergence——都是妥协

## 链接到的概念

- [[temporal-antialiasing]]
- [[motion-vectors]]
- [[taa-history-rectification]]
- [[aliasing]]
- [[msaa-ssaa]]
- [[rasterization]]
- [[mvp-transform]]
- [[emilio-lopez-ros]]

## 原文

- 链接：https://www.elopezr.com/temporal-aa-and-the-quest-for-the-holy-trail/
- demo：https://github.com/TheRealMJP/MSAAFilter
- 本地：`raw/articles/elopezr.com/2022-01-02_temporal-aa-and-the-quest-for-the-holy-trail.md`
