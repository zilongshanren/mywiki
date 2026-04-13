---
title: iCEnhanced Brigade screenshots (1)
url: http://raytracey.blogspot.com/2012/09/brigade-new-screenshots.html
author: Sam Lapere
published: '2012-09-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The aim is to make a game with this scene, some of the gameplay ideas include a small toy car or plane that you can navigate through the scene or an action packed Heavy Rain like game. Or even some physics cubes destroying the scene similar to this photoreal animation (rendered with Octane):

## 12 comments:

Sam, these look phenomenal, and are a true testament to the visual quality that unbiased renderers bring to the table. Although light propagation can be simulated relatively well with simple tricks in other RT schemes or rasterization, they lack that certain something that makes them look real. Shots like this really showcase the difference that ground-truth makes to the quality of a rendered scene. That these are real-time is simply astounding.




I'm really liking what I see coming out of OTOY. I'm also really liking the incredible gains by ImgTec with their OpenRL hardware.

Soon, it seems that the entire field of computer science behind realtime rendering will soon come to a screeching halt (or at least be reduced to a slow crawl) when these engines start to infiltrate the mainstream. Having followed the scene for quite a while, and as a later comer, it's exhilarating to see what is now possible, and a little sad that the race is mostly over.

Oh, and the game you describe really reminds me of an old Dreamcast game called "Toy Commander"! It may be worth checking out via youtube.

Thanks Sean, I appreciate this very much. It's also great to see you back. What Hayssam did with Brigade is really amazing, I can hardly believe it myself sometimes.






The nice thing about Brigade and Octane is that these technologies unify the worlds of offline and realtime rendering and both represent the final stage in computer graphics.

About ImgTec/OpenRL: it was nice to finally see some actual working ray tracing hardware. I was afraid it was going to become a second Larrabee fiasco, but they actually succeeded :)

Toy Commander indeed looks very much like what I had in mind :)

Is this the current realtime quality of the iCEnhanced, or the shots still needed some noticeable time to converge?

nice! I screenshot with the lights, are they IES lights? It would be really cool to support IES Lights in Brigade, especially for interior walk thrus.

:) I never really went anywhere. I've always kept up to date with your posts. I'm a late-comer to the world of Real-time Graphics Research (despite being a long-time observer), but my skills are increasing rapidly, and I'm sure I will contribute soon... Well, soon-ish anyhow! :) My time socializing on the web ended up eating much of my time, and I cut back on this very aggressively, so that I could produce more work.




I think you're spot on re: Brigade and Octane being the final stages for rendering. Of course there are still frontiers for real-time rendering, and even some unbiased techniques worth exploration (eg. http://zurich.disneyresearch.com/~wjarosz/publications/novak12vbls.html), but the need for approximate simulations of physical phenomena will dry up overnight!

I was also really pleased to see ImgTec's hardware! I didn't doubt their ingenuity (they seem like a

verycompetent bunch), and I know that they had mentioned that they had been working on this for some time, but I didn't expect to see it quite so soon! What interests me is that ImgTec traditional produces mobile parts, and they have boldly stated that their RT hardware will likely move into mobile devices in the not-too-distant future. With that level of implied die-area/power-consumptive efficiency both cloud and mobile infrastructure can benefit greatly. I'm curious if their aim is just competent OpenRL hardware destined for stationary machines to be ported to mobiles as dies shrink, or if the hardware is being designed to fit on small dies and tie in with the ever-popular OpenGL hardware. Regardless, it's extremely exciting, and it is a fine showcase of their business acumen and vision!I'm stoked to see Hayssam's art, and really excited by what comes next! Just make sure that we're the first to know when OTOY releases its first Brigade/Cloud demo for public consumption! ;)

"approximate simulations of physical phenomena"



Just to clarify, I'm referring to light. I'm sure that many types of physical simulation still have a very hearty future!

And who knows? Perhaps if multi-view glasses-free holographics become a serious thing, it may provide many new challenges for realtime rendering...

Hi sam, the screenshots are impressive, I'd like to ask, these enhancements are steroids ( not coming out of a physically accurate process, but there just for beautification reasons ) or real enhancements (?) to the path tracing algorithm of brigade which did not exist before ( missing features ) ?

Dima, wait for the vids ;)





Anonymous, no Brigade doesn't support IES lights, Octane does though and they are indeed awesome for architectural walkthroughs.

Sean,rest assured, you'll see the most exciting Brigade related stuff right here.

btw, added a new screenshot in the post

Mirror, some subtle effects are done in post by icelaglace, but depth of field and everything else is path traced in real-time

You'd probably be interested in this: http://advances.realtimerendering.com/s2012/Epic/The%20Technology%20Behind%20the%20Elemental%20Demo%2016x9.pptx



It's not true unbiased rendering, since it's actually cone tracing over a voxelized representation of the scene, but it can do true glossy reflections and single (at least) bounce global illumination in fully dynamic scenes. Since this is the demo for a major game engine (Unreal Engine 4), it will also almost certainly end up in various games.

Looking at the technique, it could very likely be extended to include refractions and multibounce global illumination with caustics, simply by ensuring the voxels contain normals and material information.

@Sam Lapere



"About ImgTec/OpenRL: it was nice to finally see some actual working ray tracing hardware"

what working ray tracing hardware is that exactly? Where did you get that info from?

u guys r crazy :O


keep it up !!

Post a Comment