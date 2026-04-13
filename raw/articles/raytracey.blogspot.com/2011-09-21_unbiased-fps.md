---
title: Unbiased FPS
url: http://raytracey.blogspot.com/2011/09/unbiased-fps.html
author: Sam Lapere
published: '2011-09-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/e90eda5af8a4e9f2.png)


![](../../assets/e90eda5af8a4e9f2.png)

4spp, reusing samples from the previous 6 frames, 720p resolution:

![](../../assets/9543a111d3779e58.png)


![](../../assets/9543a111d3779e58.png)

720p resolution, 4spp with 12 averaged frames (reusing samples from the previous 12 frames, resulting in heavy blur for moving objects, but crisp image quality for the rest of the scene):

![](../../assets/bb6a493d9d1d4730.png)


![](../../assets/bb6a493d9d1d4730.png)

![](../../assets/ab1abad561543b60.png)


![](../../assets/ab1abad561543b60.png)

Some features:

- a first person "gun" sticks to the camera and shoots chrome balls with physical weight

- mouse look is semi-functional, you can move the mouse cursor up to the borders of the screen

- the car can be controlled with the arrow keys

- the robot has an initial angular momentum, but essentially does nothing

- the camera is controlled with mouse + WASD keys (the classic FPS controls)

- the number of averaged frames can now be set with a slider (from 0 to 12). It regulates the amount of "blur" caused by reusing samples from previous frames and is very useful for comparison purposes. Setting the slider to 1 or higher greatly reduces the amount of noise at the expense of a more blurry image and doesn't have any impact on the framerate. You can for example quadruple the number of samples per pixel (thereby halving the amount of noise) for free and if the framerate is high enough, the blurring isn't even that distracting. Setting the slider to 12 with just 4 spp results in a very high quality image (effectively more than 100 spp) at high framerates, but at the expense of lots of motion blur when the car or camera are moving


There are no acceleration structures used (not even a bounding box around the car or the robot). Implementing those should give a nice ray tracing performance boost.


There are no acceleration structures used (not even a bounding box around the car or the robot). Implementing those should give a nice ray tracing performance boost.

## No comments:

Post a Comment