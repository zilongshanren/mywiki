---
title: Demo with non-linearly quantized moment shadow maps and more
url: http://momentsingraphics.de/HPG2017Demo.html
published: '2017-09-05'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Demo with non-linearly quantized moment shadow maps and more

My recent paper on [non-linearly quantized moment shadow maps](http://momentsingraphics.de/HPG2017.html) promises an executable demo. Preparing that took a little longer than expected but to make up for the delay, the demo has plenty of new features. Most notably it now uses [dear imgui](https://github.com/ocornut/imgui) and includes the [applications of blue noise](http://momentsingraphics.de/BlueNoise.html) I blogged about earlier. Rather than showing off the new technique only, this demo is an extension of earlier demos, so it also features soft shadows, single scattering and shadows for translucent occluders.

As usual, it comes with documented HLSL code to ease adaptation of the discussed techniques. You can also set `enable_shader_debugging = 1`

in the config file to ensure that tools like [RenderDoc](https://renderdoc.org/) let you browse the shaders. The shader code is in the [public domain](https://creativecommons.org/publicdomain/zero/1.0/).

## What's new?

This is the fourth published version of a demo with this code base. Here is an overview of the new features.

- Non-linearly quantized moment shadow maps
- This
[recently introduced extension](http://momentsingraphics.de/HPG2017.html)to moment shadow mapping applies some mathematical tricks to reduce the memory requirements of moment shadow mapping. It can go as low as 32 bits per texel, while still reducing light leaking artifacts compared to the original quantization at 64 bits per texel. Additionally, there is a heavily optimized compute shader to do the filtering of the moment shadow map in a single pass and computation of the shadows has been optimized. If you want to diminish aliasing and surface acne at a low cost, this is the way to go. The demo implements all novel techniques and a lot of related work such as the original moment shadow mapping or exponential variance shadow mapping. - New user interface
- Admittedly, the user interface in earlier versions of the demo has been
[pesky](https://twitter.com/mmalex/status/780702209797423104). The new user interface is based on[dear imgui](https://github.com/ocornut/imgui/issues)and should be self-explanatory. In case anything is still unclear, there is a ReadMe.pdf. - Shadow map interpolation
- A drawback of non-linearly quantized moment shadow maps is that you can no longer use hardware-accelerated bilinear interpolation for the moment shadow map. As fast alternative, the demo supports blue noise dithering. Manual bilinear interpolation in the pixel shader and nearest neighbor interpolation are also available. For comparison, all of these options are also available for other shadow mapping techniques.
- Dithered moment soft shadow mapping
- A noteworthy special case of the previous point is that the demo lets you try
[blue-noise dithering with moment soft shadow mapping](http://momentsingraphics.de/BlueNoise.html#bilinearinterpolation). I showed some results of that before but it gives a considerable speedup so it is nice to have that as part of the demo, available to everyone. - Blue noise dithering for single scattering
- The other two applications of blue noise dithering that I discussed in my earlier blog post are also part of this demo:
[Dithering](http://momentsingraphics.de/BlueNoise.html#dithering)is used for all single scattering techniques and[jittering](http://momentsingraphics.de/BlueNoise.html#jittering)improves the perceived quality of ray marching. - Micro-optimization for moment shadow mapping
- The code at the core of moment shadow mapping left potential for a micro-optimization that I had overlooked for a long time. The old code looks like this:
- Proper use of unorm float
- I hear that
[using](https://twitter.com/AndrewLauritzen/status/854035851256356864). Thus, it is a good thing that the new version of the demo no longer does that for the compute shaders used in single scattering.`RWTexture2D<float>`

for fixed-point formats is wrong

## Screenshots

In case you aren't convinced to click the [download link](http://momentsingraphics.de/Media/HPG2017/NonLinearMSMDemo.zip) yet, here are some screenshots and the flash forward for the [GDCE 2016 lecture](http://momentsingraphics.de/GDCEurope2016.html).

## Bug reports

Given the large number of available options and their potential combinations, full testing is difficult. Not all combinations are supposed to give good results but the demo should not crash. Bug reports via email or in the comments are welcome.