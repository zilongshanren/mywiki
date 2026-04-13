---
title: Illustrative Rendering in Unity
url: https://tedsieblog.wordpress.com/2017/07/16/illustrative-rendering-in-unity/
author: Ted Sie
published: '2017-07-16'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

#### Abstract

這次的研究對象是 Valve 在 2007 所發表的論文 [Illustrative Rendering in Team Fortress 2](http://www.valvesoftware.com/publications/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf)

在 Unity 中實現相似的 Illustrative Rendering 效果

雖然最後的實驗成果並沒有完全達到《Team Fortress 2》的畫面水準

但是透過這樣的嘗試驗證

學習到許多新的知識及想法



#### Introduction

《Team Fortress 2》是由 Valve 所開發的一款多人連線第一人稱射擊遊戲

在遊戲中透過美術與程式兩者的相互結合

呈現了獨特的 [Non-Photorealistic Renderer](https://en.wikipedia.org/wiki/Non-photorealistic_rendering)（ NPR 非真實渲染 ）

在大部分的非真實渲染中模型與光源並不會產生交互影響

但在這篇論文中說明了能與光源及環境進行有效互動的渲染技術

這次會將重點放在 **Commercial Illustration Techniques**、**Interactive Character and Model Shading** 及 **Unity 實作**三個部分


#### Commercial Illustration Techniques

風格統一是一門很大的學問

Valve 在《Team Fortress 2》中透過規範

制定了五個風格遵循重點

1. Shading 遵守暖到冷的色彩轉換。陰影會接近冷色調，而不是黑色。

2. 在接近光源陰影交接處時，飽和度會增加。而交接處會偏向紅色。

3. 盡可能地省略高頻細節。

4. 在角色的內部細節中，如：服裝皺摺，會選擇性的繪製輪廓線條。

5. 使用 Rim Hightlights（邊緣高光）來強調輪廓線，而非使用深色輪廓線。


#### Interactive Character and Model Shading

在這個小節中討論了非真實渲染演算法

在角色及其他模型的渲染中結合了**非依賴視角光照 與依賴視角光照**兩個部分

##### 非依賴視角光照部分

![](../../assets/21d260e973e515a9.png)


：紋理映射後的反射率（Albedo）


：計算法線與平行環境光的函數


：光源索引


：光源數量


：光源顏色


：將 Lambertian Term（0 至 1）映射到 RGB 顏色的變形函數


：法線向量


：光線方向


：傳統的非限制 Lambertian Term


：Lambertian Term 縮放量


：Lambertian Term 偏移量


：Lanbertian Term 指數量


###### Half Lambert

在 α、β、γ 的選擇上

從 Valve 在 1998 的第一款遊戲《Half-Life》開始

他們就使用 α = 0.5、β = 0.5、γ = 2 的配置來降低角色陰影面的細節損失

儘管在《Team Fortress 2》需要更多的真實感

他們依舊維持這個 Lambertian Term 配置

此外也透過這個配置使得 的結果


從 -1 到 1 映射成 0 到 1 獲得一個更好的衰減映射區域

由於縮放及偏移量都是 0.5

所以將這個配置命名為 Half Lambert

###### Diffuse Warping Function

透過查找美術所提供的一維紋理來取得 RGB 顏色

產生出一種卡通 “hard shading” 風格

這張紋理可以被區分成三個區塊

1. 右側的灰階梯度

2. 左側的冷色梯度

3. 中間的偏紅色陰影交界處

這個分佈區塊與上面所提到的風格遵循重點是一致的

![](../../assets/eeb09c8ea39aee1c.png)



##### View Dependent Lighting Terms

![](../../assets/92d4f006dddb8f8c.png)


：光源索引


：光源數量


：光源顏色


：在紋理通道中的高光遮罩


：由美術調整的 Fresnel 高光參數


：視線方向


：光源方向對於法線的反射向量


：由紋理中取得的高光指數


：另一個 Fresnel 參數，用於調整邊緣高光，一般使用 pow(1 – NdotV, 4)


：邊緣遮罩紋理，用於衰減特定部位的邊緣高光


：調整邊緣高光寬度


：法線向量


：世界空間 up 單位向量


：使用視線方向到像素點所產生的射線來計算 ambient cube 影響


Multiple Phong Terms

為公式左半部分

Dedicated Rim Lighting

為公式右半部分

![](../../assets/6dbd0ab9d7d05dcf.png)



#### Unity 實作

在實作階段中

將各個階段區分出來獨立實作比變更加明白各階段的結果

其中包含了 **Albedo**、**Warped Diffuse**、**Specular**、**Rim Lighting**

在最後的 Final Result 部分

使用了三種不同的 Warped Texture 來達到不同風格的呈現

分別是 **Team Fortress 2**、**Grayscale Gradient** 及 **Horror Style**

##### Albedo

![](../../assets/962db2c4cdce1587.png)


Shader "Custom/Illustrative Rendering/01.Albedo" { Properties { _MainTex ("Texture", 2D) = "white" {} } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; sampler2D _MainTex; float4 _MainTex_ST; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.uv); return col; } ENDCG } } }


##### Warped Diffuse

![](../../assets/596fe2e6b1c56f47.png)


Shader "Custom/Illustrative Rendering/02.WarpedDiffuse" { Properties { _WarpedTex ("Warped Texture", 2D) = "white" {} _WarpedScale ("Warped Scale", Float) = 1 } SubShader { Tags { "RenderType"="Opaque" "LightMode"="ForwardBase" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" #include "UnityLightingCommon.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; half3 normal : NORMAL; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; half NdotL : TEXCOORD1; }; sampler2D _WarpedTex; half4 _WarpedTex_ST; half _WarpedScale; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _WarpedTex); half3 worldNormal = UnityObjectToWorldNormal(v.normal); half3 lightDir = normalize(_WorldSpaceLightPos0.xyz); o.NdotL = dot(worldNormal, lightDir); return o; } fixed4 frag (v2f i) : SV_Target { half halfLambert = pow(0.5 * i.NdotL + 0.5, 2); half2 warpedUV = float2(halfLambert, halfLambert); half3 diffuseWarping = tex2D(_WarpedTex, warpedUV).rgb * _WarpedScale; fixed4 finalColor; finalColor.rgb = diffuseWarping; return finalColor; } ENDCG } } }


##### Specular

![](../../assets/d45d4c2e92d6fbcb.png)


Shader "Custom/Illustrative Rendering/03.Specular" { Properties { _SpecularMask ("Specular Mask", 2D) = "white" {} _Fspec ("Fresnel Specular Term", Float) = 1 _Kspec ("Specular Exponent Power", Float) = 1 } SubShader { Tags { "RenderType"="Opaque" "LightMode"="ForwardBase" } LOD 100 Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" #include "UnityLightingCommon.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; half3 normal : NORMAL; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; half3 VdotR : TEXCOORD1; }; sampler2D _SpecularMask; half4 _SpecularMask_ST; half _Fspec; half _Kspec; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _SpecularMask); half3 worldNormal = UnityObjectToWorldNormal(v.normal); half3 lightDir = normalize(_WorldSpaceLightPos0.xyz); half3 reflectDir = reflect(-lightDir, worldNormal); half3 viewDir = normalize(WorldSpaceViewDir(v.vertex)); o.VdotR = saturate(dot(viewDir, reflectDir)); return o; } fixed4 frag (v2f i) : SV_Target { half4 ks = tex2D( _SpecularMask, i.uv); half3 specularTerm = _Fspec * pow(i.VdotR, _Kspec); fixed4 col; col.rgb = _LightColor0.rgb * ks * specularTerm; col.a = 1; return col; } ENDCG } } }


##### Rim Lighting

![](../../assets/0bc916ef0fbc0644.png)


Shader "Custom/Illustrative Rendering/04.RimLighting" { Properties { _SpecularMask ("Specular Mask", 2D) = "white" {} _RimMask ("Rim Mask", 2D) = "white" {} _RimPower ("Rim Power", Float) = 4 _Krim ("Rim Exponent", Float) = 1 } SubShader { Tags { "RenderType"="Opaque" "LightMode"="ForwardBase" } LOD 100 Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" #include "UnityLightingCommon.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; half3 normal : NORMAL; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; half3 VdotR : TEXCOORD1; half3 VdotN : TEXCOORD2; half3 NdotU : TEXCOORD3; }; sampler2D _SpecularMask; half4 _SpecularMask_ST; sampler2D _RimMask; half4 _RimMask_ST; half _RimPower; half _Krim; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _RimMask); half3 viewDir = normalize(WorldSpaceViewDir(v.vertex)); half3 lightDir = normalize(_WorldSpaceLightPos0.xyz); half3 worldNormal = UnityObjectToWorldNormal(v.normal); half3 reflectDir = reflect(-lightDir, worldNormal); o.VdotR = saturate(dot(viewDir, reflectDir)); o.VdotN = saturate(dot(viewDir, worldNormal)); half3 worldUp = half3(0, 1, 0); o.NdotU = dot(worldNormal, worldUp); return o; } fixed4 frag (v2f i) : SV_Target { half4 ks = tex2D( _SpecularMask, i.uv); half fresnelRim = pow(1 - i.VdotN, _RimPower); half4 kr = tex2D(_RimMask, i.uv); half3 rimTerm = fresnelRim * kr * pow(i.VdotN, _Krim); half3 multiplePhongTerms = rimTerm; half3 dedicatedRimLighting = i.NdotU * fresnelRim * kr; half4 col; col.rgb = multiplePhongTerms + dedicatedRimLighting; col.a = 1; return col; } ENDCG } } }


##### Final Result with Team Fortress 2

![](../../assets/eeb09c8ea39aee1c.png)


![](../../assets/2f737b69aaf4f497.png)


Shader "Custom/Illustrative Rendering/05.Final" { Properties { [Header(Main Map)] _MainTex ("Albedo", 2D) = "white" {} [Header(Warped Diffuce)] _WarpedTex ("Warped Texture", 2D) = "white" {} _WarpedScale ("Warped Scale", Float) = 1 [Header(Specular)] _SpecularMask ("Specular Mask", 2D) = "white" {} _Fspec ("Fresnel Specular Term", Float) = 1 _Kspec ("Specular Exponent Power", Float) = 1 [Header(Rim)] _RimMask ("Rim Mask", 2D) = "white" {} _RimPower ("Rim Power", Float) = 4 _Krim ("Rim Exponent Power", Float) = 1 } SubShader { Tags { "RenderType"="Opaque" "LightMode"="ForwardBase" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" #include "UnityLightingCommon.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; half3 normal : NORMAL; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; half3 NdotL : TEXCOORD1; half3 VdotR : TEXCOORD2; half3 VdotN : TEXCOORD3; half3 NdotU : TEXCOORD4; }; sampler2D _MainTex; half4 _MainTex_ST; sampler2D _WarpedTex; half4 _WarpedTex_ST; half _WarpedScale; sampler2D _SpecularMask; half4 _SpecularMask_ST; half _Fspec; half _Kspec; sampler2D _RimMask; half4 _RimMask_ST; half _RimPower; half _Krim; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); half3 worldNormal = normalize(UnityObjectToWorldNormal(v.normal)); half3 lightDir = normalize(_WorldSpaceLightPos0.xyz); o.NdotL = dot(worldNormal, lightDir); half3 viewDir = normalize(WorldSpaceViewDir(v.vertex)); half3 reflectDir = reflect(-lightDir, worldNormal); o.VdotR = saturate(dot(viewDir, reflectDir)); o.VdotN = saturate(dot(viewDir, worldNormal)); half3 worldUp = half3(0, 1, 0); o.NdotU = dot(worldNormal, worldUp); return o; } fixed4 frag (v2f i) : SV_Target { //View Independent Lighting half4 k = tex2D(_MainTex, i.uv); half halfLambert = pow(0.5 * i.NdotL + 0.5, 2); half2 warpedUV = float2(halfLambert, halfLambert); half3 diffuseWarping = tex2D(_WarpedTex, warpedUV).rgb * _WarpedScale; half3 viewIndependentLight = k * _LightColor0.rgb * diffuseWarping; //View Dependent Lighting //Multiple Phong Terms half4 ks = tex2D( _SpecularMask, i.uv); half3 specularTerm = _Fspec * pow(i.VdotR, _Kspec); half fresnelRim = pow(1 - i.VdotN, _RimPower); half4 kr = tex2D(_RimMask, i.uv); half3 rimTerm = fresnelRim * kr * pow(i.VdotR, _Krim); half3 multiplePhongTerms = _LightColor0.rgb * ks * max(specularTerm, rimTerm); //Dedicated Rim Lighting half3 dedicatedRimLighting = i.NdotU * fresnelRim * kr; half3 viewDependentLight = multiplePhongTerms + dedicatedRimLighting; //Final Result fixed4 finalColor; finalColor.rgb = viewIndependentLight + viewDependentLight; finalColor.a = 1; return finalColor; } ENDCG } } }


##### Final Result with Grayscale Gradient

![](../../assets/56f82d56dbb2f0dd.png)


![](../../assets/376fd893e5ed5aa1.png)



##### Final Result with Horror Style

![](../../assets/c1dcf0b4caf7dd14.png)


![](../../assets/f007a824f93f96c8.png)



#### Github


#### 資料、圖片、資源來源

[Illustrative Rendering in Team Fortress 2](http://www.valvesoftware.com/publications/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf)

[【Shader拓展】Illustrative Rendering in Team Fortress 2](http://blog.csdn.net/candycat1992/article/details/37696187)

[Team Fortress 2 – Wikipedia](https://en.wikipedia.org/wiki/Team_Fortress_2)

[ユニティちゃんトゥーンシェーダー]