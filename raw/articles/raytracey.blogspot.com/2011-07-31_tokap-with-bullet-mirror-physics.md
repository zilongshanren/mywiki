---
title: 'TOKAP with Bullet: Mirror physics'
url: http://raytracey.blogspot.com/2011/07/tokap-with-bullet-mirror-physics.html
author: Sam Lapere
published: '2011-07-31'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I'm having great time following your blog. Like you, I love the photorealistic render that the path tracer gives.

But I'm kinda noob with the algorithm, so my question will may seems inapropriate:

For the mirror effect, are you using some kind of tricks, like RTT? or do you use plain path tracing? If so, how many rebounds do you need for such an effect?

thx in advance, and keep on with the great job, your work makes want to try out to code one myself.

The reflections are perfectly specular, so they can use a Whitted-style 'shortcut' for computational efficiency by tracing only the reflected ray. So reflections aren't path traced, but the results are the same in the case of perfect reflections. The number of bounces in the pictures is between 5 and 8 (no infinite reflections).

## 3 comments:

I'm having great time following your blog. Like you, I love the photorealistic render that the path tracer gives.




But I'm kinda noob with the algorithm, so my question will may seems inapropriate:

For the mirror effect, are you using some kind of tricks, like RTT? or do you use plain path tracing? If so, how many rebounds do you need for such an effect?

thx in advance, and keep on with the great job, your work makes want to try out to code one myself.

Thanks for the great comment!


The reflections are perfectly specular, so they can use a Whitted-style 'shortcut' for computational efficiency by tracing only the reflected ray. So reflections aren't path traced, but the results are the same in the case of perfect reflections. The number of bounces in the pictures is between 5 and 8 (no infinite reflections).

This is an amazing blog. I am so glad that I came across it.

Post a Comment