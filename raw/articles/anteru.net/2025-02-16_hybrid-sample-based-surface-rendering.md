---
title: Hybrid Sample-based Surface Rendering
url: https://anteru.net/research/hybrid-sample-based-surface-rendering
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Florian Reichl1, Matthäus G. Chajdas1, Kai
Bürger1, Rüdiger Westermann1

## Abstract

The performance of rasterization-based rendering on current GPUs strongly depends on the abilities to avoid overdraw and to prevent rendering triangles smaller than the pixel size. Otherwise, the rates at which high- resolution polygon models can be displayed are affected significantly. Instead of trying to build these abilities into the rasterization-based rendering pipeline, we propose an alternative rendering pipeline implementation that uses rasterization and ray-casting in every frame simultaneously to determine eye-ray intersections. To make ray-casting competitive with rasterization, we introduce a memory-efficient sample-based data structure which gives rise to an efficient ray traversal procedure. In combination with a regular model subdivision, the most optimal rendering technique can be selected at run-time for each part. For very large triangle meshes our method can outperform pure rasterization and requires a considerably smaller memory budget on the GPU. Since the proposed data structure can be constructed from any renderable surface representation, it can also be used to efficiently render isosurfaces in scalar volume fields. The compactness of the data structure allows rendering from GPU memory when alternative techniques already require exhaustive paging

## Project page

The [project page](https://www.in.tum.de/cg/research/publications/2012/hybrid-sample-based-surface-rendering/) contains additional information about this paper as well as an executable version.

## Download

## Bibtex

```
@inproceedings{VMV12:47-54:2012,
booktitle = {VMV 2012: Vision, Modeling \& Visualization},
year = {2012},
isbn = {978-3-905673-95-1},
issn = {-},
address = {Magdeburg, Germany},
publisher = {Eurographics Association},
author = {Florian Reichl and Matth\"{a}us G. Chajdas and Kai B\"{u}rger and R\"{u}diger Westermann },
title = {{Hybrid Sample-based Surface Rendering}},
pages = {47-54},
URL = {http://diglib.eg.org/EG/DL/PE/VMV/VMV12/047-054.pdf},
DOI = {10.2312/PE/VMV/VMV12/047-054},
year = {2012},
}
```