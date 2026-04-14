---
tags: [source, rendering, pbr, blinn-phong, 教学, 艺术家]
date: 2026-04-14
sources: 1
---

# An educational, normalised, Blinn-Phong shader（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 12 月发表的一篇"教学型"博客：他从自己的 shader 工具箱里翻出一个**归一化 Blinn-Phong** FX Composer 工程，把每一个 PBR 组件都做成可切换开关，给工作室的美术同事讲清楚"为什么我们要从旧 Blinn-Phong 迁到 PBR"。

## 摘要

文章围绕一个 FX Composer 工程逐项拆解归一化 Blinn-Phong 的每个 PBR 组件。**归一化项** $(specPower+2)/8$ 让高光越尖越亮，对应能量守恒直觉：镜面反射总能量恒定，粗糙表面把同样的能量铺开、光滑表面聚成一点，所以峰值更亮。文章随后逐项演示 gloss map（如何把 $[0,1]$ 映射到 spec power，是否用 power 还是 linear）、**gloss 贴图的线性化**（gloss 如 albedo 一样应当从 sRGB 解码，否则会让高光随粗糙度增长过快）、Fresnel 近似（Schlick 式 $F_0 + (1-F_0)(1-L\cdot H)^5$、金属 vs 非金属颜色分型）、环境反射（预过滤 cubemap + mip 选级）、specular × NdotL 的正当性（NdotL 属于 lighting 方程、对 specular 也生效）、以及 **Toksvig 型 specular AA**——从 mipmap 过的法线长度估计子像素粗糙度、反向推高 roughness 来补偿高光走样。最后给了一个 Reinhard tonemap 开关演示归一化模型如何必然需要 HDR 管线。文章自始至终都在**用图片对比 on/off**，目标读者是艺术家而不是图形程序员。

## 关键要点

- **归一化**的物理含义：$(specPower+2)/8$ 把 Blinn-Phong 的能量标定到半球积分为 1；spec power 越大 → 峰值越亮 → 和"镜面反射是同一份能量聚焦"的直觉吻合。
- **"彻底关掉高光"这件事和归一化天然冲突**。即使 specPower=0，归一化项最小值也是 0.25。美术往往要一个 specular mask；Anagnostou 给的折中是用 `gloss == 0` 作 mask。
- **Fresnel 和"能量守恒"的关系被原作者 2013 年记错了**：评论区（应是 Naty Hoffman 或同级别）指出 Fresnel 不会破坏能量守恒——现实材料本身就有 Fresnel。作者承认自己引用的是老 SIGGRAPH 课程，改正。
- **Gloss 贴图的线性化**：gloss 和 albedo 一样由美术在 sRGB 空间绘制，如果不做 $\gamma$ 解码就用到 pow 映射，会让高光随 gloss 增长过快、不可控。线性化后的曲线更平缓。
- **Deferred shading 下的 specular color 困境**：全彩色 spec 需要额外 G-Buffer 通道；多数引擎用单色 spec 退化，金和铜等特定有色金属走 forward pass。
- **Toksvig AA** 是最便宜的 specular 走样解：从 mip-averaged 法线长度反推子像素粗糙度、自动降低 spec power，移动时的高光沸腾肉眼可见改善。

## 链接到的概念

- [[normalised-blinn-phong-shader]]
- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[kostas-anagnostou]]
- [[color-space]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2013/12/23/an-educational-normalised-blinn-phong-shader/
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-12-23_an-educational-normalised-blinn-phong-shader.md`
