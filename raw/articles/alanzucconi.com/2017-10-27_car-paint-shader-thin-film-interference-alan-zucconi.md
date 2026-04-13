---
title: 'Car Paint Shader: Thin-Film Interference - Alan Zucconi'
url: https://www.alanzucconi.com/2017/10/27/carpaint-shader-thin-film-interference/
author: Alan Zucconi
published: '2017-10-27'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post completes the journey started in [The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/2017/07/25/the-mathematics-of-thin-film-interference/), by explaining how to turn the equations previously presented into actual shader code.

![](../../assets/5a696e977d36b279.gif)

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

In the previous post, we derived the equations that govern the process of thin-film interference. In a nutshell, this is an optical phenomenon that occurs when light “bounces” inside a medium which thickness is comparable to the light wavelength.

When this happens, there is a chance that some of the light immediately reflected off the surface will end up interfering with the light refracted inside the medium.

![](../../assets/0d1cda8dc6f2227b.png)


![](../../assets/0d1cda8dc6f2227b.png)

Because the two rays travels different lengths, they might end up off-phase. This means that even if the wavelengths started at the same phase, by the time both rays leave the material surface, their phases might be out of alignment.

This situation causes some wavelengths to interfere constructively, and some to interfere destructively. This means that some colours will be amplified, while other will cancel each other out. As a result, this effect causes unusual reflections, which are strongly dependent on both the view angle and the light angle.

In real life, this effect is predominantly visible in soap bubbles, which displays beautiful iridescent colours.

![](../../assets/97701778f9329091.jpg)


![](../../assets/97701778f9329091.jpg)

The effect is also commonly seen in oil spills, and are predominant in certain metals such as bismuth. In the latter, this is due to the fact that the entire surface is covered in a thin film of [bismuth(III) oxide](https://en.wikipedia.org/wiki/Bismuth(III)_oxide). Companies like The Bismuth Smiths have found a way to control the thickness of this oxidised layer, allowing them to master full control over the colour of those crystals.

More notoriously, thin-film interference is exploited in many iridescent car paints, such as the ones seen in this video:

### Implementation

The quickest way to implement this effect is to retrofit the existing iridescent shader created in part 2 of the [CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/2017/07/15/cd-rom-shader-2/) series. This is because most of the code is identical, with the small exception of the `LightingDiffraction`

function which will need to implement the new equations.

In the previous tutorial, we have seen the mathematical condition necessary for thin-film to occur for a given wavelength. Its wavelength (![Rendered by QuickLaTeX.com w](../../assets/bdbb99d128802679.png)

![Rendered by QuickLaTeX.com n_2 2 d \cos{\theta_R}](../../assets/7666812b18c5c09a.png)



: the refractive index of air,

: the refractive index of the thin-film,

: the refractive index of the material,

: the thickness of the thin-film,

the angle of reflection,

the angle of refraction inside the medium.

as seen in this diagram:

![](../../assets/0d1cda8dc6f2227b.png)


![](../../assets/0d1cda8dc6f2227b.png)

Our shader code, has only access to the light direction ![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com V](../../assets/c746ecbc0d34d082.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com \cos{\theta_L}](../../assets/3d47ceee1205dd57.png)


Finding the value of ![Rendered by QuickLaTeX.com \theta_R](../../assets/b01705fffc17ae84.png)

[Snell’s law](https://en.wikipedia.org/wiki/Snell%27s_law):

![Rendered by QuickLaTeX.com \[n_1 \sin{\theta_L} = n_2 \sin{\theta_R}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f1fa61de5820e1d803f1ee8111cc03eb_l3.png)


from which we can easily extract ![Rendered by QuickLaTeX.com \theta_R](../../assets/b01705fffc17ae84.png)


![Rendered by QuickLaTeX.com \[\sin{\theta_R} = \frac{n_1}{n_2} \sin{\theta_L}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a0ed842669c99bda807196658bf6df5a_l3.png)


![Rendered by QuickLaTeX.com \[\theta_R = asin{\left(\frac{n_1}{n_2} \sin{\theta_L}\right)}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-645981b76c2be11ac771bc25cd43cecd_l3.png)


In shader code, this becomes:

// --- Diffraction grating effect --- float3 L = gi.light.dir; float3 V = viewDir; float3 N = worldNormal; // Reminder: // thetaL = angle from L to N // thetaR = angle from reflected L inside material to N // From Snell's Law: // N1 * sin(thetaL) = N2 * sin(thetaR) float cos_thetaL = dot(N, L); float thetaL = acos(cos_thetaL); float sin_thetaR = (_N1 / _N2) * sin(thetaL); float thetaR = asin(sin_thetaR);

We can now use thin-film interference condition to find if a given wavelength is reflected back to the viewer:

float u = _N2 * 2 * d * abs(cos(thetaR)); fixed3 color = 0; for (int n = 1; n <= _Order; n++) { // Constructive interference float wavelength = u / n; color += spectral_zucconi6(wavelength); } color = saturate(color);

Here, we have used the same trick used in the CR-ROM shader. Instead of looping through all possible wavelengths (calculating if each ![Rendered by QuickLaTeX.com w](../../assets/bdbb99d128802679.png)

![Rendered by QuickLaTeX.com n_2 2 d \cos{\theta_R}](../../assets/7666812b18c5c09a.png)

`u`

in the code).

This, unfortunately, is not enough to get to the real effect. There is only a small problem we need to fix. Under certain circumstances, the phase can shift by 180 degrees. This happens when a ray of light travels from a material to another, and the first refractive index is lower than the second.

Our code needs to check if this shift happens on both reflections:

// Phase shift? // A phase shift of 180 degrees occurs on the reflected ray when // travelling from A to B AND NA < NB float shift = 0; if ( // Phase shift of first ray (_N1 < _N2) != // Phase shift of second ray (_N2 < _N3) ) shift += 0.5;

Once we have the shift, we can simply add it to `n`

to obtain the correct phase shift that light goes through when bouncing into the thin-film.

![](../../assets/772a6fd9a45ffd73.png)

[expand title=”❓ How can I use my own colours for the reflection?”]

You can’t. Not if you want a physically based effect. That being said, you can replace the `spectral_zucconi6`

function with a texture ramp of your choice. By doing this, you can change the rainbow reflection into one you like better.

However, doing so causes the effect to lose any connection with the physical mechanism that causes thin-film interference. In such a case, you might be better to just fake the effect entirely, for instance using a fake BRDF shader like the one presented in [Iridescence on mobile](https://www.alanzucconi.com/2017/07/21/iridescence-on-mobile/), which bakes the reflection into an easily editable texture.

![](../../assets/ee856237aa36dd64.png)


![](../../assets/ee856237aa36dd64.png)

[/expand]

#### Conclusion

This tutorial completes the series about iridescent material.

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
**Car Paint Shader: Thin-Film Interference**

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package for the CD-ROM Shader effect on ** Patreon**.

## Leave a Reply Cancel reply