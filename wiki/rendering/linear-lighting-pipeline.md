---
tags: [渲染, 光照, gamma, srgb, framebuffer]
date: 2026-04-19
sources: 1
---

# 线性光照管线：三种累积模式

[[ben-supnik]] 的 *Gamma and Lighting* 三部曲提出一个朴素但易被忽略的观点：**光是加性的**——把光子数相加得到更多光，这是图形管线里光照累积的物理基础。但 [[color-space|sRGB]] 不是线性的，把 sRGB RGB 值直接相加 ≠ 相加亮度。真正要做 gamma-correct lighting，就要把「在 linear 空间做光照累积」这一约束贯穿到 framebuffer 格式与 blend 阶段。工程上有三条路径，各有代价。

## 路径一：单 pass forward，shader 内累积

传统 forward renderer：所有光源在一次 fragment shader 调用里算完，结果直接相加。整个累加过程发生在 shader 的 float 域，天然线性——shader 最后再把 linear 值 encode 成 sRGB 写进 8-bit framebuffer 即可。曝光控制和 clamp 也在 shader 的浮点阶段完成。**最简单，因为 blend 阶段根本不参与累加**。

## 路径二：多 pass + `GL_ARB_framebuffer_sRGB`

想用 additive blending（每盏灯一次 draw、硬件 blend 做加法）累积到 8-bit RGB framebuffer，就必须开 [`GL_ARB_framebuffer_sRGB`](https://www.opengl.org/registry/specs/ARB/framebuffer_sRGB.txt)。开启后，GPU 在 blend 前把 dest 从 sRGB decode 到 linear、blend 完再 encode 回 sRGB 存储——blend 阶段变成 gamma-correct。同理 [`GL_EXT_texture_sRGB`](http://www.opengl.org/registry/specs/EXT/texture_sRGB.txt) 让 texture fetch 在过滤**之前**解码，texture filtering 和 framebuffer blending 这两个你在 shader 里无法干预的硬件阶段都能被修正。

**代价**：单 pass 不知道总曝光。累积到一半可能已经 saturate 了 8-bit 目标，导致 sRGB encode 时 clip。你得把整体曝光预设压得够低才不爆掉，这在动态光数量未知时是脆弱约束——经常用在 deferred 或 stencil shadow volume 方案里。

## 路径三：HDR 浮点 framebuffer

用 RGBA16F / R11G11B10F 等浮点 RT，blend 直接在 linear 浮点域累积——**无 clip 问题**、无 encode/decode 往返。缺点是带宽和 ROP 吞吐成本。事后单独做 tonemap pass 把 HDR linear → LDR sRGB，写进 swap chain。这是现代 deferred / clustered 管线的标配。

## 纹理端别忘了

三条路径都要求**输入端**也 gamma-correct：albedo / UI / diffuse texture 打 sRGB flag 让硬件 decode；normal / roughness / mask 保持 linear format——这个约定和 [[gamma-correction-srgb|shader 级编解码]] 是一回事，只是把责任挪到硬件 sampler。

## 关于「framebuffer 是什么颜色空间」

Supnik 的观察值得记：**framebuffer 的「颜色空间」很大程度是命名约定**。十年前的 OpenGL pipeline 里，你往 framebuffer 写的 RGB 在 CRT 上看起来像 sRGB，但 GL 的光照数学是 linear——等于在把 sRGB 数据塞进 linear 管线里，所有光照混合 artifact 的根源就在这儿。`framebuffer_sRGB` 扩展的意义不在于「换了颜色空间」，而是**让 blend 阶段的数学和存储格式的语义对齐**。

## 相关
- [[gamma-correction-srgb]] — shader 里 sRGB 编解码的最小实现
- [[color-space]] — TRC / primaries / white point 三要素
- [[alpha-blending]] — blend 同样必须在 linear 域
- [[deferred-rendering]] — 天然用路径三的 HDR RT
- [[color-banding]] — 8-bit 目标下 encode 顺序影响暗部台阶
- [[ben-supnik]]
- [[xplane-deferred-pipeline-hacks]] —— X-Plane 10.10 让 linear 光累加与 sRGB 几何 blend 在同一帧不同 RT 上共存的实例

## Sources

- [[sources/supnik-gamma-lighting-trilogy]]
