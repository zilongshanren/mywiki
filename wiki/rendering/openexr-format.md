---
tags: [图像压缩, 文件格式, 渲染, vfx, hdr]
date: 2026-04-14
sources: 2
---

# OpenEXR 文件格式

**OpenEXR**（由 ILM 于 1999 年开源）是电影 VFX 行业事实上的浮点 HDR 中间图像格式。它和「给屏幕用的图像格式」（PNG、JPEG、JPEG-XL）最大的区别是：EXR 一开始就是给**管线中间态**设计的——不是为了在显示器上显示，而是为了在渲染器、合成器、downstream 工具之间传递大量带结构信息的浮点数据。这个定位决定了它与众不同的特性集。

## 设计决策

- **任意通道数**：不止 RGB/alpha；depth、normal、velocity、AO、material ID、per-light AOV 等都是「一等通道」，不是「extra」。
- **每通道任意类型**：FP16 (half)、FP32 (float)、UINT 三选一，同一张图里可以混搭。
- **任意排布**：单 part / 多 part（image 里多个子图）、tiled / scanline、mipmap / ripmap；可以以任何组合存在。
- **位图样保真**：NaN / Inf 的具体位模式都严格保持；没有「显示色域」的概念，自然也不会为此做任何破坏性的重新量化。
- **多个压缩模式**：NONE、ZIP、ZIPS（line-by-line）、RLE、PIZ（wavelet + Huffman）、PXR24、B44/B44A、DWAA/DWAB、以及 3.4 新增的 **HTJ2K**（High-Throughput JPEG 2000，基于 OpenJPH）。

## 压缩模式现状（2025）

- **ZIP**：默认值，level 4。速度、比例都稳定。几年前从 zlib 换成 libdeflate 带来一次提速。是绝大多数场景的正确选择。
- **HTJ2K**：3.4 新增。压缩比略好一点，但速度下降一档。对 multi-layer 场景只对主 color 做 de-correlation，不会扫描其他「也是 RGB 颜色」的层。OpenJPH 实现性能仍有提升空间。
- **DWAA/DWAB**：3.3 开始从实现里删掉了巨大的查找表，体积明显缩水。
- **B44/B44A、PXR24**：历史包袱级别，用得少。3.4.4 进一步瘦了 B44 查找表。

详细评测见 [[lossless-float-image-compression]]。

## 官方库 vs tinyexr

**OpenEXR 官方库**（`AcademySoftwareFoundation/openexr`）十年前在非 Linux 环境下臭名昭著地难编，2025 年的 CMake + 自动依赖抓取大幅改善了体验。库分「Core」层和「C++ 高层」两块。OpenUSD 的做法很值得借鉴：只取 `src/lib/OpenEXRCore` + `external/deflate`，配合一层叫 **nanoexr** 的极薄 C 包装合并成**单个 C 源文件**，就能得到一个近似 tinyexr 的「一个文件引入」体验，但性能和特性都完整。

**tinyexr**（`syoyo/tinyexr`）是一个广为流传的简化实现，最大的卖点是单 header。代价：

- 不支持 PXR24、B44/B44A、DWAA/DWAB、HTJ2K、深度图像；
- 单线程模式下读写慢 3-4 倍（实测 6 张 4K EXR：tinyexr 6.55s vs OpenEXR 3.4.4 1.65s）；
- 线程池模型是「每次处理新建并销毁」，不适合高频重用。

**官方库 3.x 的瘦身轨迹**：3.2.4 → 3.3.5 → 3.4.4 二进制体积从 2221 KB 一路降到 649 KB；进一步关掉 HTJ2K/DWA/B44/PXR24 后可降到 303 KB，只比 tinyexr 的 251 KB 大一点点，却带着完整特性集。

## 选型建议

- **外部交付 / 管线标准**：OpenEXR 官方 C++ 库，ZIP 压缩。
- **嵌入到体积敏感的工具或引擎**：OpenEXR Core + nanoexr 单文件合并；只留 ZIP 压缩可瘦到 300 KB。
- **临时小工具 / 原型**：tinyexr 仍然是最快接入的选择，但要接受「只支持少数压缩模式」。

## 相关

- [[lossless-float-image-compression]]
- [[meshoptimizer-vertex-codec]]

## Sources

- [[sources/aras-lossless-float-image-compression]]
- [[sources/aras-openexr-vs-tinyexr]]
