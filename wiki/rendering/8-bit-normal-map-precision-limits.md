---
tags: [渲染, 法线贴图, 精度, 高光, 量化]
date: 2026-04-19
sources: 1
---

# 8-bit 法线贴图的精度极限

切线空间法线贴图存 RG8（或 RGB8）时，每通道只有 256 级。对多数漫反射表面足够，但一旦美术把 specular exponent 拉高——[[ben-supnik|Supnik]] 2011 年 5 月在 X-Plane 上踩到的就是这种情况——高光会出现**明显的法线量化台阶**，表现为颗粒感或条带。

## 为什么 specular 放大量化误差

高光的 Blinn/Phong 形式 `max(N·L, 0)^k` 里，指数 `k` 实际上是**对法线微小偏转的放大器**。在曲线顶点（`N·L ≈ 1`）附近微小变动被陡峭导数放大：把 RG 通道加一个最小单位（1/255），法线方向的角度变化虽然只有百分之一度量级，经 `^1024` 后亮度差却可能达到 2–8 个最小显示单位。Supnik 画出 `^128 / ^1024 / ^4096` 的衰减曲线：

- `^128`：每 5 单位偏移丢 6 单位亮度，温和；
- `^1024`：第一单位偏移就丢 ≈ 2 单位亮度；第二单位丢 ≈ 8；
- `^4096`：最敏感，顶点附近几乎无法形成平滑过渡。

当再叠加 **linear lighting**（见 [[linear-lighting-pipeline]]，无 gamma 曲线隐藏误差）与 HDR specular（X-Plane 常把值「顶到」2–3×），观感损失进一步放大。

## 缓解手段的工程权衡

Supnik 的选项（也是其他引擎走过的路）：

1. **Best-Fit Normals / 类似压缩**：用满 8-bit×3 通道的比特空间，每方向查表选最佳缩放，见 [[compact-normal-encoding]]。BFN 在 RGB8 预算内就能把高光稳住，代价是编码阶段一张 3D LUT。
2. **加精度**：升 `RG16`（每通道 16-bit），直接消灭问题；代价是 `BA` 通道若原本承载别的效果会被挤掉。
3. **蓝通道当指数**：RG 存扰动、B 存一个 scalar，让法线贴图变成某种「8.8 浮点」。在法线**小幅扰动**时（Supnik 观察：切线空间贴图大多时间扰动小）用 B 扩大 RG 的有效动态范围。缺点：扰动大时精度反而掉；对「小扰动要高精度」这类分布才划算。
4. **全局 gamma 曲线压 RG**：牺牲大扰动换小扰动，和方案 3 类似但不独立存指数。Supnik 自己判断**不会产品化**，因为大扰动丢精度更显眼。
5. **不要这么干（告诉美术）**：最诚实的选项，但美术不爱听。

## 与 G-Buffer 法线的关系

这篇谈的是**法线贴图**（作为纹理读入 shader 后的源头精度），不是 [[compact-normal-encoding|G-Buffer 里写出的紧凑法线]]。两者独立：G-Buffer 编码再好，上游 RG8 法线贴图不够用，下游依然条带。工程上通常并行考虑——G-Buffer 选 Lambert azimuthal 或 octahedral，贴图侧选 BFN 或升 RG16。

## 相关

- [[compact-normal-encoding]] —— G-Buffer 侧 2 通道紧凑编码
- [[tangent-space-normal-mapping]]
- [[linear-lighting-pipeline]]
- [[color-banding]]
- [[normalised-blinn-phong-shader]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-limits-of-8-bit-normal-maps]]
