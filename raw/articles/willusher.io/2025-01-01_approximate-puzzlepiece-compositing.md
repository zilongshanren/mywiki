---
title: Approximate Puzzlepiece Compositing
url: https://www.willusher.io/publications/apc-pvis25/
published: '2025-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# Approximate Puzzlepiece Compositing

#### Xuan Huang, Will Usher, Valerio Pascucci

In *IEEE Transactions on Visualization and Computer Graphics*, 2025.

![](https://cdn.willusher.io/img/apc-pvis25-teaser.jpg)

**Fig. 1:**

*Large-scale moment-based order-independent (MBOIT) distributed transparency rendering with the FUN3D Mars Lander A/143M dataset, consisting of 72 subdomains and 798M elements. Figures (a) and (b) are rendered at 2560×2560 using TACC Frontera Intel Xeon Platinum 8280 (“Cascade Lake”) nodes with 192GB memory. (c) A heatmap of the per-pixel segment counts with a range of [0, 28]. The segment lists must be individually sorted and blended in sort-last compositing due to the overlapping boundaries of data on the ranks, resulting in large data transfers and bottlenecks. Our approach ensures a constant, fixed, and small amount of communication for compositing arbitrary data distributions.*

## Abstract

The increasing demand for larger and higher fidelity simulations has made Adaptive Mesh Refinement (AMR) and unstructured mesh techniques essential to focus compute effort and memory cost on just the areas of interest in the simulation domain. The distribution of these meshes over the compute nodes is often determined by balancing compute, memory, and network costs, leading to distributions with jagged nonconvex boundaries that fit together much like puzzle pieces. It is expensive, and sometimes impossible, to re-partition the data posing a challenge for in situ and post hoc visualization as the data cannot be rendered using standard sort-last compositing techniques that require a convex and disjoint data partitioning. We present a new distributed volume rendering and compositing algorithm, Approximate Puzzlepiece Compositing, that enables fast and high-accuracy in-place rendering of AMR and unstructured meshes. Our approach builds on Moment-Based Ordered-Independent Transparency to achieve a scalable, order-independent compositing algorithm that requires little communication and does not impose requirements on the data partitioning. We evaluate the image quality and scalability of our approach on synthetic data and two large-scale unstructured meshes on HPC systems by comparing to state-of-the-art sort-last compositing techniques, highlighting our approach’s minimal overhead at higher core counts. We demonstrate that Approximate Puzzlepiece Compositing provides a scalable, high-performance, and high-quality distributed rendering approach applicable to the complex data distributions encountered in large-scale CFD simulations.