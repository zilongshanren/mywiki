---
title: Custom Depth in Unity
url: https://www.vertexfragment.com/ramblings/unity-custom-depth/
author: Steven Sell
published: '2023-04-04'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

When using a forward shader in Unity you can write out to the depth buffer using [the HLSL semantic](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics) `SV_Depth`

.

For example, a standard forward shader resembles this:

```
float4 FragMain(VertOutput input) : SV_Target
{
// Output the color green.
return float4(0.0f, 1.0f, 0.0f, 1.0f);
}
```


One can specify overrides for other semantics by defining an output structure.

```
struct ForwardFragmentOutput
{
float4 Color : SV_Target;
float Depth : SV_Depth;
};
ForwardFragmentOutput FragMain(VertOutput input)
{
ForwardFragmentOutput output = (ForwardFragmentOutput)0;
output.Color = float4(0.0f, 1.0f, 0.0f, 1.0f);
output.Depth = input.position.w;
return output;
}
```


The shader above outputs the color green, using the depth value from the interpolated clip-space position. This is the standard behaviour of a fragment shader that does not specify a `SV_Depth`

override. However, what if you want to specify your own override?

One common override is to set the depth to the max value. This is useful if you want to draw something behind everything else, such as a skybox.

`output.Depth = DEPTH_MAX;`


Where `DEPTH_MAX`

is determined [by the UNITY_REVERSED_Z macro.](https://docs.unity3d.com/2020.1/Documentation/Manual/SL-DepthTextures.html),

```
#ifdef UNITY_REVERSED_Z
#define DEPTH_MAX 0.0f
#define DEPTH_MIN 1.0f
#else
#define DEPTH_MAX 1.0f
#define DEPTH_MIN 0.0f
#endif
```


Certain effects may require you to calculate the depth value from a world-space position. An example of this is when performing raymarching as is done with volumetric clouds. When raymarching you can output the position of the cloud, but how do you turn that into a depth?

The obvious solution is to normalize the distance from that position to the camera. Something like this:

```
float3 cameraPosition = _WorldSpaceCameraPos; // Unity provided position of the camera/eye.
= float3(100.0f, 10.0f, 0.0f); // Position of the sample you want a depth value for.
float distanceToCamera = length(positionWS - cameraPosition);
float linearDepth = (distanceToCamera - _ProjectionParams.y) / (_ProjectionParams.z - _ProjectionParams.y);
```


This makes use of [the built-in Unity _ProjectionParams variable](https://docs.unity3d.com/Manual/SL-UnityShaderVariables.html) where

`.y`

is the near plane distance and `.z`

is the far plane distance. The calculated linear depth is on the range `[0, 1]`

where 0 = near and 1 = far.However, if you try to supply the linear depth value to `SV_Depth`

it will not work how you want it to. This is because the Unity depth buffer does not store linear depth values, but instead stores high precision packed depth values.

Pixel values in the Depth Texture range between 0 and 1, with a non-linear distribution. Precision is usually 32 or 16 bits, depending on configuration and platform used. When reading from the Depth Texture, a high precision value in a range between 0 and 1 is returned. (

[source])

So what we need is a way to convert our linear depth to the expected non-linear distribution. We can do this by creating the reverse of the Unity built-in `Linear01Depth`

function which converts from the non-linear distribution to a linear value. [As found in ShaderLibrary/Common.hlsl, the Linear01Depth function is defined as:](https://github.com/Unity-Technologies/Graphics/blob/19ec161f3f752db865597374b3ad1b3eaf110097/Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl#L1140)


```
float Linear01Depth(float depth, float4 zBufferParam)
{
return 1.0 / (zBufferParam.x * depth + zBufferParam.y);
}
```


Using a little algebra (and more parenthesis), we can construct the inverse of that function:

```
float LinearDepthToRawDepth(float linearDepth)
{
return (1.0f - (linearDepth * _ZBufferParams.y)) / (linearDepth * _ZBufferParams.x);
}
```


Which we can now use to calculate the expected depth value from our linear depth.

It is entirely possible that Unity already has a built-in function or helper to perform this.

However, I have not found it and I intensively Googled and looked through library shader files for a good 15 minutes or so. Maybe I should have asked ChatGPT?