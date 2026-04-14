---
tags: [source, 渲染, 纹理, mipmap, lod, 过滤, gamemaker]
date: 2026-04-14
sources: 1
---

# GM Shaders: Mipmaps（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 1 月 20 日的短文，把 mipmap 从"把 `tf_linear` 开起来"推进到"用 bias 参数做伪景深 / 廉价 blur"的层次。

## 摘要

Mipmap 是一组 2× 递减的预生成纹理金字塔（512 → 256 → 128 → … → 1），GM 里 `gpu_set_texfilter(true)` + `gpu_get_tex_mip_enable(mip_on)` 两行即可启用，三种过滤档位 `tf_point` / `tf_linear` / `tf_anisotropic` 分别代表"廉价 / 平衡 / 最好"。内部的 LOD 选择靠 `dFdx / dFdy` 在屏幕 2×2 quad 内算出 UV 导数，再 `log2(max(|dx|²,|dy|²))*0.5` 得到浮点 LOD；由此 linear filter 会在相邻两级之间做 trilinear 混合。作者特别提醒：因为导数是 quad 内计算的，`fract(uv)` 这类不连续操作会让 LOD 选错、在接缝处糊掉，应优先 `gpu_set_texrepeat(true)` 交给硬件 wrap。

本文最值得记的是 `texture2D(sampler, uv, bias)` 的第三个可选参数——**把 bias 加到系统算出的 LOD 上，就能免费获得半分辨率采样的糊感**。从这里延伸出一系列创意用法：伪景深（按焦距调 bias）、soft drop shadow、glow，以及和小半径 blur shader 叠加得到大半径低成本效果。GM 的 `texture2DLod` 并未开放，但可以用 bias 等价替代。最后是一组限制：等向过滤多 33% VRAM、各向异性多 4×、**surface 无 mipmap**（GM 的长期痛点）、POT 方块纹理最友好、边缘 padding 对 blur 必须、discontinuous UV 是接缝元凶。结尾特意推荐 Ben Golus 的 Distinctive Derivative Differences 作为深入文章。

## 关键要点

- **LOD 选择内部靠屏幕导数**：`dFdx(uv) * tex_res` 的最大长度的 `log2` 就是 LOD，linear filter 自动在相邻两级 trilinear 混合。
- **导数在 2×2 quad 里算**：任何让 UV 跳变的操作（fract、条件分支）都会让 quad 边界炸 LOD，优先用 wrap mode。
- **`texture2D(tex, uv, bias)` 的 bias 是廉价 blur**：+1 等于半分辨率采样，支持渐变 bias 做 DOF / glow / soft shadow。
- **GM 不支持 `texture2DLod`**：但可用 bias = computed_lod - system_lod 等价替代。
- **`tf_anisotropic` 解决斜视角的模糊**：代价是 4× VRAM 和更复杂的采样过程，一般推荐默认用 linear。
- **surface 没有 mipmap 是 GM 的大坑**：意味着"用 mipmap 做 bloom"这条工业界常见路线在 GM 里行不通，Xor 公开呼吁 YoYo 团队补上。
- **POT 方块 + 留边**：纹理尺寸得是 2 的幂次方且方形，blur 时必须在 sprite 四周留足空白。
- **配套文章**：Ben Golus 的 Distinctive Derivative Differences 解决各类 mipmap artifact，Jacco Bikker 另有一种 texelFetch-based 的 LOD 选择优化。

## 链接到的概念

- [[mipmap-generation-sampling]]
- [[mipmap-moire-scanline]]
- [[sampler-filter-wrap-modes]]
- [[separable-gaussian-blur]]
- [[aliasing]]
- [[xor-shader-artist]]
- [[texel-pixel-conversion]]

## 原文

- 链接：https://mini.gmshaders.com/p/mipmaps
- 本地：`raw/articles/mini.gmshaders.com/2024-01-20_gm-shaders-mipmaps.md`
