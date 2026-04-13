---
title: Hidden Costs
url: https://blog.selfshadow.com/2011/10/01/hidden-costs/
author: Stephen Hill
published: '2011-10-01'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

I recently added two of my existing publications, one about high performance [dynamic visibility](https://blog.selfshadow.com/publications/practical-visibility/) and the other on how to display [pixel quad overshading](https://blog.selfshadow.com/publications/overdraw-in-overdrive/) in real-time on Xbox 360.

The first of these was originally published in [GPU Pro 2](http://downloads.akpeters.com/gpupro/). Unfortunately, I missed some errors that crept into the typeset version, so I was pleased to finally correct those and I took the opportunity to rework a few sentences for greater clarity as well. Now that it’s online, I’ll also be able to refer directly to certain sections in follow-up blog posts on the subject.

The second took the form of a journal entry for the Microsoft Game Developer Network, which went up in the spring. It may have flown under your radar, as I’ve since spoken to a few developers who hadn’t seen it, yet were keen to have such a tool in their engine. For NDA reasons, I can’t go into all of the implementation details here, so think of it as a ‘graphical appetiser’.

In a way, the two topics are related: the primary goal of a visibility system is to efficiently remove parts of the world that can’t be seen from a given viewpoint, whereas the purpose of a debug *overshading* mode is to directly visualise pixel shader work, some of which can likewise have zero contribution to the final image.

I think it’s also fair to say that keeping both forms of redundancy in check is a critical part of optimising the rendering performance of most AAA titles. For that reason, I hope you find these articles useful, and as always, please let me know what you think!