---
title: 'Radiometry, part 1: I got it backwards'
url: http://momentsingraphics.de/Radiometry1Backwards.html
published: '2025-01-12'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Radiometry, part 1: I got it backwards

Radiometric quantities are crucial for physically-based rendering. These physical quantities enable us to formulate how much light there is in a scene, where it is and which way it is going. In the end, rendering is all about figuring out what light reaches a camera and how. Without radiometry, there is no way to formalize this problem. For example, the [rendering equation](http://momentsingraphics.de/ToyRenderer4RayTracing.html#The_rendering_equation), which is the backbone of modern rendering, is formulated in terms of radiance (a radiometric quantity). When you write a path tracer, there are two common sources of errors that result in bias. One is an insufficient understanding of Monte Carlo integration and probability theory when it comes to advanced [importance sampling strategies](http://momentsingraphics.de/ToyRenderer4RayTracing.html). The other is that you are not even trying to compute the right integral because of a flawed understanding of radiometry. There is a common way to explain radiometry by arguing in terms of differential quantities and limits. I always found that a bit confusing. Thus, we take a completely different route here. We start with the most important quantity for rendering, radiance, and use integrals to work our way towards all the other quantities.

## Going backwards

To motivate this approach, let us briefly consider the alternative. Feel free to skip this part if you have never seen another introduction to radiometry. In all the text books and lectures that I have seen, explanations start with radiant energy and then work their way to flux, irradiance and radiance. In many ways, it is neat to start with radiant energy because it can be considered the most tangible unit. If you count photons and add up their individual energy, you get radiant energy. Radiant energy heats up cars in the summer and shows up on your electricity bill when you turn on the lights. On the other hand, it is hardly ever relevant in renderers. To get from radiant energy to more relevant quantities like radiance and irradiance, you need to argue in terms of differential quantities. For example, [PBRT writes](https://www.pbr-book.org/3ed-2018/Color_and_Radiometry/Radiometry#x1-Radiance): “Irradiance and radiant exitance give us differential power per differential area at a point \(p\).” To support that, there are formulas such as

When I first learned these things, I found that quite confusing. In terms of notation, that looks like a derivative but it is not like any derivative you would have computed in high school. For starters, \(\Phi(p)\) is not really a function of a point \(p\). It is flux and it depends on the choice of an area in space. So then it makes sense that the denominator has \(A\), not \(p\), but how do you compute that? Overall, the formula conveys the right intuition: You think about what happens when you measure something for a particular surface area and then let this surface area shrink to zero. But it is not the most intuitive construction and it is difficult to grasp it in a strictly mathematical sense. Besides, some important aspects are rather hidden: The orientation of the considered surface area matters but its shape does not.

If you are somewhat confused now, I have made my point. This type of derivative shows up in introductions to radiometry and almost nowhere else in graphics. It is easy to dismiss it. On the other hand, there is something we do in graphics all the time: Computing integrals. The core of a path tracer is [Monte Carlo integration](http://momentsingraphics.de/ToyRenderer4RayTracing.html#Monte_Carlo_integration_with_area_sampling). You cannot understand physically-based rendering without understanding such integrals. And in the end, a renderer mostly computes radiance. It is quite [practical](http://momentsingraphics.de/PathTracingWorkshop.html) (but not advisable) to write a renderer that uses radiance and no other radiometric quantity. The same cannot be said for radiant energy. So why not put radiance and integration at the center of explanations of radiometry? That is what this post is about. We start with an intuitive explanation of radiance and introduce all other radiometric quantities as integrals over radiance. In the end, we still relate radiance to radiant energy and get a clear definition this way.

## Radiance \(\left[\frac{\mathrm{W}}{\mathrm{m}^2\mathrm{sr}}\right]\)

If you have ever done any physically-based rendering, you have worked with radiance, maybe unknowingly. A camera is an imperfect device to measure radiance. The brightness that you get for each pixel is approximately radiance (more accurately, it is luminance, see [part 2](http://momentsingraphics.de/Radiometry2Photometry.html)). There are quite a few reasons, why it is approximate: Most real cameras do not output [linear values](https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ), they have [depth of field](https://en.wikipedia.org/wiki/Depth_of_field), [motion blur](https://en.wikipedia.org/wiki/Motion_blur), [antialiasing](https://en.wikipedia.org/wiki/Spatial_anti-aliasing) due to pixels with finite extent and other effects like [vignetting](https://en.wikipedia.org/wiki/Vignetting) and [chromatic aberration](https://en.wikipedia.org/wiki/Chromatic_aberration). Though, in a renderer it is pretty easy to have a virtual camera with none of these effects. In fact, it takes extra effort to get them. For example, the [pinhole cameras](https://en.wikipedia.org/wiki/Pinhole_camera) used for rasterization have none of these effects.

What such cameras measure is at least proportional to radiance (resp. luminance). So if such a camera is located at a point \(x\in\mathbb{R}^3\) at time \(t\in\mathbb{R}\) and we consider the pixel that observes a surface point in direction \(\omega\in\mathbb{S}^2\) (where \(\mathbb{S}^2\) is the set of normalized direction vectors), we get a radiance

\[L(x,t,\omega)\mathrm{.}\]For now, we think of radiance as a single number but we will consider colors in [part 2](http://momentsingraphics.de/Radiometry2Photometry.html).

A key property of radiance is that it is constant along rays in vacuum. If we move a distance \(s\in\mathbb{R}\) along the ray with origin \(x\) and direction \(\omega\) and along the way we do not encounter surfaces, fog, smoke or anything like that, then we have

\[L(x,t,\omega) = L(x+s\omega,t,\omega)\mathrm{.}\]In other words, if you move your camera closer to a surface, the observed brightness does not change. It will cover a bigger portion of the picture, so overall the camera receives more light from the surface. But that is irrelevant for the radiance since it is concerned with one direction only. This insight is crucial for path tracing: To get the incoming radiance for a direction, we can just trace a ray into this direction and compute the outgoing radiance at the point that this ray hits. This is the main reason why ray tracing is so useful for rendering.

So now we have an intuitive understanding of radiance. In our treatment, that is the fundamental quantity. If you know, \(L(x,t,\omega)\) for all points, directions and times, you know exactly what a scene looks like and you can easily render it with a virtual camera. This function without time \(t\) is called the plenoptic function, also known as radiance field. We will move on to derive all the other quantities from it and then in the end, we will also have a definition of radiance in terms of radiant energy.

## Solid angle \(\left[\mathrm{sr}\right]\)

Though before we move to other radiometric quantities, I owe you an explanation of the unit of radiance. As indicated in the heading above, it is \(\frac{\mathrm{W}}{\mathrm{m}^2\mathrm{sr}}\), i.e. watts per square meter per steradian. Watts and square meters are the [SI](https://en.wikipedia.org/wiki/International_System_of_Units)-units of power and area, respectively. And steradians are the SI-unit of solid angle. So what is a solid angle?

Angles measure the size of sets of directions in 2D. In the same way, solid angles measure the size of sets of directions in 3D space. [Figure 1](http://momentsingraphics.de#angle) visualizes all directions from a point \(q\in\mathbb{R}^2\) to a square. We can treat these directions as direction vectors of length one, i.e. we normalize them. Then they cover a part of a circle of radius one. The circumference of the whole circle is \(2\pi\) but the subset of directions towards the square is shorter. Its length happens to be \(0.552\). And that is the angle subtended by the square in radians: \(\alpha=0.552~\mathrm{rad}\)

![angle](../../assets/a5b245bd8c0f5d32.svg)


**Figure 1:**We look at a square from a point \(q\). The angle \(\alpha\) subtended by it is the length of the arc on the unit circle to which this square projects.

That may be a slightly unusual way to introduce angles but the nice thing about it is that solid angles can be explained in the same way. [Figure 2](http://momentsingraphics.de#solid_angle) illustrates the solid angle subtended by a cube, i.e. all directions from a point \(x\in\mathbb{R}^3\) to the cube. Again, we normalize these direction vectors and get a subset of the unit sphere \(\mathbb{S}^2\). The area of this subset is the solid angle in steradians: \(\Omega=0.161~\mathrm{sr}\)

![solid_angle](../../assets/1c8e9f3220b26677.svg)


**Figure 2:**We look at a cube from a point \(x\). The solid angle \(\Omega\) subtended by it is the area of the spherical polygon on the unit sphere to which this cube projects.

The overall area of the unit sphere is \(4\pi\), so that is the largest meaningful solid angle. In graphics, we often only care about one hemisphere (e.g. directions going upwards from a surface). Then the largest meaningful solid angle is \(2\pi~\mathrm{sr}\). In [another post](http://momentsingraphics.de/ToyRenderer4RayTracing.html#Monte_Carlo_integration_with_area_sampling), I already discussed how to compute the size of a solid angle for a surface when you only know how to integrate over its area.

## Irradiance \(\left[\frac{\mathrm{W}}{\mathrm{m}^2}\right]\)

Now that we understand radiance and solid angle, we can start aggregating radiance in useful ways. Our first goal is to define a sortof overall radiance for a point \(x\) at time \(t\). It may be tempting to simply consider the integral over all directions: \(\int_{\mathbb{S}^2} L(x,t,\omega) \,\mathrm{d}\omega\). That is nice and simple in a mathematical sense but in a physical sense this quantity is not that useful.

A useful quantity could tell how much light a flat surface at point \(x\) receives. Of course, that depends on the orientation of the surface, so we need to know the [normal vector](https://en.wikipedia.org/wiki/Normal_%28geometry%29) of the surface \(n\in\mathbb{S}^2\). When the surface is lit at a grazing angle, the same amount of light will spread out over a greater area compared to perpendicular lighting ([Figure 3](http://momentsingraphics.de#lambert_cosine_law)). Basic trigonometry in [Figure 4](http://momentsingraphics.de#lambert_trigonometry) shows that the ratio of the cross-sectional area of a light beam \(A\) to the lit surface area \(A'\) is given by

where \(\theta\) is the angle between the normal and the direction towards the light. Since both vectors are normalized, that also matches the absolute value of their dot product \(|n\cdot\omega|\). Thus, we define irradiance as

\[E(x,t,n) := \int_{\mathbb{S}^2} L(x,t,\omega) |n\cdot\omega| \,\mathrm{d}\omega\mathrm{.}\]We integrate over all directions and weight the radiance using the dot product. This is a common integral over the unit sphere. One way to compute it in practice is using Monte Carlo integration. We do not need a funny-looking derivative or limit process here.

![lambert_cosine_law](../../assets/55b840bc934f1b95.svg)


**Figure 3:**A light beam of cross-sectional area \(A\) hits a surface area \(A'\). For perpendicular lighting \(A=A'\) but at grazing angles \(A'\) becomes arbitrarily large.

![lambert_trigonometry](../../assets/e11caeb16562aaf3.svg)


**Figure 4:**We shift the light beam around a bit to get a right triangle. Now we can tell that the ratio of the two areas \(\frac{A}{A'}\) is given by the cosine of the angle \(\theta\).

Unlike radiance, irradiance does not depend on a direction vector \(\omega\). However, it only pertains to surfaces with a specific orientation and thus it depends on the normal vector \(n\). In addition, we still have the dependence on a point \(x\) and a time \(t\). Since we integrate over normalized direction vectors \(\omega\), we get a factor with a unit of steradians (i.e. area on the unit sphere), which cancels with the steradians in the unit of radiance. Thus, the unit of irradiance is \(\frac{\mathrm{W}}{\mathrm{m}^2}\).

Intuitively, irradiance tells us how brightly a Lambertian diffuse surface with normal \(n\) is lit at a point \(x\) at time \(t\). The [BRDF](http://momentsingraphics.de/ToyRenderer4RayTracing.html#The_rendering_equation) for a Lambertian diffuse surface is \(f(\omega_i,x,\omega_o)=\frac{a(x)}{\pi}\), where \(a(x)\) is the albedo (i.e. the brightness of the surface itself) at point \(x\). Then the [rendering equation](http://momentsingraphics.de/ToyRenderer4RayTracing.html#The_rendering_equation) tells us that the light reflected by the surface is:

The reflected light is simply proportional to the irradiance. Note that \(L_i\) and \(E_i\) denote incoming radiance/irradiance on one side of the surface. When talking about light leaving a surface, irradiance may also be called radiant exitance.

## Radiant flux \([\mathrm{W}]\)

Irradiance makes statements about individual points on surfaces. The surface does not really matter but its normal vector does. If we really want to say something about the light reaching or leaving a complete surface, we need more integrals. Thus, we now consider a 2D surface in 3D space \(A\subset{\mathbb{R}^3}\). \(A\) could consist of all points on a sphere, a plane, a cube or a triangle mesh. For each point \(x\in A\), we have a normal vector \(n(x)\in\mathbb{S}^2\). Radiant flux is the integral of irradiance over this surface:

\[\Phi_A(t) := \int_A E(x,t,n(x)) \,\mathrm{d}x\mathrm{.}\]It is specific to the surface \(A\) and to a particular time \(t\). Since we have integrated over an area, the \(\mathrm{m}^2\) unit from irradiance cancels and the unit is simply watts.

The specification of light sources is probably the most useful application of radiant flux in renderers. If you make an area light bigger or smaller, you normally do not want to change how much light it emits into the scene overall. But if the brightness is specified in terms of radiance or irradiance, that is going to happen. On the other hand, if it is specified in terms of radiant flux, you can just keep this flux constant as you change the size and get the desired behavior. It is also nice because watts are a familiar unit for power consumption. Though, not all energy consumed by a light source turns into visible light and thus luminous flux is a still more suitable quantity (see [part 2](http://momentsingraphics.de/Radiometry2Photometry.html)).

## Radiant energy \([\mathrm{J}]\)

Now it is just a small step to get to the starting point of most other introductions to radiometry. If we fix a time interval from \(t_0\in\mathbb{R}\) to \(t_1\in\mathbb{R}\), we can use an old-fashioned one-dimensional integral to move from radiant flux to radiant energy:

\[Q_A(t_0,t_1) := \int_{t_0}^{t_1} \Phi_A(t) \,\mathrm{d}t\mathrm{.}\]Radiant energy tells us how much energy reaches the surface \(A\) in the given time interval. Its unit is joule. In a sense, all other quantities are artificial constructs arising from a continuous interpretation of a discrete world. But radiant energy is real. You can count photons to measure it. And that is what sensors for camera pixels or the photoreceptor cells in our eyes do.

## Going forward

Now let us go back to the interpretation of radiance as the quantity measured by a camera. As I said before, this is just an approximation. Sensors count photons and thus they measure radiant energy. They do so within a particular time interval \(t_0,t_1\), namely the exposure time. But if you want to avoid motion blur, you keep that exposure time so short that the scene does not change significantly within that time. Doing so, can be thought of as a limit process that transitions from radiant energy to radiant flux. Each pixel also has a particular area \(A\) and gathers photons within this area. Cameras these days have high resolutions though, so these pixels are tiny and thus we transition from radiant flux to an approximation of irradiance. The camera also has a lens system, so each pixel receives light from the scene from a cone of directions. To avoid depth of field, one may use a small [aperture](https://en.wikipedia.org/wiki/Aperture). Then this cone of directions shrinks and we transition from irradiance to an approximation of radiance. In reality, all these limit processes are imperfect but in a renderer, we really deal with proper differential quantities, especially with radiance.

Limit processes like this are at the core of most other explanations of radiometry. The integrals are a second class citizen. I find the integrals easier to grasp, but if you like the limit processes, maybe this analogy with a camera has helped to understand them a little better.

## Another route: Intensity \(\left[\frac{\mathrm{W}}{\mathrm{sr}}\right]\)

There is one more radiometric quantity. If we integrate radiance in a direction \(\omega\) over a surface \(A\subset\mathbb{R}^3\) and weight it by the cosine term, as for irradiance, we get intensity:

\[I_A(t,\omega) := \int_A L(x,t,\omega) |n(x)\cdot\omega| \,\mathrm{d}x\]We can further integrate intensity over all directions and arrive at flux again:

\[\Phi_A(t) = \int_{\mathbb{S}^2} I_A(t,\omega) \,\mathrm{d}\omega\]In essence, we just swapped the area integration with the directional integration and got a second path to move from radiance to radiant flux. Intensity is useful to describe lighting fixtures using so-called IES profiles. IES profiles measure how much light a light source as a whole emits into a direction \(\omega\). Thus, they provide an integral over the entire area of the light but still resolve things directionally. To be quite precise, IES profiles store luminous intensity, the photometric counterpart of intensity, which we will discuss in [part 2](http://momentsingraphics.de/Radiometry2Photometry.html).

## Conclusions

For a long time, people in real-time rendering could get away without knowing radiometry. The formulas for point lights are simple enough and for everything else some phenomenological approaches ought to give the right appearance. But now that real-time ray tracing is viable, path tracing is a tempting prospect. To write a correct path tracer, a good understanding of radiometry is really important. It answers questions like: “Should I multiply that by a cosine term (or \(4\pi\) or \(r^2\) or overall area)?” These come up all the time. If you keep guessing, it will not be long before the renderer is a mess of bugs that kindof cancel each other out but not quite. Hopefully, my approach to explaining will help some of my readers to grasp these concepts.