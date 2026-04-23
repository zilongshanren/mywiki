---
tags: [source, 渲染, shader, GLSL, 导数, mipmap]
date: 2026-04-19
sources: 1
---

# Derivatives I + II（Ben Supnik / hacksoflife）

[[ben-supnik|Supnik]] 2011-01-20 的连载两篇：Part I 讲 **UV 不连续时 `dFdx/dFdy` 会返回巨大导数**，Part II 讲**在非一致控制流（`if` 分支）里做隐式 derivative/texture fetch 是 spec 未定义行为**。本地我们合并到一篇 source summary，因为两篇共用同一套硬件心智模型（2×2 quad + lock-step）。

## 摘要

**Part I**：`texture2D(sampler, uv)` 实际展开为 `texture2DGrad(sampler, uv, dFdx(uv), dFdy(uv))`，硬件用 2×2 像素 quad 的交叉差分近似导数。一旦 UV 在 quad 内出现跳变（`if(uv.x > 0.5) uv.y += 0.25;`、`floor()` 边界、tile shader 的 swizzle），差分就返回一个巨大数，采样器判定「每像素覆盖整张纹理」，选最低 mip，产生**缝隙处的 2×2 暗带 artifact**。解法：显式传 `texture2DGrad(sampler, uv_real, dFdx(uv_original), dFdy(uv_original))`——采样用跳变后的 UV，LOD 导数用原始连续 UV。评论区 Jonathan 还给了个进一步修正：对 projective（非 affine）输入，在 screen space 重新算 `px/py` 才完全连续。

**Part II**：GLSL 1.20.8 spec §8.8 明确写了「derivative 在 non-uniform conditional 内未定义」，因此下面这段可能正确也可能塞给你一排灰色伪影像素：

```glsl
if (uv.x >= 0.0)
    gl_FragColor = texture2D(sampler, uv);
else
    gl_FragColor = vec4(0.0);
```

根因是 GPU 对 if 做 **mask 化执行**——整个 if 体在 quad 所有 lane 里都跑，结果用 mask 选择；此时 quad 内部有的 lane 的 UV「写过了」、有的「没写」，基于这种状态差分没有意义。修法：**在 if 外面先算好 `dFdx/dFdy`**，分支内部调 `texture2DGrad` 把导数显式塞进去。顺带 Supnik 把「branch coherence」概念讲了一遍：**只有整个 quad 走同一边 if 才能真省指令**，否则两侧都跑、省不了。

## 关键要点

- `texture2D` ≡ `texture2DGrad(..., dFdx(uv), dFdy(uv))`；mip 选择本质是一次 screen-space 差分。
- UV 不连续（`if`、`fract`、`floor`、swizzle）→ 巨大差分 → 选最低 mip → 2×2 暗带。
- 手喂 `texture2DGrad` 用**连续**表达式的 `dFdx/dFdy`，采样用**跳变后**的 UV。
- Projective UV 还要进一步在 screen space 算导数（Jonathan 的修正）。
- GLSL spec：**non-uniform control flow 内的 derivative 未定义**；texture2D 内部隐式调 derivative，所以 if 里不能直接 `texture2D`。
- 修法：在 if 外面算 `dx = dFdx(uv); dy = dFdy(uv);`，分支里调 `texture2DGrad(s, uv, dx, dy)`。
- Branch coherence：if 分支只有 quad 一致时才真 skip，否则两条路径都跑。
- 评论区 Aras 补充：deferred lighting、screen-space decal 等基于 depth 反推 UV 的场景特别容易踩这类 2×2 artifact。

## 链接到的概念

- [[texture2dgrad-explicit-derivatives]]
- [[divergent-gradient-in-branches]]
- [[uv-precision-derivative-loss]]
- [[fwidth-derivative-antialiasing]]
- [[mipmap-generation-sampling]]
- [[ben-supnik]]

## 原文

- 链接：
  - Part I: http://hacksoflife.blogspot.com/2011/01/derivatives-i-discontinuities-and.html
  - Part II: http://hacksoflife.blogspot.com/2011/01/derivatives-ii-conditional-texture.html
- 本地：
  - `raw/articles/hacksoflife.blogspot.com/2011-01-20_derivatives-i-discontinuities-and-gradients.md`
  - `raw/articles/hacksoflife.blogspot.com/2011-01-20_derivatives-ii-conditional-texture-fetches.md`
