---
title: Interactive rendering of Giga-Particle Fluid Simulations
url: https://anteru.net/research/interactive-rendering-of-giga-particle-fluid-simulations
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Florian Reichl1, Matthäus G. Chajdas1, Jens
Schneider2, Rüdiger Westermann1

1[Technische Universität München](https://www.cs.cit.tum.de/cg/),
2[King Abdullah University of Science and Technology](http://www.kaust.edu.sa/)

## Abstract

We describe the design of an interactive rendering system for particle-based fluid simulations comprising hundreds of millions of particles per time step. We present a novel binary voxel representation for particle positions in combination with random jitter to drastically reduce memory and bandwidth requirements. To avoid a time-consuming preprocess and restrict the workload to what is seen, the construction of this representation is embedded into front-to-back GPU ray-casting. For high speed rendering, we ray-cast spheres and extend on total-variation-based image de-noising models to smooth the fluid surface according to data specific boundary conditions. The regular voxel structure permits highly efficient ray-sphere intersection testing as well as classification of foam particles at runtime on the GPU. Foam particles are rendered volumetrically by reconstructing densities from the binary representation on-the-fly. The particular design of our system allows scrubbing through high-resolution animated fluids at interactive rates.

## Project page

The [project page](https://www.in.tum.de/cg/research/publications/2014/interactive-rendering-of-giga-particle-fluid-simulations/) contains additional information about this paper as well as an executable version.

## Download

## Bibtex

```
@article{Reichl2014Fluid,
author = {Reichl, Florian and Chajdas, Matthäus G. and Schneider, Jens and Westermann, Rüdiger},
title = {Interactive Rendering of Giga-Particle Fluid Simulations},
year = {2014},
journal = {Proceedings of High Performance Graphics 2014 (to appear)}
}
```