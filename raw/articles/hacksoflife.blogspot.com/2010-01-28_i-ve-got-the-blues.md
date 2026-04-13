---
title: I've Got the Blues
url: http://hacksoflife.blogspot.com/2010/01/ive-got-blues.html
author: Benjamin Supnik
published: '2010-01-28'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I learned this while working with alpilotx on a quirky bug: experimental instancing code was causing the instanced geometry to look completely goofy and turning the rest of the scene pretty much completely blue. The bug appeared only on NVidia hardware on Linux.

Well if you read the

[fine print](http://developer.download.nvidia.com/opengl/glsl/glsl_release_notes.pdf)closely, you'll find this:

NVIDIA’s GLSL implementation therefore does not allow built-in vertex attributes toThis is really too bad, as the GL 2.1 specification says:

collide with a generic vertex attributes that is assigned to a particular vertex attribute

index with glBindAttribLocation. For example, you should not use gl_Normal (a

built-in vertex attribute) and also use glBindAttribLocation to bind a generic vertex

attribute named “whatever” to vertex attribute index 2 because gl_Normal aliases to

index 2.

There is no aliasing among generic attributes and conventional attributes. InI can report, with a full head of steam and outrage, that the current NVidia drivers on Linux definitely work the way NVidia says they do, and not the way the spec would like them to. Documenting what their code does...the nerve of it! Those NVidia driver writes!

other words, an application can set all MAX VERTEX ATTRIBS generic attributes

and all conventional attributes without fear of one particular attribute overwriting

the value of another attribute.

What? You already knew this? Ha ha, so did I, just kidding, I was just quizzing you...

I don't think this is really news at all - I think I'm just really late to the party. In particular, X-Plane 8 and 9 run all of their shaders entirely using the built-in attributes to pass per-vertex information; sometimes that information is quite heavily bastardized to make it happen.

I'm sure there are reasons why this is evil, but I can tell you why we did it: it allows us to have a unified code path for scene graph, mesh, and buffer management. Only our shader setup code is actually sensitive to what the actual hardware is capable of doing - the rest runs on anything back to OpenGL 1.2.1.

(This is actually not 100% true. In some cases we will tag additional attributes to our vertices only on a machine with GLSL - this is a simple optimization during mesh build-up to save time and space for machines that will never use the extra attributes anyway. An example of this is the basis vectors for billboarding that are attached to trees: no GLSL means no billboarding the trees, so we drop the extra basis vectors.)

The moral of the story: let the linker pick your attribute indices.

## No comments:

## Post a Comment