---
tags: [source, 渲染, gamma, srgb, 光照, 量化]
date: 2026-04-19
sources: 4
---

# Gamma and Lighting 三部曲 + The Value of Gamma Compression（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 11 月连发四篇关于 gamma 的文章：三部曲 *Gamma and Lighting Part 1–3* 讨论 X-Plane 里 gamma-correct 渲染的工程实践，紧跟一篇 *The Value of Gamma Compression* 用一组量化对比图实证「为什么不能把美术资产直接存成 linear」。本源摘要把四篇合并，因为它们共用一个论点链。

## 摘要

**Part 1 · Color Sync**：24-bit framebuffer 下所有可用色彩空间都是非线性的——不是因为 CRT 电子学历史遗留，而是因为 8 bit/ch 不够线性编码人眼的感知动态范围。sRGB 刻意非线性是「用有限 code points 最大化感知覆盖」。工程上要保证艺术家监视器校准正确、整条资产管线追踪颜色空间（PNG 用 gAMA chunk）、引擎读入时要么不破坏颜色要么显式转换。X-Plane 采取的是在加载时重采样到用户显示器色彩曲线的「便宜做法」，代价是牺牲精度换 fill rate——作者自己承认这应该改成 shader 里做转换。

**Part 2 · Working in Linear Space**：光照累积必须在 linear 域，因为光是加性的而 sRGB RGB 相加不等于亮度相加。正确流程是 sRGB → linear → 光照累积 → linear → sRGB。`GL_EXT_texture_sRGB` 让 texel fetch 在 filtering 之前解码，`GL_ARB_framebuffer_sRGB` 让 fragment 写出在 blend 之后 encode——两个扩展修正了 shader 外你无法干预的两个硬件阶段。

**Part 3 · Errata**：展开了多 pass 光照累积的三条实现路径——详见 [[linear-lighting-pipeline]]。顺带记录了 OS X 10.5 vs 10.6 framebuffer 色彩配置管理的差异：10.5 整个 framebuffer 用设备 profile，10.6 每个窗口可以用 `HIWindowSetColorSpace` 设独立 profile，WindowManager 跨设备做 color conversion。

**The Value of Gamma Compression**：用实图回答「为什么不直接存 linear」。一条灰阶渐变在 sRGB 和 linear 两种空间里分别量化到 16 / 8 / 6 / 5 bit。sRGB 在 8 bit 下几乎无色带、5-6 bit 仍可接受；linear 在 8 bit 下暗部可见明显 [[color-banding|色带]]，6-5 bit 下暗部彻底坏掉（DXT 的 5-6-5 key 色场景）。结论：**gamma 是朋友**——虽然给光照 shader 添乱，但在 ≤8 bit 预算下它把精度砸在人眼分辨得出的地方。

## 关键要点

- 人眼对光强响应近似对数，暗部更敏感；sRGB 的非线性曲线和这个感知曲线大体对齐，不是 CRT 遗物。
- 美术资产管线要**追踪**颜色空间——要么全 pipeline 约定为 sRGB（X-Plane 的选择），要么给每个 asset 打 tag。
- Gamma-correct lighting 需要 linear 域累积；三条路径：单 pass shader 累加 / 多 pass + sRGB framebuffer blend / 多 pass + HDR float RT。
- `framebuffer_sRGB` 扩展的精髓是让 blend 阶段的数学与存储语义对齐，而不是换「颜色空间」。
- 压缩纹理（DXT/BC 的 5-6-5 endpoints）在 linear 存储下暗部会彻底崩：结论是**资产只要走 8 bit 及以下通道就必须是 sRGB 编码**。
- OS X 10.6 起每个窗口独立 color profile，跨多显示器要 `HIWindowCopyColorSpace` / `HIWindowSetColorSpace` 手动管理。

## 链接到的概念

- [[linear-lighting-pipeline]]
- [[gamma-correction-srgb]]
- [[color-space]]
- [[color-banding]]
- [[alpha-blending]]
- [[srgb-premultiplied-alpha-compression]]

## 原文

- 链接：
  - <http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-1-color-sync.html>
  - <http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-2-working-in.html>
  - <http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-3-errata.html>
  - <http://hacksoflife.blogspot.com/2010/11/value-of-gamma-compression.html>
- 本地：
  - `raw/articles/hacksoflife.blogspot.com/2010-11-22_gamma-and-lighting-part-1-color-sync.md`
  - `raw/articles/hacksoflife.blogspot.com/2010-11-22_gamma-and-lighting-part-2-working-in-linear-space.md`
  - `raw/articles/hacksoflife.blogspot.com/2010-11-22_gamma-and-lighting-part-3-errata.md`
  - `raw/articles/hacksoflife.blogspot.com/2010-11-23_the-value-of-gamma-compression.md`
