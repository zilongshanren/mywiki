---
title: Snapshot Shaders Pro - Scripting Guide
url: https://danielilett.com/snapshot-shaders-pro/scripting-guide/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

You can customise and control how each effect in *Snapshot Shaders Pro* works using scripting. The process is slightly different betwene each of the three pipelines. This page will provide a bare-bones explanation of how to modify effects in each pipeline, including the namespaces you will need to use and the classes you need to access to change properties of an effect.

# ✨ Universal Render Pipeline (URP)

URP currently uses the Renderer Features system for custom post-processing effects. Each effect is compatible with the [URP Volume](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@13.0/api/UnityEngine.Rendering.Volume.html) system, so we use that API (in the `UnityEngine.Rendering`

namespace) to access individual effects. In this example, we will modify the `textureSize`

property on a `Halftone`

effect. Attach this script to any object and drag the volume you wish to modify onto the `volume`

field.

Note: in URP, unlike the other pipelines, the name of each effect class has ‘Settings’ appended, e.g. the `Halftone`

effect is accessed through the `HalftoneSettings`

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
HalftoneSettings halftoneEffect = null;
if(volume.profile.TryGet(out halftoneEffect))
{
// Change any settings you want on the effect here.
halftoneEffect.textureSize.value = 8;
}
}
}
```


# ✨ High Definition Render Pipeline (HDRP)

HDRP supports custom post processes out of the box. These effects use the [HDRP Volume system](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@10.0/manual/Volumes-API.html), which we interact with to modify effects. In this example, we will modify the `Vortex`

effect by changing the `strength`

property.

```
using UnityEngine;
using UnityEngine.Rendering;
public class ExampleScriptHDRP : MonoBehaviour
{
public Volume volume;
private void Start()
{
// Get a reference to the specific effect you want here.
Vortex vortexEffect = null;
if (volume.profile.TryGet(out vortexEffect))
{
// Change any settings you want on the effect here.
vortexEffect.strength.value = 2.5f;
}
}
}
```


# ✨ Built-in Render Pipeline

The built-in render pipeline uses the [Post Processing Stack v2 system](https://docs.unity3d.com/Packages/com.unity.postprocessing@2.0/api/UnityEngine.Rendering.PostProcessing.html). We interface with the systems included in the `UnityEngine.Rendering.PostProcessing`

namespace. In this example, we will access an `Oil Painting`

effect attached to a profile which is being used on a volume, then tweak the `kernelSize`

variable. Attach this script to any object and drag the volume you wish to modify onto the `volume`

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
OilPainting oilPaintingEffect = null;
if(volume.profile.TryGetSettings(out oilPaintingEffect))
{
// Change any settings you want on the effect here.
oilPaintingEffect.kernelSize.value = 27;
}
}
}
```