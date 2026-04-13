---
title: Spatiotemporal Variance-Guided Filtering for Motion Blur
url: https://anteru.net/research/spatiotemporal-variance-guided-filtering-for-motion-blur
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Adding motion blur to a scene can help to convey the feeling of speed even at low frame rates. Monte Carlo ray tracing can compute accurate motion blur, but requires a large number of samples per pixel to converge. In comparison, rasterization, in combination with a post-processing filter, can generate fast, but not accurate motion blur from a single sample per pixel.

We build upon a recent path tracing denoiser and propose its variant to simulate ray-traced motion blur, enabling fast and high-quality motion blur from a single sample per pixel. Our approach creates temporally coherent renderings by estimating the motion direction and variance locally, and using these estimates to guide wavelet filters at different scales.

We compare image quality against brute force Monte Carlo methods and current post-processing motion blur. Our approach achieves real-time frame rates, requiring less than 4ms for full-screen motion blur at a resolution of 1920 × 1080 on recent graphics cards.