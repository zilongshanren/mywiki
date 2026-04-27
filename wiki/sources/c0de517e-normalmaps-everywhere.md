---
tags: [source, 渲染, 法线贴图, mipmap, 反走样, 材质]
date: 2026-04-27
sources: 1
---

# Normalmaps Everywhere（C0DE517E）

[[angelo-pesce]] 发表于 2012 年 2 月的文章，深入分析为何法线贴图在高频细节表达上有根本性缺陷，并提出遮蔽贴图和 exponent 贴图作为替代方案。

## 摘要

文章从一个反直觉的问题出发：把高分辨率网格烘焙成低多边形 + 法线贴图后，走样为什么"消失"了？答案是 mipmap 的平均把法线滤平了，高频细节就此丢失。Pesce 将这一现象系统化：法线贴图属于**导数度量**，在缩小时会趋向平坦，而应该在缩小时保持的视觉效果（皮肤毛孔、汗珠、铆钉）根本无法由法线贴图正确表达。他进而提出用**遮蔽贴图**（occlusion）和**高光指数贴图**（exponent/gloss map）来编码不同类型的亚像素细节，并引用 COD:Black Ops 的 LEAN/CLEAN 方案作为工业界的具体落地案例。

## 关键要点

- **法线贴图 mipmap 的根本问题**：法线贴图是表面导数，mipmap 平均后趋向 [0,0,1]，即平坦。细节只要缩到几个像素宽就消失，而超采样（MSAA）仅提供深度/几何采样，不增加着色采样，无法挽救。
- **预滤波 vs 后滤波**：对 diffuse 可以先做光照再平均（后滤波），法线贴图则是先平均再做光照（预滤波），这是不等价的，预滤波会引入误差。
- **遮蔽贴图（occlusion map）**：在光照之后才应用，可以正确 mipmap，能表达任何形状的细节（越尖锐的凹陷越遮蔽越深）。适合皮肤毛孔、针脚等面向各方向的细节。
- **Exponent/Gloss 贴图**：圆形高光形状（铆钉、汗珠）从远处看相当于降低了高光指数（增大散射锥）——这本来就是材质建模的正确做法，无需法线贴图。
- **COD:Black Ops LEAN/CLEAN 方案**：在 mipmap 生成时计算法线束的方差，用方差调整 gloss 量写入 mip，运行时零额外开销。这是工业级"预滤波 BRDF"的早期实例。
- **可变尺度材质**：可以在 mip 层级间平滑过渡，近处用法线贴图+高 exponent，远处用 gloss 贴图表达统计平均效果。

## 链接到的概念

- [[tangent-space-normal-mapping]]
- [[normal-map-blending]]
- [[mipmap-generation-sampling]]
- [[microfacet-brdf]]
- [[physically-based-shading]]

## 原文

- 链接：https://c0de517e.blogspot.com/2012/02/normalmaps-everywhere.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-02-01_normalmaps-everywhere.md`
