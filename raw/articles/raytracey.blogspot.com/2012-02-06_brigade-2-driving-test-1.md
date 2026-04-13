---
title: 'Brigade 2: driving test 1'
url: http://raytracey.blogspot.com/2012/02/brigade-2-driving-test-1.html
author: Sam Lapere
published: '2012-02-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another simple test with Brigade 2. I've managed to make the camera follow the vehicle while it's driving, which greatly enhances the immersion. I've also added a ramp to the scene:

4 spp with frame averaging, note the diffuse color bleeding from the floor onto the blocks at the left:

In a next test I will add some spiffy looking and highly detailed architecture to the scene (untextured at first). This image shows color bleeding and the use of diffuse, glossy, perfectly specular and refractive materials, all path traced in real-time:

Videos of this scene will be posted tomorrow.

## 3 comments:

Hi Ray. Im wondering. Why is game slower (lower fps), when there are more objects visible? I thought it is irrelevant, if they are behind camera or in front of.

The ray tracing performance depends on the amount of geometry in your viewplane (and also on material complexity). Primary rays are shot from the camera through every pixel of the screen, if they hit bounding volumes (in the acceleration structure) or primitives (scene geometry), multiple intersections have to be computed, which causes the framerate to drop. Secondary random rays are harder to predict, they can hit the skydome or other primitives in the scene, adding to the computational cost.

All Instructors must always be willing to give feedback to the relevant person, ex. A parent of the student. They must be able to answer all questions and give honest opinions regarding the student`s progress.

Post a Comment