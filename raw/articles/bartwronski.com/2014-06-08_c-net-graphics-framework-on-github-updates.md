---
title: C#/.NET graphics framework on GitHub + updates
url: https://bartwronski.com/2014/06/08/c-net-graphics-framework-on-github-updates/
published: '2014-06-08'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

As I promised I posted my C#/.NET graphics framework (more about it and motivation behind it [here](https://bartwronski.com/2014/04/10/c-net-graphics-framework/)) on GitHub: [https://github.com/bartwronski/CSharpRenderer](https://github.com/bartwronski/CSharpRenderer)

This is my first GitHub submit ever and my first experience with Git, so there is possibility I didn’t do something properly – thanks for your understanding!

List of changes since initial release is quite big, tons of cleanup + some crashfixes in previously untested conditions, plus some features:

## Easy render target management

I added helper functions to manage lifetime of render targets and allow render target re-use. Using render target “descriptors” and RenderTargetManager you request a texture with all RT and shader resource views and it is returned from a pool of available surfaces – or lazily allocated when no surface fitting given descriptor is available. It allows to save some GPU memory and makes sure that code is 100% safe when changing configurations – no NULL pointers when enabling not enabled previously code paths or adding new ones etc.

I also added very simple “temporal” surface manager – that for every surface created with it stores N different physical textures for requested N frames. All temporal surface pointers are updated automatically at beginning of a new frame. This way you don’t need to hold states or ping-pong in your rendering passes code and code becomes **much** easier to follow eg.:

RenderTargetSet motionVectorsSurface = TemporalSurfaceManager.GetRenderTargetCurrent("MotionVectors"); RenderTargetSet motionVectorsSurfacePrevious = TemporalSurfaceManager.GetRenderTargetHistory("MotionVectors"); m_ResolveMotionVectorsPass.ExecutePass(context, motionVectorsSurface, currentFrameMainBuffer);

## Cubemap rendering, texture arrays, multiple render target views

Nothing super interesting, but allows to much more easily experiment with algorithms like GI (see following point). In my backlog there is a task to add support for geometry shader and instancing for amplification of data for cubemaps (with proper culling etc.) that should speed it up by order of magnitude, but wasn’t my highest priority.

## Improved lighting – GI baker, SSAO

I added 2 elements: [temporally supersampled SSAO](https://bartwronski.com/2014/04/27/temporal-supersampling-pt-2-ssao-demonstration/) and simple pre-baked global illumination + fully GPU-based naive GI baker. When adding those passes I was able to really stress my framework and check if it works as it is supposed to – and I can confirm that adding new passes was extremely quick and iteration times were close to zero – whole GI baker took me just one evening to write.

GI is stored in very low resolution, currently uncompressed volume textures – 3 1MB R16 RGBA surfaces storing incoming flux in 2nd order SH (not preconvolved with cosine lobe – not irradiance). There are some artifacts due to low resolution of volume (64 x 32 x 64), but for cost of 3MB for such scene I guess it’s good enough. 🙂

It is calculated by doing cubemap capture at every 3d grid voxel, calcularing irradiance for every texel and projecting it onto SH. I made sure (or I hope so! 😉 but seems to converge properly) it is energy conserving, so N-bounce GI is achieved by simply feeding previous N-1 bounce results into GI baker and re-baking the irradiance. I simplified it (plus improved baking times – converges close to asymptotic value faster) even a bit more, as baker uses partial results, but with N -> oo it should converge to the same value and be unbiased.

It contains “sky” ambient lighting pre-baked as well, but I will probably split those terms and store separately, quite possibly at a different storage resolution. This way I could simply “normalize” the flux and make it independent of sun / sky color and intensity. (it could be calculated in the runtime). There are tons of other simple improvements (compressing textures, storing luma/chroma separately in different order SH, optimizing baker etc) and I plan to gradually add them, but for now the image quality is very good (as for something without normalmaps and speculars yet 😉 ).

## Improved image quality – tone-mapping, temporal AA, FXAA

Again nothing that is super-interesting, rather extremely simple and usually unoptimal code just to help debugging other algorithms (and make their presentation easier). Again adding such features was matter of minutes and I can confirm that my framework succeeds so far in its design goal.

## Constant buffer constants scripting

A feature that I’m not 100% happy with.

For me when working with almost anything in games – from programming graphics and shaders through materials/effects to gameplay scripting the biggest problem is finding proper boundaries between data and code. Where splitting point should be? Should code drive data, or the other way around. From multiple engines I have worked on (RedEngine, Anvil/scimitar, Dunia plus some very small experience just to familiarize myself with CryEngine, UnrealEngine 3, Unity3D) in every engine it was in a different place.

Coming back to shaders, usually tedious task is putting some stuff on the engine side in code, and some in the actual shaders while both parts must mach 100%. It not only makes it more difficult to modify some of such stuff, adding new properties, but also harder to read and follow code to understand the algorithms as it is split between multiple files not necessarily by functionality, but for example performance (eg. precalculate stuff on CPU and put into constants).

Therefore my final goal would be to have one meta shader language and using some meta decorators specify frequency of every code part – for example one part should be executed per frame, other per viewport, other per mesh, per vertex, per pixel etc. I want to go in this direction, but didn’t want to get myself into writing parsers and lexers and temporarily I used LUA (as extremely fast to integrate and quite decently performing).

Example would be one of my constant buffer definitions:

cbuffer PostEffects : register(b3) { /// Bokeh float cocScale; // Scripted float cocBias; // Scripted float focusPlane; // Param, Default: 2.0, Range:0.0-10.0, Linear float dofCoCScale; // Param, Default: 0.0, Range:0.0-32.0, Linear float debugBokeh; // Param, Default: 0.0, Range:0.0-1.0, Linear /* BEGINSCRIPT focusPlaneShifted = focusPlane + zNear cameraCoCScale = dofCoCScale * screenSize_y / 720.0 -- depends on focal length & aperture, rescale it to screen res cocBias = cameraCoCScale * (1.0 - focusPlaneShifted / zNear) cocScale = cameraCoCScale * focusPlaneShifted * (zFar - zNear) / (zFar * zNear) ENDSCRIPT */ };

We can see that 2 constant buffer properties are scripted – there is zero code on C# side that would calculate it like this, instead a LUA script is executed every frame when we “compile” constant buffer for use by the GPU.

## UI grouping by constant buffer

Simple change to improve readability of UI. Right now the UI code is the most temporary, messy part and I will change it completely for sure, but for the time being I focused on the use of it.

## Further hot-swap improvements

Right now everything in shader files and related to shaders is hot-swappable – constant buffer definitions, includes, constant scripts. Right now I can’t imagine working without it, definitely helps iterating faster.

## Known issues / requirements

I was testing only x64 version, 32 bit could be not configured properly and for sure is lacking proper dll versions.

One known issue (checked on a different machine with Windows 7 / x64 / VS2010) is runtime exception complaining about lack of “lua52.dll” – it is probably caused by lack of [Visual Studio 2012+ runtime](http://www.microsoft.com/en-ca/download/details.aspx?id=30679).

## Future plans

While I update stuff every week/day in my local repo, I don’t plan to do any public commits (except for something either cosmetic, or serious bug/crash fix) till probably late August. I will be busy preparing for [my Siggraph 2014 talk](http://s2014.siggraph.org/attendees/courses/events/advances-real-time-rendering-games-part-ii) and plan to release source code for the talk using this framework as well.

You must be logged in to post a comment.