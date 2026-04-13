---
title: Understanding Diffraction Grating - Alan Zucconi
url: https://www.alanzucconi.com/2017/07/15/understanding-diffraction-grating/
author: Alan Zucconi
published: '2017-07-15'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

The first post in this series, [The Nature of Light](https://www.alanzucconi.com/?p=6630), introduced the dual nature of light, exhibiting behaviours which are typical of both waves and particles. In this part, we will see how those two aspects are both necessary for iridescence to arise.

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

#### Reflection: Lights and Mirrors:

![](../../assets/05f504cac4387d2c.png)

The scientific literature often refers to a “**ray of light**“, which is a way to indicate the path that photons traverse when travelling through space and interacting with objects. Most **shading models** treat light as made of homogeneous particles, all behaving like ideal billiard balls. Generally speaking, when a ray of light hits a surface, it bounces off with the same incidence angle. Those surfaces act like ideal mirrors, perfectly reflecting light.

Objects rendered with such a technique looks like mirrors. Moreover, if the light comes from the direction **L**, it can only be seen if the viewer is looking at it from the direction **R**. This type of reflection is also called **specular**, which means “mirror-like”.

In reality, most objects exhibit another type of reflection, called **diffuse**. When a ray of light hits a diffusive surface, it is scattered more or less uniformly in all directions. This gives objects a uniform, diffuse coloration.

![](../../assets/c1c9100590813751.png)

Most modern engines (like Unity and Unreal) used to model those two behaviours with different sets of equations. A previous tutorial, [Physically Based Rendering and Lighting Models](https://www.alanzucconi.com/?p=1964), explains the **Lambertian** and **Blinn-Phong** **reflectance** models used for the diffuse and specular reflections, respectively.

Despite looking different, diffuse reflection can be explained with specular reflection alone. No surface is completely flat. One can model a rough surface as made of tiny mirror, each one fully characterised by a specular reflection. The presence of those **micro-facets** scatters rays in all directions, de-facto diffusing the incoming light.

![](../../assets/ddbee3421533fe92.png)

The disalignment of the micro-facets is often modelled by physically based shaders with properties such as “**Smoothness**” or “**Roughness**“. You can read more about this on the Unity page that explains the [Smoothness](https://docs.unity3d.com/Manual/StandardShaderMaterialParameterSmoothness.html) property available in its Standard Shader.

![](../../assets/5361e2b97eb70293.png)

#### Light As a Wave

Modelling rays of light as made out of particles is very convenient. However, it prevents us from replicating behaviours that many materials exhibit; iridescence included. Certain phenomena can only be understood if we accept the fact that light, under certain conditions, behaves like a wave.

Most shaders treat light as a particle. A result of this massive simplification is that light is subjected to an** additive composition**. If two rays of light reach a viewer, their intensity is simply added. The more rays a surface emits, the brighter it is.

![](../../assets/f96b3ea932197144.gif)

In reality, this is not the case. If two rays of light reach a viewer, the final colour depends on how their waves interact with each other. The animation below shows how two simple sinusoidal waves can either **amplify** or **cancel** each other out depending on their **phase**.

When two waves are **in phase**, it means that their peaks and troughs are perfectly aligned: in this case, the resulting wave is amplified. When the opposite happens, they can literally destroy each other. This means that if two rays of light hit a viewer in the right configuration, is as if no light at all is received.

Wave interaction can indeed sound weird. However, it is something that we have all experienced in our everyday life. Science communicator Derek Muller explains this beautifully in his video called [The Original Double Slit Experiment](https://www.youtube.com/watch?v=Iuv6hY6zsd0), where he shows **constructive** and **destructive interference** between water waves.

But What has this to do with light and iridescence? Iridescence is caused by the interaction of different wavelength of light. Certain materials can reflect photons in just the right way, amplifying certain colours and destroying others. The rainbow pattern that one can experience is the result of that interaction.

#### Diffraction

![](../../assets/fc7842047ae2b4cc.gif)

In the first section of this post, we have explored a type of interaction between light and matter: reflection. Reflection occurs when light is modelled as a particle. When we treat light as a wave, however, a new set of behaviours arise. One of them is called **diffraction**. If all of the incoming light reaches the surface at the same angle, we have a **planar wave**. *Directional lights* in Unity, for instance, produce planar waves. When a planar wave passes through a slit, it bends as seen in the animation below:

If light passes through two different slits, two new wave fronts will be generated. And as discussed before, those two new light waves could potentially interact with each other. The animation below shows how light behaves when two such slits are present, and it is possible to see that they indeed interact both constructively and destructively.

![](../../assets/8757f96d15f89773.gif)

We now have all the necessary elements to discuss why iridescence occurs.

##### Diffracting Grating

When a planar wave passes through a slit or reflects onto a bump, it bends, creating a new spherical wavefront. This means that light is scattered in all directions, similarly to what happens in the case of a diffuse reflection. If the material surface is irregular, the resulting planar waves scatter randomly, and no interference pattern emerges at a macroscopic level.

Some materials, however, possess surface patterns which repeat at a scale that is comparable with the wavelength of the incoming light. When this happens, the regularity of the pattern causes the diffracted wavefronts to interact in a repeating, nonrandom way. The resulting interaction produces a repeating interference pattern that can be appreciated at a macroscopic scale.

The abovementioned effect takes the name of **diffraction grating**. Some wavelengths of light will be greatly amplified, while others will be cancelled out. Since different wavelengths correspond to different colours, diffraction grating causes reflections of certain colours to be featured appear prominently.

That is the mechanism that allows iridescence to occur on surfaces that feature repeating pattern. This is often the case in Nature, where insects’ exoskeletons and birds’ feathers present microscopic scales arranged in a repeated pattern. In the image below, you can see a zoomed peacock’s feather.

![](../../assets/5f93b2747714e255.jpg)

#### Conclusion

The next post in this series, [The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682), will show how this particular type of iridescence can be modelled mathematically. Once the equations are derived, they will be easy to implement in a shader.

You can find the complete series here:

- Part 1.
[The Nature of Light](https://www.alanzucconi.com/?p=6630) - Part 2.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6703)(Part 1) - Part 3.
[Improving the Rainbow](https://www.alanzucconi.com/?p=6806)(Part 2) - Part 4.
**Understanding Diffraction Grating** - Part 5.
[The Mathematics of Diffraction Grating](https://www.alanzucconi.com/?p=6682) - Part 6.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6767)(Part 1) - Part 7.
[CD-ROM Shader: Diffraction Grating](https://www.alanzucconi.com/?p=6791)(Part 2) - Part 8.
[Iridescence on Mobile](https://www.alanzucconi.com/?p=6819) - Part 9.
[The Mathematics of Thin-Film Interference](https://www.alanzucconi.com/?p=6821) - Part 10.
[Car Paint Shader: Thin-Film Interference](https://www.alanzucconi.com/?p=6823)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package for the CD-ROM Shader effect on [ Patreon](https://www.patreon.com/posts/13032957).

## Leave a Reply Cancel reply