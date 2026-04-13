---
title: Physically based Shading at SIGGRAPH 2014
url: https://blog.selfshadow.com/2014/08/12/physically-based-shading-at-siggraph-2014/
author: Stephen Hill
published: '2014-08-12'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

![2pm, Wednesday 13th August. Located in the west building, rooms 211-214.](../../assets/a492388b7086d180.jpg)

2pm, Wednesday 13th August. Located in the west building, rooms 211-214.

We’re back once again with the Physically Based Shading (in Theory and Practice) course at SIGGRAPH! You can find the details on the new [course page](https://blog.selfshadow.com/publications/s2014-shading-course), but I’ll copy the schedule here, for your convenience:

`14:00`

**Physics and Math of Shading** (Naty Hoffman)

`14:20`

**Understanding the Masking-Shadowing Function** (Eric Heitz)

`14:40`

**Antialiasing Physically Based Shading with LEADR Mapping** (Jonathan Dupuy)

`15:00`

**Designing Reflectance Models for New Consoles** (Yoshiharu Gotanda)

`15:30`

*Break*

`15:45`

**Moving Frostbite to PBR** (Sébastien Lagarde and Charles de Rousiers)

`16:15`

**Physically Based Shader Design in Arnold** (Anders Langlands)

`16:35`

**Art Direction within Pixar’s Physically Based Lighting System** (Ian Megibben and Farhez Rayani)

As you can see, the composition of this year’s lineup is a little different than in previous years. To start with, we’ve incorporated a bit more *theory* into the first half of the course, beyond Naty Hoffman’s established and superlative introduction; Eric Heitz will be summarising his excellent [JGCT paper](http://jcgt.org/published/0003/02/03/) on microfacet masking-shadowing functions, and Jonathan Dupuy will be distilling their recent work on LEADR Mapping. Jonathan also discusses a number of *practical* issues in his accompanying course notes.

Either side of the break, we have two game industry speakers, Yoshiharu Gotanda and Sébastien Lagarde. Yoshiharu will be covering his latest R&D at tri-Ace, targeting next-gen hardware; Sébastien will also be presenting some advances, along with sharing the Frostbite team’s experiences in bringing physically based rendering principles to their engine and a number of titles. Séb and Charles de Rousiers have also compiled a highly detailed and extensive set of course notes, which should be available in the coming days.

[Arnold](https://www.solidangle.com/arnold) has fast become a (physically based) force to be reckoned with inside the VFX industry, so it’s high time that the renderer receive attention in the course. With that in mind, we have Anders Langlands (Solid Angle) talking about what makes his open-source shader library [ alShaders](https://bitbucket.org/anderslanglands/alshaders/overview) tick, the design decisions behind it, and how it plays to the strengths of Arnold.

Rounding off the session, we have Ian Megibben and Farhez Rayani from Pixar recounting the evolution of lighting over previous Toy Story films from an art perspective, as well as the challenges and benefits brought about by the switch to physically based rendering for Toy Story *OF TERROR!*

I hope to see you there!

### One last thing…

We’ve been fortunate to have some really excellent presentations in the course over the past few years. One of the most enduring and influential has been Brent Burley’s *Physically Based Shading at Disney*, in 2012. Two years on, Brent has taken the time to update his course notes with a few additional details, complementing the [shading model implementation](https://github.com/wdas/brdf/blob/master/src/brdfs/disney.brdf) that was added to Disney’s [BRDF Explorer](http://www.disneyanimation.com/technology/brdf.html) last November. Brent also revisits his “Smith G” roughness remapping, following the findings of Eric Heitz’ aforementioned paper. You can find Brent’s updated notes on the 2012 course page [ here](https://blog.selfshadow.com/publications/s2012-shading-course/).