---
title: High-Quality Shadows for Streaming Terrain Rendering
url: https://anteru.net/research/high-quality-shadows-for-streaming-terrain-rendering
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Matthäus G. Chajdas1, Florian Reichl1, Christian
Dick1, Rüdiger Westermann1

## Abstract

Rendering of large, detailed 3D terrains on commodity hardware has become possible through the use of ray-casting, data caching and prefetching. Adding dynamic shadows as they appear during a day-night cycle remains a challenge however, because shadow rendering requires access to the entire terrain, invalidating data streaming strategies. In this work we present a novel, practicable shadow rendering approach which distinguishes between near- and precomputed far-shadows to significantly reduce data access and runtime costs. While near-shadows are ray-traced using the current cache content, far-shadows are precomputed and stored in a very compact format requiring approximately 3 bit per height-map sample for an entire day-night cycle.

## Download

## Bibtex

```
@InProceedings{Chajdas:2015:TerrainShadows,
author = {Matth{\"{a}}us G. Chajdas and Florian Reichl and Christian Dick and R{\"{u}}diger Westermann},
title = {High-Quality Shadows for Streaming Terrain Rendering},
booktitle = {Proceedings of Eurographics 2015 - Short Papers},
pages = {57--60},
year = {2015},
}
```