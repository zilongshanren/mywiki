---
title: A retrospective on Call of Duty rendering
url: http://c0de517e.blogspot.com/2016/08/a-retrospective-on-call-of-duty.html
published: '2016-08-28'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[In my last post I did a quick recap of the research Activision published at Siggraph 2016](http://c0de517e.blogspot.ca/2016/08/activision-siggraph-2016.html). As I already broke my long-standing tradition of never mentioning the company I work for on my blog, I guess it wouldn't hurt, for completeness sake, to do a short "retrospective" of sorts, recapping some of the research published about the past few Call of Duty titles.

*I'll to remark, my opinion on the blog is as always personal, and my understanding of COD is very partial as I don't sit in production for any of the games.*

I think COD doesn't often do a lot of "marketing" of its technology compared to other games, and I guess it makes sense for a title that sells so many copies to focus its marketing elsewhere and not pander to us hardcore technical nerds, I love the work Activision does on the trailers in general (if you haven't seen the live-action ones, you're missing out), but still it's a shame that very few people consider what tricks come into play when you have

[a 60hz first person shooter on ps3](http://www.eurogamer.net/articles/digitalfoundry-face-off-modern-warfare-3).
Certainly, -I- didn't! But my relationship with COD is also kinda odd, I was fairly unaware/uninterested in it till someone lent me the DVD I think of MW2 for 360 a long time after release, and from there I binge-played MW1 and Black Ops... Strictly single-player, mostly for their -great- cinematic atmosphere (COD MW2 is probably my favorite in that regard of previous-gen, together with Red Dead Redemption), and never really trying to dissect their rendering.


*By the way, if you missed on COD single player, I think*[this critique](https://www.youtube.com/watch?v=AvN51r1o1Nc)of the campaign over the various titles is outstanding, worth your time.
Thing is, most games near the end of the 360/ps3 era went on to adopt new

[deferred rendering systems](http://c0de517e.blogspot.ca/2016/08/the-real-time-rendering-continuum.html), often without, in my opinion, having[solid reasons](http://c0de517e.blogspot.ca/2011/01/mythbuster-deferred-rendering.html)to do so.
COD instead stayed on a "simple" single-pass forward rendering, mostly with a single analytic light per object.

Not much to talk about at Siggraph there (

Not much to talk about at Siggraph there (

[with some exceptions](http://blog.selfshadow.com/publications/s2013-shading-course/)), but with a great focus on mastering that rendering system: aggressive mesh splitting per lights and materials (texture layer groups), an engine -very- optimized to emit lots of drawcalls, and lightmapped GI (which manages to be quite a bit better than most of[no-GI many-light deferred engines of the time](http://c0de517e.blogspot.ca/2012/10/notes-on-optimizing-deferred-renderer.html)).
![]() |

IMHO a lesson on picking the right battles and mastering a craft, before trying to add a lot of kitchen-sink features without much reasoning, which is always very difficult to balance in rendering (we all want to push more "stuff" in our engines, even when it's actually detrimental, as all unneeded complexity is).

**Call of Duty: Ghosts**

The way I see Ghosts is as a transition title. It's the first COD to ship on next-gen consoles, but it still had to

[be strong on current-gen](http://www.eurogamer.net/articles/digitalfoundry-call-of-duty-ghosts-face-off), which is to be expected for a franchise that needs a large install base to be able to hit the numbers it hits.
Developers now had consoles with lots more power, but still had to take care of asset production for the "previous" generation while figuring out what to do with all the newfound computational resources.

For Ghosts, Infinity Ward pushed a lot on the geometrical detail rather than doing much more computation per pixel and that makes sense as it's easier to "scale" geometry than it is to fit expensive rendering systems on previous-gen consoles. This came with two main innovations: hardware displacement mapping and hardware subdivision (Catmull-Clark) surfaces.





Both technologies were a considerable R&D endeavor and were presented at

[Siggraph](http://advances.realtimerendering.com/s2014/wade/siggraph_2014_tessellation_in_call_of_duty_ghosts.pdf),[GDC](http://www.gdcvault.com/play/1020252/Advanced-Visual-Effects-with-DirectX)and in GPU Pro 7.
Albeit both are quite well known and researched, neither was widely deployed on console titles, and the current design of the hardware tessellator on GPUs is of limited utility, especially for displacement, as it's impossible to create subdivision patterns that match well the frequency detail of the heightmaps (





[this is currently, afaik, the state-of-the-art](http://www.labri.fr/perso/guenneba/publi/MultiResMeshes4HWTess_EG2016.pdf), but doesn't map to tiled and layered displacement for world detail).
Wade Brainerd recently presented with Tim Foley et al. some quite substantial improvements

[for hardware Catmull-Clark surfaces](http://www.graphics.stanford.edu/~niessner/papers/2016/4subdiv/brainerd2016efficient.pdf)and made a proposal for a better hardware tessellation scheme at this years'[Open Problems in Computer Graphics](http://openproblems.realtimerendering.com/s2016/index.html).
![]() |

For the rest, Ghosts is still based on mesh-splitting single-pass forward shading, and non-physically based models (Phong, that the artists were very familiar with).

Personally, I have to say that IW's artists did pull the look together and I Ghosts can look very pretty, but, in general, the very "hand-painted" and color-graded look is not the art style I prefer.

**Call of Duty: Advanced Warfare**

Advanced Warfare is the first COD to have its production completely unrestricted by "previous-gen" consoles, and compared to Ghosts it takes an approach that is almost a complete opposite, spending much more resources per pixel, with a completely new lighting/shading/rendering system.

At its core is still a forward renderer but now capable of doing many lights per surface, with physically based shaders. It does even more "mesh splits" (thus more drawcalls) and generates a huge amount of shader permutations to specialize rendering exactly for what's needed by a given piece of geometry (shadows, lighting, texturing and so on...).

[We did quite a bit of research on the fundamental math of PBR](http://c0de517e.blogspot.ca/2016/07/siggraph-2015-notes-for-approximate.html)for it and it employs an entirely new lightmap baking pipeline, but where it really makes a huge difference, in my opinion, is not on the rendering engine per se, but on its keen dedication to perceptual realism.

It's a physically based renderer done "right": doing PBR math right is relatively "easy", teaching PBR authoring to artists is much harder (arguably, not something that can be done over a single product, even) but making sure that everything makes (perceptual) sense is where the real deal is, and

[Sledgehammer's attitude during the project was just perfect](http://blog.selfshadow.com/publications/s2015-shading-course/chan/s2015_pbs_cod_aw_notes.pdf).
Math and technology of course matter, and checking the math against

[ground-truth simulations is very important](http://c0de517e.blogspot.ca/2016/07/siggraph-2015-notes-for-approximate.html), but you can do a perfectly realistic game with empirical math and proper understanding of how to validate (or fit) your art against real-world reference, and you can do on the other hand a completely "wrong" rendering out of perfectly accurate math...
![]() |

Things make sense, they are overall in the right brightness ratios

Advanced Warfare did also many other innovations, Jorge Jimenez authored

[a wonderful post-effect pipeline](http://www.iryoku.com/next-generation-post-processing-in-call-of-duty-advanced-warfare)(he really doesn't do anything if it's not better than state of the art!) and AW also took a new version of

[our perpetually improving performance capture](http://ict.usc.edu/pubs/Digial%20Ira%20and%20Beyond%20-%20Creating%20Photoreal%20Real-Time%20Digital%20Characters%20(course%20notes).pdf)(and

[face rendering](http://www.iryoku.com/stare-into-the-future)) technology, developed in collaboration with

[ICT](http://ict.usc.edu/).

But I don't think that any single piece of technology mattered for AW more than the studio's focus on perceptual realism as a rendering goal. And I love it!

**Call of Duty: Black Ops 3**

I won't talk much about Black Ops 3, also because I already did a post on Siggraph 2016 where we presented lots of rendering innovations done during the previous few years.

The only presentation I'd like to add here, which is a bit unrelated to rendering, is this one: showing

The only presentation I'd like to add here, which is a bit unrelated to rendering, is this one: showing

[how to fight latency by tweaking animations](http://www.gdcvault.com/play/1022943/Fighting-Latency-on-Call-of).
Personally I think that if Sledgehammer's COD is great in its laser focus on going very deep exploring a single objective, Black Ops 3 is just crazy. Treyarch is crazy! Never before I've seen so many rendering improvements pushed on such a large, important franchise. Thus I wouldn't know really where to start...

BO3 notably switched





[from forward to deferred](http://www.dualshockers.com/2015/09/03/call-of-duty-black-ops-iii-design-director-talks-graphics-ps4-and-xbox-one-controllers-and-more/), but I'd say that most of what's on screen is new, both in terms of being coded from scratch and often times also in terms of being novel research, and even behind the scenes lots of things changed, tools, editors, even the way it bakes GI is completely unique and novel.
If I had to pick I guess I can narrow BO3 rendering philosophy down to

[unification](https://community.treyarch.com/t5/Treyarch/Engineer-s-Roundtable/ba-p/9937090)and productivity. Everything is lit uniformly, from particles to volumetrics to meshes, there are a lot less "rendering paths" and most of the systems are easier to author for.
All this sums up to a very coherent rendering quality across the screen, it's impossible to tell dynamic objects from static ones for example, and there are very few light leaks, even on specular lighting (which is quite hard to occlude).

Stylistically I'd say, to my eyes, it's somewhere in between AW and Ghosts. It's not quite as arbitrarily painted as Ghosts, and it is a PBR renderer done paying attention to its accuracy, but the data is quite more liberally art directed, and the final rendered frames lean more towards a filmic depiction than close adherence to perceptual realism.

**Call of Duty: Infinite Warfare**

...is not out yet, and I won't talk about its rendering at all, of course!

It's quite impressive though to see how much space each studio has to completely tailor their rendering solutions to each game, year after year. COD is no

[Dreams](http://www.mediamolecule.com/blog/article/siggraph_2015), but compared to titles of similar scope, I'd say it's very agile.
So rest assured, it's yet again quite radically different than what was done before, and it packs quite a few cute tricks... I can't imagine that most of them won't appear at a Siggraph or GDC, till then, you can try to guess what it's trying to accomplish, and how, from the trailers!




Three years, three titles, three different rendering systems, crafted for specific visual goals and specific production needs. The Call of Duty engines don't even have a name (not even internally!), but a bunch of very talented, pragmatic people with very few artificial constraints put on what they can change and how.

Three years, three titles, three different rendering systems, crafted for specific visual goals and specific production needs. The Call of Duty engines don't even have a name (not even internally!), but a bunch of very talented, pragmatic people with very few artificial constraints put on what they can change and how.

## 1 comment:

My favorite game till now, and they have come up with the New ‘Call of Duty: Black Ops 4’ season look so cool cant wait to play

Post a Comment