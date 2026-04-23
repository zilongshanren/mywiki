---
tags: [source, 渲染, 延迟渲染, g-buffer, x-plane]
date: 2026-04-19
sources: 1
---

# Yet Another This-Is-Our-GBuffer-Format Post（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 12 月的 G-Buffer 布局自述，是 X-Plane 10 切延迟渲染管线时一份具体到字节的记录。

## 摘要

X-Plane 的材质模型比多数商业引擎简单（没有 forward 下的 shader 联邦），所以 G-Buffer 要装的「额外材质信息」只有一个 **shininess 比例**。但它有两条非典型需求：十年来的 **additive emissive 贴图**必须保留、**艺术家重度使用 alpha translucency**。最终布局是 4 张 RT、16 字节：RGBA8 albedo+alpha / RG16F 眼空间法线 X,Y（Z 重建，不存符号）/ RG16F 深度 + shadow×256+shine 打包 / RGBA8 emissive+alpha。shadow 与 shine 两个需要 ~8 bit 的参数塞进一个 16F 通道，走 `256.0×shadow + shine` 的浮点打包——利用 float 指数作为字段位分配器，shadow 满时 shine 降到 2 bit 却被遮住看不见。16F 深度对近距阴影够用，但不适合行星尺度的位置重建——Supnik 建议绕开 G-Buffer 直接用模型视图空间的球体方程求交。emissive 的 alpha 因 GL 没有 3 通道可渲染格式 + MRT 场景不可用 extended blend 而被迫浪费。OS X 10.5 没 RG 纹理的平台走 4×RGBA_16F 后备，fill rate 最少降 20%。

## 关键要点

- 4 张 MRT / 16 字节：albedo+a、法线 X/Y、深度+(shadow,shine)、emissive+a。
- **浮点字段打包**：`256*shadow + shine` 用 16F 指数做位分配器，shadow 遮蔽 shine 的条带。
- 法线不存 Z 符号（依赖背面剔除 + art asset 的有限外推）。
- 16F 深度不够行星尺度，行星位置重建走解析几何。
- emissive 需要 replace 语义 → alpha blend 必须开 → alpha 通道被 GL 吃掉无法复用。
- OS X 10.5 走 4×RGBA_16F 后备，VRAM 翻倍、fill rate −20%。

## 评论区补充

- SebH 提到 Crytek best-fit normal 的压缩方法——Supnik 读过论文，决定暂不引入（X-Plane 的 normal map 是切线空间且外推有限）。
- Cam 问为何 emissive 要 alpha：Supnik 解释必须靠 alpha 做 replace 操作抹掉覆盖物的既有亮像素。

## 链接到的概念

- [[xplane-gbuffer-format]]
- [[deferred-rendering]]
- [[multiple-render-targets]]
- [[tangent-space-normal-mapping]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/12/yet-another-this-is-our-gbuffer-format.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-12-05_yet-another-this-is-our-gbuffer-format-post.md`
