---
tags: [渲染, 透明, 合成]
date: 2026-04-14
sources: 1
---

# Alpha Compositing（α 合成）

**α 合成**是把多个半透明图层组合成最终画面的数学运算。它是 [[alpha-blending]] 的更一般形式——[[alpha-blending]] 讨论的是 **如何把一个物体画到 framebuffer 上**，α compositing 讨论的是 **如何把多个带 alpha 的图层组合起来、且结果能作为下一步的输入**。

## Alpha 到底是什么

```
α = opacity × pixel_coverage
```

- **Opacity（不透明度）**：物体本身阻挡了多少光。
- **Pixel coverage（像素覆盖率）**：物体在该像素上占了多大面积——矢量图形抗锯齿的来源，文字渲染几乎完全依赖它。

一个 60% 不透明、覆盖像素 30% 面积的物体，在该像素的 α = 0.18。**一旦相乘，二者不可区分**——这是「alpha = opacity」这种口头简化的出处。

## 「Over」算子：合成的基本操作

Porter & Duff 1984 经典论文给出 12 个合成算子，最常用的是 **source over destination**（Sa 在 Da 之上）：

```
R_A   = S_A + D_A × (1 - S_A)
R_RGB × R_A = S_RGB × S_A + D_RGB × D_A × (1 - S_A)
```

推导核心：把问题分成两部分——「有多少背景光透过来」（用 transparency 相乘得 `(1-Sa)(1-Da)`）和「每层贡献多少自发光」（颜色 × 自身 α）。

## Premultiplied Alpha：为什么值得

非预乘形式里第二个方程需要除以 `R_A`，下一轮合成又要乘回来——不雅、还会在 filter/resample 时产生错误。解决方案：存储 `(S_RGB × S_A, S_A)` 而不是 `(S_RGB, S_A)`。方程立即简化为：

```
R'   = S' + D' × (1 - S_A)
R_A  = S_A + D_A × (1 - S_A)
```

**预乘 α 的好处**：
- 没有 division，合成可结合（associative）——不同顺序得到相同结果。
- 双线性滤波 / mipmap 生成不会在边缘出现「黑边」或「彩边」。
- 正确处理「零 α 但有自发光」的情况（如 additive 粒子），非预乘形式做不到。
- **GPU 的 `GL_ONE, GL_ONE_MINUS_SRC_ALPHA` 混合态就是预乘 over**，这是「正确的默认值」。

## 与 [[alpha-blending]] 的关系

| 维度 | Alpha Compositing | Alpha Blending（渲染管线层） |
|---|---|---|
| 讨论层次 | 数学 / 图像合成 | 管线状态（blend state） |
| 输入 | 两张带 α 的图像 | fragment vs framebuffer |
| 难点 | 方程推导、pre/straight 区分 | 深度排序、OIT |
| 预乘形式 | 首选 | GPU blend state 原生支持 |

## 关键教训

> 非预乘 α 是给人用的（美术软件友好），预乘 α 是给管线用的（数学上正确）。**引擎内部一律预乘，导出 PNG 时再 unpremultiply。**

## 相关

- [[alpha-blending]] — 硬件 blending state
- [[rasterization]] — 覆盖率计算
- [[aliasing]] — 部分覆盖的反走样用途
- [[bartosz-ciechanowski]]

## Sources

- [[sources/ciechanow-alpha-compositing]]
