---
tags: [source, 渲染, 后处理, 景深, bokeh]
date: 2026-04-14
sources: 1
---

# Bokeh depth of field – going insane! part 1（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 4 月发表的文章，是他在 2011 年 _The Witcher 2_ 上实现的**散射式 bokeh 景深效果**的回顾 + 2014 年在自家 C# 框架里的重实现，也是一个承诺会有续集的系列开篇（后续会讲 tile-based / compute / software rasterizer 版）。

## 摘要

文章有两层。第一层是**摄影美学**：Wronski 是胶片摄影爱好者，厌恶游戏里的六边形 bokeh——现代所有高端镜头都用多叶片或圆形光圈就是为了消灭这个人工痕迹，游戏里却经常看到不明就里的六边形光斑。他把"好 bokeh"分成两类——**creamy bokeh**（人像向，gaussian blur 就能做）和 **busy bokeh**（Leica/Zeiss 老镜头味，有个性有质感），后者需要任意形状的 bokeh sprite，gather 路线做不出来。第二层是**工程**：_The Witcher 2_ 的实现是「**对半分辨率每个像素生成一个 quad，在 vertex shader 里按 CoC 放大成 bokeh sprite，pixel shader 乘 bokeh 贴图，alpha blend 累加**」的硬核 scatter 方案。没有 DX10+、没有 geometry shader，完全用 vertex/pixel shader 搞定，但代价是 overdraw 爆炸——在 GTX Titan 上都能撞到 10-11 ms。它之所以能发货，是因为只在 Ultra 档 + 过场 / 对话里启用，美术非常克制地用物理正确的长焦大光圈配置把 CoC 控制在艺术上合理的范围里。2014 年的重实现加了 indexed draw、procedural vertex from vertex ID、double-width atlas 代替 MRT / GS 等优化，并顺手演示了「对的」物理色差——把 RGB 通道做成不同大小而非位移的 bokeh 光斑——配套代码开源（SlimDX / Sponza 场景）。

## 关键要点

- **scatter > gather** 的前提是需要任意 bokeh 形状 + 干净的 near-plane bleeding + 物理正确的色差。代价是 overdraw 爆炸。
- **工程流水线**：half-res color + CoC → quad grid → vertex shader 按 CoC 放大 → 非目标层 quad 移出视口 → pixel shader 乘 bokeh 贴图 → premultiplied additive blend。
- **atlasing 技巧**：near 和 far 层共享一张双倍宽的纹理，避免 MRT / GS / 二次 vertex pass。接缝处有少量漏出，靠 shader mask 消掉。
- **alpha 合成不是严格 ordered**：加法预乘 + 除法归一的近似，对绝大部分场景肉眼不可见。真要 ordered 可以做 OIT，但不值得。
- **procedural vertex from vertex ID**：不用 VB 存位置，用 SV_VertexID 现算——对 bandwidth-bound 的效果是一大收益。
- **历史第一**：Wronski 原以为 _The Witcher 2_ 是第一个发货 scatter bokeh 的游戏，Stephen Hill 指出 Lost Planet 2007 年就做了。
- **作者诚实列坑**：原版代码里 CoC 计算和合成阶段是被 hack 过的；没用 indexed draw；两次 vertex texture fetch 是浪费。
- **配开源代码**：C# + SlimDX 的自制图形框架，bokeh DoF 是其中的 demo scene，Dropbox 链接（后来修好了）。

## 链接到的概念

- [[scatter-bokeh-dof]]
- [[thin-lens-model]]
- [[chromatic-aberration-post]]
- [[alpha-blending]]
- [[draw-procedural-gpu]]
- [[separable-gaussian-blur]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/04/07/bokeh-depth-of-field-going-insane-part-1/
- 本地：`raw/articles/bartwronski.com/2014-04-07_bokeh-depth-of-field-going-insane-part-1.md`
