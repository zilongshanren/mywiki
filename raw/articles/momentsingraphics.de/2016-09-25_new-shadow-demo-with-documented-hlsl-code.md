---
title: New shadow demo with documented HLSL code
url: http://momentsingraphics.de/JCGT2016Demo.html
published: '2016-09-25'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# New shadow demo with documented HLSL code

**Update 2016-09-29:** In response to a request by [Jon Greenberg](https://twitter.com/jontology), I made a [new version of the demo](http://momentsingraphics.de/Media/JCGT2016Demo/MSMDemoV2.zip) that's more suitable for graphics debugging with [RenderDoc](https://renderdoc.org/builds) or [Visual Studio](https://msdn.microsoft.com/en-us/library/hh315751.aspx). The various passes are annotated with named, custom events and you can skip shader optimization and enable shader debugging by having the following line in *ShadowSettings.cfg*:

`enable_shader_debugging = 1`


It's time to deliver on a recent promise. [Moment shadow mapping](http://momentsingraphics.de/I3D2015.html) and its [applications](http://momentsingraphics.de/I3D2016.html) have seen quite a few minor but useful improvements lately. The [GDCE 2016 lecture](http://momentsingraphics.de/GDCEurope2016.html) covered some of them but only marginally. This post provides a brand-new [release of my shadow mapping demo](http://momentsingraphics.de/Media/JCGT2016Demo/MSMDemoV2.zip) with documented shader code including all these improvements.

The controls might not be quite self-explanatory because the primitive UI allows you to experiment with dozens of techniques for filtered hard shadows, shadows for translucent occluders, soft shadows and single scattering. If you have trouble figuring it out, please take a look at the included ReadMe.pdf. A [doxygen](https://www.stack.nl/~dimitri/doxygen/) documentation for the important shaders, including some pointers, is found at Demo/Documentation/index.html.

## What's new?

For those who already took a look at [earlier](http://momentsingraphics.de/I3D2015.html) [demos](http://momentsingraphics.de/I3D2016.html) I'd like to point out what has changed. There are no huge leaps forward but the changes improve speed and robustness of the techniques unconditionally, so you should prefer the new code under all circumstances.

- Signed depth
- It turns out that it is beneficial to use depth values defined in the interval \( [-1,1] \) rather than \( [0,1] \) as proposed originally. If you use moment shadow maps with 128 bits per texel, this yields a substantial reduction in light leaking because less biasing is needed. At 64 bits per texel, it only makes some rare artifacts even more seldom.
- Sparse quantization transform
- To diminish rounding errors, you have to multiply the moments by a particular 4x4 matrix before storing them in the four channels of the moment shadow map. This cost arises per texel and per pixel, so you want to keep it small. Thanks to the use of signed depth values, it is now possible to use a matrix where half of the entries are zero. Thus, the cost is halved.
- Biasing for the worst case
- Moment shadow mapping requires biasing to compensate for rounding errors. The originally proposed biasing scheme was optimized for the average case. If you used shadow maps with clamped depth values, it could fail in some situations. The new biasing scheme is optimized for best performance in the worst case and thus provides greater robustness at the same cost.
- Translucent occluders
- Shadows for translucent occluders now also work with exponential variance shadow maps but it is not a very good combination and only provided for comparison.
- Blocker search
- The blocker search of moment soft shadow mapping does not use the biased fragment depth anymore. Using a bias at this point is actually malicious.
- Adaptive depth bias
- For soft shadows the depth bias is now proportional to the filter size which helps to diminish surface acne more efficiently.
- Adaptive overestimation for single scattering
- Prefiltered single scattering allows you to define whether you want to under- or overestimate the brightness of the single scattering. You can also interpolate between the two results. In the new demo, this interpolation factor is adapted to the angle between light direction and view direction. This way, leaking artifacts are diminished without reducing the approximation quality elsewhere.
- Improved six moment shadow mapping
- My
[previous blog post](http://momentsingraphics.de/CubicRoots.html)already introduced the robust solution to a cubic equation that I developed for prefiltered single scattering with six moments. It makes the technique faster and more robust. Additionally, the improvements for four moment shadow mapping listed above (signed depth, sparse quantization transform and worst-case biasing) work analogously for six moment shadow mapping and help a great deal. - Optimized prefix sum generation
- I did my best to write a fast compute shader for generation of transmittance-weighted prefix sums in prefiltered single scattering. Resampling is a separate pixel-shader pass now because in the end, this is faster. The new shader is close to being bandwidth limited, at least in some cases. I've only benchmarked it on a GTX 970 though, so you might want to reevaluate on your target platforms.
- Miscellaneous
- The demo now uses sRGB consistently and supports overdarkening to diminish light leaking. Trigonometric moment shadow mapping is more robust but still way too slow to be useful. Mipmaps are only generated for textures where they are actually needed. This gives a considerable speedup.

If you are looking for detailed explanations why all of the above works, you'll have to wait a bit longer. I am currently preparing the invited extension of the [i3D 2016 paper](http://momentsingraphics.de/I3D2016.html) for the [Journal of Computer Graphics Techniques](http://jcgt.org/). This extension will cover all the improvements listed above.

## Screenshots and video

In case you aren't convinced to click the [download link](http://momentsingraphics.de/Media/JCGT2016Demo/MSMDemoV2.zip) yet, here are some screenshots and the flash forward for the [GDCE 2016 lecture](http://momentsingraphics.de/GDCEurope2016.html).

## Bug reports

The demo provided here is slated for publication with the [JCGT](http://jcgt.org/) extension of the [i3D 2016 paper](http://momentsingraphics.de/I3D2016.html). If you find any issues, please let me know. They best be fixed before the official publication.

## Download

## Comments

**Nick**

2017-08-10, 23:17

Nice, no give up!

Comments are closed.