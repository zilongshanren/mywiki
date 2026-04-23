---
tags: [source, 渲染, shader, mipmap]
date: 2026-04-19
sources: 1
---

# How To Change Your UV Map on the Fly（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 2 月的 shader 技巧帖，讲如何在 fragment shader 里动态打乱 UV 的同时不让 LOD 选择爆炸。

## 摘要

动机是用 shader 随机化 UV（swizzle / fract）来打破纹理重复感，但最简单的写法会在 UV 跳跃处产生一条糊掉的像素带。Supnik 先讲清原因：GPU 用 2×2 quad 交叉差分推导 `dFdx`/`dFdy`，采样器按这个差分选 mip——UV 一旦不连续，quad 差分瞬间暴涨，硬件判定「该采最低 mip」，那一像素就用最粗 LOD 渲染。解法是 `GL_ARB_shader_texture_lod` 里的 `texture2DGradARB`：把采样坐标与 LOD 导数**解耦**，采样用打乱后的 UV，LOD 用原始连续 UV 的导数。NVIDIA / ATI 对不连续 UV 的具体行为不同但都会出 artifact，显式导数同时摆平两家。文末顺带提醒：隐式导数在 non-uniform control flow 里是 undefined——Supnik 怀疑他遇到的许多 shader bug 都源自同 quad 内 branch 走向不一致。

## 关键要点

- GPU 通过 2×2 quad 交叉差分计算 dFdx/dFdy；采样器用差分选 mip。
- `fract()` / swizzle 造成的不连续会让差分剧烈跳跃 → 错误 LOD。
- `texture2DGradARB(tex, uv_modified, dFdx(uv), dFdy(uv))` 用原始 UV 的导数驱动 LOD。
- Shader bug 常以 2×2 像素块的形式出现，因为 quad 是硬件派发单位。
- 隐式导数在 non-uniform control flow 与 vertex shader 中 undefined。

## 链接到的概念

- [[texture2dgrad-explicit-derivatives]]
- [[fwidth-derivative-antialiasing]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/02/how-to-change-your-uv-map-on-fly.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-10_how-to-change-your-uv-map-on-the-fly.md`
