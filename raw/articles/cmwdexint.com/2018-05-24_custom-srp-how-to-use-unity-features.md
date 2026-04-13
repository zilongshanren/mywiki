---
title: '[Custom SRP] How to use Unity features?'
url: https://cmwdexint.com/2018/05/24/custom-srp/
author: Ming Wai Chan
published: '2018-05-24'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

**Update:**

If you are using **2019.1+**, you might notice there is a big change to the SRP APIs.

I’ve created a new repository and you can grab here. Much cleaner and minimal.



![May-14-2018 gif](../../assets/806e5e808fa6a906.gif)


![Screen Shot 2018-06-02 at 22.16.24](../../assets/a31f15cd9aa09437.png)


![SRPFlow](../../assets/9ba2210a703c9a91.jpg)

![Screen Shot 2018-05-12 at 18.52.43](../../assets/40b460b4ebcd5832.png)


Here lists out exact what codes enable the Unity feature when making our custom SRP.

##### *Note that my codes may not be perfectly optimised, but the concept itself won’t change.

(!) Alert: Below information might be outdated. I stopped updating this note after 2018.x releases.

Indicators:

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**pipeline** code

![icon_shader](../../assets/58a4f9580986828d.png)

**shader** code

✅ Doesn’t need to specifically care about it in codes. Write the codes as usual.



**Occlusion Culling**

![icon_script](../../assets/e3c236a2c3aa1fad.png)



**Batching**

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**Static batching** works like usual ✅

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**Dynamic batching** ~~is disabled by default~~, you can turn it on with :

DrawRendererSettings drawSettingsBase = new DrawRendererSettings(camera, passNameBase); drawSettingsBase.flags = DrawRendererFlags.EnableDynamicBatching;


**GPU Instancing**

![icon_shader](../../assets/58a4f9580986828d.png)

[instancing codes](https://docs.unity3d.com/Manual/GPUInstancing.html) in shader as usual ✅

![icon_script](../../assets/e3c236a2c3aa1fad.png)


DrawRendererSettings drawSettingsBase = new DrawRendererSettings(camera, passNameBase); drawSettingsBase.flags = DrawRendererFlags.EnableInstancing;


**Unlit Shader**

![icon_shader](../../assets/58a4f9580986828d.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)


private static ShaderPassName passNameDefault = new ShaderPassName("SRPDefaultUnlit"); //… DrawRendererSettings drawSettingsDefault = new DrawRendererSettings(camera, passNameDefault); drawSettingsDefault.SetShaderPassName(1,passNameDefault);


**Surface Shader / Standard Shader / Other legacy lit shaders**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


1. Call DrawRenderers with **legacy pass names** *e.g. ForwardBase, ForwardAdd*

2. You enable the **shader keywords** e.g. shader keywords in standard shader

3. You set the **Global Shader Properties** of lights / GI data *e.g. _LightColor0, _WorldSpaceLightPos0*

![icon_shader](../../assets/58a4f9580986828d.png)


*⚠️ Suggested that we better not to use surface shader anymore because it’s full of hidden magic which gives limitation to advanced shader programmers.*


**Compute Shader**

![icon_script](../../assets/e3c236a2c3aa1fad.png)

![icon_shader](../../assets/58a4f9580986828d.png)



**Multi-Pass Shader**

*⚠️ Remember we used to have multi-pass shader like this to achieve layered fur? It is not supported anymore. Because it creates so many draw calls (1 pass = 1 draw call). Suggested that we use alternative ways to achieve the same effect, e.g. geometry shaders, or fur quad pieces on the 3D model to imitate fur.*

**Built-in Shader Variables**

![icon_shader](../../assets/58a4f9580986828d.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)

[built-in shader variables](https://docs.unity3d.com/Manual/SL-UnityShaderVariables.html) are set with :

context.SetupCameraProperties(camera);


**_CameraDepthTexture / ****Projector / Decal / Motion Vector textures**

![icon_shader](../../assets/58a4f9580986828d.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)

**_CameraDepthTexture** :

CommandBuffer cmdDepthOpaque = new CommandBuffer(); cmdDepthOpaque.name = "Depth Pass"; //m_DepthRT has the colour format = RenderTextureFormat.Depth cmdDepthOpaque.SetRenderTarget(m_DepthRT); cmdDepthOpaque.ClearRenderTarget(true, true, Color.black); context.ExecuteCommandBuffer(cmdDepthOpaque); cmdDepthOpaque.Clear(); //Objects with Zwrite On will generate depth data filterSettings.renderQueueRange = RenderQueueRange.opaque; drawSettingsDepth.sorting.flags = SortFlags.CommonOpaque; context.DrawRenderers( cull.visibleRenderers, ref drawSettingsDepth, filterSettings); //m_DepthRTid’s has the name “_CameraDepthTexture” cmdDepthOpaque.SetGlobalTexture(m_DepthRTid, m_DepthRT); context.ExecuteCommandBuffer(cmdDepthOpaque); cmdDepthOpaque.Release();


**GrabPass**

*⚠️ In legacy pipelines, this is a very expensive operation because it t riggers re-rendering of objects. Although we can implement it in SRP but better find an alternative way to fake it.
Use in shader as usual, just pay attention to the order of rendering ✅*

![icon_shader](../../assets/58a4f9580986828d.png)

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**opaque**objects so that we can use in

**transparent**objects and achieve distortion effect. Just set the global texture with the name you want:

cmdColorOpaque.SetGlobalTexture(m_GrabOpaqueRTid, m_ColorRT);


**CameraEvent**

*⚠️ In legacy pipeline, we can extend the pipeline by adding CommandBuffer to different CameraEvents. As you can see these are legacy pipeline event names so this approach is not supported in SRP. But we are always free to edit the pipeline :). Update: we can make custom passes / use the available callback function, so that we can insert commands from other scripts. See LightWeightPipeline Passes.*

**Baked Light and Shadow / ****Reflection Probe / Light Probe**

![icon_shader](../../assets/58a4f9580986828d.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)

**Reflection probe** needs content of rendered objects, so make sure you do Blit() to BuiltinRenderTexture.CameraTarget

![icon_script](../../assets/e3c236a2c3aa1fad.png)


private static RendererConfiguration renderConfig = RendererConfiguration.PerObjectReflectionProbes | RendererConfiguration.PerObjectLightmaps | RendererConfiguration.PerObjectLightProbe; //.. DrawRendererSettings drawSettingsBase = new DrawRendererSettings(camera, passNameBase); drawSettingsBase.rendererConfiguration = renderConfig;


**Realtime Light and Shadow**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_shader](../../assets/58a4f9580986828d.png)


💡 Feel free to reference to different pipelines e.g. [LWRP](https://github.com/Unity-Technologies/ScriptableRenderPipeline/tree/master/com.unity.render-pipelines.lightweight/LWRP), [HDRP
](https://github.com/Unity-Technologies/ScriptableRenderPipeline/tree/master/com.unity.render-pipelines.high-definition/HDRP)💡 If you want simple ones e.g.

[BasicRenderPipeline](https://github.com/Unity-Technologies/ScriptableRenderPipelineData/tree/master/TestbedPipelines/BasicRenderPipeline)(only lighting), my

[playground pipeline](https://github.com/Unity-Technologies/ScriptableRenderPipelineData/tree/master/TestbedPipelines/BasicRenderPipeline)(only 1 directional light and hard shadow)


**Fog (In LightingSettings panel)**

![icon_shader](../../assets/58a4f9580986828d.png)


**HDR**

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**HDR format** (e.g. RenderTextureFormat.DefaultHDR ) on the TemporaryRenderTexture for color buffer

![icon_script](../../assets/e3c236a2c3aa1fad.png)


**MSAA**

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**msaasample** to 1,2,4,8 on TemporaryRenderTextures depends on your settings

![icon_script](../../assets/e3c236a2c3aa1fad.png)


RenderTextureDescriptor colorRTDesc = new RenderTextureDescriptor( camera.pixelWidth, camera.pixelHeight); colorRTDesc.colorFormat = m_ColorFormat; //HDR format colorRTDesc.depthBufferBits = depthBufferBits; colorRTDesc.sRGB = true; colorRTDesc.msaaSamples = 1; //MSAA colorRTDesc.enableRandomWrite = false; cmdTempId.GetTemporaryRT( m_ColorRTid, colorRTDesc, FilterMode.Bilinear);


**Post-processing stack**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)


CommandBuffer cmdpp = new CommandBuffer(); cmdpp.name = "Post-processing"; m_PostProcessRenderContext.Reset(); m_PostProcessRenderContext.camera = camera; m_PostProcessRenderContext.source = m_ColorRT; m_PostProcessRenderContext.sourceFormat = m_ColorFormat; m_PostProcessRenderContext.destination = BuiltinRenderTextureType.CameraTarget; m_PostProcessRenderContext.command = cmdpp; m_PostProcessRenderContext.flip = camera.targetTexture == null; m_CameraPostProcessLayer.Render(m_PostProcessRenderContext); context.ExecuteCommandBuffer(cmdpp); cmdpp.Release();


**Multi-Cameras**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)



bool clearcolor = true; bool cleardepth = true; if( cam.clearFlags == CameraClearFlags.Skybox || cam.clearFlags == CameraClearFlags.Depth ) {clearcolor = false;} cmd.ClearRenderTarget( cleardepth, clearcolor, camera.BackgroundColor);


**Multi-RenderTargets**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_shader](../../assets/58a4f9580986828d.png)

**SV_Target
**💡 You might want to try

[RenderPass](https://docs.unity3d.com/ScriptReference/Experimental.Rendering.RenderPass.html)approach for MRT rendering


**Multi-Pipelines**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


public override void Render( ScriptableRenderContext renderContext, Camera[] cameras) { Camera[] defaultCameras; Camera[] customCameras; SRPDefault.FilterCameras(cameras, out defaultCameras, out customCameras); SRPPlaygroundPipeline.Render(renderContext, customCameras); SRPDefault.Render(renderContext, defaultCameras); }

**Scene View / ****Preview Camera**

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**BuiltinRenderTextureType.CameraTarget** has both **Color** and **Depth** contents so that gizmo and selection outline works

*⚠️ Mind that Blit() only copies color buffer. If you want to copy depth buffer, you need a shader that outputs to SV_Depth*

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**Blit()** to **BuiltinRenderTextureType.CameraTarget** at necessary stage so that the toggle buttons on scene view functions correctly

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**UGUI**** geometry** visible in scene view, do

#if UNITY_EDITOR if (camera.cameraType == CameraType.SceneView) ScriptableRenderContext.EmitWorldGeometryForSceneView(camera); #endif


**Draw Mode**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


![icon_script](../../assets/e3c236a2c3aa1fad.png)

[this](https://github.com/Unity-Technologies/ScriptableRenderPipeline/blob/master/com.unity.render-pipelines.lightweight/LWRP/SceneViewDrawMode.cs).

#if UNITY_EDITOR ArrayList sceneViewArray = SceneView.sceneViews; foreach (SceneView sceneView in sceneViewArray) { //Define which draw mode you don't want in RejectDrawMode sceneView.onValidateCameraMode += RejectDrawMode; } #endif


**Default Shader when creating objects**

![icon_script](../../assets/e3c236a2c3aa1fad.png)

**RenderPipelineAsset** class :

public override Shader GetDefaultShader() { Shader m_DefaultShader = Shader.Find(“MyPipeline/DefaultShader”); return m_DefaultShader; }


**Pink Error Shader**

![icon_shader](../../assets/58a4f9580986828d.png)



**Make other unsupported pipelines’ shader pink**

![icon_script](../../assets/e3c236a2c3aa1fad.png)


private static ShaderPassName passNameForwardBase = new ShaderPassName("ForwardBase"); //… DrawRendererSettings drawSettingsForwardBase = new DrawRendererSettings(camera, passNameForwardBase); drawSettingsForwardBase.rendererConfiguration = RendererConfiguration.None; drawSettingsForwardBase.SetOverrideMaterial( m_ErrorMaterial, 0); //Use "Hidden/InternalErrorShader"

**Pipeline Asset**

![icon_script](../../assets/e3c236a2c3aa1fad.png)

[BasicRenderPipeline](https://github.com/Unity-Technologies/ScriptableRenderPipelineData/tree/master/TestbedPipelines/BasicRenderPipeline)

*⚠️ Thus lots of settings in the Editor will become invalid. Some settings in Graphics Settings / Quality Settings / Player Settings will be hidden once we are using our own pipeline. e.g. Built-in Shader Settings, shadow settings, MSAA settings*


### Lighting Settings / MeshRenderer Settings

![icon_script](../../assets/e3c236a2c3aa1fad.png)


#if UNITY_EDITOR SupportedRenderingFeatures.active = new SupportedRenderingFeatures() { reflectionProbeSupportFlags = SupportedRenderingFeatures.ReflectionProbeSupportFlags.None, defaultMixedLightingMode = SupportedRenderingFeatures.LightmapMixedBakeMode.Subtractive, supportedMixedLightingModes = SupportedRenderingFeatures.LightmapMixedBakeMode.Subtractive | SupportedRenderingFeatures.LightmapMixedBakeMode.Shadowmask, supportedLightmapBakeTypes = LightmapBakeType.Baked | LightmapBakeType.Mixed | LightmapBakeType.Realtime, supportedLightmapsModes = LightmapsMode.CombinedDirectional | LightmapsMode.NonDirectional, rendererSupportsLightProbeProxyVolumes = false, rendererSupportsMotionVectors = false, rendererSupportsReceiveShadows = true, rendererSupportsReflectionProbes = true }; #endif



Excellent writeup. Thanks! I understand that everything is still experimental but this should be official documentation already 🙂

(e.g. was looking for “SRPDefaultUnlit” for way too long)

LikeLike

Thanks! 😊 I’ll see if I can make these into docs… but there are still many things missing, e.g. the docs for Core RP library

LikeLike