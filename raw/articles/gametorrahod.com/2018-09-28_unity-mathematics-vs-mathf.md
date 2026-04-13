---
title: Unity.Mathematics vs Mathf.
url: https://gametorrahod.com/unity-mathematics-vs-mathf/
author: Sirawat Pitaksarit
published: '2018-09-28'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Unity’s Mathf is not 100% replacable with its burst-friendly Unity.Mathematics . Also Unity.Mathematics evolves all the time. By now you are reading this something might have changed.

## Quaternion is available for use in jobs

quaternion type it in small q like this. It is in Unity.Mathematics

## LookRotation’s difference

This is the result from the same input :

**Quaternion.LookRotation (with Vector3)**

`Look (-1.6, 61.3, 162.4) Up (0.5, -0.9, 0.0) QuatWXYZ -0.2552253 0.04192121 0.1746541 0.9500519`


Unity prints Vector3 like that but actually the number is in floating point position and contains more digits.

**quaternion.LookRotation (with float3)**

`Look float3(-1.648314f, 61.3083f, 162.3523f) Up float3(0.4771588f, -0.8788171f, 0f) QuatWXYZ -0.2451455 0.04013683 0.172545 0.9387675`


The difference :

```
Mathf -0.2552253 0.04192121 0.1746541 0.9500519
math. -0.2451455 0.04013683 0.1725450 0.93876750
```


This is actually because **math** ones** **expects a normalized vector! (No documentation or anything at all!)

## quaternion.AxisAngle expects a radian

Don’t be stupid like me and think “angle” = degree

## Where’s InverseLerp ?

It is called unlerp here. But! It is implemented without clamp and divide by 0 check.

Mathf ones works like this

```
public static float inverseLerp(float a, float b, float value)
{
if (a != b)
return math.clamp((value - a) / (b - a), 0, 1);
else
return 0.0f;
}
```


Unity.Mathematics ones works like this

```
[MethodImpl(MethodImplOptions.AggressiveInlining)]
public static float unlerp(float a, float b, float x) { return (x - a) / (b - a); }
```


So if you use a = b it will explode, if you use x outside of 0~1 range it linearly interpolate outside of a and b.

## SmoothStep’s difference

I have been tricked before, the definition of the last argument is not the same. That is, it is not 100% replacable.

![](../../assets/42ff199505ed7dab.png)

**Unity.Mathematics**: It is interpolated first before the clamp, the x value is expected to be**between edge values a~b**and not 0~1.**Mathf**: It is clamped first, the t value is expected to be**between 0~1**then maps smoothly with from~to.

Shader language’s smoothstep works like the Unity.Mathematics version.

For your information, the 0~1 input is the way Lerp / lerp function universally works shader language or not. The old Unity’s SmoothStep is lerp-like (not the school idols). The new smoothstep is more inline with the general definition.

## math.select(a, b, bool)

Which one do you think you get if the bool is true? I used to think like bool ? a : b but in a swapped order. That is wrong. Don’t be like me and spend 2 hours looking for bugs because of this.

Actually if the bool is false you get the first one. The good way to reason about this is that it “select” with a bit comparison. 0 comes before 1, and false is zero so you get the first one. Don’t think of a and b as true and false but as first and second.

## How to get just one bool from == operator?

I was comparing int2 to int2 and thought it would return one bool but no, it is a component-wise comparison and no matter what I do it returns bool2

![](../../assets/d3c38142b090b919.png)

To get just bool you have to use Equals

![](../../assets/dc57768a12213b5e.png)

(int2 is IEquatable<int2> but that does not necessary mean that == will use Equals method defined here)