---
title: Graphics Programming weekly - Issue 190 - July 4, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-190/
author: Jendrik Illner
published: '2021-07-04'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presents the use of neural fields to model materials such as fur, fabric, and grass
- model a layer of mesoscale structure, such as fur or grass, on top of a triangle mesh using neural reflectance fields
- NeRF textures are volumetric textures that use neural nets instead of voxels

![](../../assets/d1b4b4a4779ebe71.png)


- author presents the subset of Vulkan API related to compute workloads
- covering GPU discovery, resource management, compute pipeline management, synchronization, and object lifetime management

![](../../assets/118cc9b55ca1b6b7.png)


- blog post presents a comparison of AMDs FSR, CAS against other upscale techniques
- shows results from Dota 2, The Riftbreaker
- showing how quality and sharpening values influence the final results

![](../../assets/f891b3864649f452.png)


- the paper presents a filter for magnifying pixel art (such as 8- and 16-bit sprites)
- covering observations on pixel-art filtering, test data, and evaluation methodology
- shows a comparison against other filters and shows when to use what filter
- code and demo application is provided

![](../../assets/e9dc731accca6b36.png)


- the video tutorial explains how to use the add, subtract, multiply, and divide nodes in UE5 and Unity
- showing how the nodes behave and the difference in the UI between UE5 and Unity visual shader editors

![](../../assets/eb901b7b67d26653.png)

We are looking for a Rendering Engineer with experience in developing high-quality, high-performance software: in games or otherwise.

This role will suit someone who is keen to take the next step forward in their career and in interactive tech. We are working on core immersive technology that spans the full range of XR, and this is an opportunity to help shape the future of spatial computing.

Simul is an established leader in real-time graphics middleware; the company’s customers include Bandai Namco, Microsoft Game Studios, Sony, and Ubisoft. In 2020, Simul won the TIGA 2020 Best Technical Innovation Award for our work on trueSKY, the leading real-time weather SDK. We have a culture of agile development focused on quality, performance and precision. We believe in equal opportunity and a diverse, inclusive and supportive workplace.

You will be:

- Researching and developing new immersive technologies,
- Working in an agile team,
- Finding and fixing bugs and performance issues,
- Profiling and optimizing CPU, GPU and network code,
- Representing Simul at technical and non-technical events, in-person and online.

The benefits Simul offers are:

- Flexible remote working,
- Regular salary reviews and career progression,
- 22 days holiday + bank holidays,
- Dedicated self-development time.

![](../../assets/ff7737dd6e745c46.png)


- the paper presents a new operator for blending BRDF texture maps
- based on a transport mechanism that is feature aware
- preserve details by mixing the material channels using a histogram-aware color blending combined with a normal reorientation

![](../../assets/580837f102ffd766.png)


- stream of the first day of Eurographics Symposium on Rendering 2021
- all recordings from the 4 days are available

![](../../assets/90ec131216c57d83.png)

- paper presents the Moving Basis Decomposition framework
- this generalizes many existing basis expansion methods and efficient, seamless reconstruction of compressed data
- this is introduced as the foundation for a global illumination system
- compares the method against existing Blockwise PCA, Windowed blockwise PCA, and clustered PCA (PCA, Principal component analysis)

![](../../assets/b1e73b2e67833a75.png)


- the article discusses the scene structure of the authors’ renderer
- focuses on how to efficiently handle scene export/loading as flat data
- data quantization, materials, reproducible results, …
- iteration time from changing code to getting a render is below 5 seconds

![](../../assets/67d6d4d6059d38cc.png)


- paper presents a new path sampling algorithm for indirect lighting
- based on the screen-space Spatio-temporal resampling principles of ReSTIR (Spatiotemporal reservoir resampling for real-time ray tracing with dynamic direct lighting.)
- enables important paths to share contributions time, space

![](../../assets/c053cdc5fbb17f3b.png)


- the article presents an overview of why Pipeline State Object was introduced to allow predictable performance
- shows differences between hardware and drivers and explain why the old D3D11 model was unpredictable
- presents the concepts in Vulkan, D3D12 and Metal

![](../../assets/d4ba076bed31417f.png)


- the video tutorial shows a walkthrough to render the USA flag using shader toy
- shows how to render a star, stripes and combines the components
- covers how to animate the flag and apply antialiasing between the features
- additionally adds some shading to the flag

![](../../assets/41d5a7e40064a8ad.png)

Thanks to Dirk Dörr for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.