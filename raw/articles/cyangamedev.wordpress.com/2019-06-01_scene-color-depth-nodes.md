---
title: Scene Color & Depth Nodes
url: https://cyangamedev.wordpress.com/2019/06/01/scene-color-depth-nodes/
author: Cyan
published: '2019-06-01'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

### Scene Color

The **Scene Color** node allows us to sample the current **Camera’s Color buffer** – basically a texture of what the camera sees. However, it’s output varies depending on which **Render Pipeline** you are using. For Custom Render Pipelines, they must define the behaviour for the node in order for it to work. If undefined, it just returns **0** (black).

**LWRP** (Lightweight Render Pipeline) /

**URP** (Universal Render Pipeline) :

- In LWRP/URP returns a value from the
**_CameraOpaqueTexture**– so it won’t include transparent materials. - Use
**Transparent**render mode, otherwise our shader will draw itself to the colour texture. We can also use**Opaque**, but the**Render Queue**on the**Material**must be modified to**2501**or higher. - You will also need to enable the
**Opaque Texture**under the**Lightweight/Universal Render Pipeline Asset**, or change it to**“On”**on the Camera so it actually sets this texture.

**HDRP **(High Definition Render Pipeline) :

- I’m not too familiar with
**HDRP**(High Definition Render Pipeline), but after some research I believe it instead uses**_ColorPyramidTexture(?)**which may have multiple LODs (levels of detail, a.k.a. mip map levels). The node uses LOD 0 (the most detailed one). There is also a**HD Scene Color**node which allows you to access a different LOD. - You may also need to
**Multiply**the output with the**Exposure**node to get the correct result.

The node also has an input for **UVs**. It’s default input is **normalized screen coordinates **(aka the output from a **Screen Position** node) so it samples the same pixel that the camera would see below the transparent material. We can use this to create “*fake” *transparency (as in, it’s still a transparent shader but renders objects that are behind it to itself, rather than using actual transparency). And more importantly, we can offset the screen coordinates passed in to create **distortions** – useful for glass and water shaders.

Note that in the **HDRP** there seems to be a built-in **Distortion** output on the **Master** Node if you configure it to include distortion, so you might not need to use this node. I couldn’t get the node or that distortion to work though – but as I said before, I’m not familiar with that pipeline and was probably doing something wrong.

### Scene Depth

Note : I also have a newer detailed post explaining everything depth-related on my new site, here : [https://www.cyanilux.com/tutorials/depth/](https://www.cyanilux.com/tutorials/depth/)

The **Scene Depth** node allows us to sample the current **Camera’s Depth texture –** basically a texture showing how far objects are from the camera. What it returns may vary depending on which **Render Pipeline** you are using, and Custom Render Pipelines must define the behaviour for the node in order for it to work. If undefined, it returns **1** (white).

**LWRP** (Lightweight Render Pipeline) /

**URP** (Universal Render Pipeline) :

- Use
**Transparent**render mode, otherwise our shader will be writing to the depth buffer and we’ll just be getting back the depth of that object! We can also use**Opaque**, but the**Render Queue**on the**Material**must be modified to**2501**or higher. (If writing code, I believe we just need**ZWRITE**to be off). - For all pipelines, (including Built-In) the depth texture is stored in
**_CameraDepthTexture**. - For the
**LWRP/URP**, You need to enable the**Depth Texture**under the**Lightweight/Universal Render Pipeline Asset**, or change it to**“On”**on the Camera so it actually sets this texture. - Also note, strangely in order for the depth texture to be correctly rendered, the “Post Processing” option on the Camera must be enabled. (Having the Opaque Texture, HDR, or Anti Aliasing MSAA enabled on the pipeline asset also seems to force it to render, but they will have extra overhead). This is true in URP v7.3.1 at least, it’s possible that this is a bug and may be fixed in the future?
- If sampling the depth texture via code. URP provides a
[DeclareDepthTexture.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl)which can be included, then use the**SampleSceneDepth**function. This will give you the raw value, which then can be converted using the**Linear01Depth**or**LinearEyeDepth**functions (see below), with the raw value and**_ZBufferParams**as inputs.

**HDRP **(High Definition Render Pipeline) :

- Use
**Transparent**render mode, otherwise our shader will be writing to the depth buffer and we’ll just be getting back the depth of that object! (If writing code, I believe we just need**ZWRITE**to be off). - The depth texture is stored in
**_CameraDepthTexture**. - According to
[this thread](https://forum.unity.com/threads/camera-depth-texture-sampling-with-2018-3-and-hdrp-4-x-mip-map-issue.594160/), it contains multiple mip map levels, so use the**SampleCameraDepth**functions inside*ShaderVariables.hlsl*if writing code. The Shader graph**Scene Depth**node should already take this into account and correctly sample the texture.

Note that it also has multiple modes for sampling depth :

**Raw**will return the raw depth value, straight from the texture. This value is between**0**and**1**, reaching from the**near clip plane**to the**far clip plane**. When using a**Perspective**camera projection, this value is**not linear**however, a value of**0.5**for example is not halfway between them. Depending on the hardware the depth buffer might also be**reversed**so that a raw value of**0**is actually at the**far clip plane**and**1**is the**near clip plane**. I believe all this helps with precision but[this NVIDIA post](https://developer.nvidia.com/content/depth-precision-visualized)explains it a lot better than I can, (of course you don’t necessarily need to know this in order to use the node though).**Linear01**will returns the linear depth value, still between**0**and**1**. This converts the raw value using the**Linear01Depth**function, so that**0.5**is now halfway between the far and near clip planes. (Note : Should only be used with a Perspective camera).**Eye**will also convert the depth value to linear, but in eye space units, using the**LinearEyeDepth**function. A value of**0**is exactly at the camera’s position,**1**is**1**unit away from the camera,**10**is**10**units away, etc. (Note : Should only be used with a Perspective camera).

When using an **Orthographic** projection, the depth is actually already **linear**, so the **Raw** mode should be used. [This twitter thread](https://twitter.com/Cyanilux/status/1169932943869059073) provides some more information.

If interested, the **Linear01Depth** and **LinearEyeDepth** functions are defined as:

// Z buffer to linear 0..1 depth (0 at camera position, 1 at far plane). // Does NOT work with orthographic projections. // Does NOT correctly handle oblique view frustums. // zBufferParam = { (f-n)/n, 1, (f-n)/n*f, 1/f } float Linear01Depth(float depth, float4 zBufferParam) { return 1.0 / (zBufferParam.x * depth + zBufferParam.y); } // Z buffer to linear depth. // Does NOT correctly handle oblique view frustums. // Does NOT work with orthographic projection. // zBufferParam = { (f-n)/n, 1, (f-n)/n*f, 1/f } float LinearEyeDepth(float depth, float4 zBufferParam) { return 1.0 / (zBufferParam.z * depth + zBufferParam.w); } // #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl" to use these functions! (which will be automatically included with universal/ShaderLibrary/Core.hlsl)

The values of zBufferParams are also commented above, but they also vary depending on if the depth buffer is reversed or not.

// Values used to linearize the Z buffer // x = 1-far/near // y = far/near // z = x/far // w = y/far // or in case of a reversed depth buffer (UNITY_REVERSED_Z is 1) // x = -1+far/near // y = 1 // z = x/far // w = 1/far float4 _ZBufferParams;

Similar to the **Scene Color**, the** Scene Depth** node also has a **UV** input. It’s default input is **normalized screen coordinates** (aka the output from a **Screen Position** node) so it samples the same pixel that the camera would see below the transparent material.

By using the **W/A** component from the **Screen Position** set to **Raw**, we can obtain the depth to the surface of the model the shader is applied to, which can allow us to do effects such as fog planes and water shorelines.

For some examples of using the **Scene Depth** node see these posts (many of these share the same “depth intersection” technique) :

[Fog Plane Shader Breakdown](https://cyangamedev.wordpress.com/2019/12/05/fog-plane-shader-breakdown/)[Water Shader Breakdown](https://cyangamedev.wordpress.com/2019/06/10/water-shader-breakdown/)[Forcefield Shader Breakdown](https://cyangamedev.wordpress.com/2019/09/04/forcefield-shader-breakdown/)(Also uses**Scene Color**)[Forcefield Shader Breakdown (Simple)](https://cyangamedev.wordpress.com/2019/09/04/forcefield-shader-breakdown-simple/)[Cloud Shader Breakdown](https://cyangamedev.wordpress.com/2019/09/25/cloud-shader-breakdown/)

**Sources / Related Links :**

[https://docs.unity3d.com/Packages/com.unity.shadergraph@6.7/manual/Scene-Color-Node.html](https://docs.unity3d.com/Packages/com.unity.shadergraph@6.7/manual/Scene-Color-Node.html)[https://docs.unity3d.com/Packages/com.unity.shadergraph@6.7/manual/Scene-Depth-Node.html](https://docs.unity3d.com/Packages/com.unity.shadergraph@6.7/manual/Scene-Depth-Node.html)[https://docs.unity3d.com/Manual/SL-CameraDepthTexture.html](https://docs.unity3d.com/Manual/SL-CameraDepthTexture.html)[https://docs.unity3d.com/Manual/SL-DepthTextures.html](https://docs.unity3d.com/Manual/SL-DepthTextures.html)[https://forum.unity.com/threads/decodedepthnormal-linear01depth-lineareyedepth-explanations.608452/#post-4070806](https://forum.unity.com/threads/decodedepthnormal-linear01depth-lineareyedepth-explanations.608452/#post-4070806)[https://developer.nvidia.com/content/depth-precision-visualized](https://developer.nvidia.com/content/depth-precision-visualized)