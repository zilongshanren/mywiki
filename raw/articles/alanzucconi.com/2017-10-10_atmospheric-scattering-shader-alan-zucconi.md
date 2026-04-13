---
title: Atmospheric Scattering Shader - Alan Zucconi
url: https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-7/
author: Alan Zucconi
published: '2017-10-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/ee419a0421628a46.gif)

This tutorial finally concludes our journey to simulate Rayleigh Scattering for a planet’s atmosphere.

The next (and final) part will show how to change the shader to also include an additional type of scattering, known as Mie Scattering.

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) **Part 7.**[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793)- 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

You can **download** the **Unity package** for this tutorial at the bottom of the page.

#### Sampling the View Ray

Let’s recall the equation for the atmospheric scattering that we have recently derived:

![Rendered by QuickLaTeX.com \[I= I_S \sum_{P \in \overline{AB}} {S\left(\lambda, \theta, h\right) T\left(\overline{CP}\right) T\left(\overline{PA}\right) ds }\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7842ef411b4261d20fa42809f8ffcd8b_l3.png)


The amount of light that we receive is equal to the amount of light emitted from the sun, ![Rendered by QuickLaTeX.com I_S](../../assets/de81e6e81d28e2ea.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)


We could go one and implement that function directly in our shader. However, there are few optimisations that can be done. It was hinted, in a previous tutorial, that the expression could be simplified even further. The first step we can take is to decompose the scattering function into its two basic components:

![Rendered by QuickLaTeX.com \[S \left(\lambda, \theta, h\right ) = \beta \left(\lambda, h \right ) \gamma\left(\theta\right) = \beta \left(\lambda\right )\rho\left(h\right) \gamma\left(\theta\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0d83eead25b5ab2aeae45d557c79707f_l3.png)


The **phase function** ![Rendered by QuickLaTeX.com \gamma\left(\theta\right)](../../assets/5d352c329112cdd1.png)

**scattering coefficient at sea level** ![Rendered by QuickLaTeX.com \beta \left(\lambda\right )](../../assets/8a19b5c5c565820c.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com \lambda](../../assets/e4664a784ffb986a.png)


![Rendered by QuickLaTeX.com \[I = I_S \, \beta \left(\lambda\right ) \gamma\left(\theta\right) \sum_{P \in \overline{AB}} { T\left(\overline{CP}\right) T\left(\overline{PA}\right) \rho\left(h\right) ds }\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ffe4741935ecd4145dc3d7cbb318f65b_l3.png)


This new expression is mathematically equivalent to the previous one, but is more efficient to calculate since some of the most heavy parts have been taken out of the summation.

We are not ready to start implementing it. There are infinitely many points ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com I](../../assets/c2ab42bcab55cee7.png)

![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)

![Rendered by QuickLaTeX.com ds](../../assets/a15125f89deb0218.png)

![Rendered by QuickLaTeX.com ds](../../assets/a15125f89deb0218.png)


![](../../assets/4d9f4e36187e577f.png)

The number of segments in ![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)

**view samples**, since all segments lie on the view ray. In the shader, this will be the `_ViewSamples`

property. By having it as a property, it is accessible from the material inspector. This allows us to reduce the precision of the shader, in favour of its performance.

The following piece of code allows looping through all the segments in the atmosphere.

// Numerical integration to calculate // the light contribution of each point P in AB float3 totalViewSamples = 0; float time = tA; float ds = (tB-tA) / (float)(_ViewSamples); for (int i = 0; i < _ViewSamples; i ++) { // Point position // (sampling in the middle of the view sample segment) float3 P = O + D * (time + ds * 0.5); // T(CP) * T(PA) * ρ(h) * ds totalViewSamples += viewSampling(P, ds); time += ds; } // I = I_S * β(λ) * γ(θ) * totalViewSamples float3 I = _SunIntensity * _ScatteringCoefficient * phase * totalViewSamples;

The variable `time`

is used to keep track of how far we are from the origin point ![Rendered by QuickLaTeX.com O](../../assets/ab988e264adecb16.png)

`ds`

after each iteration.

#### Optical Depth PA

Each point along the view ray ![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)


![Rendered by QuickLaTeX.com \[I = I_S \, \beta \left(\lambda\right ) \gamma\left(\theta\right) \sum_{P \in \overline{AB}} \underset{\text{light contribution of}\,L\left(P\right)}{\underbrace{T\left(\overline{CP}\right) T\left(\overline{PA}\right) \rho\left(h\right) ds}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6159164ef26e68080360654572713a59_l3.png)


Like we did in the previous paragraph, let’s try to simplify it. We can expand the expression above even further, by replacing ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)


![Rendered by QuickLaTeX.com \[T\left(\overline{XY}\right) =\exp\left\{- \beta\left(\lambda\right)D\left(\overline{XY}\right)\right\}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fd2518012ab32a07346a32e231603925_l3.png)


The product of the transmittance over ![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)

![Rendered by QuickLaTeX.com \overline{PA}](../../assets/f1f3ce35da01d2ed.png)


![Rendered by QuickLaTeX.com \[T\left(\overline{CP}\right) T\left(\overline{PA}\right)=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-87457c0cc49da0c398a892e644c09c36_l3.png)


![Rendered by QuickLaTeX.com \[=\underset{T\left(\overline{CP}\right) }{\underbrace{\exp\left\{-\beta\left(\lambda\right)D\left(\overline{CP}\right)\right \}}} \,\underset{T\left(\overline{PA}\right) }{\underbrace{\exp\left\{-\beta\left(\lambda\right)D\left(\overline{PA}\right)\right \}}}=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ecd722c9a24ba9027f9ceb6a340ecc4c_l3.png)


![Rendered by QuickLaTeX.com \[=\exp\left\{-\beta\left(\lambda\right)\left(D\left(\overline{CP}\right)+D\left(\overline{PA}\right)\right)\right \}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5d98191b6fe66a309ba948042c6e900c_l3.png)


The **combined transmittance** is modelled as an exponential decay with which coefficient is the sum of the **optical depths** over the path travelled by the light (![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)

![Rendered by QuickLaTeX.com \overline{PA}](../../assets/f1f3ce35da01d2ed.png)

*scattering coefficient at sea level* (![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com h=0](../../assets/c046ce8a19a8027c.png)


The first quantity that we start calculating is the optical depth for the segment ![Rendered by QuickLaTeX.com \overline{PA}](../../assets/f1f3ce35da01d2ed.png)


![Rendered by QuickLaTeX.com \[D\left( \overline{PA}\right)=\sum_{Q \in \overline{PA}}{\exp\left\{-\frac{h_Q}{H}\right\}}\, ds\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-00d55fb340cb05b8a31ca9317b0547b6_l3.png)


If one had to implement this naively, we would create a function called `opticalDepth`

that samples points between ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com D\left( \overline{PA}\right)](../../assets/214893b79fa8032c.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

`opticalDepthSegment`

), and keep accumulating it in the for loop (`opticalDepthPA`

).

// Accumulator for the optical depth float opticalDepthPA = 0; // Numerical integration to calculate // the light contribution of each point P in AB float time = tA; float ds = (tB-tA) / (float)(_ViewSamples); for (int i = 0; i < _ViewSamples; i ++) { // Point position // (sampling in the middle of the view sample segment) float3 P = O + D * (time + viewSampleSize*0.5); // Optical depth of current segment // ρ(h) * ds float height = distance(C, P) - _PlanetRadius; float opticalDepthSegment = exp(-height / _ScaleHeight) * ds; // Accumulates the optical depths // D(PA) opticalDepthPA += opticalDepthSegment; ... time += ds; }

### ⭐ Recommended Unity Assets

#### Light Sampling

If we look back at the expression for the light contribution of ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)


![Rendered by QuickLaTeX.com \[L\left(P\right) =\underset{\text{combined transmittance}}{\underbrace{\exp\left\{-\beta\left(\lambda\right)\left(D\left(\overline{CP}\right)+D\left(\overline{PA}\right)\right)\right \}}}\, \underset{\text{optical depth of}\,ds}{\underbrace{\rho\left(h\right) ds}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-def5ac0e3e4d3338188bb0232139d31f_l3.png)


We will move the code that calculates the optical depth of the segment ![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)

`lightSampling`

. The name comes from the **light ray**, which is the segment that starts at ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)


The `lightSampling`

function, however, will not just calculate the optical depth of ![Rendered by QuickLaTeX.com \overline{CP}](../../assets/e54a81e37930d662.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)


![](../../assets/dfcfb96063476863.png)

In the diagram above, it’s easy to see that the light contribution of ![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

`lightSampling`

function will also check if the planet has been hit. This can be done by checking if the altitude of a point is negative.

bool lightSampling ( float3 P, // Current point within the atmospheric sphere float3 S, // Direction towards the sun out float opticalDepthCA ) { float _; // don't care about this one float C; rayInstersect(P, S, _PlanetCentre, _AtmosphereRadius, _, C); // Samples on the segment PC float time = 0; float ds = distance(P, P + S * C) / (float)(_LightSamples); for (int i = 0; i < _LightSamples; i ++) { float3 Q = P + S * (time + lightSampleSize*0.5); float height = distance(_PlanetCentre, Q) - _PlanetRadius; // Inside the planet if (height < 0) return false; // Optical depth for the light ray opticalDepthCA += exp(-height / _RayScaleHeight) * ds; time += ds; } return true; }

The function above first calculates the point ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

`rayInstersect`

. It then divides the segment ![Rendered by QuickLaTeX.com \overline{PA}](../../assets/f1f3ce35da01d2ed.png)

`_LightSamples`

segments of length `ds`

. The calculation for the optical depth is the same used in the outermost loop.

The function returns false if the planet has been hit. We can use this to update the missing code the outermost loop, replacing the `...`

.

// D(CP) float opticalDepthCP = 0; bool overground = lightSampling(P, S); if (overground) { // Combined transmittance // T(CP) * T(PA) = T(CPA) = exp{ -β(λ) [D(CP) + D(PA)]} float transmittance = exp ( -_ScatteringCoefficient * (opticalDepthCP + opticalDepthPA) ); // Light contribution // T(CPA) * ρ(h) * ds totalViewSamples += transmittance * opticalDepthSegment; }

Now that we have taken into account all the elements, our shader is complete.

#### Coming Next…

This post (finally!) completes the volumetric shader that simulates atmospheric scattering. So far, we have only taken into account the contribution of the Rayleigh scattering. There are many optical phenomena that cannot be explained with Rayleigh scattering alone. The next post will introduce a second type of scattering, which is known as Mie scattering.

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) **Part 7.**[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793)- 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce the volumetric atmospheric scattering presented in this tutorial.

## Leave a Reply Cancel reply