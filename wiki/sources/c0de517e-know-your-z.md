---
tags: [source, rendering, 深度缓冲, shader, 顶点着色器]
date: 2026-04-19
sources: 1
---

# Know your Z（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2010 年 8 月的小测题：**如果在 VS 里对 `hPos` 做下面两种操作，会怎样？**

```hlsl
// Option A:
hPos /= hPos.w;
// Option B:
hPos.z *= hPos.w / farPlaneViewZ;
```

## 摘要

**Option A**：把齐次坐标除以 `w`，相当于提前做透视除法。代价是**禁掉所有纹理坐标的透视插值**——光栅器以为 `w=1`，不再做 perspective-correct。Pesce 的结论：没什么正经用途。

**Option B**：看起来很小，但效果精巧。深度缓冲最终存的是 `z/w`，投影后 `z ∈ [0, far]`，这一乘一除让写入深度缓冲的值变成 `z/far`——**视空间线性的 `[0,1]` 深度**，等价于软件 W-buffer。而且**不动 `w`，不破坏纹理透视插值**。

Pesce 最初以为这是免费午餐，同事邮件指出**坑**：Z 在屏幕空间不再线性，三角形内的 Z 不再落在一个平面上——会产生新的 Z-fighting 和 Hi-Z 失效。但在**细分密 + 没有近距平行墙**的窄场景（比如角色 shadowmap）仍可用。

评论区分支到 Humus 的 linear-depth 分析，Pesce 对其中「线性 Z 让 Hi-Z 容易算 tile 范围」表示怀疑——Hi-Z 从 quad 的插值结果拿边界，不依赖屏幕空间线性。

## 关键要点

- **Option A**（`hPos /= hPos.w` in VS）：禁透视插值，无实用价值。
- **Option B**（`hPos.z *= hPos.w / far` in VS）：软件 W-buffer，得到视空间线性深度；**不破坏纹理透视插值**（因为 `w` 不变）。
- **代价**：Z 不再屏幕空间线性 → Hi-Z / 压缩退化、三角形内深度弯曲、某些卡近平面裁剪怪异。
- **适用窄场景**：角色 shadowmap、密细分网格、无近距平行墙。
- **现代首选**：[[reversed-z]] + float depth，大多数情况直接替代这个 trick。
- 评论区读者 NULL_PTR、MJP 等给出补充——COLOR 输出的 perspective-correct 在 DX10 之后不能保证，ATI HD5870 仍 correct；NVIDIA 有个 solid wireframe 论文确实用非透视 COLOR 实现。

## 链接到的概念

- [[linear-z-trick]]
- [[z-buffer]]
- [[reversed-z]]
- [[z-fighting]]
- [[hierarchical-z-buffer]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/08/know-your-z.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-08-13_know-your-z.md`
