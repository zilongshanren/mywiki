---
title: ZTest Shader – 物體遮擋效果
url: https://tedsieblog.wordpress.com/2016/07/20/ztest-shader/
author: Ted Sie
published: '2016-07-20'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

在遊戲中常常可以看到一個效果

當物體被其他物體遮擋的時候

會有其他的渲染效果表現


![ztest demo](../../assets/76afa07ed1fcb011.jpg)


(附圖遊戲為 Implosion – Never Lose Hope)

這個效果主要是利用了深度測試來檢測物體在世界空間中的位置

深度越大代表物體越遠離攝影機

而在 Unity 中

深度測試的關鍵字為 ZTest

[ShaderLab: Culling & Depth Testing](https://docs.unity3d.com/Manual/SL-CullAndDepth.html)

下面這個 Shader 是利用簡單的 ZTest 來測試物體是不是被其他物體所遮擋

若是被遮擋則渲染其他效果

Shader "Unlit/ZTest Shader" { Properties { _NormalColor("Normal Color", Color) = (1, 1, 1, 1) _ZTestColor("ZTest Color", Color) = (0, 0, 0, 1) } SubShader { Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" uniform float4 _NormalColor; struct appdata { float4 vertex : POSITION; }; struct v2f { float4 pos : POSITION; }; v2f vert (appdata v) { v2f o; o.pos = mul( UNITY_MATRIX_MVP, v.vertex); return o; } float4 frag(v2f i ) : COLOR { return _NormalColor; } ENDCG } Pass { ZTest Greater CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" uniform float4 _ZTestColor; struct appdata { float4 vertex : POSITION; }; struct v2f { float4 pos : POSITION; }; v2f vert (appdata v) { v2f o; o.pos = mul( UNITY_MATRIX_MVP, v.vertex); return o; } float4 frag(v2f i ) : COLOR { return _ZTestColor; } ENDCG } } }

原始畫面

![ZTest normal](../../assets/8ba5f955a6e5f601.png)


Shader 效果

![ZTest effect](https://tedsieblog.wordpress.com/wp-content/uploads/2016/07/ztest-effect.png?w=300&h=188)


我們也可以試著搭配不同的 Shader 來組合出不一樣的效果

Shader "Unlit/ZTest Outline Shader" { Properties { _NormalColor("Normal Color", Color) = (1, 1, 1, 1) _ZTestColor("ZTest Color", Color) = (1, 1, 1, 1) _OutlineColor ("Outline Color", Color) = (0, 0, 0, 1) _OutlineWidth ("Outline width", Range (0.0, 1.0)) = .005 } SubShader { Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" uniform float4 _NormalColor; struct appdata { float4 vertex : POSITION; }; struct v2f { float4 pos : POSITION; }; v2f vert (appdata v) { v2f o; o.pos = mul( UNITY_MATRIX_MVP, v.vertex); return o; } float4 frag(v2f i ) : COLOR { return _NormalColor; } ENDCG } Pass { ZTest Greater CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float3 normal : NORMAL; }; struct v2f { float4 pos : POSITION; }; uniform float _OutlineWidth; uniform float4 _OutlineColor; v2f vert(appdata v) { v2f o; float3 norm = normalize(v.normal); v.vertex.xyz += v.normal * _OutlineWidth; o.pos = mul(UNITY_MATRIX_MVP, v.vertex); return o; } half4 frag(v2f i) : COLOR { return _OutlineColor; } ENDCG } Pass { ZTest Greater CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float3 normal : NORMAL; }; struct v2f { float4 pos : POSITION; }; uniform float4 _ZTestColor; v2f vert(appdata v) { v2f o; float3 norm = normalize(v.normal); o.pos = mul(UNITY_MATRIX_MVP, v.vertex); return o; } half4 frag(v2f i) : COLOR { return _ZTestColor; } ENDCG } } }

原始畫面

![ZTest normal](../../assets/8ba5f955a6e5f601.png)


Shader 效果

![ZTest outline](../../assets/7f7fb5812dad2eca.png)