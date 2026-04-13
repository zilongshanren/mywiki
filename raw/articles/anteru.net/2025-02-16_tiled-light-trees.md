---
title: Tiled light trees
url: https://anteru.net/research/tiled-light-trees
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Yuriy O’Donnell1, Matthäus G. Chajdas2

*Accepted to* [ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games 2017](http://i3dsymposium.github.io/2017/)

## Abstract

Handling many light sources in real-time is still one of the big challenges in real-time graphics. Even the most recent approaches like practical clustered shading still have various problem cases with low performance. Especially in scenes with high depth variance, existing algorithms cannot adapt to the distribution of light sources properly and end up evaluating many lights that don’t contribute to the final image.

We present a new approach, “tiled light trees” - a hierarchical acceleration structure that adapts to the light source distribution. Our approach improves on the worst case performance of existing solutions. Due to traversal overhead, the proposed algorithm can be sometimes slower than clustered shading. To handle those situations optimally, we propose a hybrid approach which combines the strengths of light trees with clustered shading, outperforming any individual solution in nearly every case. Our new hybrid algorithm is easy to implement and suitable for usage in real-time applications such as games.

## Download

[Preprint (PDF, 3.2 MiB)](https://anteru.net/files/2017/TiledLightTrees-preprint.pdf)[Presentation (PPTX, 20.6 MiB)](http://frostbite-wp-prd.s3.amazonaws.com/wp-content/uploads/2017/02/26015157/I3D-TiledLightTrees.pptx)[ACM digital library](http://dl.acm.org/citation.cfm?id=3023376)(includes BibTeX)[First author’s page](https://kayru.org/publications/)[Frostbite’s page](https://www.ea.com/frostbite/news/tiled-light-trees)

## BibTex

```
@inproceedings{
O'Donnell:2017:TLT:3023368.3023376,
author = {O'Donnell, Yuriy and Chajdas, Matth\"{a}us G.},
title = {Tiled Light Trees},
booktitle = {Proceedings of the 21st ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games},
series = {I3D '17},
year = {2017},
isbn = {978-1-4503-4886-7},
location = {San Francisco, California},
pages = {1:1--1:7},
articleno = {1},
numpages = {7},
url = {http://doi.acm.org/10.1145/3023368.3023376},
doi = {10.1145/3023368.3023376},
acmid = {3023376},
publisher = {ACM},
address = {New York, NY, USA},
keywords = {culling, lighting, real-time},
}
```