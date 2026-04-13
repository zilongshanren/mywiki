---
title: Shader Toolbox for URP - Inverted-Hull Outlines
url: https://danielilett.com/shader-toolbox/hull-outlines/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Inverted-hull outlines can be used to render the mesh a second time, invert the normal direction of each triangle, and expand the mesh along vertex normal vectors. By coloring the mesh, you can achieve a cheap outline effect. However, the effect works best on rounded objects.

# Parameters

**Outline Color**- Base color to use for the entire outline.**Outline Thickness**- How far the vertices expand along vertex normals.