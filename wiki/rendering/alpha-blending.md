---
tags: [渲染, 透明]
date: 2026-04-05
sources: 2
---

# Alpha Blending（透明混合）

**半透明物体与已有 framebuffer 颜色的混合**：

```
C_final = C_src × α_src + C_dst × (1 - α_src)
```

（这是最常见的 SrcAlpha + OneMinusSrcAlpha 混合。）

这是 [[alpha-compositing|Porter-Duff source-over]] 算子在硬件 blend state 上的实例化。如果纹理和 framebuffer 用 **预乘 α**，GPU 的 blend state 可以直接写成 `GL_ONE, GL_ONE_MINUS_SRC_ALPHA`——这是数学上正确且可组合的默认值。

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

## 线性空间问题

blend 必须在 **线性色彩空间** 里做。如果在 sRGB 编码值上直接混合，红绿过渡会在中间出现不自然的变暗——参见 [[color-space]]。

## 相关

- [[alpha-compositing]] — 合成数学的完整推导
- [[color-space]] — 混合必须在线性域
- [[compute-vs-raster-points]] — 固定功能 blending 的 in-order 队列瓶颈
- [[fizzle-lod-fading]] — deferred 管线下用 discard 噪声替代 alpha blending 做 LOD 过渡
- [[z-buffer]]
- [[early-z-late-z]]
- [[fragment-shader]]
- [[hsr-tbdr]]
- [[dither-alpha-clipping]] —— 用不透明物 + Bayer 阈值 discard 伪造半透，规避 alpha blending 的排序和深度问题
- [[deferred-alpha-lighting]] —— deferred 管线下透明物体打光的四条路径
- [[dual-depth-buffer-thickness]] —— 用 `Min` 混合在一个 pass 内求厚度
- [[scatter-bokeh-dof]] — premultiplied additive blend + 最终除法归一的近似 OIT，用于 scatter bokeh 精灵累加

## Sources

- [[sources/rtr-day05]]
- [[sources/ciechanow-alpha-compositing]]
