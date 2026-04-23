---
tags: [source, rendering, 反走样, 超采样, 2d, sd]
date: 2026-04-19
sources: 1
---

# Making an HD 2D game look good on an SD television（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen|Joost van Dongen]] 2011 年 11 月的文章，讲 Swords & Soldiers 和 Awesomenauts 在老 CRT 电视 SD 分辨率下如何用超采样下采样解决 2D 细节闪烁。

## 摘要

2D 游戏美术按 1920×1080 画好，直出到 720×576 的 CRT 上直觉应该"更清晰"，但实际结果是"太清晰"——1 像素宽的美术细节会随角色移动闪烁，Photoshop 里预画好的 edge anti-aliasing 因 SD 采样错过 HD 像素而完全丢失。3D 游戏有 mipmap 和实时 AA，2D 游戏没有。解法是反向使用 supersampling：**内部渲染到高于 SD 的分辨率，再 box filter 下采样到屏幕**。Joost 实测内部 1.5× 分辨率（1080×864 → 720×576）已经足够消除闪烁——早期用 2× 太贵到 SD 模式帧率比 HD 还差。评论区问"何不加载时 resample 纹理"，Joost 给了三条反对：（1）DDS decode→resample→re-encode 流程复杂且 encoder 参数难调；（2）分辨率砍半会放大 DDS 压缩 artifact，角色动画显眼；（3）200MB 纹理全过一遍流程加载时间过长。运行时 supersampling 保留了"同一套资源跨 HD/SD 平台"的简单流水线。

## 关键要点

- **2D 没有 mipmap/实时 AA**：降采样时 Photoshop 里预画的 edge blend 会丢。
- **直出 HD→SD 的 artifact**：1 像素细节落在采样网格外时闪烁，移动下尤其明显。
- **解法 = SSAA 的下采样版**：内部渲染到更高分辨率 + box filter 回到 SD。
- **1.5× 是甜点**：1080×864 → 720×576 已经够；2× 太贵，早期 SD 帧率因此比 HD 差。
- **为什么不预先 resample 资源**：DDS 编码难、压缩 artifact 放大、加载时间长——运行时 supersampling 更简单。
- **跨平台流水线不变**：同一套 HD 资源跑 HD 和 SD 两种输出。

## 链接到的概念

- [[hd-to-sd-supersample-downscale]]
- [[msaa-ssaa]]
- [[temporal-supersampling]]
- [[image-resampling-filters]]
- [[aliasing]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/11/making-hd-2d-game-look-good-on-sd.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-11-19_making-an-hd-2d-game-look-good-on-sd-television.md`
