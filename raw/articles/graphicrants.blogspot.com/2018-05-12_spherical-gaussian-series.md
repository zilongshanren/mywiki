---
title: Spherical Gaussian series
url: http://graphicrants.blogspot.com/2018/05/spherical-gaussian-series.html
author: Brian Karis
published: '2018-05-12'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

### Intro and backstory

About 4 years ago now I ran into Spherical Gaussian (SG) math in a few different publications in a row, enough that it triggered the pattern detection in my brain. All were using SGs to approximate specular lobes. I remember feeling very similar 10 years prior when Spherical Harmonics were starting to become all the rage. Back with SH I noticed it fairly early, primarily from Tom Forsyth's slides on the topic and took the time to dig into the math and make sure I had this new useful thing in my toolbox. Doing so has proven to be well worth the time. I decided that I should do the same again and learn SGs and related math, in particular to build up a toolbox of operations I can do with them. Maybe it would prove as useful as SH has.In the years since I'd say it has certainly been worth the effort. I don't think I can say it has proven as useful as SH has been to computer graphics but it was still worth learning. I intended to write up what I had found and share the toolbox of equations compiled in a centralized place at the very least. Unfortunately laziness and procrastination got in the way.

Also scope creep. About 3 years ago I mentioned to David Neubelt that I intended to write this up and he too had done a lot of work with SGs at Ready at Dawn so we decided we'd collaborate and write a joint paper and submit it to JCGT. The intention was to make something similar to

[Stupid Spherical Harmonics (SH) Tricks](https://www.ppsloan.org/publications/StupidSH36.pdf)but for SG. That scope and seriousness is much larger than a simple single author blog post. We worked on derivations to all the formulas, wanted to have quality solutions to cube map fitting, multiple use cases proven in production, and a ton of other things to make it an exhaustive, professional, and ultimately great paper. This was much more than I ever intended as a simple blog post. I still think that paper we had in mind would be great to exist but the actual end result is it bloated the expectation of what either of us had the bandwidth or maybe the attention span to complete and after a couple of months of work the unfinished paper regretfully stagnated.

A year went by and eventually MJP of Ready at Dawn did in fact do

[a blog series write up on Spherical Gaussians](https://mynameismjp.wordpress.com/2016/10/09/new-blog-series-lightmap-baking-and-spherical-gaussians/). It is excellent and I suggest you read it before continuing if you haven't already. There are still some things I intended to cover that he did not as well as things he did that I never have done nor planned to cover so I think these should compliment each other well.

It is a royal shame I have not posted this in the 3+ years since I intended to. I had even promised folks publicly a write up was coming and then didn't deliver. I haven't posted anything on this blog since then in fact. I hope to do better and hopefully finally getting this out will unclog the pipes.

Without further ado,

- Part 1 -
[Spherical Gaussians](https://graphicrants.blogspot.com/2018/05/spherical-gaussians-part-1.html) - Part 2 -
[von Mises-Fisher](https://graphicrants.blogspot.com/2018/05/von-mises-fisher-part-2.html) - Part 3 -
[Normal map filtering using vMF](https://graphicrants.blogspot.com/2018/05/normal-map-filtering-using-vmf-part-3.html) - Part 4 - Coming soon...

## No comments:

Post a Comment