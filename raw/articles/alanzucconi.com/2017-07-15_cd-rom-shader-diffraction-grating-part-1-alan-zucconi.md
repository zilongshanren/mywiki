---
title: 'CD-ROM Shader: Diffraction Grating - Part 1 - Alan Zucconi'
url: https://www.alanzucconi.com/2017/07/15/cd-rom-shader-1/
author: Alan Zucconi
published: '2017-07-15'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post will guide you through the creation of a shader that reproduces the rainbow reflections that can be seen on CD-ROMs and DVDs. This tutorial is part of a longer series on physically based iridescence.

![](../../assets/2c71be173dfa1509.png)

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

In a previous tutorial, [The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682), we have derived the equations that capture the very nature of the iridescent reflections that certain surfaces exhibit. Iridescence occurs on materials featuring a repeating surface pattern which size is comparable to the wavelength of the light they reflect.

The optical effects we are interested in reproducing ultimately depends on three factors: the angle of the light source with the surface normal (**light direction**), the angle of the viewer (**view direction**) and the distance between the repeating gaps.

![](../../assets/b0eaecc870a327ee.png)

We want our shader to add iridescent reflections on top of the normal effects that the Standard material usually comes with. For this reason, we will extend the **lighting function** of a **Standard Surface shader**. If you are unfamiliar with the procedure, [Physically Based Rendering and Lighting Models](https://www.alanzucconi.com/?p=1964) provides a good introduction.

#### Creating a Surface Shader

![](../../assets/0f9474fedafe90c6.png)

The first step is to create a new shader.Since we want to extend a shader that already supports physically based lighting, we will start with a **Standard Surface Shader**.

The newly created CD-ROM shader needs a new property: the distance ![Rendered by QuickLaTeX.com d](../../assets/e3e196f6915d0ca1.png)

`Properties`

block, which should now look like this:

Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _Glossiness ("Smoothness", Range(0,1)) = 0.5 _Metallic ("Metallic", Range(0,1)) = 0.0 _Distance ("Grating distance", Range(0,10000)) = 1600 // nm }

This will create a new slider in the Material Inspector. The `_Distance`

property, however, still needs to be coupled with a variable in the `CGPROGRAM`

section:

float _Distance;

We are now ready to start.

#### Customising the Lighting Function

The first step we need to take is to replace the lighting function of the CD-ROM shader with a custom one. We can do this by altering the `#pragma`

directive from:

#pragma surface surf Standard fullforwardshadows

to:

#pragma surface surf Diffraction fullforwardshadows

This forces Unity to delegate the lighting calculation to a function called `LightingDiffraction`

. It is important to understand that we want to *extend* the behaviour of this Surface shader, not *override* it. For this reason, out new lighting function will start by simply calling Unity’s Standard PBR lighting function:

#include "UnityPBSLighting.cginc" inline fixed4 LightingDiffraction(SurfaceOutputStandard s, fixed3 viewDir, UnityGI gi) { // Original colour fixed4 pbr = LightingStandard(s, viewDir, gi); // <diffraction grating code here> return pbr; }

As you can see from the snippet above, the new `LightingDiffraction`

simply calls `LightingStandard`

and returns its value. If we compile the shader now, we will see no difference in the way it renders materials.

Before continuing, however, we need to create an additional function to handle the **Global Illumination**. Since we are not interested in changing that behaviour, our new global illumination function will once be a proxy for Unity’s Standard PBR function:

void LightingDiffraction_GI(SurfaceOutputStandard s, UnityGIInput data, inout UnityGI gi) { LightingStandard_GI(s, data, gi); }

Lastly, please note that since we are using `LightingStandard`

and `LightingDiffraction_GI`

directly, we will need to include `UnityPBSLighting.cginc`

our shader.

### ⭐ Recommended Unity Assets

#### Implementing the Diffraction Grating

This is the core of our shader. We are finally ready to implement the diffraction grating equations seen in [The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682). In that post, we concluded that the viewer sees an iridescent reflection which is a sum of all the wavelengths ![Rendered by QuickLaTeX.com w](../../assets/bdbb99d128802679.png)

**grating equation**:

![Rendered by QuickLaTeX.com \[\left | \sin{\theta_L} - \codt \sin{ \theta_V } \right |= \frac{n \cdot w}{d}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d1b251f371ffc7aaf5c27629be6837a4_l3.png)


with ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)


Given a certain pixel, the values for ![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)

*light direction*), ![Rendered by QuickLaTeX.com \theta_V](../../assets/b093ae38d3530c80.png)

*view direction*) and ![Rendered by QuickLaTeX.com d](../../assets/e3e196f6915d0ca1.png)

*gap distance*) are known. The unknown variables are ![Rendered by QuickLaTeX.com w](../../assets/bdbb99d128802679.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)


When we know which wavelengths contribute to the final iridescent reflection, we calculate their associated colours and add them together. The [Improving the Rainbow](https://www.alanzucconi.com/?p=6703) discussed several approached to convert wavelengths from the visible spectrum into colours. for this tutorial, we will use `spectral_zucconi6`

as it provides the best approximation with the cheapest computational cost.

Let’s see a possible implementation below:

inline fixed4 LightingDiffraction(SurfaceOutputStandard s, fixed3 viewDir, UnityGI gi) { // Original colour fixed4 pbr = LightingStandard(s, viewDir, gi); // Calculates the reflection color fixed3 color = 0; for (int n = 1; n <= 8; n++) { float wavelength = abs(sin_thetaL - sin_thetaV) * d / n; color += spectral_zucconi6(wavelength); } color = saturate(color); // Adds the refelection to the material colour pbr.rgb += color; return pbr; }

In the snippet above we use values of ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)


We now have one last thing left to do. Calculating `sin_thetaL`

and `sin_thetaV`

. That requires to introduce yet another concept: the **tangent vector**. We will see how to calculate that in the next part of this tutorial.

#### Conclusion

You can find the complete series here:

- Part 1.
[The Nature of Light](https://www.alanzucconi.com/?p=6630) - Part 2.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6703)(Part 1) - Part 3.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6806)(Part 2) - Part 4.
[Understanding Diffraction Grating](https://www.alanzucconi.com/?p=6651) - Part 5.
[The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682) - Part 6.
**CD-ROM Shader: Diffraction Grating**(Part 1) - Part 7.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6791)(Part 2) - Part 8.
[Iridescence on Mobile](https://www.alanzucconi.com/?p=6819) - Part 9.
[The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/?p=6821) - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package for the CD-ROM Shader effect on [ Patreon](https://www.patreon.com/posts/13032957).

## Leave a Reply Cancel reply