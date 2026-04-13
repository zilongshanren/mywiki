---
title: Snapshot Shaders 2 - Scripting Guide
url: https://danielilett.com/snapshot-shaders-2/scripting-guide/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

In addition to editing the parameters on each effect at edit time in the Unity Editor, you can also change parameter values at runtime using C# scripting. This page will give you a quick guide to accessing the volume components on your profile and tweaking each parameter.

This asset pack uses URP’s Renderer Features to render each effect, and leverages the URP [Volume](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/api/UnityEngine.Rendering.Volume.html) system, so we will access a given `Volume`

, find the `Volume Profile`

attached to it, and retrieve a specific effect from the profile whose parameters can then be changed as desired.

Here is an example script which accepts a `Volume`

parameter, finds an `UnderwaterSettings`

volume component attached to its `Volume Profile`

, and sets the `waveFlowMap`

, `waveFlowSpeed`

, and `causticsScrollVelocity1`

parameters.

```
using UnityEngine;
using UnityEngine.Rendering;
public class ChangeVolumeParametersExample : MonoBehaviour
{
// This is the Volume which contains the profile we want to modify.
public Volume volume;
// These are the desired parameter values, supplied through the Inspector.
public Texture2D newFlowTexture;
public float newFlowSpeed;
public Vector3 newCausticsVelocity;
private void Start()
{
// Get a reference to the UnderwaterSettings. This assumes that the
// volume has a profile attached.
UnderwaterSettings underwaterEffect = null;
if(volume.profile.TryGet(out underwaterEffect))
{
// Change parameter values.
underwaterEffect.waveFlowMap.value = newFlowTexture;
underwaterEffect.waveFlowSpeed.value = newFlowSpeed;
underwaterEffect.causticsScrollVelocity1 = newCausticsVelocity;
}
}
}
```