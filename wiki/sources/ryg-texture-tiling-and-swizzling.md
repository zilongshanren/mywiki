---
tags: [source, gpu, 纹理, morton, 内存布局]
date: 2026-04-14
sources: 1
---

# Texture tiling and swizzling（Fabian Giesen）

[[fabian-giesen|ryg]] 2011 年 1 月的长文，把各家 GPU 常见的纹理分块 / swizzle 模式统一到「嵌套分块」的一般框架，并给出一条**两指令就能沿任意 swizzle 模式走一步**的地址更新公式。这篇文章后来被 Intel 4th-Gen Core Graphics Developer's Guide 引用为共享 GPU/CPU 资源访问的推荐实现。

## 摘要

行主序纹理在列方向走会撞 cache miss。GPU 的对策是**分块**（4×4 pixels 装一条 cache line）和 **swizzle**（把线性地址按 x / y 的 bit 顺序重新编排），二者本质都是让空间相邻 → 地址相邻。所有「保序交错」的 swizzle 都可以理解为**嵌套 tile**：Morton 序就是 2×2 → 4×2 → 4×4 → 8×4 → … 的极端情形。嵌套视角两个好处：非正方形 2 的幂纹理可以自然用 `H×H` 顶层 tile + Morton；非 2 的幂尺寸可以顶层 tile 以上退回行主序。

文章的硬核贡献是软件实现。定义 `x_mask` / `y_mask` 为 x / y bits 的位置掩码（不相交），则沿 x 方向走一步等于：

```
offs_x = (offs_x - x_mask) & x_mask;
```

原理：`-x_mask` 等价于 `~x_mask + 1`，`~x_mask` 在所有 y bit 的位置上都是 1，`+1` 从最低位出发传播到第一个 x bit；每次 x bit 的进位会穿越 y 的空洞段进入下一个 x bit；最后一次 `& x_mask` 清零。这套公式对 Morton、纯 4×4 tile、任意嵌套 tile 都是**同一份代码**——只要换掩码。PPC 上内循环压到 4 条指令。配合写 cache line 对齐 + 源顺序遍历 + 非 2 幂尺寸下把 tile index 吸收进 `x_mask`，就得到一个能处理任意子矩形更新的通用 `glTexSubImage2D` 风格函数。

## 关键要点

- 分块 vs swizzle 在硬件侧同构，本质都是 swap 一部分地址 bit。
- 「嵌套分块」统一了 4×4 tile、Morton、8×8-in-32×32 等各家模式，关键条件是 x / y bits 之间的相对顺序保持不变。
- 非正方形 2 的幂纹理用 `H × H` 顶层 tile + Morton，可以彻底避免补 pad 到正方形。
- 核心技巧：`(offs - mask) & mask` 利用 y 空洞里的 1-bit 让 x 的进位自然跨过，覆盖任意嵌套 swizzle。
- 同一套公式扩展到 3D 体纹理：`offs_x` / `offs_y` / `offs_z` 三路独立更新。
- 和 BLAS 的 Morton-order 矩阵块化属于同一个族系；Wise & Frens 的论文只覆盖 Morton 序和正方形情形。

## 链接到的概念

- [[texture-swizzle-nested-tiling]]
- [[fabian-giesen]]
- [[cache-friendliness]]
- [[memory-hierarchy]]
- [[hierarchical-z-buffer]]

## 原文

- 链接：https://fgiesen.wordpress.com/2011/01/17/texture-tiling-and-swizzling/
- 本地：`raw/articles/fgiesen.wordpress.com/2011-01-17_texture-tiling-and-swizzling.md`
