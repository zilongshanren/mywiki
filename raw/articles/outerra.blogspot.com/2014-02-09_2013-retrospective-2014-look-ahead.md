---
title: 2013 Retrospective, 2014 Look Ahead
url: https://outerra.blogspot.com/2014/02/2013-retrospective-2014-look-ahead.html
author: Outerra
published: '2014-02-09'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

- enhanced terrain texturing, terrain normal maps
[dynamic and adjustable time flow](http://www.youtube.com/watch?v=Xw0LuP5l0Js)[random rocks](http://www.youtube.com/watch?v=gUl15PXPc8M)[realtime terrain deformation - craters](http://www.youtube.com/watch?v=lRpkj4HXF40)[MiG 29](http://www.youtube.com/watch?v=jVoNMhH_j3Y)- support for
[Oculus Rift](http://www.youtube.com/watch?v=2LPPdV2Md1c), stereoscopic rendering modes [FreeTrack](http://www.youtube.com/watch?v=dJFJiGZo6uw)support, can be optionally combined with Rift, 3rd party TrackIR plugin support[watercraft](http://www.youtube.com/watch?v=OxVUC65uBmw)support, amphibious vehicles support- FBX importer, export of models in self-installing OTX format
- first level biome support:
[biome colors and vegetation density](http://www.youtube.com/watch?v=OJUPdABgsrA) - built-in Y4M/WebM video capture
- initial support for Intel 4000+ Graphics (Ivy Bridge and newer, in close cooperation with Intel OpenGL team)

**What's been happening behind the scenes**

Outerra engine is in its current state already used in several special simulation projects, and thus a lot of coding went into the support, custom features and the API for use by these projects. We can't disclose many details until these projects are officially revealed, but here's something that we can show: a video showing OT in one such project, where it is used (apart from other things) to render a full 360° dome using 2x8 FullHD projectors:

The whole setup used several computers linked together in a LAN, three of which were used to render the dome - two of them driving 2x3 projectors (5760x2160 screen on R7970) , and one the remaining 2x2. Several additional networked computers were used for other displays used within the simulator, including a smaller dome in front of aircraft cockpit.

![]() |

![](../../assets/275d1fdc6f2ee155.jpg)

![](../../assets/275d1fdc6f2ee155.jpg)

There's of course a lot more stuff being developed for this side, and most of it will also ultimately get into the public Outerra version.

**Upcoming updates**

Several features are in various stages of completion and going to be released progressively in public builds of the Outerra Tech Demo.

**Material rendering enhancements, environment reflections**

Material rendering in Outerra has been further enhanced, adding environment reflections and completing the physically based lighting implementation. At the moment it works only on objects; terrain needs some extra work to be able to use it.

Material news/fixes:

- Blinn-Phong BRDF model with Schlick fresnel approximation
- prefiltered cubemap for environment reflection
- irradiance map computed from environment used for ambient light (needs a few improvements)
- fixed environment reflection and ambient intensity for objects (terrain needs more work)
- fixed transparency shader (TODO alpha masked geometry)
- fixed metallic materials
- a few performance optimizations

Another important feature in the works is an in-game material editor, that will allow tuning the materials without having to edit the material file outside and restart.

**Water rendering enhancements, foam**

Ocean rendering is still a weak part in OT, with several updates and TODO's on the way. This time the sun and sky reflections were enhanced, as well as adding a basic foam after the boats.

Obviously missing are the wake effects, reflections of boats and terrain in the water. The water is also quite patterned, as it's currently made just of several waves summed together.

The boats feel lighter than they are because the models currently use just 2 sampling points that compute the hydro forces, so any wave bump that happens to act directly on the sampling point behaves as if it was much larger and acting on half of the boat.

**Characters, animations**

True FPS/TPS modes are finally coming in the next update, replacing the existing "stick to terrain" free-camera mode. We are using animations from a commercial package so not everything fits
as it should yet, it's more a proof of the concept for us to test the whole animation
system and the FPS/TPS mode.

Features/issues:

Features/issues:

- dual-quaternion skinning, it preserves mesh volume in deformation (TODO linear skinning)
- animation system is using a simple blending; sometimes a leg or arms are not properly synchronized and this part needs some additional work
- current mercenary model has 81 bones, including the face bones.

With the new characters and object rendering changes we also did a bit of profiling and improving the performance of rendering for larger numbers of objects.


This includes:

This includes:

- improved draw call performance
- a few CPU side optimizations to free the CPU but it still needs a bunch more, because it's not as efficient as we'd like (especially on older CPUs)
- utilized instanced draw calls; if the same object is used multiple times it's hyper fast, although the triangle count is still the limiting factor, the rendering won't be stalled by the draw call overhead (which still exists even in OpenGL and especially on AMD hardware)
- improved shadowmap performance (especially for NV hardware), shadow culling algorithm needs additional work, current implementation is rather naive and sometimes buggy, but it's the first required step to get the terrain self-shadowing to work

**Clouds**

You may have seen

[early development images from the clouds implementation](http://forum.outerra.com/index.php?topic=2148.0)on the forums already:

Some info about the implementation:

- clouds are volumetric, generated from noise with a variable threshold that allows to alter % of cloud cover
- the screens above are showing just the volumes, without a finer cloud mask applied that will provide additional detail especially up close
- it's designed so that there can be a rougher global cloud map used in the future, defining the local cloud density
- currently uses just a single layer of clouds, but can use multiple ones
- the cloud rendering back-end is suitable also for things like contrails and rocket trails

**OSM roads, buildings**

Many people aren't content with the pristine unspoiled world, and are asking about getting all the civilization stuff in. Since OT can overlay vector data over the procedurally generated terrain, and the existing road engine generates the roads from vector data, import of an existing vector database of roads and other data will be possible as well.

[OpenStreetMap](http://www.openstreetmap.org/)is one of the possible sources for the road data and much more - rivers, fields, artificial forests and parks, building footprints etc. The roads and rivers will be the first to import, after the engine exposes interfaces for import plugins, allowing programmatical creation of OT roads and other entities. Import process will produce binary files usable directly by the terrain generator. The format is probably not going to be published - it's likely to change as the engine evolves, and for example right now the data even cannot be generated without knowing some of the data from the internal engine structures representing the terrain.

Some of the internal features being developed to handle the needs in this area:

- extended road system capabilities - separate properties for the left/right side, configurable road profiles, markings
- seamless road joins, splits (the existing data format puts some limitations on it)
- "river bed" road profiles and river water surface shaders
- polygonal vector mode for larger overlays - large rivers with well defined bank shapes, lakes, but also for fields, pastures, artificial trees or tree removal, terrain leveling etc

**Multiple lighting sources, terrain self-shadowing**

In Catalyst 13.12 AMD has implemented the

[OpenGL extension](http://www.opengl.org/registry/specs/NV/depth_buffer_float.txt)we needed to be able to

[handle planetary distances more efficiently](http://2012/11/maximizing-depth-buffer-range-and.html), and ultimately allowing us to implement better solution especially for the multiple lights rendering. The upcoming update will automatically switch to the new mode if it finds the extension, and people with AMD cards are advised to update to the latest driver version.

It's likely that every AMD/ATI card owner will have to update to version 13.12 or better, since our recent rendering pipeline updates seem to have uncovered some kind of a bug in earlier driver versions, that causes missing terrain shadows or abysmal performance when the shadows are enabled.

There are similar issues with older Nvidia drivers: Quadro users need to update to newer drivers to resolve a weird lighting issue, and some older mobile graphics drivers have the problem as well. We try to add the known problematic driver versions into a bad driver list that is checked upon start, but in any case, whenever you encounter missing shadows or unusual issues with the lighting, please update your graphics drivers first.

**Mars**

Apart from Earth and the Middle-Earth planet (done by

[ME-DEM project](http://www.me-dem.me.uk/)folks), there soon can be a new planet available - Mars. Below is the first screenshot from a testing run. The Mars there is with its canyons flooded and an earthly atmosphere:

There are several issues that need to be addressed. Mars data have considerably lower resolution, approximately 500m. While OT will procedurally refine the data down to the ground level anyway, its algorithms were so far tuned for details below 100m, so it needs a new profile for Mars.

There are other issues, as you can see on the screen, there's a ghosting on the craters - it's because the elevation and color data do not match up. I'm not sure where the longitudinal offset comes from yet. The color map is of quite poor quality in general; craters have baked-in lighting that should be removed as the lighting is handled in real time. Also, the colors were apparently run through some odd filters that made the ice caps pink; white balancing helps that but the texture ends up being acid yellowish.

For Mars to work nicely we have to fix all of the above, and also separate the individual planet configuration data, as at the moment they are global.

**Other news**

We did a lot of demoing and presentations in the past year and got into several projects that now allow us to grow and speed up the development. In addition to working with dedicated development teams on special simulation projects based on Outerra, we will be also expanding our core team here in Bratislava, Slovakia. New people are expected to work mainly on the import tools, server side back-end and on the UI, replacing our programmer's design.

The breadth of the scope of possible Outerra applications is huge, and we are also investigating other possibilities to launch development of other OT-based projects. A hot candidate is a unified simulator platform with the primary initial focus on a flight simulator, as it makes the largest group of inquiries we are getting. This would mean a dedicated development team working closely with the core, and in cooperation with content makers working on scenery, aircraft, simulation cores for flight and other types of vehicles.

In any case, a project of this scale would require a sufficient funding, and so we are currently discussing the development of a prototype usable for launching a Kickstarter funding campaign with several interested developers.

## No comments:

Post a Comment