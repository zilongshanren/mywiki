---
title: The Devil Is In the Details
url: http://hacksoflife.blogspot.com/2010/01/devil-is-in-details.html
author: Benjamin Supnik
published: '2010-01-29'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Stack Overflow](http://stackoverflow.com/). It makes sense, but I just feel a compulsion to answer other people's questions about OpenGL.

But there is one kind of question that drives me a little bit nutty...it goes like this:

I am new to OpenGL and I hope someone can help me. I am drawing a series of interlocking mobeus rings using glu nurb tessellateors, GL_TEX_ENV_COMBINE, a custom separate alpha blending mode, the stencil buffer, and polygon offset.My fellow OpenGL programmers: Stack Overflow is not a debugging service.

For some reason one of my polygons are clipped. If I change the combine mode to add, the purple ones move to the left. If I change the polygon offset, the problem persists.

Any ideas?

Stack Overflow is a great idea, and the site execution is really pretty good: automatic syntax formatting appropriate to code, tagging, search works pretty well. It is good for answering questions.

But a post like the above: it's not a question, it's a cry for help. (The answer, technically, is "yes", but I don't want to post that and get bad karma.) There are about a million things that could be going wrong from the fundamental design to the nuts and bolts.

In my experience, OpenGL bugs fall into three categories:

There is a one-off stupid mistake deep in the implementation that causes all hell to come down. Fixing the bug requires the usual techniques (

[divide and conquer and printf](http://hacksoflife.blogspot.com/2010/01/debugging-glsl.html)) until the bug is found and fixed. Stack crawl is not the right tool - any programmer who is going to fix this needs to be able to modify and re-run the app repeatedly, and no one is going to do this for you for free anyway.The overall algorithm design is wrong because of the design limits of the GL. Another programmer could at leaset

*tell*you that you have this problem, but only if you know enough to ask the right questions. And if you know enough to ask, heck, you probably wouldn't have designed the code this way in the first place.The GL implementation has a known bug. This is the one case where stack crawl can help, but the above question is not that. The programmer needs to have cut the problem all the way down to the one mysterious behavior (e.g. my color is showing up in one of my vertex attributes but the GL spec says

[this should not happen](http://hacksoflife.blogspot.com/2010/01/ive-got-blues.html)). In this case, at least having confirmation from other programmers that the bug is really in library code helps provide closure to the investigation.

Enough blogging, I'm going to go back to being grumpy now.

I agree wholeheartedly. It's not grumpy to try to keep up the spirit of StackOverflow which has always been about asking answerable technical questions that have definite answers; a site that we'll hit most of the time when we google an obscure library API or whatever.


ReplyDeleteThe community wiki ruins it imho, and the tolerance of open questions.

It does bring up an interesting social networking question...which is more important: the "openness" of the community (if a SO moderator came in and said "That's a stupid question" to new users all the time, the site would probably not survive) vs. the importance of enforcing community standards...

ReplyDelete