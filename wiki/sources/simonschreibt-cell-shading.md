---
tags: [source, 渲染, 描边, sprite, cel-shading]
date: 2026-04-14
sources: 1
---

# Cell Shading（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 写于 2013 年的 Game Art Tricks 早期短文，讨论了两种完全不同尺度上的「加描边」技巧：3D 的 shell mesh extrude 和 2D 的八方向 sprite 平移。

## 摘要

文章上半段讲的是 Games Academy 项目《Tummy Trundle》里用的 3D 卡通描边：复制整个模型、反转法线、加黑材质、沿法线外推一小段，由于法线翻转你只看到从原模型里「冒出来」的黑色外壳。下半段则来自 Nicolae Berbece 口述的 2D 技巧：把 sprite 复制 8 份，染成描边色，分别向 8 个方向偏移一个像素，再叠原图。评论区顺着这两个方向发散得非常精彩：有人指出现代 engine 通常直接在 vertex shader 里 extrude，不需要实体 shell mesh；有人解释非 manifold mesh 会让外推出现裂缝，要用**把 smooth normal 烤进顶点色**的 trick 绕开；有人提到 Borderlands 2 用的是 screen-space Sobel 边缘检测（跑在 G-buffer 的 normal 上），这和几何外推是完全不同的风格化路径。Simon 自己承认，这招在现代 engine 里更多是**作为教学式示范**而不是首选实现。

## 关键要点

- 3D 描边的经典做法：复制模型 + 反转法线 + 沿法线外推 + 黑材质
- 现代实现改为 vertex shader 外推 + front-face cull 替代反转法线
- Non-manifold mesh 会导致外推出现裂缝；把 smooth normal 烤进顶点色可绕开
- 2D sprite 的 8 方向偏移是一种等价的形态学膨胀，优于 Sobel（无锯齿、保留 soft alpha、小细节会变成花纹）
- Borderlands 2 采用的是 screen-space Sobel on normals——和几何 shell 走的是两条不同路径

## 链接到的概念

- [[sprite-outline-8-direction]]
- [[cel-shader-outline]]
- [[depth-texture-silhouette]]
- [[simon-trumpler]]

## 原文

- 链接：https://simonschreibt.de/gat/cell-shading/
- 本地：`raw/articles/simonschreibt.de/2013-01-21_simonschreibt.md`
