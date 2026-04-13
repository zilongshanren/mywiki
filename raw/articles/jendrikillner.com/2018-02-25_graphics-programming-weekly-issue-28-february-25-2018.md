---
title: Graphics Programming weekly - Issue 28 — February 25, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-28/
author: Jendrik Illner
published: '2018-02-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- in-depth breakdown of how the Wolfenstein 3D renderer works
- explanation of the ray-casting logic
- derivation of the mathematics found in the code

[Fast way to render lots of spheres](https://gist.github.com/sebbbi/a599d7896aa3ad36642145d54459f32b) [[wayback-archive]](https://web.archive.org/web/20180225230423/https://gist.github.com/sebbbi/a599d7896aa3ad36642145d54459f32b)

- spheres drawn in pixel shader using ray-sphere intersection test
- vertex shader generates screen space bounding boxes from sphere center + radius
- allows debug spheres to be generated from other GPU kernels

[Twitter - Ptex memory access pattern](https://twitter.com/maxliani/status/966354624595640321?s=09) [[wayback-archive]](https://web.archive.org/web/20180225230440/https://twitter.com/maxliani/status/966354624595640321?s=09)

- problems with Ptex in relation to access patterns and filtering

[Voxel lighting](https://0fps.net/2018/02/21/voxel-lighting/) [[wayback-archive]](https://web.archive.org/web/20180225230458/https://0fps.net/2018/02/21/voxel-lighting/)

- flood fill lighting
- store light information for 5 directions and store propagation information for each
- how to use word level parallelism to speed up propagation

- how to investigate constant buffer data
- look at vertex shader input / output
- detect invalid camera position from vertex output

[New Vulkan Assistant Layer Highlights Development Best Practices](https://www.lunarg.com/vulkan-assistant-layer-highlights-best-practices/) [[wayback-archive]](https://web.archive.org/web/20180225230633/https://www.lunarg.com/vulkan-assistant-layer-highlights-best-practices/)

- intended to highlight potential performance issues, questionable usage patterns, common mistakes

[Reverse engineering the rendering of The Witcher 3, part 4 - vignette](http://astralcode.blogspot.ca/2018/02/reverse-engineering-rendering-of.html) [[wayback-archive]](https://web.archive.org/web/20180225230703/http://astralcode.blogspot.ca/2018/02/reverse-engineering-rendering-of.html)

- description of controls
- additional mask texture allows variation across the screen
- reverse engineered HLSL code

- on Tuesday, March 20th there will be a substance day at GDC
- open for expo pass and above

- list of AMD sessions at GDC