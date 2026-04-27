---
tags: [渲染, g-buffer, 法线编码, 延迟渲染, decal]
date: 2026-04-27
sources: 1
---

# G-Buffer 多基底法线编码（Multiple Tangent Bases）

在延迟渲染中，G-Buffer 法线编码面临一个三角约束：紧凑（位数少）、精确（量化误差小）、可混合（支持像素 shader decal 的硬件 blend）。两通道编码配合视空间方向可以实现可混合性，但精度不足；世界空间编码精度好，但因为投影不连续而不可混合。**多基底方案**用少量额外 bit 突破了这个约束。

## 思路来源

这个方案由 Frostbite 的 Alex Fry 构想，Sébastien Lagarde 在 SIGGRAPH 2014 《Moving Frostbite to PBR》中提及但未展开。[[angelo-pesce]] 在 2015 年 1 月的博客中将其阐述清楚，并在评论区与 Lagarde 补充了若干实现细节。

## 核心洞察

Decal 在 G-Buffer pass 时使用硬件 blend——它必须读取当前像素的法线，与 decal 的法线混合后写回。硬件 blend 是**加权线性组合**，因此编码空间必须连续（不能在混合范围内有跳变或折叠点）。

多基底方案的关键在于：
- 将法线球面划分为若干区域，每个区域由一个"切线空间基底"（tangent basis）覆盖
- G-Buffer 中存储 2–4 bit 的基底选择 index，以及在该基底内的 2-通道法线投影
- Decal 渲染时**只读取基底 index**（不混合），然后在同一基底内做法线的线性混合

由于 decal 法线在同一基底内混合，没有跨区域折叠，混合是连续的。这几个 bit 可以"偷"自 G-Buffer 中任意组件的最高位（decal blend 时只需读取这些位，不输出它们，因此不会被混合掉）。

## 基底选择策略

合理的基底集合是**带符号单位立方体的 8 个顶点方向**（即 `(±1, ±1, ±1)` 归一化），对应 3 bit index。每个基底覆盖法线球面的一个球面八分体。

以几何法线（而非 normal map 之后的法线）做基底选择是工程上合理的近似——几何法线决定了表面朝向的大方向，normal map 只是在此基础上的扰动，不太可能把法线推出所选基底的覆盖范围。

基底内的投影只需处理**该基底覆盖的子集**（约半球加上覆盖区域带来的少量"余量"），投影精度因此比覆盖全球的编码高。使用 3 bit（8 个基底）时，每个基底覆盖约 1/8 球面；2 bit（4 个基底）也可以工作，精度略低但仍优于单一视空间编码。

## 与其他方案的对比

| 方案 | 位数 | 可混合 | 精度 |
|------|------|--------|------|
| XYZ 三通道 | 3 × 16F | 是 | 最高（但浪费） |
| 视空间两通道 | 2 × 10–16 bit | 是 | 中等（抖动明显） |
| Octahedral / BFN | 2 × 8–16 bit | 否（有折叠） | 高 |
| 多基底（2 bit） | 2 × 10 bit + 2 bit | 是 | 视空间以上 |
| 多基底（3 bit） | 2 × 10 bit + 3 bit | 是 | 接近全局最优 |

## 已知落地

Activision Black Ops 3 使用了 2 bit + Lambert azimuthal equal-area 投影，配合 TAA 的蓝噪声 dither 消除 shiny 表面的量化条带（见评论区补充）。最终选择 2 bit 是因为"基底间重叠区域足够小，不需要 3 bit 的精度"。

## 注意事项

若投影不覆盖某些法线（精确裁剪，增加每基底精度），需确保所有可能的法线（含切线空间扰动后的法线）不会超出基底覆盖范围——否则边界处会出现接缝（不同基底对同一方向的量化精度不同，导致相邻像素间出现色调跳变）。

## 相关

- [[compact-normal-encoding]] — 整体 2-通道法线编码技术概述
- [[deferred-rendering]] — G-Buffer 的布局与约束
- [[normal-decal-edge-blending]] — decal 法线混合的一般问题
- [[tangent-space-normal-mapping]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-gbuffer-normal-encodings]]
