---
title: BRDF Importance Sampling for Linear Lights
url: http://momentsingraphics.de/HPG2021.html
published: '2021-07-07'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# BRDF Importance Sampling for Linear Lights

Christoph Peters.

2021–07 in *Computer Graphics Forum (Proc. HPG)* 40, 8.

[Official version](https://doi.org/10.1111/cgf.14379)

## Abstract

We introduce an efficient method to sample linear lights, i.e. infinitesimally thin cylinders, proportional to projected solid angle. Our method uses inverse function sampling with a specialized iterative procedure that converges to high accuracy in only two iterations. It also allows us to sample proportional to a linearly transformed cosine. By combining both sampling techniques through suitable multiple importance sampling heuristics and by using good stratification, we achieve unbiased diffuse and specular real-time shading with low variance outside penumbrae at two samples per pixel. Additionally, we provide a fast method for solid angle sampling.

## Images

![teaser](../../assets/d4d7f7dcdbd1f590.webp)


![teaser](../../assets/d4d7f7dcdbd1f590.webp)

## Notes

This work has been presented at HPG 2021 on July 7th 2021. The author's version has been published on June 18th.

## Downloads and links

[Paper](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-paper.pdf)[Blog post series about the renderer](http://momentsingraphics.de/ToyRendererOverview.html)[Blog post about BRDF importance sampling](http://momentsingraphics.de/ToyRenderer4RayTracing.html)[Source code on GitHub (branch linear_lights)](https://github.com/MomentsInGraphics/vulkan_renderer/tree/linear_lights)[Code without data and dependencies (0.3 MB)](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-code.zip)[Code with data and dependencies (251 MB)](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-code_and_data.zip)[Additional scenes (Bistro, 724 MB)](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-bistro.zip)[PDF-slides](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-slides.pdf)[Python code for slides](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-slides_python.zip)[Blog post about Matplotlib slides](http://momentsingraphics.de/MatplotlibSlides.html)[Fast forward video (00:30)](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-fast_forward.mp4)[Presentation video (19:37)](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-presentation.mp4)[Fast forward on Youtube](https://youtu.be/eGfX1iWzkh0?t=5321)[Presentation on Youtube (with Q&A)](https://www.youtube.com/watch?v=1BnT89BAjeg&t=8405s)