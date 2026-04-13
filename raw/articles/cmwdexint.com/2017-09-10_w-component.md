---
title: w component
url: https://cmwdexint.com/2017/09/10/w-component/
author: Ming Wai Chan
published: '2017-09-10'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

I have been so confusing about the w component for ages, until I read this:

[Explaining Homogeneous Coordinates & Projective Geometry](http://www.tomdalling.com/blog/modern-opengl/explaining-homogenous-coordinates-and-projective-geometry/)

So I quickly made a simple to shader to test it out:

![20170910](../../assets/4503d89ead69e055.gif)


To summarize, w component is the

The

dimension is the distance from the projector to the screen(object).

when w > 1, the object looks far (smaller)

when w = 1, the size remains the same

when w = 0, it’s actually covering the whole screen

This is the reason why we have make sure the w component is correct when we are doing **_Object2World** and **_World2Object**

Also a interesting point to note from the blog post:

If

, then it is a point light. If , then it is a directional light.

###### (Thanks Kemal for the tutorial links!)