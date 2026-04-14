---
tags: [渲染, ssr, reflection, post-process]
date: 2026-04-14
sources: 1
---

# Screenspace Reflections（SSR）

**屏幕空间反射**是 2013—2014 年间随 Crysis 2 DX11 更新、Killzone: Shadow Fall、Assassin's Creed 4 这一批次世代作品普及起来的间接镜面解法。核心思路是沿反射向量在 **已经渲染出来的屏幕空间深度缓冲** 里做 raymarching，命中时直接拿主场景 color buffer 里该位置已经着色好的像素作为反射颜色。因为主 pass 已经评估了光照，SSR 的额外成本只有一段 post-effect 式的 ray marching + 若干滤波，却能覆盖曲面、水波、normal map、动画材质、emissive、粒子等一切 cubemap 烘不到的东西。

## 为什么是 post-effect

[[deferred-rendering|延迟管线]] 下，cubemap 或 planar reflection 要做「几何重渲染」的代价越来越难接受——CPU 的额外 culling、GPU 的额外几何处理都是实打实的。SSR 不需要任何 CPU 侧准备，和 [[tiled-light-prepass|光照 pass]]、[[chromatic-aberration-post|色差]] 一样可以整段开关和缩放分辨率，是典型的 post-effect 思维。更重要的是 Fresnel 项天然偏向掠射方向，而掠射方向的反射向量大概率打在屏幕内，SSR 的命中率被这条物理规律反过来优待。

## 三类先天缺陷

Wronski 明确把 SSR 的根本问题拆成三类，这个分类在后续 SSR 讨论里被反复引用：

1. **离屏信息缺失**：反射向量出屏，尤其是接近屏幕边缘的像素会大量丢失。
2. **背面信息缺失**：主角在镜面里的第三人称反射——他正脸对着相机、背面对着反射面，背面从不被光栅化过，SSR 永远看不到。
3. **厚度假设失效**：depth buffer 只是一张高度场，必须对每个像素假设一个「厚度」用于 ray 测试。假设太薄，层叠物下会漏光「shadow」；假设太厚，明显的反射面会被误判错过。

这三类缺陷共同作用下，静态截图可以很漂亮，但相机或物体一动就暴露无遗——于是出现 flicker、blinking holes、character ghosting。

## 稳定化技术栈

任何能落地的 SSR 实际上是一整套滤波链：

- **半分辨率或更低的 ray pass**（带宽所迫），配合 [[depth-aware-upsampling]]。
- **[[temporal-supersampling]] / 时域累积**——这一条几乎是必须的，它把空间噪声换成时间迟滞。
- **conservative test + pre-blur source image**：降低亚像素 aliasing 引入的 noise。
- **按 gloss 分别做分离模糊**：粗糙面用大半径，镜面用小半径，样本 confidence 加权。
- **flood-fill 填洞**：对 raymarch miss 的区域做邻域扩散。
- **始终与 [[parallax-corrected-cubemap|localized cubemap]] 叠加**：这是 Wronski 反复强调的硬约束——SSR 只能做「加料」，不能做反射的唯一来源。

## Fresnel 与遮蔽

SSR 的一个副作用很受欢迎：它天然给 cubemap 提供了 SSAO 式的遮蔽。没有 SSR 时阴暗墙角里「闪闪发光」的 shiny 物体是 cubemap 泄漏的经典问题，SSR 命中的区域 confidence 高、miss 的区域自然退回 cubemap，边缘也就自动收住。

## 未来方向

Wronski 在 2014 年就预见到 SSR 的演进必然走向「屏幕空间之外」：多帧累积 radiance / geometry 缓存、第二层深度缓冲（depth peeling）解决厚度假设、低分辨率体素 / SDF / 粗 BVH 引导光线——这些后来都变成现实（voxel cone tracing、signed-distance field tracing、[[hybrid-raytracing-pipeline|混合硬件 RT + 屏幕空间精算]]）。

## 相关

- [[temporal-supersampling]]
- [[temporal-antialiasing]]
- [[motion-vectors]]
- [[deferred-rendering]]
- [[parallax-corrected-cubemap]]
- [[hybrid-raytracing-pipeline]]
- [[depth-aware-upsampling]]
- [[hbao-interleaved-sampling]]
- [[bartosz-wronski]]

## Sources

- [[sources/bartwronski-future-of-ssr]]
