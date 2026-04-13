---
title: Real-time Hybrid Hair Rendering
url: https://anteru.net/research/realtime-hybrid-hair-rendering
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Hair models rendered using our technique. The left half is directly rasterized, the right half of each mesh runs through our ray-marcher. Hair count is 136.320 hair strands for the head, and 961.280 for the bear, respectively.

Rendering hair is a challenging problem for real-time applications. Besides complex shading, the sheer amount of it poses a lot of problems, as a human scalp can have over 100,000 strands of hair, with animal fur often surpassing a million. For rendering,both strand-based and volume-based techniques have been used, but usually in isolation. In this work, we present a complete hair rendering solution based on a hybrid approach. The solution requires no pre-processing, making it a drop-in replacement,that combines the best of strand-based and volume-based rendering. Our approach uses this volume not only as a level-of-detail representation that is raymarched directly, but also to simulate global effects, like shadows and ambient occlusion in real-time.

@inproceedings{JCLR2019,booktitle={Eurographics Symposium on Rendering - DL-only and Industry Track},editor={Boubekeur, Tamy and Sen, Pradeep},title={{Real-Time Hybrid Hair Rendering}},author={Jansson, Erik Sven Vasconcelos and Chajdas, Matthäus G. and Lacroix, Jason and Ragnemalm, Ingemar},year={2019},publisher={The Eurographics Association},ISSN={1727-3463},ISBN={978-3-03868-095-6},DOI={10.2312/sr.20191215}}