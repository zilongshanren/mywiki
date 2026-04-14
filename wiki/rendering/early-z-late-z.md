---
tags: [渲染, 优化, 深度缓冲]
date: 2026-04-05
sources: 1
---

# Early-Z vs Late-Z

**Z-test 在 fragment shader 之前（Early-Z）还是之后（Late-Z）执行**，决定被遮挡 fragment 是否浪费 shader 执行。

## Early-Z

在 fragment shader **之前**做 depth test：被遮挡的 fragment **不执行 shader**——节省大量计算。是默认行为。

## Late-Z

Depth test 在 fragment shader **之后**：必须先执行 shader 才知道最终深度。性能显著下降。

## 什么破坏 Early-Z

- **`discard` / alpha test**：shader 可能拒绝 fragment，必须先跑。
- **写入 `gl_FragDepth`**：fragment shader 可能改变深度。
- **Alpha-to-Coverage**：最终覆盖取决于 shader 输出。

## HSR vs Early-Z

TBDR 在 tile 粒度上做的 **HSR（Hidden Surface Removal）**比 Early-Z 更激进——能完全消除 tile 内 overdraw，前提是没有破坏因素。详见 [[hsr-tbdr]]。

## 实践建议

- **从前往后**渲染不透明物体：大幅提升 Early-Z 效率。
- **Depth Pre-Pass**：先只写 Z（空 fragment shader），再渲染：强制所有后续 fragment 都能 Early-Z 剔除。
- **避免无谓 discard**：用不透明材质替代 alpha test（或用 Alpha-to-Coverage + MSAA）。

## 相关

- [[z-buffer]]
- [[hsr-tbdr]]
- [[overdraw]]
- [[fragment-shader]]
- [[fizzle-lod-fading]] —— 用 discard 保留 early-z 能力、避免 alpha blending 的工程选择
- [[depth-aware-upsampling]] —— 用 stencil 提前分类像素、再用 early stencil discard 分派 simple/complex shader
- [[conservative-depth]] —— `SV_DepthGreaterEqual` / `[earlydepthstencil]` 两条 Early-Z 救援通道

## Sources

- [[sources/rtr-day05]]
- [[sources/interplay-depth-testing]] —— Anagnostou 的 D3D11 depth testing 阶段与 Conservative Depth / `[earlydepthstencil]` 整理
