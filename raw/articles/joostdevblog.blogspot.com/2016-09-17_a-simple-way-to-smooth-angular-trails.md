---
title: A simple way to smooth angular trails
url: http://joostdevblog.blogspot.com/2016/09/a-simple-way-to-smooth-angular-trails.html
author: Joost van Dongen
published: '2016-09-17'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[tools for making trails](http://joostdevblog.blogspot.nl/2016/09/creating-crisper-special-effects-with.html). One problem I encountered with trails is that they often don't look very good when attached to a character. Player movement in a platformer like

[Awesomenauts](http://www.awesomenauts.com/)is not very smooth: all of a sudden you jump, or land, or turn around, and this creates a trail with lots of angles in it. For some effects this is fine, but especially for wider trails a smoother, curvier look is much better. Today I would like to discuss the smoothing algorithm I implemented to solve this.

![](../../assets/ca01234030694027.jpg)

Before I continue, here's last week's overview video of our trails again, since it also contains some footage of the smoothing:

Key when smoothing a trail is that the trail should always remain attached to the emitter (in this case a character). If the smoothing makes the trail detach from the emitter just a little bit, it starts to look floaty and incorrect. An artist can work around this by fading out the trail near its start, but this is not always desired. This makes smoothing a challenge: the emitter follows the player's angular movement but the resulting trail should not.

The trail must also look stable: it can't suddenly pop from unsmooth to smooth. The conclusion of these two requirements is that we must apply the smoothing over time instead of immediately or in one step.

The smoothing algorithm I came up with turns out to be really simple. It was inspired by how

[subdivision surfaces](https://en.wikipedia.org/wiki/Subdivision_surface)work on 3D mesh smoothing, but without the subdividing.

![](../../assets/97d4dbe676f1357e.gif)

The basic idea is this: for each segment of the trail I calculate the position in between its neighbouring segments, and then move the segment a little bit towards that centre. On a straight trail without corners this means nothing happens: the segment is already in between its neighbours. But on a corner this achieves exactly what we want: the corner moves inwards a bit, rounding the corner.

![](../../assets/44f49b9e82e0c915.gif)

By repeating this process every frame with very small steps we get a curve that over time becomes ever smoother. At first it only processes the corners, but every frame it grows to smoothen further along the straight parts as well.

![](../../assets/4ee0822c36d7a7b1.gif)

To control the smoothing I've provided our artists with two settings: one sets how strong the smoothing should be, and the other how long it should keep smoothing. If you let the smoothing take too long the trail keeps deforming and starts looking floaty and unstable. What usually works best is to use quite a strong smoothing for a very short amount of time (around 0.5 seconds). This way it stops quickly enough that the player doesn't notice significant instability.

An implementation note is that we ignore the first and last segment, since those have only one neighbour, which happens to also solve the problem that the curve needs to stay attached to the emitter. A small but important detail is that not only the first and last segment should be left out of the smoothing, but also the second and penultimate segment. This is because in my version of trails the start of the trail moves with the emitter, causing it to start really close to the second segment, which gives odd results when smoothing. Something similar happens with the final segment.

Now that I've explained how it works, here's a short video that shows the impact of the various settings that control the smoothing:

A downside of this algorithm is that the strength of the smoothing depends on the number of segments. The fewer segments there are, the stronger the effect is. This means that if an artist tweaks the number of segments after having set the smoothing, she'll need to tweak the smoothing again.

The smoothing algorithm I've described here today gets the job done, is easy to implement and costs little performance. It's nice how sometimes seemingly complex problems can have such easy solutions. :) Next week I'll discuss the texture distortion caused by deformed polygons, which is a problem for both trails and normal 2D sprites.

This is somehow incredible. Principally about Ix's movement and how smooth is all his control. You can notice too the Chucho's Bike mode. When you do arc movements to manage the fire rate at the enemies with more accurate. This is a nice job and apparently simple way to solve some roughness in movements in vectors

ReplyDeleteThis comment has been removed by the author.

ReplyDelete