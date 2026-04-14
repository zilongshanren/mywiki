---
tags: [source, shader, vertex-animation, 植被, unity]
date: 2026-04-14
sources: 1
---

# Waving Grass Shader in Unity（Linden Reid）

[[linden-reid]] 2018 年 1 月 7 日的 Unity shader 教程，灵感来自《塞尔达：旷野之息》的风吹草原。整篇聚焦顶点动画——她此前写过 cel shading，所以光照只扫一行过。

## 摘要

核心问题是让独立 mesh 的多株草共享同一阵风。解法分 5 步：(1) `worldPos = mul(input.vertex, unity_ObjectToWorld)` 转世界空间，`samplePos = worldPos.xz / _WorldSize.xz` 归一化到 `[0,1]` 作为风场纹理 UV——因为所有草共用材质，这张图自然变成全局风场。(2) `samplePos += _Time.x * _WindSpeed.xz` 让采样位置随时间沿风向平移（fragment 测试时用 `frac` 把值拉回 0-1）。(3) `windSample = tex2Dlod(_WindTex, ...)` 采样梯度纹理，然后 `output.pos.z += sin(_WaveSpeed * windSample) * _WaveAmp`、`output.pos.x += cos(...)` 做顶点 offset。(4) 用 `heightFactor = (input.vertex.y > _HeightCutoff) * pow(input.vertex.y, _HeightFactor)` 乘到幅度上——低于阈值的草根为 0，高处指数放大。(5) fragment shader 走 `dot(N, L)` 采样 ramp 纹理做 cel 光照。作者强调风场纹理必须左右无缝否则会产生接缝。评论区提到用 UV.U 代替 vertex.y 才能支持 GPU instancing 合批——后续 GPU 草叶绘制必然要这样做。

## 关键要点

- **世界空间采样** 让独立 mesh 共享全局风场——这是整篇的核心思想
- `frac()` 把 `_Time` 累加后的采样坐标拉回 `[0,1]`
- `sin/cos(windSample)` 驱动 xz 顶点偏移，相位由空间位置决定
- `heightFactor` 分两级：布尔阈值（草根不动）+ `pow(y)`（越高越柔）
- 风场梯度纹理必须左右边缘无缝
- 不重算法线——薄片草叶视觉可接受
- 评论区补充：用 UV.U 替代 vertex.y 支持 GPU instancing

## 链接到的概念

- [[waving-grass-shader-vertex-offset]]
- [[texture-encoded-state]]
- [[cel-shader-outline]]
- [[shaping-functions]]
- [[gpu-driven-grass-tiles]]
- [[deferred-grass-shader]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2018/01/07/waving-grass-shader-in-unity/
- 本地：`raw/articles/lindenreid.wordpress.com/2018-01-07_waving-grass-shader-in-unity.md`
