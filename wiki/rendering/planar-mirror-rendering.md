---
tags: [mirror, reflection, stencil, rendering]
date: 2026-04-19
sources: 1
---

# 平面镜渲染

平面镜（wall mirror, still water）和球面反射的区别是它只反射**一个特定平面两侧**的场景。最诚实的实现是「重新渲染一次场景，相机镜像到平面另一侧」——但性能压力随镜子数量乘倍增加。[[simon-trumpler]] 在 *Sims 4 Mirrors* 里把这个工艺的每一层（LOD fallback、oblique projection、stencil mask、独立 culling）都抓了出来。

## 核心工艺

对每面镜子：

1. **镜像相机**——把主相机沿镜面做反射变换得到「虚拟相机」，它看到的是镜后世界；
2. **Oblique 投影矩阵**——修改投影矩阵使镜面平面成为 near plane，避免穿模到镜子前方；
3. **写 stencil mask**——把镜子表面用特殊 stencil ID（2、3、4…）写入 stencil buffer；
4. **独立 culling**——对镜像相机做 frustum + occlusion culling，不复用主相机结果；
5. **在 stencil 限制下渲染**——只在对应 stencil ID 的像素上渲染，避免跨镜子漏光；
6. **合成回主画面**——镜像渲染结果直接出现在 color buffer 的对应位置（不用额外 RT）。

*Sims 4* 的特殊巧思是：**pixelation / 粒子等后处理也按 stencil 剪裁**，保证镜像世界里的淋浴像素块只出现在镜内不泄漏到镜外。

## 性能与 LOD

镜子多到 10+ 面时一帧要画 11 次场景（主+10 个镜像），即便 culling 干净也难顶。常见优化：

- **距离 fallback**——远处镜子切到预渲染贴图或完全黑掉；*Sims 4* 用的是静态贴图 + 距离淡入；
- **简化几何**——镜像 pass 用 LOD 高一级的 mesh；
- **低分辨率 RT**——镜面模糊本来就要 blur，低分辨率 RT 再 bilinear 放大不丢质感；
- **屏幕空间反射 (SSR)** 替代——只对能在屏幕内找到对应像素的平面有效，斜视角失败；
- **Planar reflection capture**（UE 的叫法）——烘焙，静态场景用；
- **Cubemap 近似**——非平面但够近似，适合静止水面等。

## 与 stencil portal 的同源性

*Sims 4* 的 stencil-mask 派发与 [[stencil-portal-shader-antichamber]] 的 Antichamber 门户同出一辙——把 stencil 当「只渲染我管辖区域」的 per-object mask。两者本质都是**空间分区 + per-region 渲染**，区别只是 portal 跨几何空间，mirror 跨反射空间。

## 与其他反射技术的分工

| 技术 | 平面镜 | 球面曲面 | 遮挡反射 | 实时性 |
|---|---|---|---|---|
| Planar mirror（本页） | ✔ 真实 | ✘ | ✔ 完整 | 每帧重画 |
| [[screenspace-reflections]] | ✔ 但斜视角失败 | ~ | ✘ | 一帧 cheap |
| [[parallax-corrected-cubemap]] | ~ | ✔ | ✘ | 预烘焙 |
| Ray tracing | ✔ | ✔ | ✔ | 需要 RT 硬件 |

## 相关

- [[stencil-buffer]]
- [[stencil-portal-shader-antichamber]]
- [[screenspace-reflections]]
- [[parallax-corrected-cubemap]]

## Sources

- [[sources/simonschreibt-sims-4-mirrors]]
