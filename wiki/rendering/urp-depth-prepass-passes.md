---
tags: [shader, urp, hlsl, depth-buffer, prepass, depth-normals]
date: 2026-04-19
sources: 1
---

# URP 的 DepthOnly / DepthNormals Prepass

URP 下 `_CameraDepthTexture` 并不**总是**直接复制自 depth buffer——它的填充路径取决于管线配置。SSAO、depth-normals 类 outline 这些需要"在不透明绘制之前"就拿到 depth/normal 的效果，会触发 Unity 走一条 **prepass**：在主 opaque 渲染之前先跑一遍每个 opaque mesh 的轻量化 Pass，把深度（和可选法线）写到专用目标。这意味着**自定义 shader 如果没写对应 prepass Pass，就会在这些效果里"消失"**——SSAO 视图里看不到这个物体、描边画不出它的轮廓。

## 两种 prepass

URP 有两条 prepass 路径，互斥选用：

- **DepthOnly Pass**：`LightMode = DepthOnly`。只写深度到 `_CameraDepthTexture`，输出单通道 float。`ZWrite On`、`ColorMask R`（只开红通道，其他 RGB 不浪费带宽）。
- **DepthNormals Pass**：`LightMode = DepthNormals`。同时写深度到 `_CameraDepthTexture` 和 world-space 法线到 `_CameraNormalsTexture`。输出 `float4(normalWS, 0)`，`ZWrite On`，不设 ColorMask（四通道都用）。

Unity 根据 Renderer Feature 需要（SSAO 要 depth+normal 就走 DepthNormals；单纯要 depth 就走 DepthOnly）自动选一条运行。**两个 Pass 都应该在你的 shader 里出现**——缺哪个，对应路径里这个物体就看不见。

## 最小模板

对纯 opaque、不做 vertex 位移或 alpha clip 的 shader，两个 Pass 长这样：

```hlsl
Pass
{
    Tags { "LightMode" = "DepthOnly" }
    ZWrite On
    ColorMask R
    HLSLPROGRAM
    #pragma vertex depthOnlyVert
    #pragma fragment depthOnlyFrag
    #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

    struct appdata { float4 positionOS : POSITION; };
    struct v2f    { float4 positionCS : SV_POSITION; };

    v2f depthOnlyVert(appdata v)
    {
        v2f o = (v2f)0;
        o.positionCS = TransformObjectToHClip(v.positionOS.xyz);
        return o;
    }

    float depthOnlyFrag(v2f i) : SV_TARGET { return i.positionCS.z; }
    ENDHLSL
}

Pass
{
    Tags { "LightMode" = "DepthNormals" }
    ZWrite On
    HLSLPROGRAM
    #pragma vertex depthNormalsVert
    #pragma fragment depthNormalsFrag
    #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

    struct appdata {
        float4 positionOS : POSITION;
        float3 normalOS   : NORMAL;
    };
    struct v2f {
        float4 positionCS : SV_POSITION;
        float3 normalWS   : TEXCOORD0;
    };

    v2f depthNormalsVert(appdata v)
    {
        v2f o = (v2f)0;
        o.positionCS = TransformObjectToHClip(v.positionOS.xyz);
        float3 nWS   = TransformObjectToWorldNormal(v.normalOS);
        o.normalWS   = NormalizeNormalPerVertex(nWS);
        return o;
    }

    float4 depthNormalsFrag(v2f i) : SV_TARGET
    {
        float3 n = NormalizeNormalPerPixel(i.normalWS);
        return float4(n, 0);
    }
    ENDHLSL
}
```

主 Pass 需显式标 `Tags { "LightMode" = "SRPDefaultUnlit" }`（或 `UniversalForward` / `UniversalForwardOnly` / `UniversalGBuffer`，视用途）——不标会被自动归 `SRPDefaultUnlit`，但明示更稳定。

## 当 vertex shader 做了位移怎么办

上面的模板只做 object→clip 变换。如果主 Pass 做了 vertex displacement（wave、skinning 之外的自定义位移）或 alpha clip（[[dither-alpha-clipping]] / `discard`），**这两个 prepass 也必须做**——否则深度写入的是未位移 mesh、被裁剪掉的像素在 depth 里还在。

做法：把主 Pass 的 vertex 数学、CBUFFER、贴图采样全复制进 prepass 的 vert/frag，保留 clip(v.alpha - threshold)、移除光照计算。这是 URP 自定义 shader 的一个日常痛点——**同一份 displacement 数学要抄三份**（主 Pass + DepthOnly + DepthNormals）。

## 与 LightMode tag 家族的关系

URP 所有特殊 Pass 都靠 `LightMode` tag 被 pipeline 挑中：

| LightMode tag | 用途 |
|---|---|
| `SRPDefaultUnlit` | 默认 unlit 主 Pass（不标时的 fallback） |
| `UniversalForward` | URP Lit 标准前向主 Pass |
| `UniversalForwardOnly` | 同 `UniversalForward` 但不支持 deferred（toon / custom lit 常用） |
| `UniversalGBuffer` | Deferred 的 G-Buffer 填充 |
| `DepthOnly` | 本条 |
| `DepthNormals` | 本条 |
| `ShadowCaster` | 阴影投射 |
| `Meta` | 烘焙 lightmap 读元数据 |

[[sources/danielilett-toon-shaders-pro-outline-post|Outline Post Process]] 的 Light Modes 选项就是用这个 tag 决定哪些 shader 的哪些物体被画进 mask。

## 相关

- [[depth-texture-silhouette]] —— 从 `_CameraDepthTexture` 读深度做后处理的前置
- [[early-z-late-z]] —— 为什么 opaque front-to-back + prepass 对 GPU 友好
- [[shaderlab-hlsl-basics]]
- [[urp-render-objects-feature]]

## Sources

- [[sources/danielilett-shader-code-depth-buffer]]
