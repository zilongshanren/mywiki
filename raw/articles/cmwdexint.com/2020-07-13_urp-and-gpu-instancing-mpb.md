---
title: URP and GPU instancing & MPB
url: https://cmwdexint.com/2020/07/13/urp-and-gpu-instancing-mpb/
author: Ming Wai Chan
published: '2020-07-13'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Tested with: 2020.1.0b16.4138 + **URP 9.0.0-preview.38**, Windows DX11

**Objects with same material & same property values**

| SRP batcher ON material GPU instancing OFF | SRP batched |
| SRP batcher ON material GPU instancing ON | SRP batched (because if SRP batcher is ON, gpu instancing will be ignored) |
| SRP batcher OFF material GPU instancing ON | GPU instanced |

**Objects with different material & ****different** **property values**

**Objects with different material &**


**different****property values**

| SRP batcher ON material GPU instancing OFF | SRP batched |
| SRP batcher ON material GPU instancing ON | SRP batched (because if SRP batcher is ON, gpu instancing will be ignored) |
| SRP batcher OFF material GPU instancing ON | Not batched nor instanced (expected because they are different materials) |

**Objects with same material & ****different** **property values** set by MaterialPropertyBlock

**Objects with same material &**


**different****property values**set by MaterialPropertyBlock

| SRP batcher ON material GPU instancing OFF | Not batched nor instanced (because MPB values are not same) |
| SRP batcher ON material GPU instancing ON | Not batched nor instanced (same as above) |
| SRP batcher OFF material GPU instancing ON | Not batched nor instanced (because properties are non-instanced) |

According to [Unity Documentation about GPU instancing](https://docs.unity3d.com/Manual/GPUInstancing.html), user can use MaterialProperyBlock to have different material properties for each instances.

Apparently the test showed that this is not true anymore in Universal Render Pipeline.

**Reason:**

URP shader properties are all wrapped by SRP batcher macros “CBUFFER_START(UnityPerMaterial)”.

GPU instancing need to use this macro “UNITY_INSTANCING_BUFFER_START(MyProps)”

**Solution:**

What if we really want to have GPU-instanced object with different properties set by MPB?

Edit the URP shader or have a custom shader like this:

Shader "Custom/Instancing In URP" { Properties { _MainTex ("_MainTex (RGBA)", 2D) = "white" {} _Color ("Color 1", Color) = (1,1,1,1) } SubShader { Tags { "RenderType"="Opaque" "DisableBatching" = "True" } Pass { HLSLPROGRAM #pragma vertex vert #pragma fragment frag #pragma multi_compile_instancing #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; UNITY_VERTEX_INPUT_INSTANCE_ID }; struct v2f { float4 vertex : SV_POSITION; float2 uv : TEXCOORD0; UNITY_VERTEX_INPUT_INSTANCE_ID }; sampler2D _MainTex; float4 _MainTex_ST; UNITY_INSTANCING_BUFFER_START(MyProps) UNITY_DEFINE_INSTANCED_PROP(float4, _Color) UNITY_INSTANCING_BUFFER_END(MyProps) v2f vert (appdata v) { v2f o; UNITY_SETUP_INSTANCE_ID(v); UNITY_TRANSFER_INSTANCE_ID(v, o); o.vertex = TransformObjectToHClip(v.vertex.xyz); o.uv = TRANSFORM_TEX(v.uv, _MainTex); return o; } float4 frag (v2f i) : SV_Target { UNITY_SETUP_INSTANCE_ID(i); float4 col = tex2D(_MainTex, i.uv); float4 color = UNITY_ACCESS_INSTANCED_PROP(MyProps, _Color); col *= color; return col; } ENDHLSL } } }

thank you so much for this awesome information,

one quick note that you mentioned “(because MPB values are not same)”, I don’t know what you mean here but the reason as documented by Unity is just simply SRP batcher is not compatible with MPB.

for anyone who wants to also change offset and tiling along the _Color you should declare this _TextureST(“Texture ST”, Vector) = (1,1,0,0) in your properties and add this “UNITY_DEFINE_INSTANCED_PROP(float4, _TextureST)” below “UNITY_DEFINE_INSTANCED_PROP(float4, _Color)” that is between the START and END of the buffer and at the end add this in vert function

//o.uv = TRANSFORM_TEX(v.uv, _MainTex);

float4 texST = UNITY_ACCESS_INSTANCED_PROP(MyProps, _TextureST);

o.uv = v.uv * texST.xy + texST.zw;

return o;

which means comment the TRANSFORM_TEX macro and instead use your own instance before returning;

LikeLike

I tried everything the docs recommended and more to get GPU instancing working without just disabling the SRP batcher in its entirety and nothing worked. You are my savior 🙏

LikeLike