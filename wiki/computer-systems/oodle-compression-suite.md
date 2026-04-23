---
tags: [压缩, oodle, kraken, rdo, bcn, 游戏资源]
date: 2026-04-14
sources: 1
---

# Oodle 压缩套件：Kraken、Mermaid、Texture RDO

**Oodle** 是由 RAD Game Tools（2020 年被 Epic 收购，业务牌照上改名为 Epic Games Tools，社区里仍称 RAD）开发的一组数据压缩库，[[fabian-giesen]] 是其核心作者之一。它并非一个算法，而是三条互不重叠的产品线，经常被外界混为一谈。

## 三条产品线

**Oodle Data** 做无损数据压缩，对标 Deflate/ZIP、7zip/LZMA、Zstd、LZ4。最初为游戏资源在磁盘上的存储设计，但本身是通用的字节流压缩。它的算法家族强调**解码速度**：

- **Kraken**——主打 jack-of-all-trades，比 Deflate 压缩率好得多、比 Zstd 略好，同时解码快。典型情况下 Kraken 解码比 Deflate 快约 4 倍。
- **Mermaid**——比 Kraken 解得更快，压缩率稍低。
- **Selkie**——再快一档，压缩率再低一档。
- **Leviathan**——反方向：解码慢但压缩率最高。

游戏开发者按 CPU 预算与磁盘预算在这四档里挑。对于仍走蓝光实体发行的游戏，99 GB 和 101 GB 会决定能不能塞进 100 GB 光盘，几个百分点的压缩率差别在这种场景下是硬约束。

**Oodle Network** 专打 UDP 小包场景，典型包小于 100 字节。它是无损的、但针对「独立小消息、几乎无 per-packet 开销」优化，代价是解码比 Oodle Data 慢。

**Oodle Texture** 是 BC1–BC7（合称 BCn）GPU 压缩纹理的编码器，见 [[bc7-solid-color-encoding]]。核心特色是 **RDO**（Rate-Distortion Optimization）：详见下文。

## Kraken 与 PS5 的常见误解

因 Kraken 在 PS4 游戏上被广泛采用，Sony 在 PS5 上把 Kraken 解码做成了硬件单元（由 Sony 与 AMD 合作开发），PS5 解压几乎「免费」。

网络上经常有人把「PS5 游戏比 PS4 小得多」直接归功于 Kraken。这里 [[fabian-giesen]] 明确澄清：

- Kraken 相对 Deflate 的典型差距是 **10–15%**。无损压缩界里一个百分点已经是大新闻，但这里仍不是「砍半」的量级。
- 某些 PS4 游戏在 PS5 上的包体缩得多得多，**主因不是 Kraken**，而是**打包工具去重**：
  - PS4 游戏要从机械硬盘读，为了避免长 seek，资源常常在光盘上重复多份摆放。
  - PS5 一律走 SSD，seek 不是问题。Sony 的打包工具会自动发现并消除这些跨资源的大段重复。
- 去重的功劳归 Sony 打包工具团队，不是压缩算法。

这个澄清对任何做资源打包与发行的人都有意义：**分清「per-byte 熵编码收益」和「宏观去重收益」**，二者在数量级上可能差 10 倍。

## Oodle Texture 与 RDO

BCn 是一族定长块（固定 bit rate）的 GPU 纹理压缩格式，随机访问友好。正因为是定长块，「简单」区域（如纯色）被用掉的 bit 数远多于其信息量，在 VRAM 里这是我们为随机访问付的代价——可以接受；但在**磁盘和下载**里就是纯浪费。实践中 BCn 纹理在磁盘上会再套一层无损压缩（Deflate、Zstd、Oodle Data）。

**RDO 的核心洞察**：BCn 编码器在挑「同等误差下哪种编码」时有自由度。如果让编码器**意识到**下游会再过一次无损压缩，就可以主动偏向「更容易被无损压缩吃掉」的编码——比如让相邻块共用相似的 endpoint。Oodle Texture RDO 正是这么做：在引入少量可控误差的前提下，磁盘与下载体积**常常减半以上**，而 **VRAM 占用完全不变**（因为最终还是定长 BCn 格式，运行时无需任何额外解码步骤）。

Oodle Texture 团队定下的目标是：在典型设置下，RDO 输出的误差应当**接近非 RDO 编码器的水平**——换句话说，你得到的是和以前一样好的纹理保真度，只是磁盘脚印小了一大半。

## 相关

- [[bc7-solid-color-encoding]] —— BC7 编纯色块的最优端点选择
- [[fabian-giesen]]
- [[adaptive-arithmetic-coding]] —— ryg 在无损压缩另一侧的根技术
- [[lossless-float-image-compression]] —— 另一个 BC/RDO 相关的浮点图像压缩对照
- [[meshoptimizer-vertex-codec]]

## Sources
- [[sources/ryg-oodle-kraken-misconceptions]]
- [[sources/ryg-mrsse]] — BC6H 编码的 HDR 误差度量
- [[sources/ryg-bc7-optimal-solid-color-blocks]] — BC7 纯色块的最优编码
- [[sources/ryg-oodle-2-9-14-intel-13th-14th-gen]] — Oodle 2.9.14 的 Intel 13/14 代 work-around
- [[sources/chipsandcheese-image-compression-part2]] — 现代图像编解码器对比（JPEG-XL/AVIF/WebP）
