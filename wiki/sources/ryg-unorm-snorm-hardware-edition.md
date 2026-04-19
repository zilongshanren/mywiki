---
tags: [source, 渲染, gpu, 硬件实现, ieee754]
date: 2026-04-19
sources: 1
---

# UNORM and SNORM to float, hardware edition（Fabian Giesen / ryg）

[[fabian-giesen|ryg]] 2024 年 12 月的文章，补完之前 [[unorm-float-conversion|软件精确 UNORM→float]] 的另一面：**在硬件里**做 UNORM / SNORM 到 float32 的精确转换到底要付多少面积？答案：极少。

## 摘要

关键观察：除以 $2^n - 1$ 在几何级数展开下变成"把 n-bit 整数沿分数位反复复制"；由于各复制段 bit 范围不重叠，**这不是真加法而是 wiring**。完整硬件数据通路：(1) 识别并特判两个特殊值（UNORM8: 0x00→0.0, 0xFF→1.0；SNORM 多两个 ±1 的冗余表示）；(2) 16-bit leading-zero count + 左移，同时得出指数 `126 - num_lz`；(3) 尾数用 normalized 值的 bit 重复得到 23 bit；(4) round-to-nearest 只需加 `normalized_x[7]`。由于特殊值已剔除，rounding 进位**永不跨指数**，只需 15-bit adder 即可。UNORM8 可归约为 UNORM16（把字节复制两次：$65535 = 255 \cdot 257$）。SNORM 变体多一个 abs + 符号提取（又是一个 15-bit adder）。全部算下来：一个 LZ 模块 + 一个 16-bit adder + 一点 mux——没有乘法器、没有除法器、没有迭代。

## 关键要点

- $1/(2^n - 1) = \sum_k 2^{-kn}$ 在硬件里 = **bit 模式重复**。
- UNORM8 → UNORM16 等于字节复制两次：$65535 = 255 \cdot 257$。
- 特殊值先处理，rounding 永不跨指数——省 full-width adder。
- UNORM / SNORM / 不同位宽**共用同一数据通路**，仅前端 mux 不同。

## 链接到的概念

- [[unorm-snorm-hardware-conversion]]
- [[unorm-float-conversion]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/12/24/unorm-and-snorm-to-float-hardware-edition/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-12-24_unorm-and-snorm-to-float-hardware-edition.md`
