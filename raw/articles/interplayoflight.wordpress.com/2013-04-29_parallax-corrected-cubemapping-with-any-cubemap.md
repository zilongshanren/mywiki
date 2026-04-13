---
title: Parallax-corrected cubemapping with any cubemap
url: https://interplayoflight.wordpress.com/2013/04/29/parallax-corrected-cubemapping-with-any-cubemap/
author: Kostas Anagnostou
published: '2013-04-29'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Recently I was using a parallax corrected cubemapping technique to add some glass reflections to a project (you can read about parallax corrected cubemapping in this[ excellent writeup](http://seblagarde.wordpress.com/2012/09/29/image-based-lighting-approaches-and-parallax-corrected-cubemap/)). In general, doing planar reflections with cubemaps is not that easy, the cubemap is considered “infinite” and since it is accessed only with the reflection vector it has no notion of location (that means it does not register well with the scene, it seems detached from it and the reflections do not correspond to actual scene items/features).

The basic idea behind the parallax corrected cubemapping technique is to add this missing position/locality to the cubemap by “fitting” it to a bounding box that surrounds a scene (or part of it, you can use and blend more cubemaps if needed). For this to work well though, the cubemap must have been generated specifically for this part of the scene, taking its dimensions into consideration. Trying to fit a generic cubemap to any scene will not work well.

In my case I needed to quickly add some general reflections to the glass, the main requirement was that they should not float and sort of take the camera motion in the room into consideration. Parallax corrected cubemapping is very suitable for this, my only problem was that I did not have but a generic, blurry, cubemap to use. The room to apply the cubemap to was not a “cube” (the z dimension was double that of x, and the y dimension was half that of x) and in the end all I got was some ugly warped (but parallax correct :-) ) reflection effects.

A quick fix to this was to take the non uniform dimensions of the room (bounding box) into consideration when calculating the parallax corrected reflection vector. The code from the [original article](http://seblagarde.wordpress.com/2012/09/29/image-based-lighting-approaches-and-parallax-corrected-cubemap/) was:

float3 DirectionWS = PositionWS - CameraWS; float3 ReflDirectionWS = reflect(DirectionWS, NormalWS); // Following is the parallax-correction code // Find the ray intersection with box plane float3 FirstPlaneIntersect = (BoxMax - PositionWS) / ReflDirectionWS; float3 SecondPlaneIntersect = (BoxMin - PositionWS) / ReflDirectionWS; // Get the furthest of these intersections along the ray // (Ok because x/0 give +inf and -x/0 give –inf ) float3 FurthestPlane = max(FirstPlaneIntersect, SecondPlaneIntersect); // Find the closest far intersection float Distance = min(min(FurthestPlane.x, FurthestPlane.y), FurthestPlane.z); // Get the intersection position float3 IntersectPositionWS = PositionWS + ReflDirectionWS * Distance; // Get corrected reflection ReflDirectionWS = IntersectPositionWS - CubemapPositionWS; // End parallax-correction code return texCUBE(envMap, ReflDirectionWS);

The scale due to non-cube bounding box dimensions was calculated as following:

float3 BoxDiff = (BoxMax - BoxMin); float minDim = min(BoxDiff.z, min(BoxDiff.x, BoxDiff.y)); float3 BoxScale = minDim / BoxDiff;

and finally the corrected reflection vector was scaled by BoxScale just before sampling the cubemap:

ReflDirectionWS *= BoxScale;

With this small trick any cubemap can be used along with the parallax corrected cubemapping technique (the cubemap will still not match the contents of the scene of course, but at least it won’t seem detached).

Hey,

I am not sure I get your point or maybe I misunderstand the post. The original code currently work for any kind of AABB box, mean not only cube.

On the original article I also provide code for OBB (also non uniform) which work even for not centered box (i.e pivot not at 0.0).

Cheers

It does indeed, for cubemaps generated for a specific scene, regardless of the dimensions of the room. When you generate a custom cubemap for a scene it takes into consideration the uneven dimensions of the scene nicely (by compressing them into a cube) and the code in the original article just works (by uncompressing to the original dims of the bounding box).

What I found though is that when you try to use the code for a cubemap that was not generated specifically for the scene it warps the cubemap and it does not cover the bounding box correctly (as expected — I know that the original method wasn’t intended to be used like that). This small addition just stretches the cubemap so as to cover the whole bounding box. Hacky technique, that solved a specific problem I had, thought I’d share it.

Thank you for the very interesting articles BTW, keep up the good work!

Ok, I get it. Thank you for the tips :)