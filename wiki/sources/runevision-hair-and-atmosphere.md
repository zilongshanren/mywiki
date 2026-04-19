---
tags: [source, rendering, unity, hair, atmosphere, 2025]
date: 2026-04-19
sources: 1
---

# Rune Skovbo Johansen - Hair Shader & Atmospheric Perspective（runevision blog 合集）

[[rune-skovbo-johansen]] 于 2025 年 10 月 23 日在 `blog.runevision.com` 发布的一批合并贴文，同一页包含两篇值得单独归档的技术文章（以及一篇 creatures 进展、一篇 2024 年度回顾），此处只提炼其中的两篇技术内容。

## 摘要

**第一篇：Hair Shader**。作者用闲暇时间为 Unity 通用 sphere/capsule 做了一套不依赖特殊发丝网格或纹理的发丝渲染。基于 Unity Standard BRDF 做各向异性模拟——把表面近似为沿 UV-V 方向对齐的圆柱簇。共三档实现：Full Multisample（沿发丝方向旋转 50 个法线并对每个跑完整 BRDF）、Specular Multisample（只对 specular 项多采样）、Approximation（靠经验公式拟合）。权重函数用两个余弦（法线与原法线夹角的 cos × 法线与视线夹角的 cos）的乘积，即可抓到各向异性高光。已开源到 GitHub。

**第二篇：Atmospheric Perspective**。作者在日本旅行观察远山后修正了自己"远山只是朝天空色淡出"的旧认知。真实规律是：远山先趋近深蓝，再在更远处**继续变淡**趋近近地平线的苍白——原因与近地平线天空发白一致，是阳光穿过更厚空气后 Rayleigh（也许还有 Mie）散射在色空间里走出的弧形轨迹。基于此他指出游戏里常用的 *fog trick* 无法表达这段弯折：无论把雾色设成天顶蓝还是地平线白，都会在某个距离出错。工程替代方案包括 iq 的多通道指数雾、Unreal 的 Sky Atmosphere Component（基于 Bruneton-Neyret 2008）、Unity HDRP 的 Physically Based Sky。

## 关键要点

- **各向异性发丝**不必上 Kajiya-Kay / Marschner；只要沿发丝方向在 180° 扇面内多采样法线并以余弦乘积加权，就能在 Standard BRDF 之上得到可信效果。
- **性能档位**可显著降：从 50 次完整 BRDF → 50 次仅 specular → 0 次多采样但拟合公式。
- **空气透视的弯折**：距离越远，颜色从饱和蓝转向苍白，而非无限趋近单色。
- **Fog trick 的局限**：任何"朝单一颜色淡出"的方案都违反"远山大气色不会比紧贴天空还淡"的常识。
- **山面光影**：光照侧偏绿（日光 + 植被），背光侧偏蓝（只剩大气散射）——大气色**始终**存在，只是在光照侧被地表色压过。
- 作者自认**看不懂多数图形学论文**；他的方法论是观察、直觉、试错，再与原作者交流。

## 链接到的概念

- [[hair-shader-anisotropic]]
- [[atmospheric-perspective]]
- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[volumetric-fog-froxels]]
- [[spectral-rendering]]

## 原文

- URL：https://blog.runevision.com/2025/
- 本地：`raw/articles/blog.runevision.com/2025-10-23_runevision-blog.md`
- 同期重复抓取 skip：`raw/articles/blog.runevision.com/2025-10-23_runevision-blog-2.md`（月页/只含 hair），`raw/articles/blog.runevision.com/2025-10-23_runevision-blog-3.md`（归档页/仅含 hair）
