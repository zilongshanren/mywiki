---
title: Bungie talks about ray tracing and voxels
url: http://raytracey.blogspot.com/2012/01/bungie-talking-about-ray-tracing-and.html
author: Sam Lapere
published: '2012-01-02'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://www.gamasutra.com/view/news/39332/The_Big_Graphics_Problems_Bungie_Wants_To_Solve.php](http://www.gamasutra.com/view/news/39332/The_Big_Graphics_Problems_Bungie_Wants_To_Solve.php)

Some interesting fragments:

I've certainly seen how even today people are having a lot of trouble rendering shadows without a lot of blockiness or dithering.

HC: That's kind of the problem with computer game graphics these days. A lot of things people consider solved problems are actually quite far from being solved, and shadows are one of them. After all these years we don't have a very satisfactory shadow solution. They're improving; every generation of games they're improving, but they're nowhere near the perfect solution that people thought we already have.

What do you think might be the answer? Your potential megatexture solution, or something else?

HC: We are still far from seeing perfect shadows. Shadows are a byproduct of lighting. All frequency shadows (shadows that are hard and soft in all the right places) are a byproduct of global illumination, and these things are notoriously hard in real time.<

About the potential of using voxels for faster and more efficient global illumination:There's just not enough machine power, even in today's generation or the next generation, to be able to capture that kind of fidelity. There are also inherent limitations to the current techniques, such as shadow maps, for example. When the light is near the glancing angle of a shadow receiver, then it is impossible to do the correct thing.With the current state of the art shadow techniques we can manage the resolution much better, and we can do high quality filtering, but we still have long ways to go to get where we need to be, even if we just talk about hard shadows from direct illumination.I think megatextures could help, but still fundamentally there are things you cannot solve with our current shadow meshes. And until the performance supports real-time ray tracing and global illumination, we're going to continue seeing hack after hack for rendering shadows.

HC: Voxels are very very interesting to us. For example, when we take advantage of voxelization, we basically voxelize our level and then we build these portalizations and clustering of our spaces based on the voxelization. And so voxelization, what it does is hide all the small geometry details. And in the regular data structures, it's very easy to reason out the space when it's voxelized versus dealing with individual polygons.But besides this ability, there's also the very interesting possibility for us to use voxelization or a voxelized scene to do lighting and global illumination. We have some thoughts in that area that we might research in the future, but in general I think it's a very good direction for us to think about; to use voxelization to hide all the details of the scene geometry and sort of decouple the complexity of the scene from the complexity of lighting and visibility. In that way everything becomes easier in voxelization.

## 1 comment:

i like this blog...

Construction & Property Jobs | Careers & Recruitment at Jobscharger.com

http://www.jobscharger.com/JobIndustry/Construction-Property-7-.html

Post a Comment