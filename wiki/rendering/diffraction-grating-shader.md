---
tags: [渲染, shader, 物理光学, 衍射, 切向, unity]
date: 2026-04-14
sources: 1
---

# 衍射光栅着色器（CD-ROM）

CD-ROM 表面在光下出现的彩虹色反射并不是染料或涂层——而是**衍射光栅**（diffraction grating）现象：圆心排列的微细沟槽宽度接近可见光波长，不同波长的光在不同观察角度发生相长干涉，形成色散。[[alan-zucconi|Alan Zucconi]] 的 CD-ROM Shader 系列把这个物理模型搬进了 Unity Surface Shader。

## Grating 方程的简化形式

从光栅方程出发，给定入射角 $\theta_L$、观察角 $\theta_V$、光栅周期 $d$ 和 衍射阶 $n$，被相长干涉保留下来的波长为：

$$\lambda_n = \frac{d\,|\sin\theta_L - \sin\theta_V|}{n}$$

把这翻译进 shader，只需要切向方向 $T$（而不是传统的法线 $N$）——因为对一条沟槽来说，**法线到处都朝外**，能区分"沿槽 vs 垂直于槽"的只有切向。用切向和光向、视线的点积就可以同时拿到两个正弦值：

$$T \cdot L = \sin\theta_L, \qquad T \cdot V = \sin\theta_V$$

然后对几个 $n = 1 \dots 8$ 阶循环，每阶算一个 $\lambda_n$，用 [[spectral-zucconi-rainbow|branchless 的 `spectral_zucconi6`]] 把波长转成 RGB，再把所有阶累加叠到原本的 PBR 颜色上。整段 lighting function 只有十几行。

## 从 UV 推出局部切向

CD 的 tracks 是同心圆排列的，不能用模型自带的 tangent。作者用一个非常巧妙的 trick：**直接从 UV 坐标算切向**。假设 CD 的 UV 被映射成一张 (0,0)→(1,1) 的 quad：

```hlsl
// uv: [-1, +1]
fixed2 uv           = IN.uv_MainTex * 2 - 1;
fixed2 uv_radial    = normalize(uv);                              // 指向外，圆心→点
fixed3 uv_tangent   = fixed3(-uv_radial.y, 0, uv_radial.x);       // 正交旋转 90° → 沿同心圆切向
```

再把 tangent 从 object space 变换到 world space：

```hlsl
worldTangent = normalize(mul(unity_ObjectToWorld, float4(uv_tangent, 0)));
```

这一步必须在 **surface function** 里做——因为 UV 坐标在自定义 `LightingXxx` 函数里不可见。这是 Unity Surface Shader 里常见的 "在 surf 阶段提前算好、通过全局变量传给 lighting 阶段" 的模式。

## 与 Zucconi Rainbow 的组合

```hlsl
float u = abs(dot(L, T) - dot(V, T));   // = |sinθ_L - sinθ_V|
fixed3 color = 0;
for (int n = 1; n <= 8; ++n) {
    float wavelength = u * d / n;
    color += spectral_zucconi6(wavelength);
}
pbr.rgb += saturate(color);
```

多阶叠加 + 饱和钳位是为了呈现「越靠近正反射角，高阶衍射越亮」的感觉。参数 `d`（槽距）控制彩虹的张角——把它交给美术就能在肥皂泡、CD、羽毛等不同尺度的 grating 之间切换。

## 为什么切向方法比 anisotropic BRDF 简单

传统各向异性 BRDF（Ward, Ashikhmin-Shirley）也能做出沿沟槽方向锐利拉长的高光，但需要预计算 tangent 场 + 额外的 NDF。衍射光栅着色器的妙处在于它**直接抓住了物理本质的那一步**——`sinθ_L - sinθ_V`——省略了整个微表面统计框架，只靠一个光栅方程 + 波长 RGB 化就得到了彩虹色散。代价是它对材质整体粗糙度、多次散射都不建模，只做「在 grating 上发生什么」这一件事。

## 相关

- [[spectral-zucconi-rainbow]] — 提供 wavelength→RGB 的子例程
- [[physically-based-shading]] — 调用它的宿主 BRDF
- [[shader-vector-math-primer]] — 切向 / UV / 坐标系知识
- [[coordinate-spaces]]
- [[alan-zucconi]]

## Sources

- [[sources/alanzucconi-cdrom-diffraction-2]]
