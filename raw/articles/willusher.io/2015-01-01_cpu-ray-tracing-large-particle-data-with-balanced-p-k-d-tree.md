---
title: CPU Ray Tracing Large Particle Data with Balanced P-k-d Trees
url: https://www.willusher.io/publications/pkd/
published: '2015-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# CPU Ray Tracing Large Particle Data with Balanced P-k-d Trees

#### Ingo Wald, Aaron Knoll, Gregory P. Johnson, Will Usher, Valerio Pasucci, and Michael E. Papka

In *IEEE Vis (conference)*, 2015.

![](https://cdn.willusher.io/img/1YNpRJ1.webp)

**Fig. 1:**

*Full-detail ray tracing of giga-particle data sets. From left to right: CosmicWeb early universe data set from a P3D simulation with 29 billion particles; a 100 million atom molecular dynamics Al^2O^3−SiC materials fracture simulation; and a 1.3 billion particle Uintah MPM detonation simulation. Using a quad-socket, 72-core 2.5GHz Intel Xeon E7-8890 v3 Processor with 3TB RAM and path-tracing with progressive refinement at 1 sample per pixel, these far and close images (above and below) are rendered at 1.6 (far) / 1.0 (close) FPS (left), 2.0 / 1.2 FPS (center), and 1.0 / 0.9 FPS (right), respectively, at 4K (3840×2160) resolution. All examples use our balanced P-k-d tree, an acceleration structure which requires little or no memory cost beyond the original data.,*

## Abstract

We present a novel approach to rendering large particle data sets from molecular dynamics, astrophysics and other sources. We employ a new data structure adapted from the original balanced k-d tree, which allows for representation of data with trivial or no overhead. In the OSPRay visualization framework, we have developed an efficient CPU algorithm for traversing, classifying and ray tracing these data. Our approach is able to render up to billions of particles on a typical workstation, purely on the CPU, without any approximations or level-of-detail techniques, and optionally with attribute-based color mapping, dynamic range query, and advanced lighting models such as ambient occlusion and path tracing.

`@inproceedings{Wald_PKD_2015, author={I. Wald and A. Knoll and G. P. Johnson and W. Usher and V. Pascucci and M. E. Papka}, booktitle={2015 IEEE Scientific Visualization Conference (SciVis)}, title={{CPU} ray tracing large particle data with balanced {P-k-d} trees}, year={2015}, doi={10.1109/SciVis.2015.7429492} }`