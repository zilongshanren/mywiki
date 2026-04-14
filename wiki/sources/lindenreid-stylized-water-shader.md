---
tags: [source, shader, water, depth, unity]
date: 2026-04-14
sources: 1
---

# Simple Water Shader in Unity（Linden Reid）

[[linden-reid]] 2017 年 12 月的 Unity shader 教程，教初学者用 camera depth texture 和顶点噪声做一张「卡通风水面」。她在文首写明这其实是披着 Unity 外衣的通用图形教程——关键在算法，不在 API。

## 摘要

教程分成两个独立部件。**Foam line** 靠 camera depth texture：先在相机上加一个 `ExecuteInEditMode` 脚本把 `depthTextureMode` 置为 `Depth`，然后 shader 里 `SAMPLE_DEPTH_TEXTURE_PROJ` + `LinearEyeDepth` 得到水下物体到相机的距离 `depth`；再用 `foamLine = 1 - saturate(_DepthFactor * (depth - input.screenPos.w))`——其中 `screenPos.w` 就是水面当前像素到相机的 view-space z，两者相减即水下物体到水面的距离。这个值可以直接当 `_EdgeColor` 的混合权重，也可以当 ramp 纹理的 u 坐标得到 cel 风硬边。**Wave animation** 是顶点 shader 里 `sin(_Time * _WaveSpeed * tex2Dlod(_NoiseTex, uv)) * _WaveAmp` 加到 `pos.y/x` 上——噪声让每个顶点相位错开，`sin` 提供周期。作者强调需要 `tex2Dlod` 因为 vertex stage 没有隐式 LOD。最后还给了一个 `_ExtraHeight` 的 fudge 避免水面最低点穿过水下物体。评论里大量读者问题集中在相机尺度和 `LinearEyeDepth` vs `Linear01Depth` 的坑，以及相交物体必须投阴影才能进 depth texture 这个 Unity legacy 细节。

## 关键要点

- Depth texture 的一个有用读法：`depth - screenPos.w` 等于水下物体到水面的距离
- `_CameraDepthTexture` 由 shadow caster pass 顺带生成——物体必须能投影
- Ramp 贴图采样可把 foam 线变成硬边 cel 风
- 顶点动画 `sin(time * noise)` 是最便宜的波动合成，需要 `tex2Dlod`
- 正交相机不适用；`LinearEyeDepth` 随相机尺度而失效

## 链接到的概念

- [[stylized-water-shader]]
- [[depth-texture-silhouette]]
- [[cel-shader-outline]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/12/15/simple-water-shader-in-unity/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-12-15_simple-water-shader-in-unity.md`
