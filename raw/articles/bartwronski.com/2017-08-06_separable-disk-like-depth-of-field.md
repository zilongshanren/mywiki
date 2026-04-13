---
title: Separable disk-like depth of field
url: https://bartwronski.com/2017/08/06/separable-bokeh/
published: '2017-08-06'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

This is a short note accompanying shadertoy: [https://www.shadertoy.com/view/lsBBWy](https://www.shadertoy.com/view/lsBBWy) .

It is direct implementation of [“Circularly symmetric convolution and lens blur” by Olli Niemitalo](http://yehar.com/blog/?p=1495) (no innovation on my side, just a *toy* implementation) and got inspired by Kleber Garcia’s Siggraph 2017 presentation [“Circular Separable Convolution Depth of Field”](http://dl.acm.org/citation.cfm?id=3085022).

### Why?

For depth of field effect, Gaussian blurs are seen artistically as “boring”, while hexagonal DoF (popular few years ago) can be subjectively not attractive (artificial, cheap camera qualities). I wrote a bit [about bokeh, DoF and some crazy implementation in Witcher 2 in the past](https://bartwronski.com/2014/04/07/bokeh-depth-of-field-going-insane-part-1/). Working on Far Cry 4 and other titles, I used a different approach – [scatter as gather “stretched” Poisson bokeh](https://bartwronski.com/2014/12/09/designing-a-next-generation-post-effects-pipeline/) to compute DoF together with motion blur and at the same time.

Circular kernels can be very expensive; prone to noise, ringing etc. One can try to approximate them, like [Guerilla Games in Michal Valient’s Killzone presentation](https://www.slideshare.net/guerrillagames/killzone-shadow-fall-demo-postmortem), undersample with blur afterwards like [Crytek in Tiago Sousa’s presentation](http://www.crytek.com/download/Sousa_Graphics_Gems_CryENGINE3.pdf), or try to use some separable approaches like [Colin Barré-Brisebois](https://colinbarrebrisebois.com/2017/04/18/hexagonal-bokeh-blur-revisited/).

Unfortunately, there are no circularly symmetric separable filters other than Gaussian filter in real domain. However, in complex domain, one can find whole family of functions (complex phasors multiplied by Gaussian “bell”) that their magnitude is! This is what Olli Niemitalo’s post describes and introduces some “fitted” functions to approximate disk DoF.

### Results – quality

As a proof-of-concept, I implemented it here: https://www.shadertoy.com/view/lsBBWy . It has a version with a single component and a version with two components (“harmonics”).

Version with a single component produces quite strong ringing, but much more “pronounced” bokeh than Gaussian one:

![circular_vs_gaussian](../../assets/7a7e61491eccc627.gif)

Circular bokeh single component approximation vs Gaussian.

Version with two components is going to be twice more expensive memory and ALU-wise, but doesn’t have those artifacts so strong:

![circular_two_vs_one](../../assets/f67dab586e90acf5.gif)

Two component vs single component approximation. Notice less ringing and smaller passband – almost perfect, circular shape.

I personally don’t think this ringing or “donut hole” is unpleasant at all; IMO it resembles some older lenses with “busy bokeh” and is something we simulated in Witcher on purpose:

![](../../assets/01941bee5c987a55.jpg)

Witcher 2 artistic “busy bokeh”.

![ND7_1568](../../assets/3e7f19b1c1476b00.jpg)

Real world lens “busy bokeh” with some ringing visible.

### Results – implementation / performance

Shader toy implementation I provided is obviously not optimal. Recomputing weights and their sum is very wasteful; most of this can be precomputed and stored in an uniform / constant buffer. Instead I stored most of them in first texture / buffer (“Buffer A”).

If we exclude weights, per every component first (“horizontal”) pass requires a “simplified” real times complex multiply and accumulate (2 madds, one per real and one per imaginary component).

Second (“vertical”) pass requites full complex multiplies and accumulates – however after applying optimization from Olli we can keep real component only – (2 madds).

So assuming that there are N taps in both horizontal and vertical directions, every component needs roughly 4**N “full rate”/simple** instructions – not bad at all. For two components it’s **8N instructions** . Both variation just read normal amounts of memory in the first pass (one fetch per tap), but on 2nd pass have either 2x or 4x more memory bandwidth required.

Similarly larger are the storage costs – every RGB channel is multiplied by 2 and by number of components. So using a single component we’d need 6 floating point channels (that can get negative – complex phasor!), for two components 12, so probably 4 RGBA16F textures.

In general, like with many post effects memory bandwidth is definitely a concern here; this technique requires even more of it and can get pretty expensive, but most blurring can be done in local / groupshared memory in compute shaders; and one can do some optimizations like blurring in YCoCg space and storing chroma components in lower res etc. So in general I definitely think it’s practical and cool approach.

In general I really like this technique, I don’t know if I’d use it in practice (still see lots of benefit in combining DoF and MB), but find it really beautiful and elegant, especially maths behind it. 🙂

### References

“*Circularly symmetric convolution and lens blur*“, Olli Niemitalo [http://yehar.com/blog/?p=1495](http://yehar.com/blog/?p=1495)

*“Circular separable convolution depth of field”*, Kleber Garcia [http://dl.acm.org/citation.cfm?id=3085022](http://dl.acm.org/citation.cfm?id=3085022)

“*Killzone: Shadow Fall Demo Postmortem*“, Michal Valient [https://www.slideshare.net/guerrillagames/killzone-shadow-fall-demo-postmortem](https://www.slideshare.net/guerrillagames/killzone-shadow-fall-demo-postmortem)

“*Graphic gems of CryEngine 3*“, Tiago Sousa [http://www.crytek.com/download/Sousa_Graphics_Gems_CryENGINE3.pdf](http://www.crytek.com/download/Sousa_Graphics_Gems_CryENGINE3.pdf)

“*Hexagonal Bokeh Blur Revisited*“, Colin Barré-Brisebois [https://colinbarrebrisebois.com/2017/04/18/hexagonal-bokeh-blur-revisited/](https://colinbarrebrisebois.com/2017/04/18/hexagonal-bokeh-blur-revisited/)

Pingback: Circularly symmetric convolution and lens blur « iki.fi/o

Pingback: 各种Depth of Field « Babylon Garden