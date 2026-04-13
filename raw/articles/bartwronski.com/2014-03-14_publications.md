---
title: Publications
url: https://bartwronski.com/publications/
published: '2014-03-14'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Collaborative Texture Filtering

[T. Akenine-Möller](https://cs.lth.se/outdated/tomas-akenine-moller/), [P. Ebelin](https://scholar.google.com/citations?user=q5P31y8AAAAJ&hl=sv), [M. Pharr](https://pharr.org/matt/), and [ B. Wronski](https://bartwronski.com/).

Accepted to

*ACM/EG Symposium on High Performance Graphics (HPG), 2025*

![](../../assets/09f2048828927b68.png)


![](../../assets/09f2048828927b68.png)

Recent advances in texture compression provide major improvements in compression ratios, but cannot use the GPU’s texture units for decompression and filtering. This has led to the development of stochastic texture filtering (STF) techniques to avoid the high cost of multiple texel evaluations with such formats. Unfortunately, those methods can give undesirable visual appearance changes under magnification and may contain visible noise and flicker despite the use of spatiotemporal denoisers. Recent work substantially improves the quality of magnification filtering with STF by sharing decoded texel values between nearby pixels (Wronski 2025). Using GPU wave communication intrinsics, this sharing can be performed inside actively executing shaders without memory traffic overhead. We take this idea further and present novel algorithms that use wave communication between lanes to avoid repeated texel decompression prior to filtering. By distributing unique work across lanes, we can achieve zero-error filtering using ≤1 texel evaluations per pixel given a sufficiently large magnification factor. For the remaining cases, we propose novel filtering fallback methods that also achieve higher quality than prior approaches.

## Generative Detail Enhancement for Physically Based Materials

[S. Hadadan](https://www.cs.umd.edu/~saeedhd/#home), [B. Bitterli](https://benedikt-bitterli.me/), [T. Zeltner,](https://tizianzeltner.com/) [J. Novák](https://research.nvidia.com/person/jan-novak), [J. Munkberg](https://research.nvidia.com/person/jacob-munkberg), [J. Hasselgren](https://research.nvidia.com/person/jon-hasselgren), [ B. Wronski](https://bartwronski.com/), and

[M. Zwicker](https://www.cs.umd.edu/~zwicker/). Accepted to

*ACM SIGGRAPH 2025 Conference Proceedings*

![](../../assets/332d543f17aa6b89.png)


![](../../assets/332d543f17aa6b89.png)

We present a tool for enhancing the detail of physically based materials using an off-the-shelf diffusion model and inverse rendering. Our goal is to enhance the visual fidelity of materials with detail that is often tedious to author, by adding signs of wear, aging, weathering, etc. As these appearance details are often rooted in real-world processes, we leverage a generative image model trained on a large dataset of natural images with corresponding visuals in context. Starting with a given geometry, UV mapping, and basic appearance, we render multiple views of the object. We use these views, together with an appearance-defining text prompt, to condition a diffusion model. The details it generates are then backpropagated from the enhanced images to the material parameters via inverse differentiable rendering. For inverse rendering to be successful, the generated appearance has to be consistent across all the images. We propose two priors to address the multi-view consistency of the diffusion model. First, we ensure that the initial noise that seeds the diffusion process is itself consistent across views by integrating it from a view-independent UV space. Second, we enforce geometric consistency by biasing the attention mechanism via a projective constraint so that pixels attend strongly to their corresponding pixel locations in other views. Our approach does not require any training or finetuning of the diffusion model, is agnostic of the material model used, and the enhanced material properties, i.e., 2D PBR textures, can be further edited by artists.

## Improved Stochastic Texture Filtering Through Sample Reuse

[ B. Wronski](https://bartwronski.com),

[M. Pharr](https://pharr.org/matt/), T. Akenine-Möller. Accepted to

*ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games (I3D) 202*5

![](../../assets/cdb6ea51eede8ea4.png)


![](../../assets/cdb6ea51eede8ea4.png)

Stochastic texture filtering (STF) has re-emerged as a technique that can bring down the cost of texture filtering of advanced texture compression methods, e.g., neural texture compression. However, during texture magnification, the swapped order of filtering and shading with STF can result in aliasing. The inability to smoothly interpolate material properties stored in textures, such as surface normals, leads to potentially undesirable appearance changes.

We present a novel method to improve the quality of stochastically-filtered magnified textures and reduce the image difference compared to traditional texture filtering. When textures are magnified, nearby pixels filter similar sets of texels and we introduce techniques for sharing texel values among pixels with only a small increase in cost (0.04-0.14 ms per frame). We propose an improvement to weighted importance sampling that guarantees that our method never increases error beyond single-sample stochastic texture filtering. Under high magnification, our method has >10 dB higher PSNR than single-sample STF. Our results show greatly improved image quality both with and without spatiotemporal denoising.

## GPU Friendly Laplacian Texture Blending

[ B. Wronski](https://bartwronski.com), Accepted to

*Journal of Computer Graphics Techniques (JCGT), vol. 14, no. 1, 21-39, 2025*

[JCGT Official Paper Page](https://jcgt.org/published/0014/01/02/), [arXiv version](https://arxiv.org/abs/2502.13945)

Texture and material blending is one of the leading methods for adding variety to rendered virtual worlds, creating composite materials, and generating procedural content. When done naively, it can introduce either visible seams or contrast loss, leading to an unnatural look not representative of blended textures. Earlier work proposed addressing this problem through careful manual parameter tuning, lengthy per-texture statistics precomputation, look-up tables, or training deep neural networks. In this work, we propose an alternative approach based on insights from image processing and Laplacian pyramid blending.

Our approach does not require any precomputation or increased memory usage (other than the presence of a regular, non-Laplacian, texture mipmap chain), does not produce ghosting, preserves sharp local features, and can run in real time on the GPU at the cost of a few additional lower mipmap texture taps.

## Filtering After Shading with Stochastic Texture Filtering

[M. Pharr](https://pharr.org/matt/)*, [ B. Wronski](https://bartwronski.com)*,

[M. Salvi](https://research.nvidia.com/person/marco-salvi),

[M. Fajardo](https://sushideathrobots.github.io/). Accepted to

*ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games (I3D) 2024*,

**Best Paper Award**(*Equal contributors)

2D texture maps and 3D voxel arrays are widely used to add rich detail to the surfaces and volumes of rendered scenes, and filtered texture lookups are integral to producing high-quality imagery. We show that applying the texture filter after evaluating shading generally gives more accurate imagery than filtering textures before BSDF evaluation, as is current practice. These benefits are not merely theoretical, but are apparent in common cases. We demonstrate that practical and efficient filtering after shading is possible through the use of stochastic sampling of texture filters.

Stochastic texture filtering offers additional benefits, including efficient implementation of high-quality texture filters and efficient filtering of textures stored in compressed and sparse data structures, including neural representations. We demonstrate applications in both real-time and offline rendering and show that the additional error from stochastic filtering is minimal. We find that this error is handled well by either spatiotemporal denoising or moderate pixel sampling rates.

## Random-Access Neural Compression of Material Textures

[K. Vaidyanathan](https://www.linkedin.com/in/karthik-vaidyanathan-13489b/)*, [M. Salvi](https://research.nvidia.com/person/marco-salvi)*, ** B. Wronski***,

[T. Akenine‑Möller](https://research.nvidia.com/person/tomas-akenine-moller),

[P. Ebelin](https://research.nvidia.com/person/pontus-ebelin),

[A. Lefohn](https://research.nvidia.com/person/aaron-lefohn), Accepted to

**ACM Siggraph 2023**(

*Equal contributors)

We propose a novel neural compression technique specifically designed for material textures. We unlock two more levels of detail, i.e., 16X more texels, using low bitrate compression, with image quality that is better than advanced image compression techniques, such as AVIF and JPEG XL. Our method allows on-demand, real-time decompression with random access similar to block texture compression on GPUs, enabling compression on disk and memory. The key idea behind our approach is compressing multiple material textures and their mipmap chains together using a small neural network, that is optimized for each material, to decompress them. We use a custom training implementation to achieve practical compression speeds, whose performance surpasses that of general frameworks, like PyTorch, by an order of magnitude.

## Fast and High-quality Image Denoising via Malleable Convolutions

[Y. Jiang](https://yifanjiang.net/), [ B. Wronski](https://bartwronski.com/),

[B. Mildenhall](https://bmild.github.io/),

[J. T. Barron](https://jonbarron.info/),

[Z. Wang](https://spark.adobe.com/page/CAdrFMJ9QeI2y/),

[T. Xue](https://people.csail.mit.edu/tfxue/), Accepted to

**ECCV 2022**

![](../../assets/ddb08f90ac48387c.png)

[Project website](https://yifanjiang.net/MalleConv.html), [arXiv preprint](https://arxiv.org/abs/2201.00392)

To achieve spatial-varying processing without significant overhead, we present Malleable Convolution (MalleConv), as an efficient variant of dynamic convolution. The weights of MalleConv are dynamically produced by an efficient predictor network capable of generating content-dependent outputs at specific spatial locations. Unlike previous works, MalleConv generates a much smaller set of spatially-varying kernels from input, which enlarges the network’s receptive field and significantly reduces computational and memory costs. These kernels are then applied to a full-resolution feature map through an efficient slice-and-conv operator with minimum memory overhead.

## Procedural Kernel Networks

** B. Wronski**, arXiv preprint / technical report

In this work, we introduce Procedural Kernel Networks (PKNs), a family of machine learning models which generate parameters of image filter kernels or other traditional algorithms. A lightweight CNN processes the input image at a lower resolution, which yields a significant speedup compared to other kernel-based machine learning methods and allows for new applications. The architecture is learned end-to-end and is especially well suited for a wide range of low-level image processing tasks, where it improves the performance of many traditional algorithms. We also describe how this framework unifies some previous work applying machine learning for common image restoration tasks.

## Image Stylization: From Predefined to Personalized, IET Research Journal 2020

[I.Garcia-Dorado](http://www.ignaciogarciadorado.com/), [P. Getreuer](https://getreuer.info/), ** B. Wronski**,

[P. Milanfar](https://sites.google.com/view/milanfarhome/), IET Research Journals 2020 special edition.

![](../../assets/079d30e31fa5489d.png)

[https://arxiv.org/abs/2002.10945](https://arxiv.org/abs/2002.10945) Arxiv preprint

We present a framework for interactive design of new image stylizations using a wide range of predefined filter blocks. Both novel and off-the-shelf image filtering and rendering techniques are extended and combined to allow the user to unleash their creativity to intuitively invent, modify, and tune new styles from a given set of filters.

## Handheld Multi-Frame Super-Resolution, ACM Siggraph 2019 Technical Paper

[B. Wronski](https://www.google.com/url?q=https%3A%2F%2Fbartwronski.com%2F&sa=D&sntz=1&usg=AFQjCNHIiF28JQSA9S4or0S0vjrjkvcysA), [I. Garcia-Dorado](http://www.google.com/url?q=http%3A%2F%2Fwww.ignaciogarciadorado.com%2F&sa=D&sntz=1&usg=AFQjCNEwA4GPzzlkVfsY6wtZDb9ny8pQ_g), M. Ernst, D. Kelly, M. Krainin, [C.K. Liang](http://www.google.com/url?q=http%3A%2F%2Fchiakailiang.org%2F&sa=D&sntz=1&usg=AFQjCNEZ7GmcnWy1yMX2FderL0bzT9cOUA), [M. Levoy](http://www.google.com/url?q=http%3A%2F%2Fgraphics.stanford.edu%2F~levoy%2F&sa=D&sntz=1&usg=AFQjCNFpw_nOi6iMLAr5mdfLVtbweSYOhw), and [P. Milanfar](https://www.google.com/url?q=https%3A%2F%2Fsites.google.com%2Fcorp%2Fview%2Fmilanfarhome%2F&sa=D&sntz=1&usg=AFQjCNHOlMckKwJjHZTh7402Ga1BsOYp_Q), * to appear in ACM Transactions on Graphics, Vol. 38, No. 4, Article 28, July 2019 (SIGGRAPH 2019)

![unnamed (1)](../../assets/3910c9eef9c7e354.jpg)

We present a multi-frame super-resolution algorithm that supplants the need for demosaicing in a camera pipeline by merging a burst of raw images. In the above figure we show a comparison to a method that merges frames containing the same-color channels together first, and is then followed by demosaicing (top). By contrast, our method (bottom) creates the full RGB directly from a burst of raw images. This burst was captured with a hand-held mobile phone and processed on the device. Note in the third (red) inset that the demosaiced result exhibits aliasing (Moiré), while our result takes advantage of this aliasing, which changes on every frame in the burst, to produce a merged result in which the aliasing is gone but the cloth texture becomes visible.

## Volumetric fog: Unified, compute shader based solution to atmospheric scattering, ACM Siggraph 2014

![sig2014](../../assets/b189438558fbb382.jpg)

**Bartlomiej Wronski**, ACM Siggraph 2014

[PPTX Version](https://bartwronski.com/wp-content/uploads/2014/08/bwronski_volumetric_fog_siggraph2014.pptx) – 83MB (with movies)

[PDF Version with presenter notes](https://bartwronski.com/wp-content/uploads/2014/08/bwronski_volumetric_fog_siggraph2014.pdf) – 6MB

This talk presents “Volumetric Fog”, a novel technique developed by Ubisoft Montreal for *Assassin’s Creed 4: Black Flag* for next-gen consoles and PCs.

The technique addresses problem of calculating in unified, coherent and optimal way various atmospheric effects related to the atmospheric scattering:

- Fog, smoke and haze with varying participating media density
- „God rays”
- Light-shafts
- Volumetric lighting and shadows

Developed technique supports varying density of participating media, multiple light sources, is compatible with both deferred and forward shading and is faster than existing ray marching approaches.

## Assassin’s Creed 4: Road to Next-gen Graphics, GDC 2014

![gdc2014](../../assets/aa6a9ba029c6f501.jpg)

**Bartlomiej Wronski**, GDC 2014

### Presentation

[PDF Version](https://bartwronski.com/wp-content/uploads/2014/03/ac4_gdc.pdf) – 4.11MB

[PDF Version with presenter notes](https://bartwronski.com/wp-content/uploads/2014/03/ac4_gdc_notes.pdf) – 9.63MB

[PPTX Version without the movies](https://bartwronski.com/wp-content/uploads/2014/03/ac4_gdc_nomovies.pptx) – 7MB

[PPTX Version with the movies](https://bartwronski.com/wp-content/uploads/2014/03/ac4_gdc.pptx) – 164MB

### Movies separate download

[Global Illumination – time of day cycle](https://bartwronski.com/wp-content/uploads/2014/03/gi_timeofday.avi) – 17 MB

[Volumetric fog – animated plants shadows](https://bartwronski.com/wp-content/uploads/2014/03/volumefog_animatedplants.wmv) – 21 MB

[Volumetric fog – local lights support](https://bartwronski.com/wp-content/uploads/2014/03/lightsandvolumefog.wmv) – 39 MB

[Screenspace reflections – on / off video](https://bartwronski.com/wp-content/uploads/2014/03/abstergo_ssr_01.wmv) – 79MB

This talk will describe the novel techniques and easy-to-integrate effects of Assassin’s Creed IV that contribute to the next-gen look. It will provide attendees with basic information about porting various GPU effects to next-gen consoles. The talk is divided into four parts. First, there will be a description of deferred normalized irradiance probes – a GI technique that is based on FarCry 3 deferred radiance transfer volumes. The next part will describe volumetric fog – a novel technique that simulates various light scattering phenomena through the use of compute shaders and light accumulation in volumetric textures. The third part will include information about atmospheric and material effects such as GPU-simulated rain particles and raymarched screenspace reflections that can easily contribute to the next-gen look of the game without many content or pipeline changes. Finally, there will be a brief description of AMD Southern Islands architecture and practical lessons learned while developing/porting/optimizing those GPU effects to PlayStation 4 and Xbox One.

## Assassin’s Creed 4: Lighting, weather and atmospherics, Digital Dragons 2014

![dd2014](../../assets/c499768a5244c0ad.jpg)

**Bartlomiej Wronski**, Digital Dragons 2014

[PPTX Version, 226MB ](https://bartwronski.com/wp-content/uploads/2014/05/assassin_s-creed-4-digital-dragons-2014.pptx)– but worth it (tons of videos!)

[PPTX Version with extremely compressed videos](https://bartwronski.com/wp-content/uploads/2014/05/assassin_s-creed-4-digital-dragons-2014-low-res.pptx), 47MB

[PDF Version with sparse notes](https://bartwronski.com/wp-content/uploads/2014/05/assassin_s-creed-4-digital-dragons-2014.pdf), 6MB

# Other publications

## GPU Pro 6: Advanced Rendering Techniques

![9781482264616](../../assets/95bd2e8677da0bb8.jpg)

A K Peters/CRC Press

Published September 11, 2015

Reference – 586 Pages – 279 Color Illustrations

ISBN 9781482264616 – CAT# K24427

Two articles:

**Deferred Normalized Irradiance Probes**, John Huelin, Benjamin Rouveyrol, and *Bartlomiej Wronski*

**Volumetric Fog and Lighting**, *Bartlomiej Wronski*

Pingback: My GDC 2014 slides are up | Bart Wronski

Pingback: GCN – two ways of latency hiding and wave occupancy | Bart Wronski

Pingback: Digital Dragons 2014 slides | Bart Wronski

Pingback: Siggraph 2014 talk slides are up! | Bart Wronski

Pingback: Volumetric lights - Alexandre Pestana

Pingback: Major C#/.NET graphics framework update + volumetric fog code! | Bart Wronski

Pingback: Digital Dragons 2014 programming track | knarkowicz

Pingback: Adventures in postprocessing with Unity | Interplay of Light

Pingback: hikari – Implementing Single-Scattering | devfault

Pingback: Why are video games graphics (still) a challenge? Productionizing rendering algorithms | Bart Wronski

Pingback: How I use ChatGPT daily (scientist/coder perspective) | Bart Wronski