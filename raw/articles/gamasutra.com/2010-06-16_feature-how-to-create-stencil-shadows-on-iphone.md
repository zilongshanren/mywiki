---
title: 'Feature: How To Create Stencil Shadows On iPhone'
url: https://www.gamedeveloper.com/art/feature-how-to-create-stencil-shadows-on-iphone
published: '2010-06-16'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Feature: How To Create Stencil Shadows On iPhone

Gamasutra <a href="http://www.gamasutra.com/view/feature/5867/creating_stencil_shadows_on_iphone.php">delivers a technique</a> for creating true 3D stencil-buffer shadows on the iPhone, despite the fact that "at a glance, it would seem that the common tec

June 16, 2010

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Author: by Staff

Gamasutra's [latest feature](http://www.gamasutra.com/view/feature/5867/creating_stencil_shadows_on_iphone.php) delivers a technique for creating true 3D stencil-buffer shadows on the iPhone, despite the fact that, according to author Brian Hall, "At a glance, it would seem that the common techniques used to produce shadows are not possible on the iPhone." As we all know, the technique of adding realistic shadows allows 3D games to achieve much greater depth -- and, at the same time, the current generation of iPhones can't deliver the same fidelity of graphics we're used to from many other platforms. "At the highest level, the method is straightforward. First, the scene objects are rendered. Second, the objects to cast shadows have their edges processed, extruded into volumes, and the volumes are rendered into the stencil buffer," writes Hall, who works as manager of console technologies at Turbine Entertainment. "Last, a full screen shadow colored quad is rendered over the scene using the stencil buffer as a mask." "Mobile platforms for some of us are a blast from the past, where we again get to trick limited hardware to do things we want it to do, in order to obtain stunning visuals. The result: Dynamic Shadows on the iPhone, despite its imposed limitations." he writes. [The feature](http://www.gamasutra.com/view/feature/5867/creating_stencil_shadows_on_iphone.php), live today on Gamasutra, contains the step-by-step procedure along with illustrative screenshots of each step in the process.