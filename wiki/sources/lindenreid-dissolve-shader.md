---
tags: [source, shader, vfx, dissolve, unity]
date: 2026-04-14
sources: 1
---

# Dissolve Shader in Unity（Linden Reid）

[[linden-reid]] 2017 年 12 月应推特读者请求写的 dissolve 教程——「会渐渐隐形的怪物」。和 [[ronja-texture-dissolve|Ronja 的版本]] 本质相同，但结构更贴近演出用途（多层边缘色 + 全局 alpha fade）。

## 摘要

基础 dissolve 就是经典三步：`tex2Dlod(_NoiseTex, uv)` 取噪声，`threshold = _Time * _DissolveSpeed`，`clip(noiseSample - threshold)`——时间推进时阈值上升，低亮噪声像素先被 discard，网格按噪声形状渐进消失。作者的新点子在**多级边缘色**：在主 clip 之前先算一个「更快」的阈值 `thresh = _Time * _ColorThreshold`，得到 `useDissolve = noiseSample - thresh < 0`（0/1），再用 `color = (1-useDissolve)*color + useDissolve*_DissolveColor` 把基础色和边缘色二选一——避免了在 shader 里写 `if`。可以堆多层，越外层的边缘色配越高的 `_ColorThreshold`，于是形成「已 clip → 正在烧焦 → 将被烧焦 → 原色」的同心梯度。最后可选地加一个 `color.a -= saturate(_Time * _FadeSpeed)` 让整个模型在 dissolve 的同时整体淡出。示例代码嵌在一个 cel 光照 shader 里，作者说明拆出 dissolve 部分即可复用。

## 关键要点

- 算法骨架与 Ronja 一致：`clip(noise - timeScaled)`
- 避免 `if`：用 `useDissolve = (noise - thresh < 0)` 的 0/1 mask 做线性混合
- 多级 `_ColorThreshold` 堆叠出同心色带，每层阈值要递减
- 可选的 `color.a -= saturate(time * fadeSpeed)` 叠一个全模型 alpha fade
- 示例把 dissolve 嵌入到一个 cel 光照 pass，作者提示可拆分

## 链接到的概念

- [[texture-dissolve]]
- [[cel-shader-outline]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/12/16/dissolve-shader-in-unity/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-12-16_dissolve-shader-in-unity.md`
