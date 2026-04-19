---
tags: [shader, toon, outline, post-process, urp, edge-detection]
date: 2026-04-19
sources: 1
---

# Toon 风格描边的六种算法

描边（outline）是 toon / cel shading 体系的必备补件——没有一圈清晰的轮廓，硬阶梯色块的视觉就不闭合。但"怎么画描边"历史上至少有**六种互不兼容**的算法，各有各的适用场景、性能开销和视觉取舍。[[daniel-ilett|Daniel Ilett]] 的 *Toon Shaders Pro for URP* 把这六种做成一个后处理 Feature 的 **Outline Type** 下拉，是目前 wiki 里见过最完整的一次并排陈列。

## 六种算法概览

| 算法 | 信号源 | 实现范式 | 典型用途 |
|---|---|---|---|
| 1. **Depth Normal Color Outlines** | `_CameraDepthTexture` + `_CameraNormalsTexture` + 颜色 | 全屏 fragment，梯度检测（Sobel/Roberts 类） | 屏幕空间通用描边，不挑 mesh |
| 2. **High Quality Masked Object Outlines** | 自定义 layer 的 object mask RT | 额外渲染 pass 产 mask → 全屏 edge detect → 可变厚度 | 特定物体组"被描边"，最灵活 |
| 3. **Pixel Width Masked Object Outlines** | 同上 | 同上但算法简化成 1px 硬边 | mask 方案但成本最低的一档 |
| 4. **Hull Outlines (Inverted Hull)** | mesh 几何本身 | 第二次渲染 mesh，沿法线外推、反转 culling | 每个物体独立一圈、PS2 风 |
| 5. **Debug Outline Mask** | 同 2 | 直接输出 mask 本身 | 调试用，看哪些物体被选中 |
| 6. **No Outlines** | — | — | 占位关闭 |

选哪种取决于三个问题：描边是"全场景通吃"还是"只给主角"？需不需要可变厚度和距离淡出？可以接受多画一次 mesh（inverted hull）吗？

## 1. Depth Normal Color Outlines —— 屏幕空间梯度

全屏 post-process：对每个像素用 Sobel 式核采周围几个样，独立计算 **color 梯度** / **depth 梯度** / **normal 梯度**，每种给一对 (sensitivity, strength) 参数，最后加权组合成描边强度。再加一个 **Depth Threshold**——比这个深度更远的像素直接不检测（防止天空 / 远景被误判）。

**优势**：不需要额外 Pass、对场景所有物体同等生效、不依赖 mesh 是 manifold。
**劣势**：厚度 = 1 像素（采样半径扩大可得粗边但会模糊）、"平面同色"区域不出边（需要法线差异配合）。
和 [[sources/danielilett-snapshot2-outline]] 是同一思路，参数化更细。

## 2–3. Masked Object Outlines —— 挑物体的屏幕空间方案

单独建一张 mask RT：用 URP Renderer Feature ([[urp-render-objects-feature|Render Objects]] 变体) 把 `Object Mask` 指定 layer 的物体以**简化材质**画进去——可以按 mesh 外缘、按每个三角形、按所有物体的集体并集、或按顶点色分区四种模式。再对 mask 跑 edge detection。

**Masked Outline Thickness**：kernel 半径，粗细可控但线性影响成本。**Masked Outline Smoothing**：远处采样贡献降低，伪平滑。**Outline Draw Sides**：描边画在 mask 内侧（物体内）、外侧（物体外）、或两侧都画（总厚度翻倍）。**Fade Start/End**：按与相机距离淡出，远处物体描边逐渐消失。**Mask Ignore Depth**：不做深度测试直接画 mask——描边会穿墙看见（标记 off-screen 敌人的透视视效）。

**High Quality** 版支持这一整套参数；**Pixel Width** 版裁剪成"1 像素硬边"——成本最低但只能给次要物体用。

- **Light Modes 选项**决定哪些 shader 进 mask：`UniversalForwardOnly`（Ilett 的 Toon shader 标这个 tag）、`UniversalForward`（URP Lit）、`SRPDefaultUnlit`、`UniversalGBuffer`。用户需要了解自己 shader 的 tag 才能把它选进 mask。

## 4. Hull Outlines —— 几何方案

[[cel-shader-outline|经典 inverted hull]]——每个 mesh 用第二 material 再画一次，反转面朝向 + 沿顶点法线外推一点点。从侧面看只有背面的"膨胀壳"露出在原 mesh 外缘，形成一圈描边。

**优势**：描边随物体动而不是屏幕梯度——不会有"同平面被误判"问题；每物体独立厚度；不需要 depth/normals texture。
**劣势**：每画一个物体多一 draw call；manifold mesh 要求严格（非 manifold 会出裂缝）；对透明物体的排序有干扰。

Ilett 版额外暴露的参数：
- **Outline Thickness**（沿法线外推距离）。
- **Outline Transparency**：外推 mesh 是否画成半透明（改变渲染顺序）。
- **Outline Lighting**：给描边本身应用 diffuse shading——背光的描边暗下去；配合 **Flip Outline Direction** 可倒转受光方向（迎光暗、背光亮）。
- **Outline Min Lighting**：受光最低值兜底，避免全黑。

作者注：这种风格更像 PS2（Borderlands）而非 PS1——PS1 很少用 inverted hull。

## 挑选框架

```
需要的是……
├── 全屏、不管物体？             → Depth Normal Color Outlines
├── 只有主角 / 特定层？            → Masked Object Outlines (HQ 或 Pixel)
├── 每物体独立、能接受多 1 次 draw？ → Hull Outlines
└── 想看 mask 选中了谁？           → Debug Outline Mask
```

实际项目常**组合两种**——例如主角用 Hull Outlines（清晰、独立）+ 场景整体用 Depth Normal（统一风格），通过两个 Renderer Feature 叠加。

## Render Pass Event 的取舍

Outline feature 暴露 **Render Pass Event**：before URP 内置 post（color grading / bloom）或 after。

- **Before**：描边会被 bloom 扩散、被 color grading 调色 → 柔和、和场景融入的手绘感。
- **After**：描边保持原本指定颜色 → 锐利、漫画感。

## 相关

- [[cel-shader-outline]] —— Inverted Hull + Stencil 的经典 shader 版
- [[cel-shading-pipeline]] —— 描边在完整 toon 管线里的位置
- [[sobel-edge-detection]] —— Depth Normal Outlines 的数学基础
- [[depth-texture-silhouette]] —— depth 通道的基础
- [[urp-render-objects-feature]] —— Masked 方案的底层 pass
- [[stencil-buffer]]

## Sources
- [[sources/danielilett-toon-shaders-pro-outline-post]]
- [[sources/danielilett-snapshot-pro-outline-sobel]] —— Snapshot Pro 单路 color Sobel 档（Toon Pro 的前身雏形）
- [[sources/danielilett-snapshot-pro-outlines-fancy]] —— Snapshot Pro 三通道 Sobel 档，等同 Toon Pro 的 Depth Normal Color Outlines
