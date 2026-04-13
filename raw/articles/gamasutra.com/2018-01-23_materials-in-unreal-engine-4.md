---
title: Materials in Unreal Engine 4
url: https://www.gamedeveloper.com/art/materials-in-unreal-engine-4
author: Trent Polack
published: '2018-01-23'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Materials in Unreal Engine 4

A brief guide on material usage in Unreal Engine 4 along with best practices and links to our open-source assets.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

I tend to call master materials “shaders” (which is how I’ll refer to them from now on unless I specifically talk about USF shaders) as, at least for me, they tend to be “uber-shaders” done with the material editor. Which I do primarily to differentiate between special-case materials and my general-purpose shaders.

![](../../assets/13ea5864faf48aae.png)

A mech from

#### Using Materials

And I can’t recommend strongly enough how Materials — as opposed to Material Instances — should be used as sparingly as possible. The more spread-out your materials are, the more involved a process it becomes to make changes after you realize something is wrong or additional features are needed. Not to mention that once a material is used for a particle or mesh, whenever you delete a material and attempt to replace its references, you cannot replace it with a material instance; they can only be replaced by other materials. And this… is a real annoying and time-consuming issue to remedy.

If you absolutely must use materials over material instances, then your next best bet is to consolidate as much common logic into a [material function](https://blog.joy-machine.com/materials-in-unreal-engine-4-28417504acd2#material-functions) as you possibly can. Do anything you can to consolidate logic whenever possible.

#### Shaders

The shaders I create (which you can see in the [material shader library in this repo](https://github.com/joymachinegames/joymachine-public/tree/master/ue4/material_shaders)) contain a whole lot of logic, customizable features, and complexity. Here’s an example of an early version of my standard shader:

While it’s can easily become a gargantuan node graph, the resulting material instances created from it are not high-complexity shaders (always remember you can view the resulting HLSL shader code in UE). Here’s a comparison between a simple material instance:

And a material instance created from my standard shader:

I have all possible instance properties displayed (irrelevant ones are hidden by default) for both instance editors; the standard shader screen shot wasn’t able to fit in the remaining texture customization properties as well as detail texturing properties. The only difference in the resulting complexity was a single instruction count increase on the random example material instance, despite the enormous difference in configuration possibilities.

Which brings me to the material parameter node that is the most important thing in the entire world: the [Static Switch Parameter](https://docs.unrealengine.com/latest/INT/Engine/Rendering/Materials/ExpressionReference/Parameters/#staticswitchparameter). This parameter node exposes checkboxes to the material editor that completely discard any logic leading up to the chosen flag state (true/false). This means that, despite the extensive amount of possible functionality in a shader, that possible functionality is completely irrelevant to the generated material instance’s generated HLSL code. So, basically, I have every material in my game derived from a core shader library (most of which is in this repo, save for some more proprietary ones); any changes/fixes/optimizations that I realize need to be made can be made solely on the parent shader and it will propagate to any instance derived from it — saving me an extraordinary amount of hassle. And if I need more features on a given instance, I just check/uncheck the relevant switch property, and a new tree of parameters become available and the material instance’s complexity is increased/decreased accordingly.

#### Particle Shaders

Particle materials can be a bit more of a pain in the ass, given how specific they can be to a given effect. I’m still in the process of refining how I handle these, but so far I’ve found, still, a set of shaders for particle materials — a different shader per lighting model, basically — in tandem with a variety of material functions the most useful workflow while still consolidating as much logic as possible.

The only really drastic change between particle material instances and standard surface material instances is that particle material instances rely far more heavily on overrides for blending, lighting type, and two-sidedness. Since these can all be handled on the instance level, however, there’s no reason to create separate master materials for variations on all of these. Just ensure that your basic shaders connect to as many output material pins as possible, as some will be grayed out in your master material but still used if an instance makes any overrides.

#### Material Functions

Even with my hard adherence to consolidating as much shading/texturing logic as I possibly can into shaders, that’s still not enough to really consolidate as much as I’d really like to be doing. Material functions are the material editor’s form of logic encapsulation: individual functions with inputs and outputs that can be used and reused to your heart’s content across any number of materials.

I maintain a [constantly-updating library of material functions](https://github.com/joymachinegames/joymachine-public/tree/master/ue4/material_functions) as I work that I’ve found invaluable whenever I work. As an example of some of my most-used materials:

mf_normal_lerp — A function to properly blend together two normal maps that maintains the proper normal data.

mf_metallic_shading — A function to exaggerate the metallic shading on a material surface; it bases the material's roughness based on the vector between the camera and the pixel being evaluated. Aspects of this functionality is now integrated into the material editor (as of UE 4.17 or 4.18) with the curvature-based roughness parameter in the material properties (which I also have a material function for, as it’s more useful than making it a property of a master material).

mf_luminance — Properly evaluate the luminance value of the given pixel (best used in postprocessor materials).

mf_component_max_v3 — A stupid simple function that just grabs the maximum value from a three-component vector. It sounds dumb. It's amazing.


And as far as feature availability goes, material functions have all of the same node graph functionality as any material. You can even create and expose parameters to the material instance editor — though, without exception, I recommend not creating customizable parameters within material functions (just make them inputs, then create the parameters in the material using the material function). This is mostly a convention, but it’s one that has helped prevent a whole lot of confusion when looking back on materials I haven’t touched in a while.

More information, assets, and other resources on the [Joy Machine public GitHub repo](http://github.com/joymachinegames/joymachine-public).

#### Later Topic

I’ve also customized my UE4 build to support alternate BRDF models and shading terms (a good resource on this [is here](http://simonstechblog.blogspot.com/2011/12/microfacet-brdf.html)) that are added straight into the material and material instance editors as optional shading models to the standard ones. Doing this requires engine code modification, so it’s not as trivial, but I’ll get an article out on it sooner or later.