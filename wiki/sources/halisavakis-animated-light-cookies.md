---
tags: [source, rendering, shader, unity, light-cookie]
date: 2026-04-19
sources: 1
---

# Animated light cookies（Harry Alisavakis / Technically Art）

[[harry-alisavakis]] 发表于 2020 年 6 月的 portfolio 短贴，展示用 Unity 内置管线里的 **Custom Render Texture** 配合自定义着色器，做出动画化的 **light cookie**（投影在灯光上的遮罩贴图，用来塑造光斑形状，例如窗格、树叶、水面 caustics）。

## 摘要

文章正文只有一行字加两张 GIF：作者做了「小实验」，让一张 light cookie 贴图不再是静态图片，而是由一张 Custom Render Texture 实时生成并滚动——这样灯光打到地面上的光斑会随时间变形。思路是把 CRT 当作"带状态的 shader 画布"：每帧运行一个 update material 把上一帧的内容读出来做位移 / 扰动 / 波形叠加，再写回同一张 RT；把这张 RT 绑到 `Light.cookie` 上，就得到会动的光影。

由于原文没有给 breakdown、代码片段或 shader graph 截图，这篇属于纯作品展示，技术细节需要自行脑补。记录下来主要是留作 [[harry-alisavakis]] 作品时间线的节点，以及 "Custom Render Texture 做动画 cookie" 这一思路的早期引用。

## 关键要点

- **Light cookie**：作为聚光灯 / 方向光的遮罩贴图，在 Unity 内置管线下通过 `Light.cookie` 赋值。把它动起来就能得到会动的光斑 / 窗帘阴影 / caustics。
- **Custom Render Texture（CRT）**：Unity 的一种可编程 RT，带 Update Material，能每帧自更新。天然适合做 feedback 循环（读前一帧 → 写回）。
- 两张 GIF 展示的是不同扰动参数下的 cookie：一张像随机软斑块缓慢流动，另一张更接近水面 caustics 风格的条纹。
- 原文未给 shader 代码或参数，只是 portfolio 性质的短贴。

## 链接到的概念

- [[harry-alisavakis]]

## 原文

- 链接：https://halisavakis.com/portfolio/animated-light-cookies/
- 本地：`raw/articles/halisavakis.com/2020-06-20_animated-light-cookies.md`
