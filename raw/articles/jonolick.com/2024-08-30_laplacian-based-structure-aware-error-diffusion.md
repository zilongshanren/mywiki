---
title: Laplacian Based Structure-Aware Error Diffusion
url: https://www.jonolick.com/home/laplacian-based-structure-aware-error-diffusion
published: '2024-08-30'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
I've been looking at various error diffusion techniques for an internal use case and was first pointed to Structure-Aware Error Diffusion which worked pretty well, but was pretty slow. I then came across a different paper: Laplacian Based Structure-Aware Error Diffusion. This article is about that technique. Its from 2010 so not super recent, but its new to me so here we go.
First up, why error diffusion? You use it when you have binary colors or palettized colors and such. In the internal use case it was for a binary mask of sorts. I won't go super into detail on that as I don't know how much I'm supposed to reveal or not about it - so I opt for revealing nothing (sorry). Anyways, Halftoning, the process of converting grayscale images to binary (black and white) images, has long been crucial for printing and display applications. The challenge has always been to preserve as much of the original image detail and structure as possible using only black and white pixels. The technique described in this paper built upon the classic Floyd-Steinberg error diffusion algorithm but introduced key modifications to better preserve image structure:
At the time, the researchers tested their algorithm against then state-of-the-art halftoning methods and found it produced superior results, especially for preserving fine details and textures. Notably, it performed about 25% better on structural similarity metrics (MSSIM) for low-contrast image regions. Despite the more complex processing, the technique maintained similar computational efficiency to basic error diffusion. It ran orders of magnitude faster than some optimization-based halftoning algorithms of that era. Visual comparisons showed the algorithm's ability to faithfully reproduce subtle textures that were lost with other methods of the time. For example, in a test image of a snail, the technique clearly preserved the shell texture that was blurred out by other algorithms.
|
## Archives
## Categories |