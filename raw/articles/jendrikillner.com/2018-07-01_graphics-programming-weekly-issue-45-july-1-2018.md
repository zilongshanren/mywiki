---
title: Graphics Programming weekly - Issue 45 — July 1, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-45/
author: Jendrik Illner
published: '2018-07-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

a technique that allows the generation of infinite output space from a small example texture (such a grass, snow) in a pixel shader only

for example tillable terrain textures

cheap to evaluate; 0.29ms for a fullscreen quad

the approach is to partition the output space into a triangle grid and to pick three random patches from the input texture to blend to create the output patch

this is made possible through the variance preserving blending operation, and this can also be used to improve triplanar mapping

a technique to improve importance sampling for spherical light sources by projecting the visible spherical cap onto a 2D plane, and taking uniform samples within this plane

yields noise-free direct illumination for constant illumination with no occluders

technique changes shading rate adaptively based on the local content of the image

partitions the framebuffer into subdivision levels; uses these to estimate the variance between neighboring pixels to decide if new shading information needs to be calculated or if the shading result can be estimated from neighboring pixels

a technique that adjusts the temporal accumulation factor dynamically per pixel and frame

done by calculating per-pixel temporal gradients. These are reconstructed from sparse information that captures the change of luminance between the last and current frame