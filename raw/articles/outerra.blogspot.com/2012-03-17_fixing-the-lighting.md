---
title: Fixing the lighting
url: https://outerra.blogspot.com/2012/03/fixing-lighting.html
author: Outerra
published: '2012-03-17'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

While trying to find out what's the problem with ambient lighting on objects, which was making them too dark, I discovered that there's another problem with terrain lighting. Parts of the terrain that are subject to horizontal displacement were having incorrectly computed normals. For some reason the displacement effect was not affecting the terrain normal vector fully, resulting in contrast being lower than appropriate. The reason was probably a forgotten coefficient from an earlier debugging session, because when I derived the

[Jacobian](http://outerra.blogspot.com/2009/05/horizontal-displacement.html)again, there was this value of 0.5 that didn't belong anywhere.

It wasn't the first time when a surgical tool from a year-old operation was found inside our code. On the other hand, maybe one day we'll discover a hidden sleep() call and get unbelievable speedup by removing it :-)

Here are some comparison screens, old one on the left, fixed on the right side.

Another issue that was solved along the way were the artifacts on ATI cards in the shadowed areas. On ATI cards the floating point values that are output from shader may apparently end up slightly modified when written to a floating point render target, because of the blending unit. It does not matter when these values are supposed to be normal floating point values, but if the exact bit representation is important because these values are actually reinterpreted, a floating point render target cannot be used. Fortunately, the fix was easy once the reason for the artifacts was known.

Here's also the

[updated ambient lighting](http://outerra.blogspot.com/2012/03/fixing-lighting.html#ambient):

![]() |

## 1 comment:

One can only appreciate such explanations to found issues. Great work.

Post a Comment