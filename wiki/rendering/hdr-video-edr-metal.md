---
tags: [hdr, edr, 视频, 色彩管理, metal, apple]
date: 2026-04-19
sources: 1
---

# HDR 视频与 EDR on Metal

苹果平台上把 HDR 视频渲染到屏幕不只是解码问题——还涉及**色彩管理 + 自适应 tonemapping + 当前屏幕能力感知**。EDR（Extended Dynamic Range）是 Apple 平台用来做这件事的抽象层：它不是一种格式，而是一套告诉系统"我的内容有超过 SDR reference white 的亮度，请根据屏幕能力自适应呈现"的合约。[[warren-moore|Warren Moore]] 2025 年写过完整管线教程。

## 核心概念

- **SDR reference white** ≈ 100 nits，EDR 值 1.0
- **EDR headroom**：当前屏幕能显示的最大值与 reference white 的比例。随屏幕亮度 / 环境光 / 用户调节实时变化
  - macOS：`NSScreen.maximumExtendedDynamicRangeColorComponentValue`
  - iOS：`UIScreen.currentEDRHeadroom`
- **EDR 值 > 1.0** 表示超过 reference white 的亮度（高光、光源）
- **HDR 格式**的两条常见 transfer function：
  - **HLG（Hybrid Log-Gamma）**：向下兼容 SDR（piecewise、前半段等于 SDR transfer function）
  - **PQ（Perceptual Quantizer）**：不兼容 SDR，被 HDR10 / Dolby Vision 使用
- **色域**：HDR 视频常见 Rec. 2020（远大于 sRGB 和 P3）

## Metal 层的三件套

```swift
metalLayer.wantsExtendedDynamicRangeContent = true
metalLayer.colorspace = CGColorSpace(name: .extendedLinearITUR_2020)
metalLayer.pixelFormat = .rgba16Float
```

三个都必须。缺 `wantsExtendedDynamicRangeContent` 值会被 clip；缺 extended linear color space 值会被 gamma 压；缺 `.rgba16Float` 无法存储超 1.0 值。

## AVFoundation → Metal 管线

1. `AVURLAsset(url:)` → `AVPlayerItem(asset:)` → `AVPlayer(playerItem:)`
2. 挂 `AVPlayerItemVideoOutput`，`outputSettings` 里声明：
   - `AVVideoColorPrimaries_ITU_R_2020`
   - `AVVideoTransferFunction_Linear` —— 让 AVFoundation 代解 HLG/PQ 到线性
   - `AVVideoYCbCrMatrix_ITU_R_2020`
   - `AVVideoAllowWideColorKey: true`
   - `kCVPixelFormatType_64RGBAHalf`
3. 播放循环里 `videoOutput.copyPixelBuffer(forItemTime:)` 拿 `CVPixelBuffer`
4. `CVMetalTextureCache` 做零拷贝 `CVPixelBuffer` → Metal texture。**Swift 里必须在 command buffer completion handler 里保活 `CVMetalTexture`**，否则 cache 会回收下层资源

## 两条 tonemapping 路径

### EDR 自动 tonemapping（上屏）

从 `CVPixelBuffer` attachment 抽元数据：

- HLG：`kCVImageBufferAmbientViewingEnvironmentKey`
- HDR10：`kCVImageBufferMasteringDisplayColorVolumeKey` + `kCVImageBufferContentLightLevelInfoKey`

构 `CAEDRMetadata.hlg(...)` 或 `.hdr10(displayInfo:contentInfo:opticalOutputScale:)`（scale 通常 100.0）赋给 `metalLayer.edrMetadata`，系统按当前 headroom 做 mapping。

### Shader 手写 tonemapping（离屏 / 自定义 pipeline）

WWDC21 "Explore HDR with EDR" 说过"AVFoundation 不把 HDR 格式解到 EDR"——意思是 pixel buffer 里的值并非"最适合当前屏幕"的 EDR 值，只有 layer EDR tonemapping 打开后系统做这步。离屏场景要手写：

**PQ EOTF** 把非线性 PQ → 绝对亮度（nits，BT.2100 公式）：

```hlsl
float3 eotf_pq(float3 x) {
    float c1 = 107/128.0, c2 = 2413/128.0, c3 = 2392/128.0;
    float m1 = 1305/8192.0, m2 = 2523/32.0;
    float3 p = pow(x, 1.0/m2);
    return 10000.0 * pow(max(p - c1, 0.0) / (c2 - c3 * p), 1.0/m1);
}
```

**HLG inverse OETF + OOTF**（piecewise，因为 HLG 是 SDR 兼容）：

```hlsl
float inv_oetf_hlg(float v) {
    float a = 0.17883277;
    float b = 1.0 - 4*a;
    float c = 0.5 - a * log(4*a);
    return v <= 0.5 ? v*v/3.0 : (exp((v-c)/a) + b) / 12.0;
}
float3 ootf_hlg(float3 Y, float Lw) {
    float gamma = 1.2 + 0.42 * log10(Lw / 1000.0);
    return pow(Y, gamma - 1.0) * Y;
}
```

**Max-RGB Reinhard**（Reinhard 2002 + Burke 2020）避免 per-channel scale 漂色：

```hlsl
float3 tonemap_maxrgb(float3 x, float maxIn, float maxOut) {
    if (maxIn <= maxOut) return x;
    float a = maxOut / (maxIn * maxIn);
    float b = 1.0 / maxOut;
    float cmax = max(x.r, max(x.g, x.b));
    return x * (1 + a * cmax) / (1 + b * cmax);
}
```

组合成 `tonemap_pq(x, edrHeadroom)` / `tonemap_hlg(x, edrHeadroom)`。

## 易错点

- 没有元数据时给 `CAEDRMetadata` 赋一个合理默认，避免极亮 highlight 被下游 clip
- tvOS 没有 `wantsExtendedDynamicRangeContent`；新 `CALayer.preferredDynamicRange` 可能可用（未广泛验证）
- `CVMetalTexture` 生命期管理错会让 cache 资源提前回收，画面出怪

## 相关
- [[color-space]]
- [[local-tonemapping]]
- [[metal-api-overview]]
- [[cametal-layer-drawable]]
- [[gamma-correction-srgb]]
- [[warren-moore]]
- [[sources/wolfgang-engel-hdr10-tv-setup]] —— 2017 年关于 HDR10 TV 用户端校准复杂度的早期观察

## Sources

- [[sources/metalbyexample-hdr-video]]
