---
tags: [source, rendering, msaa, edge-detection, deferred-rendering, light-prepass]
date: 2026-04-27
sources: 1
---

# Edge Detection Trick（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 发表于 2010 年 3 月的短文，转载并补充 Benualdo 在 Light Pre-Pass 论坛中提出的 MSAA 边缘检测技巧。

## 摘要

文章介绍了在支持 MSAA 表面线性采样的平台上检测边缘像素的廉价方法：对 normal buffer 同时做 POINT 采样和 LINEAR 采样，两者之差的绝对值超过阈值时说明当前像素跨越几何边缘，需要以超采样精度执行光照。Linear 采样得到的平均法线可在同一 pass 中用于非边缘像素的光照，避免额外 pass。评论中还出现了一种用 3D 体积纹理 mipmap 自动检测颜色变化率的边缘方法（利用硬件 LOD 计算替代 ddx/ddy 指令来节省 ALU），以及如何用 stencil buffer 将边缘标记一次、多个光源复用的优化方案。Engel 强调深度值必须与法线打包在同一纹理才能正确处理"法线相同但深度不同"的边缘案例。

## 关键要点

- POINT vs LINEAR 法线差值做边缘检测，eps 阈值控制误报率
- 深度必须打包进同一张贴图（或同样处理），防止法线相同但深度跳变的漏检
- Linear 采样值可双用：检测边缘 + 非边缘像素光照，节省一个 pass
- 体积纹理 mipmap 技巧：将颜色值用作 3D 纹理坐标，让硬件 mip 选择来衡量颜色变化率，速度快于手写 ddx/ddy
- 边缘 stencil 仅生成一次，多个光源 pass 通过 stencil ref 复用，避免每光源重复检测

## 链接到的概念

- [[rendering/msaa-ssaa]]
- [[rendering/deferred-rendering]]
- [[rendering/tiled-light-prepass]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2010/03/edge-detection-trick.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2010-03-20_edge-detection-trick.md`
