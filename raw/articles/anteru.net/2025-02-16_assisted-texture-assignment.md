---
title: Assisted texture assignment
url: https://anteru.net/research/assisted-texture-assignment
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Assisted texture assignment learns which textures to apply to which surface, and automatically completes the assignment. (Scene courtesy of id Software from Quake 4)

Virtual environments are typically textured by manually choosing an image to apply on each surface. This implies browsing through large sets of generic textures for each and every surface in the scene. We propose to facilitate this long and tedious process. Our algorithm assists the user while he assigns textures to surfaces. Each time an image is chosen for a surface, our algorithm propagates this information throughout the entire environment. Our approach is based on a new surface similarity measure. We exploit this measure in an algorithm ranking all possible textures for a given surface. Hence, we do not simply assign a texture to the surface but also propose an ordered list of choices for the user. In the unavoidable event of an ambiguous choice, the user can quickly make a decision and select the best texture. Our algorithm is fast enough to allow for interactive feedback. Applications range from assisted interactive texturing to fully automatic initial texturing solutions.

@InProceedings{CLS10,author="Chajdas, Matth{\"a}us G. and Lefebvre, Sylvain and Stamminger, Marc",title="Assisted Texture Assignment",booktitle="Proceedings of the ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games",year="2010",publisher="ACM Press",url="http://www-sop.inria.fr/reves/Basilic/2010/CLS10"}