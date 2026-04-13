---
title: 'libIS: A Lightweight Library for Flexible In Transit Visualization'
url: https://www.willusher.io/publications/libis-isav18/
published: '2018-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# libIS: A Lightweight Library for Flexible In Transit Visualization

#### Will Usher, Silvio Rizzi, Ingo Wald, Jefferson Amstutz, Joseph Insley, Venkatram Vishwanath, Nicola Ferrier, Michael E. Papka, and Valerio Pascucci

In *ISAV: In Situ Infrastructures for Enabling Extreme-Scale Analysis and Visualization (ISAV '18)
*, 2018.

![](https://cdn.willusher.io/img/UYlTqhT.webp)

**Fig. 1:**

*Interactive in situ visualization of a 172k atom simulation of silicene formation with 128 LAMMPS ranks sending to 16 OSPRay renderer ranks, all executed on Theta in the mpi-multi configuration. When taking four ambient occlusion samples per-pixel, our viewer averages 7FPS at 1024x1024. Simulation dataset is courtesy of*

[Cherukara et al.](https://pubs.rsc.org/en/content/articlelanding/2017/nr/c7nr03153j).## Abstract

As simulations grow in scale, the need for in situ analysis methods to handle the large data produced grows correspondingly. One desirable approach to in situ visualization is in transit visualization. By decoupling the simulation and visualization code, in transit approaches alleviate common difficulties with regard to the scalability of the analysis, ease of integration, usability, and impact on the simulation. We present libIS, a lightweight, flexible library which lowers the bar for using in transit visualization. Our library works on the concept of abstract regions of space containing data, which are transferred from the simulation to the visualization clients upon request, using a client-server model. We also provide a SENSEI analysis adaptor, which allows for transparent deployment of in transit visualization. We demonstrate the flexibility of our approach on batch analysis and interactive visualization use cases on different HPC resources.

## Content

`@inproceedings{usher_libis_2018, title = {{libIS}: {A} {Lightweight} {Library} for {Flexible} {In} {Transit} {Visualization}}, year = {2018}, booktitle = {ISAV: In Situ Infrastructures for Enabling Extreme-Scale Analysis and Visualization}, series = {ISAV'18}, author = {Usher, Will and Rizzi, Silvio and Wald, Ingo and Amstutz, Jefferson and Insley, Joseph and Vishwanath, Venkatram and Ferrier, Nicola and Papka, Michael E. and Pascucci, Valerio}, doi={10.1145/3281464.3281466} }`