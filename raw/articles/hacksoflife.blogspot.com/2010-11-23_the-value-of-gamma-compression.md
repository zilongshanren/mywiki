---
title: The Value Of Gamma Compression
url: http://hacksoflife.blogspot.com/2010/11/value-of-gamma-compression.html
author: Benjamin Supnik
published: '2010-11-23'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The answer is: not at 8 bits, and definitely not with DXT compression.

The following images show a gray-scale bar, quantized to: 16, 8, 6, and 5 bits per channel. (16-bits per channel would be typical of a floating point, HDR, or art asset pipeline, 8-bits is what most apps will have to run on the GPU, and 5/6 bits simulate the banding in the key colors of DXT-compressed textures, which are 5-6-5.)

![](../../assets/475f1f8722ff78e3.png)


![](../../assets/475f1f8722ff78e3.png)

![](../../assets/05efa79013d9da04.png)


![](../../assets/05efa79013d9da04.png)

![](../../assets/333c2453dd3ef221.png)


![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEivbI3zVltPStU6wARc9eUg3sSvtH0vC3rjbtLc99hcNa6GPO3UPAWGqYxm0NEzd0D5Dc6HH4C8ACXvZ_e1zn9E1GYeArBwTrbOaMr1GxqwnbCa-1JBoH9RI9pWNbZAXhz7Hlm67dReX64V/s200/srgb_8.png)

![](../../assets/c17cc2c9feec5a5b.png)


![](../../assets/c17cc2c9feec5a5b.png)

In the images labeled "srgb" (gamma is 1.0) the colors are quantized in sRGB (non-linear) space. Becuase sRGB is perceptually even, the banding appears to be even to a human - it's a good use of our limits bits. 8-bit color is pretty much smooth, and artifacts are minimized for 5 and 6 bits (although we can definitely see some banding here.)

Now what happens if we quantize in linear space? You'd get this:

![](../../assets/b4c0ee99202a756c.png)


![](../../assets/b4c0ee99202a756c.png)

![](../../assets/cc5a7caadfa43643.png)


![](../../assets/cc5a7caadfa43643.png)

![](../../assets/633b5616b3b68d8c.png)


![](../../assets/633b5616b3b68d8c.png)

![](../../assets/8afca29aa0456c3a.png)


![](../../assets/8afca29aa0456c3a.png)

Note: the program generates these ramps in sRGB space (hence they are "evenly spaced", converts to linear, quantizes, then converts back. So this is what your textures would look like if your art assets were converted to and stored linearly.

What can we see? Well, if we have 16-bits per channel we're still okay. But at 8-bits (the normal way to send an uncompressed texture to the GPU) we have visible banding in the darker regions. This is because linear isn't an efficient way to space out limited bits for our eyes.

The situation is really bad for the 6 and 5-bit compressed textures; we have so little bandwidth that the entire dark side of the spectrum is horribly quantized.

The moral of the story (if there is one): gamma is your friend - it's non-linear, which is annoying for lighting shaders, but when you have 8 bits or less, it puts the bits where you need them.

## No comments:

## Post a Comment