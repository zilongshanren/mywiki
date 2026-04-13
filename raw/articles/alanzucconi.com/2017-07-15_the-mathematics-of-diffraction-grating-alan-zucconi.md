---
title: The Mathematics of Diffraction Grating - Alan Zucconi
url: https://www.alanzucconi.com/2017/07/15/the-mathematics-of-diffraction-grating/
author: Alan Zucconi
published: '2017-07-15'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post introduces the mathematics behind the optical phenomenon known as diffraction grating, which is responsible for iridescent reflections in many materials.

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

The previous post in this series, [Understanding Diffraction Grating](https://www.alanzucconi.com/?p=6651), explained why iridescence occurs on some materials. Light is a wave, and it bends every time it finds an obstacle in its path. If a material presents a microscopic slit or a bump, this will an incoming planar wave to scatter in all direction. If those slits or bumps are arranged in a regular pattern, a new wavefront is generated for each one of them. All those wavefronts will interfere with each other, causing certain wavelengths (which are perceived by the human eye as colours) to appear prominently.

We now have everything we need to start modelling this phenomenon mathematically. Let’s start by imagining a material which features imperfections that repeat at a known distance ![Rendered by QuickLaTeX.com d](../../assets/e3e196f6915d0ca1.png)

![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)

![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)

![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)


![](../../assets/b0eaecc870a327ee.png)

Since the imperfections repeat regularly every ![Rendered by QuickLaTeX.com d](../../assets/e3e196f6915d0ca1.png)

![Rendered by QuickLaTeX.com d](../../assets/e3e196f6915d0ca1.png)

*at least* a light ray reaching the viewer for each slit.

#### Derivation

The two rays of light depicted in the diagram above travel different distances before reaching the viewer. If they start in phase, they might not be when they arrive at their destination. To understand how those two rays interfere with each other (constructively or destructively) we have to calculate how off phase they are when they reach the viewer.

Those two rays are guaranteed to be in phase until the first one hit the surface. The second ray travels an extra a distance ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

![Rendered by QuickLaTeX.com d \cdot \sin{\theta_L}](../../assets/72088302d580a328.png)


![](../../assets/0e16fca54ba72124.png)

Using a similar construction, we can calculate the extra distance ![Rendered by QuickLaTeX.com y](../../assets/6cc181d8f36d0fd4.png)

![Rendered by QuickLaTeX.com y=d \cdot \sin{\theta_V}](../../assets/4609f0934300af14.png)


![](../../assets/96f5773b2035f7b9.png)

Those two segments ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)


However, this is not the only case in which the two rays could be in phase. If their length difference is an integer multiple of the wavelength ![Rendered by QuickLaTeX.com w](../../assets/bdbb99d128802679.png)


![Rendered by QuickLaTeX.com \[d \codt \sin{\theta_L} - d \codt \sin{ \theta_V } = n \cdot w\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-de78cdc8a39d8e174173857dd76f9f54_l3.png)


![Rendered by QuickLaTeX.com \[\sin{\theta_L} - \codt \sin{ \theta_V } = \frac{n \cdot w}{d}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-72b378675382c952b3a3a482358491b3_l3.png)


#### Visualisation

Let’s take a moment to understand what that equation means. If the light comes with incident angle ![Rendered by QuickLaTeX.com \theta_L](../../assets/42f21da72929992c.png)

![Rendered by QuickLaTeX.com \theta_V](../../assets/b093ae38d3530c80.png)

![Rendered by QuickLaTeX.com w](../../assets/bdbb99d128802679.png)

![Rendered by QuickLaTeX.com d \left( \sin{\theta_L} - \sin{ \theta_V } \right)](../../assets/e1b36d18ff805196.png)


This effect is visualised in the following diagram, taken from the very interesting thread [A complex approach: Iridescence in cycles](https://blenderartists.org/forum/showthread.php?340095-A-complex-approach-Iridescence-in-cycles/page2):

![](../../assets/adfa2f8f284a1ea5.jpg)

The white ray follows the path traversed by photons for the specular reflection. A viewer watching the material from different angles will see a cyclic rainbow pattern. Each colour corresponds to a different wavelength, while the order indicates its respective integer ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com \sin{\theta_L} - \sin{ \theta_V }](../../assets/bf0b4d941af551cb.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)


![Rendered by QuickLaTeX.com \[\left | \sin{\theta_L} - \codt \sin{ \theta_V } \right |= \frac{n \cdot w}{d}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d1b251f371ffc7aaf5c27629be6837a4_l3.png)


### 📚 Recommended Books

#### Conclusion

You can find the complete series here:

- Part 1.
[The Nature of Light](https://www.alanzucconi.com/?p=6630) - Part 2.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6703)(Part 1) - Part 3.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6806)(Part 2) - Part 4.
[Understanding Diffraction Grating](https://www.alanzucconi.com/?p=6651) - Part 5.
**The Mathematics of Diffraction Grating** - Part 6.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6767)(Part 1) - Part 7.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6791)(Part 2) - Part 8.
[Iridescence on Mobile](https://www.alanzucconi.com/?p=6819) - Part 9.
[The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/?p=6821) - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package for the CD-ROM Shader effect on [ Patreon](https://www.patreon.com/posts/13032957).

## Leave a Reply Cancel reply