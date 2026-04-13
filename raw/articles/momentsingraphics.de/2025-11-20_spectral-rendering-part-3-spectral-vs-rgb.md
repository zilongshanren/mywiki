---
title: 'Spectral rendering, part 3: Spectral vs. RGB'
url: http://momentsingraphics.de/SpectralRendering3Results.html
published: '2025-11-20'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Spectral rendering, part 3: Spectral vs. RGB

Now that we have a spectral renderer, it is time to see if it was worth the effort.
I hope you agree with my reasoning in [part 1](http://momentsingraphics.de/SpectralRendering1Spectra.html#RGB_rendering), that RGB rendering does not match the physical reality, but does it really matter?
We will now compare RGB rendering to spectral rendering using my [spectral path tracer](https://github.com/MomentsInGraphics/path_tracer/tree/spectral).
In the process, we will look at various types of light sources.
RGB rendering simply multiplies RGB triples of illuminants and textures component-wise to arrive at the linear RGB color displayed on screen.
Spectral rendering uses proper illuminant spectra (mostly from [LSPDD.org](https://lspdd.org)) and reflectance spectra that are upsampled from sRGB using [Fourier sRGB](http://momentsingraphics.de/SpectralRendering1Spectra.html#Fourier_sRGB).

Throughout this blog post, I will be using figures that allow you to compare results in an interactive fashion. Clicking on the tabs or pressing number keys 1, 2, 3 selects an image to display (RGB rendering, spectral rendering or the illuminant spectrum). The mouse wheel lets you zoom in/out and you can pan by clicking and dragging. At the bottom you see magnified insets of all three images for the cursor position (I am well aware that this part is not useful for the spectrum).

## Illuminant E and D65

In [Figure 1](http://momentsingraphics.de#illuminant_e) we use illuminant E, which is just a constant spectrum.
Based on how we have constructed the [Fourier sRGB lookup table](http://momentsingraphics.de/SpectralRendering1Spectra.html#Fourier_sRGB), we expect RGB rendering and spectral rendering to give nearly the same result here.
The reason for that is that we simply used the CIE XYZ color matching functions without multiplying by an illuminant.
Thus, our illuminant is implicitly constant (i.e. illuminant E) and we expect that directly reflected illuminant-E light will have exactly the sRGB color from the original texture.
The only reason why the results between RGB or spectral rendering might differ slightly is that we account for indirect illumination in these renderings.
Indeed, the results are nearly indistinguishable.

**Figure 1:**Our test scene under illuminant E. RGB and spectral rendering produce nearly identical results.

Some might argue that we should have used [illuminant D65](https://en.wikipedia.org/wiki/Illuminant_D65) instead of illuminant E to construct the lookup table, because that has been defined to be white light.
Most spectral upsampling techniques in the literature do not do so.
The best argument for this design decision that I have heard is that sRGB (255, 255, 255) should correspond to a constant reflectance spectrum with value one.
Anything else would be counterintuitive: Reflection on perfect white surfaces would change the color of incoming light.
If a non-constant illuminant is baked into the upsampling technique, this criterion may be violated.

[Figure 2](http://momentsingraphics.de#illuminant_d65) shows results for illuminant D65.
Indeed, there are visible differences in the colors, especially in the reds.
Though, they are relatively minor.

**Figure 2:**Our test scene under illuminant D65. There are minor but visible differences between RGB and spectral rendering.

Neither of these two results is inherently better or more correct than the other. RGB rendering relies on the rather unphysical notion that all light has one of only three wavelengths. Strictly speaking, even this interpretation is not entirely compatible with how the sRGB color space is defined since its primaries are not monochromatic spectra. Though, under the set of definitions used to define the scene in RGB rendering, the result of RGB rendering is (tautologically) correct.

For the spectral renderer, we utilize a more complete representation of the illuminant in the form of an illuminant spectrum.
And we have used [Fourier sRGB](http://momentsingraphics.de/MAM2019.html) to come up with smooth reflectance spectra that match our surface sRGB colors.
Thus, the renderer models the physical reality more accurately, but that does not automatically mean that we get a more accurate rendition of the scene.
The only information that we have about the reflectance spectra is their sRGB color, so the upsampled reflectance spectra may not match those that the material intended by the artist (or the captured sample) would have.
We get an interpretation that is compatible with everything we know about the scene and with physical light transport, but nothing more than that.

## Other smooth illuminant spectra

In [Figure 3](http://momentsingraphics.de#illuminant_led), we use the spectrum of a warm-white light-emitting diode (LED).
Like most LEDs, this one has a relatively smooth illuminant spectrum composed of two lobes that mostly cover visible wavelengths (hence the good energy efficiency).
Once again, the most visible differences are in the reds.
While spectral rendering made them slightly brighter for illuminant D65, this time it is making them darker.
Greens also shift a bit, but overall the differences are still relatively minor.
One of the design goals for white illuminants is good [color rendering](https://en.wikipedia.org/wiki/Color_rendering_index), i.e. making sure that colors look like they would under illuminant D65.
LEDs generally perform relatively well in this regard, so it is unsurprising that the differences are minor here.

**Figure 3:**Our test scene under an LED spectrum. All colors shift a bit, especially the reds and greens.

[Figure 4](http://momentsingraphics.de#illuminant_incandescent) uses an incandescent spectrum, i.e. what you would get out of an old light bulb with a filament that heats up.
In the visible spectrum, the incandescent illuminant spectrum is essentially a smooth ramp that keeps going up as you move into infrared.
In other words, these light sources mostly emit invisible lights, which is why they are so inefficient that they have been [prohibited in most countries](https://en.wikipedia.org/wiki/Phase-out_of_incandescent_light_bulbs).
Here, the differences between RGB and spectral rendering start to become more interesting.
With RGB rendering, blue becomes quite saturated and slightly green, while bright red turns slightly orange.
With spectral rendering, blue surfaces become less saturated and get a yellow tint from the illuminant.
RGB rendering is not capable of reducing the saturation of colors in this manner.
With spectral rendering, illuminant spectra with strong maxima around certain colors will always do so.

**Figure 4:**Our test scene under an incandescent spectrum. Compared to RGB rendering, spectral rendering desaturates surface colors somewhat.

## Spiky illuminant spectra

Now we move on to illuminant spectra with many distinct peaks.
The most common examples are coated fluorescent lamps (CFL), as shown in [Figure 5](http://momentsingraphics.de#illuminant_cfl).
The highly saturated balloons become a bit brighter with spectral rendering, especially the green ones.
Blues and reds also shift a bit, but overall, the changes here are not that big.

**Figure 5:**Our test scene under a CFL spectrum. This time, the greens are particularly affected.

Metal halide (MH) lamps can have even more spiky spectra as shown in [Figure 6](http://momentsingraphics.de#illuminant_mh).
While the light of this lamp is relatively close to being white, its effect on surface colors in the spectral renderer differs drastically from that of other white illuminants like D65 or the LED considered above.
Many saturated surface colors get a blue tint and become much less saturated.
The choice of a different white illuminant has drastically altered the look of this scene in the spectral renderer.
The RGB renderer reduces the illuminant spectrum to RGB before using it.
Therefore, white is white and surfaces keep their colors.

**Figure 6:**Our test scene under a MH spectrum. With spectral rendering, the saturation of saturated surfaces is drastically reduced.

## (Nearly) monochromatic spectra

The most drastic differences between RGB rendering and spectral rendering can be observed when the illuminants are nearly monochromatic, i.e. they emit most of their light close to one specific wavelength.
For example, low-pressure sodium-vapor lamps emit almost all of their light near a wavelength of \(589~\mathrm{nm}\).
They are commonly used as street lamps, since they have been available since the 1920s and have an efficiency that rivals modern LEDs.
High-pressure sodium (HPS) lamps have slightly broader spectra and [Figure 7](http://momentsingraphics.de#illuminant_hps) uses one of those (since we have another fully monochromatic example below).
Light never changes its wavelength in the spectral renderer (since we do not model fluorescence).
Thus, the nearly monochromatic light of the HPS lamps stays nearly monochromatic as it scatters throughout the scene.
No matter what color a surface has, the reflected light will have a color very close to the incoming light, just of different brightness.
In the RGB renderer, we just treat this light as a mix of red and green and thus surface colors are not overridden like that.
We would be able to get such an effect for red light, green light or blue light, but not for a mixture of those.
In this way, RGB rendering hands out special treatment for these three light colors, whereas a spectral renderer can deal with monochromatic light of any wavelength.

**Figure 7:**Our test scene under a HPS spectrum. With spectral rendering, the color of the light overrides the color of surfaces almost completely.

To drive this point home [Figure 8](http://momentsingraphics.de#illuminant_500nm), uses perfectly monochromatic light at \(500~\mathrm{nm}\).
Now the spectral rendering is perfectly monochromatic.
Different pixels only differ in their overall brightness.
The RGB renderer treats this illuminant as a mixture of blue and green and thus surface colors are retained to some extent.

**Figure 8:**Our test scene under monochromatic light at \(500~\mathrm{\mathrm{nm}}\). With spectral rendering, colors only differ by their brightness.

## Gamut compression

Actually, it is not quite right to say that the monochromatic light at \(500~\mathrm{\mathrm{nm}}\) is a mixture of green and blue. It mixes positive amounts of green and blue and a negative amount of red. Its RGB representation is \((-1,1,0.36)\). A color with negative entries like that is called out of gamut. The sRGB gamut is relatively small, so all non-primary colors that are a bit more saturated will be out of gamut. And monochromatic spectra are the most saturated spectra that you can possibly have.

That poses a challenge for both RGB and spectral rendering, but for RGB rendering, it is more pronounced.
The spectral renderer is mostly oblivious to RGB color spaces.
It just models realistic light transport and estimates the spectrum of light that reaches the camera.
RGB color spaces only come into play for storing the end result and displaying that on a screen.
To display an RGB color that may be out of gamut on a screen, gamut compression should be used and there is an [ACES standard](https://docs.acescentral.com/system-components/output-transforms/technical-details/gamut-compression/) for that.
I considered implementing that, but there are limits to how much work I want to put into a blog post.
For the results shown here, I simply clamped RGB vectors to the interval \([0,1]\) before converting to sRGB.
Thus, you should keep in mind that some of the images above have an “invisible third channel” with negative values.

## Conclusions

In spite of being extremely wide-spread, RGB rendering clashes quite badly with principles of physically-based rendering. While we invest a lot of effort to model or measure various materials or light sources, we simultaneously put an overly simplistic model of color at the foundation of it all. RGB color spaces are designed to be used for display devices and they are perfectly fine for this purpose. However, they are not meant to be used to simulate light scattering and doing so in RGB requires assumptions that are far from being physically-based.

Spectral rendering enables accurate color reproduction under all sorts of illuminants. While the primary colors red, green and blue play a special role in RGB rendering, spectral rendering can handle monochromatic illuminants of all colors and arbitrary mixtures thereof. That opens up new possibilities in lighting design, where the spectra of light sources can influence the colors of surfaces in ways that would not be possible with RGB rendering. It also makes it much easier to reproduce colors seen in real scenes: A major advantage of spectral rendering in production rendering is that it becomes easier to combine rendered and real footage, e.g. for virtual makeup. And it nicely decouples aspects of the camera such as its spectral sensitivity curves or color space from all aspects of light transport.

In real-time rendering, many of the effects mentioned above would typically be faked using per-scene color grading.
That works reasonably well if the lighting is dominated by a single type of light sources, but when there is a mixture of different light sources, this approach quickly hits a wall.
Spectral rendering handles these situations accurately (although [importance sampling](http://momentsingraphics.de/SpectralRendering2Rendering.html#Handling_multiple_illuminants) may be a challenge).

With this blog post series, I am hoping to combat some misconceptions about RGB and spectral rendering, but I have only scratched the surface.
The SIGGRAPH 2021 course on the subject [[Weidlich21]](http://momentsingraphics.de#_Weidlich21) is recommended further reading and makes similar points.
There are many benefits of spectral rendering that I have not mentioned: [Metamerism](https://w.wiki/FjtY) can be handled and modeling effects such as [fluorescence](https://en.wikipedia.org/wiki/Fluorescence) or [dispersion](https://w.wiki/Fjta) becomes more natural.
My main point here is that spectral rendering is more principled, enables accurate color reproduction and is affordable right now, even in real-time rendering.

The current reality is that even offline rendering is usually based on RGB.
The most notable exception is the work of [Wētā FX](https://en.wikipedia.org/wiki/W%C4%93t%C4%81_FX).
They have been using spectral rendering throughout their pipeline for years and ever since Avatar: The Way of Water, they have relied on [my method](http://momentsingraphics.de/Siggraph2019.html) for spectral upsampling of reflectance.
They also indicated that they would probably use this technique for all spectra if they were to start from scratch now [[Weidlich21]](http://momentsingraphics.de#_Weidlich21).
So while this blog post series has only covered one of many approaches, it is one that has proven itself in production rendering.
And I have demonstrated that [its overhead](http://momentsingraphics.de/SpectralRendering2Rendering.html#Timings) is low enough, even for real-time rendering.

## Downloads and links

## References

[ Weidlich, Andrea and Forsythe, Alex and Dyer, Scott and Mansencal, Thomas and Hanika, Johannes and Wilkie, Alexander and Emrose, Luke and Langlands, Anders (2021). Spectral imaging in production. In ACM SIGGRAPH 2021 Courses.
][Official version](https://doi.org/10.1145/3450508.3464582) | [Author's version](https://jo.dreggn.org/home/2021_spectral_imaging.pdf)