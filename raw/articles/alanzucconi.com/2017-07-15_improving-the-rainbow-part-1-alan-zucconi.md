---
title: Improving the Rainbow - Part 1 - Alan Zucconi
url: https://www.alanzucconi.com/2017/07/15/improving-the-rainbow/
author: Alan Zucconi
published: '2017-07-15'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Our journey to photorealism requires us to understand not only how light works, but also how we perceive colours. How many colours are in the rainbow? And why pink is not one of them? Those are some of the questions that this post will address.

![](../../assets/8cd3539bd485907c.png)

You can find the complete series here:

- Part 1.
[The Nature of Light](https://www.alanzucconi.com/?p=6630) - Part 2.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6703)(Part 1) - Part 3.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6806)(Part 2) - Part 4.
[Understanding Diffraction Grating](https://www.alanzucconi.com/?p=6651) - Part 5.
[The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682) - Part 6.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6767)(Part 1) - Part 7.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6791)(Part 2) - Part 8.
[Iridescence on Mobile](https://www.alanzucconi.com/?p=6819) - Part 9.
[The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/?p=6821) - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

A link to **download** the **Unity project** used in this series is also provided at the end of the page.

#### Introduction

This post will introduce the most common techniques used in computer graphics to reproduce the colours that appear in the rainbow. While this might seem a useless exercise, it actually has very practical applications. Each colour of the rainbow corresponds to a specific wavelength of light. This correspondence will allow us to simulate physically based reflections.

The second part of this post, [Improving the Rainbow – Part 2](https://www.alanzucconi.com/?p=6806&preview=true), will introduce a novel approach that is highly optimised for shaders, yet yielding the best results so far (see below).

A comparative WebGL versions of all the techniques discussed in this tutorial can be found on [Shadertoy](https://www.shadertoy.com/view/ls2Bz1).

#### Colour Perception

The **retina** is the part of the eye that is specialised in the detection of light. In there, **cone cells** are able to send signals to the brain when they detect certain wavelengths of light. Since light is a wave in the electromagnetic field, cone cells work under the same principles that allow us to detect radio waves. Cone cells are, *de-facto*, tiny antennas. If you have studied electronics, you should know that the length of an antenna is related to the wavelength it captures. This is why the human eye features three different types of cone cells: short, medium and long. Each one is specialising at detecting a particular range of wavelengths.

![](../../assets/c6ef5790a1e32198.png)

The diagram above shows how strongly each cone cell type reacts to different wavelengths. When one of those cone types activate, the brain interprets their signal as colour. Despite what often stated, the short, medium and long cone cells do not represent specific colours. More correctly, each type responds differently to a different range of colours.

It is incorrect to assume that short, medium and long cone cells detected blue, green and red light. Despite this, many textbooks (and even shaders!) rely on this assumption to get a relatively acceptable approximation of an otherwise very complex phenomenon.

#### Spectral Colour

If we want to reproduce the physical phenomena that make iridescence possible, we need to re-think the way we store and manipulate colours in a computer. When you create a light source in Unity (or any other game engine) you can specify its colour, as a mixture of three primary components: red, green and blue. While it is certainly true that red, green and blue lights can be mixed up to create all the visible colours, this is not how light *really* works at its most fundamental level.

A light source can be modelled as a constant stream of photons. Photons which carry different amounts of energy are perceived by our eyes as different colours. However, there is no “white photon”. It is the sum of many photons, each one with a different wavelength, that gives a light its white appearance.

What we will need for the future posts in this series is being able to talk about the very building blocks of light. When we will talk about “wavelengths” you should think about specific colours of the rainbow. This post shows different approaches to make that connection possible. What we want to achieve is, ultimately, a function that given the wavelength of a light wave returns its perceived colour:

fixed3 spectralColor (float wavelength);

For the rest of this series, we will express wavelength in nanometres (a billionth of a meter). The human eye can perceive lights ranging from 400 nm to 700 nm. Wavelengths outside that range do exist but are not perceived as colours.

#### Spectral Map

The following image shows how the human eye perceives wavelengths ranging from 400 nanometers (blue) to 700 nanometers (red).

![](../../assets/26e1033946504ea4.png)

It is easy to see that the distribution of colours in the visible spectrum is highly nonlinear. If we plot, for each wavelength, the respective R, G and B components of its perceived colour, we will end up with something like this:

![](../../assets/9ebe6c01c6c8cb7a.png)

There is no simple function that can fully reproduce that curve. The easiest, cheapest approach we can implement is simply using that texture in our shader as a mean to map wavelengths to colours.

The first step is to make a new texture available in the shader. We can do this by adding a texture property to the `Properties`

block a new shader.

// Properties Properties { ... _SpectralTex("Spectral Map (RGB)",2D) = "white" {} ... } // Shader code SubShader { ... CGPROGRAM ... sampler2D _SpectralTex; ... ENDCG ... }

Our `spectralColor`

function only remap wavelengths in the range [400,700] onto UV coordinates in the range [0,1]:

fixed3 spectral_tex (float wavelength) { // wavelength: [400, 700] // u: [0, 1] fixed u = (wavelength -400.0) / 300.0; return tex2D(_SpectralTex, fixed2(u, 0.5)); }

In this specific case, we don’t need to enforce wavelength in the range [400, 700]. If the spectral texture is imported with **Repeat: Clamp**, any value outside that range will automatically appear as black.

#### JET Colour Scheme

Sampling a texture might seem a good idea. However, it could drastically slow down put shader. We will see our critical this is in the post on CD-ROMs iridescence where each pixel would require several texture samples.

There are several functions that approximate the distributions of colours of the light spectrum. One of the simplest is possibly the JET colour scheme. This is the default colour scheme in MATLAB, and it was originally devised to better visualise astrophysical fluid jet simulations from the National Center for Supercomputer Applications.

![](../../assets/cb9a448090a036e3.png)

The JET colour scheme is the combination of three different curves: a blue, green and red one. This is clearly highlighted by colour decomposition:

![](../../assets/6ce35437e28e0045.png)

We can easily reimplement the JET colour scheme by writing the equations of the lines that make up the diagram above.

// MATLAB Jet Colour Scheme fixed3 spectral_jet(float w) { // w: [400, 700] // x: [0, 1] fixed x = saturate((w - 400.0)/300.0); fixed3 c; if (x < 0.25) c = fixed3(0.0, 4.0 * x, 1.0); else if (x < 0.5) c = fixed3(0.0, 1.0, 1.0 + 4.0 * (0.25 - x)); else if (x < 0.75) c = fixed3(4.0 * (x - 0.5), 1.0, 0.0); else c = fixed3(1.0, 1.0 + 4.0 * (0.75 - x), 0.0); // Clamp colour components in [0,1] return saturate(c); }

The R, G and B values of the resulting colour are capped in the range [0,1] using the Cg function `saturate`

. If your camera is set to HDR ([High Dynamic Range Rendering](https://docs.unity3d.com/Manual/HDR.html)), this is necessary to avoid colours with components that go above 1.

Please, note that if you want to adhere strictly to the JET colour scheme, values outside the visible range will not be black.

#### Bruton Colour Scheme

Yet another approach to convert wavelengths to visible colours is provided by Dan Bruton in “[Approximate RGB values for Visible Wavelengths](http://www.physics.sfasu.edu/astro/color/spectra.html)“. Similarly to what happened for the JET colour scheme, he starts from an approximated distribution of how colours are perceived.

![](../../assets/c31b198ee6555dab.png)

His approach, however, better approximates the activity of the long cone cells, showing a more violet hue towards the lower end of the visible spectrum:

![](../../assets/b7c54bcd9758ff6e.png)

Which translated into the following code:

// Dan Bruton fixed3 spectral_bruton (float w) { fixed3 c; if (w >= 380 && w < 440) c = fixed3 ( -(w - 440.) / (440. - 380.), 0.0, 1.0 ); else if (w >= 440 && w < 490) c = fixed3 ( 0.0, (w - 440.) / (490. - 440.), 1.0 ); else if (w >= 490 && w < 510) c = fixed3 ( 0.0, 1.0, -(w - 510.) / (510. - 490.) ); else if (w >= 510 && w < 580) c = fixed3 ( (w - 510.) / (580. - 510.), 1.0, 0.0 ); else if (w >= 580 && w < 645) c = fixed3 ( 1.0, -(w - 645.) / (645. - 580.), 0.0 ); else if (w >= 645 && w <= 780) c = fixed3 ( 1.0, 0.0, 0.0 ); else c = fixed3 ( 0.0, 0.0, 0.0 ); return saturate(c); }

#### Bump Colour Scheme

Both the JET and Bruton colour schemes use discontinuous functions. As such, they feature quite sharp colour variations. Moreover, they do not fade to black outside the visible range. The book GPU Gems addresses those issue by replacing the sharp lines of the previous colour schemes with more gentle *bumps*. Each bump is simply a parabola of the type ![Rendered by QuickLaTeX.com y=1-x^2](../../assets/5cf4d36091e27bb2.png)


![Rendered by QuickLaTeX.com \[bump\left(x \right ) = \left\{\begin{matrix}0 & \left|x\right|>1 \\1-x^2 & \mathit{otherwise}\end{matrix}\right.\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e20d843d035b54eb00fb627cb9756e5f_l3.png)


The author, Randima Fernando, uses a bump for each colour component, arranged in the following way:

![](../../assets/c67323a6f0f08645.png)

![](../../assets/a1c63e04bf7c8aed.png)

We can write the following code:

// GPU Gems inline fixed3 bump3 (fixed3 x) { float3 y = 1 - x * x; y = max(y, 0); return y; } fixed3 spectral_gems (float w) { // w: [400, 700] // x: [0, 1] fixed x = saturate((w - 400.0)/300.0); return bump3 ( fixed3 ( 4 * (x - 0.75), // Red 4 * (x - 0.5), // Green 4 * (x - 0.25) // Blue ) ); }

An additional advantage of this colour scheme is that it does not use texture samples or branches, making it one of the best solution if you prefer performance over quality. At the end of this tutorial, you will see a revised version of this colour scheme which provides best performances while still yielding high fidelity of colours.

#### Spektre Colour Scheme

One of the most accurate colour scheme available has been made by Stack Overflow used [Spektre](https://stackoverflow.com/users/2521214/spektre). They explain their methodology in [RGB values of visible spectrum](https://stackoverflow.com/questions/3407942/rgb-values-of-visible-spectrum), where they sampled the blue, green and components of real data from the solar spectrum. Then, they fit individual intervals with simple functions. The result is presented in the following diagram:

![](../../assets/34b20dee3a33115f.png)

Which produces:

![](../../assets/d0a16d96b7cf412a.png)

And here is the code:

// Spektre fixed3 spectral_spektre (float l) { float r=0.0,g=0.0,b=0.0; if ((l>=400.0)&&(l<410.0)) { float t=(l-400.0)/(410.0-400.0); r= +(0.33*t)-(0.20*t*t); } else if ((l>=410.0)&&(l<475.0)) { float t=(l-410.0)/(475.0-410.0); r=0.14 -(0.13*t*t); } else if ((l>=545.0)&&(l<595.0)) { float t=(l-545.0)/(595.0-545.0); r= +(1.98*t)-( t*t); } else if ((l>=595.0)&&(l<650.0)) { float t=(l-595.0)/(650.0-595.0); r=0.98+(0.06*t)-(0.40*t*t); } else if ((l>=650.0)&&(l<700.0)) { float t=(l-650.0)/(700.0-650.0); r=0.65-(0.84*t)+(0.20*t*t); } if ((l>=415.0)&&(l<475.0)) { float t=(l-415.0)/(475.0-415.0); g= +(0.80*t*t); } else if ((l>=475.0)&&(l<590.0)) { float t=(l-475.0)/(590.0-475.0); g=0.8 +(0.76*t)-(0.80*t*t); } else if ((l>=585.0)&&(l<639.0)) { float t=(l-585.0)/(639.0-585.0); g=0.82-(0.80*t) ; } if ((l>=400.0)&&(l<475.0)) { float t=(l-400.0)/(475.0-400.0); b= +(2.20*t)-(1.50*t*t); } else if ((l>=475.0)&&(l<560.0)) { float t=(l-475.0)/(560.0-475.0); b=0.7 -( t)+(0.30*t*t); } return fixed3(r,g,b); }

#### Conclusion

This post provides an overview of some of the most common techniques to generate rainbow-like patterns in a shader. The second part of this post, [Improving the Rainbow – Part 2](https://www.alanzucconi.com/?p=6806&preview=true), will introduce a novel approach to solve this problem.

Name | Gradient |
| JET | ![]() |
| Bruton | ![]() |
| GPU Gems | ![]() |
| Spektre | ![]() |
| Zucconi | ![]() |
| Zucconi6 | ![]() |
| Visible | ![]() |

You can find the complete series here:

- Part 1.
[The Nature of Light](https://www.alanzucconi.com/?p=6630) - Part 2.
**Improving the Rainbow**(Part 1) - Part 3.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6806)(Part 2) - Part 4.
[Understanding Diffraction Grating](https://www.alanzucconi.com/?p=6651) - Part 5.
[The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682) - Part 6.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6767)(Part 1) - Part 7.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6791)(Part 2) - Part 8.
[Iridescence on Mobile](https://www.alanzucconi.com/?p=6819) - Part 9.
[The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/?p=6821) - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package for the CD-ROM Shader effect on [ Patreon](https://www.patreon.com/posts/13032957).

## Leave a Reply Cancel reply