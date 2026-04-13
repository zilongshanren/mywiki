---
title: BRDF Importance Sampling for Polygonal Lights
url: http://momentsingraphics.de/Siggraph2021.html
published: '2021-06-11'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# BRDF Importance Sampling for Polygonal Lights

Christoph Peters.

2021–07 in *ACM Transactions on Graphics (Proc. SIGGRAPH)* 40, 4.

[Official version](https://doi.org/10.1145/3450626.3459672)

## Abstract

With the advent of real-time ray tracing, there is an increasing interest in GPU-friendly importance sampling techniques. We present such methods to sample convex polygonal lights approximately proportional to diffuse and specular BRDFs times the cosine term. For diffuse surfaces, we sample the polygons proportional to projected solid angle. Our algorithm partitions the polygon suitably and employs inverse function sampling for each part. Inversion of the distribution function is challenging. Using algebraic geometry, we develop a special iterative procedure and an initialization scheme. Together, they achieve high accuracy in all possible situations with only two iterations. Our implementation is numerically stable and fast. For specular BRDFs, this method enables us to sample the polygon proportional to a linearly transformed cosine. We combine these diffuse and specular sampling strategies through novel variants of optimal multiple importance sampling. Our techniques render direct lighting from Lambertian polygonal lights with almost no variance outside of penumbrae and support shadows and textured emission. Additionally, we propose an algorithm for solid angle sampling of polygons. It is faster and more stable than existing methods.

**Keywords:** projected solid angle sampling, solid angle sampling, light sampling, next event estimation, spherical polygons, spherical triangles, polygonal lights, real-time ray tracing, rendering, linearly transformed cosines, LTC, Monte Carlo integration, optimal MIS

## Images

![RepresentativeImage](../../assets/78ce0b9febbf6c96.jpg)


![RepresentativeImage](../../assets/78ce0b9febbf6c96.jpg)

## Notes

This work gets presented at SIGGRAPH 2021 on 12th of August. The author's version has been published on 11th of June 2021.

## Downloads and links

[Paper](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-paper.pdf)[Supplemental document](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-supplement.pdf)[Blog post series about the renderer](http://momentsingraphics.de/ToyRendererOverview.html)[Blog post about BRDF importance sampling](http://momentsingraphics.de/ToyRenderer4RayTracing.html)[Source code on GitHub](https://github.com/MomentsInGraphics/vulkan_renderer)[Code without data and dependencies (0.5 MB)](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-code.zip)[Code with data and dependencies (374 MB)](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-code_and_data.zip)[Additional scenes (Bistro, 724 MB)](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-bistro.zip)[PDF-slides](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-slides.pdf)[Python code for slides](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-slides_python.zip)[Blog post about Matplotlib slides](http://momentsingraphics.de/MatplotlibSlides.html)[Fast forward video (00:30)](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-fast_forward_video.mp4)[5-minute presentation video](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-5_minute_video.mp4)[19-minute presentation video](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-19_minute_video.mp4)