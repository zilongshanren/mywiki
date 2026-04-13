---
title: Using Unity as an FX Composer replacement for shader prototyping
url: https://interplayoflight.wordpress.com/2013/02/04/unity-as-an-fx-composer-replacement-for-shader-prototyping/
author: Kostas Anagnostou
published: '2013-02-04'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A few days ago, while preparing a presentation on physically based rendering, I needed to create a few shaders to showcase the difference between the various reflectance models. As always I fired up my aging FX composer and tried to load a Stanford Dragon model I found on the internet (various formats and polygon counts). FX Composer consistently failed to cooperate. Then, I remembered Unity and its very capable content pipeline so I thought I’d give it a go. And voila I got my model rendering with two drag-n-drops.

This got me thinking about how good the free version of Unity would be as an FX composer replacement. I am aware that Unity is a game engine and not specifically tuned for material/shader creation, but it has many good features like the price (can’t get a better deal than free), content pipeline, scene editor, material inspector UI and a shader editor that could make it a prime candidate. I’ve been using FX Composer to prototype/try shaders for quite some time now, but it is starting to show its age with its D3D10 support and, frankly, not so slick UI and Editor/Scene Viewer. So I set about investigating it.

Unity has a custom, although not that much different, material format and does not support fx files, which might be an issue for art pipelines/engines that are based on this file format for material creation.

Shader "Custom/BlinnBRDFShader" { Properties { } SubShader { Pass { Name "PassName" Blend SrcAlpha OneMinusSrcAlpha CGPROGRAM #pragma vertex vert #pragma fragment frag #pragma target 3.0 #include "UnityCG.cginc" struct v2f { float4 pos : SV_POSITION; }; v2f vert (appdata_base v) { v2f o; o.pos = mul (UNITY_MATRIX_MVP, v.vertex); return o; } half4 frag (v2f i) : COLOR { return float4(1,0,0,0.5); } ENDCG } } Fallback "VertexLit" }

Unity’s material property definition is different to fx as well, using a “Properties” block. Also, unlike FXComposer, in Unity properties defined in the “Properties” section must be declared for access in the shader code (for example a Range property must be bound to a float variable) as well.

Properties { SpecularColour ("Specular Colour", Color) = (1.0, 0.71, 0.29, 1) DiffuseColour ("Diffuse Colour", Color) = (0.0, 0.0, 0.0, 1) Roughness ("Roughness", Range (0.0,100)) = 20 Exposure ("Exposure", Range (0.0,2)) = 0.1 LightIntensity ("Light Intensity", Range (1,50)) = 15 NoiseTexture ("Texture", 2D) = "white" { } Cube ("Reflection Map", Cube) = "" {} }

It does support Cg though for shader coding, which is as close to HLSL as you can get, and GLSL. It also supports Hull and Domain Shaders introduced in Shader Model 5 (D3D11), so you can actually perform tessellation, something not possible in FX composer.

Like FX Composer, all properties defined in the Unity shader file are exposed to the material Inspector UI. Both applications support colour pickers for colour selection and sliders which make property tweaking easier. For some reason Unity material sliders do not seem to display the current slider value.

Both applications provide shaders with state data such as common transforms, time as well as camera positions, light positions, colours etc for correct lighting and shading.

Also both support shader passes, to create multipass effects. Unity does not have the notion of a Technique, but it uses the SubShader semantic which is similar. Like a Technique, a subshader supports a number of passes each with its own device state setting commands (Alpha Blending, Culling modes etc). A main difference is that you can’t define shader functions outside a pass (so you can’t reuse a vertex shader for example between passes). You can use include files to store common functionality though. Finally, Unity (free) does not support render to texture so it is not possible to create multipass effects that require this functionality. In overall, FX composer’s technique/pass support in conjunction to its render-to-texture functionality allows for more complex multi-pass effects than the free version of Unity.

On to shader creation and editing, FX composer has shader templates for common shaders (such as blinn, phong with normal mapping) which I imagine some people may find useful. Unity by default creates a simple surface shader.

FX composer has a built-in shader editor with syntactic highlighting, while Unity uses Monodevelop for shader development (with syntactic highlighting as well) which is an external application. It is strange though that with FX composer you have to compile the shader to see it applied to the model, while with Unity you just have to save it and it will compile it automatically. A word of caution, at first the compiler errors might throw you off since they seem mostly irrelevant to the cause of error. You have to carefully go through the error list and locate what actually is wrong with your code.

In general the FX composer environment appears more “visual” with more icons on the buttons and preview icons; it seems more suited to people accustomed to working with Maya and similar editors. The latest Unity version supports preview thumbnails for its assets so by separating them into appropriate folders you can emulate FX Composer’s Material and Texture library look fairly well though.

Both programs support an adequate variety of model/texture formats, although Unity’s content pipeline seems more robust. Both programs have also support for basic polygon shapes such as cubes, planes and spheres for easy shader testing.

Something I liked in Unity is the easy way it allows to create cubemaps, you just create a Cubemap node and drop 6 textures on it, much easier than storing the cubemap in dds files.

In general, Unity’s scene editor is superb and much easier to use, to navigate the camera, to transform objects/lights. Also Unity feels more “drag n drop”, to import assets, set textures and other properties.

And now the verdict. Putting fx materials and complex multipass effects concerns aside, Unity is well suited to graphics programmers and technical artists who wouldn’t mind spending an hour learning the custom material format ([there is documentation](http://docs.unity3d.com/Documentation/Components/SL-Reference.html) on the custom material features on Unity’s web site as well as lots of help on the internet if needed). On the other hand FX composer would probably look easier and more familiar to artists.

If Unity-FXComposer/Maya material sharing is an issue then one potential solution (apart from writing your own parser to convert from one file format to another) would be to have some of your shader functions in headers files to reuse as much as possible, and use the materials to set up the UI in each application.

I, personally, am convinced and will switch to Unity for shader prototyping (I already have really).

PS: To get you started here is the material for the above dragon rendering, it implements a normalised BlinnPhong with Fresnel. To use it, create a new Material in Unity and assign it as a shader. This material contains a second pass as well, for demo purposes, which currently does nothing. Change the output alpha to 0.5 to see it working.

Shader "Custom/BlinnBRDFShader" { Properties { SpecularColour ("Specular Colour", Color) = (1.0, 0.71, 0.29, 1) DiffuseColour ("Diffuse Colour", Color) = (0.0, 0.0, 0.0, 1) SpecularPower ("Specular Power", Range (0.0,100)) = 20 Exposure ("Exposure", Range (0.0,2)) = 0.1 LightIntensity ("Light Intensity", Range (1,50)) = 15 } SubShader { Pass { Name "FirstPass" Blend Off Lighting On CGPROGRAM #pragma vertex vert #pragma fragment frag #pragma target 3.0 #include "UnityCG.cginc" struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; float3 normal : TEXCOORD1; float4 worldPos : TEXCOORD2; }; //declare the properties here for shader code access float SpecularPower; float4 DiffuseColour; float4 SpecularColour; float Exposure; float LightIntensity; float3 HDR(float3 L) { L = L * Exposure; L.r = L.r < 1.413 ? pow(L.r * 0.38317, 1.0 / 2.2) : 1.0 - exp(-L.r); L.g = L.g < 1.413 ? pow(L.g * 0.38317, 1.0 / 2.2) : 1.0 - exp(-L.g); L.b = L.b < 1.413 ? pow(L.b * 0.38317, 1.0 / 2.2) : 1.0 - exp(-L.b); return L; } v2f vert (appdata_base v) { v2f o; o.pos = mul (UNITY_MATRIX_MVP, v.vertex); o.worldPos = mul(_Object2World, v.vertex); o.normal = mul((float3x3)_Object2World, v.normal); return o; } half4 frag (v2f i) : COLOR { //calculate some useful vectors float3 L = normalize( _WorldSpaceLightPos0.xyz ); float3 V = normalize(_WorldSpaceCameraPos.xyz-i.worldPos.xyz); float3 N = normalize(i.normal); float3 H = normalize(L + V); float3 R = reflect(-V, N); float NdotH = saturate(dot(N,H)); float LdotH = dot(L,H); float NdotL = saturate(dot(N,L)); float NdotV = saturate(dot(N,V)); //calculate fresnel float3 fresnel = SpecularColour.rgb+ (1-SpecularColour.rgb) * pow( 1-LdotH , 5); //calc resulting colour float3 result = (DiffuseColour.rgb + fresnel * pow(NdotH, SpecularPower) * (SpecularPower+4)/8) * LightIntensity * NdotL; return half4(HDR(result), 1); } ENDCG } Pass { Name "SecondPass" Blend SrcAlpha OneMinusSrcAlpha CGPROGRAM #pragma vertex vert #pragma fragment frag #pragma target 3.0 #include "UnityCG.cginc" struct v2f { float4 pos : SV_POSITION; }; v2f vert (appdata_base v) { v2f o; o.pos = mul (UNITY_MATRIX_MVP, v.vertex); return o; } half4 frag (v2f i) : COLOR { return float4(1,0,0,0.0); } ENDCG } } Fallback "VertexLit" }

[…] Here's a nice blog post comparing NVIDIA's FX Composer to Unity when it comes to quick shader prototyping. […]

If you want to view the current slider value (and you want the slider as well), just duplicate the property and replace “range” with ” float”. You can use vector as well instead of color.

[…] time ago I did an investigation on how/if Unity can be used as a FX Composer replacement, using the free version as a test. I then concluded that to a large degree Unity could be used for […]