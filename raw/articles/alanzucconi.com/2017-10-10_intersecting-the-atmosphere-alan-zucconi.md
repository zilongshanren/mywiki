---
title: Intersecting The Atmosphere - Alan Zucconi
url: https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-6/
author: Alan Zucconi
published: '2017-10-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/488fe0db18d2fa0c.gif)

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) **Part 6.**[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781)- Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

You can **download** the **Unity package** for this tutorial at the bottom of the page.

#### Intersecting the Atmosphere

As discussed before, the only way we can calculate the **optical depth** of a segment that passes through the atmosphere, is via a **numerical integration**. This means dividing out interval in smaller segments of length ![Rendered by QuickLaTeX.com ds](../../assets/a15125f89deb0218.png)


![](../../assets/4d9f4e36187e577f.png)

In the image above, the optical depth of the ![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)


![](../../assets/47f2eaaf908db961.png)

The first step is, obviously, finding the points ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com O](../../assets/ab988e264adecb16.png)

*origin*. In a surface shader, ![Rendered by QuickLaTeX.com O](../../assets/ab988e264adecb16.png)

`worldPos`

variable inside the `Input`

structure. This is how far the shader goes; the only piece of information available to us are ![Rendered by QuickLaTeX.com O](../../assets/ab988e264adecb16.png)

![Rendered by QuickLaTeX.com D](../../assets/81012a1469029eac.png)

**view ray**, and the atmospheric sphere centred at ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

**atmospheric sphere** and the **view ray** from the camera.

First of all, we should notice that ![Rendered by QuickLaTeX.com O](../../assets/ab988e264adecb16.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

`float3`

), ![Rendered by QuickLaTeX.com AO](../../assets/0a4db8c582c24878.png)

![Rendered by QuickLaTeX.com O](../../assets/ab988e264adecb16.png)

`float`

). Both ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com AO](../../assets/0a4db8c582c24878.png)


![Rendered by QuickLaTeX.com \[A = O + \overline{AO}\,D\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7edc80394bb78957f3efad4299c3a0b5_l3.png)


![Rendered by QuickLaTeX.com \[B = O + \overline{BO}\,D\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-999843cf8838fbd7b8aba5dcb9301c6d_l3.png)


where the overline notation ![Rendered by QuickLaTeX.com \overline{XY}](../../assets/aad526819b6fd5b6.png)

![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)


For efficiency reasons, in the shader code we will use ![Rendered by QuickLaTeX.com AO](../../assets/0a4db8c582c24878.png)

![Rendered by QuickLaTeX.com BO](../../assets/a68f949ad891f260.png)

![Rendered by QuickLaTeX.com OT](../../assets/ff6793995d9b24cb.png)


![Rendered by QuickLaTeX.com \[\overline{AO} = \overline{OT} - \overline{AT}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-662259f4309a9c0b6c421906befbf360_l3.png)


![Rendered by QuickLaTeX.com \[\overline{BO} = \overline{OT} + \overline{BT}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ad4ae9bc98d8eac6ce7390686cebee2e_l3.png)


We should also notice that the segments ![Rendered by QuickLaTeX.com \overline{AT}](../../assets/ec378d1ec95eb2b1.png)

![Rendered by QuickLaTeX.com \overline{BT}](../../assets/d2fb90923196a3bf.png)

![Rendered by QuickLaTeX.com \overline{AO}](../../assets/fe654224c0340576.png)

![Rendered by QuickLaTeX.com \overline{AT}](../../assets/ec378d1ec95eb2b1.png)


The segment ![Rendered by QuickLaTeX.com \overline{OT}](../../assets/fe23b9445a894f57.png)

![Rendered by QuickLaTeX.com \overline{OT}](../../assets/fe23b9445a894f57.png)

![Rendered by QuickLaTeX.com CO](../../assets/e0148116de91324a.png)

**dot product**. If you are familiar with shaders you might know the dot product as a measure of how “aligned” two directions are. When it is applied to two vectors and the second one has unitary length, it becomes a projection operator:

![Rendered by QuickLaTeX.com \[\overline{OT} = \left(C-O\right) \cdot D\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-902408c8ee173449e9b067f3e6dae582_l3.png)


One should notice that ![Rendered by QuickLaTeX.com \left(C-O\right)](../../assets/dfbc90fc5068c905.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com O](../../assets/ab988e264adecb16.png)


What we need to calculate next is the length of the segment ![Rendered by QuickLaTeX.com \overline{AT}](../../assets/ec378d1ec95eb2b1.png)

**Pythagoras’ theorem** on the triangle ![Rendered by QuickLaTeX.com \overset{\triangle}{ACT}](../../assets/50e5a440da14cf4d.png)


![Rendered by QuickLaTeX.com \[R^2 = \overline{AT}^2 + \overline{CT}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ced8fb8560a90a31a408f824e30b6ce2_l3.png)


which means that:

![Rendered by QuickLaTeX.com \[\overline{AT} = \sqrt{R^2 - \overline{CT}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c8a2a966c381817d0c482f373250496f_l3.png)


The length of ![Rendered by QuickLaTeX.com \overline{CT}](../../assets/bf38545549393a2c.png)

![Rendered by QuickLaTeX.com \overset{\triangle}{OCT}](../../assets/073de188afbd5c63.png)


![Rendered by QuickLaTeX.com \[\overline{CO}^2 = \overline{OT}^2 + \overline{CT}^2\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda3066d3231a6f92257550eb89308a4_l3.png)


![Rendered by QuickLaTeX.com \[\overline{CT} = \sqrt{\overline{CO}^2 - \overline{OT}^2}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0e561b48e80fa364f02eea0fa2bf919c_l3.png)


We know have all the quantities that we need. To sum it up:

![Rendered by QuickLaTeX.com \[\overline{OT} = \left(C-O\right) \cdot D\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-902408c8ee173449e9b067f3e6dae582_l3.png)


![Rendered by QuickLaTeX.com \[\overline{CT} = \sqrt{\overline{CO}^2 - \overline{OT}^2}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0e561b48e80fa364f02eea0fa2bf919c_l3.png)


![Rendered by QuickLaTeX.com \[\overline{AT} = \sqrt{R^2 - \overline{CT}^2}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-256b6553f4651d99d96146950ad8d6ad_l3.png)


![Rendered by QuickLaTeX.com \[\overline{AO} = \overline{OT} - \overline{AT}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-662259f4309a9c0b6c421906befbf360_l3.png)


![Rendered by QuickLaTeX.com \[\overline{BO} = \overline{OT} + \overline{AT}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d47f3c0e4a68ce96eb89ddaa17def743_l3.png)


That set of equation contains square roots. They are only defined on non-negative numbers. If ![Rendered by QuickLaTeX.com R^2 > \overline{CT}^2](../../assets/2d631a0d43102a41.png)


We can translate this into the following Cg function:

bool rayIntersect ( // Ray float3 O, // Origin float3 D, // Direction // Sphere float3 C, // Centre float R, // Radius out float AO, // First intersection time out float BO // Second intersection time ) { float3 L = C - O; float DT = dot (L, D); float R2 = R * R; float CT2 = dot(L,L) - DT*DT; // Intersection point outside the circle if (CT2 > R2) return false; float AT = sqrt(R2 - CT2); float BT = AT; AO = DT - AT; BO = DT + BT; return true; }

There is not a single value, but three to return: ![Rendered by QuickLaTeX.com \overline{AO}](../../assets/fe654224c0340576.png)

![Rendered by QuickLaTeX.com \overline{BO}](../../assets/7a7677e2d7f615c7.png)

`out`

keywords, which makes any change the function does on those parameters persistent after its termination.

### ⭐ Recommended Unity Assets

#### Colliding with the Planet

There is an additional issue that we have to take into account. Certain view rays hit the planet, hence their journey through the atmosphere reaches an early termination. One approach could be to revise the derivation presented above.

An easier, yet less efficient approach, is to run `rayIntersect`

twice, and then to adjust the ending point if needed.

![](../../assets/c79e84d32e63fab4.png)

This translates to the following code:

// Intersections with the atmospheric sphere float tA; // Atmosphere entry point (worldPos + V * tA) float tB; // Atmosphere exit point (worldPos + V * tB) if (!rayIntersect(O, D, _PlanetCentre, _AtmosphereRadius, tA, tB)) return fixed4(0,0,0,0); // The view rays is looking into deep space // Is the ray passing through the planet core? float pA, pB; if (rayIntersect(O, D, _PlanetCentre, _PlanetRadius, pA, pB)) tB = pA;

#### Coming Next…

This post showed how it is possible to find intersections between a sphere and a ray. We will use this in the next post to calculate the entrance and exit points of the view ray with the atmospheric sphere.

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) - Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) **Part 6.**[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781)- Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce the volumetric atmospheric scattering presented in this tutorial.

## Leave a Reply Cancel reply