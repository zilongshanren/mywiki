---
title: The Smell of Victory
url: http://hacksoflife.blogspot.com/2013/07/the-smell-of-victory.html
author: Benjamin Supnik
published: '2013-07-22'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

You might think the primary purpose of X-Plane is to help people enjoy the experience of flight at home, or to help pilots train for real-world situations. You would be wrong.


X-Plane's real purpose is to slowly drive the last traces of sanity out of OpenGL driver-writer's already deep-fried minds. X-Plane is joined in this noble calling by a legion of other sometimes-badly-behaved legacy applications that are shot through with conditional logic based on random OS and driver versions.


And you know...I think we're winning. From comment 9 of


X-Plane's real purpose is to slowly drive the last traces of sanity out of OpenGL driver-writer's already deep-fried minds. X-Plane is joined in this noble calling by a legion of other sometimes-badly-behaved legacy applications that are shot through with conditional logic based on random OS and driver versions.

And you know...I think we're winning. From comment 9 of

[GL_ARB_buffer_storage](http://www.opengl.org/registry/specs/ARB/buffer_storage.txt)(just released as part of Core OpenGL 4.4):I would like to suggest to the ARB that, in the future, they name the hints things like GL_REALLY_FAST_BIT and GL_NO_REALLY_THIS_BUFFER_NEEDS_TO_BE_FAST_BIT. You guys are going to ignore the hint bits anyway; the hint bits might as well directly express what we are trying to code.9) What is the meaning of CLIENT_STORAGE_BIT? Is it one of those silly hint things? DISCUSSION: Unfortunately, yes, it is. For some platforms, such as UMA systems, it's irrelevant and all memory is both server and client accessible. The issue is, that on some platforms and for certain combinations of flags, there may be multiple regions of memory that can satisfy the request (visible to both server and client and coherent to both, for example), but may have substantially different performance characteristics for access from either. This bit essentially serves as a hint to say that that an application will access the store more frequently from the client than from the server. In practice, applications will still get it wrong (like setting it all the time or never setting it at all, for example), implementations will still have to second guess applications and end up full of heuristics to figure out where to put data and gobs of code to move things around based on what applications do, and eventually it'll make no difference whether applications set it or not. But hey, we tried.

...or GL_TRUST_ME_I_KNOW_WHAT_I_AM_DOING_BIT :D

ReplyDelete