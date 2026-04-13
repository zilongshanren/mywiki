---
title: 'Spectral rendering, part 1: Spectra'
url: http://momentsingraphics.de/SpectralRendering1Spectra.html
published: '2025-11-06'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Spectral rendering, part 1: Spectra

In my [previous blog post](http://momentsingraphics.de/Radiometry2Photometry.html), I explained spectral radiometric quantities and a few basics of spectral rendering.
In this blog post series, we dive into much more detail on spectral rendering.
I present a specific way to implement it in a [real-time path tracer](https://github.com/MomentsInGraphics/path_tracer/tree/spectral) and demonstrate what advantages it brings compared to RGB rendering.
RGB rendering is still by far the most common way to do rendering.
Colors just get multiplied component-wise, i.e. red times red, green times green and blue times blue.
That is a poor approximation of our physical reality.
In practice many of the issues that this causes are covered up by manual color grading.
Spectral rendering offers more accurate color reproduction, more independence of the choice of color spaces, support for unusual light spectra and all that at a rather negligible computational cost.
It is not an obscenely expensive theoretical avenue for offline rendering, but a viable addition to real-time renderers (rasterizers and path tracers alike) that can be made to work with existing assets.
If you do not believe me, maybe these posts can change that.
It does not hurt to read the [series on radiometry](http://momentsingraphics.de/RadiometryOverview.html) first, but in principle, this series is self-contained.
This first part focuses on what kinds of spectra we need to specify a scene and how we can get them.

## Problem statement

Colors of light are a more complex phenomenon than what the human eye can perceive.
To completely describe the color of a single light source, we need an illuminant spectrum \(i(\lambda)\), which maps a wavelength \(\lambda\in[360~\mathrm{nm},830~\mathrm{nm}]\) in the [visible spectrum](https://en.wikipedia.org/wiki/Visible_spectrum) to the amount of light being emitted at that wavelength.
[Figure 1](http://momentsingraphics.de#illuminant_spectrum) shows an example of a fairly complicated illuminant spectrum.
As explained in my [post on spectral radiometry](http://momentsingraphics.de/Radiometry2Photometry.html), such an illuminant spectrum can describe spectral flux, spectral radiance or any other radiometric quantity.

When light hits a surface, light of a different color will be reflected.
That is due to the reflectance spectrum \(a(\lambda)\) of the surface, which provides the surface albedo for each wavelength, i.e. the fraction of light at that wavelength that gets reflected.
In general, the albedo depends on the direction of incoming light and we will account for that later, when we make our BRDF spectral.
Each path produced by a [path tracer](http://momentsingraphics.de/PathTracingLectures.html), accounts for \(n-1\) bounces, where \(n\) is the path length.
Each surface point where a bounce happens has a different reflectance spectrum \(a_1(\lambda),\ldots,a_{n-1}(\lambda)\).
Real-time renderers are often mostly focused on direct illumination such that there is only one reflectance spectrum to worry about (because \(n=2\)).
I will formulate the more general case here, but I want to emphasize that all of this is compatible with rasterization.
The color of the light spectrum after all these bounces is given by the product of all these spectra:

This formula glosses over various scalar factors that do not depend on the wavelength:
If \(i(\lambda)\) provides [spectral radiance](http://momentsingraphics.de/Radiometry2Photometry.html), the missing factors at each path vertex are the BRDF (normalized to albedo 1), the cosine term and the reciprocal of the density used for importance sampling of directions.
My [path tracing lectures](http://momentsingraphics.de/PathTracingLectures.html) describe these in more detail.
The equation above focuses on the part of the computation that an RGB renderer would perform by multiplying RGB triples for surface colors by colors of light sources.
[Part 2](http://momentsingraphics.de/SpectralRendering2Rendering.html) discusses the efficient implementation of these equations.

Next, we turn that into an RGB color that we can display on a screen.
For that, we use the [CIE XYZ color matching functions](https://en.wikipedia.org/wiki/CIE_1931_color_space#Color_matching_functions) \(\bar{x}(\lambda), \bar{y}(\lambda), \bar{z}(\lambda)\).
These functions model how the human visual system perceives color and are shown in [Figure 2](http://momentsingraphics.de#xyz_color_matching).
We use them to reduce the spectrum \(s(\lambda)\), which reaches the camera, into an XYZ triple:

In the next step, we convert from XYZ to linear sRGB, also known as [Rec. 709](https://en.wikipedia.org/wiki/Rec._709), using a linear transform:

We could easily be using other color spaces here, e.g. [Rec. 2020](https://en.wikipedia.org/wiki/Rec._2020) for HDR screens with wide gamut.
We may then apply gamut compression, color grading and tone mapping, or if we want to keep it simple, we just clamp each RGB value to the range from 0 to 1 (more on that in [part 3](http://momentsingraphics.de/SpectralRendering3Results.html#Gamut_compression)).
Finally, we apply the non-linearity of sRGB to get to an sRGB triple.
This non-linearity is given by:

We apply it to each channel separately:

\[R_\mathrm{srgb} := E(R_\mathrm{linear}),~ G_\mathrm{srgb} := E(G_\mathrm{linear}),~ B_\mathrm{srgb} := E(B_\mathrm{linear})\]Then we multiply these values by 255, round to an integer and in doing so we have our usual 24-bit sRGB color for display on a (LDR) monitor.

![xyz_color_matching](../../assets/69391587ebf4680e.svg)


**Figure 2:**A plot of the CIE XYZ color matching functions as defined in 1931. The colors of the three graphs are chosen arbitrarily.

At this point, we have defined the color of a pixel: We need three integrals over products of a color matching function, \(n-1\) reflectance spectra and an illuminant spectrum. Doing so, may seem unreasonably expensive on first sight, especially when the alternative is RGB rendering. On top of that, it is not clear how we are supposed to acquire all these spectra in the first place. Do we let artists draw a graph for a reflectance spectrum for every pixel of every texture? Probably not. The remainder of this series will address these questions and show why the effort is worthwhile.

## RGB rendering

Before we come up with a spectral renderer, let us look back at what we have learned and relate that to RGB rendering.
There is an interpretation of RGB rendering that is compatible with spectral rendering.
We can pretend that our illuminant spectrum \(i(\lambda)\) emits light at exactly three wavelengths, one for red, one for green and one for blue.
For this purpose, we could for example use the three primaries used by [Rec. 2020](https://en.wikipedia.org/wiki/Rec._2020), which are monochromatic light at \(630~\mathrm{nm}\) (red), \(532~\mathrm{nm}\) (green) and \(467~\mathrm{nm}\) (blue).
Then for the reflectance spectra, we only need to know the albedos at these three wavelengths, which we pretend correspond to the RGB values in our textures.
Then the equations above play out in such a way, that we are just performing component-wise multiplication of RGB triples for illuminants and reflectances.
That is exactly what RGB renderers do, so in this sense you can call them physically-based.

There are a few caveats with that though.
First of all, the reasoning above is mixing up color spaces: RGB rendering is most commonly done in linear sRGB (Rec. 709), not with Rec. 2020.
More importantly, real illuminants just do not have spectra like that.
You can build an illuminant like that, but it will make [colors behave unexpectedly](https://www.youtube.com/watch?v=uYbdx4I7STg).
The [spectrum of daylight](https://lspdd.org/database/2661) is much smoother than that.
Artificial light sources may have sharper peaks, as shown in [Figure 1](http://momentsingraphics.de#illuminant_spectrum), but they will not all have exactly three peaks at exactly the same three wavelengths.
On top of that, many surfaces exhibit [fluorescence](https://en.wikipedia.org/wiki/Fluorescence) such that the reflected light actually has a different wavelength.
If we want colors to behave realistically, we need to work with realistic spectra.

## Data for illuminant spectra

As explained above, we primarily care about two kinds of spectra: Illuminant spectra and reflectance spectra.
Usually, we want a single illuminant spectrum per light source (although we could make it depend on position and direction).
If you have a real light source, you can use a spectrometer to measure its illuminant spectrum.
If you do not happen to have a spectrometer at hand, but your light source is sold in the European Union, you can also just check its energy label.
It will include a graph of the illuminant spectrum and you can extract it from that image if you feel so inclined.
[Figure 3](http://momentsingraphics.de#illuminant_spectrum_energy_label) shows an example.
To emphasize what I just said: The EU maintains a [database of illuminant spectra](https://eprel.ec.europa.eu/screen/product/lightsources) with more than half a million different types of light sources!
It includes absolutely all light sources that have been sold in the EU in recent years.

![illuminant_spectrum_energy_label](../../assets/6c24693edae65cf6.jpg)

**Figure 3:**A graph of the illuminant spectrum for one of the light bulbs in my home as found in

[its energy label](https://eprel.ec.europa.eu/screen/product/lightsources/899358). How these graphs are plotted varies a lot and they may have artifacts (e.g. this one is a raster graphic with JPEG artifacts), but you can still get the spectra out of there without too much work.

Alternatively, you can rely on less extensive databases where the spectra are available in a more convenient format.
For the purpose of this blog post series, I have made extensive use of the [light spectral power distribution database (LSPDD)](https://lspdd.org), which has ca. 300 measured illuminant spectra.
My spectral renderer ships with all of them.
The indices that LSPDD assigns to its illuminants have a few gaps and I filled those gaps with monochromatic spectra or other spectra that I wanted to experiment with.

The storage cost is not such a big concern for illuminant spectra. For example, if we store a single spectrum with samples at \(1~\mathrm{nm}\) intervals from \(360~\mathrm{nm}\) to \(830~\mathrm{nm}\) using 32-bit floats, we end up with \((830-360)\cdot4 = 1880\) bytes. If we have 500 different illuminant spectra for 500 different types of light sources (which is a lot), the total storage cost will still be less than a megabyte.

## Data for reflectance spectra

Reflectance spectra are more tricky.
Surface colors are typically controlled by textures.
If we have 500 materials, each with a texture resolution of \(4096\times4096\), we are dealing with 8 billion texels.
With [BC1 compression](https://registry.khronos.org/DataFormat/specs/1.3/dataformat.1.3.html#s3tc_bc1_noalpha), we need half a byte per texel, which makes that amount manageable (4 GB overall).
But what do we do for spectral rendering?
We have to provide a reflectance spectrum for each texel.
A simple approach is to sample wavelengths from \(400~\mathrm{nm}\) to \(700~\mathrm{nm}\) at \(10~\mathrm{nm}\) intervals, which gives us 30 samples.
If we store each sample using one byte, we still end up with

I do not know about you, but I do not have that much VRAM.

And of course, we would also have to create all these reflectance spectra somehow.
Almost all assets out there and all the art pipelines used to create them are built around RGB textures.
It would be desirable to have a method that simply gives us a matching reflectance spectrum for any given RGB triple.
We know the sRGB color for a texel and then we want a reflectance spectrum \(a(\lambda)\) such that the XYZ triple
\begin{aligned}
X_a &:= \int_{360~\mathrm{nm}}^{830~\mathrm{nm}} a(\lambda) \bar{x}(\lambda) \,\mathrm{d}\lambda \\
Y_a &:= \int_{360~\mathrm{nm}}^{830~\mathrm{nm}} a(\lambda) \bar{y}(\lambda) \,\mathrm{d}\lambda \\
Z_a &:= \int_{360~\mathrm{nm}}^{830~\mathrm{nm}} a(\lambda) \bar{z}(\lambda) \,\mathrm{d}\lambda
\end{aligned}
matches this sRGB color exactly (once we convert it to sRGB as described above).
Finding such a spectrum is a problem known as spectral upsampling.
I have published a [solution](http://momentsingraphics.de/Siggraph2019.html) for this problem at SIGGRAPH 2019 and that is what this blog post will focus on.
If you want to learn more about alternative solutions, you can read the related work section of this [paper](http://momentsingraphics.de/Siggraph2019.html).

## Fourier sRGB

The spectral upsampling method that I will use in this blog post series relies on a preprocessing step applied to each sRGB texture.
This step uses a 3D lookup table of resolution \(256^3\) to convert the sRGB color for each pixel to a color space that I dubbed [Fourier sRGB](http://momentsingraphics.de/MAM2019.html).
[Figure 4](http://momentsingraphics.de#fourier_srgb_lut) shows this lookup table.
Just like sRGB, Fourier sRGB describes a color using three numbers and in general, they will be fairly close to the original sRGB colors.
As a result, you can compress Fourier sRGB textures the same way as sRGB textures, e.g. using [BC1](https://registry.khronos.org/DataFormat/specs/1.3/dataformat.1.3.html#s3tc_bc1_noalpha).
The spectral renderer will only ever work with these Fourier sRGB textures, the original sRGB versions are no longer needed during rendering.

**Figure 4:**The 3D lookup table that is used to get from sRGB to Fourier sRGB. The x-axis is \(R_\mathrm{sRGB}\), the y-axis \(G_\mathrm{sRGB}\) and \(B_\mathrm{sRGB}\) grows from 0 to 1 as the video is playing.

Now suppose we have traced a ray that hit a surface point and at that surface point, we have sampled a Fourier sRGB texture.
Sampling is done the same way as for sRGB textures with a format that indicates that we apply the inverse sRGB non-linearity \(E^{-1}\) upon sampling (e.g. using [VK_FORMAT_BC1_RGB_SRGB_BLOCK](https://registry.khronos.org/vulkan/specs/latest/man/html/VkFormat.html)).
We now have three numbers \(R_\mathrm{LF}, G_\mathrm{LF}, B_\mathrm{LF}\) (in linear Fourier sRGB, which is what the \(\mathrm{LF}\) stands for).
Based on that, we want to be able to compute the reflectance \(a(\lambda)\) at every wavelength \(\lambda\) in the visible spectrum.
The solution should have the following properties:

- For all wavelengths \(\lambda\), the reflectance \(a(\lambda)\) is in the interval \([0,1]\), i.e. we do not reflect a negative amount of light or more light than we received (energy conservation).
- When we compute \(X_a,Y_a,Z_a\) as explained above and convert from XYZ to sRGB, that matches the original sRGB color exactly (except for errors introduced by rounding to 8-bit values and compression).
- The reflectance spectrum resembles real-world reflectance spectra, i.e. it is a relatively smooth function.

The last point requires further explanation: In [Figure 1](http://momentsingraphics.de#illuminant_spectrum), we saw that illuminant spectra can be spiky and complicated.
Thankfully, reflectance spectra are more well-behaved and smooth.
[Figure 5](http://momentsingraphics.de#reflectance_spectrum) shows an example that is fairly representative in this regard.
There are large databases of reflectance spectra and none of them exhibit sharp peaks or steep slopes or anything like that.
Thus, the reflectance spectra that we get out of our textures should be similarly smooth signals.

The method to compute the spectrum \(a(\lambda)\) from three coefficients is described in [one of my papers](http://momentsingraphics.de/Siggraph2019.html) and [another paper of mine](http://momentsingraphics.de/MAM2019.html) introduced Fourier sRGB.
For the purpose of this blog post, we will just treat this as a black box, or maybe more appropriately as black magic;
I still find it genuinely surprising that the underlying mathematical problems can be solved efficiently.
If you want an explanation, you have to read the two papers.
Let us look at inputs and outputs of this black box then.
First, we invoke a function that turns the linear Fourier sRGB triple \((R_\mathrm{LF}, G_\mathrm{LF}, B_\mathrm{LF})\) into a vector of three so-called Lagrange multipliers \(L\in\mathbb{R}^3\).
To actually evaluate the reflectance \(a(\lambda)\) at a wavelength \(\lambda\), we have to map the wavelength through a warping function, which gives us a so-called phase \(\varphi\in[-\pi,0]\).
[Figure 6](http://momentsingraphics.de#xyz_warp) shows this warping function.
In [part 2](http://momentsingraphics.de/SpectralRendering2Rendering.html#Implementing_wavelength_sampling), we merge that warp with another step, which makes it basically free.
With these preparations taken care of, the formula to evaluate the reflectance \(a(\lambda)\) boils down to:

![xyz_warp](../../assets/52dbee75a72d989d.svg)


**Figure 6:**The warping function that is used to turn a wavelength \(\lambda\) into a phase \(\varphi\).

As shown in [Figure 7](http://momentsingraphics.de#arctan), the way in which this formula uses \(\arctan\) guarantees that \(a(\lambda)\) is indeed in the interval \([0,1]\).
And the Lagrange multipliers \(L\) have been computed in such a way that this spectrum matches the original sRGB color.
At the same time, reflectance spectra constructed like this generally resemble natural reflectance spectra quite well.
To get a sense of what these spectra look like, you should take a look at this [Shadertoy implementation](https://www.shadertoy.com/view/X3cBRl).
You can click on any color and see the graph of the corresponding reflectance spectrum.
I could have just treated the whole path from Fourier sRGB and a wavelength to the reflectance as a black box.
But the intermediate step with the Lagrange multipliers \(L\in\mathbb{R}^3\) is useful, because once you have them, you can efficiently compute the reflectance for many different wavelengths.

![arctan](../../assets/d6adb29217267956.svg)


**Figure 7:**The function \(\frac{1}{\pi} \arctan(x) + \frac{1}{2}\) squeezes any input into the interval \((0,1)\).

## An alternative approach

If you have been very attentive, you may now be wondering whether this is unnecessarily complicated:
We could just be storing the three Lagrange multipliers in our texture instead of the three Fourier sRGB values, right?
And yes, that would work.
In fact, that is very similar to another spectral upsampling technique [[Jakob19]](http://momentsingraphics.de#_Jakob19).
There are two caveats though: First of all, the values of these Lagrange multipliers are all over the place.
They may take extremely large values or extremely small values and have to be stored with sufficient precision.
Using 16-bit floats works well enough, but then we are storing 6 bytes per texel.
And texture formats with 6 bytes are [not widely supported](https://vulkan.gpuinfo.org/listdevicescoverage.php?optimaltilingformat=R16G16B16_SFLOAT&featureflagbit=SAMPLED_IMAGE) by graphics hardware, so maybe we would prefer to pad that to 8 bytes.
Compared to half a byte that we need with BC 1 compression, that is 12 or 16 times more.
It is better to incur a bit more computation than to increase memory and bandwidth requirements that heavily.
Secondly, linear interpolation and filtering of Lagrange multipliers may give rather unintuitive results (see Figure 17 in my [paper](http://momentsingraphics.de/Siggraph2019.html)).

## Conclusions

We now know how to get illuminant spectra and how to turn existing RGB textures into reflectance spectra.
Thus, the most pressing needs in terms of spectral data are taken care of.
If you still want to specify (some of) your illuminant spectra via RGB, you can use upsampling via Fourier sRGB to do so.
For reflectance, you may want to implement special handling for particularly important spectra, e.g. skin, vegetation, hair or metals.
It is not hard to find measured data for all of these cases and [my paper](http://momentsingraphics.de/Siggraph2019.html) also provides the means to store arbitrary reflectance spectra compactly, using more than three Fourier coefficients.

From a practical point of view, the biggest issue with this approach is how we often intertwine rendering and color representation.
Many rendering systems use shader graphs that explicitly rely on the notion that colors are RGB triples.
If these shader graphs merely produce reflectance textures, we can just bake those and convert to Fourier sRGB.
If baking is not an option, we may have to use the sRGB to Fourier sRGB lookup table at run time, which is not cheap but not prohibitively expensive either.
If the shaders operate on RGB to define BRDFs or even aspects of the light transport itself, it may become challenging to define what spectral rendering is supposed to do with that.
These issues depend a lot on the specific choices in a renderer and there is no single silver bullet to overcome them.
In general, the transition to spectral rendering will change the look of existing assets.
[Part 3](http://momentsingraphics.de/SpectralRendering3Results.html) studies the differences.
If it looked the same, we would have no reason to do it.
[Figure 8](http://momentsingraphics.de#teaser_hps) gives a little preview in a case where the differences are quite big.
You can also experiment with it yourself by downloading the [spectral path tracer](https://github.com/MomentsInGraphics/path_tracer/tree/spectral).

In the [next part](http://momentsingraphics.de/SpectralRendering2Rendering.html) of this series, we deal with the actual spectral rendering based on all these spectral data and explain how to define spectral BRDFs.

**Figure 8:**Interactive comparison of RGB and spectral rendering in a scene with high-pressure sodium vapor lamps.

## Downloads and links

## References

[ Jakob, Wenzel and Hanika, Johannes (2019). A Low-Dimensional Function Space for Efficient Spectral Upsampling. Computer Graphics Forum, 38(2).
][Official version](https://doi.org/10.1111/cgf.13626) | [Author's version](https://rgl.epfl.ch/publications/Jakob2019Spectral)

[ Peters, Christoph and Merzbach, Sebastian and Hanika, Johannes and Dachsbacher, Carsten (2019). Using Moments to Represent Bounded Signals for Spectral Rendering. ACM Transactions on Graphics (Proc. SIGGRAPH), 38(4).
][Official version](https://doi.org/10.1145/3306346.3322964) | [Author's version](http://momentsingraphics.de/Siggraph2019.html)

[ Peters, Christoph and Merzbach, Sebastian and Hanika, Johannes and Dachsbacher, Carsten (2019). Spectral Rendering with the Bounded MESE and sRGB Data. Workshop on Material Appearance Modeling. The Eurographics Association.
][Official version](https://doi.org/10.2312/mam.20191304) | [Author's version](http://momentsingraphics.de/MAM2019.html)