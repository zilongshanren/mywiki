---
tags: [source, 渲染, 帧分析, aaa]
date: 2026-04-14
sources: 1
---

# The Rendering of Rise of the Tomb Raider（Emilio López Ros）

[[emilio-lopez-ros|Emilio López Ros]] 2018 年末发表的长篇帧分析，用 RenderDoc 1.2 抓取 Rise of the Tomb Raider（Crystal Dynamics，2015）的 DX12 版本一帧，把 Foundation 引擎一个夜景 frame 从头到尾拆开——从 depth pre-pass 到最后的 UI composite，几乎覆盖了一个现代 AAA 延迟渲染管线的全部模块。是了解工业界如何把一个 30ms 预算塞满各种 trick 的稀有窗口。

## 摘要

文章从**100 绘图调用的 depth pre-pass**开始讲 [[early-z-late-z|Early-Z]] 的实际收益（某山景像素数从 104k 减到 23k，77% 节省）。然后进入 Foundation 引擎最不一样的选择——它不是传统 [[deferred-rendering]]，而是 [[tiled-light-prepass]]：仅写 normal + glossiness + metallic bit 的薄 pass，先算出 diffuse/specular/ambient 三张光照图，再**第二次**提交几何体做材质合成。同时讲解了 DX12 下的多线程 command list 录制（7 个 color pass、各 100–200 drawcalls）。

接着是**阴影 atlas**（16384×8196 16-bit，容纳 8 张 shadow map，多 light 源复用）、**[[hbao-interleaved-sampling|HBAO+ 的 4×4 interleaved sampling]]**、**[[depth-aware-upsampling|stencil 驱动的 depth-aware upsampling]]**、**[[volumetric-fog-froxels|froxel 体积雾]]**（40×23×16 光源 grid + 160×90×64 光贡献 volume）、**PureHair 的 7-buffer 流水线**（TressFX 续作）、**Reinhard photographic tonemapping + log average luminance**、**7 compute shader 的 bloom 链**、以及 SSR、反射、motion blur 的实现。

文章同时记录了若干**值得单独学习的 trick**：[[fizzle-lod-fading|fizzle LOD fading]] 而非 alpha blending、snow deformation 的 compute 流水线（GPU Pro 7 详述）、linear space UI 渲染（因为 UI 是 3D-like 的），以及 FP32→FP16 在 group shared memory 中的带宽优化。

## 关键要点

- **光照方案**：tiled light prepass 不是 tiled deferred——thin G-Buffer + 二次几何提交，省带宽费绘图
- **多次几何复用**：pre-pass 用 ~100 drawcalls 换 77% 像素着色节省，stencil 分类让 upsample 分支只付自己的钱
- **屏幕切 tile**：光源用 16×16 tile 做 culling，volumetric 用 40×23×16 做粗 culling
- **体积雾的 froxel 流水线**：compute 收集光、blur、front-to-back 累积——per-pixel 只付 16 条指令
- **Interleaved HBAO**：把 32-sample 的 AO 按 4×4 空间交织成 16 个独立计算，再 blur 合并——等效 512 sample 但 cache 友好
- **stencil discard trick**：same pattern 复用于 ambient lighting、particles、motion blur 的 upsampling
- **log average luminance**：compute shader 分 tile 聚合 log 亮度，再做 pyramid reduce——几乎无中间 buffer
- **FXAA only**：ROTR 没有 TAA，用 FXAA + 可选 SSAA。作者明确提到 TAA 正在成为 AAA 标配（这篇文章在 2018 年底）
- **光照格式选择**：三张 RGBA16F 而非 R11G11B10F，因为 alpha 通道有额外信息占用

## 链接到的概念

- [[tiled-light-prepass]]
- [[hbao-interleaved-sampling]]
- [[depth-aware-upsampling]]
- [[fizzle-lod-fading]]
- [[volumetric-fog-froxels]]
- [[deferred-rendering]]
- [[early-z-late-z]]
- [[stencil-buffer]]
- [[emilio-lopez-ros]]

## 原文

- 链接：https://www.elopezr.com/the-rendering-of-rise-of-the-tomb-raider/
- 本地：`raw/articles/elopezr.com/2018-12-31_the-rendering-of-rise-of-the-tomb-raider.md`
