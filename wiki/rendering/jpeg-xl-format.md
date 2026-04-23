---
tags: [图像压缩, 编解码, jpeg-xl, avif, webp, 渲染]
date: 2026-04-19
sources: 2
---

# JPEG-XL 格式

JPEG-XL（JXL）是 JPEG 委员会主导的新一代图像编码标准，目标是在几乎所有场景下全面超越 JPEG，同时对 JPEG 保持向后兼容性（支持 JPEG → JXL 无损再压缩）。BlueSwordM 在 Chips and Cheese 的图像压缩系列第二篇中对其与 AVIF、WebP 进行了系统对比。

## 核心技术特性

JPEG-XL 保留了 JPEG 的基本框架——YCbCr 色彩空间、DCT 变换、渐进解码——但在此之上做了全面升级：

- **可变 DCT（VARDCT）**：从固定的 8×8 扩展到 4×4 至 256×256 可变块大小，适应不同纹理频率。
- **XYB 色彩空间**：感知对齐的色彩模型，量化步长与人眼敏感度更匹配。
- **自适应量化**：高位深支持（最高 32-bit float），HDR/宽色域原生支持。
- **渐进解码**：支持多层次渐进预览，优于 JPEG 的单层渐进，对网络图像加载体验友好。
- **多帧与动画**：可替代 GIF，并附带深度图、热力图等多层元数据。
- **无损 JPEG 重压缩**：将现有 JPEG 文件转为 JXL 无损格式，文件尺寸可缩减约 20%，且转换可逆。

## 与 AVIF 和 WebP 的对比

在中高画质（中等 BPP）的场景下，JPEG-XL 在以下维度均领先：

- **编码速度**（多线程时接近 libjpeg-turbo）
- **解码速度**（最快，配合渐进解码对显示延迟友好）
- **细节保留**（高 BPP 时优于 AVIF libaom-av1）

AVIF（基于 AV1 的图像格式）的优势在于**极低 BPP**（极度压缩）场景，AV1 的方向性预测和环路滤波在此发挥更大作用，代价是整体编码速度慢约一个数量级（libaom-av1 单线程）。AVIF 还有 35 MP 的分辨率限制，超过后需要分块，引入额外复杂度。

WebP 的有损部分基于 VP8，整体效果与 mozjpeg 相近甚至略差。其无损模式（基于独立开发的图像压缩方案）持续优于 PNG，但采用率一直偏低，原因是在浏览器普及较晚且与 JPEG/PNG 相比优势不够明显。

## 与 [[jpeg-codec-pipeline]] 的关系

JPEG-XL 是 [[jpeg-codec-pipeline|JPEG 三段式流程]]（色彩变换 → DCT + 量化 → 熵编码）的直接演进：用 XYB 替换 YCbCr，用 VARDCT 替换固定 8×8，用算术编码替换 Huffman。这使得 JXL 解码器可以以相对小的代码增量实现对现有 JPEG 的识别和无损转码。

## 参见

- [[jpeg-codec-pipeline]]
- [[adaptive-arithmetic-coding]]
- [[planar-rotation-dct]]
- [[color-space]]

## Sources

- [[sources/chipsandcheese-image-compression-part2]]
- [[sources/chipsandcheese-jpeg-image-compression-overview]]
