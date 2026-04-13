---
title: Update on Futuristic Buildings
url: http://raytracey.blogspot.com/2011/07/update-on-futuristic-buildings.html
author: Sam Lapere
published: '2011-07-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[previous post](http://raytracey.blogspot.com/2011/07/futuristic-buildings-new-real-time-path.html): I brought back my beloved car character from Unbiased Truck Soccer. Some images (rendered blazingly fast at 16 spp per frame):

![](../../assets/214b15349fe00123.png)


![](../../assets/214b15349fe00123.png)

![](../../assets/2408e90961af6116.png)


![](../../assets/2408e90961af6116.png)

One 720p image (16 spp, almost no noise to be found):

![](../../assets/51bd658b42c1e2ee.png)


![](../../assets/51bd658b42c1e2ee.png)

I still have to create a tight fitting bounding box around the car to increase the path tracing performance (although the performance is still quite good without it). The source code of Simplex Paternitas also provides examples of rotation matrices and scripted camera animation sequences, so there are lots of cool things left to explore. The car will eventually be user controllable with a camera following the car and in contrast to my previous demos featuring the car (Unbiased Truck Soccer etc.), it will also be able to rotate instead of just translate.



UPDATE: The rotation of the car is now working. Below is a video that was rendered on my 8600M GT with only 4 samples per pixel per frame (framerate is about 5 fps at 640x480 resolution).


UPDATE: The rotation of the car is now working. Below is a video that was rendered on my 8600M GT with only 4 samples per pixel per frame (framerate is about 5 fps at 640x480 resolution).

There still isn't an acceleration structure for the car (in this case an axis aligned bounding box), which degrades the path tracing performance a little, but the code for should be done soon. After that I'm going to make the car user controllable. There's also a new 'futuristic building' which degrades performance even more, so it will need a hitbox as well:

![](../../assets/0fbebd0c53b4ce36.png)


![](../../assets/0fbebd0c53b4ce36.png)

## 2 comments:

Great progress. Sorry I've been too busy to look into things.



I'm glad there are some better frameworks around now. The TOKASPT code was not so flexible.

This seems like a much better base to start with.

Hi Kerrash!




It's been a long time indeed :-) Glad you're still following my blog.

The code of this new path tracer is indeed a lot more accessible and straightforward than tokaspt's code.

I have also been studying C++ for the past 6 weeks in my spare time, which has helped me a lot at understanding the program and writing new code. I'm adding new stuff every day now, and I've already succeeded at making the rotation of the car work. And it looks great!

Post a Comment