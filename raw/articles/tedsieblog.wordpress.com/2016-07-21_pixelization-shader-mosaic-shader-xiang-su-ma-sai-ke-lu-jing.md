---
title: Pixelization Shader (Mosaic Shader) – 像素、馬賽克濾鏡
url: https://tedsieblog.wordpress.com/2016/07/21/pixelization-shader-mosaic-shader/
author: Ted Sie
published: '2016-07-21'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

像素化效果又或是稱作馬賽克效果

常常運用在特殊風格的遊戲中

這次用了三種不同方式實作了馬賽克效果


1.單一物體表面

Shader "Unlit/Pixelization Shader" { Properties { _MainTex ("Base (RGB) Trans (A)", 2D) = "white" {} _PixelSize ("Pixel Size", Range(0, 1.0)) = 100 } SubShader { Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" sampler2D _MainTex; fixed _PixelSize; struct appdata { fixed4 vertex : POSITION; fixed2 uv : TEXCOORD0; }; struct v2f { fixed4 vertex : SV_POSITION; fixed2 uv : TEXCOORD0; }; v2f vert(appdata v) { v2f o; o.uv = v.uv; o.vertex = mul(UNITY_MATRIX_MVP, v.vertex); return o; } fixed4 frag(v2f i) : COLOR { fixed2 uv = i.uv; if(_PixelSize != 0) { uv = fixed2((int)(uv.x / _PixelSize), (int)(uv.y / _PixelSize)) * _PixelSize; } fixed4 col = tex2D(_MainTex, uv); return col; } ENDCG } } }

原始畫面

![pixelization object normal](../../assets/1e4649a34d7aab65.png)


馬賽克效果

![pixelization object effect](../../assets/67dbd5c87eb87896.png)


2.Image Effect

將 PixelizationImageEffect.cs 附加到場景中的 Camera

並配合上面的 Pixelization Shader

using UnityEngine; using System.Collections; [ExecuteInEditMode] public class PixelizationImageEffect : MonoBehaviour { [Range(0, 1.0f)] public float pixelSize = 0.0f; private string m_pixelSizePropertyName = "_PixelSize"; private int m_pixelSizeID; private Material m_material; void Awake () { InitPropertyIDs(); } private void InitPropertyIDs() { if(m_material == null) m_material = new Material( Shader.Find("Unlit/Pixelization Shader") ); m_pixelSizeID = Shader.PropertyToID(m_pixelSizePropertyName); } private void OnValidate() { if(m_material == null) m_material = new Material( Shader.Find("Unlit/Pixelization Shader") ); m_material.SetFloat(m_pixelSizeID, pixelSize); } void OnRenderImage (RenderTexture source, RenderTexture destination) { Graphics.Blit (source, destination, m_material); } }

原始畫面

![pixelization image effect normal](../../assets/64de6415d1522611.png)


馬賽克效果

![pixelization image effect effect](../../assets/3bb1dc6324bc9d6a.png)


3.特定螢幕區域

常常我們會有這種特殊需求

需要為特定範圍的螢幕做特殊處理

這時候無論是處理一般物體的表面或是 Image Effect 都不能達到這個效果

所以我們利用了 GrabPass 這個渲染通道

來抓取螢幕的特定區域並做效果處理

Shader "Unlit/Grab Pixelization Shader" { Properties { _PixelSize ("Pixel Size", Range(0, 1.0)) = 100 } SubShader { Tags { "Queue" = "Transparent+1" } GrabPass {} Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" sampler2D _GrabTexture; float4 _GrabTexture_TexelSize; fixed _PixelSize; struct appdata { fixed4 vertex : POSITION; }; struct v2f { fixed4 vertex : SV_POSITION; fixed4 uv : TEXCOORD0; }; v2f vert(appdata v) { v2f o; o.vertex = mul(UNITY_MATRIX_MVP, v.vertex); o.uv = ComputeScreenPos(o.vertex); return o; } fixed4 frag(v2f i) : COLOR { fixed4 uv = i.uv; if(_PixelSize != 0) { uv.xy = fixed2((int)(uv.x / _PixelSize), (int)(uv.y / _PixelSize)) * _PixelSize; } fixed4 col = tex2Dproj(_GrabTexture, UNITY_PROJ_COORD(uv)); return col; } ENDCG } } }

在場景中新增 Quad 並將賦有 Grab Pixelization Shader 的 Material 附上

![Grab Pixel Material](../../assets/ef89f8a127bdb0f8.png)


接著就可以移動 Quad 來對特定區域做馬賽克效果處理

![Grab Pixelation Shader](../../assets/93361b56462f6cd2.gif)


不好意思打擾一下，Grab Pixelization Shader 中 41行 應該為 ComputeGrabScreenPos。

我自己實驗的結果是跟 ComputeScreenPos 差一個Y軸，不過不太確定是不是就是因為左手/右手座標系的取出來的差別

謝謝您。

LikeLike

可以直接使用 ComputeGrabScreenPos 來取得 grabUV

也可以透過 ComputeScreenPos 並搭配 UNITY_PROJ_COORD(uv)

但這邊還是直接使用 ComputeGrabScreenPos 會更適合

LikeLike

您好，不過我自己是這樣的方式還是會有上下顛倒的問題耶。

我的版本是5.5.2f1，shader code 是直接貼上您上面的連結，想詢問是不是我有哪邊搞錯了。

目前我是用ComputeGrabScreenPos + UNITY_PROJ_COORD 就沒有問題，用 ComputeScreenPos 的話不管有沒有套 UNITY_PROJ_COORD 都會顛倒的樣子

LikeLike

已經追蹤不到這邊使用的 Unity 版本

目前若是會使用到 GrabPass 或是 command buffer

我也都是直接使用 ComputeGrabScreenPos 來直接取得 uv 了

LikeLike

平台差異也許是導致顛倒的可能性之一

我測試的環境都是在 Macbook 進行的

GPU 是使用 DirectX 的話就有可能會導致顛倒的情況發生

因為在進行這個測試的當下並沒有考慮到平台差異的部分

LikeLiked by 1 person

原來可能是因為DirectX 跟 OpenGL 的座標系導致差異啊….

謝謝您的解說，謝謝您！

LikeLike

应该不会是平台的原因，Unity是封装OpenGL，坐标系的转换是内置好的，

LikeLike