---
tags: [渲染, 性能优化, 移动端, 后处理]
date: 2026-04-14
sources: 1
---

# 变分辨率渲染（Dynamic / Scaled Resolution Rendering）

**在保持 backbuffer 尺寸不变的前提下，让所有内部渲染目标按一个统一缩放系数降采样，最后再 stretch blit 回全尺寸。** 这是一种针对像素密集型负载的"终极"优化手段：画面整体像素计算量按缩放系数的平方下降，而画质损失通常小于同等幅度的显式特性关闭。

[[people/gameknife|gameknife]] 在 2013 年为 [[gkengine]] 做渲染优化时，把这套思路总结为三个层次：

1. **单特性降采样**：对最昂贵的屏幕空间 pass 单独降采样。典型目标是 SSAO、shadow mask、[[bloom-threshold-blur-composite|bloom]] 等后处理步骤——这些 pass 本身是低频信号，砍一半分辨率几乎看不出来。
2. **全局分辨率缩放**：在 texture manager 里挂一个全局 scale 属性，backbuffer 之外的所有 RT 统一按比例分配。gameknife 实测 **0.75× 渲染尺寸 + stretch 到 1.0× backbuffer**，像素计算量降到接近 1/2，DEMO 场景的帧率直接从 104 FPS 提升到 240 FPS。
3. **锐化补偿**：缩放下的画面会出现"图像压缩感"的模糊。补偿手段是一个轻量的 unsharp mask pass ——先做一次微弱高斯模糊，再把原图与模糊结果做线性**外插**（`lerp(blur, curr, k)`，k > 1），放大高频反差。这个手法早于 AMD FidelityFX CAS / NIS 等公开方案数年。

## 半分辨率 pass 的边界伪影

shadow mask 是最容易被独立降采样的 pass——它本质上是一张屏幕空间遮蔽贴图。但直接半分辨率渲染再到着色阶段做线性采样会在阴影与受光的边界上**采到非阴影值**，表现为树干、屋檐等物体阴影边缘的"白边"。

gameknife 给出的修法是：**在着色时对右下方像素额外采一次阴影值，两次取 min**。这相当于把所有边界像素偏向阴影一侧。副作用是本该全亮的区域偶尔会出现"黑边"，但视觉上黑边的观感远比白边温和，属于可接受权衡。

同类思路广泛存在于半分辨率 SSAO、半分辨率透明、半分辨率粒子等场合——全分辨率 depth + bilateral upsample 是另一条更昂贵的替代路线。

## 与地形 shader 采样的相互作用

变分辨率本身不会破坏纹理采样，但它和一些"省事"的 shader 写法相互放大了问题。gkEngine 原本因为地形的多层混合在 shader 内部用 `frac` 生成 texcoord，自动 mip 会在 block 边界发生采样错误，干脆**关了 mipmap**——这在全分辨率下就已经颗粒感偏重，低分辨率渲染加锐化后更明显。

修法是放弃 `ddx` 自动 LOD，改为**用像素线性深度手动计算 mip level**，再走 `tex2Dlod` 显式指定层次。一个意外发现是：`tex2Dlod` 在 DX9 世代实际展开成两条采样指令（GPA 里会显示两次 tex_ld），比 `tex2Dgrad` 反而更贵；把手动 LOD 从 `tex2Dlod` 改成 `tex2Dgrad` 送入计算好的 ddx/ddy，地形 block 的采样次数直接从 26 次砍半到 9 次。

## 相关

- [[bottleneck-analysis]] —— "先测瓶颈再优化"是变分辨率之所以成立的前提：Pixel-bound 才值得降采样
- [[deferred-rendering]] —— gkEngine 的变分辨率管线最终配合 deferred shading 切换使用
- [[sampler-filter-wrap-modes]] —— stretch blit 本质是一次双线性上采样
- [[mipmap-moire-scanline]] —— mipmap 选择错误会和低分辨率渲染叠加放大失真
- [[bloom-threshold-blur-composite]] —— bloom 是另一个典型的低频、可降采样的后处理 pass
- [[gkengine]]

## Sources

- [[sources/gameknife-gkengine-rendering-optimization]]
