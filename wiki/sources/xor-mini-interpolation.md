---
tags: [source, 渲染, shader, 纹理, 滤波]
date: 2026-04-14
sources: 1
---

# Mini: Interpolation（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 10 月的 Mini 系列一篇，主题是**纹理滤波**——nearest / linear / cubic 的本质都是不同的**插值方案**，而且都可以用 linear 采样器外加几行 GLSL 自己实现。

## 摘要

文章先给出 GameMaker 里开启 linear filtering 的 API，顺带踩一脚 alpha 混合 bug（alpha 也在线性混合，导致不透明像素落到半透明背景上也会被吃掉亮度），用 `gpu_set_blendmode_ext_sepalpha` 做 premultiplied-alpha 式的补救。重点在后半段：nearest 只是把像素坐标 `floor` 然后加 0.5 居中采样，**linear 采样器可以完美复现 nearest**；cubic 则是把 sub-pixel 分数部分套上 `3x² - 2x³`（smoothstep）再回代，得到比纯 linear 更圆的过渡；更奢侈的 quintic `6x⁵ - 15x⁴ + 10x³` 也只多几条乘法。作者把 cubic 公式和 [[shader-color-interpolation]] 里的 lerp 串起来——一个公式在滤波、smoothstep、value noise 平滑上都要用到。最后还介绍了 mipmap：`texture2D(sampler, uv, lod)` 的第三参数控制 LOD，可以做 blur/bloom。GameMaker 特有的限制是 mipmap 对 surface 和 font 不生效。

## 关键要点

- **Linear 滤波的 alpha 坑**：默认 blend 模式会把 alpha 和 color 一起插值，导致不透明像素看起来有黑边。premultiplied alpha + `(one, inv_src_alpha, one, one)` 是标准解。
- **手工 nearest**：`floor(coord/texel)` 然后 `(pixel + 0.5) * texel` 回代，半个纹素居中。
- **Cubic filtering**：`subpixel*subpixel*(3 - 2*subpixel)` 替换线性 sub-pixel，换 linear 采样器得到更圆的过渡。
- **Quintic 备选**：`x³(x(6x-15) + 10)`——在噪声函数页里用得更多，见 [[classic-shader-noise]]。
- **Mipmap API**：`gpu_set_tex_mip_enable(true)` + `texture2D(..., lod)` 手动 LOD，可用于 blur/bloom；GameMaker 里不支持 surface 和 font。
- **公式复用**：`3x²-2x³` = smoothstep，也等于 value noise 的 cubic 插值；一条公式贯穿滤波与程序纹理。

## 链接到的概念

- [[shader-color-interpolation]]
- [[classic-shader-noise]]
- [[sampler-filter-wrap-modes]]
- [[alpha-blending]]
- [[alpha-compositing]]
- [[texel-pixel-conversion]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-interpolation-1430549
- 本地：`raw/articles/mini.gmshaders.com/2022-10-28_mini-interpolation.md`
