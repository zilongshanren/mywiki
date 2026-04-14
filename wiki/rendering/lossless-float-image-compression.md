---
tags: [图像压缩, 文件格式, 渲染, 浮点, vfx]
date: 2026-04-14
sources: 2
---

# 无损浮点图像压缩（Lossless Float Image Compression）

电影/VFX 管线里的中间图像几乎都是**浮点多通道**：一张 `.exr` 里除了 RGB/alpha 还有 depth、normal、velocity、direct/indirect lighting、AO、material ID 等层；每层可能是 FP16 或 FP32，甚至同一张图里不同通道浮点精度不同。无损压缩这样的数据和「压一张 JPEG」完全不是同一个问题——它更像是「压一大堆结构化、相关度各异的浮点流」。

## 评测维度

合理的对比要同时看三件事，[[aras-pranckevicius]] 的 2025 年评测把它做成了「两张散点图」：

1. **压缩比**（compressed / uncompressed）。
2. **压缩速度**（GB/s，分母是未压缩大小，这样能跨压缩比比较）。
3. **解压速度**（GB/s，同样按未压缩大小计）。

压缩时间基本不包括磁盘 I/O（内存进出），否则真实存储带宽会把所有格式都拉平。

## 主要候选格式

### [[openexr-format|OpenEXR]] ZIP

工业默认值。代码干净（80 行代码读写一张图）、特性齐全（任意通道数、多 part、mipmap、任意浮点精度）、性能中庸但稳定。默认压缩级别 4 已经压缩比足够。

### OpenEXR HTJ2K（3.4 新增）

基于 High-Throughput JPEG 2000（OpenJPH 实现）。**压缩比略好一点，压缩/解压都慢一档**。主要短板：HTJ2K 的 de-correlation 只作用于主 color layer，对 multi-layer EXR 里其他「其实也是 RGB 颜色」的层没有加成，空间没吃到。未来商业 HTJ2K 实现（Kakadu）比 OpenJPH 快不少，性能有改善空间。

### JPEG-XL 无损

现代「通用图像格式」，但定位基本锁在**「屏幕上的图像」**：API 和内部结构都围绕 color/LDR/animation/photoshop layers 展开；extra channels、FP16/FP32 浮点都是挂件。实测结果：

- level 1-3 压缩比不如 OpenEXR，速度又慢 3x；
- level 4+ 才开始赢压缩比，level 8 和 JPEG-XL 默认 level 7 能把压缩比拉到 2.4x，但**压缩速度比 OpenEXR 慢 100 倍**，解压慢 5-13 倍；
- FP16 subnormal 不能往返，NaN/inf 在无损模式里也不保证保留位图样——而 EXR 连 NaN 的具体位模式都保持原样；
- libjxl 要求 color interleaved + extra channels planar，手工 massage 数据；读写代码量 550 行 vs OpenEXR 的 80 行。

### meshoptimizer 「MOP」

最大的意外：把每个像素当作一个「顶点」喂给 [[meshoptimizer-vertex-codec]]（它本来是 mesh 压缩器），再把输出管道到 zstd，结果是：

- 压缩比 ~2.3x（和 JPEG-XL level 7-8 相当）；
- **压缩快 30-100 倍**、解压快 20 倍；
- meshoptimizer 本身只要 26 KB 代码，zstd 加 405 KB；
- 是 delta/prediction 编码（非 LZ），天然适合浮点图像里通道内的「局部平滑」。

缺点：不是真正的图像格式，没有 metadata/layer/色彩空间概念，只适合「内部管线自用」。

## 结论

1. 外部交付/工业标准：继续用 EXR ZIP。
2. 如果 OpenEXR 4.x 把 HTJ2K 的 multi-layer de-correlation 做起来，再看。
3. JPEG-XL 目前不是一个好选择：浮点不完整无损，API 笨重，速度差一个量级。
4. 内部工具/游戏引擎里只要能无损回读的场景：meshoptimizer + zstd 可以考虑，收益可观。

## 相关

- [[openexr-format]]
- [[meshoptimizer-vertex-codec]]
- [[adaptive-arithmetic-coding]]

## Sources

- [[sources/aras-lossless-float-image-compression]]
- [[sources/aras-openexr-vs-tinyexr]]
