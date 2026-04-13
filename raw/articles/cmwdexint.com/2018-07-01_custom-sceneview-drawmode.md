---
title: Custom SceneView DrawMode
url: https://cmwdexint.com/2018/07/01/custom-sceneview-drawmode/
author: Ming Wai Chan
published: '2018-07-01'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

##### The beautiful scene is from the asset store package:

[RPG Medieval Kingdom Kit by BEFFIO](https://assetstore.unity.com/packages/3d/environments/fantasy/rpg-medieval-kingdom-kit-118468)

![Screen Shot 2018-06-28 at 21.43.05](../../assets/d34d99c0abf171b0.png)


Download : [https://drive.google.com/open?id=1hloorB11hPcIXIIKBIRzqvon9mpmbYPK](https://drive.google.com/open?id=1hloorB11hPcIXIIKBIRzqvon9mpmbYPK)

If you are looking for doing it in** custom SRP**, please visit [my github](https://github.com/cinight/CustomSRP/tree/master/Assets/SRP0902_SceneViewDrawMode)

How to use :

Just add your shaders and names to the CustomDrawModeAsset

This does not work in SRP. But we can implement the same thing in the pipeline code:

Possible pipeline codes:

//Variables

private static ShaderPassName passNameDefault =

new ShaderPassName(“SRPDefaultUnlit”);

private static Material mat;

private static FilterRenderersSettings filterSettings;

//In Pipeline

DrawRendererSettings drawSettingsDefault =

new DrawRendererSettings(cam, passNameDefault);

drawSettingsDefault.SetShaderPassName(1,passNameDefault);

if (mat==null) mat = new Material(CustomDrawModeAssetObject.cdma.customDrawModes[i].shader);

drawSettingsDefault.SetOverrideMaterial( mat, 0 );

filterSettings = new FilterRenderersSettings(true);

filterSettings.renderQueueRange = RenderQueueRange.opaque;

drawSettingsDefault.sorting.flags = SortFlags.CommonOpaque;

context.DrawRenderers(cull.visibleRenderers, ref drawSettingsDefault, filterSettings);

filterSettings.renderQueueRange = RenderQueueRange.transparent;

drawSettingsDefault.sorting.flags = SortFlags.CommonTransparent;

context.DrawRenderers(cull.visibleRenderers, ref drawSettingsDefault, filterSettings);

LikeLike

Just found this while researching how to add custom draw modes for artists to check their work, so thanks! I did have a question, though: I’ve noticed that when enabled, all the other draw modes (aside from the Shading Mode and custom categories) are unselectable. I double checked your video and noticed the same thing happening there. Is there any way to get them back short of doing a domain reload and ensuring the CustomDrawModeAsset doesn’t get loaded?

LikeLike

You can have them back by editing the script 🙂 In one of the script there is a function which does the filtering. Let me know if you have problem understanding the codes.

LikeLike

Actually nevermind, I just noticed the AcceptedDrawMode callback!

LikeLike

Thanks for this! There’s one formality I’d kindly asked of you: Could you please clarify under which License Terms this can be used?

LikeLike

Feel free to use it if you find it useful : )

LikeLike