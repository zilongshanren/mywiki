---
tags: [source, rendering, shader, pipeline, post-processing]
date: 2026-04-19
sources: 1
---

# Combining Shaders（Xor / GM Shaders Mini）

[[xor-shader-artist|Xor]] 发表于 2025-04-19 的一篇**工程经验帖**：把两个后处理效果合并成单 pass 之前该检查什么，以及具体怎么合并。

## 摘要

作者在前作里写过多趟 shader（典型例子是可分离 Gaussian blur 把 N² 采样降到 2N）。但 multi-pass 需要中间 surface、额外 draw call、更多显存，有时候还不可行。Combining shaders 是另一种选择。Xor 给出一张按重要度排序的 checklist：**Performance**（两个都贵就别合）、**Sample Count**（采样数会相乘，8×32 → 256）、**Coordinates**（不同空间要显式转换）、**Textures**（过滤/边界/blend mode/alpha 必须一致）、**Uniforms**（总量和接口得对齐）。过了 checklist 就按机械套路：把每个 shader 改写成 `vec4 f(vec2 uv)` 函数，嵌套调用，**内层先执行**。示例把 grayscale 嵌进 chromatic aberration 的 for-loop 内：每次 CA 采样前先去色，顺序上 desaturation→CA；反过来如果要 CA→desaturation，会把昂贵 CA 嵌进 desaturation 里，从而只算一次 CA。核心经验：**把采样多的放外层、单采样的放内层**，避免昂贵代码被循环放大。

## 关键要点

- 合并 vs multi-pass 不是风格选择，是**按 5 项 checklist 做决策**。
- 最容易踩的坑：采样数相乘，不是相加。
- 合并的机械流程就是「改成函数 + 嵌套」，uniform/宏不用传。
- 顺序决定嵌套方向，也决定昂贵代码被循环执行的次数。
- 附 Xor 自己的三个 one-pass blur 参考实现：1PassBlur（golden-angle 盘形）、MipBlur（利用 mipmap）、Bokeh（景深）。

## 链接到的概念

- [[shader-combination-strategies]]
- [[ping-pong-surfaces]]
- [[separable-gaussian-blur]]
- [[chromatic-aberration-post]]

## 原文

- 链接：https://mini.gmshaders.com/p/combiningshaders
- 本地：`raw/articles/mini.gmshaders.com/2025-04-19_combining-shaders.md`
