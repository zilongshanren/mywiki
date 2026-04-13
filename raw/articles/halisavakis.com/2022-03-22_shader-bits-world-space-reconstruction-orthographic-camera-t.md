---
title: 'Shader bits: World space reconstruction, orthographic camera texture projection
  & fake perspective UVs'
url: https://halisavakis.com/shader-bits-world-space-reconstruction-orthographic-camera-texture-projection-fake-perspective-uvs/
published: '2022-03-22'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Hey there! It’s been a while 👀

I’ve found that I’ve been copying around some shader code from different files here and there, and I thought it’d be handy for me and for you to have those around in a new Shader Bits post.

Let’s get started~

## World-space reconstruction

While I was creating yet another water shader on [a stream](https://youtu.be/red4RKVd8PE) I found myself wanting to add caustics below the water surface, without modifying the terrain shader or adding any other extra elements.

Luckily, I had [Cyan](https://twitter.com/Cyanilux) on the stream who suggested this method in order to reconstruct the world-space position of the world when looking through an object:

```
sampler2D _CameraDepthTexture;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.worldPos = mul(unity_ObjectToWorld, v.vertex);
o.screenPos = ComputeScreenPos(o.vertex);
return o;
}
fixed4 frag (v2f i) : SV_Target
{
float depth = tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(i.screenPos));
depth = LinearEyeDepth(depth);
float3 worldSpaceCoords = ((_WorldSpaceCameraPos - i.worldPos) / i.screenPos.w) * depth - _WorldSpaceCameraPos;
return float4(frac(worldSpaceCoords), 1.0);
}
```

Using this snippet you’ll visualize the world-space coordinates of the world through the object to which a material using this shader is attached.

Alex Ameye shared a beautiful application of this effect here: [https://twitter.com/alexanderameye/status/1505910721376362503?s=20&t=jEF_JxkCMIVsVIpp7v_PQg](https://twitter.com/alexanderameye/status/1505910721376362503?s=20&t=jEF_JxkCMIVsVIpp7v_PQg)

## Orthographic camera texture projection

I’ve found it pretty common for me to use render textures from orthographic cameras for dynamic effects. A great example of this approach is for water ripples, as demonstrated in [this tutorial](https://www.patreon.com/posts/24192529) by Joyce.

You’ll have to pass to the shader the world-space position of the orthographic camera and its orthographic size in order for this to work. Given that we name these properties as `_OrthographicCamPosition`

and `_OrthographicCamSize`

respectively, the snippet looks like this:

```
float2 orthoProjUV = IN.worldPos.xz - _OrthographicCamPosition.xz;
orthoProjUV = orthoProjUV/(_OrthographicCamSize *2);
orthoProjUV += 0.5;
```

where IN.worldPos is the world-space position.

## Fake perspective UVs

I might not use this as often, but it’s a neat trick so I thought I’d store this here for when I need it again. It’s a simple UV manipulation to fake some perspective depth on a 2D surface. The snippet looks like this:

```
float2 puv = i.uv;
puv.x -= 0.5;
puv /= 1.0 - puv.y * 2.0;
puv.x += 0.5;
```

Outputting these UVs on a flat plane (with a frac to better see the values) will yield these results:

![](https://i0.wp.com/halisavakis.com/wp-content/uploads/2022/03/image-1.png?resize=491%2C490&ssl=1)

Hope these will come in handy for you! See you in the next one!