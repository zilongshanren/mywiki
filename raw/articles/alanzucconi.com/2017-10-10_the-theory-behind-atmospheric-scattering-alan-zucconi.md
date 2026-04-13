---
title: The Theory Behind Atmospheric Scattering - Alan Zucconi
url: https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-2/
author: Alan Zucconi
published: '2017-10-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the tutorial on volumetric atmospheric scattering. In this post we will start deriving the equations that govern this complex, yet beautiful optical phenomenon.

![](../../assets/488fe0db18d2fa0c.gif)

You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) **Part 2.**[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404)- Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

You can **download** the **Unity package** for this tutorial at the bottom of the page.

#### Introduction

In the first part of this tutorial, we have discussed how light can be deflected by the air molecules present in a planet’s atmosphere. This process is called **scattering**, and we have highlighted two special cases. **Out-scattering** occurs when a ray of light that was directed towards the camera is deflected away from it (diagram below).

![](../../assets/9ecb5b1cabaa7738.png)

Conversely, **in-scattering** occurs when a ray of light is deflected directly towards the camera.

![](../../assets/0aefca561e7fbeab.png)


#### The Transmittance Function

To calculate the amount of light transmitted to the camera, is helpful to take the same journey that light rays from the sun undergo. By looking at the diagram below, is easy to see that light rays reaching ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com I_C](../../assets/979a301354667e9e.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com I_P](../../assets/457e324e8f29677a.png)

![Rendered by QuickLaTeX.com I_C](../../assets/979a301354667e9e.png)


The ratio between ![Rendered by QuickLaTeX.com I_C](../../assets/979a301354667e9e.png)

![Rendered by QuickLaTeX.com I_P](../../assets/457e324e8f29677a.png)

**transmittance**:

![Rendered by QuickLaTeX.com \[T\left(\overline{CP}\right) = \frac{I_P}{I_C}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8471db80c74dc57d8fb698e7d94374c7_l3.png)


and we can use it to indicate the percentage of light that is not scattered (**transmitted**) during the journey from ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)


Consequently, the amount of light that ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)


![Rendered by QuickLaTeX.com \[I_P = I_C \, T\left(\overline{CP}\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-2d3a9843d045fd5a8a087c5235ed90bd_l3.png)


#### The Scattering Function

The point ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

**scattering function** ![Rendered by QuickLaTeX.com S](../../assets/4b8b5ff505466deb.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


![](../../assets/4de63488127ee25b.png)

The value of ![Rendered by QuickLaTeX.com S\left(\lambda, \theta, h\right)](../../assets/a2c414113c497e94.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

**wavelength** ![Rendered by QuickLaTeX.com \lambda](../../assets/e4664a784ffb986a.png)

**scattering angle** ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

**altitude** ![Rendered by QuickLaTeX.com h](../../assets/5b0f1268bf785a2d.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)


We now have all the tools necessary to write a general equation that shows how much light is transferred from ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)


![Rendered by QuickLaTeX.com \[I_{PA} = \boxed{I_P} \, S\left(\lambda,\theta,h\right) \, T\left(\overline{PA}\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8a16120274a4f00e03931e5d8eb65b24_l3.png)


We can expand ![Rendered by QuickLaTeX.com I_P](../../assets/457e324e8f29677a.png)


![Rendered by QuickLaTeX.com \[I_{PA} = \boxed{I_C \, T\left(\overline{CP}\right)}\, S\left(\lambda,\theta,h\right) \,T\left(\overline{PA}\right)=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-333e59f43a8a2595c96c60199519ddf7_l3.png)


![Rendered by QuickLaTeX.com \[=\underset{\text{in-scattering}}{ \underbrace{I_C \,S\left(\lambda,\theta,h\right)} }\,\underset{\text{out-scattering}}{\underbrace{T\left(\overline{CP}\right)\, T\left(\overline{PA}\right)}}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b45cbf1a7881d82e2b2817cc2a8bda6a_l3.png)


The equation should be self explanatory:

- Light is travels from the sun to

, unscattered in the vacuum of space; - Light enters the atmosphere and travels from

to

. In doing so, only the fraction

reaches its destination due to **out-scattering**; - Part of the light that has reached

from the sun is deflected back to the camera. The ratio of light subjected to **in-scattering**is

; - The remaining light travels from

to

, and once again only the fraction

is transmitted.

#### The Numerical Integration

If you have paid attention to the previous paragraphs, you might have noticed an apparent inconsistency in the way intensity have been written. The symbol ![Rendered by QuickLaTeX.com I_{PA}](../../assets/08d80732e82884bd.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)


The total amount of light ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com I_A](../../assets/95678973100e49d4.png)

![Rendered by QuickLaTeX.com P \in \overline{AB}](../../assets/5d4c8cd8a76dc8ab.png)

![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)

![Rendered by QuickLaTeX.com \overline{AB}](../../assets/b082555e60e95014.png)

![Rendered by QuickLaTeX.com ds](../../assets/a15125f89deb0218.png)


![](../../assets/4d9f4e36187e577f.png)

This process of approximation is called **numerical integration**, and leads to the following expression:

![Rendered by QuickLaTeX.com \[I_A = \sum_{P \in \overline{AB}} {I_{PA}\, ds }\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-73cd82418fd97766d94d6358af98d6a3_l3.png)


The more points we’ll take into account, the more accurate our final result will be. In reality, what we will have to do in our atmospheric shader is to loop through several points ![Rendered by QuickLaTeX.com P_i](../../assets/b4a50ebd874809dc.png)


#### Directional Light

If the sun is relatively close, it is best modelled as a **point light** source. In that case, the amount of light received at ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

**directional light** source. The light received from directional light sources remain constant regardless of the distance it travels. Hence, every point ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)


![](../../assets/5b15c00d7cccc2b1.png)

We can use this assumption to simplify our set of equations.

Let’s replace ![Rendered by QuickLaTeX.com I_C](../../assets/979a301354667e9e.png)

![Rendered by QuickLaTeX.com I_S](../../assets/de81e6e81d28e2ea.png)

**sun intensity**.

![Rendered by QuickLaTeX.com \[I_A = \sum_{P \in \overline{AB}} {\boxed{I_{PA}}\, ds } =\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8f734e88963dd38415b3ffa2917e06b5_l3.png)


![Rendered by QuickLaTeX.com \[= \sum_{P \in \overline{AB}} {\boxed{I_C \,S\left(\lambda,\theta,h\right) \,T\left(\overline{CP}\right)\, T\left(\overline{PA}\right)}\, ds }=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7b6d42d41aabb5d5175a9a9efef9f817_l3.png)


![Rendered by QuickLaTeX.com \[= I_S \sum_{P \in \overline{AB}} {S\left(\lambda,\theta,h\right) \,T\left(\overline{CP}\right) \, T\left(\overline{PA}\right) \,ds }=\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-110455eddefb3f07666c41a10691f6ef_l3.png)


There is another optimisation that we can perform, and it involves the scattering function ![Rendered by QuickLaTeX.com S\left(\lambda,\theta,h\right)](../../assets/13961b2acffd7637.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com S\left(\lambda,\theta,h\right)](../../assets/13961b2acffd7637.png)


#### Absorption Coefficient

When describing the possible outcomes of the interaction between light and air molecules, we have only introduced two. Passing straight through, or being deflected. There is a third possibility. Some chemical compounds absorb light. The atmosphere on Earth has plenty of chemicals with such a property. Ozone, for instance, is present in the higher atmosphere and is known to react strongly to ultraviolet light. Its presence, however, has virtually no effect on the colour of the sky, since it absorbs light outside the visible spectrum.Here on Earth, the contribution of light-absorbing chemicals is often ignored.

Here on Earth, the contribution of light-absorbing chemicals is often ignored. The same cannot be done for other planets. The typical colouration of Neptune and Uranus, for instance, is caused by the abundant presence of methane in their atmospheres. Methane is known for absorbing red light, resulting in a blue hue. In the rest of this tutorial we will ignore the absorption coefficient, although we will add a way to tint the atmosphere.

### 📚 Recommended Books

#### Coming Next…

In this tutorial, we have derived a very general form of the equations that govern **single scattering**. The approach described is, in theory, applicable to all translucent volumes receiving light from a single source.

The two key aspects are, of course, the transmittance function ![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

![Rendered by QuickLaTeX.com S](../../assets/4b8b5ff505466deb.png)


You can find all the post in this series here:

- Part 1.
[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374) **Part 2.**[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404)- Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce the volumetric atmospheric scattering presented in this tutorial.

## Leave a Reply Cancel reply