---
tags: [渲染, shader, water, depth, vfx, unity]
date: 2026-04-14
sources: 1
---

# 风格化水面 Shader（Stylized Water Shader）

一张透明平面 + 一点顶点噪声 + 一次深度纹理采样，就是 indie/卡通游戏里最常见的「风格化水面」。它不追求 PBR 水体，而是用两种手段做出辨识度：**相交处的泡沫线**（foam line）和**随时间摇摆的顶点动画**。两个部件独立，可以随意组合到任意光照模型上。Linden 的教程以 Unity 为载体，但算法本身与 API 无关——任何能读 camera depth texture、能在 vertex shader 里采样噪声的管线都能复刻。

## Foam line：用 depth 差换出水线

核心观察是：水面是一张半透明平面，玩家只在「另一个物体穿过水面」的地方希望看到高光。如何在 fragment 里知道「这个像素背后有东西离得很近」？答案是 [[depth-texture-silhouette|camera depth texture]]——Unity 里通过在相机上把 `depthTextureMode = Depth` 开启（inspector 里没这个开关，得写一个脚本 `ExecuteInEditMode`），然后在 shader 里读 `_CameraDepthTexture`。

关键三行：

```hlsl
float4 depthSample = SAMPLE_DEPTH_TEXTURE_PROJ(_CameraDepthTexture, input.screenPos);
float depth = LinearEyeDepth(depthSample);
float foamLine = 1 - saturate(_DepthFactor * (depth - input.screenPos.w));
```

第一行采样屏幕空间深度；`LinearEyeDepth` 把非线性的深度纹理值还原成 view space 深度（米）。第三行的「魔法」在于 `input.screenPos.w`——clip space 变换后 `w` 实际存着顶点在 view space 下的 z，也就是**水面当前像素**到相机的距离。`depth - screenPos.w` 则是**水下物体到水面的距离**。`_DepthFactor` 调节灵敏度，`saturate` 夹到 `[0, 1]`，`1 -` 翻转让浅水处为高值——foam 线越亮。这个技巧的精髓是：shader 只需要**两张深度之差**，整个水面本身还是同一张平面 mesh，完全不需要知道水下是什么。

有了 `foamLine` 以后，可以把它当作：

- **梯度混色**：`col = _Color + foamLine * _EdgeColor`——得到从水色平滑过渡到泡沫白的自然水线。
- **ramp 采样**：`tex2D(_DepthRampTex, float2(foamLine, 0.5))`——借用 [[cel-shader-outline|cel shader]] 的 ramp 贴图思路，让边缘成为带台阶的硬线，得到卡通风水面（Linden 本人觉得更搭她的 cel-shaded 狗模型）。

> **Unity 的坑**：相交物体必须**能投射阴影**——depth texture 实际上是 shadow caster pass 顺便生成的，如果物体材质关闭了阴影或 inspector 里不 cast，它就不进 depth 纹理，foam 线也就画不出。这是 Unity 历史遗留的 legacy 实现细节。

## 顶点波动：`sin(time * noise)`

波动是顶点 shader 的小算术：先用 `tex2Dlod(_NoiseTex, uv)` 采样一张静态噪声纹理（vertex stage 没有隐式 LOD，必须用 `tex2Dlod`），得到每顶点的伪随机相位，再用 `sin(_Time * _WaveSpeed * noise) * _WaveAmp` 得到一个 y 偏移加到顶点位置上。噪声的作用是让每个顶点的震荡相位错开，避免整张平面像刚体一样同步上下；`sin` 保证震荡周期性；两者相乘只是最便宜的「看起来还行」的合成。

教程还多加了 `_ExtraHeight` fudge，用来避免水面的最低点穿过水下物体的上表面——一个典型的「不懂原理但工作良好」的 hack。

## 和其他风格化效果的组合

水面的 foam 线和顶点动画是正交的：foam 只改颜色，顶点动画只改位置。它可以接任何光照模型——把 [[cel-shader-outline|cel shader]] 的 ramp lighting 叠到水面 `_Color` 上即可同时有硬阴影和硬泡沫；也可以串 [[texture-dissolve|dissolve]] 做「水蒸发」演出。作者后续的 ice shader 教程就是在此基础上加一个 grab pass 折射，对水面做再调制。这类 shader 的组合性来自它们共同的结构：fragment 阶段只写 `color = base + effect1 + effect2`，各 effect 彼此不看。

## 常见坑

- **水面全白**：`LinearEyeDepth` 返回的是米级的线性深度，一旦相机远于 1 米就被 saturate 掉——调小相机 near/far 或换成 `Linear01Depth`。评论区里许多人就是靠换函数「修好」的。
- **正交相机不适用**：`screenPos.w` 在正交投影下不是 view-space z，foam 公式会退化。
- **低多边形时漏波**：顶点动画的频率上限由顶点密度决定，水面 mesh 需要按预期波长切细。
- **穿模**：顶点位移后要同步补偿 shadow caster pass，否则自阴影会在原位。

## 相关

- [[depth-texture-silhouette]] —— 深度纹理采样的通用原理
- [[cel-shader-outline]] —— 同作者的 ramp lighting + outline 教程，此处复用 ramp 思路
- [[texture-dissolve]] —— 同样的「噪声 + 阈值」范式
- [[fragment-shader]]
- [[watercolour-shader-experiments]]

## Sources

- [[sources/lindenreid-stylized-water-shader]]
