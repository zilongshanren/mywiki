---
tags: [source, unity, shader, 光照, cel-shading, stencil, ramp-texture]
date: 2026-04-14
sources: 1
---

# Cel Shading Part 5 - Finishing Touches（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 卡通渲染系列的收尾篇。它不是简单的总结，而是**修两个前面埋的坑**：Part 4 的描边 stencil ref 写死在 `1`，两个物体叠在一起时描边会断；Part 2 的 `fwidth + smoothstep` 光照量化只能做两段阶梯，美术想要三段、五段就得重写 shader。两个问题对应两个具体补丁。

## 摘要

**Stencil ID 化**：把 `Ref 1` 硬编码改成一个 Integer Property `_ID`，在 `Stencil { Ref[_ID] ... }` 里引用。这样每个材质可以设不同的 ID，互不干扰；反过来，把几个 mesh 都设成同一个 ID 就能让它们被当成一个整体描边——Ilett 用这个技巧让 Ethan 的身体和眼镜共享一条外轮廓，指出这是 Borderlands 风格"整体粗描边 + 贴图里烘焙细节"的做法。**Lighting Ramp 纹理**：替换掉原来的 `fwidth + smoothstep` 两步量化，改成一次纹理采样 `tex2D(_LightingRamp, float2(diffuse * 0.5 + 0.5, 0.5))`。纹理横向从左到右对应最暗到最亮，美术画几段硬色阶就得到几段光照阶梯，甚至可以带颜色做暖色阴影。Wrap Mode 必须设 Clamp，否则 `diffuse = ±1` 会采到另一端产生伪影。文章以系列总结结尾，预告下一个大系列是 Portals。

## 关键要点

- **`Ref[_ID]` 的方括号语法**是 ShaderLab 里从 Properties 读值的通用写法——因为 `_ID` 不在 `CGPROGRAM` 块里使用，所以**不需要在代码部分再声明一遍**，只在 Properties 里声明即可。
- 两个不同材质即使用同一个 shader，只要 `_ID` 不同，stencil 就独立——**stencil 是逐像素的共享状态，但 ref 值是逐 draw call 传入的**，所以 shader 代码不变也能支持多 ID。
- `diffuse * 0.5 + 0.5` 把点乘结果 `[-1, 1]` 线性重映射到 `[0, 1]`——这里**保留了背面**（`L·N < 0`）信息，背面对应 ramp 纹理最左端；普通 Lambert 会 `max(0, diffuse)` 截断掉背面，ramp 方案则给了美术"画一个渐暗的背面色"的自由。
- Ramp 纹理方案的代价是**一次 texture fetch**——在移动端大批量渲染时要权衡带宽和灵活度。
- 这套补丁把前面所有部分（diffuse 量化、specular、bump、fresnel、outline、stencil ID）粘合成最终的 `FinalCelShaded.shader`，但光照方程的结构没有变——只是把量化器从 `smoothstep` 换成了纹理查表。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[cel-shader-outline]]
- [[stencil-buffer]]

## 原文

- 链接：https://danielilett.com/2019-06-23-tut2-5-cel-shading-end/
- 本地：`raw/articles/danielilett.com/2019-06-23_cel-shading-part-5-finishing-touches.md`
