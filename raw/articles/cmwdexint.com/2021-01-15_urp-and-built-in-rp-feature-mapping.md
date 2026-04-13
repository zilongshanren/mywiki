---
title: URP and Built-in RP feature mapping
url: https://cmwdexint.com/2021/01/15/urp-and-built-in-rp-feature-mapping/
author: Ming Wai Chan
published: '2021-01-15'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

URP Documentation has this [feature comparison table](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@10.2/manual/universalrp-builtin-feature-comparison.html) ([U6 link](https://docs.unity3d.com/6000.0/Documentation/Manual/render-pipelines-feature-comparison.html)) showing feature parity with Built-in RP,

e.g. telling what is supported and not yet supported.

This blog post shows the comparison in terms of usage.

Based on Unity 2020.2.2f1 + URP 10.2.2

Feature | Built-in RP | Universal RP (URP) |
| Renderer / Object
| Called on Renderer: ■ OnWillRenderObject ■ OnBecameVisible ■ OnBecameInvisible Called on GameObject: ■ OnRenderObject | same as Built-in RP. |
| Camera
| Called on Camera: ■ OnPreCull ■ OnPreRender ■ OnPostRender ■ OnRenderImage | use
■ beginFrameRendering ■ beginCameraRendering ■ endCameraRendering ■ endFrameRendering see below for more callbacks. |

[Rendering Events](https://docs.unity3d.com/2020.2/Documentation/Manual/GraphicsCommandBuffers.html)[CameraEvent](https://docs.unity3d.com/2020.2/Documentation/ScriptReference/Rendering.CameraEvent.html)+ Camera.AddCommandBuffer[LightEvent](https://docs.unity3d.com/2020.2/Documentation/ScriptReference/Rendering.LightEvent.html)+Light.AddCommandBuffer

[RenderPassEvent](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@10.2/api/UnityEngine.Rendering.Universal.RenderPassEvent.html). See[example](https://github.com/Unity-Technologies/Graphics/blob/master/TestProjects/UniversalGraphicsTest/Assets/Test/Runtime/CameraCallbackTests.cs).Add this RendererFeature to a ForwardRendererData asset.

[Documentation](https://docs.unity3d.com/2020.2/Documentation/Manual/ExecutionOrder.html)[here](https://github.com/cinight/URPScriptOrder)checkbox

(Lit)

and all the other legacy / mobile lit shaders

(Unlit)

but recommended to use URP’s own unlit shaders:

Universal Render Pipeline/Unlit shaders

ProjectView > Create > Shader:

■ Standard Surface Shader

■ Unlit Shader

■ Image Effect Shader

ProjectView > Create > Shader:

■ Unlit Shader

■ Image Effect Shader

Create ShaderGraph (node-based shader editor).

ProjectView > Create > Shader > Universal Render Pipeline

Tags { “LightMode” = “ForwardBase” }

Name “FORWARD_DELTA”

Tags { “LightMode” = “ForwardAdd” }

Name “ShadowCaster”

Tags { “LightMode” = “ShadowCaster” }

Name “DEFERRED”

Tags { “LightMode” = “Deferred” }

Name “META”

Tags { “LightMode”=”Meta” }

(from Standard shader)

Tags{“LightMode” = “UniversalForward”}

Name “ShadowCaster”

Tags{“LightMode” = “ShadowCaster”}

Name “GBuffer”

Tags{“LightMode” = “UniversalGBuffer”}

Name “DepthOnly”

Tags{“LightMode” = “DepthOnly”}

Name “DepthNormals”

Tags{“LightMode” = “DepthNormals”}

Name “Meta”

Tags{“LightMode” = “Meta”}

Name “Universal2D”

Tags{ “LightMode” = “Universal2D” }

(from

[URP Lit shader](https://github.com/Unity-Technologies/Graphics/blob/10.x.x/release/com.unity.render-pipelines.universal/Shaders/Lit.shader))_Color

(from Standard shader)

_BaseColor

(from

[URP Lit shader](https://github.com/Unity-Technologies/Graphics/blob/10.x.x/release/com.unity.render-pipelines.universal/Shaders/Lit.shader))[DepthTextureMode](https://docs.unity3d.com/2020.2/Documentation/ScriptReference/DepthTextureMode.html)■_CameraDepthTexture

■_CameraDepthNormalsTexture

■_CameraMotionVectorsTexture

on UniversalRenderPipeline asset

■_CameraDepthTexture

enable Opaque Texture checkbox

on UniversalRenderPipeline asset

■_CameraOpaqueTexture