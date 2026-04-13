---
title: Texture Effects with Polar Coordinates
url: https://www.vertexfragment.com/ramblings/polar-coordinates/
author: Steven Sell
published: '2024-02-28'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/3bc58a68417e31f1.gif)


[Overview](https://www.vertexfragment.com#overview)[The Wrong Road](https://www.vertexfragment.com#the-wrong-road)[Course Correction](https://www.vertexfragment.com#course-correction)[On the Right Path](https://www.vertexfragment.com#on-the-right-path)[But What About the Water Ring?](https://www.vertexfragment.com#but-what-about-the-water-ring)[Source Code](https://www.vertexfragment.com#source-code)

Recently a lot of my time has been spent working on visual effects for *Beyond the Storm*. Those flashy (or not so flashy) little details, and not the gargantuan visual tasks such as terrain, water, sky, etc. One effect that proved more difficult than originally anticipated was creating water rings resulting from footsteps in shallow water.

As usual, *Breath of the Wild* serves as a constant inspiration for this project due to the similar-ish stylized visuals. I swear, it’s not the only thing that is serving as inspiration ([that volumetric fog](https://www.vertexfragment.com/ramblings/urp-volumetric-fog/) in *Elden Ring* …).

In BotW the effect is composed of approximately three different components: two particle systems (one large textured splash, one small circle emitter), and the expanding ring. And it is that ring which I failed to replicate several times until I remembered about *polar coordinates*.

As usual, I like to begin with what didn’t work when trying to replicate these effects. It is in these journeys that we truly learn and expand our knowledge, and even though this approach was wrong it did produce interesting results and also played a role in the final effect. *Journey Before Destination*, and all of that.

If you watch the effect play out in BotW it is quite simple: a ring which expands outwards and fades away. There are some undulations to it, and it breaks apart, but those shouldn’t be too hard to achieve, right? And that is where I began.

**Fragment Shader (HLSL)**

```
CBUFFER_START(UnityPerMaterial)
float4 _RingDimensions; // (Radius Min, Radius Max, Thickness Min, Thickness Max)
float _TimeOverride; // Time on range [0, 1] for development purposes.
FragMain(VertOutput input) : SV_Target
{
float fade01 = EaseOutQuadratic(_TimeOverride);
float ringRadius = lerp(_RingDimensions.x, _RingDimensions.y, fade01);
float ringThickness = lerp(_RingDimensions.w, _RingDimensions.z, fade01);
float ringDistance = distance(input.uv.xy, float2(0.5f, 0.5f));
float ring = saturate(abs(ringDistance - ringRadius) / ringThickness);
return float4(ring.xxx, 1.0f);
}
```


This gives [the basic SDF](https://iquilezles.org/articles/distfunctions2d/) for a ring, as shown below.

![](../../assets/23ccb5091d0ca7b1.png)


Which can then be sharpened with a little `pow`

er.

` float ring = pow(saturate(abs(ringDistance - ringRadius) / ringThickness), 16.0f);`


![](../../assets/a6d3a341e4554055.png)


So now that we have a water ring, which expands and fades when played, how do we add the undulations or ripples?

This can be accomplished by adjusting the distance to the ring, using three new control parameters: `_RingWaveStrength`

, `_RingWaveLength`

, and `_RingWaveSpeed`

. By using `sin`

(or `cos`

if that is more your speed), we get smooth waves along the ring. In motion these ripples also move thanks to the adjustment to the UV being sampled.

```
float2 ringUV = input.uv.xy + _Time.y * _RingWaveSpeed;
ringDistance += _RingWaveStrength * (sin(ringUV.x * _RingWaveLength) + sin(ringUV.y * _RingWaveLength));
```


![](../../assets/5c0da7edd7e24eeb.png)


It’s a neat effect, and other cool visuals can be achieved by messing around with the input parameters. However, it’s not suitable for a water ring, at least not one that replicates the effect in BotW. There are two main shortcomings with it when compared against the reference source: the fade of the ring is uniform, and there is a single constant ring. In the reference work the fade is non-uniform, likely resulting from the introduction of some noise and the ripple ring can also break apart and/or there can be multiple ripples at once.

At this point my head was firmly stuck in SDF-land and I kept tweaking and adjusting the ring formulas. I accomplished breaking the ring apart into multiple pieces, and applying some noise influence on the fade but nothing looked quite right. So at this point I threw in the towel and went to search how other people approached the problem.

As it turns out the water footstep rings are not a highly discussed effect from BotW. [Much like with my exploration of their puff particles](https://www.vertexfragment.com/ramblings/stylized-puff-particles/), I was on my own.

There is [this effect tutorial by Gabriel Aguiar](https://www.youtube.com/watch?v=_H8gBKGKbnU) where part of his final effect has what we are looking for. Unfortunately it’s a step not covered in the free video, however it did put my head back onto the right path. At one point in the tutorial he creates a circle in Blender and rearranges the UVs so that all exterior vertices are at `uv.y = 0`

and all inner vertices are at `uv.y = 1`

. Once setup in this manner, the texture can simply be translated up/down along the UVs and the result is it emanating from the center of the circle.

While a neat way to achieve the effect, it is very limited. It is only usable on meshes who have had their UVs aligned in such a specific manner, and the mesh itself must be circular. It is definitely an approach for a technical artist who does not have shader programming knowledge and/or is limited to shader node graphs.

However for those of us with access to shader programming we can harness the power of *polar coordinates*!

Polar coordinates are an alternative coordinate system, as opposed to the cartesian coordinates the majority of us are more familiar with. Like cartesian coordinates, a polar coordinate is measured from some origin of your choosing. With cartesians this is typically the bottom-left corner of the image/screen (or top-left in Windows land), but with polar this typically is the center point.

The coordinate itself is two-dimensional and is represented by an angle and distance to that center point: \( (r, \theta) \), where the angle lies on the range \( [-\pi, \pi] \). For graphics purposes it isn’t uncommon to convert the angle to a more “usable” range such as \( [-1, 1] \), \( [-0.5, 0.5] \), or even \( [0, 1] \). The important thing is that you (and your code) is consistent.

Previously throughout my code I was storing polar coordinates as \( (\theta, r) \) and not \( (r, \theta) \). Again, it doesn’t really matter so long as you are consistent, but it’s also important to be consistent with the *rest of the world*. These mistakes *can* make cool effects though. As Mr. Ross calls them, happy little accidents.

![](../../assets/0124e6d366424e66.png)


The above is from the expanding ring effect (shown at the top of the ramble) before updating it to the corrected convention. It’s pretty neat looking.

As polar coordinates are a key part of trigonometry, I will not go into much depth regarding them as there are literal textbooks on the subject. However, for graphics one of the most important functions is converting cartesian to polar (and back again) as we typically work with UVs, world-space coordinates, etc.

**Cartesian to Polar**

```
/**
* Returns the polar coordinate of the specified coordinates.
* The returned polar coordinate is (distance, angle) from the origin.
* The angle is on the range [-PI, PI].
*/
float2 CartesianToPolar(float2 cartesian, float2 origin)
{
float2 atOrigin = cartesian - origin;
float dist = length(atOrigin);
float angle = atan2(atOrigin.y, atOrigin.x);
return float2(dist, angle);
}
/**
* Returns the UV coordinate converted to polar coordinates, assuming an origin of (0.5, 0.5).
*/
float2 UVToPolar(float2 uv)
{
return CartesianToPolar(uv, float2(0.5f, 0.5f));
}
```


**Polar to Cartesian**

```
/**
* Returns the polar coordinate on the range [-PI, PI] around the provided polar origin
* to cartesian coordinates at the origin (0, 0).
*/
float2 PolarToCartesian(float2 polar, float2 origin)
{
float2 cartesian = float2(cos(polar.y), sin(polar.y)) * polar.x;
return (cartesian + origin);
}
/**
* Returns the polar coordinates on the range [-PI, PI] around the origin (0.5, 0.5)
* to cartesian coordinates at the origin (0, 0).
*/
float2 PolarToUV(float2 polar)
{
return PolarToCartesian(polar, float2(0.5f, 0.5f));
}
```


Note that there is a slight error introduced when converting cartesian → polar → cartesian due to floating point accuracy. This error, though small as it is, can be visualized.

```
float4 FragMain(VertOutput input) : SV_Target
{
float2 uvAsPolar = UVToPolar(input.uv.xy);
float2 polarAsUV = PolarToUV(uvAsPolar);
return float4(abs(polarAsUV - input.uv.xy) * _ErrorMagnifier, 0.0f, 1.0f);
}
```


![](../../assets/004706b1350d2652.png)


Now that we have discussed my mistakes, lets get back on track with replicating that simple expanding ring effect.

Let’s begin by simply sampling a tileable noise texture using our UV coordinates converted to polar coordinates.

```
float4 FragMain(VertOutput input) : SV_Target
{
float2 polar = CartesianToPolar((input.uv.xy * _UVScale), float2(0.5f, 0.5f) * _UVScale);
float sampled = SAMPLE_TEXTURE2D(_Texture, sampler_Texture, polar.yx).r;
return float4(sampled.xxx, 1.0f);
}
```


![](../../assets/41df97118be2921c.png)


You may notice a discontinuity at angle \( 0 \) on the polar sampled images. This is “normal” and can be alleviated through better tiling noises and further image adjustments, especially motion. Speaking of motion, we can add some to make the noise expand out from the origin and spin by simply modifying the polar coordinate based on time.

```
polar.y = (polar.y + PI) * ONE_OVER_TWO_PI; // Convert from [-PI, PI] to [0, 1]. This causes a swirl and helps hide the discontinuity.
-= _Time.y * _MovementSpeed;
polar.y += _Time.y * _RotationSpeed;
```


![](../../assets/bf90568a044fd069.gif)


We now have a nice swirling, expanding noise that can be broken into rings. The trick is to select only a portion of our noise, and that is where the accident from earlier with the SDFs come into play. Those SDF rings are a perfect solution for extracting out some of the noise.

```
float fade01 = EaseOutQuadratic(frac(_Time.y / _FadeDuration));
// _RingDimensions is (Min Radius, Max Radius, Min Thickness, Max Thickness)
float ringRadius = lerp(_RingDimensions.x, _RingDimensions.y, fade01);
float ringThickness = lerp(_RingDimensions.w, _RingDimensions.z, fade01);
// Can't use polar.x due to its use of _UVScale, so have to recalculate the distance.
float ringDistance = distance(input.uv.xy, float2(0.5f, 0.5f));
float ring = 1.0f - pow(saturate(abs(ringDistance - ringRadius) / ringThickness), _RingSoftness);
return float4(ring.xxx, 1.0f);
```


![](../../assets/0c8c7cc29acf2740.gif)


*time*. Easings are functions that interpolate over that range, and are always handy to have in your math utilties (both on the GPU and the CPU).

For example `EaseOutQuadratic`

is implemented as:

```
float EaseOutQuadratic(float x)
{
return 1.0f - pow(1.0f - x, 2.0f);
}
```


A list of various easing functions, and their examples, can be found at [https://easings.net/](https://easings.net/)

Now let’s combine the polar sampled noise with the SDF ring.

```
float final = (sampled * ring);
return float4(final.xxx, 1.0f);
```


![](../../assets/2c83d062281b0a12.gif)


We are almost there! The last step is something that I have noticed in numerous BotW effects, and that is a time-based dissolve. This is very similar to what I detailed in my stylized puff particle ramble. We simply subtract the current time fade value (on the range \( [0, 1] \)) from our `final`

value. This makes it so that as the effect progresses, only the highest points of the noise are visible causing the rest of it to fade or dissolve away.

Additionally I use a `_FinalStrength`

modifier which can be used to increase the hardness of the final result.

`final = saturate((final - fade01) * _FinalStrength);`


![](../../assets/a65f67c0a05e5cbb.gif)


Add on some HDR tint (and make sure your bloom post-process volume is enabled) and baby, you’ve got a stew going.

![](../../assets/4b298c8f92233175.gif)


Yes I did start this ramble talking about water rings and *Breath of the Wild*. And yes, I never showed a water ring or even technically worked up to one. And the simple truth is that water rings, even the ones in BotW, don’t really screenshot well.

They are typically, by design, small and fairly subtle effects. You never really want to draw attention to them. But they still need to fit the rest of the art style and look decent when someone finally does notice them. Now bright flashy effects, those show up well and that is why the examples make use of them.

But if you *really* want to see one, here you go.

![](../../assets/df985095326d6315.png)


I also titled this ramble *Texture Effects with Polar Coordinates* and proceeded to only show a single effect. And again the truth is a lot of this is found through trial and error and self-discovery. A compendium of different effects, caused by slight tweaks here and there, could be made. But practically it is of no use. Even the texture being sampled makes a huge difference in the final result.

It is important to note that polar coordinates do have a plethora of other uses. For example, my raymarch volumetric clouds (buzzwords!) are rendered to an offscreen render texture using polar coordinate sampling. Using polar coordinates in this way allows them to be projected onto a hemispherical mesh.

![](../../assets/2461d506f944d2c0.png)


Below is the source for the fragment shader program used to generate the example images in this ramble.

As usual it is written for Unity, but can be easily adapted to any other framework.

```
// -----------------------------------------------------------------------------------------
// Utilities
// -----------------------------------------------------------------------------------------
#ifndef PI
#define PI 3.141592f
#endif
#ifndef ONE_OVER_TWO_PI
#define ONE_OVER_TWO_PI 0.159155f
#endif
/**
* See https://easings.net/
*/
float EaseOutQuadratic(float x)
{
return 1.0f - pow(1.0f - x, 2.0f);
}
/**
* Returns the polar coordinate of the specified coordinates.
* The returned polar coordinate is (distance, angle) from the origin.
* The angle is on the range [-PI, PI].
*/
float2 CartesianToPolar(float2 cartesian, float2 origin)
{
float2 atOrigin = cartesian - origin;
float dist = length(atOrigin);
float angle = atan2(atOrigin.y, atOrigin.x);
return float2(dist, angle);
}
/**
* Returns the UV coordinate converted to polar coordinates, assuming an origin of (0.5, 0.5).
*/
float2 UVToPolar(float2 uv)
{
return CartesianToPolar(uv, float2(0.5f, 0.5f));
}
// -----------------------------------------------------------------------------------------
// Fragment
// -----------------------------------------------------------------------------------------
FragMain(VertOutput input) : SV_Target
{
// -------------------------------------------------------------------------
// Polar Sampled Texture
// -------------------------------------------------------------------------
= CartesianToPolar((input.uv.xy * _UVScale), float2(0.5f, 0.5f) * _UVScale);
polar.y = (polar.y + PI) * ONE_OVER_TWO_PI; // Convert from [-PI, PI] to [0, 1]. This causes a swirl and helps hide the discontinuity.
-= _Time.y * _MovementSpeed;
polar.y += _Time.y * _RotationSpeed;
float sampled = pow(SAMPLE_TEXTURE2D(_Texture, sampler_Texture, polar.yx).r, _Smoothness);
// -------------------------------------------------------------------------
// SDF Expanding Ring
// -------------------------------------------------------------------------
float fade01 = EaseOutQuadratic(frac(_Time.y / _FadeDuration));
float ringRadius = lerp(_RingDimensions.x, _RingDimensions.y, fade01);
float ringThickness = lerp(_RingDimensions.w, _RingDimensions.z, fade01);
float ringDistance = distance(input.uv.xy, float2(0.5f, 0.5f)); // Can't use polar.y due to its use of _UVScale.
float ring = 1.0f - pow(saturate(abs(ringDistance - ringRadius) / ringThickness), _RingSoftness);
// -------------------------------------------------------------------------
// Final Output
// -------------------------------------------------------------------------
float final = saturate(((sampled * ring) - fade01) * _FinalStrength);
return float4(final.xxxx) * _Tint;
}
```