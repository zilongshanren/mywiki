---
title: Instant Radiosity and light-prepass rendering
url: https://interplayoflight.wordpress.com/2013/03/21/instant-radiosity-and-light-prepass-rendering/
author: Kostas Anagnostou
published: '2013-03-21'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Global illumination (along with physically based rendering) is one of my favourite graphics areas and I don’t miss the opportunity to try new techniques every so often. One of my recent lunchtime experiments involved a quick implementation of [Instant Radiosity](http://www.liensberger.it/Web/Blog/wp-content/uploads/Instant_Radiosity_kl08.pdf), GI technique that can be used to calculate first bounce lighting in a scene, to find out how it performs visually.

The idea behind Instant Radiosity is simple, cast rays from a (primary) light into the scene and mark the positions where they hit the geometry. Then for each hit sample the surface colour and add a new point light (secondary light, often called Virtual Point Light – VPL) at the collision point with that colour. The point light is assumed to emit light in a hemisphere centred on the collision point and oriented towards the surface normal. Various optimisations can be added on top like binning VPLs that are close together to reduce the number of lights.

Typically Instant Radiosity creates a large number of point lights, a situation not ideal for forward rendered scenes. On the other hand [light-prepass engines](http://diaryofagraphicsprogrammer.blogspot.co.uk/2008/03/light-pre-pass-renderer.html) (and deferred shading engines although in this case the bandwidth requirements might increase due to the larger G-Buffer) are much better suited to handle large numbers of lights, and such an engine (Hieroglyph to be more specific) I used for my quick implementation.

To determine light ray-surface collisions, one can use CPU raycasting or a compute shader based GPU solution like Optix. In [this article](http://graphicsrunner.blogspot.co.uk/2011/03/instant-radiosity-using-optix-and.html?m=1) the use of Optix is described in the context of a deferred lighting engine with very good results. In my case, I opted for a coarser but simpler solution to find the light ray/scene intersections which involved rendering the scene from the point of view of the light and creating two low resolution textures storing world positions (a cheated a bit here as I should really store normals) and surface colour. In essence, each texel stores a new VPL to be used when calculating scene lighting. This approach is in fact quite similar to the [Reflective Shadowmaps](http://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0CDgQFjAA&url=http%3A%2F%2Fciteseerx.ist.psu.edu%2Fviewdoc%2Fdownload%3Fdoi%3D10.1.1.87.6346%26rep%3Drep1%26type%3Dpdf&ei=1x5LUZWWM8WEhQeriYHgBQ&usg=AFQjCNEoCgYa_rQjjpJL_5tesGCnqR6hkw&sig2=iANd3c0O41aeri7CF7pSng&bvm=bv.44158598,d.ZG4&cad=rja) technique, although in the context of the deferred lighting engine (in which lighting is done in one pass) I chose to store surface albedo and not surface radiance (or radiant flux as in the original paper).

For the purposes of my test, two 32×32 rendertargets storing world positions in the first and surface albedo on the second proved enough (resolution-wise). The following screenshot is the surface albedo as viewed from the directional light.

I am then feeding the two rendertargets as textures to the lighting pass shader directly to extract the Virtual Point Lights from. This has the advantage that I don’t have to read the textures back on the CPU to get the positions, gaining some performance increase. Hieroglyph performs lighting by calculating a quad for each light using a geometry shader and passing it to the pixel shader.

This is what the lightbuffer looks like after we render the bounced, point lights to it:

We can see the directional light being reflected from various surfaces, taking their albedo colour and lighting nearby objects.

Finally we use the lightbuffer to light the scene:

Once we add the surface albedo the bounced light colour becomes apparent. The radius of each VPL can be changed to cover more, or less area accordingly.

Moving the directional (primary) light does not seem to introduce any visible artifacts, although I’d imagine this is due to the low resolution of the reflective shadowmap, which means that VPLs are quite sparsely distributed.

This technique can be quite appealing as it is a straightforward way to add approximate first bounce lighting in a deferred, dynamically lit scene without adding any complexity, or actually modifying the lighting pass. There are some drawbacks; one, which is inherent to Instant Radiosity, is the fact that occlusion is not calculated for the VPLs meaning that light from the VPL can seem to penetrate a surface to reach areas that it shouldn’t. Determining occlusion for each VPL can be costly although it could probably be coarsely performed in screen space using the depth buffer. Directional and spot lights in the scene can easily be supported, not so for point lights which would require an[ onmi-directional shadowmap](http://http.developer.nvidia.com/GPUGems/gpugems_ch12.html) approach, or [dual paraboloid shadowmaps](http://graphicsrunner.blogspot.co.uk/2008/07/dual-paraboloid-shadow-maps.html) to cover the whole scene. Coloured lights are not supported in this instance since I am storing surface albedo and not radiance. To achieve this would essentially require two lighting passes, one for the primary light and one for the VPLs. Finally the number of primary scene lights must be quite low (or one ideally) due to the number of prepasses required to calculate the reflective shadowmap for each.

This was a quite rushed implementation to get a feel of how the technique works. I’d definitely like to revisit in it the future and improve it by storing normals and depth instead of world positions (so that bounched lights can indeed be hemispheres) and maybe try other primary light types.

In the meantime, if anyone wants to have a go, here is the [source code](http://sdrv.ms/10ngnXR). You’ll have to install [Hieroglyph](http://hieroglyph3.codeplex.com/) to get it working.