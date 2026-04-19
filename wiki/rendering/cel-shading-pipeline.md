---
tags: [渲染, shader, toon, cel-shading, 光照, stencil, unity]
date: 2026-04-14
sources: 5
---

# Cel Shading 完整管线

[[daniel-ilett|Daniel Ilett]] 2019 年的 Cel Shading 系列把**卡通渲染**拆成一条完整的流水线：先把传统 [[diffuse-lighting-lambertian|Phong 光照家族]]讲一遍，再在 [[unity-surface-shaders|Unity Surface Shader]] 上把**漫反射量化成硬色阶**、接上高光、加上 bump map 和 Fresnel 边缘光，最后用 [[stencil-buffer]] + 法线外推加一圈描边，并留一个可配置的 **lighting ramp 纹理**给美术自由调色。整条管线是经典内建管线时代 Unity toon shader 的"教科书路径"，也是理解 [[cel-shader-outline|cel+outline 双 pass 结构]]所有改写版本的根。

## 第 0 步：把 Phong 光照拆成四份

Cel shader 的起点不是新算法，而是**把 Lambert 的平滑渐变人为打断**——所以得先把原始 Phong 模型的四个分量摆清楚：

- **环境光（Ambient）**：场景所有物体的"基底亮度"，模拟间接光反弹；Phong 用一个全局常数近似，ray tracer 才能算对。
- **漫反射（Diffuse）**：`L · N`，只看光向和法线夹角。配合逐像素（Phong shading 区别于逐顶点的 Gouraud / 逐面的 flat）能得到光斑从亮到暗的柔和过渡。
- **镜面高光（Specular）**：视线相关的亮斑，用 **half-vector** `normalize(L + V)` 和法线做点乘后取 `pow(·, glossiness)`，`glossiness` 越大高光越集中。
- **Fresnel / Rim**：`1 - V · N`，只看视线和法线——视线掠射时亮度最高，给物体边缘补一条轮廓光。

`L_total = L_ambient + L_diffuse + L_specular + L_fresnel`。这个拆分本身没有卡通味道，真正让它变 toon 的是后面每一步都往信号里塞**硬阈值**。

## 第 2 步：自定义 Lighting 函数把 diffuse 切成阶梯

Unity Surface Shader 默认用 `Standard` PBR 光照；要实现 toon 必须换成**自定义 Lighting 函数**——用 `half4 LightingCel(SurfaceOutput s, half3 lightDir, half3 viewDir, half atten)` 这种命名约定，然后 `#pragma surface surf Cel`。这时需要用旧版 `SurfaceOutput`（没有 `Metallic / Smoothness`）而不是 `SurfaceOutputStandard`，因为你要接管整个光照方程而不是填给 PBR。

在 `LightingCel` 里，最原始的两色 cel shading 就是一句三目：

```hlsl
float diffuse = dot(normal, lightDir);
diffuse = diffuse > 0 ? 1 : 0;
```

但硬阈值会产生可见锯齿（阴影边界是 1 个像素宽的 step）。Ilett 的抗锯齿方案是**让过渡宽度随屏幕空间梯度自适应**：

```hlsl
float delta = fwidth(diffuse) * _Antialiasing;
float diffuseSmooth = smoothstep(0, delta, diffuse);
```

`fwidth = abs(ddx) + abs(ddy)` 反映了 diffuse 这个标量在相邻像素间变化多快——在光照中间它近乎 0，在明暗边界它突然变大。用它作为 `smoothstep` 的上界，边界像素得到一个 1-2 像素宽的柔和过渡，而大片光区和阴影区保持纯色。`_Antialiasing` 是美术可调的倍率，数值太大就会变成普通渐变、卡通感尽失。

## 镜面高光也要量化

Specular 做同样的处理：`halfVec = normalize(lightDir + viewDir)`、`specular = pow(dot(normal, halfVec) * diffuseSmooth, _Glossiness)`。乘 `diffuseSmooth` 是为了**防止阴影面出现高光**——在背光位置高光永远被 0 遮蔽。然后再用 `smoothstep(0, 0.01 * _Antialiasing, specular)` 切成硬斑。注意这里**不用 `fwidth`**——specular 的 `pow` 函数使其在边界变化过于剧烈，`fwidth` 会给出很大的值、导致羽化失控，直接用常量上界更稳。

## 第 3 步：Bump Map 与 Fresnel Rim

法线贴图在 surface shader 里接入极其轻量：在 `Input` 里加 `float2 uv_BumpMap`，在 `surf` 里写一句 `o.Normal = UnpackNormal(tex2D(_BumpMap, IN.uv_BumpMap))`。`UnpackNormal` 负责把 `[0,1]` RGB 反压缩成 `[-1,1]` 的切线空间法线（见 [[tangent-space-normal-mapping]]）。`LightingCel` 本来就会 normalize `s.Normal`，所以 `surf` 这边不需要再处理——整个光照计算自动用扰动后的法线进行，明暗细节在 diffuse 阶梯里显现。

Fresnel 则完全是光照函数里加一行：

```hlsl
float rim = 1 - dot(normal, viewDir);
rim = rim * diffuse;                      // 只在受光面发亮
float fresnelSize = 1 - _Fresnel;
float rimSmooth = smoothstep(fresnelSize, fresnelSize * 1.1, rim);
```

乘以 `diffuse`（而不是 `diffuseSmooth`）是 Ilett 的一个小细节：背光面不应该出现 rim 光，但也不想让 rim 光严格跟随 diffuse 的硬色阶——取原始的平滑 `diffuse` 作为 mask 能让 rim 在阴影边界自然淡出。`smoothstep(fresnelSize, fresnelSize * 1.1, rim)` 把 rim 也切成硬阶，上下界相差 10% 留作羽化。

三段光照 `(diffuseSmooth + specularSmooth + rimSmooth) * _LightColor0 + unity_AmbientSky` 最后乘 albedo 输出。

## 第 4 步：沿法线外推 + Stencil 描边

描边用的是经典两 pass 方案，[[cel-shader-outline]] 已有详述——这里补几个 Ilett 版本独有的细节：

- **顶点外推在 object space**：`pos = v.vertex + normalize(v.normal) * _OutlineSize`，然后才过 `UnityObjectToClipPos`。如果顺序反过来、在 clip space 里加法线，透视除法会让远处的描边变细（屏幕空间自适应）——有时候这正是想要的，但 Ilett 教的是"世界空间等宽描边"。
- **Pass 2 关掉 ZWrite 保留 ZTest**：`ZWrite off  ZTest on`。描边不应该污染 depth buffer——否则后面的透明物体排序会以为被描边遮住；但它仍然要做深度测试，否则会穿过其他物体。
- **Stencil 双 Ref**：Pass 1 写入 `Ref 1 Comp always Pass replace`，Pass 2 读取 `Ref 1 Comp notequal`。外推后的描边 mesh 覆盖了整个模型区域，但只有「原模型未写入 stencil 的像素」才会被着色——正好等于"外边缘的一圈"。

## 第 5 步：Stencil ID 化 + Lighting Ramp 纹理

**Stencil ID** 是 Part 4 写死 `Ref 1` 的延伸修复。两个用同 ref 值的物体在空间上重叠时，后画的物体的外推 pass 会被前一个物体的 stencil 挡住，导致描边断裂。解法是把 ref 做成材质属性：

```shaderlab
Properties { _ID("Stencil ID", Int) = 1 }
Stencil { Ref [_ID] ... }
```

每个材质用不同的 `_ID`，就能避免相互干扰；反过来，**故意给多个 mesh 同一个 ID** 可以把它们当成"一个整体"描边——Ilett 用这个技巧把 Ethan 模型的身体和眼镜合成一条外轮廓。这也是 Borderlands 风格的惯用做法：整体一圈粗描边 + 细节在贴图里烘焙。

**Lighting Ramp 纹理**则替换掉了 `fwidth + smoothstep` 的硬阶生成逻辑。给一张 2D 纹理（通常只用一行像素），把 `diffuse` 映射到 u 轴：

```hlsl
float3 diffuseSmooth = tex2D(_LightingRamp, float2(diffuse * 0.5 + 0.5, 0.5));
```

`diffuse * 0.5 + 0.5` 把 `[-1, 1]` 的点乘结果映射到 `[0, 1]` 采样坐标。纹理要点——**Wrap Mode 必须设 Clamp**，否则 `diffuse = ±1` 时会采到另一端产生伪影。这个方案的好处：

- **多段光照无需代码**：想要 3 段、5 段，改一张贴图即可；纯 shader 做 N 段要写 N 个 smoothstep。
- **暖色阴影自由做**：ramp 纹理可以携带颜色，左半边紫、右半边白就给了紫色阴影的"半写实卡通"。
- **美术工作流**：完全在 Photoshop 里迭代，不需要改 `.shader` 文件。

代价是**一次额外的纹理采样**——移动端批量使用时要权衡带宽。这条思路本质上和 [[cel-shader-outline]] 中 Linden 的 ramp 方案是同一个，只是 Ilett 把它作为"可选的 Part 5 升级"，而 Linden 从一开始就只讲 ramp 写法。

## 与 PBR 管线的关系

这套 cel 管线依赖两样非 PBR 时代的东西：

1. **Surface Shader + 自定义 Lighting 函数** —— URP 里完全没有；URP 要做同样的事得在 `HLSLPROGRAM` 里手写完整 forward 光照循环，或者用 Shader Graph 的 Custom Function 节点。
2. **双 pass Stencil** —— URP 也支持，但 [[scriptable-render-pipeline|SRP]] 默认 pipeline 里对 stencil 的写入/读取管理更严格，需要自己用 Renderer Feature 排序两个 pass。

所以 2020 年以后这套教程整体被改写——概念和数学完全不变，变的只是"光照循环怎么拿进来"。对 toon shader 的理解本身，这 5 篇仍然是绕不开的入门路径。

## 相关
- [[diffuse-lighting-lambertian]] —— Lambert 公式在 cel shading 之前的原始形态
- [[cel-shader-outline]] —— Linden 的纯 ramp 版本，和本文第 5 步共享思路
- [[unity-surface-shaders]] —— 自定义 Lighting 函数的宿主
- [[tangent-space-normal-mapping]] —— bump map 的前置理解
- [[stencil-buffer]] —— 描边 pass 的核心机制
- [[normalised-blinn-phong-shader]] —— 能量守恒版 Blinn-Phong
- [[coordinate-spaces]] —— 为什么 outline 必须在 object space 外推
- [[toon-outline-post-process-modes]] —— Toon Shaders Pro 的六种描边算法目录（屏幕空间 / 物体 mask / inverted hull）

## Sources
- [[sources/danielilett-cel-shading-part-0]]
- [[sources/danielilett-cel-shading-part-2]]
- [[sources/danielilett-cel-shading-part-3]]
- [[sources/danielilett-cel-shading-part-4]]
- [[sources/danielilett-cel-shading-part-5]]
- [[sources/danielilett-godot-visual-shaders]] —— 系列延伸到 Godot：Dissolve / Hologram / Hull Outline 在 VisualShader 里的等价实现
- [[sources/danielilett-toon-shaders-pro-toon]] —— Toon Shaders Pro 核心 HLSL shader 的参数手册，把 diffuse / specular / rim / shadow 四层各自独立 smoothstep 阈值化的完整开关清单
- [[sources/danielilett-toon-shaders-pro-toon-graph]] —— 上同 Shader Graph 变体，暴露 CalculateToonLighting subgraph 给 SG 用户再利用
- [[sources/danielilett-toon-shaders-pro-terrain]] —— Terrain 专版：去掉 base color 接入 splatmap、新增 stochastic texturing 消 tiling、独立 Ambient Light Strength floor
