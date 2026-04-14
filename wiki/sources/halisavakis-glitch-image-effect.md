---
tags: [source, 渲染, unity, shader, glitch, 后处理]
date: 2026-04-14
sources: 1
---

# My take on shaders: Glitch image effect (Harry Alisavakis)

[[harry-alisavakis]] *My take on shaders* 系列 2017-09-23 的一篇。Alisavakis 承认自己"研究了很久各种 glitch 实现"，最后归纳出一个三层叠加 + 单旋钮控制器的配方，这一篇是他想一次性把这套东西讲清楚的成品。

## 摘要

他把 glitch 视觉拆成三个独立失真的叠加：**（1）两张 [[random-stripes-mask-shader|随机条纹 mask]]**（一张向右偏移、一张向左偏移）做水平撕裂；**（2）`sin(uv.y * _WavyDisplFreq)` 合成的波浪 UV 位移** 让画面像松掉的磁带一样纵向抖动（这里他用一个 `lerp(red, green, (sin+1)/2)` 的 R/G 双通道遮罩同时承载上下两个位移方向）；**（3）经典 [[chromatic-aberration-post|色差]]** 把 R/G/B 三通道分别用不同偏移采样。三者都先算到 `displUV` 再交给色差三次采样——顺序关键。

第二部分是他引以为傲的"控制器": 引入单一 float `_GlitchEffect`，在 shader 里用 `frac(_GlitchEffect)` 对 0.33 / 0.5 / 0.8 三个阈值分档，逐步解锁位移量、色差量、条纹 fill，让外部脚本只要推一个标量就能从"全无失真"平滑过渡到"最失真"，得到节奏化的"时而好时而坏"的 glitch。他自己点评说"most confusing part could be the controller, but that's just something I figured out after playing around for a while"，阈值数字完全是经验值。

## 关键要点

- **三件套组合** = 两套随机条纹 mask + 波浪 UV 位移 + 色差，单 pass 合并。
- **顺序**: 位移先算好 `displUV` → 色差三次采样（R/G/B 各用不同偏移）。倒过来会糊。
- **波浪位移用 R/G 双通道 mask** 同时承载上下偏移方向，`displ.r * up - displ.g * down` 合成连续位移向量。
- **`_GlitchEffect` 单旋钮控制器** 把 9 个 uniform 压缩到 1 个，用 `frac()` 做循环、用阈值 `< 0.33 / < 0.5 / < 0.8` 分档解锁；数字拍脑袋但工程有意义：便宜的失真先出现，贵的失真最后出现。
- **lerp in-range**: 每段内部 `lerp(0, target, frac * 系数)` 让这档内部也平滑放大，而不是硬开关。
- 合并到单 pass 是为了移动 GPU 友好，和 [[unity-postprocessing-adventures|后处理优化]] 原则一致。
- 结尾附了一个 UE4 material 的等价实现截图（没贴代码），说明这套结构不是 Unity 独占。

## 链接到的概念

- [[glitch-image-effect]]
- [[random-stripes-mask-shader]]
- [[uv-displacement-image-effect]]
- [[chromatic-aberration-post]]
- [[unity-image-effect-basics]]
- [[shaping-functions]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-glitch-image-effect/>
- 本地：`raw/articles/halisavakis.com/2017-09-23_my-take-on-shaders-glitch-image-effect.md`
