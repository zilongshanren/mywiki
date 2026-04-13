---
title: The Mathematics of Rayleigh Scattering - Alan Zucconi
url: https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-3/
author: Alan Zucconi
published: '2017-10-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post introduces the Mathematics of Rayleigh Scattering, which is the optical phenomenon that causes the sky to appear blue. The equations derived in this tutorial will be translated into shader code in the next tutorial.

![](../../assets/488fe0db18d2fa0c.gif)

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) **Part 3.**[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472)- Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

You can **download** the **Unity package** for this tutorial at the bottom of the page.

#### Introduction

In the previous tutorial, we have derived an equation that provides a good framework to approximate atmospheric scattering in a shader. What we have omitted, however, is the fact that a single equation will not yield believable results. If we want an atmospheric shader that looks good, we have to step up our Maths.

The interaction between light and matter is extremely complex, and there is no easy way to fully describe it. Modelling atmospheric scattering is, in fact, exceptionally difficult. Part of the problem comes from the fact that the atmosphere is not a homogeneous medium. Both its density and composition change significantly as a function of the altitude, making it virtually impossible to come up with a “perfect” model.

This is why the scientific literature presents several models of scattering, each one designed to describe a subset of optical phenomena occurring under specific conditions. Most optical effects that planets exhibit can be reproduced by taking into consideration two different models: **Rayleigh scattering** and **Mie scattering**. Those two mathematical tools allow predicting how light scatters on objects of different size. The former models how light is reflected by the oxygen and nitrogen molecules that make up most of the air. The latter, models how light reflects on much larger compounds that are suspended in the lower atmosphere, such as pollen, dust and pollutants.

Rayleigh scattering causes the sky to be blue, and sunsets to be red. Mie scattering gives clouds their white colour. If you want to understand *how*, we’ll have to delve deeper into the mathematics of scattering.

#### Rayleigh Scattering

What is the fate of a photon that hits a particle? To answer this question, we first need to redefine it in a more formal way. Let’s imagine a ray of light travelling through empty space, suddenly colliding with a particle. The outcome of such a collision varies dramatically depending on the size of the particle and the colour of the light. If the particle is small enough (such as atoms and molecules) the behaviour of the light is best predicted by the **Rayleigh scattering**.

What happens is that a part of the light continues its journey unaffected. However, a small percentage of that original light interact with the particle and get scattered in all directions. Not all directions, however, receive an equal amount of light. Photons are more likely to pass straight through the particle or to bounce back. Conversely, the less likely outcome for a photon is being deflected by 90 degrees. Such a behaviour can be seen in the diagram below. The blue line shows the preferred directions for the scattered light.

![](../../assets/05c4fc3f44e15162.png)

This optical phenomenon is described mathematically by the **Rayleigh scattering equation** ![Rendered by QuickLaTeX.com S \left(\lambda, \theta, h \right )](../../assets/5fb7b0325e466e5c.png)

![Rendered by QuickLaTeX.com I_0](../../assets/2e533417c872eeba.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


![Rendered by QuickLaTeX.com \[I = I_0 \, S \left(\lambda, \theta, h\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-16c717f18c59923f5d9fd824672ad00d_l3.png)


![Rendered by QuickLaTeX.com \[S \left(\lambda, \theta, h\right ) =\frac{\pi^2 \left(n^2-1 \right )^2}{2}\underset{\text{density}}{\underbrace{\frac{\rho\left(h\right)}{N}}}\overset{\text{wavelength}}{\overbrace{\frac{1}{\lambda^4}}}\underset{\text{geometry}}{\underbrace{\left(1+\cos^2\theta \right )}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6530382caa329954b697579f0dc979b6_l3.png)


Where:


: the **wavelength**of the incoming light;

: the **scattering angle**;

: the **altitude**of the point;

: the **refractive index**of air;

: the **molecular number density**of the standard atmosphere. This is the number of molecules per cubic metre;

: the **density ratio**.This number is equal to

at sea level, and decreases exponentially with

. There is a lot to say about this function, and we will do it in a future post of this series.

The first thing we have noticed about the Rayleigh scattering is that certain directions receive more light than others. The second important aspect is that the amount of light scattered is strongly dependent on the wavelength ![Rendered by QuickLaTeX.com \lambda](../../assets/e4664a784ffb986a.png)

![Rendered by QuickLaTeX.com S \left(\lambda, \theta\right, 0 )](../../assets/66f9bff74c36d9bf.png)

![Rendered by QuickLaTeX.com S](../../assets/4b8b5ff505466deb.png)

![Rendered by QuickLaTeX.com h=0](../../assets/c046ce8a19a8027c.png)

**scattering at sea level**.

The image below shows a rendering of the scattering coefficients for a continuous range of wavelength/colour of the visible spectrum (code available on [ShaderToy](https://www.shadertoy.com/view/4tsyWs)).

![](../../assets/c8fdb1e23a40ba2d.png)

The centre of the image appears is black because wavelengths in that range are outside the visible spectrum.

#### Rayleigh Scattering Coefficient

The equation for the Rayleigh scattering indicates how much light is scattered towards a particular direction. It does not tell, however, how much energy is scattered in total. To calculate that, we need to take into account the energy dispersion in *all* directions. Such a derivation is not for the faint-hearted; if you are not comfortable with advanced Calculus, this is the result:

![Rendered by QuickLaTeX.com \[\beta \left(\lambda, h \right )=\frac{8\pi^3 \left(n^2-1 \right )^2}{3}\frac{\rho\left(h\right)}{N}\frac{1}{\lambda^4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-3906bff30524399c8699a8f74f0b771c_l3.png)


Where ![Rendered by QuickLaTeX.com \beta \left(\lambda, h \right )](../../assets/e8172f9798b752ec.png)

**Rayleigh scattering coefficient**.

If you have read the previous part of this tutorial, you might have guessed that ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

**extinction coefficient** used in the definition of the transmittance ![Rendered by QuickLaTeX.com T\left(\overline{AB}\right)](../../assets/6bafaed8c37a9efd.png)

![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)


Unfortunately, calculating ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com \beta \left(\lambda\right )](../../assets/8a19b5c5c565820c.png)

**Rayleigh scattering coefficient as sea level** (![Rendered by QuickLaTeX.com h=0](../../assets/c046ce8a19a8027c.png)


![Rendered by QuickLaTeX.com \[\beta \left(\lambda \right )=\frac{8\pi^3 \left(n^2-1 \right )^2}{3}\frac{1}{N}\frac{1}{\lambda^4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d3f6de95e52ed2d25b9e218bbbcae3e0_l3.png)


This new equation provides yet another way to understand how different colours of light get scattered. The chart below shows the amount of scattering light is subjected to, as a function of its wavelength.

It is the strong relationship between the scattering coefficient ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com \lambda](../../assets/e4664a784ffb986a.png)


With the same reasoning, we can understand why the sky appears blue. The light from the sun arrives with a specific direction. However, its blue component is scattered in every direction. When you are looking at the sky, blue light is coming from every direction.

#### Rayleigh Phase Function

The original equation that describes the Rayleigh scattering, ![Rendered by QuickLaTeX.com S \left(\lambda, \theta\right )](../../assets/7118b6a03f771f53.png)

![Rendered by QuickLaTeX.com \beta \left(\lambda\right )](../../assets/8a19b5c5c565820c.png)


![Rendered by QuickLaTeX.com \[S \left(\lambda, \theta, h\right ) = \beta \left(\lambda, h\right ) \gamma \left(\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-38f9fec62437c856079f4f548b2fb599_l3.png)


This new quantity ![Rendered by QuickLaTeX.com \gamma \left(\theta\right)](../../assets/fac2895dc641cc65.png)

![Rendered by QuickLaTeX.com S \left(\lambda, \theta, h\right )](../../assets/9aaae65a504f6660.png)

![Rendered by QuickLaTeX.com \beta \left(\lambda\right )](../../assets/8a19b5c5c565820c.png)


![Rendered by QuickLaTeX.com \[\gamma \left(\theta\right) = \frac{S \left(\lambda, \theta, h\right )} {\beta \left(\lambda\right )}=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0af034bee7201514330efa34476a17b9_l3.png)


![Rendered by QuickLaTeX.com \[=\underset{S \left(\lambda, \theta, h\right )}{\underbrace{\frac{\pi^2 \left(n^2-1 \right )^2}{2}\frac{\rho\left(h\right)}{N}\frac{1}{\lambda^4}\left(1+\cos^2\theta \right )}}\,\underset{\frac{1}{\beta \left(\lambda\right )}}{\underbrace{\frac{3}{8\pi^3 \left(n^2-1 \right )^2}\frac{N}{\rho\left(h\right)}\lambda^4}}=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-35976d9a9d5e2ee0557ad706dd13588f_l3.png)


![Rendered by QuickLaTeX.com \[= \frac{3}{16\pi} \left(1+\cos^2 \theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c3ed66f2189ac896babfc524304b2f02_l3.png)


You can see that this new expression does not depend on the wavelength of the incoming light. This might seem counter-intuitive, since we definitely know that the Rayleigh scattering affects shorter wavelenghts more.

What ![Rendered by QuickLaTeX.com \gamma \left(\theta\right)](../../assets/fac2895dc641cc65.png)

![Rendered by QuickLaTeX.com \frac{3}{16\pi}](../../assets/df707bc1fa73b991.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com 4\pi](../../assets/c91cc6e73a2fbf03.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


We will see in the upcoming parts how separating these two components will allow deriving more efficient equations.

#### A Quick Recap

**Rayleigh scattering equation**: indicates the ratio of light that is deflected in the direction

. The intensity of the scattering depends on the wavelength

of the incoming light.

![Rendered by QuickLaTeX.com \[S \left(\lambda, \theta, h\right ) =\frac{\pi^2 \left(n^2-1 \right )^2}{2}\frac{\rho\left(h\right)}{N}\frac{1}{\lambda^4}\left(1+\cos^2\theta \right )\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-1e4f445c777056e9e816bb47f1610d88_l3.png)


Also:

![Rendered by QuickLaTeX.com \[S \left(\lambda, \theta, h\right ) = \beta \left(\lambda,h \right ) \gamma\left(\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b4d80f0ee6d96a22d2ea2b309dbbeee9_l3.png)


**Rayleigh scattering coefficient**: it indicates the ratio of light that is lost to scattering after a single collision.

![Rendered by QuickLaTeX.com \[\beta \left(\lambda,h \right )=\frac{8\pi^3 \left(n^2-1 \right )^2}{3}\frac{\rho\left(h\right)}{N}\frac{1}{\lambda^4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fb71b93508ed39ebe75a5a530afdcd59_l3.png)


**Rayleigh scattering coefficient at sea level**: it is equivalent to

. Creating this additional coefficient will be very helpful to derive more efficient equations.

![Rendered by QuickLaTeX.com \[\beta \left(\lambda \right )=\beta \left(\lambda,0 \right )=\frac{8\pi^3 \left(n^2-1 \right )^2}{3}\frac{1}{N}\frac{1}{\lambda^4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ecbd3541067e34eb8702dc44dfc17cd0_l3.png)


If we consider the wavelengths which loosely maps to red, green and blue colours, we obtain the following results:

![Rendered by QuickLaTeX.com \[\beta\left(680nm\right) = 0.00000519673\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-81cd42dab446959f2204dbd758913dcd_l3.png)


![Rendered by QuickLaTeX.com \[\beta\left(550nm\right) = 0.0000121427\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a2c82b3cb20c2dc6928b40421b8e61e2_l3.png)


![Rendered by QuickLaTeX.com \[\beta\left(440nm\right) = 0.0000296453\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a6282614241a20505bb063bf0d49012d_l3.png)


These results are calculate assuming ![Rendered by QuickLaTeX.com h=0](../../assets/c046ce8a19a8027c.png)

![Rendered by QuickLaTeX.com \rho=1](../../assets/da8790161374ed0b.png)


**Rayleigh phase function**: controls the scattering geometry, which indicates the relative ratio of light lost in a particular direction. The

coefficient serves as a normalisation factor, so that the integral over a unit sphere is

.

![Rendered by QuickLaTeX.com \[\gamma\left(\theta\right)= \frac{3}{16\pi} \left(1+\cos^2 \theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-54afa0038519da143e8e238ec4ad0b78_l3.png)


**Density ratio**: this is a function that is used to model the density of the atmosphere. It will be formally introduced in a future post. If you do not mind Maths spoilers, it is defined as:

![Rendered by QuickLaTeX.com \[\rho\left(h\right)=exp\left\{-\frac{h}{H}\right\}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-282e393097c54e78375196187023c0d7_l3.png)


where ![Rendered by QuickLaTeX.com H=8500](../../assets/e4fa5f2d635d1bf8.png)

**scale height**.

### 📚 Recommended Books

#### Coming Next…

This tutorial introduced the concept and the Mathematics of Rayleigh Scattering. In the next one, we will explain how to model Earth’s atmosphere in an effective way. For now, we will only focus on the Rayleigh scattering. The last post in this series, [An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578), will complete the shader by adding a second type of scattering.

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) **Part 3.**[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472)- Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

A big thanks goes to [Stephen Lavelle](https://twitter.com/increpare), who kindly helped with the derivations.

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce the volumetric atmospheric scattering presented in this tutorial.

## Leave a Reply Cancel reply