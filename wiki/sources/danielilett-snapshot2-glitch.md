---
tags: [source, unity, urp, post-processing, glitch, volume]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders 2 - Glitch（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Snapshot Shaders 2* 撰写的 **Glitch** 后处理参数手册——URP [[urp-volume-post-processing|Volume override]] 形态的故障特效，把三类独立失真合成一套可调效果。

## 摘要

与 [[glitch-image-effect|Alisavakis 的三件套 Glitch 后处理]]（条纹 + 波浪 UV + 色差）相比，Ilett 的 Snapshot 2 Glitch 走的是**纹理驱动 + 参数化随机性**的产品化路线，把三种可叠加的失真分离为独立子效果——每个都有 On/Off 开关：

1. **Offset Glitches**：由一张**垂直条纹 offset 贴图**驱动——每行像素的亮度决定那一行的水平偏移量（黑=全左、白=全右、灰=不动）。*Offset Texture* 控制撕裂图案本身，*Offset Speed* 是贴图在 Y 方向的滚动速度，*Offset Tiling* 决定垂直平铺次数，*Use Point Filter* 在点采样和双线性之间切换（决定撕裂是"台阶"还是"渐变"）。
2. **Slice Band Glitches**：一条周期性出现的**水平宽带**覆盖时整带像素横移，随机开关。有 Strength（偏移量）、Speed（滑动速度）、Jitter（抖动）、Width（带宽）、Min/Max Duration（每次可见时长范围）、Frequency（每秒触发次数）。这是纯程序化的，不依赖贴图。
3. **Block Artifact Glitches**：屏幕按 UV 分块，**随机选一部分块从错误位置采样**。Tiling 决定块数，Chance 决定占比，Strength Min/Max 决定偏移范围，Speed 决定块的刷新频率。

## 关键要点

- 与 Alisavakis 的单一 `_GlitchEffect` 标量分档不同，这里**三个子效果完全独立**——更工业化，美术可以只开"色差 + 撕裂"而不开"块伪影"
- **Offset Texture 是自定义失真的入口**——美术可以画一张专属的"波形"贴图决定撕裂节奏，这是硬编码 `sin(uv.y*f)` 所做不到的
- Slice Band 的 Min/Max Duration + Frequency 是用来模拟"信号偶发中断"的时间控制——偶尔才出现的那一下才像"信号出问题"
- Block Artifact 的 Strength 方向反直觉：<1 右移、>1 左移——Ilett 在参数说明里特别标注了这一点
- 模块分离的代价：一次 Glitch pass 需要 3 套 if/分支或 3 次采样，比 Alisavakis 合并成一个 fragment 的路径更贵；换来的是 tweak 时的独立性
- 本效果受 [[volume-mask-layers|Masking Layers]] 系统约束——可以局部地只 glitch 特定 layer 的对象

## 链接到的概念

- [[glitch-image-effect]]
- [[urp-volume-post-processing]]
- [[chromatic-aberration-post]]
- [[crt-shader-effects]]

## 原文

- 链接：https://danielilett.com/snapshot-shaders-2/glitch/
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-2-glitch.md`
