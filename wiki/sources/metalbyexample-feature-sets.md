---
tags: [source, 渲染, metal, feature-set, 设备能力, 参考]
date: 2026-04-14
sources: 1
---

# Feature Sets and Capabilities（Warren Moore）

[[warren-moore|Warren Moore]] 2014 年 9 月的一篇短参考文，讲 Metal 刚在 iOS 8 GM 里加进来的 `MTLFeatureSet` 与 `MTLDevice supportsFeatureSet:` 查询——用来区分 A7（iPhone 5s / iPad Air 1）和 A8（iPhone 6）之间的 GPU 能力差异。文章篇幅不长，主要价值是标记"Metal 一开始就不是无差别的"这件事。

## 摘要

Apple 在 iOS 8 GM 给 `MTLDevice` 协议加了 `supportsFeatureSet:` 方法，对应的枚举只有两项：`MTLFeatureSet_iOS_GPUFamily1_v1`（A7，PowerVR G6430）和 `MTLFeatureSet_iOS_GPUFamily2_v1`（A8，PowerVR GX6450）。两者的差别文章归纳为两条：**color attachment 数量**（A7 最多 4 个、A8 最多 8 个，意味着 A8 可以一次 render pass 同时写 8 张纹理，对 [[deferred-rendering|deferred 渲染]] 的 G-buffer 是硬门槛）和**ASTC 纹理压缩支持**（A8 才支持 ASTC，A7 只能用 PVRTC）。文章配了一个 `MBEDeviceCapabilities` 工具类，把 `highestSupportedFeatureSet` / `maximumRenderPassColorAttachments` / `supportsASTCPixelFormats` 这几项打包成 read-only property 在 UI 上显示。最后还有一个冷知识：runtime 里 `MTLCreateDefaultSystemDevice` 在 debugger 下永远返回 `MTLDebugDevice`，脱离 debugger 才返回设备特定类如 `AGXG3Device`（A7）或 `AGXG4PDevice`（A8）——Apple 的 driver 按 SoC 代号分发。

## 关键要点

- **Metal 的 feature set 从一天起就是分层的**：`GPUFamily1/2` 对应 A7/A8——2014 年两家之间的 delta 很小，但这条 API 路径后来变得至关重要。现在 `MTLFeatureSet_iOS_GPUFamilyN` 已经扩展到 Family 9（Apple Silicon），功能差异远不止当年的两条。
- **Color attachment 上限直接决定能跑多少种渲染管线**：A7 的 4 张上限让 MRT-based deferred 只能做最小 G-buffer（albedo/normal/depth），A8 的 8 张则可以加 metallic/roughness/emissive 等扩展通道。
- **ASTC vs PVRTC** 是 A7/A8 之间的另一条分界——ASTC 支持更灵活的 block size 和质量梯度，GPU 解码免费，是 Apple 平台后来事实上的标准纹理压缩格式。
- **查询 API 的设计哲学**：不是"问 GPU 硬件型号"，而是"问能不能做 X"——这让 app 可以对 future hardware 自然兼容，不需要维护白名单。
- **`MTLDebugDevice` 的存在**：debugger 下的 device 是 Apple 的 wrapper，负责参数检查和错误日志；脱离 debugger 之后才是裸驱动——这是 Metal validation 层的实现机制。

## 链接到的概念

- [[metal-api-overview]]
- [[deferred-rendering]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/feature-sets/
- 本地：`raw/articles/metalbyexample.com/2014-09-24_feature-sets-and-capabilities.md`
