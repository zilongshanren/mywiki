---
title: A Comparison of Rendering Techniques for 3D Line Sets with Transparency
url: https://www.willusher.io/publications/tvcg20_oit/
published: '2020-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# A Comparison of Rendering Techniques for 3D Line Sets with Transparency

#### Michael Kern, Christoph Neuhauser, Torben Maack, Mengjiao Han, Will Usher, and Rüdiger Westermann

In *IEEE Transactions on Visualization and Computer Graphics*, 2020.

![](https://cdn.willusher.io/img/Sceg1iM.webp)

**Fig. 1:**

*Strengths and weaknesses of transparent line rendering techniques. For each pair, the left image shows the ground truth (GT). Right images show (a) approximate blending using MLABDB, (b) opacity over-estimation of MBOIT, (c) reverse blending order of MLABDB, (d) blur effect of MBOIT. Speed-ups to GT rendering technique: (a) 7, (b) 2, (c) 3.5, (d) 4.5.*

## Abstract

This paper presents a comprehensive study of rendering techniques for 3D line sets with transparency. The rendering of transparent lines is widely used for visualizing trajectories of tracer particles in flow fields. Transparency is then used to fade out lines deemed unimportant, based on, for instance, geometric properties or attributes defined along with them. Accurate blending of transparent lines requires rendering the lines in back-to-front or front-to-back order, yet enforcing this order for space-filling 3D line sets with extremely high-depth complexity becomes challenging. In this paper, we study CPU and GPU rendering techniques for transparent 3D line sets. We compare accurate and approximate techniques using optimized implementations and several benchmark data sets. We discuss the effects of data size and transparency on quality, performance, and memory consumption. Based on our study, we propose two improvements to per-pixel fragment lists and multi-layer alpha blending. The first improves the rendering speed via an improved GPU sorting operation, and the second improves rendering quality via transparency-based bucketing.",

## Content

`@article{kern_comparison_20, journal = {IEEE Transactions on Visualization and Computer Graphics}, title = {{A Comparison of Rendering Techniques for 3D Line Sets with Transparency}}, author = {Kern, Michael and Neuhauser, Christoph and Maack, Torben and Han, Mengjiao and Usher, Will and Westermann, Rüdiger}, year = {2020}, DOI = {10.1109/TVCG.2020.2975795} }`