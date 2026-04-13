---
title: '[Good for shader debug] UAV RandomWriteTarget'
url: https://cmwdexint.com/2017/06/16/good-for-shader-debug-uav-randomwritetarget/
author: Ming Wai Chan
published: '2017-06-16'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Send data to **c# script** from **shader**: vert/frag and surface shaders!


**C# Script**

It keeps a compute buffer which stores the float array, and it’s buffer size is declared to store three float values (4 byte each). The compute buffer will then bind to number 4 UAV buffer.

On each frame when you hit play, it grabs the value of the compute buffer and show them on console.

using UnityEngine; using System.Collections; public class UAVTest : MonoBehaviour { public Material mat; private ComputeBuffer fieldbuf; private float[] fdata = new float[3]; void OnEnable() { Setup(); } void OnDisable() { if (fieldbuf != null) { fieldbuf.Release(); fieldbuf.Dispose(); fieldbuf = null; } } void Setup() { if (fieldbuf == null) { fieldbuf = new ComputeBuffer(3, sizeof(float), ComputeBufferType.Default); } } void OnRenderObject() { Graphics.ClearRandomWriteTargets(); Setup(); mat.SetPass(0); mat.SetBuffer("Field", fieldbuf); Graphics.SetRandomWriteTarget(4, fieldbuf); fieldbuf.GetData(fdata); for (int i = 0; i < fdata.Length; i++) { print(mat.name+" : " + i + ": " + fdata[i]); } } }

### Vert and Fragment shader

It also keeps a structured float array and it’s using the number 4 UAV buffer. You can assign values to the float array in pixel shader. Things that you need to add into your shader code:

- #pragma target 5.0
- Since it’s using compute buffer

- RWStructuredBuffer Field : register(u4);
- Remember to match the number in C# script

- Field[0] = 12.3;, Field[1] = 4.56;, Field[2] = 0.789f;
- Since you declared there are 3 float values in C# script so you are free to use them at anywhere in fragment shader


Shader "UAVTest/VertFrag" { Properties { _MainTex("_MainTex (RGBA)", 2D) = "white" {} } SubShader { Tags{ "RenderType" = "Opaque" } LOD 200 Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #pragma target 5.0 #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; sampler2D _MainTex; float4 _MainTex_ST; RWStructuredBuffer Field : register(u4); v2f vert(appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); return o; } fixed4 frag(v2f i) : SV_Target { float4 col = tex2D(_MainTex, i.uv); Field[0] = 12.3; Field[1] = 4.56; Field[2] = 0.789f; return col; } ENDCG } } }

### Surface shader

It’s actually same as vert+frag shader. But more things need to be done:

- Wrap the buffer codes with #ifdef UNITY_COMPILER_HLSL … #endif
- Surface shader is not ordinary shaders…

- Others are just same as vert and frag!

Shader "UAVTest/VertSurf" { Properties { _Amount("Extrusion Amount", Range(-1,1)) = 0.5 _MainTex("Albedo (RGB)", 2D) = "white" {} _Glossiness("Smoothness", Range(0,1)) = 0.5 _Metallic("Metallic", Range(0,1)) = 0.0 } SubShader { Tags{ "RenderType" = "Opaque" } LOD 200 CGPROGRAM #pragma surface surf Standard fullforwardshadows addshadow vertex:vert #pragma multi_compile_instancing #pragma target 5.0 sampler2D _MainTex; struct Input { float2 uv_MainTex; }; half _Glossiness; half _Metallic; #ifdef UNITY_COMPILER_HLSL RWStructuredBuffer Field : register(u4); #endif //D3D 64KB * 500 Objects OPENGL 16KB * 125 Objects UNITY_INSTANCING_CBUFFER_START(Props) UNITY_DEFINE_INSTANCED_PROP(float, _Amount) UNITY_INSTANCING_CBUFFER_END void vert(inout appdata_full v, out Input o) { UNITY_INITIALIZE_OUTPUT(Input,o); UNITY_SETUP_INSTANCE_ID(v); v.vertex.xyz += v.normal * UNITY_ACCESS_INSTANCED_PROP(_Amount); } void surf(Input IN, inout SurfaceOutputStandard o) { fixed4 c = tex2D(_MainTex, IN.uv_MainTex); o.Albedo = c.rgb; o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; #ifdef UNITY_COMPILER_HLSL Field[0] = 0.123f; Field[1] = 0.0456f; Field[2] = 0.00789f; #endif } ENDCG } }

### Result

On the scene, create a sphere, create a material using either shader, assign the script, and hit play.

You will see 3 float values which comes from shader on console. 🙂

Project Link: [https://drive.google.com/file/d/0BwLgUykgFtANVTdSaDF6R2FvaWs/view?usp=sharing](https://drive.google.com/file/d/0BwLgUykgFtANVTdSaDF6R2FvaWs/view?usp=sharing)

OR

## One thought on “[Good for shader debug] UAV RandomWriteTarget”