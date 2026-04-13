---
title: 'Fractals 101: The Mandelbrot Set - Alan Zucconi'
url: https://www.alanzucconi.com/2016/08/23/fractals-101-mandelbrot/
author: Alan Zucconi
published: '2016-08-23'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of [Fractals 101](https://www.alanzucconi.com/2016/08/17/fractals-101/), a series of tutorial dedicated to fractals. This post will investigate two popular fractals: the Mandelbrot set and its 3D cousin, the Mandelbulb.

![mandelbulb](../../assets/536f76c950d84283.gif)


![mandelbulb](../../assets/536f76c950d84283.gif)

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[The Mandelbrot Set](https://www.alanzucconi.com#part1) - Part 2.
[Colouring the Fractal](https://www.alanzucconi.com#part2) - Part 3.
[The Mandelbulb](https://www.alanzucconi.com#part3) - Part 4.
[Visualising the Mandelbulb](https://www.alanzucconi.com#part4) [Conclusion](https://www.alanzucconi.com#conclusion)

The previous post in this series, [Fractals 101](https://www.alanzucconi.com/2016/08/17/fractals-101/), showed how fractals can be constructed by iteration. Fractals created this way have indeed an infinite complexity, but they are also very boring. Their strong self-similarity doesn’t really allow for any *interesting* complexity to arise. Luckily, this is not always the case. Most fractals appear in the most unexpected places, rewarding you with endless beauty.

One of the most famous fractals of this kind is the [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set). Firstly defined in the 1978 , it was later computed and visualised by the mathematician Benoit Mandelbrot in 1980. The Mandelbrot set arises from an extremely simple equation:

![Rendered by QuickLaTeX.com \[f_c\left(x\right)=x^2+c\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-69e72d5aefc79f8fc6e00a5dce6d1535_l3.png)


In order for this fractal to appear, both ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

*complex numbers*. This blog has dedicated an entire post on [Complex Numbers](https://www.alanzucconi.com/?p=4461), in the context of 2D rotations.

The complexity hidden in ![Rendered by QuickLaTeX.com f_c](../../assets/641677f816fe2475.png)

![Rendered by QuickLaTeX.com f_c](../../assets/641677f816fe2475.png)

![Rendered by QuickLaTeX.com f_c](../../assets/641677f816fe2475.png)

![Rendered by QuickLaTeX.com z=0](../../assets/b974f7edecdf339a.png)


![Rendered by QuickLaTeX.com \[z_0 =0\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-28ea17d89342c069a690180264be5073_l3.png)


![Rendered by QuickLaTeX.com \[z_1 = f_c\left(z_0\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-06282dcbefcbcba546d0d718ecd13d38_l3.png)


![Rendered by QuickLaTeX.com \[z_2 = f_c\left(z_1\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-195f1504db3b2f0cd880616893ab857f_l3.png)


![Rendered by QuickLaTeX.com \[z_3 = f_c\left(z_2\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-206eba1c21d62736dd4788e67f1cdffb_l3.png)


![Rendered by QuickLaTeX.com \[...\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-efc90af5e7b4839892888e829bfcc4a2_l3.png)


…and so on.

For any ![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

![Rendered by QuickLaTeX.com f_c\left(0\right)](../../assets/122a882e7fdb291a.png)

![Rendered by QuickLaTeX.com f_c](../../assets/641677f816fe2475.png)


At a first glance, this produces a black and white figure:

![322px-Mandelset_hires](../../assets/4371ab634c6e8805.png)

White points are the values of ![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

![Rendered by QuickLaTeX.com f_c\left(0\right)](../../assets/122a882e7fdb291a.png)

![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

![Rendered by QuickLaTeX.com f_c\left(0\right)](../../assets/122a882e7fdb291a.png)


The really interesting behaviour happens on the edge of the Mandelbrot set, where the white and black parts of the plane meet. Not only the edge exhibits self-similarity; it also hides an endless sea of complexity.

![Mandelbrot_zoom](../../assets/43d9651ccc939312.gif)

![Mandelbrot_sequence_new](../../assets/ee040114e8da137e.gif)

The original equation that defines the Mandelbrot set only allows for a black and white figure. Many coloured version of the Mandelbrot set exist, using several different technique. The most common relies on the speed at which ![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)


If you’re familiar with Shaders, the following code will allow you to calculate a Mandelbrot fractal. It requires ![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


float mandelbrot (float2 c) { float2 z = 0; float2 zNext; int i; for (i = 0; i < _MaxIterations; i ++) { // f(z) = z^2 + c zNext.x = z.x * z.x - z.y * z.y + c.x; zNext.y = 2 * z.x * z.y + c.y; z = zNext; // Bounded? if ( dist(z,float2(0,0)) > 2) break; } return i / float(_MaxIterations); }

The `mandelbrot`

function can be fed with the UV of a piece of geometry. Its return value can be used to sample a ramp texture. This allows a fine control over the final colour of the produced fractal.

It’s important to notice that ![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

![Rendered by QuickLaTeX.com z](../../assets/e0718681f6d9dd40.png)

![Rendered by QuickLaTeX.com z](../../assets/e0718681f6d9dd40.png)


![Rendered by QuickLaTeX.com \[z = x+\i y\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-98655fb7bb640e010edb2b90def85dd4_l3.png)


![Rendered by QuickLaTeX.com \[z^2 = z\cdot z = \left(x+\i y\right)\left(x+\i y\right)=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b282d59909ac4d3dbf1d9d476c22a91e_l3.png)


![Rendered by QuickLaTeX.com \[=x^2 + \i^2 y^2 + 2\i xy\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-1c55178fea3d838f7a5d4dc49494d49b_l3.png)


And, since ![Rendered by QuickLaTeX.com \i^2=-1](../../assets/51ad35c5c245eb66.png)


![Rendered by QuickLaTeX.com \[z^2 = x^2 - y^2 + 2\i xy\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7c66e7cd89400f53df0fb26d8a01ba99_l3.png)


The concept behind the Mandelbrot set has been subject of extensive research. While a 3D equivalent of the Mandelbrot set does not exist, Daniel White and Paul Nylander came up with a 3D shape that exhibits similar properties. This shape has been called the [Mandelbulb](https://en.wikipedia.org/wiki/Mandelbulb), since its similarity with a round bulb.

The logic behind its creation is similar to the one that generated the Mandelbrot set. Starting from zero, we iterate a 3D function ![Rendered by QuickLaTeX.com g_c\left(v\right)](../../assets/3321119d73927315.png)

![Rendered by QuickLaTeX.com v](../../assets/1bf6fd37becd9c3d.png)

![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)

![Rendered by QuickLaTeX.com v=\left[x,y,z\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5fcffe31ff27a8a610a64e1cadab340c_l3.png)


![Rendered by QuickLaTeX.com \[g_c\left(v\right) =\left[ r^n\sin \left( n\theta \right)\cos \left(n\phi\right) , r^n\sin \left(n\theta \right)\sin \left(n\phi\right), r^n\cos \left(n\theta\right)\right]\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ee3e6ea0afc0af80088f514b09ae0b15_l3.png)


With:

![Rendered by QuickLaTeX.com \[r=\sqrt{x^2+y^2+z^2}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5f5e24ef7709bfb9137dc3b0c83f3775_l3.png)


![Rendered by QuickLaTeX.com \[\phi=arctan\left(\frac{y}{x}\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b9399812364a1c9f35a1570fd3d75a0f_l3.png)


![Rendered by QuickLaTeX.com \[\theta=arccos\left(\frac{z}{r}\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fca96a00e3462803d477ce82bc50d53f_l3.png)


The parameters ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

*power factor* of the Mandelbulb, and it’s used to control its shape. The introduction of trigonometric functions are used to express the Mandelbulb in spherical coordinates. Exactly like we did before, the 3D points ![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)


![Rendered by QuickLaTeX.com \[v_0 =\left[0,0,0\right]\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-9894cfc8cba9ed921515d081d2f313f7_l3.png)


![Rendered by QuickLaTeX.com \[v_1 = g_c\left(v_0\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-baed75db62d691fcf2737b011ad7e1ec_l3.png)


![Rendered by QuickLaTeX.com \[v_2 = g_c\left(v_1\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-bbeabbf79ab47493e848f4a0d29e16b9_l3.png)


![Rendered by QuickLaTeX.com \[v_3 = g_c\left(v_2\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-07b246d9b72ea2901e33365b77f6bd20_l3.png)


![Rendered by QuickLaTeX.com \[...\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-efc90af5e7b4839892888e829bfcc4a2_l3.png)


stays bounded.

![1024px-Power_8_mandelbulb_fractal_overview](../../assets/01b2e77e59e9e914.jpg)

To give a better understanding of what the Mandelbulb looks like, I have created a 360 video that shows the birth of this fractal, slowly changing its power factor ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com 1.4](../../assets/65b1e1d23f3966d5.png)

![Rendered by QuickLaTeX.com 6](../../assets/365de9985eedaf99.png)


The Mandelbulb has been rendered inside out, using a volumetric shader in Unity. The 360 effect has been achieved using 3 cameras with a large field of view. All images are wrapped to an equirectangular projection using another shader. Despite being rendered at a very high resolution, the compression of YouTube makes some parts of video slightly blurred.

#### Other resources

- Part 1.
[Fractals 101](https://www.alanzucconi.com/?p=5445) - Part 2.
**Fractals 101: The Mandelbrot Set**

## Leave a Reply Cancel reply