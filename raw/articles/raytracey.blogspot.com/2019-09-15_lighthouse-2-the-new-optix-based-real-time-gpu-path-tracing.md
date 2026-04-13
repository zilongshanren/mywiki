---
title: LightHouse 2, the new OptiX based real-time GPU path tracing framework, released
  as open source
url: http://raytracey.blogspot.com/2019/09/lighthouse-2-new-optix-based-real-time.html
author: Sam Lapere
published: '2019-09-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

If you haven't heard of Jacco Bikker before, he is the original author of the Brigade engine, which pioneered the use of real-time path tracing in games (way before Nvidia got interested) and was released as open source in 2010 (see


Brigade was a real trailblazer and showed off a glimpse of what photorealistic games could look like in a not so distant future. Brigade 2, its successor (and also developed by Jacco Bikker) was fully GPU based which pushed performance to another level.


As I used to work a lot with Brigade and designed many tech demos with the engine for this blog (see for example

[https://raytracey.blogspot.com/2010/04/real-time-pathtracing-demo-shows-future.html](https://raytracey.blogspot.com/2010/04/real-time-pathtracing-demo-shows-future.html)).Brigade was a real trailblazer and showed off a glimpse of what photorealistic games could look like in a not so distant future. Brigade 2, its successor (and also developed by Jacco Bikker) was fully GPU based which pushed performance to another level.

As I used to work a lot with Brigade and designed many tech demos with the engine for this blog (see for example

[https://raytracey.blogspot.com/2013/03/real-time-path-traced-carmageddon.html](https://raytracey.blogspot.com/2013/03/real-time-path-traced-carmageddon.html)and[https://raytracey.blogspot.com/2013/10/brigade-3.html](https://raytracey.blogspot.com/2013/10/brigade-3.html)), I was quite thrilled to read that Jacco released a new path tracing engine which fully exploits OptiX and the new hardware accelerated RTX ray tracing cores on Nvidia's Turing GPUs.
The Lighthouse engine has a couple of unique features:

- Lighthouse uses Nvidia's OptiX framework, which provides state-of-the-art methods to build and traverse BVH acceleration structures, including a built-in "top level BVH" which allows for real-time animated scenes with thousands of individual meshes, practically for free.
- There are 3 manually optimised OptiX render cores:
- OptiX 5 (for Maxwell and Pascal GPUs)
- OptiX Prime (for Maxwell and Pascal GPUs)
- OptiX 7 (with full RTX support for Turing GPUs)
- OptiX 7 is much more low level than previous OptiX versions, creating more control for the developer, less overhead and a substantial performance boost on Turing GPUs compared to OptiX 5/6 (about 35%)
- A Turing GPU running Lighthouse 2 with OptiX 7 (with RTX support) is
__about 6x faster__than a Pascal GPU running OptiX 5 for path tracing (you have to try it to believe it :-) ) - Lighthouse incorporates the new "blue noise" sampling method (
[https://eheitzresearch.wordpress.com/762-2/](https://eheitzresearch.wordpress.com/762-2/)), which creates cleaner/less noisy looking images at low sample rates - Lighthouse manages a full game scene graph with instances, camera, lights and materials, including the Disney BRDF (the so-called "principled" shader) and their parameters can be edited on-the-fly through a lightweight GUI

Some screenshots (rendered with Lighthouse's OptiX 7 core on a RTX 2060)

![]() |

![]() |

![]() |

![]() |

![]() |

Lighthouse is still a work in progress, but due to its relative simplicity it's easy to quickly test a new sampling algorithm or experiment with a new fast denoiser, ensuring the code and performance remains on par with the state-of-the-art in rendering research.

Given the fact that it handles real-time animation, offers state-of-the-art performance and is licensed under Apache 2.0, Lighthouse 2 may soon end up in professional 3D tools like Blender for fast, photorealistic previews of real-time animations. Next-gen game engine developers should also keep an eye on this.

Stay tuned for more™ !






P.S. I may release some executable demos for people who can't compile Lighthouse on their machines.

### Useful links

- Lighthouse 2 code on Github:
[https://github.com/jbikker/lighthouse2](https://github.com/jbikker/lighthouse2) - Lighthouse 2 wiki:
[https://github.com/jbikker/lighthouse2/wiki](https://github.com/jbikker/lighthouse2/wiki)(early stages) - Lighthouse 2 forum:
[https://ompf2.com/viewforum.php?f=18](https://ompf2.com/viewforum.php?f=18)

P.S. I may release some executable demos for people who can't compile Lighthouse on their machines.

## No comments:

Post a Comment