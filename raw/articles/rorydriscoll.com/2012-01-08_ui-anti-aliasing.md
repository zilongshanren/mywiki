---
title: UI Anti-Aliasing
url: https://www.rorydriscoll.com/2012/01/08/ui-anti-aliasing/
author: Rory
published: '2012-01-08'
source_blog: CodeItNow
source_site: https://www.rorydriscoll.com
category: graphics
fetched: '2026-04-13'
---

I’ve been working on making a really simple IMGUI implementation for my engine at home. I like to do a little bit of research when I’m approaching something new to me like this, so I went hunting around for publicly available implementations. While doing this, I came across [Mikko Mononen’s](http://digestingduck.blogspot.com/) implementation in [Recast](http://code.google.com/p/recastnavigation/).

I was impressed when I ran the demo with how smooth his UI looked. It turns out that he’s using a little trick (which I’d never seen before, but I’m sure is old to many) to smooth of the edges of his UI elements.

Basically, the trick is to create a ring of extra vertices by extruding the edges of the polygon out by a certain amount. These extra vertices take the same color as the originals, but their alpha is set to zero. Mikko calls this ‘feathering’.

In my case, I found that I got good results by feathering just one pixel. Here’s a quick before/after comparison of the my IMGUI check box at 800% zoom:

And here’s a 1-to-1 example showing rounded button corners:

It’s a pretty nice improvement for a very simple technique! If you’re interested in what the code looks like, then either take a look at [Mikko’s IMGUI implementation](http://code.google.com/p/recastnavigation/source/browse/trunk/RecastDemo/Source/imgui.cpp?r=213), or you can find the code I use to feather my convex polygons below.

My implementation is a little less efficient since I recalculate each edge normal twice, but I chose to keep it simple for readability.

[…] path to get an approximation of pixel coverage on each pixel. This technique is mentioned in the CodeItNow blog. The problem with this technique is that shapes are slightly […]