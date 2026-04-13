---
title: Unity Material Property Drawer – 客製化材質編輯器
url: https://tedsieblog.wordpress.com/2017/03/02/unity-material-property-drawer/
author: Ted Sie
published: '2017-03-02'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

材質球 [Material](https://docs.unity3d.com/ScriptReference/Material.html)，是在 Unity 中調整畫面呈現的一個必備元素，透過材質球可以相當輕易的達到可見即所得的效果。

在 Unity 環境下撰寫 [Shader](https://docs.unity3d.com/Manual/SL-Reference.html) 後，會透過材質球選取我們所完成的 Shader 並且在 [Inspector](https://unity3d.com/learn/tutorials/topics/interface-essentials/inspector) 中顯示可調整的參數，但是這些參數往往無法滿足我們的需求，這時候就會針對特定需求來進行調整。


![customizedmaterialeditor_01](../../assets/a28d57b21e8bbec1.png)


Shader "Custom/Normal" { Properties { _Int("Int", Int) = 1 _Range("Range", Range(0, 1)) = 1 _Color("Color", Color) = (1, 1, 1, 1) _Vector("Vector", Vector) = (1, 1, 1, 1) _Cube("Cube", Cube) = "white" {} _2D("2D", 2D) = "white" {} _3D("3D", 3D) = "white" {} } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _Color; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { return _Color; } ENDCG } } }


在製作客製化材質編輯器時只要有兩種做法，[MaterialEditor](https://docs.unity3d.com/ScriptReference/MaterialEditor.html) 以及 [MaterialPropertyDrawer](https://docs.unity3d.com/ScriptReference/MaterialPropertyDrawer.html)。


#### MaterialEditor

與一般我們在撰寫客製化腳本編輯器是一樣的概念，透過重新複寫材質球腳本來提高便利性，可以編寫出功能最完善且最符合需求的材質編輯器，但相對較為複雜且無法很方便地重複利用，Unity 中預設的 Standard 既是透過這種方式來客製化編輯器，若有興趣也可以直接在官方 Built in shaders 裡找到 StandardShaderGUI.cs。

![customizedmaterialeditor_standard](../../assets/11b0b566f2032425.png)


#### MaterialPropertyDrawer

為 Unity ShaderLab 中的一種擴充語法（Syntax），用法相當的輕便且容易上手，可以透過這種語法方便的進行材質編輯器的擴充，也是這次要探討的主題。在 MaterialPropertyDrawer 中，Unity 提供了以下幾種擴充語法 **Header**、**Space**、**Toggle**、**Enum**、**KeywordEnum**、**PowerSlider** 以及 **IntRange**，下面就來依次說明。

PS: 本次的環境為 Unity 5.5.0f3，所有說明皆為用法範例，並無特殊功能。


#### Header

與 [HeaderAttribute](https://docs.unity3d.com/ScriptReference/HeaderAttribute.html) 一樣，透過包裝宣告參數，來達到編排版面的作用。

![customizedmaterialeditor_header](../../assets/5737b881eaabc217.png)


Shader "Custom/Header" { Properties { [Header(This is the first Header)] _FirstColor("First Color", Color) = (1, 1, 1, 1) [Header(This is the second Header)] _SecondColor("Second Color", Color) = (1, 1, 1, 1) } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _FirstColor; float4 _SecondColor; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = _FirstColor + _SecondColor; return col; } ENDCG } } }


#### Space

與 [SpaceAttribute](https://docs.unity3d.com/ScriptReference/SpaceAttribute.html) 一樣，在兩參數之間安插任意垂直空間，來達到編排版面的作用。

![customizedmaterialeditor_space](../../assets/b79509440db339f7.png)


Shader "Custom/Space" { Properties { [Header(This is the first Header)] _FirstColor("First Color", Color) = (1, 1, 1, 1) [Space] [Header(This is the second Header)] _SecondColor("Second Color", Color) = (1, 1, 1, 1) [Space(50)] [Header(This is the third Header)] _ThirdColor("Third Color", Color) = (1, 1, 1, 1) } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _FirstColor; float4 _SecondColor; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = _FirstColor + _SecondColor; return col; } ENDCG } } }


#### Toggle

以觸發器型態表示浮點數，可以用來處理開關變換的過程，需要注意的是，在宣告參數 _Invert 後，必須額外使用 #pragma shader_feature 定義 _INVERT_ON（大寫參數名 + _ON）來作為配套使用，這邊就用簡單的負片效果當作示範。

![customizedmaterialeditor_toggle](../../assets/a81c6471af9e52ca.png)


Shader "Custom/Toggle" { Properties { _Color ("Color", Color) = (1, 1, 1, 1) [Toggle] _Invert("Invert?", Float) = 0 } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma shader_feature _INVERT_ON #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _Color; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = _Color; #if _INVERT_ON col = 1 - col; #endif return col; } ENDCG } } }


#### Enum

Enum 是一般在撰寫 Scripts 時常常見到的功能，而在 ShaderLab 中也一樣支援了這個語法，這邊使用切換 Culling Mode 來當作範例。透過這種切換方式，就能夠單純地利用 Material 的生成，來切換各種不同型態的 Culling Mode.

![customizedmaterialeditor_enum](../../assets/68d836d8b1d89843.png)


Shader "Custom/Enum" { Properties { _Color("Color", Color) = (1, 1, 1, 1) [Enum(UnityEngine.Rendering.CullMode)] _CullMode ("Cull Mode", Float) = 0 } SubShader { Tags { "RenderType"="Opaque" } Pass { Cull [_CullMode] CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _Color; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = _Color; return col; } ENDCG } } }


#### KeywordEnum

與 Enum 相似，可以自定義枚舉名稱，需要注意在參數宣告後，需與 #pragma multi_compile 配套使用（大寫參數名 + 大寫枚舉名）。

![customizedmaterialeditor_keywordenum](../../assets/b45fab1a24dc4231.png)


Shader "Custom/KeywordEnum" { Properties { [KeywordEnum(Red, Green, Blue)] _ColorMode ("Color Mode", Float) = 0 } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma multi_compile _COLORMODE_RED _COLORMODE_GREEN _COLORMODE_BLUE #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = fixed4(0, 0, 0, 1); #if _COLORMODE_RED col.r = 1; #elif _COLORMODE_GREEN col.g = 1; #elif _COLORMODE_BLUE col.b = 1; #endif return col; } ENDCG } } }


#### PowerSlider

使用上與原始的 Range(min, max) 大同小異，唯一的差別是滑動條上的數值不再是線性變化。

![customizedmaterialeditor_powerslider](../../assets/fbb9c175b40eb212.png)


Shader "Custom/PowerSlider" { Properties { [PowerSlider(3.0)] _Shininess ("Shininess", Range (0.01, 1)) = 0.08 } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _Color; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = _Color; return col; } ENDCG } } }


#### IntRange

使用上與原始的 Range(min, max) 大同小異，唯一的差別是滑動條上的數值為整數變化。

![customizedmaterialeditor_intrange](../../assets/c7ad5572b6924add.png)


Shader "Custom/IntRange" { Properties { [IntRange] _Alpha ("Alpha", Range (0, 255)) = 100 } SubShader { Tags { "RenderType"="Opaque" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _Color; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = _Color; return col; } ENDCG } } }


#### 結語

透過 MaterialPropertyDrawer 雖然可以相當簡單的製作出屬於自己的材質編輯器，但製作簡單也就意味著擴充性的不足，單獨依靠 MaterialPropertyDrawer 依然沒有辦法擁有完整的控制權，若是需求特殊時，仍然必須使用 MaterialEditor 來作為首要選擇。但在無特別開發需求的狀況下，仍然可以透過 MaterialPropertyDrawer 來節省大量開發時間

![customizedmaterialeditor_final](../../assets/0e27b6830eae1df9.png)


Shader "Custom/Customize" { Properties { [Header(Toggle)] [Toggle] _Invert("Invert?", Float) = 0 [Toggle(ENABLE_FANCY)] _Fancy ("Fancy?", Float) = 0 [Header(KeywordEnum)] [KeywordEnum(None, Add, Multiply)] _Overlay ("Overlay mode", Float) = 0 [Space] [Header(PowerSlider)] [PowerSlider(3.0)] _Shininess ("Shininess", Range (0.01, 1)) = 0.08 [Space] [Header(IntRange)] [IntRange] _Alpha ("Alpha", Range (0, 255)) = 100 [Header(Cull)] [Enum(UnityEngine.Rendering.CullMode)] _CullMode ("Cull Mode", Float) = 0 [Space] [Header(Blend)] [Enum(UnityEngine.Rendering.BlendMode)] _BlendSrcFactor ("Blend SrcFactor", Float) = 0 [Enum(UnityEngine.Rendering.BlendMode)] _BlendDstFactor ("Blend DstFactor", Float) = 0 [Header(Stencil)] [IntRange] _StencilRef ("Stencil Reference", Range(0, 255)) = 0 [Enum(CompareFunction)] _StencilComp ("Stencil Compare Function", Float) = 0 [Enum(UnityEngine.Rendering.StencilOp)] _StencilOp ("Stencil Operation", Float) = 0 } SubShader { Tags { "RenderType"="Opaque" } Stencil { Ref [_StencilRef] Comp [_StencilComp] Pass [_StencilOp] } Pass { Cull [_CullMode] Blend [_BlendSrcFactor] [_BlendDstFactor] CGPROGRAM #pragma shader_feature _INVERT_ON #pragma shader_feature ENABLE_FANCY #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 vertex : SV_POSITION; }; float4 _Color; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = _Color; #if _INVERT_ON col = 1 - col; #endif #if ENABLE_FANCY col.r = 0.5; #endif return col; } ENDCG } } }


#### GitHub

#### 參考資料

[Unity – Scripting API: MaterialEditor](https://docs.unity3d.com/ScriptReference/MaterialEditor.html)

[Unity – Scripting API: MaterialPropertyDrawer](https://docs.unity3d.com/ScriptReference/MaterialPropertyDrawer.html)

Unity – Script API: UnityEngine.Rendering.Enumerations

[【Unity Shader】自定义材质面板的小技巧](http://blog.csdn.net/candycat1992/article/details/51417965)