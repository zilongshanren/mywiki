---
tags: [渲染, shader, 透明, fresnel, normal-map, grabpass, unity]
date: 2026-04-14
sources: 1
---

# 冰晶 Shader（Fresnel + Bump + GrabPass 扭曲）

[[linden-reid]] 2017 年底的这一篇把三个独立可用的风格化效果拼成一个「冰/水晶」材质：**边缘不透明的 Fresnel 半透明**、**加在顶点法线上的 noise 法线扰动**、以及**用 [[unity-grabpass-blur|GrabPass]] 抓背景后再做屏幕空间扭曲**。整篇的价值不是「冰」这个结果，而是这三块技术都能单独搬到其他 shader 里——水面、玻璃、灵魂气场都用得上。

## Fresnel 边缘：`dot(V, N)` + `pow` + ramp

冰要的视觉是**正面看穿透、边缘看不透明**。这个经典效果由 Fresnel 近似给——当视线几乎平行于表面时反射占主导、不透明；垂直于表面时折射/透射占主导、透明。代码上只需要视线方向 `viewDir` 和世界空间法线 `normal`：

```hlsl
float edgeFactor = abs(dot(input.viewDir, input.normal));
float opacity = min(1.0, _Color.a / edgeFactor);
opacity = pow(opacity, _EdgeThickness);
```

当视线平行于表面时 `dot` ≈ 0，`_Color.a / edgeFactor` 变大、被 `min` 钳到 1——完全不透明；正对时 `dot` ≈ 1，得到较低的 `_Color.a` 值——半透明。`_EdgeThickness` 是 `pow` 的指数，越大越陡——控制不透明带收窄的速度。`abs` 是为了 `Cull Off` 场景下背面也走同一公式。

然后她用 `edgeFactor`（或者这个例子里的 `1 - edgeFactor`）去采样一张横向 ramp 纹理决定边缘颜色——这又是 [[cel-shader-outline|cel shader]] 里那套「把光照梯度外化成纹理」的思路，艺术家不改代码就能换色。要求是 `Tags { Queue = Transparent }` + `Blend SrcAlpha OneMinusSrcAlpha` + `Cull Off`，都是 Unity transparent 的标准配置。

## Bump mapping：`normalMapSample + vertexNormal`

这一步 Linden 刻意强调了一个**不写出来就看不出来的坑**：她的 noise 噪声纹理不是通过标准 [[tangent-space-normal-mapping|切线空间法线贴图]] 去和顶点法线合成，而是直接把**纹理的 RGB 当成法线向量加到世界空间顶点法线上**——

```hlsl
float3 bump = tex2D(_BumpTex, input.texCoord.xy).rgb + input.normal.xyz;
```

这在几何上不严谨（没有做切线空间变换、没有归一化），但视觉上恰好给出**既有模型面朝向、又有高频扰动**的"iridescent"效果——物体旋转时高光跟着动（顶点法线贡献），但表面看起来又是油膜状的细碎反射（noise 贡献）。拿这个「扰动过的法线」去和光方向算点积、再去采样 ramp 纹理，就得到一层 cel-shaded 的 bump 光照。她自嘲这张 noise 纹理是「lazy noise texture, lol」——重点是视觉"够像"，不是物理正确。

这是风格化 shader 里的一个常见心态：**PBR 追求精确，stylized 追求可控**。只要艺术家能通过几个 slider 调出想要的效果，公式本身不需要推导正确。

## 屏幕空间扭曲：GrabPass + bump 偏移

最后一块是放在前面的独立 pass，负责让冰背后的东西「歪掉」。核心是 [[unity-grabpass-blur|GrabPass]]——Unity 的一个内置机制，在当前 pass 前把「到目前为止已经画好的帧缓冲」抓成一张纹理 `_BackgroundTexture`，后面的 pass 可以采样它：

```shaderlab
GrabPass { "_BackgroundTexture" }
```

扭曲只需要在 vertex shader 里把 grab 的屏幕坐标偏一下：

```hlsl
output.pos = UnityObjectToClipPos(input.vertex);
output.grabPos = ComputeGrabScreenPos(output.pos);
float3 bump = tex2Dlod(_BumpTex, float4(input.texCoord.xy, 0, 0)).rg;
output.grabPos.xy += bump.xy * _DistortStrength;
```

然后 fragment shader 用偏移后的坐标采样 `_BackgroundTexture`：

```hlsl
return tex2Dproj(_BackgroundTexture, input.grabPos);
```

这和 [[stylized-water-shader|水面]] 的折射扭曲、[[unity-grabpass-blur|雾气窗]] 的模糊玻璃完全同构——GrabPass 是一张「现成的屏幕快照」，任何对屏幕坐标的扰动都会变成一种屏幕空间后效。代价是 GrabPass 非常贵：每遇到一个它就要 flush 一次当前帧缓冲到纹理——所以不能滥用，场景里同时存在多个 GrabPass 材质会直接拖垮移动端。这也是评论区里有人反馈「iOS Unity 2019.3 上这个 shader 不工作」的根因——现代 URP/SRP 的 GrabPass 语义变了（见 [[scene-color-depth-nodes|Scene Color node]]）。

## 三件套的共同心智模型

这三块可以分别归结为三种风格化技术范式：

- **Fresnel 透明度** = 「把视角几何翻译成 alpha」。也出现在霓虹灯辉光、护盾、能量场、[[journey-sand-specular|Journey 沙子高光]]。
- **Noise 作法线** = 「把 2D 噪声当作表面微几何代理」。比 [[tangent-space-normal-mapping|切线空间 normal map]] 糙但够用，广泛出现在水面、油膜、史莱姆。
- **GrabPass 屏幕扭曲** = 「后效在材质里做」。完整的 post 栈会把它放到 [[urp-volume-post-processing|URP 后处理]]，但在 Built-in Pipeline 年代这是唯一的「透明物体背后再采一次」途径。

整体结构是"**先抓背景并扭曲，再画 alpha-blended 的冰本体**"——pass 顺序一颠倒就坏了。

## 相关

- [[unity-grabpass-blur]] —— GrabPass 的另一经典用法（模糊窗）
- [[stylized-water-shader]] —— 同作者的折射水面，共享 GrabPass 扭曲思路
- [[cel-shader-outline]] —— ramp 采样的 cel 光照在这里的复用
- [[texture-encoded-state]] —— 把美术可调项编码进纹理的范式
- [[tangent-space-normal-mapping]] —— 严谨做法 vs 本文的"lazy"做法
- [[alpha-blending]]
- [[scene-color-depth-nodes]] —— URP 时代的 GrabPass 替代
- [[linden-reid]]

## Sources

- [[sources/lindenreid-ice-shader-unity]]
