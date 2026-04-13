---
title: Prevent Object Culling in Unity
url: https://www.vertexfragment.com/ramblings/unity-prevent-object-culling/
author: Steven Sell
published: '2022-05-01'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

Occasionally you may need to ensure that an object is not clipped and is always visible, so long as the camera is looking at it. Such use-cases that I personally have come across are:

- Custom skyboxes and effects.
- Object-based sun, moon, etc.
- Large particle systems that Unity does not properly update bounds for.

These can be broken down into two-categories: objects that should not be clipped by the left/right/top/bottom frustum planes and objects that should not be clipped by the far plane.

To prevent object culling you first need to have an understanding of *why* it is being clipped.

The full details are beyond the scope of this ramble, and there are ample other sources out there that go into depth as this is not an Unity-specific behavior and all 3D renderers make use of it. It being [Frustum Culling](https://learnopengl.com/Guest-Articles/2021/Scene/Frustum-Culling).

The short of it is a camera defines a view frustum which is composed of 6 planes: near, far, left, right, top, bottom. Additionally every visible object in Unity using a `MeshRenderer`

has a [render bounds](https://docs.unity3d.com/ScriptReference/Renderer-bounds.html). If an object’s render bounds is outside all 6 planes of the frustum then Unity discards it and it is not rendered that frame. To prevent an object being clipped because it is outside all of the side planes you simply need to trick Unity into thinking it is within the planes.

```
public sealed class PreventFrustumCulling : MonoBehaviour
{
public MeshRenderer Renderer;
private void Start()
{
Renderer = Renderer ?? GetComponent<MeshRenderer>();
}
private void Update()
{
if ((Camera.main == null) || (Renderer == null))
{
return;
}
Bounds adjustedBounds = Renderer.bounds;
adjustedBounds.center = Camera.main.transform.position + (Camera.main.transform.forward * (Camera.main.farClipPlane - Camera.main.nearClipPlane) * 0.5f);
adjustedBounds.extents = new Vector3(0.1f, 0.1f, 0.1f);
Renderer.bounds = adjustedBounds;
}
}
```


Each frame we place the render bounds directly in front of the camera, half-way through the frustum. We also resize the extents so that they are smaller and fit within the frustum. Typically this latter part is not necessary so long as the center is within the frustum bounds.

The solution above is sufficient for preventing culling by the side planes, but not for the far plane. If you need to have an object placed very far away, beyond the far plane, then a custom shader is needed as well.

This is because the above solution will prevent the object from being culled on the CPU side, but will not stop it from being culled on the GPU during [the rasterizer stage](https://docs.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage).

As the Unity rendering ecosystem is quite diverse I will not provide an universal shader that meets every need. By diverse, I am referring to:

- At least 4 different render pipelines: Built-In, URP, HDRP, SRP.
- At least 2 different renderers each: Forward and Deferred.
- At least 2 different shader languages each: CG and HLSL.
- Support for shader graphs.

The adjustment needed however would be the same for all. Within the vertex program we need to modify the vertex positions so that they fit within the bounds of [clip space](https://learnopengl.com/Getting-started/Coordinate-Systems) and are not discarded by the rasterizer.

Below is an example vertex program for URP v12, but the general concept can be applied anywhere.

```
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/ShaderVariablesFunctions.hlsl"
// Configurable +/- nudge so we are not checking against the exact far plane bounds.
// Personally use a _FarPlaneOffset of 1.0.
float _FarPlaneOffset;
CBUFFER_END
struct VertInput
{
float4 position : POSITION;
// ...
struct VertOutput
{
float4 position : SV_POSITION;
// ...
VertMain(VertInput input)
{
VertOutput output = (VertOutput)0;
VertexPositionInputs vertexInput = GetVertexPositionInputs(input.position.xyz);
// Get our clip-space position which we will be adjusting as needed.
= vertexInput.positionCS;
// Get our world-space position and its distance from the camera.
= vertexInput.positionWS;
float3 cameraToPositionWS = positionWS - _WorldSpaceCameraPos;
float distanceToCamera = length(cameraToPositionWS);
float distancePastFarPlane = (distanceToCamera + _FarPlaneOffset) - _ProjectionParams.z;
// If our vertex is beyond the far plane, then we pull it back in.
if (distancePastFarPlane >= 0.0f)
{
// Our new distance is the previous distance minus the how far past the plane we are.
// We use _FarPlaneOffset to provide a material configurable further nudge.
float correctedDistance = distanceToCamera - distancePastFarPlane - _FarPlaneOffset;
float3 dirCameraToPosition = normalize(cameraToPositionWS);
float3 correctedPositionWS = _WorldSpaceCameraPos + (dirCameraToPosition * correctedDistance);
// Transform the corrected world-space position to clip space.
= TransformWorldToHClip(correctedPositionWS);
}
return output;
}
```


The global variables should be available to all rendering environments, however the functions are URP specific. Fortunately the source is freely available and so can be adapted to any other environment as needed.

**Variables:**

**Functions:**

With that vertex shader, any vertex beyond the far clip will be pulled back in and pass through the rasterizer.

Unfortunately there aren’t too many alternatives to the above approaches, at least as far as I am aware of.

The most obvious alternate approach is a multi-camera based one, where the far distant objects are rendered to a separate camera with better fitting near/far clip planes. The render texture of the secondary camera would need to be combined with the primary camera.