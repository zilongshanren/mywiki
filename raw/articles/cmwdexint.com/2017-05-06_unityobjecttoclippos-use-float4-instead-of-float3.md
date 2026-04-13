---
title: UnityObjectToClipPos(use float4 instead of float3)
url: https://cmwdexint.com/2017/05/06/unityobjecttoclipposuse-float4-instead-of-float3/
author: Ming Wai Chan
published: '2017-05-06'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

In the past, we uses `mul(UNITY_MATRIX_MVP, v.vertex)`

to convert vertex position from local to world space. *v.vertex* is *float4* which has w component.

But in most cases w is = 1. To make vertex shader run faster, Unity replaced it with `UnityObjectToClipPos(float3 pos)`

, which ignores w component even you pass a *float4* position instead of *float3*.

For some advanced users who still need the w component in their custom shaders, here is a cheaper **UnityObjectToClipPos() **function which respects the w component!😄

`// More efficient than computing M*VP matrix product`


inline float4 UnityObjectToClipPosRespectW(in float4 pos)

{

return mul(UNITY_MATRIX_VP, mul(unity_ObjectToWorld, pos));

}