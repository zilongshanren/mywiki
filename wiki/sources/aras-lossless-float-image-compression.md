---
tags: [source, 渲染, 图像压缩, 文件格式, openexr]
date: 2026-04-14
sources: 1
---

# Lossless Float Image Compression（Aras Pranckevičius / aras-p.info）

[[aras-pranckevicius]] 发表于 2025 年 7 月的文章，系统评测 OpenEXR（ZIP / 新的 HTJ2K）、JPEG-XL、以及他自己用 meshoptimizer + zstd 拼出的「MOP」格式在**无损浮点多通道图像**上的表现。结论直白：老老实实用 EXR ZIP，但如果只是内部管线可以试试 meshoptimizer。

## 摘要

作者的用例是影视合成里的 multi-layer 浮点图（FP16/FP32，通道里装着 AO、direct/indirect lighting、normal、depth、velocity、material ID 等），数据集取自 Blender splash 和 Poly Haven HDRI。OpenEXR 3.4 即将加入 HTJ2K（基于 OpenJPH 实现 High-Throughput JPEG 2000）压缩模式：压缩比略有提升（1.87x → 1.95x），但压缩和解压都慢一档；对 multi-layer 场景尤其不友好，因为 HTJ2K 只对「主 color」做 de-correlation，不会对 direct diffuse 这种实际也是 RGB 的层做。JPEG-XL 在 level 1-3 几乎全败，level 4+ 才开始赢压缩比，但 level 8 就比 EXR 慢了 **100 倍**，且 API 要求 color 通道交错 + 额外通道平面化，写读代码量是 OpenEXR 的 7 倍（550 vs 80 行），FP16 下还不完全无损（subnormal/NaN 不能往返）。真正的惊喜来自 meshoptimizer 的 vertex codec——它本来是 mesh 压缩器，但把像素当作「顶点」喂进去，配合 zstd 就能拿到 2.3x 压缩比、比 EXR/JPEG-XL 都更好的压缩/解压速度（30-100 倍快于 JPEG-XL），代码体积仅 26 KB。

## 关键要点

- **EXR ZIP 依然是默认选择**：速度、比例、生态三项都够用，和默认 level 4 几乎锁死。
- **HTJ2K 对 multi-layer 不友好**：只对单一 color layer 做 de-correlation，浪费了其他「其实也是 RGB」的层的压缩空间。
- **JPEG-XL 定位错配**：它是冲着「屏幕上的图像」设计的，API 和内部结构都围绕 color 展开；extra channels、多通道浮点是「挂件」，FP16 subnormal 都不保证无损。
- **meshoptimizer 压浮点图像意外好用**：作为 delta/prediction 编码（非 LZ），它的输出还可以再喂给 zstd，达到 JPEG-XL level 7-8 级压缩比但快两个数量级。
- **代码体积对比**：meshoptimizer 26 KB，zstd 405 KB，HTJ2K/OpenJPH 308 KB，libjxl 6 MB。对嵌入式/游戏引擎内部工具来说差别显著。
- **性能量纲**：统一按「未压缩数据大小 / 时间」计 GB/s，可直接比较不同压缩比下的实际吞吐。
- Apple M4 Max 的高内存带宽让所有数字都比 Ryzen 5950X 好看，是测评平台差异的典型样本。

## 链接到的概念

- [[lossless-float-image-compression]]
- [[openexr-format]]
- [[meshoptimizer-vertex-codec]]

## 原文

- 链接：https://aras-p.info/blog/2025/07/08/Lossless-Float-Image-Compression/
- 本地：`raw/articles/aras-p.info/2025-07-08_lossless-float-image-compression-aras-website.md`
