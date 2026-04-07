---
tags: [渲染, 透明]
date: 2026-04-05
sources: 1
---

# Alpha Blending（透明混合）

**半透明物体与已有 framebuffer 颜色的混合**：

```
C_final = C_src × α_src + C_dst × (1 - α_src)
```

（这是最常见的 SrcAlpha + OneMinusSrcAlpha 混合。）

## 为什么透明比不透明难

- **Z-Buffer 只能存一个深度**——多个半透明重叠时无法正确排序。
- 必须**从后往前**渲染（画家算法）。
- **不写** Z buffer（只读）——否则后续物体会被错误拒绝。
- Order-dependent：渲染顺序错了，颜色就错了。

## 排序成本

每帧对可见透明物体按深度排序。动态场景里是 CPU 开销。

## OIT（Order-Independent Transparency）

解决 order-dependent 问题的技术：
- **Depth Peeling**：多遍剥离，高成本。
- **Weighted Blended OIT**（Morgan McGuire）：单遍近似，质量可接受。
- **Per-Pixel Linked Lists**：存储每像素所有 fragment，几乎精确但高内存。

## Alpha Test

**二值丢弃**（`if (a < threshold) discard;`），不是混合。破坏 [[early-z-late-z|Early-Z]] 和 [[hsr-tbdr|HSR]]。

## 相关

- [[z-buffer]]
- [[early-z-late-z]]
- [[fragment-shader]]
- [[hsr-tbdr]]

## Sources

- [[sources/rtr-day05]]
