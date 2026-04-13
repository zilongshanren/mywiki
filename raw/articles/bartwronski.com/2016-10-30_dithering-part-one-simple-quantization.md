---
title: Dithering part one – simple quantization
url: https://bartwronski.com/2016/10/30/dithering-part-one-simple-quantization/
published: '2016-10-30'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Introduction

First part of this [mini-series](https://bartwronski.com/2016/10/30/dithering-in-games-mini-series/) will focus on more theoretical side of dithering -some history and applying it for 1D signals and to quantization. I will try to do some frequency analysis of errors of quantization and how dithering helps them. It is mostly theoretical, so if you are interested in more practical applications, be sure to check the index and other parts.

You can find Mathematica notebook to reproduce results [here ](https://raw.githubusercontent.com/bartwronski/BlogPostsExtraMaterial/master/DitheringPostSeries/1DQuantization.nb)and the pdf version [here](https://github.com/bartwronski/BlogPostsExtraMaterial/blob/master/DitheringPostSeries/1DQuantization.pdf).

## What is dithering?

Dithering can be defined as intentional / deliberate adding of some noise to signal to prevent large-scale / low resolution errors that come from quantization or undersampling.

If you have ever worked with either:

- Audio signals,
- 90s palletized image file formats.

You must have for sure encountered dithering options that by adding some noise and small-resolution artifacts “magically” improved quality of audio files or saved images.

However, I found on Wikipedia quite an amazing fact about when dithering was first defined and used:

…[O]ne of the earliest [applications] of dither came in World War II. Airplane bombers used mechanical computers to perform navigation and bomb trajectory calculations. Curiously, these computers (boxes filled with hundreds of gears and cogs) performed more accurately when flying on board the aircraft, and less well on ground. Engineers realized that the vibration from the aircraft reduced the error from sticky moving parts. Instead of moving in short jerks, they moved more continuously. Small vibrating motors were built into the computers, and their vibration was called dither from the Middle English verb “didderen,” meaning “to tremble.” Today, when you tap a mechanical meter to increase its accuracy, you are applying dither, and modern dictionaries define dither as a highly nervous, confused, or agitated state. In minute quantities, dither successfully makes a digitization system a little more analog in the good sense of the word.

— Ken Pohlmann,Principles of Digital Audio

## Dithering quantization of a constant signal

*DC offset*)

**0.3**, simple rounding without any dithering will be the most boring function ever – just

**zero**!

**0.3**and therefore average is also

**0.3**. This means that we introduced quite big bias to our signal and completely lost original signal information.

quantizedDitheredSignal =


Round[constantSignalValue + RandomReal[] – 0.5] & /@ Range[sampleCount];

![Constant_dither_noise.png](../../assets/3f104bcb6c742342.png)

![Constant_dither_noise_img.png](../../assets/a2191772000b2c1c.png)

**plot of the error**and average error.

![Constant_dither_error.png](../../assets/6cfa69700065d8ab.png)

Mean[ditheredSignalError]


0.013

![spectrum_quantization_noise_comparison.gif](../../assets/e3c28ff163255308.gif)

Red plot/spike = frequency spectrum of error when not using dithering (constant, no frequencies). Black – with white noise dithering.

**dithering distributes quantization error / bias among many frequencies**.

## Frequency sensitivity and low-pass filtering

- Increased maximal error.
- Almost zeroed average, mean error.
- Added constant white noise (full spectral coverage) to the error frequency spectrum, reducing the low-frequency error.

- Our vision has a limit of acuity. Lots of people are short-sighted and see blurred image of faraway objects without correction glasses.
- We perceive medium scale of detail much better than very high or very low frequencies (small details of very smooth gradients may be not noticed).
- Our hearing works in specific frequency range (20Hz -20kHz, but it gets worse with age) and we are most sensitive to middle ranges – 2kHz-5kHz.

Therefore, any error in frequencies closer to upper range of perceived frequency will be much less visible.

Furthermore, our media devices are getting better and better and provide lots of **oversampling**. In TVs and monitors we have “retina”-style and 4K displays (where it’s impossible to see single pixels), in audio we use at least 44kHz sampling file formats even for cheap speakers that often can’t reproduce more than 5-10kHz.

![Constant_dither_noise_lowpass.png](../../assets/78de6b12b53a7630.png)

Red – desired non-quantized signal. Green – quantized and dithered signal. Blue – low pass filter of that signal.

![Constant_dither_noise_golden_lowpass.png](../../assets/6831d278add89015.png)

![Constant_dither_noise_golden_spectrum.png](../../assets/086c202eddde01eb.png)

## Quantizing a sine wave

![sine_quantize.png](../../assets/4789f1c220c26298.png)

*odd harmonics*.

![sine_quantize_spectrum.png](../../assets/4b5ab5f19c26061d.png)

![sine_quantize_error.png](../../assets/b649ffa0046f090e.png)

![sine_quantize_error_spectrum.png](../../assets/e3b21cbeca2875dd.png)

![sine_quantize_lowpass.png](../../assets/13f3a64c6a60292c.png)

Low-pass filtered quantized sine

![sine_quantize_error_lowpass.png](../../assets/9f83130b21c1a2e2.png)

Low-pass filtered quantized sine error

![sine_quantize_dither.png](../../assets/e2e6eb2d415beabe.png)

![sine_quantize_dither_img.png](../../assets/57c0167d74c1704e.png)

![spectrum_quantization_noise_comparison_sine.gif](../../assets/44d74f42902257fa.gif)

![sine_quantize_dither_lowpass.png](../../assets/62305e88277a9f5e.png)

![sine_quantize_dither_lowpass_comparison.png](../../assets/1a9e62c8038fe211.png)

Red – original sine. Green – low pass filtered undithered signal. Blue – low pass filtered dithered signal.

Plotting both error functions confirms numerically that error is much smaller:

![sine_quantize_dither_lowpass_error.png](../../assets/5abbc9d2ea89be49.png)

Red – error of low-pass filtered non-dithered signal. Blue – error of low-pass filterer dithered signal.

Finally, let’s just quickly look at a signal with better dithering function containing primarily high frequencies:

![sine_quantize_dither_vs_golden_img.png](../../assets/c9699c5f46e7660c.png)

Upper image – white noise function. Lower image – a function containing more higher frequencies.

![sine_quantize_dither_golden_lowpass_comparison.png](../../assets/721bd3d96da89952.png)

Low-pass filtered version dithered with a better function – almost perfect results if we don’t count filter phase shift!

And finally – all 3 comparisons of error spectra:

![spectrum_quantization_noise_golden__comparison_sine.gif](../../assets/9fae59f537c7b1b7.gif)

Red – undithered quantized error spectrum. Black – white noise dithered quantized error spectrum. Blue – noise with higher frequencies ditherer error spectrum.

## Summary

- Dithering distributes quantization error / bias among many different frequencies that depend on the dithering function instead of having them focused in lower frequency area.
- Human perception of any signal (sound, vision) works best in very specific frequency ranges. Signals are often over-sampled for end of perception spectrum in which perception is almost marginal. For example common audio sampling rates allow reproducing signals that most adults will not be able to hear at all. This makes use of dithering and trying to shift error into this frequency range so attractive because of previous point.
- Different noise functions produce different spectra of error that can be used knowing which error spectrum is more desired.

In [the next part](https://bartwronski.com/2016/10/30/dithering-part-two-golden-ratio-sequence-blue-noise-and-highpass-and-remap/) we will have a look at various dithering functions – the one I used here (golden ratio sequence) and blue noise.

Pingback: Dithering part two – golden ratio sequence, blue noise and highpass-and-remap | Bart Wronski

Pingback: Dithering in games – mini series | Bart Wronski