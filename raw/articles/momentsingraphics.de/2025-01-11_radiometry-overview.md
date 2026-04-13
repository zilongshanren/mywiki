---
title: 'Radiometry: Overview'
url: http://momentsingraphics.de/RadiometryOverview.html
published: '2025-01-11'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Radiometry: Overview

Physically-based rendering requires physical quantities, specifically radiometric and photometric quantities. They are at the foundation of the rendering equation. Without a solid understanding, you cannot properly describe what you are trying to compute in your renderer, let alone compute it correctly and efficiently. In this short blog post series, I describe these concepts in ways that are a bit off the beaten path. Hopefully, that will help some of you to gain a better understanding. Note that the link to part 2 will be broken until that post becomes available:

[Part 1: I got it backwards](http://momentsingraphics.de/Radiometry1Backwards.html)- This post covers all basic radiometric quantities (radiance, irradiance, flux, energy and intensity). Unlike most explanations, it starts with radiance and works its way up to energy. In doing so, it avoids strange limit processes and instead works with nothing but integrals.
[Part 2: Spectra and photometry](http://momentsingraphics.de/Radiometry2Photometry.html)- Each photon has a wavelength but radiometric quantities are blind to that fact. In the literal sense, radiance accounts for infrared and ultraviolet light all the same as for visible light. This post first introduces spectral versions of radiometric quantities, which allow us to tell different wavelengths apart. Then it describes photometric quantities, which are tied to the perception of brightness in the human visual system. Finally, it covers a few basics of spectral rendering.