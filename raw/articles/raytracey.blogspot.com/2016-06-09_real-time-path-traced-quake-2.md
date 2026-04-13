---
title: Real-time path traced Quake 2
url: http://raytracey.blogspot.com/2016/06/real-time-path-traced-quake-2.html
author: Sam Lapere
published: '2016-06-09'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Last week, Edd Biddulph released the code and some videos of a very impressive project he's working on: a real-time path traced
version of Quake 2 running on OpenGL 3.3.


Project link with videos:

Full source code on Github:

Project link with videos:

[http://amietia.com/q2pt.html](http://amietia.com/q2pt.html)Full source code on Github:

[https://github.com/eddbiddulph/yquake2/tree/pathtracing](https://github.com/eddbiddulph/yquake2/tree/pathtracing)
![]() |

The path tracing engine behind this project is quite astonishing when you consider the number of lightsources in the level and
the amount of dynamic
characters (each with a unique pose) that are updated every single frame. I had a very interesting talk with Edd on some of the features of his engine, revealing that he used a lot of clever optimisations (some of which are taking advantage of the specific properties of the Quake 2 engine).

Copying Edd's answers here:

Why Quake 2 instead of Quake 3

I chose Quake 2 because it has area lightsources and the maps were designed with multiple-bounce lighting in mind. As far as I know, Quake 3 was not designed this way and didn't even have area lightsources for the baked lighting. Plus Quake 2's static geometry was still almost entirely defined by a binary space partitioning tree (BSP) and I found that traversing a BSP is pretty easy in GLSL and seems to perform quite well, although I haven't made any comparisons to other approaches. Quake 3 has a lot more freeform geometry such as tessellated Bezier surfaces so it doesn't lend itself so well to special optimisations. I'm a big fan of both games of course :)


How the engine updates dynamic objects

All dynamic geometry is inserted into a single structure which is re-built from scratch on every frame. Each node is an axis-aligned bounding box and has a 'skip pointer' to skip over the children. I make a node for each triangle and build the structure bottom-up after sorting the leaf nodes by morton code for spatial coherence. I chose this approach because the implementation is simple both for building and traversing, the node hierarchy is quite flexible, and building is fast although the whole CPU side is single-threaded for now (mostly because Quake 2 is single-threaded of course). I'm aware that the lack of ordered traversal results in many more ray-triangle intersection tests than are necessary, but there is little divergence and low register usage since the traversal is stackless.


How to keep noise to a minimum when dealing with so many lights

The light selection is a bit more tricky. I divided lightsources into two categories - regular and 'skyportals'. A skyportal is just a light-emitting surface from the original map data which has a special texture applied, which indicates to the game that the skybox should be drawn there. Each leaf in the BSP has two lists of references to lightsources. The first list references regular lightsources which are potentially visible from the leaf according to the PVS (potentially visible set) tables. The second list references skyportals which are contained within the leaf. At an intersection point the first list is used to trace shadow rays and make explicit samples of lightsources, and the second list is used to check if the intersection point is within a skyportal surface. If it's within a skyportal then there is a contribution of light from the sky. This way I can perform a kind of offline multiple importance sampling (MIS) because skyportals are generally much larger than regular lights. For regular lights of course I use importance sampling, but I believe the weight I use is more approximate than usual because it's calculated always from the center of the lightsource rather than from the real sample position on the light.


One big point about the lights right now is that the pointlights that the original game used are being added as 4 triangular lightsources arranged in a tetrahedron so they tend to make quite a performance hit. I'd like to try adding a whole new type of lightsource such as a spherical light to see if that works out better.


Ray tracing specific optimisations

I'm making explicit light samples by tracing shadow rays directly towards points on the lightsources. MIS isn't being performed in the shader, but I'm deciding offline whether a lightsource should be sampled explicitly or implicitly.


Which parts of the rendering process use rasterisation

I use hardware rasterisation only for the primary rays and perform the raytracing in the same pass for the following reasons:


- Translucent surfaces can be lit and can receive shadows identically to all other surfaces.
- Hardware anti-aliasing can be used, of course.
- Quake 2 sorts translucent BSP surfaces and draws them in a second pass, but it doesn't do this for entities (the animated objects) so I would need to change that design and I consider this too intrusive and likely to break something. One of my main goals was to preserve the behaviour of Q2's own renderer.
- I'm able to eliminate overdraw by making a depth-only pre-pass which even uses the same GL buffers that the raytracer uses so it has little overhead except for a trick that I had to make since I packed the three 16-bit triangle indices for the raytracer into two 32-bit elements (this was necessary due to OpenGL limitations on texture buffer objects).
- It's nice that I don't need to manage framebuffer stuff and design a good g-buffer format.

The important project files containing the path tracing code

If you want to take a look at the main parts that I wrote, stick to src/client/refresh/r_pathtracing.c and src/client/refresh/pathtracer.glsl. The rest of my changes were mostly about adding various GL extensions and hooking in my stuff to the old refresh subsystem (Quake 2's name for the renderer). I apologise that r_pathtracing.c is such a huge file, but I did try to comment it nicely and refactoring is already on my huge TODO list. The GLSL file is converted into a C header at build time by stringifyshaders.sh which is at the root of the codebase.


More interesting tidbits

- This whole project is only made practical by the fact that the BSP files still contain surface emission data despite the game itself making no use of it at all. This is clearly a by-product of keeping the map-building process simple, and it's a very fortunate one!

- The designers of the original maps sometimes placed pointlights in front of surface lights to give the appearence that they are glowing or emitting light at their sides like a fluorescent tube diffuser. This looks totally weird in my pathtracer so I have static pointlights disabled by default. They also happen to go unused by the original game, so it's also fortunate that they still exist among the map data.

- The weapon that is viewed in first-person is drawn with a 'depth hack' (it's literally called RF_DEPTHHACK), in which the range of depth values is reduced to prevent the weapon poking in to walls. Unfortunately the pathtracer's representation would still poke in to walls because it needs the triangles in worldspace, and this would cause the tip of the weapon to turn black (completely in shadow). I worked around this by 'virtually' scaling down the weapon for the pathtracer. This is one of the many ways in which raytracing turns out to be tricky for videogames, but I'm sure there can always be elegant solutions.

If you want to mess around with the path traced version of Quake 2 yourself (both AMD and Nvidia cards are supported as the path tracer uses OpenGL), simply follow these steps:


Edd also said he's also planning to add new special path tracing effects (such as light emitting particles from the railgun) and implementing more optimisations to reduce the path tracing noise.

- on Windows, follow the steps under section 2.3 in the readme file (link: https://github.com/eddbiddulph/yquake2/blob/pathtracing/README). Lots of websites still offer the Quake 2 demo for download (e.g. http://www.ausgamers.com/files/download/314/quake-2-demo)
- download and unzip the Yamagi Quake 2 source code with path tracing from https://github.com/eddbiddulph/yquake2
- following the steps under section 2.6 of the readme file, download and extract the premade MinGW build environment, run MSYS32, navigate to the source directory with the makefile, "make" the release build and replace the files "q2ded.exe", "quake2.exe" and "baseq2\game.dll" in the Quake 2 game installation with the freshly built ones
- start the game by double clicking "quake2", open the Quake2 console with the ~ key (under the ESC key), type "gl_pt_enable 1", hit Enter and the ~ key to close the console
- the game should now run with path tracing

Edd also said he's also planning to add new special path tracing effects (such as light emitting particles from the railgun) and implementing more optimisations to reduce the path tracing noise.

## 6 comments:

A far cry from Pong eh? :D

Indeed :) Tokap had a good run, but this has infinitely more potential.

Does this work with a gamepad?

Hi. He managed someone to compile game? I can not make it. Quake 2.exe crash when run !

Sam, I think the your fresnel reflectance's codes have a misktake:








float R0 = (nt - nc)*(nt - nc) / (nt + nc)*(nt + nc);

should be

float R0 = (nt - nc)*(nt - nc) / ((nt + nc)*(nt + nc));

The wrong code will cause a unnatural refractive appearance.

And I have another question, in the following codes:

float R0 = (nt - nc)*(nt - nc) / (nt + nc)*(nt + nc);

float c = 1.f - (into ? -ddn : dot(tdir, n));

float Re = R0 + (1.f - R0) * c * c * c * c * c;

float Tr = 1 - Re; // Transmission

float P = .25f + .5f * Re;

float RP = Re / P;

float TP = Tr / (1.f - P);

// randomly choose reflection or transmission ray

if (curand_uniform(randstate) < 0.25) // reflection ray

{

mask *= RP;

dw = rayInWorldSpace;

dw -= n * 2.0f * dot(n, rayInWorldSpace);

pointHitInWorldSpace = x + nl * 0.01; // scene size dependent

}

else // transmission ray

{

mask *= TP;

dw = tdir; //r = Ray(x, tdir);

pointHitInWorldSpace = x + nl * 0.001f; // epsilon must be small to avoid artefacts

}

why P is calculated like that? And in "curand_uniform(randstate) < 0.25", why 0.25?

It keeps crashing too under windows 8. But original Yamagi Quake works fine.

Post a Comment