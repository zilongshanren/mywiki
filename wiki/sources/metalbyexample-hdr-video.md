---
tags: [source, metal, hdr, 视频, edr, 色彩管理]
date: 2026-04-19
sources: 1
---

# Rendering HDR Video with AVFoundation and Metal（Warren Moore / Metal by Example）

[[warren-moore|Warren Moore]] 发表于 2025 年 3 月 10 日，从 AVFoundation 解码到 Metal 渲染的完整 HDR 视频播放管线，附 GitHub 可运行样例。涵盖 EDR 语义、PQ/HLG 解码、tonemapping、色彩空间链条——苹果平台上做 HDR 图像工作流的最接近"完整教程"的参考文。

## 摘要

核心概念拆分：

- **HDR**：相对 SDR（~100 nits reference white）的高动态范围信号
- **EDR（Extended Dynamic Range）**：不是格式，是苹果平台上一套**自适应色彩管理系统**。给它 EDR 值就能根据当前屏幕亮度、环境光、设备能力（从 100 nits SDR 到 1600 nits Pro Display XDR）自动调整；"headroom" 是当前能显示的最亮值与 reference white（EDR 值 1.0）的比例
- **色彩空间**：gamut（白点 + 原色）+ transfer function。sRGB gamut 覆盖人眼 <40%，extended 色空间允许分量超出 [0,1]。P3 / Rec.2020 是 HDR 视频主力 gamut；transfer function HLG（向下兼容 SDR）vs PQ（HDR10 / Dolby Vision 用）

管线：

1. `AVURLAsset(url:)` → `AVPlayerItem` → `AVPlayer.play()`，音频能响但没画面
2. `AVPlayerItemVideoOutput` 从 player item 拿 pixel buffer。关键是 `outputSettings` dict 里声明：`AVVideoColorPrimaries_ITU_R_2020` + `AVVideoTransferFunction_Linear` + `AVVideoYCbCrMatrix_ITU_R_2020` + `AVVideoAllowWideColorKey: true` + `kCVPixelFormatType_64RGBAHalf`（匹配 Metal 的 `.rgba16Float`）。`AVVideoAllowWideColorKey` + transfer function 选 Linear 意味着 AVFoundation **会替你解码 PQ/HLG 到线性 Rec.2020**（若选 EDR 路径），若要自己解码则换策略
3. `CVMetalTextureCache` 把 `CVPixelBuffer` 零拷贝变成 Metal texture。注意 `CVMetalTexture` 对象必须在 GPU 用完前保活，Swift 里在 command buffer completion handler 里释放
4. Metal layer 设置三件套：`wantsExtendedDynamicRangeContent = true`、`colorspace = extendedLinearITUR_2020`、`pixelFormat = .rgba16Float`

两条 tonemapping 路径：

- **EDR 自动 tonemapping**：从 pixel buffer attachment 里抽 HLG/HDR10 元数据（`kCVImageBufferAmbientViewingEnvironmentKey` / `kCVImageBufferMasteringDisplayColorVolumeKey` / `kCVImageBufferContentLightLevelInfoKey`），构 `CAEDRMetadata.hdr10(...)` 或 `.hlg(...)` 赋给 layer.edrMetadata。系统据此 + 当前屏幕能力做 mapping
- **自己写 shader tonemapping**（离屏渲染 / 自定义 pipeline 场景）：
  - PQ EOTF 把非线性 PQ 信号解成绝对亮度（nits，公式出自 BT.2100）
  - HLG 走 inverse OETF + OOTF（HLG 是 SDR 兼容 piecewise function）
  - 统一到 linear Rec.2020 后应用 **max-RGB Reinhard**（Reinhard et al. 2002 + Burke et al. 2020 的 per-component max 改良）：`x * (1 + a * maxRGB) / (1 + b * maxRGB)`，`a = maxOutput/maxInput²`、`b = 1/maxOutput`
  - EDR headroom 在 macOS 查 `NSScreen.maximumExtendedDynamicRangeColorComponentValue`、iOS 查 `UIScreen.currentEDRHeadroom`

一个容易忽略的工程点：WWDC21 "Explore HDR with EDR" 说"AVFoundation 不把 HDR 格式解到 EDR"——意思是 `CVPixelBuffer` 里的值并非自动映射成"最适合当前屏幕"的 EDR 值，只有 layer 启用 EDR tonemapping 后系统才做这步；离屏渲染要自己做 tonemapping，否则 highlights 会被下游 clip。

样例代码在 [metal-by-example/metal-hdr-video](https://github.com/metal-by-example/metal-hdr-video)。

## 关键要点

- EDR 是自适应 HDR 管理系统，不是格式；headroom 随屏幕 / 环境 / 用户亮度变化
- HDR 视频管线三件套：Metal layer `wantsExtendedDynamicRangeContent` + `extendedLinearITUR_2020` + `.rgba16Float`
- `CVMetalTextureCache` 是 CVPixelBuffer → Metal texture 零拷贝桥
- `AVPlayerItemVideoOutput` 的 `outputSettings` 决定色彩空间和像素格式，选 Linear transfer 让 AVFoundation 代解 PQ/HLG
- EDR 自动 tonemapping 靠 CAEDRMetadata + pixel buffer attachment（ambient viewing / mastering display / content light level）
- 离屏场景必须自己写 tonemapping shader：PQ EOTF 或 HLG inverse OETF+OOTF 到 linear，再 max-RGB Reinhard
- EDR headroom：macOS `NSScreen.maximumExtendedDynamicRangeColorComponentValue` / iOS `UIScreen.currentEDRHeadroom`
- tvOS 没有 `wantsExtendedDynamicRangeContent`，iOS 26+ 可能走 `CALayer.preferredDynamicRange`（作者未实测）

## 链接到的概念

- [[hdr-video-edr-metal]]
- [[color-space]]
- [[local-tonemapping]]
- [[metal-api-overview]]
- [[cametal-layer-drawable]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/hdr-video/
- 本地：`raw/articles/metalbyexample.com/2025-03-10_rendering-hdr-video-with-avfoundation-and-metal.md`
