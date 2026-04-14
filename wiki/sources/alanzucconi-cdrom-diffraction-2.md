---
tags: [source, rendering, shader, 物理光学, 衍射, unity]
date: 2026-04-14
sources: 1
---

# CD-ROM Shader: Diffraction Grating – Part 2（Alan Zucconi）

[[alan-zucconi|Alan Zucconi]] 2017 年 7 月的文章，在 Unity Surface Shader 里把 CD-ROM 表面的衍射彩虹实现出来，核心是"从 UV 推切向" + 「$T \cdot L, T \cdot V$ 光栅方程」。

## 摘要

CD-ROM 的彩虹色反射来自同心圆排列的微细沟槽：它们间距接近可见光波长，构成物理衍射光栅，不同波长在不同角度发生相长干涉。本文把 grating 方程 $\lambda_n = d|\sin\theta_L - \sin\theta_V|/n$ 落到 shader 代码里。关键难点是"局部切向方向"——模型法线对每块 CD 面都指向外，无法区分"沿槽 vs 垂直于槽"，切向才能。作者用一个妙招：直接把 UV 坐标 remap 到 $[-1, 1]$、取 normalize 得到径向向量，再旋转 90° 得到切向，这一步必须在 surf 函数里算好传给 lighting 函数。合起来只需要几个 `dot`、一个 8 阶循环、每阶调用一次 [[spectral-zucconi-rainbow|`spectral_zucconi6`]]，就能得到随机视角下完整的 CD 彩虹反射。

## 关键要点

- Grating 方程 $\lambda = d|\sin\theta_L - \sin\theta_V|/n$ 直接用 $T\cdot L$、$T\cdot V$ 得到两个 sine
- 切向方向从 UV 坐标算：`uv*2-1` → normalize → rotate 90° → 再 object→world 变换
- UV 在 Surface Shader 的 lighting 函数里不可见，必须在 surf 函数里提前 bake 成全局变量
- 对 $n=1\ldots 8$ 阶累加 + `spectral_zucconi6` 转 RGB + saturate
- 和各向异性 BRDF 相比，这个方法直接抓住了 grating 的物理本质，省略了整个微表面统计框架

## 链接到的概念

- [[diffraction-grating-shader]]
- [[spectral-zucconi-rainbow]]
- [[physically-based-shading]]
- [[shader-vector-math-primer]]
- [[coordinate-spaces]]

## 原文

- 链接：<https://www.alanzucconi.com/2017/07/15/cd-rom-shader-2/>
- 本地：`raw/articles/alanzucconi.com/2017-07-15_cd-rom-shader-diffraction-grating-part-2-alan-zucconi.md`
