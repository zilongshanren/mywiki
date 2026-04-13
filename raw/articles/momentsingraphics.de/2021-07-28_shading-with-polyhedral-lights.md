---
title: Shading with polyhedral lights
url: http://momentsingraphics.de/PolyhedralLights.html
published: '2021-07-28'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Shading with polyhedral lights

In the past winter term at [Karlsruhe Institute of Technology](https://cg.ivd.kit.edu/), I had the pleasure of supervising Bastian Urbach's bachelor thesis. His topic has been the generalization of methods for shading with polygonal lights to polyhedral lights. He has been highly motivated and creative. The result is an efficient method for GPU-accelerated real-time shading with convex or non-convex polyhedral lights (see [Figure 1](http://momentsingraphics.de#Neon)). Shading itself works either through linearly transformed cosines [[Heitz2016]](http://momentsingraphics.de#_Heitz2016) or through Monte Carlo integration. And it's implemented in [Unity](https://unity.com/). Both the [bachelor thesis and the implementation](https://bastian.urbach.one/rtswplusd/) are now freely available on Bastian's blog. If that sounds interesting, go ahead and read his short blog post or the whole thesis. It's much like a concurrent work published recently at EGSR [[Aakash2021]](http://momentsingraphics.de#_Aakash2021) but there are pros and cons for both techniques. The blog post discusses those as well.

![Neon](../../assets/abd3ef8ce835494b.webp)

**Figure 1:**A plane lit by several non-convex polyhedral lights.

## Link

## References

[ Kt, Aakash and Sakurikar, Parikshit and Narayanan, P. J. (2021). Fast Analytic Soft Shadows from Area Lights. Eurographics Symposium on Rendering - DL-only Track. ][Official version](https://doi.org/10.2312/sr.20211295) | [Author's version](https://aakashkt.github.io/)

[ Heitz, Eric and Dupuy, Jonathan and Hill, Stephen and Neubelt, David (2016). Real-time Polygonal-light Shading with Linearly Transformed Cosines. ACM Transactions on Graphics (proc. SIGGRAPH), 35(4). ][Official version](https://doi.org/10.1145/2897824.2925895) | [Author's version](https://eheitzresearch.wordpress.com/415-2/)