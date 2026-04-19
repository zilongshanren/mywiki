---
tags: [渲染, 纹理压缩, bc7, 编码器]
date: 2026-04-19
sources: 1
---

# BC7 纯色块的最优编码

[[fabian-giesen|Fabian Giesen]] 在 Oodle Texture 的 BC7 encoder 里记录了一条**数学上可证最优、实现只需两行代码**的小结论：对任意 8-bit RGBA 纯色块 (solid-color block)，BC7 mode 5 永远能**精确还原**；而且不需要查表，一行公式搞定端点。

## 背景与选择

纯色块（4×4 像素同色）在游戏纹理里非常常见（UI、贴花边缘、UV 未覆盖区）。BC1/BC3 常常无法精确命中 8-bit 输入色；ASTC 有专门的 "void-extent blocks" 模式直接存单色；BC7 没有专属模式但胜在表达力。BC7 的 8 种 mode 里挑一个：

- **Mode 5** 存 RGB 端点各 7 bit 精度 + Alpha 端点 8 bit 精度，RGB / A 独立编码，2 bit 色索引。

Alpha 直接 8 bit 存端点 + 索引 0 搞定。RGB 的问题是：7 bit 端点 × 2 = 只覆盖 128 个值，怎么命中 256？

## 核心观察

BC7 mode 5 的 2-bit 索引四个取值对应的插值系数是 $\{0, 21/64, 43/64, 1\}$。索引 0 / 3 只能返回端点扩展后的那 128 个值。索引 1 / 2 以端点为支点做插值、互为对称，所以只需考虑「两端点 + 索引全 1」这种配置，再靠**插值本身的 7-bit→ 8-bit 舍入**取得第 256 种值。

Giesen 构造（反查表推导出）的公式是：

```c
// 精确满足：target == (43 * expand7(e0) + 21 * expand7(e1) + 32) >> 6
// 其中 expand7(x) = (x << 1) | (x >> 6)
e0 = target >> 1;
e1 = ((target < 128) ? (target + 1) : (target - 1)) >> 1;
// 全部 16 个索引置 1
```

对 R / G / B 各通道独立做一次。全部索引设为 1。就这样，**每种 8-bit 目标色都能被精确命中**。

## 为什么这重要

- **可证明**：输入空间有限（256），公式显式、遍历验证即可——不像 BC1 纯色需要借浮点最优化兜底。
- **不需要 LUT**：比查「最佳 (e0, e1) 表」更省 cache，主循环里也避免了数据依赖。
- **runs 里的一致性**：纯色块常常连片出现，同一个颜色总是映射到同一个编码——比起"多种等价编码随机选一个"，RDO 和熵编码都会开心。

Oodle Texture 所有 BC7 encoder 版本（普通 / RDO）都用这段逻辑作为 solid-block 快速路径。

## 相关

- [[fabian-giesen]]
- [[unorm-float-conversion]] — 也是「看似要查表的精度问题，其实有闭式算法」的兄弟案例

## Sources

- [[sources/ryg-bc7-optimal-solid-color-blocks]]
