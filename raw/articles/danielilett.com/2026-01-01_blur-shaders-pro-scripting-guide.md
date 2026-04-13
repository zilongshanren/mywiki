---
title: Blur Shaders Pro - Scripting Guide
url: https://danielilett.com/blur-shaders-pro/scripting-guide/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

You can customise and control how each effect in *Blur Shaders Pro* works using scripting. The process is slightly different betwene each of the three pipelines. This page will provide a bare-bones explanation of how to modify effects in each pipeline, including the namespaces you will need to use and the classes you need to access to change properties of an effect.

# ✨ Universal Render Pipeline (URP)

URP currently uses the Renderer Features system for custom post-processing effects. Each effect is compatible with the [URP Volume](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@13.0/api/UnityEngine.Rendering.Volume.html) system, so we use that API (in the `UnityEngine.Rendering`

namespace) to access individual effects. In this example, we will modify the blur size of a `Blur`

effect. Attach this script to any object and drag the volume you wish to modify onto the `volume`

field.

Note: in URP, unlike the other pipelines, the name of each effect class has ‘Settings’ appended, e.g. the `Blur`

effect is accessed through the `BlurSettings`

class.

```
using UnityEngine;
using UnityEngine.Rendering;
public class ExampleScriptURP : MonoBehaviour
{
public Volume volume;
private void Start()
{
// Get a reference to the specific effect you want here.
BlurSettings blurEffect = null;
if(volume.profile.TryGet(out blurEffect))
{
// Change any settings you want on the effect here.
blurEffect.strength.value = 50;
blurEffect.blurStepSize.value = 2;
}
}
}
```


# ✨ High Definition Render Pipeline (HDRP)

HDRP supports custom post processes out of the box. These effects use the [HDRP Volume system](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@10.0/manual/Volumes-API.html), which we interact with to modify effects. In this example, we will modify the `Blur`

effect by changing the `strength`

and `blurStepSize`

properties.

```
using UnityEngine;
using UnityEngine.Rendering;
public class ExampleScriptHDRP : MonoBehaviour
{
public Volume volume;
private void Start()
{
// Get a reference to the specific effect you want here.
Blur blurEffect = null;
if (volume.profile.TryGet(out blurEffect))
{
// Change any settings you want on the effect here.
blurEffect.strength.value = 50;
blurEffect.blurStepSize.value = 2;
}
}
}
```


# ✨ Built-in Render Pipeline

The built-in render pipeline uses the [Post Processing Stack v2 system](https://docs.unity3d.com/Packages/com.unity.postprocessing@2.0/api/UnityEngine.Rendering.PostProcessing.html). We interface with the systems included in the `UnityEngine.Rendering.PostProcessing`

namespace. In this example, we will access a `RadialBlur`

effect attached to a profile which is being used on a volume, then tweak the `strength`

and `stepSize`

variables. Attach this script to any object and drag the volume you wish to modify onto the `volume`

field.

```
using UnityEngine;
using UnityEngine.Rendering.PostProcessing;
public class ExampleScriptBuiltIn : MonoBehaviour
{
public PostProcessVolume volume;
private void Start()
{
// Get a reference to the specific effect you want here.
RadialBlur radialBlurEffect = null;
if(volume.profile.TryGetSettings(out radialBlurEffect))
{
// Change any settings you want on the effect here.
radialBlurEffect.strength.value = 50;
radialBlurEffect.stepSize.value = 2;
}
}
}
```