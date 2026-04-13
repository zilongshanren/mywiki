---
title: 'Radiometry, part 2: Spectra and photometry'
url: http://momentsingraphics.de/Radiometry2Photometry.html
published: '2025-01-19'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Radiometry, part 2: Spectra and photometry

The radiometric quantities introduced in [part 1 of this series](http://momentsingraphics.de/Radiometry1Backwards.html) are completely color-blind. That is an obvious drawback for rendering. Thus far, our notion is that radiance is a single number, not a color. A fairly common practice in rendering is to have separate radiance values for red, green and blue. If your scene happens to be lit exclusively by light sources with only three wavelengths and does not exhibit [fluorescence](https://en.wikipedia.org/wiki/Fluorescence), that is a physically accurate approach. Unfortunately, real scenes are not that simple. In this post, we describe the physical reality more completely. We consider spectral versions of all radiometric quantities. Then we take a look at human perception of color and brightness, which leads to photometric quantities. Next, we figure out how to handle that efficiently in a renderer. And finally I rant a bit about all the confusion that surrounds this subject.

## The electromagnetic spectrum

Light has wave properties and thus each photon has a wavelength \(\lambda\in\mathbb{R}\). For visible light, it is usually measured in nanometers. Humans mostly see light with wavelengths between \(400~\mathrm{nm}\) and \(700~\mathrm{nm}\). However, pretty much all wavelengths are possible in the [electromagnetic spectrum](https://en.wikipedia.org/wiki/Electromagnetic_spectrum). Your \(5~\mathrm{GHz}\) wifi uses microwaves with a wavelength of \(6~\mathrm{cm}\). Your doctor may take X-ray images using photons with wavelengths around \(10~\mathrm{pm}\).

The way we defined our radiometric quantities, they count photons at all wavelengths. A photon with wavelength \(\lambda\) carries a [radiant energy](http://momentsingraphics.de/Radiometry1Backwards.html#Radiant_energy_\([\mathrm{J}]\%29) of

where \(c\) is the [speed of light](https://en.wikipedia.org/wiki/Speed_of_light) and \(h\) is the [Planck constant](https://en.wikipedia.org/wiki/Planck_constant). So photons of different wavelengths are counted differently because their radiant energy is antiproportional to their wavelength. But they all count.

It is needless to say that this is pretty useless for rendering. The signal from your wifi router does not illuminate the scene, so there is no point in incorporating it into radiometric quantities. Shorter wavelengths, especially [ultraviolet](https://en.wikipedia.org/wiki/Ultraviolet), may be converted to visible light through [fluorescence](https://en.wikipedia.org/wiki/Fluorescence) though, so there is a point in accounting for those. In any case, we need the means to differentiate light at different wavelengths.

## Spectral radiometric quantities

To define that cleanly, we start with [radiant energy](http://momentsingraphics.de/Radiometry1Backwards.html#Radiant_energy_\([\mathrm{J}]\%29) and stick to the notion of adding up radiant energy of individual photons. However, we no longer do so for all wavelengths. We only consider photons with a wavelength of \(\lambda\) or less (i.e. in the interval \([0~\mathrm{nm},\lambda]\)). We denote the resulting radiant energy by

We can view this as function of the wavelength \(\lambda\). Since we only consider more photons as we make \(\lambda\) bigger, this function grows monotonically. It is essentially a [cumulative distribution function](https://en.wikipedia.org/wiki/Cumulative_distribution_function), except that it is not normalized to end at a value of one (its unit is still joule).

Of course, this quantity is still pretty useless for rendering. If \(\lambda\) is in the visible spectrum, this radiant energy will incorporate gamma rays and X-rays, because they have shorter wavelengths. It would be nicer to have a quantity that pertains to a single wavelength. To get that, we now take the derivative with respect to \(\lambda\):

\[Q_A(t_0,t_1,\lambda) := \frac{\partial}{\partial\lambda} Q_{A,[0~\mathrm{nm},\lambda]}(t_0,t_1)\mathrm{.}\]This derivative is nothing fancy, just a common one-dimensional derivative. But it gives us a pretty useful quantity: Spectral radiant energy (in wavelength). Since we took the derivative with respect to wavelength, the unit is now \(\frac{\mathrm{J}}{\mathrm{nm}}\).

From this spectral radiant energy, we get spectral versions of all other radiometric quantities as well. For example, we get spectral radiant flux with unit \(\frac{\mathrm{W}}{\mathrm{nm}}\), which relates to spectral radiant energy through

\[Q_A(t_0,t_1,\lambda) = \int_{t_0}^{t_1} \Phi_A(t,\lambda) \,\mathrm{d}t\mathrm{.}\]Basically, we just add a wavelength \(\lambda\) to each parameter list and divide the unit by \(\mathrm{nm}\). Colors are now described by wavelength-dependent functions, which we call spectra. It is not so trivial to deal with them in a renderer. We look into that below, but first we link spectra to RGB colors.

## Photometric quantities

We want to move from physically meaningful spectral quantities to perceptually meaningful quantities that we can display on a screen. Say a pixel of our virtual camera receives spectral radiance \(L(x,t,\omega,\lambda)\). We do not use motion blur or anything like that, so all we want is to convert this spectral radiance to a color for display. To do so, we need the [CIE XYZ color matching functions](https://en.wikipedia.org/wiki/CIE_1931_color_space#Color_matching_functions) \(\bar{x}(\lambda), \bar{y}(\lambda), \bar{z}(\lambda)\). They model how a human standard observer perceives colors and the CIE provides tables for their values. [Figure 1](http://momentsingraphics.de#xyz_color_matching) shows a plot of them. Using these functions, we can convert our spectral radiance to XYZ:

By design, different spectral radiance with the same XYZ values is perceived as the same color by a human (disregarding that color perception is slightly different between individuals). That is known as [metamerism](https://en.wikipedia.org/wiki/Metamerism_%28color%29). From XYZ, we can convert to many other standardized color spaces. For most displays, you should convert to [sRGB, as explained on Wikipedia](https://en.wikipedia.org/wiki/SRGB#From_CIE_XYZ_to_sRGB).

![xyz_color_matching](../../assets/69391587ebf4680e.svg)


**Figure 1:**A plot of the CIE XYZ color matching functions as defined in 1931. The colors of the three graphs are chosen arbitrarily.

Among \(L_X\), \(L_Y\) and \(L_Z\), the value \(L_Y\) is special because it is the [luminance](https://en.wikipedia.org/wiki/Luminance), which is a photometric quantity. In general, if you want to determine a single brightness value from a tristimulus color (e.g. RGB or XYZ), using \(Y\) as defined in CIE XYZ is a perceptually meaningful choice. And having a single brightness value is useful when you reason about lighting. Radiometric quantities also provide a single brightness but it is not perceptually meaningful because it incorporates invisible light. Luminance on the other hand is weighted using \(\bar{y}(\lambda)\), which is carefully designed to model the perceived brigthness for a human standard observer.

Since this concept is useful in many engineering disciplines, there is a complete set of photometric quantities to complement the radiometric quantities we encountered thus far. They also have their own units. Each of them is computed from the corresponding spectral radiometric quantity by multiplying by \(\bar{y}(\lambda)\) and integrating over all wavelengths. The following table helps to translate between them.

| Radiometric quantity | Photometric quantity |
|---|---|
| Radiance \(L(x, t, \omega)\) \([\frac{\mathrm{W}}{\mathrm{m}^2 \mathrm{sr}}]\) | Luminance \([\frac{\mathrm{lm}}{\mathrm{m}^2\mathrm{sr}} = \mathrm{nit}]\) (nit) |
| Irradiance \(E(x, t, n)\) \([\frac{\mathrm{W}}{\mathrm{m}^2}]\) | Illuminance \([\frac{\mathrm{lm}}{\mathrm{m}^2} = \mathrm{lx}]\) (lux) |
| Intensity \(I_A(t, \omega)\) \([\frac{\mathrm{W}}{\mathrm{sr}}]\) | Luminous intensity \([\frac{\mathrm{lm}}{\mathrm{sr}} = \mathrm{cd}]\) (candela) |
| Radiant flux \(\Phi_A(t)\) \([\mathrm{W}]\) | Luminous flux \([\mathrm{lm}]\) (lumen) |
| Radiant energy \(Q_A(t_0, t_1)\) \([\mathrm{J}]\) | Luminous energy \([\mathrm{lm}\,\mathrm{s} = \mathrm{T}]\) (talbot) |

Note that nits and talbots are not [SI units](https://en.wikipedia.org/wiki/International_System_of_Units). Surprisingly, most of these quantities are somewhat familiar from everyday life. If you buy a light bulb these days, its brightness is usually given in lumens, i.e. as luminous flux. The peak brightness of a monitor is given in nits, i.e. as luminance. For spot lights, which mostly illuminate a fairly small cone, candelas are a more useful unit, i.e. luminous intensity.

## Representing spectra

Unlike photometric quantities, spectral quantities give us a complete and physically meaningful description of colors. But at the same time, they amplify the amount of data we need to store quite a bit. Spectra are continuous, so in theory we have to store infinitely many numbers, just to describe one of them. Obviously, that is infeasible. Instead, we may choose to pick a sufficiently large set of wavelengths, say one every \(5~\mathrm{nm}\) and store values for these intervals. For the visible spectrum, we end up with ca. 80 samples. But if you think of storing a texture with millions of pixels and then storing values for 80 wavelengths for each pixel, that is still infeasible. Reducing the number of samples compromises quality at some point.

That gives me an opportunity to shamelessly advertise [my own work](http://momentsingraphics.de/Siggraph2019.html). In a scene description, we mostly deal with two kinds of spectra: Emission spectra provide the color of light sources, whereas reflectance spectra describe surface colors (more technically called albedos). Both are functions of the wavelength, but beyond that, they do not have much in common. A surface cannot reflect more light than it receives, so reflectance spectra always take values between 0 and 1. And if you look at measured reflectance spectra, e.g. the one in [Figure 2](http://momentsingraphics.de#reflectance_spectrum), you find that they tend to be fairly smooth functions. They do not vary rapidly. Contrary to that, emission spectra have no upper bound and some commonly found light sources such as fluorescent tubes have wild spectra with many sharp peaks (see [Figure 3](http://momentsingraphics.de#emission_spectrum)).

![emission_spectrum](../../assets/5584a285dd949299.svg)


**Figure 3:**The emission spectrum of a fluorescent tube has sharp peaks at many different wavelengths.

This fact works to our advantage. We usually only have one color per light source. Storing a table of 80 emissions for 80 wavelengths is viable to describe a light source. And there are many great databases with measured emission spectra, e.g. the [light spectral power distribution database](https://lspdd.org/). On the other hand, we commonly store surface colors in textures, so those have to be stored as compactly as possible. That is where [my paper](http://momentsingraphics.de/Siggraph2019.html) comes into play. The idea is to describe a reflectance spectrum \(a(\lambda)\) by real Fourier coefficients:

The index \(j\) determines the frequency. We always need frequency \(j=0\). Then the cosine in this integral is just constant 1 and we get the average reflectance. And then we go up to as many coefficients as we want to afford in terms of storage. E.g. we may store \(c_0,c_1,c_2,c_3\) into a 4-channel texture.

Then we have to get back from these coefficients to a continous spectrum with values between 0 and 1. And since you are reading “moments in graphics,” the solution of course uses the theory of moments. Read [the paper](http://momentsingraphics.de/Siggraph2019.html) if you want details but the gist of it is that there is a neat formula to compute a spectrum with all the desired properties and this formula is also inexpensive to compute. [Figure 4](http://momentsingraphics.de#bounded_mese) shows the result. These spectra are always between 0 and 1, behave smoothly, have exactly the right Fourier coefficients and generally approximate real-world reflectance spectra well.

![bounded_mese](../../assets/840c91a7e297d87a.svg)


**Figure 4:**Out of 4 real Fourier coefficients, we get an excellent approximation (blue) of the original reflectance spectrum (dotted).

As is, this approach is only useful when we know the reflectance spectrum \(a(\lambda)\) at all wavelengths. But an artist would not normally create a texture with one channel per wavelength. Practically all albedo textures that are fed to renderers use some RGB color space. Therefore, I also came up with a way to convert RGB textures to textures with three real Fourier coefficients. And on top of that, you can transform these coefficients in such a way that they behave a lot like RGB values. I call that [Fourier sRGB](http://momentsingraphics.de/MAM2019.html). That means you can use a preprocessing step to convert all RGB textures to Fourier sRGB and then store those in exactly the same (compressed) manner as common RGB textures. That brings the memory and bandwidth overhead of spectral rendering down to practically nothing (compared to RGB rendering).

## Spectral rendering

Now we know practical ways to describe emission spectra of our light sources and reflectance spectra of our surfaces. But what about the spectral radiance values that a path tracer has to deal with? There are two ways to go about this: The first one is to use lots of samples. For example, you can use 16 wavelengths and then where you would otherwise store an RGB color for a ray, you now store 16 spectral radiance values. But this approach is biased and it is also quite costly to handle that many wavelengths.

A more elegant and, when done correctly, more efficient approach is to treat wavelengths as another dimension over which we integrate with Monte Carlo estimators. Hero wavelength spectral sampling [[Wilkie2014]](http://momentsingraphics.de#_Wilkie2014) is a good way to do that while keeping the variance low in most cases. We pick one wavelength uniformly at random (maybe using a [blue noise texture](http://momentsingraphics.de/BlueNoise.html)). Another three wavelengths are picked with equidistant spacing with respect to that first wavelength. So if we picked \(421~\mathrm{nm}\) at random, we also use \(521~\mathrm{nm}\), \(621~\mathrm{nm}\) and \(721~\mathrm{nm}\). We evaluate all the relevant reflectance and emission spectra at all of these wavelengths, multiply the respective values and eventually get four values of spectral radiance reaching the camera. Then we use the XYZ color matching functions to directly turn that into a tristimulus color, which we add to the frame buffer.

For peaky emission spectra like the one in [Figure 3](http://momentsingraphics.de#emission_spectrum), hero wavelength sampling may still cause too much noise. In that case, I recommend to sample wavelengths proportionally to the emission spectrum. This can be combined with uniform jittered sampling, which essentially gives us a non-uniform hero wavelength sampling. See Section 4.4 in [my paper](http://momentsingraphics.de/Siggraph2019.html) for details.

All of this is more costly than RGB rendering but not by as much as you might think. It does not cost significant bandwidth and mostly boils down to a bit of additional computation in fragment shaders. And it is compatible with RGB assets. There is still a perception that spectral rendering is this crazy expensive predictive rendering thing that is completely out of reach in real time. Hopefully, I have been able to convince you that this is misplaced. It is viable today and sweeps away a lot of color reproduction issues.

## Confusions

There is [a lot of confusion](https://xkcd.com/1882/) around digital color reproduction. Honestly, when I write about it, I also feel like I am walking on egg shells because I would hate to make a bad situation worse. One source of confusion is that spectra are continuous and storing them exactly takes too much storage. If you only store values for a small number of wavelengths, you have to interpolate and how you do that influences how you compute integrals. The next person dealing with the same data is probably going to do something differently and that is enough to cause a discrepancy. My [moment-based spectra](http://momentsingraphics.de/Siggraph2019.html) are truly continuous, so that might help a bit.

The other big source of confusion is the multitude of tristimulus color spaces, i.e. ways to define some sort of RGB from XYZ. There are many choices to begin with and they typically depend on the choice of a white point, i.e. a spectrum that is considered white (which is usually [illuminant D65](https://en.wikipedia.org/wiki/Illuminant_D65) but not always). Also, XYZ itself has changed. I linked the 1931 standard above, which is still widely used, but the latest version from 2006 defines slightly different color matching functions \(\bar{x}(\lambda), \bar{y}(\lambda), \bar{z}(\lambda)\). And then there is a whole stack of technologies messing with these tristimulus color spaces: Image editing software, renderers, browsers, operating systems, graphics drivers, displays, printers, and so forth. What a display or a printer do when you output a particular RGB-triple from a program depends on many things. Next time you go shopping for TVs, you can marvel at how diverse the color reproduction is on that wall of TVs showing the same station. Fortunately, the human visual system also does its own white balance, which means that we are nearly blind to these discrepancies without a side-by-side comparison. Unfortunately, that also makes them hard to detect and debug.

When spectral upsampling methods are used to get from RGB to spectra, many of these confusions suddenly enter into the otherwise so clean world of spectral rendering. So if you venture into this direction, be sure to make up your mind on the choice of the XYZ standard, the white point and the exact RGB space you are using. Then maybe, you will not end up regretting your choice once you have a few gigabytes of assets depending on it.

## Conclusions

This post ended with a bit of a downer. The good news is that the definition of spectral radiometric quantities is rock solid. And if you develop a spectral renderer, you are in control of what spectra you feed to it. It is not a matter of right or wrong, it is a matter of establishing standards that work for the artists creating assets. Ideally, that also works across companies. Colors are represented by continuous spectra. Photometric units may be used on top of that to define brightness. In a spectral renderer, the light transport is not tied to human perception in any way. If you choose to change something about the color space used for output on a screen, e.g. to account for properties of a camera instead of the human visual system, you can do that immediately without recreating all assets.

## References

[ Wilkie, Alexander and Nawaz, Sehera and Droske, Marc and Weidlich, Andrea and Hanika, Johannes (2014). Hero Wavelength Spectral Sampling. Computer Graphics Forum (proc. EGSR), 33(4). ][Official version](https://doi.org/10.1111/cgf.12419) | [Author's version](https://cgg.mff.cuni.cz/publications/hero-wavelength-spectral-sampling/)