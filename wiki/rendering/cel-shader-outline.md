---
tags: [渲染, shader, toon, 光照, stencil, unity]
date: 2026-04-14
sources: 1
---

# Cel Shader 与描边（Cel Shader with Outline）

Cel shading 是最经典的非 PBR 风格化光照：阴影边界硬、色块分明、看起来像手绘赛璐珞。配上一圈纯色描边，整个模型就有了漫画风的封闭轮廓。Linden 的教程把这两个部件拆成一个 Unity shader 的两 pass：**Pass 1 做 ramp lighting + albedo**，**Pass 2 做法线 extrude + stencil test 后的纯色描边**。核心技巧只有两条——**用 ramp 纹理代替连续光照函数**和**用 [[stencil-buffer]] 让第二次绘制避开原模型区域**。

## Cel 光照：把 dot(N, L) 喂给 ramp

经典 Lambert 光照得到的是 `max(0, dot(N, L))`——一个平滑的 `[0, 1]`。cel 效果要的是**两到三段阶梯**，Linden 的解法不是写一堆 `if`、也不是用 `step`，而是把这个标量当作一张 **1D ramp 纹理**的 u 坐标去采样：

```hlsl
float ramp = saturate(dot(input.normal, lightDir));
float3 lighting = tex2D(_RampTex, float2(ramp, 0.5)).rgb;
float3 rgb = albedo.rgb * lighting * _Color.rgb;
```

ramp 纹理要点：**水平方向从深到亮，只有几段硬色阶**（比如左半边深蓝、右半边白），且采样模式设为 clamp+point，不要双线性过滤——否则色阶之间出现插值。把光照梯度外化成一张 2D 纹理资产的好处是**美术调整不用改代码**：想要暖阴影就把左半边改成紫色，想要三段光就切成黑/灰/白。这和 [[texture-encoded-state|texture-encoded state]] 的思路一致——把本该在代码里分支的逻辑编码进纹理。

一个典型的新手错误是把 ramp 采样放到 vertex shader 而不是 fragment shader：vertex 阶段只有顶点法线，三角形内部的 lighting 被线性插值，硬色阶在面的中间就会被 smear 成渐变。**光照必须在 fragment 做**，才能每像素查表。

## 描边：沿法线 extrude + stencil mask

描边这一步更有意思。做法是把模型再画一遍，但沿顶点法线外推一小段 `_OutlineExtrusion`：

```hlsl
float3 normal = normalize(input.normal);
float4 newPos = input.vertex + float4(normal, 0.0) * _OutlineExtrusion;
output.pos = UnityObjectToClipPos(newPos);
```

不沿 `vertex * scale` 做缩放的原因是：缩放会把描边厚度按模型离中心的距离放大，凹面位置描边会变薄甚至反转。**沿法线推**保证了所有面的描边厚度都相等，即使是复杂非凸几何也能得到均匀轮廓。

但这样做会让描边 mesh 完全覆盖原模型——需要一个机制把原模型区域里的描边像素剔掉。Linden 用的是 [[stencil-buffer|stencil buffer]]：

```hlsl
// Pass 1（原模型）：
Stencil { Ref 4  Comp always  Pass replace  ZFail keep }

// Pass 2（描边）：
Cull OFF
Stencil { Ref 4  Comp notequal  Fail keep  Pass replace }
```

Pass 1 把原模型覆盖的所有像素在 stencil buffer 标成 `4`。Pass 2 画放大后的 mesh，但只有 stencil 不等于 `4` 的像素才会写入——于是原模型内部被 mask 掉，只剩下「外扩的一圈」露出来，在视觉上形成描边。`Cull OFF` 是为了让描边 pass 不 backface culling，否则沿法线外推的顶点如果面朝内会被丢掉，描边就会断。

几处作者反复踩过的坑：

- **非 manifold mesh**：如果模型的面在共享顶点时不共享索引（低模 / 拼接 mesh 常见），法线 extrude 会让本该相邻的面之间出现裂缝——和 [[procedural-greeble|procedural greeble]] 遇到的问题本质相同。**必须用 manifold mesh**。
- **Skybox clear flag**：评论里有人发现相机 clear flag 设为 skybox 时描边不显示——这通常是因为 skybox 会写入 stencil 为 0，导致 stencil 比较全部通过，outline 把自己盖掉了。
- **描边过粗时边界锯齿**：因为它本质是放大版 mesh 的光栅化，没有任何抗锯齿手段；要缓解只能用 post AA（[[analytical-antialiasing|analytical AA]] 对固定宽度的 stencil outline 无效）。

## 设计取舍

两 pass 的 cel+outline 是教科书级的 multi-pass shader 例子：

- 它**不修改主 pass 的光照**，所以可以同 [[stylized-water-shader|水面]]、[[texture-dissolve|dissolve]] 等效果自由叠。
- 它用 stencil 而不是 depth 来做 masking，因此**不需要改变 depth test 顺序**——比「先画外扩 mesh 后画本体，靠深度遮挡」更稳定。
- 它只适合**有清晰轮廓的卡通风格**。真实 PBR 场景里这种硬描边会显得突兀，且两遍绘制对移动端带宽敏感。

## 相关

- [[stencil-buffer]] —— 描边依赖的核心机制
- [[texture-encoded-state]] —— 把逻辑外化到纹理的范式
- [[procedural-greeble]] —— 同样依赖 manifold mesh 的顶点外推
- [[stylized-water-shader]] —— 同作者同风格，共享 ramp lighting 思路
- [[texture-dissolve]]
- [[sprite-outline-8-direction]] —— 2D sprite 上的同思路「复制副本做外框」
- [[cel-shading-pipeline]] —— Daniel Ilett 5 部曲版本，同样的 cel+outline 思路但从 Phong 光照开始逐步搭建，含 bump/fresnel/stencil-ID 等扩展
- [[animated-dotted-outline-shader]] —— 同一两 pass 管线上把 outline fragment 改成 `sin(distance)` 距离场 + `_Time` 相位平移的动画虚线
- [[godot-visual-shaders]] —— Godot VisualShader 里的等价实现：StandardMaterial + Next Pass 挂 ShaderMaterial、Cull Mode → Front

## Sources

- [[sources/lindenreid-cel-shader-outline]]
- [[sources/danielilett-cel-shading-part-4]] — Daniel Ilett 版的同一双 pass + stencil 描边，含 ShaderLab 字段（Ref/Comp/Pass/Fail/ZFail）逐条解释
- [[sources/danielilett-cel-shading-part-5]] — Stencil ID 化修复 + lighting ramp 纹理替换硬阶
- [[sources/lindenreid-animated-dotted-outline]] —— 动画虚线描边的 fragment shader 扩展
