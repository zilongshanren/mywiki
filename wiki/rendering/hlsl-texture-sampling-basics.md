---
tags: [hlsl, unity, urp, 纹理, 采样, 入门]
date: 2026-04-19
sources: 1
---

# HLSL 纹理采样的五件套

URP / HDRP 时代 Unity 放弃了内建 RP 的 `sampler2D _MainTex; tex2D(...)` 这套老 API，改用**分离式** `TEXTURE2D` + `SAMPLER` 宏（和 DX11+、Metal、现代 GL 对齐）。Ilett 的 Shader Code Basics Part 02 把最小可用的纹理采样流程拆成五个组件，记住这五个就能写新 shader。

## 五件套

在 `HLSLPROGRAM` 块内，每张要采样的纹理都要声明这些：

```hlsl
float4 _BaseTexture_ST;          // (tilingX, tilingY, offsetX, offsetY)
TEXTURE2D(_BaseTexture);         // 声明纹理资源
SAMPLER(sampler_BaseTexture);    // 声明 sampler
```

配合 ShaderLab 一侧：

```
Properties
{
    _BaseTexture("Base Texture", 2D) = "white" {}   // 注意尾部 {} 必须有
}
```

然后 vertex shader 里：

```hlsl
o.uv = TRANSFORM_TEX(v.uv, _BaseTexture);   // 展开为 v.uv * _ST.xy + _ST.zw
```

fragment shader 里：

```hlsl
float4 col = SAMPLE_TEXTURE2D(_BaseTexture, sampler_BaseTexture, i.uv);
```

五件套 = `TEXTURE2D` + `SAMPLER` + `_ST` + `TRANSFORM_TEX` + `SAMPLE_TEXTURE2D`。

## 每一件做什么

- **`TEXTURE2D(name)`** —— 底层展开为 `Texture2D name` 的 HLSL 5.0 纹理资源。注意这里不含 sampler，这是和老 `sampler2D` 的区别。
- **`SAMPLER(sampler_name)`** —— 声明一个 **SamplerState**。`sampler_` + 纹理名是 Unity 的约定：这样声明的 sampler 会**自动继承纹理 Inspector 里的 Wrap/Filter 设置**。如果想绕过 Inspector 设置，可以 include `GlobalSamplers.hlsl` 然后用 `sampler_LinearRepeat` / `sampler_PointClamp` 这种**全局共享**的 sampler（见 [[sampler-filter-wrap-modes]]）。
- **`_BaseTexture_ST`** —— `S`caling `T`ranslation。`float4` 的 xy 是 tiling（平铺数），zw 是 offset（位移）。每张 2D 纹理自动隐含一个这样的变量，是 Unity 为 `Tiling and Offset` 字段做的约定。
- **`TRANSFORM_TEX(uv, tex)`** —— 宏，展开为 `uv * tex##_ST.xy + tex##_ST.zw`。把 mesh 自带的 UV 乘平铺加偏移。一般在 vertex shader 里做（vertex 插值器自动把结果插到每个 fragment）。
- **`SAMPLE_TEXTURE2D(tex, sampler, uv)`** —— 宏，展开为 `tex.Sample(sampler, uv)`。跨平台兼容 API——在 Metal / Vulkan 下 Unity 会替换为对应的内建调用。

## Mesh 那一侧：UV 来自 `TEXCOORD0` 语义

mesh vertex 除了 position，会挂上**最多 8 条 UV 通道**（`TEXCOORD0..7`）。0 号是"正常 UV"，其余通常存 lightmap UV（1 号）、detail UV、custom data。appdata 里写：

```hlsl
struct appdata
{
    float4 positionOS : POSITION;
    float2 uv         : TEXCOORD0;
};
```

`v2f` 也要有一个 `TEXCOORD0` 字段把插值后的 UV 传给 fragment。[[vertex-shader-basics|rasterizer]] 负责三角形内插值。

## 滚动贴图：`_Time.y * _ScrollSpeed`

想让贴图随时间移动（云、河水、传送带）：

```hlsl
float2 uv = i.uv + _Time.y * _ScrollSpeed;
float4 col = SAMPLE_TEXTURE2D(_BaseTexture, sampler_BaseTexture, uv);
```

`_Time` 是 Unity 全局 uniform，四个分量分别是 `(t/20, t, 2t, 3t)`。大多数时候用 `_Time.y`。注意如果滚动贴图要无缝循环，纹理的 Wrap Mode 必须是 **Repeat**——否则 UV 超出 `[0, 1]` 就会被 clamp 成一片死色。

## 关于采样是否花钱

每次 `SAMPLE_TEXTURE2D` 都是一次 GPU 纹理读——会走 texture cache、依据 mipmap level 拿数据。**带宽通常是 shader 的主要瓶颈**，在 mobile / TBDR 上尤其敏感。两张纹理采样的微优化见 [[two-texture-sampling-tricks]]。

## 相关

- [[shaderlab-hlsl-basics]]
- [[sampler-filter-wrap-modes]]
- [[srp-batcher-cbuffer]] —— 和纹理采样在同一份教程里讲的 SRP Batcher 入门
- [[two-texture-sampling-tricks]]
- [[vertex-shader-basics]]
- [[uv-manipulation-nodes]]

## Sources

- [[sources/danielilett-shader-code-textures-uvs]]
