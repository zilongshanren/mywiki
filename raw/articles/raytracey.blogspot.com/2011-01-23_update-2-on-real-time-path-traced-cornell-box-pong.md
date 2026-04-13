---
title: Update 2 on real-time path traced Cornell Box Pong
url: http://raytracey.blogspot.com/2011/01/update-2-on-real-time-path-traced.html
author: Sam Lapere
published: '2011-01-23'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I have made a simulation of the gameplay of Cornell Box Pong, running at a (simulated) 9 fps (


[click here or on the animation to see the whole thing instead of only the left half](http://img13.imageshack.us/img13/4457/pongsimulation1.gif)):![](http://img13.imageshack.us/img13/4457/pongsimulation1.gif)


![](http://img13.imageshack.us/img13/4457/pongsimulation1.gif)

This is the quality that could be expected in real-time (10 fps) when running on a high-end Fermi card (GTX 480, 570, 580). Notice the color bleeding from the green and red wall on the white spheres, the yellow ball is reflected in the paddles and refracted in the glass sphere in front. I could also animate the spheres in the background to show off the color bleeding even better and the side or back walls could change color during gameplay to add a nice visual effect (e.g. when the pong ball hits one of the side walls), the paddles could emit light when bouncing the ball back, etc... The goal is to make a very simple game, with simple geometry but with real-time, fully dynamic, photorealistic lighting demonstrating ultrahigh-quality dynamic GI effects only possible with real-time path tracing.


These are the frames making up the animation in full "simulated real-time"quality (rendered for about 3 seconds on my laptop with GeForce 8600GT M, should render in less then 100 milliseconds on a GTX580):


These are the frames making up the animation in full "simulated real-time"quality (rendered for about 3 seconds on my laptop with GeForce 8600GT M, should render in less then 100 milliseconds on a GTX580):

![](../../assets/6f4a7f95934a790c.png)


![](../../assets/6f4a7f95934a790c.png)

![](../../assets/ab0d43938eef15dc.png)


![](../../assets/ab0d43938eef15dc.png)

![](../../assets/555c29035d2e5757.png)


![](../../assets/555c29035d2e5757.png)

![](../../assets/12d8586796c4bfc8.png)


![](../../assets/12d8586796c4bfc8.png)

![](../../assets/ee368d59ec758f80.png)


![](../../assets/ee368d59ec758f80.png)

![](../../assets/4395c97c8fa36480.png)


![](../../assets/4395c97c8fa36480.png)

![](../../assets/bcb9b2969b515e40.png)


![](../../assets/bcb9b2969b515e40.png)

![](../../assets/f9743f3b91615579.png)


![](../../assets/f9743f3b91615579.png)

![](../../assets/a744732917bea5bf.png)


![](../../assets/a744732917bea5bf.png)

![](../../assets/219bdbcf9f067e3f.png)


![](../../assets/219bdbcf9f067e3f.png)

![](../../assets/03a3e0d1442d2c69.png)


![](../../assets/03a3e0d1442d2c69.png)

![](../../assets/716ef86e001b191a.png)


![](../../assets/716ef86e001b191a.png)

![](../../assets/37248b2f6982996b.png)


![](../../assets/37248b2f6982996b.png)

![](../../assets/928d9618c5367114.png)


![](../../assets/928d9618c5367114.png)

## 2 comments:

I'd probably agree that axis aligned plane intersections would likely be quicker than sphere-ray intersections. I've seen the difference myself in my own physics routines.



Perhaps a combination of both, planes for the walls balls for the paddles (and ball :) ). I Kinda of like the look of the round paddles.

Typically the old game deflects the ball differently based on the position it hits the paddle, spheres would help to show this better.

Thanks for the comment, I also think that spherical paddles are easier to predict in which direction the ball will bounce back. I hope I can develop this further, but I have a lot of work with my totally unrelated PhD right now ;)

Post a Comment