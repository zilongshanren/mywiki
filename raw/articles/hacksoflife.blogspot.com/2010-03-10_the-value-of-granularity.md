---
title: The Value Of Granularity
url: http://hacksoflife.blogspot.com/2010/03/value-of-granularity.html
author: Benjamin Supnik
published: '2010-03-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[leaky abstraction](http://www.joelonsoftware.com/articles/LeakyAbstractions.html). It promises to draw in 3-d. And it does! But it doesn't say a lot about how long that drawing will take, yet performance is central to GL-based games and apps. Filling in this gap is transient information about OpenGL and its current dominant implementations that isn't easy to come by - it comes from a mix of insight from other developers, connecting the dots, reading many disparate documents, and direct experimentation. This isn't easy for someone who isn't working full time as an OpenGL developer, so I figure there may be some value to blogging things I have learned the hard way about OpenGL while working on X-Plane.

OpenGL presents new functionality via extensions. (It also presents new functionality via version numbers, but the extensions tend to range ahead of the version numbers because the version number can only be bumped when

*all*required extensions are available.) When building an OpenGL game you need a strategy for coping with different hardware with different capabilities. X-Plane dates back well over a decade, and has been using OpenGL for a while, so the app has had to cope with pretty much every extension being not available at one point or another.

Our overall strategy is to categorize hardware into "buckets". For X-Plane 9 we have 2.5 buckets:

- Pre-shader hardware, running on a fixed function pipeline.
- Modern shader enabled hardware, using shaders whenever possible.
- We have a few shaders that get cased off into a special bucket for the first-gen shader hardware (R300, NV25), since that hardware has some performance and capability limitations.

So here is what has turned out to be surprising: we were basically forced to allow X-Plane to run with a very granular set of extensions for debugging purposes. An example will ilWhat lustrate.

Using the buckets strategy you might say: "The shader bucket uses GLSL, FBOs, and VBOs. Any hardware in that category has all three, so don't write any code that uses GLSL but not FBOs, or GLSL but not VBOs." The idea is to save coding by reducing the combination of all possible OpenGL hardware (we have eight combos of these three extensions) to only two combinations (have them all, don't have them all).

What we found in practice was that being able to run in a semi-useful state without FBOs but with GLSL was immensely useful for in-field debugging. This is not a configuration we'd ever want to really support or use, but at least during the time period that we started using FBOs heavily, the driver support for them was spotty on the configurations we hit in-field. Being able to tell a user to run with --no_fbos was an invaluable differential to demonstrate that a crash or corrupt screen was related specifically to FBOs and not some other part of OpenGL.

As a result, X-Plane 9 can run with any of these "core" extensions in an optional mode: FBOs, GLSL, VBOs (!), PBOs, point sprites, occlusion queries, and threaded OpenGL. That list matches a series of driver problems we ran across pretty directly.

Maintaining a code base that supports virtually every combination is not sustainable indefinitely, and in fact we've started to "roll up" some of these extensions. For example, X-Plane 9.45 requires a threaded OpenGL driver, whereas X-Plane 9.0 would run without it. We remove support for individual extensions going missing when tech support calls indicate that "in field" the extension is now reliable.

At this point it looks like FBOs, threaded OpenGL, and VBOs are pretty much stable. But I believe that as we move forward into newer, weirder OpenGL extensions, we will need to keep another set of extensions optional on a per-feature basis as we find out the hard way what isn't stable in-field.

## No comments:

## Post a Comment