---
title: Accurate Normal Reconstruction from Depth Buffer
url: https://atyuwen.github.io/posts/normal-reconstruction/
published: '2020-01-20'
source_blog: C++ Minor
source_site: https://atyuwen.github.io/
category: graphics
fetched: '2026-04-19'
---

Months ago I read a nice article 1 about normal reconstruction by János Turánszki (@turanszkij), which reminded me that I had also tackled this problem before, but for a different purpose. While Turánszki reconstructed normal from depth buffer for better SSAO, I was aimed for rendering decals.

In screen-space decals rendering, normal buffer is required to reject pixels projected onto near-perpendicular surfaces. But back then I was working on a forward pipeline, so no normal buffer was outputted. It seemed the best choice was to reconstruct it directly from depth buffer, as long as we could avoid introducing errors, which was not easy though. Fortunately, accurate normal reconstruction is impossible in theory but possible in practice, we eventually found a way inspired by Humus’s SDAA idea 2, which is more accurate but also more expensive than Turánszki’s method. However, it’s worth the cost because decals are highly sensitive to the reconstruction errors. Following shows decals rendered in purple with different normal reconstruction strategies.

![](../../assets/61c00375a2a94266.png)

- Left: simply uses cross(ddx, ddy), note the artifacts in areas labeled with
**a**,**b**, and**c**. - Middle: the
*improved approach*, the artifacts in[1](https://atyuwen.github.io#fn:1)**a**disappeared, but those in**b**and**c**still exist. - Right: our
*accurate method*, all artifacts are eliminated.

To understand how those artifacts occur and disappear, I drawn a picture to illustrate the two typical types of discontinuities in depth buffer, in which the eye and arrow denote the camera position and direction respectively, and the blue dots denote the depth samples.

![](../../assets/6b0d962802ae77db.png)

In figure (1), Turánszki’s method works very well. 3 taps are enough to eliminate errors: since $|d-c|$ is less than $|b-c|$, we can say that point $c$ is more likely on segment $de$ rather than segment $ab$. But this is not the case in figure (2): although $|b-c| < |d-c|$, the point $c$ is apparently on segment $de$ instead of $ab$. This observation perfectly explains why the *improved approach* can only remove part of the artifacts in decal rendering.

So we can conclude that 3 taps (on each direction) is inadequate. Humus’s SDAA 2 uses 5 sample taps along with a second depth layer to calculate edge locations, here we can use the same 5-tap pattern to determinate whether $c$ is on $ab$ or $de$. (Unlike SDAA, we don’t have to calculate the accurate edge location, so the second-depth buffer is not needed.) Following describes the method step by step.

![](../../assets/d89a29e86cd07eab.png)

- Extrapolate segment $ab$ to $c$, get a new point $c_1$.
- Extrapolate segment $ed$ to $c$, get a new point $c_2$.
- If $|c_1-c| < |c_2-c|$, report $c$ is on $ab$, otherwise report $c$ is on $de$.

Note this method can locate $c$ correctly in both figure (1) and (2). Now we can apply this algorithm twice to get horizontal and vertical derivatives, then a cross product gives you the normal accurately. Here is the pseudo shader code.

```
// Try reconstructing normal accurately from depth buffer.
// input DepthBuffer: stores linearized depth in range (0, 1).
// 5 taps on each direction: | z | x | * | y | w |, '*' denotes the center sample.
float3 ReconstructNormal(texture2D DepthBuffer, float2 spos: SV_Position)
{
float2 stc = spos / ScreenSize;
float depth = DepthBuffer.Sample(DepthBuffer_Sampler, stc).x;
float4 H;
H.x = DepthBuffer.Sample(DepthBuffer_Sampler, stc - float2(1 / ScreenSize.x, 0)).x;
H.y = DepthBuffer.Sample(DepthBuffer_Sampler, stc + float2(1 / ScreenSize.x, 0)).x;
H.z = DepthBuffer.Sample(DepthBuffer_Sampler, stc - float2(2 / ScreenSize.x, 0)).x;
H.w = DepthBuffer.Sample(DepthBuffer_Sampler, stc + float2(2 / ScreenSize.x, 0)).x;
float2 he = abs(H.xy * H.zw * rcp(2 * H.zw - H.xy) - depth);
float3 hDeriv;
if (he.x > he.y)
hDeriv = Calculate horizontal derivative of world position from taps | * | y |
else
hDeriv = Calculate horizontal derivative of world position from taps | x | * |
float4 V;
V.x = DepthBuffer.Sample(DepthBuffer_Sampler, stc - float2(0, 1 / ScreenSize.y)).x;
V.y = DepthBuffer.Sample(DepthBuffer_Sampler, stc + float2(0, 1 / ScreenSize.y)).x;
V.z = DepthBuffer.Sample(DepthBuffer_Sampler, stc - float2(0, 2 / ScreenSize.y)).x;
V.w = DepthBuffer.Sample(DepthBuffer_Sampler, stc + float2(0, 2 / ScreenSize.y)).x;
float2 ve = abs(V.xy * V.zw * rcp(2 * V.zw - V.xy) - depth);
float3 vDeriv;
if (ve.x > ve.y)
vDeriv = Calculate vertical derivative of world position from taps | * | y |
else
vDeriv = Calculate vertical derivative of world position from taps | x | * |
return normalize(cross(hDeriv, vDeriv));
}
```


*Feb 16 Update*: The `he`

and `ve`

in above code are so calculated because we need to do perspective correct interpolation here, i.e, interpolating on 1/depth instead of depth.

At last I need to say that this *accurate method* may still fail on tiny triangles, but it’s rarely noticeable. We’ve used this technique in decal rendering for years, our artists never complain about any artifact. Hope you find it useful.

For reference, Ben Golus [implemented this technique in Unity](https://gist.github.com/bgolus/a07ed65602c009d5e2f753826e8078a0), as well as the *improved method*. His implementation takes non-linear depth values so the interpolation part is slightly different (see the comment below). iq also have a [shadertoy implemention](https://www.shadertoy.com/view/fsVczR) which assumes a linear depth buffer.

-
János Turánszki, “Improved normal reconstruction from depth”.

[https://wickedengine.net/2019/09/22/improved-normal-reconstruction-from-depth](https://wickedengine.net/2019/09/22/improved-normal-reconstruction-from-depth).[↩︎](https://atyuwen.github.io#fnref:1)[↩︎](https://atyuwen.github.io#fnref1:1) -
Emil Persson. “Second-Depth Antialiasing”. In GPU Pro 4, A K Peters, 2013, pp. 201–212.

[↩︎](https://atyuwen.github.io#fnref:2)[↩︎](https://atyuwen.github.io#fnref1:2)