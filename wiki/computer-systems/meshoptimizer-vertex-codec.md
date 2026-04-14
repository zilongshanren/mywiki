---
tags: [压缩, 性能, 几何]
date: 2026-04-14
sources: 1
---

# meshoptimizer Vertex Codec

**meshoptimizer** 是 Arseny Kapoulkine（zeux）维护的 mesh 处理库，里面有一个独立的「**vertex codec**」——一个专门用来无损压缩顶点流的算法，**不是 LZ 系**，而是 delta / prediction + 紧凑打包。它在 mesh 压缩场景里早已被广泛使用（glTF 的 `EXT_meshopt_compression` 扩展就是它），但更有意思的故事是：**它用在非 mesh 数据上也很能打**。

## 设计直觉

Mesh 里的顶点属性有一个很强的结构假设：**相邻顶点往往数值很接近**（位置、法线、UV、权重都是）。vertex codec 利用这一点：

- 把数据按「顶点」分块，每个顶点内部字节按通道错列；
- 相邻顶点之间用差分 / 预测，残差落在很小的数值范围；
- 残差用比特级紧凑打包，避开完整 LZ 字典表的开销。

结果是**解压极快**（接近内存带宽）、**压缩也很快**（比 zstd/zlib 快很多），压缩比中等。它不是万能压缩，但对「局部平滑的结构化流」特别有效。

## 在浮点图像上的意外胜利

[[aras-pranckevicius]] 把像素当作「顶点」喂给 vertex codec：把一张图分成 16K 像素的 chunk、每个 chunk 独立压缩、并行跑。像素大小不是 4 的倍数时用 0 填充。对多层浮点 EXR 数据（FP16/FP32 的 AO、depth、normal 等通道），得到了非常强的结果（见 [[lossless-float-image-compression]]）：

- **单用 vertex codec**：压缩比 ~2.0x，和 EXR HTJ2K 持平；但压缩快 2 倍、**解压快 5 倍**。
- **vertex codec + zstd 管道**：压缩比 ~2.3x，相当于 JPEG-XL level 7-8；但压缩**快 30-100 倍**、解压快 20 倍。代码体积仅 26 KB（zstd 另外 405 KB）。

这个组合击败 OpenEXR ZIP、HTJ2K、JPEG-XL 的所有 level，在内部管线场景里非常有吸引力。

## 为什么「mesh 压缩器压浮点图像」能赢

答案在三件事的叠加：

1. **数据假设匹配**：浮点图像的通道内局部相关度高，和 mesh 顶点属性的假设一致。
2. **预测残差对 zstd 友好**：vertex codec 输出已经「把低熵挤到一起」，再让 zstd 做一次熵编码，零重复工作，压缩比继续提升。
3. **现代 CPU 上 delta/打包是内存带宽限速**：几乎没有 CPU 计算开销，而 LZ 类压缩器要维护滑动窗口和匹配查找。

## 相关

- [[lossless-float-image-compression]]
- [[openexr-format]]
- [[adaptive-arithmetic-coding]]

## Sources

- [[sources/aras-lossless-float-image-compression]]
