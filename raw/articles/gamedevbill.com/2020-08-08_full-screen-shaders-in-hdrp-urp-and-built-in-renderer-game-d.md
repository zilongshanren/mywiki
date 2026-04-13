---
title: Full Screen Shaders in HDRP, URP, and Built In Renderer - Game Dev Bill
url: https://gamedevbill.com/full-screen-shaders-in-unity/
author: Bill
published: '2020-08-08'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![Full Screen Shaders in Unity title image](../../assets/f07cdbc1d5ddb991.png)

Full screen shaders, also referred to as *custom post processing effects*, are a critical tool in the arsenal of most game makers. In Unity, utilizing full screen shaders is dependent on which of the three rendering setups you are using. Full screen shaders in the built in renderer are most straightforward. Full screen shaders in HDRP come in a close second. Then in a distant third, full screen shaders in URP.

All three techniques are covered relatively well across the internet, just not all in one place. So I decided to bring it all together here, and only have one place I needed to reference.

Please ping me on [Twitter](https://twitter.com/gamedevbill) or [comment on the forum](https://forum.unity.com/threads/gamedevbill-tutorial-comment-thread.945515/) if anything isn’t working for you. And if it is working I would always appreciate, [a follow on Twitter](https://twitter.com/gamedevbill), a download of [my free shader graph node](https://assetstore.unity.com/packages/vfx/shaders/cartesian-coordinate-shader-graph-node-158568?aid=1011l3QFn), or a purchase of a [recommended ](https://assetstore.unity.com/packages/3d/vegetation/the-illustrated-nature-153939?aid=1011l3QFn)[asset](https://assetstore.unity.com/packages/vfx/shaders/nodes-for-shader-graph-124611?aid=1011l3QFn).

*This article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

## Full Screen Shaders in the Built In Renderer

We’ll start with the simplest. As I already covered in [my previous overview of shaders in Unity](https://gamedevbill.com/shader-series-3-shaders-in-unity/), using full screen shaders here requires you to add a component to your camera ([github](https://github.com/gamedevbill/ShaderBaseline/blob/master/ShaderBaseline/Assets/Scripts/AwesomeScreenShader.cs)).

public class AwesomeScreenShader : MonoBehaviour { public Shader awesomeShader = null; private Material m_renderMaterial; void Start() { if (awesomeShader == null) { Debug.LogError("no awesome shader."); m_renderMaterial = null; return; } m_renderMaterial = new Material(awesomeShader); } void OnRenderImage(RenderTexture source, RenderTexture destination) { Graphics.Blit(source, destination, m_renderMaterial); } }

The only input to this code is the shader file. Being the built-in renderer, shader graph isn’t an option. So you’ll need to [write the code](https://gamedevbill.com/shader-series/) yourself or [get Amplify Shader Editor from the asset store](https://assetstore.unity.com/packages/tools/visual-scripting/amplify-shader-editor-68570?aid=1011l3QFn).

![](../../assets/47564a87aa0bc8d1.gif)

I’ve got a post coming soon explaining the above heat haze effect (I’ll link it here once it exists). The free [dragon](https://assetstore.unity.com/packages/3d/characters/creatures/dragon-the-soul-eater-and-dragon-boar-77121?aid=1011l3QFn), [log](https://assetstore.unity.com/packages/3d/fallen-tree-barrier-free-49089?aid=1011l3QFn), and [tree ](https://assetstore.unity.com/packages/3d/vegetation/the-illustrated-nature-sample-161188?aid=1011l3QFn)([full tree](https://assetstore.unity.com/packages/3d/vegetation/the-illustrated-nature-153939?aid=1011l3QFn)) assets are all from the asset store.

## Full Screen Shaders in HDRP

Full screen shader effects in HDRP are very similar to the built in renderer. Covered relatively well in the [official docs](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@7.1/manual/Custom-Post-Process.html), I’ll focus on the differences to built-in, and explain some items glanced over in the docs. In HDRP, you create these effects via the post processing stack.

To create the artifacts you need, right click in an Assets directory, and create both the post processing code (*Create > Rendering > C# Post Process Volume*) and the code shader (*Create > Shader > HDRP > Post Process*).

Note that the shader has to be code based. In most scenarios, HDRP pushes people towards using the shader graph. In this instance, however, only code shaders will work. I would assume this will change at some point, but as of HDRP 7.1.8, this is how it works.

Once you have created the two artifacts described above (C# and shader files) you’ll be most of the way there. Especially if you name the shader and the C# file the same thing (because the generated C# will find the shader of the same name). The generated C# file will be almost exactly the same as the sample code in the linked docs. Even so far as having an exposed “intensity” variable that it passes to the shader. The generated shader on the other hand does nothing. To be clear, it does nothing really well. It has all the scaffold you need, so you just need to jump into the method called `CustomPostProcess `

(the fragment shader), and make it do something pretty.

For my example, I’m going to do a conditional black & white effect. What I am calling “positional grayscale”. Basically, I chose the area around the main hard-hat to stay full color, and the rest of the image to be black & white. Code shown below if interested (screenshot further beyond that)

float4 CustomPostProcess(Varyings input) : SV_Target { UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input); uint2 positionSS = input.texcoord * _ScreenSize.xy; float3 sourceColor = LOAD_TEXTURE2D_X(_InputTexture, positionSS).xyz; float3 blackAndWhite = Luminance(sourceColor).xxx; float dist = length(input.texcoord - float2(0.34,0.5)); float mult = smoothstep(0.08, 0.10, dist); float3 outColor = sourceColor * (1-mult) + blackAndWhite * mult; return float4(outColor, 1); }

### Differences to Built In Renderer

There are four main differences between the HDRP C# and built in renderer.

One, you are not attaching a `MonoBehaviour `

to a camera, but instead adding a Post Processing effect to a Post Processing Volume. As such, the class type is `CustomPostProcessVolumeComponent, IPostProcessComponent`

. A key impact of this is that you can only expose certain data types. In my built in renderer example, I exposed a public `Shader `

variable. Here you cannot do that, and must use `Shader.Find()`

.

Second, for this to work, you have to add the effect you just created in *Project Settings > HDRP Default Settings*. A property called injectionPoint in the C# file drives where you can add it. The code snippet below is using BeforePostProcess, which matches the screenshot.

public override CustomPostProcessInjectionPoint injectionPoint => CustomPostProcessInjectionPoint.BeforePostProcess;

![HDRP Default Settings allows you to add a Before Post Process](../../assets/f29aee5e6ab62b13.png)

Third, the logic you’d previously put in `Start `

and `OnRenderImage `

are instead done in `Setup `

and `Render `

respectively. The logic isn’t exactly the same, but it’s very close.

Fourth, there are a few additional bits of code that you hadn’t needed in the built in renderer code.

public bool IsActive() => m_renderMaterial != null; public override CustomPostProcessInjectionPoint injectionPoint => CustomPostProcessInjectionPoint.BeforePostProcess; public override void Cleanup() => CoreUtils.Destroy(m_renderMaterial);

![Full Screen shader in HDRP - position based grayscale](../../assets/b26f7981da2502cf.png)

## Full Screen Shaders in the Universal RP

Saving the hardest for last, let’s talk about full screen shaders in URP. Unlike HDRP, the post processing volume system in URP does not support custom effects. Instead you have to write a custom renderer feature. I will note, it’s on their roadmap to have complete support, it’s just not up as of the writing of this article (URP version 8.2.0)

One bit of good news here is that custom renderer features provide much more flexibility. The result is you can use an unlit shader graph if you so choose. Don’t forget to grab some [additional nodes from the asset store](https://assetstore.unity.com/packages/vfx/shaders/nodes-for-shader-graph-124611?aid=1011l3QFn) as needed.

Tutorial writer Cyan has a [really good write-up on getting this going](https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/). I’ll still cover it here, partly to be thorough, and partly because I’ll highlight a few extra details for anyone totally unfamiliar with scriptable render pipelines.

### Material & Shader

First you create a material and shader. The shader can be code based or a shader graph. If using the graph, make it unlit (there’s no lighting in post-processing). Once you have the shader, set your material to use it. The only important detail in the shader is that it needs an input called `_MainTex`

. If you remember from my [shader graph tutorial](https://gamedevbill.com/shader-series-5-unity-shader-graph/), the shader graph input name doesn’t matter, it’s the “Reference” on that input that must be called `_MainTex`

.

### Renderer Feature

Next, make a C# file anywhere in your Assets directory, using the Blit code at the end of this article. I will again emphasize, it is copied completely from Cyan’s site.

With that, you need to set Blit as a Renderer Feature.

Start in *Edit->Preferences->Graphics.* From there you can select your SRP asset to find it in your project (double click it). WIth that selected, you can see the RendererList. Double click the ForwardRenderer (if ForwardRenderer isn’t your renderer, it should be, so try to find one and put it there).

Here you can add Renderer Features. Click the + and it’ll suggest “Blit” as one of the options because it’s found that code in your Assets folder. After adding the feature, you have to click it to see it’s settings (it may not look clickable, but it is). There you add your previously created material. Make sure Event is set to “Before Rendering Post Processing” and Blit Material Pass Index is set to 0 (so it doesn’t do costly and dumb things like a shadow pass).

![Where to add Blit function in Forward Renderer feature list.](../../assets/f440e3abd98fd5b9.png)

For URP I’ve created another conditionally black and white shader, similar to the HDRP shader above. In the HDRP shader, the screen was black and white based on position. In this shader graph, I make things black and white based on saturation. This utilizes some graph nodes I’ll discuss in a future tutorial (rgb2hsv & hsv2rgb). I’ll link it here once it exists.

![Full Screen shader in URP. Based on a shader graph.](../../assets/0ae8c228ecb37457.png)

![Saturation gating shader graph](../../assets/2e028c5c80bb6191.png)


![Saturation gating shader graph](../../assets/2e028c5c80bb6191.png)

## Conclusion

As I said at the start, this article is primarily a collection of data from around the web. All the info here can be found elsewhere, but from what I could tell, not in one place.

If you are interested in digging around other sources, you can try searching for both full screen shaders and “custom post processing effects”. From my experience, users of the built in renderer tend to use “full screen shader” more. In the newer renderers, however, you are more likely to hear “custom post processing shader”.

### Blit Code

Here’s the full blit code needed for the URP post process. Again, I took this directly from an [article written by Cyan](https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/). The only actual difference is I changed a `blitMaterialPassIndex `

to default to 0 (first pas only) instead of -1 (all passes).

using UnityEngine; using UnityEngine.Rendering; using UnityEngine.Rendering.Universal; // this was used on https://gamedevbill.com, but originally taken from https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/ // Saved in Blit.cs public class Blit : ScriptableRendererFeature { public class BlitPass : ScriptableRenderPass { public enum RenderTarget { Color, RenderTexture, } public Material blitMaterial = null; public int blitShaderPassIndex = 0; public FilterMode filterMode { get; set; } private RenderTargetIdentifier source { get; set; } private RenderTargetHandle destination { get; set; } RenderTargetHandle m_TemporaryColorTexture; string m_ProfilerTag; public BlitPass(RenderPassEvent renderPassEvent, Material blitMaterial, int blitShaderPassIndex, string tag) { this.renderPassEvent = renderPassEvent; this.blitMaterial = blitMaterial; this.blitShaderPassIndex = blitShaderPassIndex; m_ProfilerTag = tag; m_TemporaryColorTexture.Init("_TemporaryColorTexture"); } public void Setup(RenderTargetIdentifier source, RenderTargetHandle destination) { this.source = source; this.destination = destination; } public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData) { CommandBuffer cmd = CommandBufferPool.Get(m_ProfilerTag); RenderTextureDescriptor opaqueDesc = renderingData.cameraData.cameraTargetDescriptor; opaqueDesc.depthBufferBits = 0; // Can't read and write to same color target, use a TemporaryRT if (destination == RenderTargetHandle.CameraTarget) { cmd.GetTemporaryRT(m_TemporaryColorTexture.id, opaqueDesc, filterMode); Blit(cmd, source, m_TemporaryColorTexture.Identifier(), blitMaterial, blitShaderPassIndex); Blit(cmd, m_TemporaryColorTexture.Identifier(), source); } else { Blit(cmd, source, destination.Identifier(), blitMaterial, blitShaderPassIndex); } context.ExecuteCommandBuffer(cmd); CommandBufferPool.Release(cmd); } public override void FrameCleanup(CommandBuffer cmd) { if (destination == RenderTargetHandle.CameraTarget) cmd.ReleaseTemporaryRT(m_TemporaryColorTexture.id); } } [System.Serializable] public class BlitSettings { public RenderPassEvent Event = RenderPassEvent.AfterRenderingOpaques; public Material blitMaterial = null; public int blitMaterialPassIndex = 0; public Target destination = Target.Color; public string textureId = "_BlitPassTexture"; } public enum Target { Color, Texture } public BlitSettings settings = new BlitSettings(); RenderTargetHandle m_RenderTextureHandle; BlitPass blitPass; public override void Create() { var passIndex = settings.blitMaterial != null ? settings.blitMaterial.passCount - 1 : 1; settings.blitMaterialPassIndex = Mathf.Clamp(settings.blitMaterialPassIndex, -1, passIndex); blitPass = new BlitPass(settings.Event, settings.blitMaterial, settings.blitMaterialPassIndex, name); m_RenderTextureHandle.Init(settings.textureId); } public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData) { var src = renderer.cameraColorTarget; var dest = (settings.destination == Target.Color) ? RenderTargetHandle.CameraTarget : m_RenderTextureHandle; if (settings.blitMaterial == null) { Debug.LogWarningFormat("Missing Blit Material. {0} blit pass will not execute. Check for missing reference in the assigned renderer.", GetType().Name); return; } blitPass.Setup(src, dest); renderer.EnqueuePass(blitPass); } }

## References

- URP setup & code –
[Cyan](https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/) - HDRP setup & code –
[Unity docs](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@7.1/manual/Custom-Post-Process.html) - TV from Title Image –
[Bruna Araujo](https://unsplash.com/@brucaraujo?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)on[Unsplash](https://unsplash.com/s/photos/crt-monitor?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) - Asset Store items:
[dragon](https://assetstore.unity.com/packages/3d/characters/creatures/dragon-the-soul-eater-and-dragon-boar-77121?aid=1011l3QFn),[log](https://assetstore.unity.com/packages/3d/fallen-tree-barrier-free-49089?aid=1011l3QFn),[free-tree](https://assetstore.unity.com/packages/3d/vegetation/the-illustrated-nature-sample-161188?aid=1011l3QFn), and[full tree](https://assetstore.unity.com/packages/3d/vegetation/the-illustrated-nature-153939?aid=1011l3QFn). - Web hosting
[provided by BlueHost](https://www.bluehost.com/track/gamedevbill/AboutMe).

*Do something. Make progress. Have fun.*

## 3 comments on Full Screen Shaders in HDRP, URP, and Built In Renderer

## Comments are closed.