---
title: 'SIGGRAPH 2025 Course: Physically Based Shading in Theory and Practice'
url: https://blog.selfshadow.com/publications/s2025-shading-course/
author: Stephen Hill
published: '2026-01-01'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

![Courtesy of Amazon Prime Video](../../assets/5160d7108e51b172.jpg)

Courtesy of Amazon Prime Video

## Course Description

Physically based shading has transformed the way we approach production rendering and simplified the lives of artists in the process. By adhering to physically based, energy-conserving models, one can easily create realistic materials that maintain their properties under a variety of lighting conditions. In contrast, traditional ad hoc models have required extensive tweaking to achieve the same result. Building upon previous incarnations of the course ([[1]](http://renderwonk.com/publications/s2010-shading-course/), [[2]](https://blog.selfshadow.com/publications/s2012-shading-course), [[3]](https://blog.selfshadow.com/publications/s2013-shading-course), [[4]](https://blog.selfshadow.com/publications/s2014-shading-course), [[5]](https://blog.selfshadow.com/publications/s2015-shading-course), [[6]](https://blog.selfshadow.com/publications/s2016-shading-course), [[7]](https://blog.selfshadow.com/publications/s2017-shading-course), [[8]](https://blog.selfshadow.com/publications/s2020-shading-course)), we present further research and practical advice on the subject, from film and game production.

## Background

For an introduction to the topic of physically based shading, we recommend watching [this presentation](https://www.youtube.com/embed/j-A0mwsJRmk?start=69) by Naty Hoffman, from the 2015 course.

## Syllabus

`09:00`

**Fundamentals of Physically Based Shading** (Naty Hoffman) [[slides]](https://blog.selfshadow.com/hoffman/s2025_pbs_hoffman_slides.pdf)

`09:20`

**OpenPBR: A Closer Look at Novel Features and Implementation Details** (Peter Kutz) [[slides]](https://blog.selfshadow.com/openpbr/s2025_pbs_openpbr_slides.pdf) [[course notes]](https://blog.selfshadow.com/openpbr/s2025_pbs_openpbr_notes_v1.3.pdf)

`09:45`

**EON: Advancing Rough Diffuse Reflection with Energy Preservation and Clipped LTC Sampling** (Peter Kutz and Stephen Hill) [[slides]](https://blog.selfshadow.com/eon/s2025_pbs_eon_slides.pdf)

`10:05`

**Spectral Rendering in a Non-Spectral Renderer: How Can we Author and Render Fluorescence in RGB?** (Laurent Belcour) [[slides]](https://blog.selfshadow.com/belcour/slides/index.html)

`10:30`

*Break*

`10:45`

**Strand: A Production Model for Shading Hair, Fur and Feathers** (Alain Hostettler) [[slides]](https://blog.selfshadow.com/hostettler/s2025_pbs_hostettler_slides.pdf) [[course notes]](https://blog.selfshadow.com/hostettler/s2025_pbs_hostettler_notes.pdf)

`11:10`

**Bridging the Gap Between Offline and Real Time with Neural Materials** (Andrea Weidlich) [[slides]](https://blog.selfshadow.com/weidlich/s2025_pbs_weidlich_slides.pdf) [[course notes]](https://blog.selfshadow.com/weidlich/s2025_pbs_weidlich_notes_v1.1.pdf)

`11:35`

**Driving Toward Reality: Physically Based Tone Mapping and Perceptual Fidelity in Gran Turismo 7**

[[slides]](https://blog.selfshadow.com/pdi/s2025_pbs_pdi_slides_v1.1.pdf)

[[code]](https://blog.selfshadow.com/pdi/supplemental/gt7_tone_mapping.cpp)

(Kenichiro Yasutomi, Kentaro Suzuki and Hajime Uchimura)

**Note**: please direct any corrections or general questions to: pbs <at> selfshadow <dot> com.

## Organisers

**Stephen Hill** is a Principal Rendering Engineer within Lucasfilm’s Advanced Development Group, where he is engaged in physically based rendering R&D for productions such as *Carne y Arena*, and more recently *The Mandalorian*. He was previously a 3D Technical Lead at Ubisoft Montreal, where he contributed to a number of *Splinter Cell* titles as well as *Assassin’s Creed Unity*.

**Stephen McAuley** started in video games in 2006 at Bizarre Creations before moving to Ubisoft in 2011, where he spearheaded the graphical vision on the *Far Cry* brand. In 2020, he joined Sony Santa Monica as a Lead Rendering Engineer and is now Technical Director. He focuses on physically based lighting and shading, data-driven rendering architecture and overall improvements in visual quality. He is also passionate about sharing his knowledge with the industry as a whole, running internal and external training and conferences.

## Presenters

**Laurent Belcour** is a computer graphics researcher working at Intel Corporation in Grenoble, France. He defended his PhD at the University of Grenoble in 2012 and then worked at Inria Bordeaux, the University of Montréal, and Unity Technologies. His research interests include material models, (quasi) Monte Carlo rendering, importance sampling, and machine learning.

**Naty Hoffman** has recently retired after a storied career in real-time rendering. He has worked at Meta (improving the appearance of Meta Avatars), Lucasfilm (designing and implementing advanced rendering algorithms for ILM StageCraft and VR experiences), 2K Games (driving technology development across the publishing label), Activision (doing graphics R&D for many games including the *Call of Duty* series), SCE Santa Monica Studio (coding graphics technology for *God of War III*), Naughty Dog (developing PS3 first-party libraries), Westwood Studios (leading graphics development on *Earth and Beyond*) and Intel (driving Pentium pipeline modifications and assisting with the SSE and SSE2 instruction set definitions). During his career, Naty was also responsible for many influential publications and presentations, on rendering topics including physically based shading, cinematic lighting, and color perception in graphics.

**Alain Hostettler** is a Senior R&D Engineer at Industrial Light & Magic (ILM). He joined ILM in 2021 after finishing his MSc in Computer Science at ETH Zurich with a focus on computer graphics, and an internship at Disney Research Studios in Zurich, where he researched methods to improve the ML-based denoising of Monte Carlo renders. At ILM, Alain is working in the offline rendering and shading engineering team. He has implemented numerous plugins for RenderMan to support productions and is continuously working on improving and extending *Lama*, the modular material system that powers look development at ILM.

**Peter Kutz:** After writing his first photorealistic path tracer as a hobby at the University of Pennsylvania and interning at Pixar, Peter spent five years at Walt Disney Animation Studios working on the Hyperion renderer – contributing to its architecture, implementing features for multiple films, and co-authoring several papers on volume rendering and beyond. He later joined the Apple Vision Pro team to develop hybrid rasterization and ray tracing for AR applications. For the past five years, Peter has been at Adobe, crafting proprietary path-tracing solutions for Adobe’s in-house GPU-first renderer and helping to define standards such as the Adobe Standard Material and OpenPBR, bridging cutting-edge research with practical production needs in physically based shading.

**Kentaro Suzuki** is a Lead Graphics Engineer at Polyphony Digital Inc. His computer graphics life began with the demoscene culture of the early 2000s. After studying computer graphics at university, he joined Polyphony Digital Inc., where he has contributed to the world-famous *Gran Turismo* racing game series. His primary interests are developing various real-time rendering techniques and exploring offline ray-tracing algorithms.

**Hajime Uchimura** is an Image Processing Engineer at Polyphony Digital Inc. He started computer graphics with the MSX at the age of six. He joined Polyphony Digital Inc. after high-precision calculation research for his master’s degree. His main topics are image processing and color science. He’s the proud father of a girl and a boy.

**Andrea Weidlich** is a Principal Researcher at NVIDIA in the Real-Time Rendering Research department. Before joining NVIDIA, she worked for Weta Digital, where she designed the material system attached to Weta’s proprietary physically based renderer, Manuka. Her main research areas are appearance modelling and material prototyping. Andrea holds a Master of Arts in Applied Media from the University of Applied Arts Vienna and a PhD in Computer Science from Vienna University of Technology.

**Kenichiro Yasutomi** is a Lead Technical Artist at Polyphony Digital Inc. He studied urban engineering at university. However, he became fascinated by computer graphics, which he began using for presentations. Eventually, he entered the game industry as an artist.

## Additional Contributors

**Pascal Barla** received his PhD in 2006 on the topic of Expressive Rendering at INP Grenoble (France). After being recruited as a permanent researcher at Inria Bordeaux Sud Ouest in 2007, his research has expanded to the more general domain of visual appearance, with interests in both optics and perception.

**Alban Fichet** is a software research engineer at Intel in the Grenoble GraphiX Research Team. Before that, he worked at Unity Technologies. Starting from his PhD at Grenoble University and his postdoc at Institut d’Optique Graduate School in Bordeaux Alban worked on material appearance and capture, as well as accurate light transport simulation.

**Jamie Portsmouth** is a Principal Software Engineer at Autodesk, working on Autodesk’s Arnold renderer. He is mostly focused on physically based rendering, most recently helping to define the OpenPBR Surface uber-shader standard.