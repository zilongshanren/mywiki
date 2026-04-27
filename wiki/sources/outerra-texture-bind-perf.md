---
tags: [source, rendering, opengl, performance, texture]
date: 2026-04-27
sources: 1
---

# OpenGL Notes #2: Texture Bind Performance（Outerra / Laco Hrabcak）

[[people/outerra-team]] 的 Laco Hrabcak 发表于 2012 年 11 月，记录在 NVIDIA 硬件上 `glBindMultiTextureEXT` 导致的异常性能下降及解决方案。

## 摘要

Outerra 对象渲染器在 NVIDIA GTX 460 上，逐 mesh 绑定纹理时对象 pass 耗时从预期的 ~5 ms 飙升至 15 ms；AMD 6850 无此问题（~5 ms）。通过 Nsight 定位，延迟集中在纹理绑定后的 draw call，而非绑定调用本身。分析发现 NVIDIA SM4 硬件暴露 96–192 个 `MAX_COMBINED_TEXTURE_IMAGE_UNITS`，频繁更改绑定会触发驱动内部某种状态同步。解决方案"Texture Bind Groups"：帧初一次性把所有纹理绑定到连续 unit，逐 mesh 只发送一个 `glUniform1iv` 传递 unit 索引，整帧无额外绑定。NVIDIA 性能恢复到 3.36 ms（接近单纹理基线 3.3 ms），AMD 同样持平或更好。该方案对超出 unit 数量的场景，按 unit 上限分组处理。

## 关键要点

- NVIDIA 独有的纹理绑定延迟问题（AMD 不受影响）。
- `MAX_COMBINED_TEXTURE_IMAGE_UNITS`（NVIDIA 96–192）是可利用的超额资源。
- 把"逐 drawcall 绑定"变为"帧初一次绑定 + 索引"，消除绑定频繁切换的驱动同步。
- `glUniform1iv` 的开销可忽略不计。
- 该方案是 bindless rendering 出现前的工程近似。

## 链接到的概念

- [[opengl-texture-bind-batching]]
- [[bindless-rendering]]
- [[draw-call]]
- [[batching]]

## 原文

- 链接：https://outerra.blogspot.com/2012/11/opengl-notes-2-texture-bind-performance.html
- 本地：`raw/articles/outerra.blogspot.com/2012-11-15_opengl-notes-2-texture-bind-performance.md`
