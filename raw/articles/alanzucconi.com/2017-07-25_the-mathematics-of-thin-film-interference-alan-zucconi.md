---
title: The Mathematics of Thin-Film Interference - Alan Zucconi
url: https://www.alanzucconi.com/2017/07/25/the-mathematics-of-thin-film-interference/
author: Alan Zucconi
published: '2017-07-25'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post continues our journey through the Mathematical foundations of iridescence. This time, we will discuss a new way in which material can split light: **thin-film interference**. This is how bubbles (and car paint) get their unique reflections.

![](../../assets/772a6fd9a45ffd73.png)

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

In the previous posts, we have described how materials with certain repeated patterns exhibit iridescent reflections. Such a phenomenon is called **diffraction grating**. However, that is not the only way in which a material can split light into its components. Another one is called** thin-film interference** and occurs when a material is made out of multiple layers.

The diagram below shows a typical example of thin-film interference. Let’s imagine this to be a thin layer of water distributed onto a different surface. When a ray of light hits the water, it splits in two; a part is reflected back, while the rest goes deeper into the material. The latter ray is subjected to refraction, a phenomenon that causes light to “bend” when entering or exiting different materials.

![](../../assets/95b94dab77dd9d92.png)

Reflection and refraction can only happen where two different materials meet. For this reason, light continues to bounce inside the material until there’s energy left.

The reason why this phenomenon causes iridescent reflections to appear is, once again, due to the fact that light behaves like a wave. All those rays have travelled different distances; hence, they will reach the eye of the viewer with different phases. Under certain circumstances, some of those light rays will be in phase, amplifying each other. As a result, some colours will be boosted in the final reflection, while other will cancel each other out. Once again, iridescence is caused by **constructive interference**.

As you can see, there can be countless occasions for light to interfere. A calculation of that proportion is often unfeasible for rendering games in real-time. In this tutorial, we will focus on a simplified version of this problem, which only takes into account the interference of the first two rays:

![](../../assets/0d1cda8dc6f2227b.png)

#### Optical Path Difference

Like we did in the tutorial on diffraction grating, once again we have to calculate the difference in length travelled by the two reflected rays. However, there are a couple of important difference that needs to be highlighted. Diffraction grating is a **diffusive** phenomenon: rays are scattered in all directions. In that context, it made sense for an incoming ray of light from a **light direction** ![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

**view direction** ![Rendered by QuickLaTeX.com V](../../assets/c746ecbc0d34d082.png)

**specular** phenomenon. Surfaces are perfectly smooth, and rays are reflected with the same incident angle.

Another issue is that rays are travelling through different media. This has a direct effect on their phase, as light travels at different speeds in different media. This forces us to rely on a quantity called **optical path difference**, which (loosely speaking) measures the **phase offset** of two light rays. For rays travelling through the same medium, the optical path difference is equal to the difference in length of their paths. For different media, we have to take into account their **refractive index**. This is a property that determines how much light “bends” when it enters into or exits from a material. The refractive index of empty space is equal to ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com 1.000293](../../assets/7fe783d6ab145a3e.png)

![Rendered by QuickLaTeX.com 1.333](../../assets/4989caccb40cef16.png)


![](../../assets/22432738f24bd53b.png)

Looking at our diagram above, we can see that the grey parts of common to both rays. The first ray travels the distance ![Rendered by QuickLaTeX.com \overline{AD}](../../assets/d67d983fa02664b5.png)

![Rendered by QuickLaTeX.com n_1](../../assets/98188fb35dabdea4.png)

![Rendered by QuickLaTeX.com \overline{AB}+\overline{BC}](../../assets/ea811f017b7b691a.png)

![Rendered by QuickLaTeX.com n_2](../../assets/d60003de2e441f4a.png)


![Rendered by QuickLaTeX.com \[OPD = n_2 \left(\overline{AB}+\overline{BC}\right) - n_1 \overline{AD}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-88803bce4f0f2f756e5ea93c611988c8_l3.png)


##### Path Length of the Second Ray

Let’s start by calculating the path length of the second ray, since is the easier one. It is easy to see that both ![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)

![Rendered by QuickLaTeX.com \overline{BC}](../../assets/20f2a8a0b0611fe7.png)

![Rendered by QuickLaTeX.com \widehat{ABE}](../../assets/73aa9d350e9cfe65.png)

![Rendered by QuickLaTeX.com d](../../assets/e3e196f6915d0ca1.png)

![Rendered by QuickLaTeX.com \overline{BE}](../../assets/2bd559a5413ce215.png)


If you are unfamilair with trigonometry, the following diagram should help you understanding how to calculate the length of all the unknown sides of the ![Rendered by QuickLaTeX.com \widehat{ABE}](../../assets/73aa9d350e9cfe65.png)


![](../../assets/2f623e374b4566cb.png)

Hence:

![Rendered by QuickLaTeX.com \[\overline{AB} = \overline{BC} = \boxed{d \sec{\theta_R}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-523f92180922d14c6605acc0c96cc258_l3.png)


![Rendered by QuickLaTeX.com \[\overline{AB}+\overline{BC} = 2 \boxed{d \sec{\theta_R}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5eb027606a4a2cfcdff9f7c91ed64d3b_l3.png)


##### Path Length of the First Ray

Calculating the length of ![Rendered by QuickLaTeX.com \overline{AC}](../../assets/69f71321c9e91bc2.png)

[The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682). In that post we concludede that:

![Rendered by QuickLaTeX.com \[\overline{AD} = \boxed{\overline{AC}} \sin{\theta_L}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-88fc6d39226f9617e250ce2232e7c15e_l3.png)


By working on the ![Rendered by QuickLaTeX.com \widehat{ABE}](../../assets/73aa9d350e9cfe65.png)

![Rendered by QuickLaTeX.com \overline{AE}](../../assets/ad5c272cbc666643.png)


![Rendered by QuickLaTeX.com \[\overline{AC} = \overline{AE} + \overline{EC}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-00123d90091eb22b2d57210ada1c8bfc_l3.png)


![Rendered by QuickLaTeX.com \[\overline{AE} = \overline{EC} = d \tan{\theta_R}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d72fafb3a4f130eb5d31a4c4dcf89bd5_l3.png)


![Rendered by QuickLaTeX.com \[\overline{AC} = \boxed{2 d \tan{\theta_R}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-368a7e9baf118993d3271e8f6d62b76a_l3.png)


Hence:

![Rendered by QuickLaTeX.com \[\overline{AD} = \boxed{ 2 d \tan{\theta_R}} \sin{\theta_L}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-43ac4000f3be8b73fc1fa807a00fc6e5_l3.png)


##### Path Difference

To sum up:

![Rendered by QuickLaTeX.com \[OPD = n_2 \boxed{\left(\overline{AB}+\overline{BC}\right) }- n_1 \boxed{ \overline{AD} }=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7e3123472828b948ea0a36347f4261fd_l3.png)


![Rendered by QuickLaTeX.com \[= n_2 \boxed{2 d \sec{\theta_R}} - n_1 \boxed{2 d \tan{\theta_R} \sin{\theta_L}} =\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-57fb75857e61510afd0eec2d6669670a_l3.png)


![Rendered by QuickLaTeX.com \[=2d \left( n_2 \sec{\theta_R} - n_1 \tan{\theta_R} \sin{\theta_L} \right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7b21e737ea1069e21cc0134810959f77_l3.png)


Expanding with the following trigonometric identities ![Rendered by QuickLaTeX.com \sec{\theta_R} = \frac{1}{\cos{\theta_R}}](../../assets/d36aff547b59fc39.png)

![Rendered by QuickLaTeX.com \tan{\theta_R} = \frac{\sin{\theta_R}}{\cos{\theta_R}}](../../assets/727040b28aeb4dd8.png)


![Rendered by QuickLaTeX.com \[OPD=2d \left( n_2 \boxed{\sec{\theta_R}} - n_1 \boxed{\tan{\theta_R}} \sin{\theta_L} \right)=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c81eae2a40d858d6248eeb29125ee3c0_l3.png)


![Rendered by QuickLaTeX.com \[= 2 d \left (n_2 \boxed{\frac{1}{\cos{\theta_R}}}- n_1 \boxed{\frac{\sin{\theta_R}}{\cos{\theta_R}}} \sin{\theta_L}\right) = \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c47bd64ad0dd306136d22552fa5e3ba7_l3.png)


![Rendered by QuickLaTeX.com \[= \frac{2d}{\cos{\theta_R}} \left(n_2 - n_1 \sin{\theta_R} \sin{\theta_L }\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-1ca5558d04ece60cff9dff58dfffceac_l3.png)


To progress in this expansion even further, we need to mention a foundamental equation in optics, called the **Snell’s law**. It connects the refractive indices to the incident and reflected angles:

![Rendered by QuickLaTeX.com \[n_1 \sin{\theta_L} = n_2 \sin{\theta_R}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f1fa61de5820e1d803f1ee8111cc03eb_l3.png)


From which we can extract:

![Rendered by QuickLaTeX.com \[\sin{\theta_L} = \frac{n_2}{n_1} \sin{\theta_R}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-60d4610a3a8b1c76e543719541faa989_l3.png)


Substituting ![Rendered by QuickLaTeX.com \sin{\theta_L}](../../assets/0dc0d8c0c3f7cbfa.png)

![Rendered by QuickLaTeX.com n_2](../../assets/d60003de2e441f4a.png)


![Rendered by QuickLaTeX.com \[OPD = \frac{2d}{\cos{\theta_R}} \left(n_2 - n_1 \sin{\theta_R} \boxed{\sin{\theta_L }}\right) =\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d2c9ba43fa82b1a0cc4e155e05f7f187_l3.png)


![Rendered by QuickLaTeX.com \[= \frac{2d}{\cos{\theta_R}} \left(n_2 - \not{n_1} \sin{\theta_R}\boxed{\frac{n_2}{ \not{n_1}} \sin{\theta_R}}\right) =\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f884cafa2e37b2a3f985af5ccade2afe_l3.png)


![Rendered by QuickLaTeX.com \[= \frac{2d}{\cos{\theta_R}} \left(\boxed{n_2} - \sin{\theta_R}\boxed{n_2}\sin{\theta_R}\right) =\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-feca8d01a85c3a7fea77d62cf8f2c01c_l3.png)


![Rendered by QuickLaTeX.com \[= \frac{\boxed{n_2} 2 d}{\cos{\theta_R}} \left(1 - \sin^2{\theta_R}\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-1221bd769cee0abaf4c3fb126abf2964_l3.png)


From Pythagora’s Theorem:

![Rendered by QuickLaTeX.com \[\cos^2{\theta_R} + \sin^2{\theta_R} = 1\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d7bc23d09b154f1b44355e75e738e4b5_l3.png)


![Rendered by QuickLaTeX.com \[1 - \sin^2{\theta_R} = \cos^2{\theta_R}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7c751b80dc4b3f69e85decbcbe47f5e7_l3.png)


Substituting and simplifying:

![Rendered by QuickLaTeX.com \[OPD= \frac{n_2 2 d}{\cos{\theta_R}}\left(\boxed{1 - \sin^2{\theta_R}}\right) =\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8185b9bcd953844b5e948dbae422047c_l3.png)


![Rendered by QuickLaTeX.com \[= \frac{n_2 2 d}{\not{\cos{\theta_R}}}\boxed{\cos^{\not{2}}{\theta_R}}=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-919fe4ef4df86eda5b19962bba85830e_l3.png)


![Rendered by QuickLaTeX.com \[= n_2 2 d\cos{\theta_R} = OPD\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b44170b68a9a632788fb26ac2204dba4_l3.png)


#### Phase Shift

Like we discussed in [The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682), when the ![Rendered by QuickLaTeX.com OPD](../../assets/c9740280bc9615d8.png)


![Rendered by QuickLaTeX.com \[n_2 2 d \cos{\theta_R} = n \codt w\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-bcc7b13e73bce43c6249226f79b95234_l3.png)


with ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com n_A < n_B](../../assets/dca9a0976a9bcdfe.png)


If we take the example of a soap bubble, the first ray to be reflected off the surface film will indeed be subjected to a phase shift since ![Rendered by QuickLaTeX.com n_{air} < n_{film}](../../assets/936eb075042f3f26.png)


Before changing our equation, however, we need to check whether a similar phase shift occurs to the second ray or not. The only moment in which the second ray is reflected is when it crosses the film barrier. However, ![Rendered by QuickLaTeX.com n_{film} > n_{air}](../../assets/c93fa3d10ca791f3.png)


As a result, we have to alter our equation to take this into account:

![Rendered by QuickLaTeX.com \[n_2 2 d \cos{\theta_R} = \left(n + \frac{1}{2}\right) \codt w\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6f24214e858467512f9a0b2d3eba4329_l3.png)


We will see, in the next part of this tutorial, an efficient way to do this procedurally based on the refractive indices of the media.

#### Conclusion

This tutorial introduces the Mathematical foundations of the optical phenomenon known as thin-film interference. In the next post, we will see how we can actually implement that in a Shader.

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
**The Mathematics of Thin-Film Interference** - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

You can download the Unity package for the CD-ROM Shader and Thin-Film Shader effects on [ Patreon](https://www.patreon.com/posts/13032957).

## Leave a Reply Cancel reply