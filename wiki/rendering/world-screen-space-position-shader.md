---
tags: [渲染, unity, shader, 坐标, shader-bits]
date: 2026-04-14
sources: 1
---

# Shader 里的 world / screen space position

Shader 里经常要拿到"当前像素对应的世界坐标"或者"当前像素在屏幕里的位置"——前者驱动 [[planar-mapping|triplanar 贴图]]、距离场、雾效、[[abzu-portal-cards-shader|按相机距离 fade 的 portal card]]；后者驱动 scanline、屏幕空间 mask、[[screenspace-reflections|屏幕空间反射]]、[[cel-shader-outline|描边]]、后处理 blit。[[harry-alisavakis|Harry Alisavakis]] 在 *Shader bits* 系列的首篇里把这两件小事整理成一份**可直接抄**的备忘录，覆盖 Unity 里的两种 shader 风格：手写 vertex/fragment 和 surface shader。

## Vertex/fragment：明式传递

手写 vertex/fragment 要显式声明 v2f interpolator 里多出一个字段，在 vertex shader 里算好，再让硬件插值过来。

**World space** 只需一次矩阵乘：

```hlsl
struct v2f {
    float2 uv : TEXCOORD0;
    float4 vertex : SV_POSITION;
    float4 worldPos : TEXCOORD2;
};

v2f vert(appdata v) {
    v2f o;
    o.vertex = UnityObjectToClipPos(v.vertex);
    o.uv = TRANSFORM_TEX(v.uv, _MainTex);
    o.worldPos = mul(unity_ObjectToWorld, v.vertex);
    return o;
}
```

`unity_ObjectToWorld` 是 Unity 预置的对象到世界的模型矩阵——把顶点从模型空间推到世界空间的一次矩阵乘法，就是 [[mvp-transform|MVP 变换]] 链中 M 的那一下。注意 `worldPos` 要用 `float4` 放插值器里，而不是 `float3`，避免插值精度问题。

**Screen space** 则有专门的一行辅助函数：

```hlsl
o.scrPos = ComputeScreenPos(o.vertex);
```

`ComputeScreenPos` 接收 clip space 位置（已经 `UnityObjectToClipPos` 过的），内部完成齐次除法前的映射，返回 `(x, y, z, w)`，其中 `xy / w` 就是 `[0, 1]` 的屏幕 UV。它把"把 clip space 映射到 `[0, 1]` viewport"这个琐碎细节封成了一步，Unity 里要做任何屏幕空间采样（抓 `_CameraDepthTexture` / `GrabPass` / 屏幕遮罩）都先过它。

## Surface shader：`Input` struct 的魔法

Surface shader 的抽象级别更高，不需要手写 vert 和 v2f——Unity 只要看到 `Input` 结构里出现了**带特定名字**的字段，就自动帮你计算。

```hlsl
struct Input {
    float2 uv_MainTex;
    float3 worldPos;   // 写名字就给
    float3 screenPos;  // 同理
};
```

就这么简单。`worldPos` 和 `screenPos` 是 Unity 内置识别的**保留字段名**，写上去它就自动在背后补齐 vertex pass 的计算。这是 surface shader "省事"的一个典型代价平衡：失去了底层控制权，但换来了"想要就写个名字"的便利。这也提示我们，Unity 的 surface shader 在底层其实是一个**代码生成器**——它把 surface 函数包进一个生成出来的 vertex/fragment 骨架里，并根据你 `Input` 里的字段按需 emit 对应的 interpolator。

## `Input` 保留字段速查

类似的"写上名字就生效"的 [[unity-surface-shaders|surface shader]] `Input` 字段还有好几个：

- `float3 viewDir` —— 像素到相机的方向
- `float2 uv_XxxTex` —— 某纹理的 UV（Unity 按前缀识别）
- `float4 color : COLOR` —— 顶点色
- `float3 worldNormal` —— 世界空间法线

这是一套**按约定驱动**的 API：没有 IDL，没有显式注册，识别完全靠名字匹配。好处是把典型需求压到 0 boilerplate，坏处是"你想要的"和"Unity 能识别的"之间有一张隐式白名单，写错一个字母就彻底不工作而且没有报错提示。

## 为什么这是一篇"shader bits"

Alisavakis 在系列首篇里说：这种"小但有用的技巧点"应该有个集中地方被记录下来，方便后人（包括自己）查阅。这篇文章本身就是那种**典型的 TA 备忘录**——没有要讲清楚一个宏大概念，只是把两个常用操作的模版固化下来，避免每次写新 shader 都要翻旧代码。把它收在 wiki 里也是同样的用意：查「worldPos 怎么拿」的时候直接抄。

## 相关

- [[coordinate-spaces]] —— 完整的模型 → 世界 → 视 → 裁 → NDC → 屏幕链条
- [[mvp-transform]] —— 矩阵变换链，`unity_ObjectToWorld` 是其中 M 的具体命名
- [[unity-surface-shaders]] —— surface shader 的代码生成器模型与 `Input` 白名单
- [[planar-mapping]] —— 用 worldPos 生成 UV 的典型下游
- [[abzu-portal-cards-shader]] —— 同作者的前一篇直接用到了这套取 worldPos 的套路
- [[screenspace-reflections]]
- [[cel-shader-outline]]
- [[shader-vector-math-primer]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-shader-bits-world-screen-pos]]
