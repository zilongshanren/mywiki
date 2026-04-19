---
title: 'Stingray Renderer Walkthrough #8: stingray-renderer & mini-renderer'
url: https://bitsquid.blogspot.com/2017/03/stingray-renderer-walkthrough-8.html
author: Tobias
published: '2017-03-14'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

In the last [post](http://bitsquid.blogspot.com/2017/03/stingray-renderer-walkthrough-7-data.html) we looked at our systems for doing data-driven rendering in Stingray. Today I will go through the two default rendering pipes we ship as templates with Stingray. Both are entirely described in data using two `render_config`

files and a bunch of `shader_source`

files.

We call them the **“stingray renderer”** and the **“mini renderer”**

The “stingray renderer” is the default rendering pipe and is used in almost all template and sample projects. It’s a fairly standard “high-end” real-time rendering pipe and supports the regular buzzword features.

The `render_config`

file is approx 1500 lines of *sjson*. While 1500 might sound a bit massive it’s important to remember that this configuration is highly configurable, pretty much all features can be dynamically switched on/off. It also run on a broad variety of different platforms (mobile -> consoles -> high-end PC), supports a bunch of different debug visualization modes, and features four different stereo rendering paths in addition to the default mono path.

If you are interested in taking a closer look at the actual implementation you can download stingray and you’ll find it under `core/stingray_renderer/renderer.render_config`

.

Going through the entire file and all the implementation details would require multiple blog posts, instead I will try to do a high-level break down of the default [ layer_configuration](http://bitsquid.blogspot.se/2017/03/stingray-renderer-walkthrough-7-data.html) and talk a bit about the feature set. Before we begin, please keep in mind that this rendering pipe is designed to handle lots of different content and run on lots of different platforms. A game project would typically use it as a base and then extend, optimize and simplify it based on the project specific knowledge of the content and target platforms.

Here’s a somewhat simplified dump of the contents of the `layer_configs/default`

array found in `core/stingray_renderer/renderer.render_config`

in Stingray v1.8:

```
// run any render_config_extensions that have requested to insert work at the insertion point named "first"
{ extension_insertion_point = "first" }
// kick resource generator for rendering all shadow maps
{ resource_generator="shadow_mapping" profiling_scope="shadow mapping" }
// kick resource generator for assigning light sources to clustered shading structure
{ resource_generator="clustered_shading" profiling_scope="clustered shading" }
// special layer, only responsible for clearing hdr0, gbuffer2 and the depth_stencil_buffer
{ render_targets=["hdr0", "gbuffer2"] depth_stencil_target="depth_stencil_buffer"
clear_flags=["SURFACE", "DEPTH", "STENCIL"] profiling_scope="clears" }
// if vr is supported kick a resource generator laying down a stencil mask to reject pixels outside of the lens shape
{ type="static_branch" platforms=["win"] render_settings={ vr_supported=true }
pass = [
{ resource_generator="vr_mask" profiling_scope="vr_mask" }
]
}
// g-buffer layer, bulk of all materials renders into this
{ name="gbuffer" render_targets=["gbuffer0", "gbuffer1", "gbuffer2", "gbuffer3"]
depth_stencil_target="depth_stencil_buffer" sort="FRONT_BACK" profiling_scope="gbuffer" }
{ extension_insertion_point = "gbuffer" }
// linearize depth into a R32F surface
{ resource_generator="stabilize_and_linearize_depth" profiling_scope="linearize_depth" }
// layer for blending decals into the gbuffer0 and gbuffer1
{ name="decals" render_targets=["gbuffer0" "gbuffer1"] depth_stencil_target="depth_stencil_buffer"
profiling_scope="decal" sort="EXPLICIT" }
{ extension_insertion_point = "decals" }
// generate and merge motion vectors for non written pixels with motion vectors in gbuffer
{ type="static_branch" platforms=["win", "xb1", "ps4", "web", "linux"]
pass = [
{ resource_generator="generate_motion_vectors" profiling_scope="motion vectors" }
]
}
// render localized reflection probes into hdr1
{ name="reflections" render_targets=["hdr1"] depth_stencil_target="depth_stencil_buffer"
sort="FRONT_BACK" profiling_scope="reflections probes" }
{ extension_insertion_point = "reflections" }
// kick resource generator for screen space reflections
{ type="static_branch" platforms=["win", "xb1", "ps4"]
pass = [
{ resource_generator="ssr_reflections" profiling_scope="ssr" }
]
}
// kick resource generator for main scene lighting
{ resource_generator="lighting" profiling_scope="lighting" }
{ extension_insertion_point = "lighting" }
// layer for emissive materials
{ name="emissive" render_targets=["hdr0"] depth_stencil_target="depth_stencil_buffer"
sort="FRONT_BACK" profiling_scope="emissive" }
// kick debug visualization
{ type="static_branch" render_caps={ development=true }
pass=[
{ resource_generator="debug_visualization" profiling_scope="debug_visualization" }
]
}
// kick resource generator for laying down fog
{ resource_generator="fog" profiling_scope="fog" }
// layer for skydome rendering
{ name="skydome" render_targets=["hdr0"] depth_stencil_target="depth_stencil_buffer"
sort="BACK_FRONT" profiling_scope="skydome" }
{ extension_insertion_point = "skydome" }
// layer for transparent materials
{ name="hdr_transparent" render_targets=["hdr0"] depth_stencil_target="depth_stencil_buffer"
sort="BACK_FRONT" profiling_scope="hdr_transparent" }
{ extension_insertion_point = "hdr_transparent" }
// kick resource generator for reading back any requested render targets / buffers to the CPU
{ resource_generator="stream_capture_buffers" profiling_scope="stream_capture" }
// kick resource generator for capturing reflection probes
{ type="static_branch" platform=["win"] render_caps={ development=true }
pass = [
{ resource_generator="cubemap_capture" }
]
}
// layer for rendering object selections from the editor
{ type="static_branch" platforms=["win", "ps4", "xb1"]
pass = [
{ type = "static_branch" render_settings={ selection_enabled=true }
pass = [
{ name="selection" render_targets=["gbuffer0" "ldr1_dev_r"]
depth_stencil_target="depth_stencil_buffer_selection" sort="BACK_FRONT"
clear_flags=["SURFACE" "DEPTH"] profiling_scope="selection"}
]
}
]
}
// kick resource generators for AA resolve and post processing
{ resource_generator="post_processing" profiling_scope="post_processing" }
{ extension_insertion_point = "post_processing" }
// layer for rendering LDR materials, primarily used for rendering HUD and debug rendering
{ name="transparent" render_targets=["output_target"] depth_stencil_target="stable_depth_stencil_buffer_alias"
sort="BACK_FRONT" profiling_scope="transparent" }
// kick resource generator for rendering shadow map debug overlay
{ type="static_branch" render_caps={ development=true }
pass = [
{ resource_generator="debug_shadows" profiling_scope="debug_shadows" }
]
}
// kick resource generator for compositing left/right eye
{ type="static_branch" platforms=["win"] render_settings={ vr_supported=true }
pass = [
{ resource_generator="vr_present" profiling_scope="present" }
]
}
{ extension_insertion_point = "last" }
```


So what we have above is a fairly standard breakdown of a rendered frame, if you have worked with real-time rendering before there shouldn’t be much surprises in there. Something that is kind of cool with having the frame flow in this representation and pairing that with the hot-reloading functionality of `render_configs`

, is that it really encourages experimentations: move things around, comment stuff out, inject new resource generators, etc.

Let’s go through the frame in a bit more detail:

First of all there are a bunch of `extension_insertion_point`

at various locations during the frame, these are used by [ render_config_extensions](http://bitsquid.blogspot.se/2016/08/render-config-extensions.html) to be able to schedule work into an existing

`render_config`

. You could argue that an extensions system to the `render_configs`

is a bit superfluous, and for an in-house game engine targeting a specific industry that might very well be the case. But for us the extension system allows building features a bit more modular, it also encourages sharing of various rendering features across teams.```
// kick resource generator for rendering all shadow maps
{ resource_generator="shadow_mapping" profiling_scope="shadow mapping" }
```


We start off by rendering shadow maps. As we want to handle shadow receiving on alpha blended geometry there’s no simple way to reuse our shadow maps by interleaving the rendering of them into the lighting code. Instead we simply gather all shadow casting lights, try to prioritize them based on screen coverage, intensity, etc. and then render all shadows into two shadow maps.

One shadow map is dedicated to handle a single directional light which uses a cascaded shadow map approach, rendering each cascade into a region of a larger shadow map atlas. The other shadow map is an atlas for all local light sources, such as spot and point lights (interpreted as 6 spot lights).

```
// kick resource generator for assigning light sources to clustered shading structure
{ resource_generator="clustered_shading" profiling_scope="clustered shading" }
```


We separate local light sources into two kinds: “simple” and “custom”. Simple lights are either spot lights or point lights that don’t have a custom material graph assigned. Simple light sources, which tend to be the bulk of all visible light sources in a frame, get inserted into a [clustered shading acceleration structure](http://www.humus.name/Articles/PracticalClusteredShading.pdf).

While simple lights will affect both opaque and transparent materials, custom lights will only affect opaque geometry as they run a more traditional deferred shading path. We will touch on the lighting a bit more soon.

```
// special layer, only responsible for clearing hdr0, gbuffer2 and the depth_stencil_buffer
{ render_targets=["hdr0", "gbuffer2"] depth_stencil_target="depth_stencil_buffer"
clear_flags=["SURFACE", "DEPTH", "STENCIL"] profiling_scope="clears" }
// if vr is supported kick a resource generator laying down a stencil mask to reject pixels outside of the lens shape
{ type="static_branch" platforms=["win"] render_settings={ vr_supported=true }
pass = [
{ resource_generator="vr_mask" profiling_scope="vr_mask" }
]
}
```


Here we use the layer system to record a bind and a clear for a few render targets into a [ RenderContext](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-3-render.html) generated by the

[.](http://bitsquid.blogspot.se/2017/03/stingray-renderer-walkthrough-7-data.html)

`LayerManager`

Then, depending on if the `vr_supported`

render setting is true or not we kick a resource generator that marks in the stencil buffer any pixels falling outside of the lens region. This resource generator only does something if the renderer is running in stereo mode. Also note that the branch above is a `static_branch`

so if `vr_supported`

is set to false the execution of the `vr_mask`

resource generator will get eliminated completely during boot up of the renderer.

```
// g-buffer layer, bulk of all materials renders into this
{ name="gbuffer" render_targets=["gbuffer0", "gbuffer1", "gbuffer2", "gbuffer3"]
depth_stencil_target="depth_stencil_buffer" sort="FRONT_BACK" profiling_scope="gbuffer" }
{ extension_insertion_point = "gbuffer" }
// linearize depth into a R32F surface
{ resource_generator="stabilize_and_linearize_depth" profiling_scope="linearize_depth" }
// layer for blending decals into the gbuffer0 and gbuffer1
{ name="decals" render_targets=["gbuffer0" "gbuffer1"] depth_stencil_target="depth_stencil_buffer"
profiling_scope="decal" sort="EXPLICIT" }
{ extension_insertion_point = "decals" }
// generate and merge motion vectors for non written pixels with motion vectors in gbuffer
{ type="static_branch" platforms=["win", "xb1", "ps4", "web", "linux"]
pass = [
{ resource_generator="generate_motion_vectors" profiling_scope="motion vectors" }
]
}
```


Next we lay down the gbuffer. We are using a fairly fat “floating” gbuffer representation. By floating I mean that we interpret the gbuffer channels differently depending on material. I won’t go into details of the gbuffer layout in this post but everything builds upon a standard metallic PBR material model, same as most modern engines runs today. We also stash high precision motion vectors to be able to do accurate reprojection for TAA, RGBM encoded irradiance from light maps (if present, else irradiance is looked up from an IBL probe), high precision normals, AO, etc. Things quickly add up, in the default configuration on PC we are looking at 192 bpp for the color targets (i.e not counting depth/stencil). The gbuffer layout could use some love, I think we should be able to shrink it somewhat without losing any features.

We then kick a resource generator called `stabilize_and_linerize_depth`

, this resource generator does two things:

- It linearizes the depth buffer and stores the result in an R32F target using a
`fullscreen_pass`

. - It does a hacky TAA resolve pass for depth in an attempt to remove some intersection flickering for materials rendering after TAA resolve. We call the output of this pass
`stable_depth`

and use it when rendering editor selections, gizmos, debug lines, etc. We also use this buffer during post processing for any effects that depends on depth (e.g. depth of field) as those runs after AA resolve.

After that we have another more minimalistic gbuffer layer for splatting deferred decals.

Last but not least we kick another resource generator that calculates per pixel velocity for any pixels that haven’t been rendered to during the gbuffer pass (i.e skydome).

```
// render localized reflection probes into hdr1
{ name="reflections" render_targets=["hdr1"] depth_stencil_target="depth_stencil_buffer"
sort="FRONT_BACK" profiling_scope="reflections probes" }
{ extension_insertion_point = "reflections" }
// kick resource generator for screen space reflections
{ type="static_branch" platforms=["win", "xb1", "ps4"]
pass = [
{ resource_generator="ssr_reflections" profiling_scope="ssr" }
]
}
// kick resource generator for main scene lighting
{ resource_generator="lighting" profiling_scope="lighting" }
{ extension_insertion_point = "lighting" }
```


At this point we are fully done with the gbuffer population and are ready to do some lighting. We start by laying down the indirect specular / reflections into a separate buffer. We use a rather standard three-step fallback scheme for our reflections: screen-space reflections, falling back to localized parallax corrected pre-convoluted radiance cubemaps, falling back to a global pre-convoluted radiance cubemap.

The `reflections`

layer is the target layer for all cubemap based reflections. We are naively rendering the cubemap reflections by treating each reflection probe as a light source with a custom material. These lights gets picked up by a resource generator performing traditional deferred shading - i.e it renders proxy volumes for each light. One thing that some people struggle to wrap their heads around is that the resource generator responsible for running the deferred shading modifier isn’t kicked until a few lines down (in the `lighting`

resource generator). If you’ve paid attention in my previous posts this shouldn’t come as a surprise for you, as what we describe here is the *GPU* scheduling of a frame, nothing else.

When the reflection probes are laid down we move on and run a resource generator for doing Screen-Space Reflections. As SSR typically runs in half-res we store the result in a separate render target.

We then finally kick the `lighting`

resource generator, which is responsible for the following:

- Build a screen space mask for sun shadows, this is done by running multiple
`fullscreen_passes`

. The`fullscreen_passes`

transform the pixels into cascaded shadow map space and perform PCF. Stencil culling makes sure the shader only runs for pixels within a certain cascade. - SSAO with a bunch of different quality settings.
- A fullscreen pass we refer to as the “global lighting” pass. This is the pass that does most of the heavy lifting when it comes to the lighting. It handles mixing SSR with probe reflections, mixing of SSAO with material AO, lighting from all simple lights looked up from the clustered shading structure as well as calculates sun lighting masked with the result from sun shadow mask (step 1).
- Run a traditional deferred shading modifier for all light sources that has a material graph assigned. If the shader doesn’t target a specific layer the lights proxy volume will be rendered at this point, else it will be scheduled to render into whatever layer the shader has specified.

At this point we have a fully lit HDR output for all of our opaque materials.

```
// layer for emissive materials
{ name="emissive" render_targets=["hdr0"] depth_stencil_target="depth_stencil_buffer"
sort="FRONT_BACK" profiling_scope="emissive" }
// kick debug visualization
{ type="static_branch" render_caps={ development=true }
pass=[
{ resource_generator="debug_visualization" profiling_scope="debug_visualization" }
]
}
// kick resource generator for laying down fog
{ resource_generator="fog" profiling_scope="fog" }
// layer for skydome rendering
{ name="skydome" render_targets=["hdr0"] depth_stencil_target="depth_stencil_buffer"
sort="BACK_FRONT" profiling_scope="skydome" }
{ extension_insertion_point = "skydome" }
// layer for transparent materials
{ name="hdr_transparent" render_targets=["hdr0"] depth_stencil_target="depth_stencil_buffer"
sort="BACK_FRONT" profiling_scope="hdr_transparent" }
{ extension_insertion_point = "hdr_transparent" }
// kick resource generator for reading back any requested render targets / buffers to the CPU
{ resource_generator="stream_capture_buffers" profiling_scope="stream_capture" }
// kick resource generator for capturing reflection probes
{ type="static_branch" platform=["win"] render_caps={ development=true }
pass = [
{ resource_generator="cubemap_capture" }
]
}
// layer for rendering object selections from the editor
{ type="static_branch" platforms=["win", "ps4", "xb1"]
pass = [
{ type = "static_branch" render_settings={ selection_enabled=true }
pass = [
{ name="selection" render_targets=["gbuffer0" "ldr1_dev_r"]
depth_stencil_target="depth_stencil_buffer_selection" sort="BACK_FRONT"
clear_flags=["SURFACE" "DEPTH"] profiling_scope="selection"}
]
}
]
}
```


Next follows a bunch of layers for doing various stuff, most of this is straightforward:

`emissive`

- Layer for adding any emissive material influences to the light accumulation target (`hdr0`

)`debug_visualization`

- Kick of a resource generator for doing debug rendering. When debug rendering is enabled, the post processing pipe is disabled so we can render straight to the output target / back buffer here. Note: This doesn’t need to be scheduled exactly here, it could be moved later down the pipe.`fog`

- Kick of a resource generator for blending fog into the accumulation target.`skydome`

- Layer for rendering anything skydome related.`hdr_transparent`

- Layer for rendering transparent materials, traditional forward shading using the clustered shading acceleration structure for lighting. VFX with blending usually also goes into this layer.`stream_capture_buffer`

- Arbitrary location for capturing various render targets and dumping them into system memory.`cubemap_capture`

- Capturing point for reflection cubemap probes.`selection`

- Layer for rendering selection outlines.

So basically a bunch of miscellaneous stuff that needs to happen before we enter post processing…

```
// kick resource generators for AA resolve and post processing
{ resource_generator="post_processing" profiling_scope="post_processing" }
{ extension_insertion_point = "post_processing" }
```


Up until this point we’ve been in linear color space accumulating lighting into a 4xf16 render target (`hdr0`

). Now its time to take that buffer and push it through the post processing resource generator.

The post processing pipe in the Stingray Renderer does:

- Temporal AA resolve
- Depth of Field
- Motion Blur
- Lens Effects (chromatic aberration, distortion)
- Bloom
- Auto exposure
- Scene Combine (exposure, tone map, sRGB, LUT color grading)
- Debug rendering

All steps of the post processing pipe can dynamically be enabled/disabled (not entirely true, we will always have to run some variation of step 7 as we need to output our result to the back buffer).

```
// layer for rendering LDR materials, primarily used for rendering HUD and debug rendering
{ name="transparent" render_targets=["output_target"] depth_stencil_target="stable_depth_stencil_buffer_alias"
sort="BACK_FRONT" profiling_scope="transparent" }
// kick resource generator for rendering shadow map debug overlay
{ type="static_branch" render_caps={ development=true }
pass = [
{ resource_generator="debug_shadows" profiling_scope="debug_shadows" }
]
}
// kick resource generator for compositing left/right eye
{ type="static_branch" platforms=["win"] render_settings={ vr_supported=true }
pass = [
{ resource_generator="vr_present" profiling_scope="present" }
]
}
```


Before we present we allow rendering of unlit geometry in LDR (mainly used for HUDs and debug rendering), potentially do some more debug rendering and if we’re in VR mode we kick a resource generator that handles left/right eye combining (if needed).

That’s it - a very high-level breakdown of a rendered frame when running Stingray with the default “Stingray Renderer” `render_config`

file.

We also have a second rendering pipe that we ship with Stingray called the “Mini Renderer” - *mini* as in *minimalistic*. It is not as broadly used as the Stingray Renderer so I won’t walk you through it, just wanted to mention it’s there and say a few words about it.

The main design goal behind the mini renderer was to build a rendering pipe with as little overhead from advanced lighting effects and post processing as possible. It’s primarily used for doing mobile VR rendering. High-resolution, high-performance rendering on mobile devices is hard! You pretty much need to avoid all kinds of fullscreen effects to hit target frame rate. Therefore the mini renderer has a very limited feature set:

- It’s a forward renderer. While it’s capable of doing per pixel lighting through clustered shading it rarely gets used, instead most applications tend to bake their lighting completely or run with only a single directional light source.
- No post processing.
- While all lighting is done in linear color space we don’t store anything in HDR, instead we expose, tonemap and output sRGB directly into an LDR target (usually directly to the back buffer).

The `mini_renderer.render_config`

file is ~400 lines, i.e. less than 1/3 of the stingray renderer. It is still in a somewhat experimental state but is the fastest way to get up and running doing mobile VR. I also feel that it makes sense for us to ship an example of a more lightweight rendering pipe; it is simpler to follow than the `render_config`

for the full stingray renderer, and it makes it easy to grasp the benefits of data-driven rendering compared to a more static hard-coded rendering pipe (especially if you don’t have source access to the full engine as then the hard-coded rendering pipe would likely be a complete black box for the user).

I realize that some of you might have hoped for a more complete walkthrough of the various lighting and post processing techniques we use in the Stingray renderer. Unfortunately that would have become a very long post and also it feels a bit out of context as my goal with this blog series has been to focus on the architecture of the stingray rendering pipe rather than specific rendering techniques. Most of the techniques we use can probably be considered “industry standard” within real-time rendering nowadays. If you are interested in learning more there are lots of excellent information available, to name a few:

- Sébastien Lagarde & Charles de Rousiers amazing course notes from their Siggraph 2014 presentation: “Moving Frostbite to PBR”:
[http://www.frostbite.com/2014/11/moving-frostbite-to-pbr/](http://www.frostbite.com/2014/11/moving-frostbite-to-pbr/) - Morgan McGuire’s excellent Siggraph 2016 presentation: “Peering Through a Glass, Darkly

at the Future of Real-Time Transparency”:[http://graphics.cs.williams.edu/papers/TransparencySIGGRAPH16/](http://graphics.cs.williams.edu/papers/TransparencySIGGRAPH16/) - Everything from Natalya Tatarchuk’s Siggraph courses: “Advances in Real-Time Rendering in 3D Graphics and Games”:
[http://advances.realtimerendering.com/](http://advances.realtimerendering.com/) - Everything from Stephen Hill’s and Stephen McAuley’s Siggraph courses: “Physically Based Shading in Theory and Practice”:
[http://blog.selfshadow.com/publications/s2016-shading-course/](http://blog.selfshadow.com/publications/s2016-shading-course/)

In the next and final post of this series we will take a look at the shader and material system we have in Stingray.

I know it is not related to the post in itself, but I couldn't help but wonder: is there a place where you describe how your Hashset is implemented? I saw the code of the Bitsquid foundational library, but I mean a more conceptual description. I think it would be pretty useful and important, since you seem to have tried to implement a kind of hash table that is laid contiguously in memory (which is non trivial to find out there). Thanks anyways!

ReplyDeleteStingray's information driven engineering and adaptability have helped us fabricate a wide arrangement of games, and fast emphasis times for both code and substance makers has supported our efficiency essentially. The motor has been a key achievement factor for us since we're ready to create top-notch games in an abbreviated time span. Cheap assignment help UK


DeleteError code 0xc004f050 alludes to an issue with enacting Windows key. The issue shows up when you attempt to enact a duplicate of Windows by utilizing Windows Activation wizard. This happens when the framework winds up unsteady and basic framework documents begin missing. Despite the fact that Windows 10 is a free update for Windows 7/Windows 8/Windows 8.1 clients, the enactment blunder is as yet an issue. On the off chance that you previously had Windows 7/Windows 8/Windows 8.1 actuated and completed an overhaul effectively, at that point there ought to be no issue. This Problem Occurs just when you complete a clean introduce.


ReplyDeleteVisit for more:- windows 10 activation error code 0xc004f050

thanks to give for informative


ReplyDeleteWebsite Designing Company in Delhi

thanks to give for informative contentTop 10 Packers and movers in Delhi



ReplyDeleteThis comment has been removed by the author.

ReplyDeleteStingray Renderer from Autodesk At the Game Developers Conference (GDC) Europe 2015, Autodesk reported that its new Stingray game motor, Stingray Renderer Walkthrough Welcome To streamline information moving inside the Autodesk advancement groups.


ReplyDeleteRegards,

Cheap Reliable Essay Writing Service | 6$ Essay

Autodesk is escaping the game-motor business. The organization will screen its Stingray item, I have Stingray shader in Maya and might want to see it in Arnold.


ReplyDeleteLow Price Essay Writing Service USA | 6$ Essay.

good morning flower images free download

ReplyDeletehappy wedding anniversary di and jiju

When you return home, My Silver Service will be right there to transport you home keeping your whole family safe and sound.


ReplyDeleteMaxi Taxi

Error 3371



ReplyDeleteQuickbooks error h505

Quickbooks error code h505

Quickbooks h505

Quickbooks Error 6000 77

Quickbooks Error Code 6000

We have over 500 experts essay writers, ready and waiting to help you improve your writing skills.


ReplyDeleteOnline Classes

She exceeds my expectations, not only the article, I like the title too! I wish her success and also recommend her for your creative writing.



ReplyDeleteAnimator in Fiverr

Our service is very fast and pure, so call us any time of day and night and get an immediate response.


ReplyDeleteAssignment Writing UK

They were extremely proficient and truly worked admirably planning an inventive and connecting with logo! I was extremely satisfied with the result. They were mindful and finished their work when they said they would!

ReplyDeleteLogo Design Services

WOW! I Love it...



ReplyDeleteand i thing thats good for you >>

LUCKY NUMBER Thank you!




ReplyDeleteهاست لینوکستعرفه طراحی سایتSuggest good information in this message, click here.

ReplyDeleteusmountainproperties.com

gatlimited.com

Thanks for providing great informatic and looking beautiful blog, really nice required information & the things i never imagined and i would request, write more blog and blog posts like that for us.

ReplyDeleteBrilliant Information. Thank you for sharing.

ReplyDeleteIf you are using Windows 10, it has already uploaded many caches or junk files to your device. Because of this, Avast Antivirus does not work properly or closes some of your programs. Then, if you want to Uninstall Avast Antivirus in Windows 10 in your device.

You can visit our blog and read our guidelines for installing Avast Antivirus in Windows 10 and resolve issues on your own.

I read your post. It really nice information. Thanks for giving me this information.

ReplyDeleteAkshi Engineers Pvt. Ltd. is well-known industry for

Drivers & Automation Manufacturers, Suppliers & Exporters as per client's requirements in India. We provide tailored solutions for a wide range of industries, including electric drivers and automation, with the goal of revolutionizing energy conservation efforts by introducing reputable corporations' revolutionary power-saving products.google 888

ReplyDeletegoogle 889

google 890

google 891

google 892

google 893

Magnificent beat ! I wish to apprentice while you amend your web site, how could i subscribe for a blog web site?


ReplyDeleteThe account aided me a acceptable deal. 온라인경마

Hi there! I could have sworn I’ve been to this site before but after browsing through some of the articles I realized it’s new to me.


ReplyDeleteNonetheless, I’m certainly happy I came across it and I’ll be bookmarking it

and checking back regularly! 메이저사이트

google 3494

ReplyDeletegoogle 3495

google 3496

google 3497

google 3498

SO good indeed! Glad to have found your page!! This is such great work!! Interesting to read for sure!! 파친코



ReplyDeleteI must say you’ve done a very good job with this. Also, the blog loads extremely quick for me on Chrome. Superb Blog! 블랙잭사이트




ReplyDeleteI appreciate, result in I discovered exactly what I was looking for many year and Now my search is end after reading your blogs content 토토


ReplyDeleteIf you aren’t using SEO Software then you will know the amount of work load involved in creating accounts, confirming emails and submitting your contents to thousands of websites.



ReplyDeleteWith THIS SOFTWARE the link submission process will be the easiest task and completely automated, you will be able to build unlimited number of links and increase traffic to your websites which will lead to a higher number of customers and much more sales for you

카지노사이트

wep.

Thanks for one’s marvelous posting! I seriously enjoyed reading it, you may be a



ReplyDeletegreat author.I will remember to bookmark your blog and definitely will come back later in life.

I want to encourage you continue your great writing, have a nice

afternoon!Click Me Here 슬롯사이트

1YANGSKIE

Thanks for sharing excellent information. Your web site is very cool. I am impressed by the details that you've on this site. 홀덤



ReplyDeleteI was reading some of your articles on this website and I conceive this web site is very instructive! Retain putting up.


ReplyDelete파칭코사이트인포

먹튀검증 Just wish to say your article is as amazing. The clarity to your publish is simply spectacular and i could think you are a professional in this subject. Fine with your permission let me to grab your feed to stay up to date with impending post. Thanks one million and please keep up the enjoyable work.




ReplyDelete토토365프로 I was impressed by the good writing.Thank you.




ReplyDeleteIf you want to know the social graph game, come here!

Great article, totally what I was looking for.

Yay google is my queen assisted me to find this great web site! 온라인카지노사이트


ReplyDeleteI quite like reading an article that can make men and women think. Also, thanks for allowing me to comment! Feel free to visit my website; 카지노사이트



ReplyDeleteHey there, I think your website might be having browser compatibility issues. When I look at your website in Safari, it looks fine but when opening in Internet Explorer, it has some overlapping. I just wanted to give you a quick heads up! Other then that, awesome blog! web site. Feel free to visit my website; 카지노사이트



ReplyDeleteThere is an inborn curiosity about the Love Marriage Astrology, and Astrology can do it for you. Click here to know "

ReplyDeletedate of birth compatibility for marriage". You can also book a direct appointment to bail out of all the issues.Genuine Information. It is really helpful for me. Thanks for sharing with us. Keep sharing again.

ReplyDeleteAOL Mail is one of the leading web-mail service platforms for interfaces that allow users to stay connected with their peers through best email convenience. Sometimes, when you face your

AOL Mail Not Working On iPhone, you can contact our experts. They will patiently guide you with top-notch solutions.Mmm.. great to be here in your article or post, whatever, I figure I ought to likewise buckle down for my own site like I see some great and refreshed working in your site.카지노사이트프로


ReplyDeleteA good blog always comes-up with new and exciting information and while reading I have feel that this blog is really have all those quality that qualify a blog to be a one.바카라사이트



ReplyDeleteHello there! Nice article!!! But anyways here’s one of the trusted online baccarat site we can offer you so many promo and event everyday!! Good luck!!! 토토사이트


ReplyDeleteHоw dо ореn-ѕоurсе рrоduсtіvіtу ѕuіtеѕ compare tо MS Office - аnd dоеѕ іt mаkе ѕеnѕе fоr уоur оrgаnіzаtіоn tо сhооѕе frее соmmunіtу software rаthеr thаn Microsoft's commercially licensed оffеrіng




ReplyDelete일본경마

magosucowep

You have a interesting site! Find it more interesting because of the content. We can offer you more, By clicking the link below and learned more: 토토사이트


ReplyDeleteWow this is nice page. Hoping to see more of this. In case you are looking for something interesting, Just follow the link below: 카지노사이트


ReplyDeleteWow!! Thank you for sharing this post. Having a hard time looking for good and trusted site? I can offer you more and learn more by clicking the link below: 파워볼사이트


ReplyDeleteYour blog is great!!! Good content!! I would recommend this to my friends. But are you looking for online casino site? Click the link below: 바카라사이트


ReplyDeleteThe Indian education system is one of the most complex in the world. There are so many different types of exams, from state to national, that it can be difficult to keep track of what you need to do and when. Whether you're a student looking ahead at the next few years or a parent wondering how to get your child into a good school, this article will give you some insight into some of the


ReplyDeletetoughest exams in India2022.I read your post. It is amazing and helpful information for me. Thanks for sharing with everyone. I am Sofi Vergara, I am working as a tech expert at Yahoo support. I have 3 years of experience in this field. If you have any problems related to

ReplyDeleteYahoo Helpetc, then please contact me for instant help related to Yahoo email problems.I read your post. It is amazing and helpful information for me. Are you looking for a solution

ReplyDeleteHow to Delete Cache App Activity? Cash App Activity is a record of all transaction activity from sending or receiving the money to your contacts. To delete your cache app activity, you have it in the right place. If you have any questions regarding deleting Cash App transaction history, please contact us at our Cash App customer service.I like the helpful info you provide in your articles.


ReplyDeleteI will bookmark your blog and check again here regularly. I'm quite certain I'll learn many new stuff right here!

Best of luck for the next! 룰렛

This is the right site for everyone who would like to find out about this topic. 카지노사이트프로



ReplyDeleteIts an amazing website, really enjoyed your articles. Helpful and interesting too. 바카라사이트



ReplyDeleteI am very much delighted with your information. 카지노



ReplyDeleteThis comment has been removed by the author.

ReplyDeleteTechnologistan is the popoular and most trustworthy resource for technology, telecom, business and auto news in Pakistan

ReplyDelete8171 check onnline

At Twitter and Salesforce, Bret Taylor Steps Into the Limelight

ReplyDeleteOnly 4 Players Have A Real Chance To Win The 2022 NBA MVP Award

How does Men’s Health Clinic Dallas Help?

What is Hormone Pellet Therapy Atlanta GA?

What are the benefits of taking testosterone therapy Miami?

Who’s The Best Orthodontist In Greensboro North Carolina

How To Prepare For Filing A Medical Malpractice Lawsuit

Five childbirth injuries new parents don’t know about

Benefits of the Compex Mini Wireless Muscle Stimulator

FiFa 15 Crack Origin Activation Error – Windows 11, 10, 8, 7

The growth of


ReplyDeleteaircraft engine marketis also driven by demand for new generation engines with low emissions and lower weight, which will enhance the fuel efficiency of aircraft. Due to this trend, the companies are investing into research and development of new engine models with latest technologies like additive manufacturing and use of composite technologies.Also Read:

Point-of-Care (POC) Diagnostic Market|Guidewires Market|Telemedicine MarketNice Blog. Thanks for sharing with us. Such amazing information.






ReplyDeleteOnly Blog

Guest Blogger

Guest Blogging Site

Guest Blogging Website

Guest Posting Site

First of all, thank you for your post. 온카지노 Your posts are neatly organized with the information I want, so there are plenty of resources to reference. I bookmark this site and will find your posts frequently in the future. Thanks again ^^




ReplyDeleteWhen I read your article on this topic, the first thought seems profound and difficult. There is also a bulletin board for discussion of articles and photos similar to this topic on my site, but I would like to visit once when I have time to discuss this topic. 바카라사이트I think it would be nice if you come to if you can solve my problem.




ReplyDeleteTerrific work! This is the type of info that are meant to

ReplyDeletebe shared across the web. Shame on Google for not

positioning this publish higher! 스포츠토토

Come on over and talk over with my site .

See the website and the information is very interesting, good work! 카지노

ReplyDeleteThank you for providing information from your website. On of the good website in search results.

I love your blog.. very nice colors & theme. Did you make this website yourself or did you hire someone to do it for you? Plz reply as I’m looking to create my own blog and would like to find out where u got this from. thanks 온라인카지노


ReplyDeleteeveryone an extremely breathtaking chance to read from this blog. It is always so lovely and jam-packed with a great time. Feel free to visit my website; 온라인카지노



ReplyDeleteWonderful items from you, man. I’ve have in mind your stuff previous to and you’re just extremely excellent. I actually like what you’ve acquired here, really like what you’re saying and the way in which through which you assert it. You’re making it entertaining and you still care for to keep it smart. I cant wait to read far more from you. That is actually a terrific web site. Feel free to visit my website; 토토



ReplyDeleteNice response in return of this question with real arguments and explaining the whole thing about that.



ReplyDelete바둑이사이트넷

I read your post. It's really an awesome information. Thanks for sharing with us.

ReplyDeleteAre you seeking immediate technical help to know

How to Delete Cash App Account? If so, all you need to do is contact Cash App's support. To get information about the problem, you need to either contact the hotline number or connect via live chat.What should be the immediate step


ReplyDeleteHow To Change Yahoo Password? is the most important aspect. If you are a Yahoo email user and want to have the solution factors, then do not worry anymore, you can simply talk to the Yahoo support team to ask the relevant strategies and resolve the issues. Different kinds of systems are there that have to be followed while changing the passwords effectively.


ReplyDeleteHey friend, it is very well written article, thank you for the valuable and useful information you provide in this post. Keep up the good work! FYI, Pet Care adda

Sita Warrior Of Mithila Pdf Download , IDFC First Select Credit Card Benefits,Poem on Green and Clean Energy

It is really amazing information. Thanks for sharing.


ReplyDeleteAkshi Engineers is one of the most trustworthy, well-known, and professional workers

Pinch Roll MachineManufacturers in India and other countries. A pinch machine is a type of machine that is commonly used in steel pants to feed hot ingots to rolling mills. We have a variety of rolls that are tested by quality controllers in our manufacturing unit to ensure their study structure, reliability, and low maintenance cost.Thanks for sharing such great & useful information. keep it up.

ReplyDeleteIf you are looking for the

Play Boy Job Servicein India, Here, Mushkan Play Boy Job provides one of the best Play Boy Job Services in your cities. To join For Play Job Service, Contact us or visit our website.Buy the shop for the best fitness band in India and get the best fitness tracker

ReplyDeletedevice just in 2000. Get the best fitness tracker device only in 2000 in India. Offer limited get the tracker now.best fitness band under 2000

Hi everybody, This web page is remarkable and so is exactly how the subject has been expanded.


ReplyDelete토토사이트

바카라사이트

파워볼

바카라

Your article is very good, I have read many articles but I am really impressed with your posts. Thank you, I will review this article. To know about me, try talking to me. Visit Here:- Spectrum Email Not Working


ReplyDeleteThis is one of the best website I have seen in a long time thank you so much, thank you for let me share this website to all my friends. 먹튀검증디비

ReplyDeleteGuest Post


ReplyDeletetrending technology

blogging platforms

advantages of blogging platforms

Guest Post

The high payout rate is therefore able to return huge profits to members. Create a good experience that is new and good for the heart. betflix

ReplyDeleteThank you for this paragraph. It gives clear ideas for new viewers of the blog.



ReplyDelete토토사이트링크

토토사이트

바카라사이트

온라인카지노


ReplyDeleteI've read some great stuff here. Will definitely bookmark and visit again. I am amazed at the effort you put into creating such an excellent and informative website. Thanks so much for sharing. college of education waka-biu admission form

I read your blogs really informative keep sharing such good content.

ReplyDeleteSecurity Services in West London

Moreover, our therapists don't work body to body spa near me on your private areas and absolute privacy shall be ensured when you are changing clothes or when you are at the massage table.

ReplyDeleteAdd to the quandary that many massage therapists arenow practicing as part of a health care team in either a hospital or clinic, and b to b massage centre near me

ReplyDeletethe issuebecomes muddied further. Another consideration is the addition of continuing education skills gained after massage schoolgraduation; these skills often clearly place one therapist at a considerably different level of practice than another


ReplyDeleteIt appears the use of massage may largely be based upon anecdotal accounts that convey positive testaments about this form body massage near me of therapy, however applying scientific principles to the study of massage does pose methodological challenges for the researcher.

Overall, incorporating regular b2b massage bangalore into your self-care routine can do wonders for your physical and mental well-being.

ReplyDeleteCan I cherry pick my way to a happy body massage in bangalore endingcomprehensive massage therapy” as delivered by well-trained Ontario therapists,

ReplyDeleteMassage is a technique that has been body to body massage spa near me

ReplyDeleteused for many years to treat different problems.

Emotional Healing: Energy Healing Massage can help release body to body massage centres in chennai emotional blockages and foster emotional healing.

ReplyDeleteA head massage is a deep style massage that focuses on the head, neck and shoulders. A head massage applies a range of techniques b2b massage bangalore to help reduce stress and release tension in the upper body

ReplyDeleteThe sessions that have ejaculation as body to body massage near me the focus at the end tend to be shorter, and are not usually referred to as therapy.

ReplyDeleteWe need to prepare your personal 300 Dollar Loan No Credit Check data and information about employment and bank accounts to share details with multiple lenders we are working with.

ReplyDeleteTherapeutic Exercise Specialist, and Pn1 b to b massage centre near me is a health and human performance college professor, fitness blogger, mother, and passionate fitness professional

ReplyDeleteIntroducing our



ReplyDeleteMedical financing program, a comprehensive solution designed to ease the financial burden of healthcare expenses. We understand the importance of accessible medical care, and our program offers flexible payment options tailored to individual needs. Whether it's elective procedures, unexpected medical bills, or essential treatments, our financing ensures that quality healthcare remains within reach. With competitive interest rates and transparent terms, we prioritize your well-being without compromising financial stability.Experience peace of mind as you navigate your healthcare journey with our Medical Financing Program, empowering you to prioritize your health without compromising on quality care. Your well-being is our priority; let us support you every step of the way.

In addition to a complete body treatment, treat your body to an improved therapies choose from our selection of pure essential oils to help awaken your mind and rebalance your system b2b spa near me

ReplyDeleteWe have practiced many massage therapies since our founding in 2008, backed by our extensive knowledge in the science and art of traditional body massage spa near me.

ReplyDeleteThis tutorial was really beneficial. You did a good job of breaking down Stingray Renderer, which always felt a little intimidating. It's interesting to note that I employed resume writing services in UAE to match my creative work with my CV when updating my portfolio, which really enhanced my rendering and design projects.

ReplyDeleteAwesome

ReplyDeletebody massage spa in chennai