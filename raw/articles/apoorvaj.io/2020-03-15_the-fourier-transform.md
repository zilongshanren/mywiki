---
title: The Fourier transform
url: https://apoorvaj.io/aliasing-in-computer-graphics
published: '2020-03-15'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

Most people who have come in contact with computer graphics know that aliasing commonly refers to jagged edges that occur when rendering triangles. In this article, we look at other manifestations of aliasing in 3D graphics, and attempt to theoretically unify them. We won’t properly look at how to solve aliasing, only focusing on reasoning about the problem instead.

The diagrams and animations in this article were made using Python.
I’ve made the code freely available [here](https://github.com/ApoorvaJ/public-notebooks/blob/master/aliasing_in_graphics.ipynb),
in the public domain.

I won’t describe the Fourier transform in this post in detail. There
are other excellent sources for understanding it, both from an intuitive
perspective, [ But what is the
Fourier Transform? A visual introduction.](https://www.youtube.com/watch?v=spUNpyF58BY) by Grant Sanderson.
and a more formal one.

In short, the Fourier transform converts from a time domain representation of a signal to a frequency domain representation of it. You can apply the Inverse Fourier transform to go in the opposite direction.

\text{Time domain} \xrightleftharpoons[\text{Inverse Fourier transform}]{\text{Fourier transform}} \text{Frequency domain}

*Sampling* is the process of obtaining a discrete-time signal
by noting the value of a continuous-time signal at (usually) equally
spaced instants in time. Sampling converts the *independent
variable* (i.e. the horizontal axis—in this case, time) from
continuous to discrete.

The sampled value is a real number. When you want to represent this
value digitally, you have a finite number of bits to work with.
*Quantizing* is the process of converting the real sampled value
to a valid float or integer. Quantization converts the *dependent
variable* (i.e. the vertical axis) from continuous to discrete.

It is important to note that image banding arises from quantization, while aliasing arises from sampling.

Before we look at aliasing, let’s look at *proper sampling*
and reconstruction.

We take a continuous signal—a Gaussian pulse (a). Frequency domain amplitude plots (b and c) reveal that we see a peak between 0.0 and 0.02 Hz. (All of the examples in this article use real-valued time domain signals, so the frequency domain plots are symmetric around x = 0).

We sample the function at some high-enough
frequency, More
on this frequency shortly. and we get a finite set of discrete
values. We pretend that these values form a continuous signal—with
values at the discrete points, and zero everywhere else. This signal is
called an impulse train (d). The frequency plots (e and f) show that the
impulse train has the same pattern as the original signal (b and c), but
repeated.

If we chop off all frequencies higher than 0.02 in the impulse train’s frequency domain (e and f), we end up with a frequency plot (i) identical to that of the original signal. Now if we apply the inverse Fourier transform, we get the original signal (g) back. This process is called reconstruction.

If this were an actual system, we might digitize the finite set of sampled values, and use it for transmission, storage, or any other digital application. We would reconstruct the signal on the receiving end or while playing back the stored signal. In reality, we might convolve a low-pass filter in the time domain to perform the reconstruction, instead of chopping off the frequency domain.

Observe how the original frequency plot (b) was repeated in the
impulse train frequency plot (e). As you *increase* the sampling
frequency, the impulse train obviously gets denser, but the repeated
sections in the frequency domain move *farther away* from each
other. Conversely, as you *decrease* the sampling frequency, the
repeated sections move *closer* together, until they start
additively overlapping with each other. This frequency where this
overlapping starts occurring is called the *Nyquist rate*.

In the original frequency plot (c), we have non-zero values in the
range [0.0, 0.02], denoted by the two ▲s. This range is called the
*bandwidth* of the original signal (Remember that we only look at
the positive frequencies [0.0, 0.5], because of the aforementioned
symmetry in the negative frequencies.)

The Nyquist rate is two times the bandwidth. This means that to properly sample our signal, we need to do so at 0.02 \times 2 = 0.04 Hz or above.

Let’s see what happens if we sample below this frequency. Figures (j) through (o) show a similar process as above, but with a lower sampling rate.

![Improper sampling](../../assets/9355c63694f8525d.png)

![Improper sampling](../../assets/3c3b26201bc24ccb.png)


Notice how we do not get a clean, repeated frequency plot in (l). As a result, the low-pass-filtered frequency plot (o) is not clean, and the reconstructed signal (m) is not the same as the original signal (a).

This is called *aliasing*, because higher frequencies in the
original signal masquerade as lower frequencies in the reconstructed
signal.

A surprising fact that arises out of sampling and reconstruction, is
that if a continuous-time signal is properly sampled, then the resulting
*finite set of samples* contains the same amount of information
as the *infinite samples* present in the original signal!

So far, we’ve looked at aliasing in the way that it is canonically described in digital signal processing theory. Now let’s frame this phenomenon in terms of graphics.

A crucial difference between (for instance) audio processing and
graphics is that, in audio systems, we reconstruct the discrete-time
signal to produce a continuous-time signal, which then is the final
output (e.g. vibrations produced by a speaker diaphragm). But *in
graphics, our final output is discrete*—i.e. pixel values.

Despite this, if we sample below the Nyquist rate, aliasing still
occurs. In other words, *aliasing occurs during sampling, not during
reconstruction*.

Now we’ll look at three different ways aliasing manifests in practice:

This is the most widely known manifestation of aliasing—jagged edges along triangle meshes. To understand why this occurs, let’s look at a 1D slice of a white triangle on a black background. Where there is no triangle, the underlying continuous function has a value of zero. When the triangle starts, the value instantly jumps to one. This means that the underlying continuous function is a step function.

When you rasterize this triangle slice onto the screen, you’re basically sampling this underlying function at pixel centers. The sampling period (inversely related to sampling frequency) is the distance between the pixel centers.

Since the underlying function is a step, its bandwidth is infinite (because of the instantaneous change). This means that no finite amount of resolution is enough to completely avoid aliasing.

The left plot represents the underlying step function, and the strip on the bottom shows how it would appear when sampled along 16 pixel centers. As we move our “triangle”, notice how the pixels jump, even though the underlying function moves smoothly. This is exactly what leads to jagged edges in 2D.

The right plot shows a low-pass-filtered version of the step function, with a cut-off frequency half that of the (pixel) sampling frequency. The pixel strip here shows smooth motion using greyscale values.

An important thing to note is that *this anti-alias filter is not
a blur*. A blur would’ve occurred after the sampling, while this is
applied before.

In practice, rasterizers do not apply analytical filters to underlying functions. Instead, practical anti-aliasing techniques supersample the neighborhood around the pixel center, and then perform a weighted sum. This weighted sum can be seen as just a cheap low-pass filter. E.g. if you just average the values of neighborhood pixels, you’re convolving a box filter. If you do a distance-weighted average, you’re convolving something akin to a Gaussian filter. When choosing filters for the supersampled image, you’re trying to balance performance and frequency cutoff.

Even while supersampling, aliasing technically still occurs, but you get more usable bandwidth, and thus less noticeable jagged edges.

Sub-pixel triangles shimmering in and out of existence is also another manifestation of the same problem.

Finally, there is an alternate way to view rasterization—a pixel can
be seen as being a little square, contrary to some paper
titles. [ A pixel is
not a little square [PDF]](http://alvyray.com/Memos/CG/Microsoft/6_pixel.pdf) by Alvy Ray Smith. In this
view, you want to integrate the underlying function over the area of the
pixel, to compute the

The Nyquist rate can be seen as a measure of information contained in
a signal. If a signal has bandwidth \frac{f}{2}, then it must be sampled at a
frequency greater than f to preserve
the information content. Conversely, if a discrete signal has been
sampled at frequency f, then it
*must* have an information bandwidth less than \frac{f}{2}.

![]() |
![]() |
Source
|

Say the first original image is sampled at frequency f_o. Then it is minified, lowering the sampling frequency to f_m. If the original image contains frequencies in the band [\frac{f_m}{2}, \frac{f_o}{2}], then they will alias. You can see that happening on the second image, in the form of Moiré patterns.

![](../../assets/291f92e1160ccfcc.png)


This occurs in graphics at any point when the sampling frequency drops lower than the original frequency, such as:

**When a texture is minified because it is viewed from
farther away.** *Mipmapping* aims to fix this problem by
low-pass pre-filtering textures and storing copies in lower resolutions.
When viewing a minified texture, the GPU picks the closest bigger
mipmap, and thus minimizes the aliased bandwidth.

**When a texture is perspective-skewed.** This
occurs most often on ground textures, and is closely related to the
previous point. Here, the parts of the texture closer to the camera are
sampled frequently, while those in the distance are sampled
infrequently. GPUs fix this using *anisotropic filtering*,
i.e. using different mipmaps for the same geometry, depending on the
local sampling frequency.

**When a texture is rotated.** As you rotate a
texture, sampling gets sparser, being the most sparse at 45° rotations.
This will result in aliasing too, albeit in a narrower frequency
band.

This is closely related to texture aliasing, but can be more complex to fix. Each pixel is shaded according to some underlying function. This function is complicated, and takes in parameters such as the pixel position, geometric normal, textured normal, diffuse color, roughness, light positions, etc., and produces a color as an output. If the Nyquist rate of the output of this function is greater than our pixel frequency, then aliasing will occur.

This is the most generalized way to look at aliasing in graphics, and
the two above variants can also fit into this category. I mention it
separately because problems such as [specular aliasing](https://www.youtube.com/watch?v=Mm1efTnXtRY)
can only be described at this level of abstraction.

Any band-limited continuous signal has a frequency called the Nyquist rate. To avoid aliasing, you can sample above that rate. Alternatively, you can remove frequencies in the signal that are higher than your sampling budget.

In conclusion, I hope this article gave you a better idea about the underpinnings of aliasing and how to reason about it. A lot of areas in graphics touch upon this subject, so it’s very useful to understand.

I encourage you to play around with the Python code, which is freely
available [here](https://github.com/ApoorvaJ/public-notebooks/blob/master/aliasing_in_graphics.ipynb),
in the public domain.