---
title: Post Processing in the Universal RP
url: https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/
author: Cyan
published: '2020-06-22'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

The **Universal Render Pipeline** (URP, previously known as Lightweight RP) uses an integrated **Volume **system for Post Processing effects, sometimes referred to as Post Processing V3 / PPv3. These effects include things like Bloom, Chromatic Aberration, Depth of Field, Color Adjustments, Tonemapping, Vignette, etc. Note that URP does not have Ambient Occlusion yet, it’s on the [roadmap](https://portal.productboard.com/8ufdwj59ehtmsvxenjumxo82/tabs/3-universal-render-pipeline-previously-lwrp), but you may also be able to find solutions on the asset store.

![](../../assets/0c76c6aa49e07187.png)

##### Sections :

## PPv2

The “**Post Processing**” package listed in the Package Manager, also known as the **Post Processing Stack V2** (PPv2), is intended for use with the built-in pipeline. Some versions of URP that are supported by Unity 2019.4 LTS (around URP v7.2 to v7.4?) support PPv2, however newer versions from v8.0 onwards will not, so using the integrated Volume system is recommended.

If you are upgrading an existing project, there is currently no easy way to convert from PPv2 to PPv3 as far as I’m aware, it has to be done manually. If you still want to use PPv2 instead, there should be an option on the **URP Asset** to switch the Post Processing “**Feature Set**” from the integrated solution to “**Post Processing V2**”.

![](../../assets/d0d3358d2ef39f6c.png)

This option will only show when the package is installed, and of course you need to be using a LWRP/URP version that supports PPv2 (Unity 2019.4 LTS, v7.2 to v7.4? I’ve tested with Unity 2019.3.3f1 and URP v7.3.1).

With this set, you can then continue using the **Post-Process Layer** and **Post-Process Volume** components on objects, see [here](https://docs.unity3d.com/Packages/com.unity.postprocessing@2.3/manual/Quick-start.html) for more information on using PPv2. Note that certain features might not be supported (Ambient Occlusion, Temporal Anti-aliasing and Motion Blur).

You’ll also want to make sure **Post Processing** is enabled on the Camera, in order to see the effects in the game view! You can also find screen-space Anti-aliasing here.

![](../../assets/b7c90d540425eb79.png)

## Integrated / PPv3

To use integrated [Post Processing](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@8.0/manual/integration-with-post-processing.html) solution in URP, you can add the “**Volume**” component to a **GameObject**, or right-click in the Hierarchy and select something under the **Volume** heading.

![](../../assets/ba035a3b8c59616d.png)

A volume can be set as **Global**, where it affects the entire scene or **Local**, where it will also require a **Collider** (preferably with **IsTrigger** enabled) to be added. With local, the effects will only appear when the camera is inside the volume/collider. You can use the **Blend Distance** to create a smooth transition.

There’s also a **Weight** setting, which is how much the post processing effects contribute, with **0** being not at all, and **1** being fully. If you have multiple volumes overlapping or volumes inside other volumes, you will also want to use the **Priority** setting. The higher the value, the higher the priority.

Each Volume has a **Profile** which holds the Post-processing effects. Multiple volumes can share the same profile. Click the New button to create a profile, then use the **Add Override** button to add effects to the list. For a list & info about each effect, see [here](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@9.0/manual/EffectList.html).

![](../../assets/9088fe25efd4d6f9.png)

Each setting has a default value and will be greyed out. To edit a setting click the checkbox on the left side to override the value.

Now that there’s a volume in the scene, You’ll want to click on the **Camera** and make sure **Post Processing** is enabled, in order to see the effects in the game view. You can also find screen-space Anti-aliasing here.

![](../../assets/b7c90d540425eb79.png)

The camera also has **Volume Mask** and **Volume Trigger** settings under the **Environment** heading. The mask includes which layers will affect the camera – any volumes on layers not included in that list will not affect the camera. The trigger setting is which transform that is used to test against local volumes. If left blank, the camera’s transform is used.

![](../../assets/1f38eb4d321ac02e.png)

## Custom Effects

Currently the integrated volume system does not support custom effects, but it is on the [roadmap](https://portal.productboard.com/8ufdwj59ehtmsvxenjumxo82/c/37-post-processing-custom-effects). We can instead apply global post processing shader effects using a custom **Renderer Feature**, applied to the **Forward Renderer**.

![](../../assets/56ba5d05ed7b488b.png)

The feature uses a **Blit**, which copies the contents of a texture to a render texture, using a custom shader to apply the effect. The code for this feature is at the end of the post.

The shader should include a **Texture2D property** with the reference “**_MainTex**“, in order to obtain the input from the blit. We can then make adjustments to the image, e.g. inverting the colours via a **One Minus** node, and pass that into the **Color** input on the **Master** node.

The **Master** node should be Unlit, as this is all done in screen space where having PBR lighting would not make sense.

![](../../assets/3a0b2636c2dc672e.png)

Note that shadergraph produces **multiple passes** which shouldn’t be used for the blit. The renderer feature included a **Blit Material Pass Index **where we can specify which pass should be used. If set to **-1**, all passes will be rendered (including the shadow caster which causes a large black rectangle to appear when in Opaque surface mode), setting it to **0** will use the first pass only.

Below is the full code for a feature that handles this, based on the example [here](https://github.com/Unity-Technologies/UniversalRenderingExamples/tree/master/Assets/Scripts/Runtime/RenderPasses). You don’t really have to understand what it does in order to use it. Just have it somewhere in your Assets, and it will be available to the **Forward Renderer** features list.

Note : The code below is written for Unity 2019/2020. For newer versions, see [this repo](https://github.com/Cyanilux/URP_BlitRenderFeature). Unity 2022 now also has a Fullscreen Graph and Fullscreen Pass Renderer Feature built-in.

Also if you want to be able to enable/disable a renderer feature at runtime, you can obtain a public reference to it to achieve that. See an example [here](https://twitter.com/Cyanilux/status/1275060844355702789).

```
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
// Saved in Blit.cs
public class Blit : ScriptableRendererFeature {
public class BlitPass : ScriptableRenderPass {
public enum RenderTarget {
Color,
RenderTexture,
}
public Material blitMaterial = null;
public int blitShaderPassIndex = 0;
public FilterMode filterMode { get; set; }
private RenderTargetIdentifier source { get; set; }
private RenderTargetHandle destination { get; set; }
RenderTargetHandle m_TemporaryColorTexture;
string m_ProfilerTag;
public BlitPass(RenderPassEvent renderPassEvent, Material blitMaterial, int blitShaderPassIndex, string tag) {
this.renderPassEvent = renderPassEvent;
this.blitMaterial = blitMaterial;
this.blitShaderPassIndex = blitShaderPassIndex;
m_ProfilerTag = tag;
m_TemporaryColorTexture.Init("_TemporaryColorTexture");
}
public void Setup(RenderTargetIdentifier source, RenderTargetHandle destination) {
this.source = source;
this.destination = destination;
}
public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData) {
CommandBuffer cmd = CommandBufferPool.Get(m_ProfilerTag);
RenderTextureDescriptor opaqueDesc = renderingData.cameraData.cameraTargetDescriptor;
opaqueDesc.depthBufferBits = 0;
// Can't read and write to same color target, use a TemporaryRT
if (destination == RenderTargetHandle.CameraTarget) {
cmd.GetTemporaryRT(m_TemporaryColorTexture.id, opaqueDesc, filterMode);
Blit(cmd, source, m_TemporaryColorTexture.Identifier(), blitMaterial, blitShaderPassIndex);
Blit(cmd, m_TemporaryColorTexture.Identifier(), source);
} else {
Blit(cmd, source, destination.Identifier(), blitMaterial, blitShaderPassIndex);
}
context.ExecuteCommandBuffer(cmd);
CommandBufferPool.Release(cmd);
}
public override void FrameCleanup(CommandBuffer cmd) {
if (destination == RenderTargetHandle.CameraTarget)
cmd.ReleaseTemporaryRT(m_TemporaryColorTexture.id);
}
}
[System.Serializable]
public class BlitSettings {
public RenderPassEvent Event = RenderPassEvent.AfterRenderingOpaques;
public Material blitMaterial = null;
public int blitMaterialPassIndex = -1;
public Target destination = Target.Color;
public string textureId = "_BlitPassTexture";
}
public enum Target {
Color,
Texture
}
public BlitSettings settings = new BlitSettings();
RenderTargetHandle m_RenderTextureHandle;
BlitPass blitPass;
public override void Create() {
var passIndex = settings.blitMaterial != null ? settings.blitMaterial.passCount - 1 : 1;
settings.blitMaterialPassIndex = Mathf.Clamp(settings.blitMaterialPassIndex, -1, passIndex);
blitPass = new BlitPass(settings.Event, settings.blitMaterial, settings.blitMaterialPassIndex, name);
m_RenderTextureHandle.Init(settings.textureId);
}
public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData) {
var src = renderer.cameraColorTarget;
var dest = (settings.destination == Target.Color) ? RenderTargetHandle.CameraTarget : m_RenderTextureHandle;
if (settings.blitMaterial == null) {
Debug.LogWarningFormat("Missing Blit Material. {0} blit pass will not execute. Check for missing reference in the assigned renderer.", GetType().Name);
return;
}
blitPass.Setup(src, dest);
renderer.EnqueuePass(blitPass);
}
}
```

For more examples, there’s a good example of an [Outline Shader here](https://alexanderameye.github.io/outlineshader.html), by Alexander Ameye. It produces a similar effect to the image at the top of this post and is made using two renderer features. The first feature is used to redraw the scene with an overrideMaterial to capture the normals of objects in the scene in a texture, which is then used in the outline shader (as well as the depth texture). That shader is then blitted to the screen using a similar render feature to the above Blit feature.

The [UniversalRenderingExamples here](https://github.com/Unity-Technologies/UniversalRenderingExamples) also provide some examples of using render features for a few effects.