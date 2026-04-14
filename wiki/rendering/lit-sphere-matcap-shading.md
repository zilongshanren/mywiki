---
tags: [渲染, shader, 光照, matcap, 风格化, 反查表]
date: 2026-04-14
sources: 1
---

# Lit Sphere 着色：用一张图当光照查找表

**Lit Sphere Shading**（又称 MatCap，ZBrush 里的「材质球着色」）是一种把整个光照-材质响应压进一张 2D 纹理里的技术。它不算 lighting 模型——它**绕开**了 lighting 模型。做法是：用物体表面法线在**屏幕空间**里投影出的 `(x, y)` 作为 UV，直接去采样一张「已经预渲染好」的球体图像。这张图像本身是某种光照下的反射结果，所以任何被这个 shader 覆盖的物体都会继承它的整体光感——高光、阴影、rim、背光全都一次性来。

[[simon-trumpler|Simon Trümpler]] 在研究《魔兽世界：熊猫人之谜》那个经典的热气球时发现了这项技术的应用。热气球的中心有一团黄色的「热源辉光」，**无论你从哪个角度看，这团辉光都保持在气球正中**。他原以为是 [[fresnel-effect|Fresnel]] 加 mask，但从内存里抓出了 diffuse 贴图的 alpha 通道后才看明白：那是一张二维的径向 gradient——**不是 UV 位置的梯度，而是法线方向的梯度**。Blizzard 的做法是把法线的屏幕空间分量映射成 UV：

```hlsl
float2 matcapUV = normalize(normal_view.xy) * 0.5 * length(normal_view.xy) + 0.5;
float3 litColor = tex2D(_LitSphereTex, matcapUV).rgb;
```

或者更简洁的版本是 `matcapUV = normal_view.xy * 0.5 + 0.5`。于是：

- 面向相机的法线（`normal_view.z ≈ 1`）采样到纹理**中心**——被染成最亮的黄色辉光
- 法线向两侧偏（接近气球轮廓）时采样到**纹理边缘**——对应气球外圈的暗红气囊颜色
- 整张图相当于一个「把所有可能的法线方向都打包好」的查找表

这就是为什么辉光「永远在中心」：它和世界空间无关，只和**哪些表面法线碰巧朝向相机**有关。你把气球转个 180 度，辉光依然在气球正中——因为表面法线面向相机的位置变了，但「面向相机」这件事本身没变。

## 对比 Fresnel

评论区有人问：这跟 Fresnel 不就是一回事吗？Fresnel 不也用 `dot(N, V)`？答案是**机制像，能力不同**。Fresnel 只是一个标量（`pow(1 - dot(N, V), k)`），它只告诉你「从正视到掠射过渡的一个插值因子」，配色必须另外写。Lit sphere 是一张 2D 纹理——它不仅可以有径向 gradient，**还可以把左右/上下的方向差异编码进颜色**，给出类似「左上打光、右下阴影」的全向响应。Fresnel 是 1D，lit sphere 是 2D；前者是后者的特殊情况。

Simon 后来在更新里补上了 Charles Hollemeersch 给出的**反向 Fresnel**做法：

```hlsl
half fresnel = pow(saturate(dot(normal, viewDir)), sizeOfTheGlow);
half  mask   = tex2D(mymask, uv).r;
half3 color  = half3(mycolor);
half3 glow   = fresnel * color + (bias * color) * mask;
```

这个版本用 `dot(N, V)`（不是传统 Fresnel 的 `1 - dot(N, V)`）——**面向相机的地方更亮**，再用一张 mask 把辉光限制在气球上的特定花纹里。等价的效果、更少的美术资产、更多的 shader 参数；是 lit sphere 的**参数化、低内存**替代。

## 设计取舍

Lit sphere 是一种把**光照响应「产品化」成资产**的思路：美术可以直接在 Photoshop 或 ZBrush 里调一张 matcap 图，交给 shader 程序员接进管线就完事。好处是：

- **艺术家完全主导视觉**。需要哪种高光、哪种冷暖对比，在绘图软件里画就行，不用动 BRDF。
- **成本极低**。一次纹理采样 + 一个 normal-to-UV 计算，便宜到可以给所有次要物件用。
- **和真实光照解耦**。热气球「看起来自发光」完全不需要场景里有对应光源——它的光源被画进了那张 matcap 图里。

代价同样明显：

- **不响应场景光照**。场景里打了多少灯、什么颜色、在哪个方向，lit sphere 都视而不见。这是 Simon 举的例子里它能被接受的原因——*热气球本身就是光源*，根本不需要接外部光照。
- **法线必须在 view space 计算**。World-space 法线会让「光源位置」随着相机旋转——视觉上就不是「光从左上角打过来」了而是「光跟着你转」。
- **无法做阴影和遮挡**。自身法线决定一切，附近物体给它留的阴影进不来。

Lit sphere 在 ZBrush、Sculptris、各种风格化游戏（包括 MMO、独立手绘游戏）里非常常见。它是 [[matcap|matcap]] 这条大路线的核心，也是「把渲染管线外包给 Photoshop」这个哲学里最纯粹的一步。

## 相关

- [[fresnel-effect]] —— 以 `dot(N, V)` 为基础的同类但维度更低的方法
- [[cel-shader-outline]] —— 同样在「把光照外化成资产」这条思路上
- [[texture-encoded-state]] —— 把逻辑编码进纹理的更一般范式
- [[rim-lighting]]

## Sources

- [[sources/simonschreibt-wow-balloon]]
