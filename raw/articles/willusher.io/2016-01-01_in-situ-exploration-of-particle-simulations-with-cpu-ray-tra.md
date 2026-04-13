---
title: In Situ Exploration of Particle Simulations with CPU Ray Tracing
url: https://www.willusher.io/publications/isp-jsfi/
published: '2016-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# In Situ Exploration of Particle Simulations with CPU Ray Tracing

#### Will Usher, Ingo Wald, Aaron Knoll, Michael E. Papka, and Valerio Pascucci

In *Supercomputing Frontiers and Innovations*, 2016.

![](https://cdn.willusher.io/img/DO3JqOb.webp)

**Fig. 1:**

*A coal particle combustion simulation in Uintah at three different timesteps with (left to right): 34.61M, 48.46M and 55.39M particles, with attribute based culling showing the full jet (top) and the front in detail (bottom). Using our in situ library to query and send data to our rendering client in OSPRay these images are rendered interactively with ambient occlusion, averaging around 13 FPS at 1920×1080. The renderer is run on 12 nodes of the Stampede supercomputer and pulls data from a Uintah simulation running on 64 processes (4 nodes). Our loosely-coupled in situ approach allows for live exploration at the full temporal fidelity of the simulation, without prohibitive IO cost.*

## Abstract

We present a system for interactive in situ visualization of large particle simulations, suitable for general CPU-based HPC architectures. As simulations grow in scale, in situ methods are needed to alleviate IO bottlenecks and visualize data at full spatio-temporal resolution. We use a lightweight loosely-coupled layer serving distributed data from the simulation to a data-parallel renderer running in separate processes. Leveraging the OSPRay ray tracing framework for visualization and balanced P-k-d trees, we can render simulation data in real-time, as they arrive, with negligible memory overhead. This flexible solution allows users to perform exploratory in situ visualization on the same computational resources as the simulation code, on dedicated visualization clusters or remote workstations, via a standalone rendering client that can be connected or disconnected as needed. We evaluate this system on simulations with up to 227M particles in the LAMMPS and Uintah computational frameworks, and show that our approach provides many of the advantages of tightly-coupled systems, with the flexibility to render on a wide variety of remote and co-processing resources.

`@article{Usher_InSituParticles_2016, author={Will Usher and Ingo Wald and Aaron Knoll and Michael E. Papka and Valerio Pascucci}, title={In {Situ} {Exploration} of {Particle} {Simulations} with {CPU} {Ray} {Tracing}}, journal={{Supercomputing} {Frontiers} and {Innovations}}, volume={3}, number={4}, year={2016}, issn={2313-8734}, doi={10.14529/jsfi160401} }`