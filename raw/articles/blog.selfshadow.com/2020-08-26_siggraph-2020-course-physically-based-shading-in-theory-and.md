---
title: 'SIGGRAPH 2020 Course: Physically Based Shading in Theory and Practice'
url: https://blog.selfshadow.com/publications/s2020-shading-course/
author: Stephen Hill
published: '2020-08-26'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

![© Disney 2019.](../../assets/16c1ddbaab0c9f9f.jpg)

© Disney 2019.

## Course Description

Physically based shading has transformed the way we approach production rendering and simplified the lives of artists in the process. By adhering to physically based, energy-conserving models, one can easily create realistic materials that maintain their properties under a variety of lighting conditions. In contrast, traditional ad hoc models have required extensive tweaking to achieve the same result. Building upon previous incarnations of the course ([[1]](http://renderwonk.com/publications/s2010-shading-course/), [[2]](https://blog.selfshadow.com/publications/s2012-shading-course), [[3]](https://blog.selfshadow.com/publications/s2013-shading-course), [[4]](https://blog.selfshadow.com/publications/s2014-shading-course), [[5]](https://blog.selfshadow.com/publications/s2015-shading-course), [[6]](https://blog.selfshadow.com/publications/s2016-shading-course), [[7]](https://blog.selfshadow.com/publications/s2017-shading-course)), we present further research and practical advice on the subject, from film and game production.

## Background

For an introduction to the topic of physically based shading, we recommend watching [this presentation](https://www.youtube.com/embed/j-A0mwsJRmk?start=69) by Naty Hoffman, from the 2015 course.

## Syllabus

`08:30`

[ Some Thoughts on the Fresnel Term](https://blog.selfshadow.com#hoffman) (Naty Hoffman)

[[slides]](https://blog.selfshadow.com/hoffman/s2020_pbs_hoffman_slides.pdf)

`09:00`

[(Laurent Belcour)](https://blog.selfshadow.com#belcour)

**Bringing an Accurate Fresnel to Real-Time Rendering…**[[slides]](https://blog.selfshadow.com/belcour/slides/index.html)

[[notebook]](https://nbviewer.jupyter.org/github/belcour/sig2020_fresnel_decomposition/blob/master/notebook.ipynb)

[[code]](https://blog.selfshadow.com/belcour/s2020_pbs_belcour_code.zip)

[[supplemental]](https://blog.selfshadow.com/belcour/s2020_pbs_belcour_supplemental.pdf)

[[project page]](https://belcour.github.io/blog/research/publication/2020/08/26/brdf-fresnel-decompo.html)

`09:20`

[(Jonathan Stone and Niklas Harrysson) [slides:](https://blog.selfshadow.com#materialx)

**MaterialX Physically Based Shading Nodes**[pptx](https://blog.selfshadow.com/materialx/s2020_pbs_materialx_slides.pptx),

`09:40`

[(Lee Kerley) [slides:](https://blog.selfshadow.com#kerley)

**Putting the Pieces Together: A Physically(ish) Based Approach to Material Composition**[key](https://blog.selfshadow.com/kerley/s2020_pbs_kerley_slides.key),

`10:00`

[(Sébastien Hillaire)](https://blog.selfshadow.com#hillaire)

**Physically Based and Scalable Atmospheres in Unreal Engine**[[slides]](https://blog.selfshadow.com/hillaire/s2020_pbs_hillaire_slides.pdf)

`10:20`

[(Jasmin Patry) [slides:](https://blog.selfshadow.com#patry)

**Samurai Shading in***Ghost of Tsushima*[online](https://blog.selfshadow.com/patry/slides/index.html),

[[supplemental]](https://blog.selfshadow.com/patry/s2020_pbs_patry_supplemental.pdf)

`11:00`

[(Rob Pieké, Igor Skliar and Will Earl)](https://blog.selfshadow.com#mpc)

**Let’s Get Physical: The Hairy History of Shading at MPC**[[slides]](https://blog.selfshadow.com/mpc/s2020_pbs_mpc_slides.pdf)

`11:30`

**Q & A**

**Note**: please direct any corrections or general questions to: pbs <at> selfshadow <dot> com.

## Organisers

**Stephen Hill** is a Principal Rendering Engineer within Lucasfilm’s Advanced Development Group, where he is engaged in physically based rendering R&D for productions such as *Carne y Arena*, and more recently *The Mandalorian*. He was previously a 3D Technical Lead at Ubisoft Montreal, where he contributed to a number of *Splinter Cell* titles as well as *Assassin’s Creed Unity*.

**Stephen McAuley** started in video games in 2006 at Bizarre Creations before moving to Ubisoft in 2011, where he spearheaded the graphical vision on the *Far Cry* brand. In 2020, he joined Sony Santa Monica as a Lead Rendering Engineer. He focuses on physically based lighting and shading, data-driven rendering architecture and overall improvements in visual quality. He is also passionate about sharing his knowledge with the industry as a whole, running internal and external training and conferences.

## Presentations

**Naty Hoffman** is a Principal Engineer & Architect in the Lucasfilm Advanced Development Group. Previously he was the Vice President of Technology at 2K, and before that he worked at Activision (doing graphics R&D for various titles, including the *Call of Duty* series), SCE Santa Monica Studio (coding graphics technology for *God of War III*), Naughty Dog (developing PS3 first-party libraries), Westwood Studios (leading graphics development on *Earth and Beyond*) and Intel (driving Pentium pipeline modifications and assisting the SSE/SSE2 instruction set definition).


**Laurent Belcour** is a research scientist at Unity Technologies, focused on real-time and offline rendering. He completed his PhD on theoretical light transport at the University of Grenoble, under the supervision of Cyril Soler and Nicolas Holzschuch. Since then, his research interests have expanded to material modeling and Monte-Carlo integration.

**Mégane Bati** is a PhD student since Sept. 2018 at LP2N in Bordeaux (France), under the supervision of Romain Pacanowski and Pascal Barla. She is interested in material appearance modeling, and especially the inverse design of layered materials.

**Pascal Barla** received his PhD in 2006 on the topic of *Expressive Rendering* at INP Grenoble (France). After being recruited as a permanent researcher at Inria Bordeaux Sud Ouest in 2007, his research has expanded to the more general domain of visual appearance, with interests in both optics and perception.


**Jonathan Stone** is a Senior Software Engineer in the Lucasfilm Advanced Development Group and the lead developer of MaterialX. He has designed real-time rendering and look-development technology for Lucasfilm since 2010, working on productions including *The Mandalorian*, *Star Wars: The Force Awakens*, and *Pacific Rim*. Previously he led graphics development at Double Fine Productions, where he designed the rendering engines for *Brütal Legend* and *Psychonauts*.

**Niklas Harrysson** is a Principal Software Engineer working at Autodesk. For the past ten years, his work has been focused around rendering, shading and lighting in Autodesk’s M&E products. Prior to joining Autodesk, he worked at Illuminate Labs for eight years, developing ray tracing and light simulation software. His current projects are centered around MaterialX and in particular physically based shader construction and code generation.

**Iliyan Georgiev** is a researcher and principal software engineer at Autodesk. He holds a PhD degree from Saarland University, Germany, for which he received the Eurographics PhD Thesis Award. His research is focused primarily on Monte Carlo methods for physically based light transport simulation. Iliyan publishes regularly at top-tier scientific journals and conferences, and his work has been incorporated into various production rendering systems.


**Lee Kerley** is the Head of Shading at Sony Pictures Imageworks, where he has worked as part of the shading team for over twelve years. He focuses on the approaches the studio takes towards look development, lighting, shading, and rendering. Most recently, he has been working on user-facing material authoring tools and dynamic material composition in a production environment. While at Imageworks, he has contributed to movies as diverse as *Spider-Man 3*, *The Amazing Spider-Man*, and *Spider-Man: Into the Spider-Verse*.


**Sébastien Hillaire** is a Senior Rendering Engineer at Epic Games, focusing on the Unreal Engine renderer. He is pushing visual quality and performance in many areas, such as physically based shading, volumetric simulation and rendering, and visual effects, to name a few. Before joining Epic Games, he worked at Dynamixyz, then Criterion Games and Frostbite at Electronic Arts.


**Jasmin Patry** is a Lead Rendering Engineer at Sucker Punch Productions, where he has worked on *Infamous 2*, *Infamous Second Son*, *Infamous First Light*, and *Ghost of Tsushima*. Prior to that, he was at Radical Entertainment and contributed to their *Hulk*, *Scarface*, and *Prototype* titles. As a graduate student in the Computer Graphics Lab at the University of Waterloo, he created the popular Linux game *Tux Racer*, which was named “Best Free Software” by PC Magazine and has downloads numbering in the millions. His interests include physically based rendering, scientific computing, and performance optimization — and anything that makes games look better and run faster.


**Rob Pieké** was a Principal Architect at MPC Film. He dabbled in computer graphics programming in BASIC on the PCjr from an early age, and was completely hooked by the visual effects industry after seeing *Jurassic Park* in the cinema. After studying Computer Engineering at the University of Waterloo, Rob led a small VFX R&D team at C.O.R.E. Digital Pictures in Toronto, before moving to London to join MPC for *The Chronicles of Narnia: Prince Caspian*. He has since developed a wide range of technologies used on Hollywood blockbusters, from the *Harry Potter* series to *Guardians of the Galaxy*, *The Jungle Book* and, most recently, *The Lion King*. With a particular skew towards rendering, Rob is always interested in the use and abuse of new technologies, and what “the next big thing” for the visual effects industry might be. He recently joined SideFX as a Senior Software Developer.

**Igor Skliar** is a Senior Shader Writer at MPC Film. Graduating from the School of Art (majoring in Fine Art) as well as the National Research University of Electronic Technology, he combined his interests in math, physics and fine art, seeking to create the finest materials for the CG industry. Igor has a keen interest in rendering technologies and PBR for real production, developing and supporting the evolution of shaders to be more physically plausible and energy conserving. After joining MPC, his passion in rendering made him a key shader writer for such projects as *The Lion King* (for which he introduced a new fur BxDF), *Maleficent: Mistress of Evil* (for which he extended the BxDF to work efficiently on feathers), *Blade Runner 2049*, *Ghost in the Shell*, *Passengers* and many others.

**Will Earl** is Head of Optimization at MPC Film, working on improving efficiencies within asset development and production rendering. He has worked for several years at MPC Film as a lighting and look-development lead, most recently on *Pokémon Detective Pikachu* and *Sonic The Hedgehog*. Prior to that, he worked at Aardman Animations as Shot Technical Director and got his start in visual effects at Weta Digital as a Modeller on *King Kong*.