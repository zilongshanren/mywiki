---
title: 'Ray Tracing Generalized Tube Primitives: Method and Applications'
url: https://www.willusher.io/publications/tubes/
published: '2019-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# Ray Tracing Generalized Tube Primitives: Method and Applications

#### Mengjiao Han, Ingo Wald, Will Usher, Qi Wu, Feng Wang, Valerio Pascucci, Charles D. Hansen, and Chris R. Johnson

In *Computer Graphics Forum (Proceedings of EuroVis)*, 2019.

![](https://cdn.willusher.io/img/tTv2l2j.webp)

**Fig. 1:**

*Visualizations using our “generalized tube” primitives. (a): DTI tractography data, semi-transparent fixed-radius streamlines (218K line segments). (b): A generated neuron assembly test case, streamlines with varying radii and bifurcations (3.2M l. s.). (c): Aneurysm morphology, semi-transparent streamlines with varying radii and bifurcations (3.9K l. s.) and an opaque center line with fixed radius and bifurcations (3.9K l. s.). (d): A tornado simulation, with radius used to encode the velocity magnitude (3.56M l. s.). (e): Flow past a torus, fixed-radius pathlines (6.5M l. s.). Rendered at: (a) 0.38FPS, (b) 7.2FPS, (c) 0.25FPS, (d) 18.8FPS, with a 2048x2048 framebuffer; (e) 23FPS with a 2048x786 framebuffer. Performance measured on a dual Intel Xeon E5-2640 v4 workstation, with shadows and ambient occlusion.*

## Abstract

We present a general high-performance technique for ray tracing generalized tube primitives. Our technique efficiently supports tube primitives with fixed and varying radii, general acyclic graph structures with bifurcations, and correct transparency with interior surface removal. Such tube primitives are widely used in scientific visualization to represent diffusion tensor imaging tractographies, neuron morphologies, and scalar or vector fields of 3D flow. We implement our approach within the OSPRay ray tracing framework, and evaluate it on a range of interactive visualization use cases of fixed- and varying-radius streamlines, pathlines, complex neuron morphologies, and brain tractographies. Our proposed approach provides interactive, high-quality rendering, with low memory overhead.

`@article{han_ray_2019, journal = {Computer Graphics Forum}, title = {{Ray Tracing Generalized Tube Primitives: Method and Applications}}, author = {Han, Mengjiao and Wald, Ingo and Usher, Will and Wu, Qi and Wang, Feng and Pascucci, Valerio and Hansen, Charles D. and Johnson, Chris R.}, year = {2019}, publisher = {The Eurographics Association and John Wiley & Sons Ltd.}, ISSN = {1467-8659}, DOI = {10.1111/cgf.13703} }`