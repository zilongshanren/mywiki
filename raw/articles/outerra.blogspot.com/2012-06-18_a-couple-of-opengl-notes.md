---
title: A couple of OpenGL notes
url: https://outerra.blogspot.com/2012/06/couple-of-opengl-notes.html
author: Outerra
published: '2012-06-18'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

#### A couple of notes mostly for my own reference, and for the unlucky souls who google through here after encountering similar problems.

#### A floating-point depth buffer

Some time ago I wrote about the possible use of

[a reversed-range floating point depth buffer](http://outerra.blogspot.sk/2009/12/floating-point-depth-buffer.html)as an alternative to the

[logarithmic depth buffer](http://outerra.blogspot.sk/2009/08/logarithmic-z-buffer.html)(see also

[+Thatcher Ulrich](https://plus.google.com/110179169236197163158/posts)'s

[post about logarithmic buffers](http://tulrich.com/geekstuff/log_depth_buffer_vis.html)). A RFP depth buffer has got some advantages over the logarithmic one we are still using today, namely no need to write depth values in the fragment shader for objects close to the camera in order to suppress depth bugs caused by insufficient geometry tesselation, because the depth values interpolated across polygon diverge from the required logarithmic value significantly in that case.

Writing depth values in a fragment shader causes a slight performance drop because of the additional bandwidth the depth values take, and also because it disables various hardware optimizations related to depth buffers. However, we have found the performance drop to be quite small in our case, so we didn't even test the floating point buffer back then.

A disadvantage of floating-point depth buffer is that it takes 32 bits, and when you also need a stencil buffer it no longer fits into a 32 bit alignment, and thus consumes twice as much memory as a 24b integer buffer + 8b stencil (if there was a 24-bit floating point format, its resolution would be insufficient and inferior in comparison to the logarithmic one, in our case).

Recently we have been doing some tests of our new object pipeline, and decided to test the reversed floating-point buffer to see if the advantages can outdo the disadvantages.

However, a new problem arose that's specific to OpenGL: since in OpenGL the depth values use normalized device range of -1 to 1, techniques that rely on a higher precision of floating point values close to zero cannot be normally used because the far plane is mapped to -1 and not to 0.

Alright, I thought, I will sacrifice half of the range and simply output 1..0 values from the vertex shader, the precision will be still sufficient.

However, there is a problem that OpenGL does implicit conversion from NDC to 0..1 range to compute the actual values to write to the depth buffer. That conversion is defined as 0.5*(f-n)*z + 0.5(f+n) where n,f are values given by glDepthRange. With default values of 0,1 that means that the output value of z from vertex shader gets remapped by 0.5*z + 0.5.

Since the reversed FP depth buffer relies on better precision near 0, the addition of 0.5 to values like 1e-12 pretty much discards most of the significant bits, rendering the technique unusable.

Calling glDepthRange with -1, 1 parameters would solve the problem (making the conversion 1*z + 0), but the spec explicitly says that "The parameters n and f are clamped to the range [0; 1], as are all arguments of type clampd or clampf".

On Nvidia hardware the NV_depth_buffer_float extension comes to the rescue, as it allows to set non-clamped values, but alas it's not supported on AMD hardware, and that's the end of the journey for now.

Update: a more complete and updated info about the use of reverse floating point buffer can be found in post

[Maximizing Depth Buffer Range and Precision](http://outerra.blogspot.com/2012/11/maximizing-depth-buffer-range-and.html).

#### Masquerading integer values as floats in outputs of fragment shaders

Occasionally (but in our case quite often) there's a need to combine floating point values with integer values in a single texture. For example, our shader that generates road mask (to be applied over terrain geometry in another pass) needs to output road height as float, together with road type and flags as integers. Since using shader instructions uintBitsToFloat or floatBitsToUint is cheap (they are just type casts), it can be easily done.

However, there's a problem: if you use a floating-point render target for that purpose, the exact bit representation of the masqueraded integer values may not be preserved on AMD hardware, as the blending unit, even though inactive, can meddle with the floating point values, altering them in a way that doesn't do much to the interpretation of floating point values, but changes the bits in some cases.

In this case you need to use an integer render target and cast the floating point values to int (or uint) instead.

## No comments:

Post a Comment