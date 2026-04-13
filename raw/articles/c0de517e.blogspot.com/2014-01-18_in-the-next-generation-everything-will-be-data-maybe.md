---
title: In the next-generation everything will be data (maybe)
url: http://c0de517e.blogspot.com/2014/01/in-next-generation-everything-will-be.html
published: '2014-01-18'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*I've just finished sketching a slide deck on data... stuff. And I remembered I had a half-finished post on my blog tangentially related to that, so I guess it's time to finish it. Oh. Oh. I didn't remember it was rambling so much. Brace yourself...*



**Rant on technology and games.**

Computers, computing is truly revolutionary. Every technological advance has been incredible, enabling us to deal with problems, to work, to express ourselves in ways we could have never imagined. It's fascinating, and it's one of the things that drew me to computer science to begin with.

Why am I writing this? Games are high-tech, we know that, is this really the audience for such a talk? Well. Truth is, really, we aren't that much. Now I know, the grass is always greener and everything, but really in the past decade or so technology surprised me yet again and turned things over their heels. Let's face it, the web won. Languages come and go, code is edited live, methodologies evolve, psychology,

[biometrics](http://www.nngroup.com/books/eyetracking-web-usability/), a lot of cool happens there, innovation. It's a thriving science. Well, web and trading (but let's not talk of evil stuff here for now) and maybe some other fields, you get the point.
Now, I think I even know why: algorithms make money in these fields. Shaving milliseconds can mark the success or death of a service. I am, supposedly, in one of the most technical subfields of videogame programming: rendering. Yet it's truly hard to say whether an innovation I might produce does make more money on a shipped title. It's even debatable what kind of dent in sales better visuals as a whole do make. We're quite far removed, maybe a necessary condition, at best, but almost always not sufficient.

Now, actually I don't want to put our field down that much. We're still cool. Technology still matters and I'm not going to quit my job anytime soon and I enjoy the technological part of it as well as the other parts. But, there's space to learn, and I think it's time to start looking at things with a different perspective...

**An odd computing trick that rendering engineers don't want you to know.**

Sometimes, working on games, engineers compete on resources. Rendering takes most, and the odd thing is we can still complain about how much animation, UI, AI, and audio take.

[All your CPU are belong to us](http://en.wikipedia.org/wiki/All_your_base_are_belong_to_us)!
To a degree we are right, see for example what happens when a new console comes out. Rendering takes it all (even struggling), gameplay usually fits, happy to have more memory sitting around unused. We are good at using the hardware, the more hardware, the more rendering will do. And then everybody complains that rendering was already "good enough" and that games don't change and animation is the issue and so on.

Rendering in other words, scales. SIMD? More threads? GPUs? We eat them all... Why? Well, because we know about data! We're all about data.

Don't tell people around, but really, at its best rendering is a few simple kernels that go through data wrapped hopefully in an interface that doesn't upset artists too much. We take a scene of several thousands of objects and we find the visible ones from a few different points of view. Then we sort and them and send everything to the GPU.

Often the most complex of all this is loading and managing the data and everything that happens around the per-frame code. The GPU? Oh, there things get even more about the data! It goes through millions of triangles, transforms them to place them on screen and then yet again finds the visible ones. These generate pixels that are even more data, for which we need to determine a color. Or roughly something like that.

The amount of data we filter through our few code "kernels" is staggering, so it's we devote a lot of care to them.


Arguably many "unsuccessful" visuals are due to trying to do more than it's worth doing or it's possible to do well. Caring too much for the number of features instead of specializing on a few very well executed data paths. You could even say that Carmack has been very good at this kind of specialization and that made his technology have quite the successful legacy it has.

Arguably many "unsuccessful" visuals are due to trying to do more than it's worth doing or it's possible to do well. Caring too much for the number of features instead of specializing on a few very well executed data paths. You could even say that Carmack has been very good at this kind of specialization and that made his technology have quite the successful legacy it has.

**Complexity and cost.**

Ok all fine, but why should we (and by we I'm imagining "non-rendering" engineers) care? Yes, "gameplay" code is more "logic" than "data", that's maybe the nature of it and there's nothing wrong with it. Also wasn't code a compressed form of data anyhow?

True, but does it have to be this way? Let's start talking about why it maybe shouldn't. Complexity. The least code, the best. And we're really at a point where everybody is scared about complexity, our current answer is tools, as in, doing the same thing, with a different interface.


Visual programming? Now we're about data right? Because it's not code in a text editor, it's something else... Sprinkle some XML scripting language and you're data-oriented.

Visual programming? Now we're about data right? Because it's not code in a text editor, it's something else... Sprinkle some XML scripting language and you're data-oriented.

So animation becomes state machines and blend trees. AI becomes scripts, behaviour trees and boxes you connect together. Shaders and materials? More boxes!

An odd middle ground, really we didn't fundamentally change the ways things are computed, just wrapped them changing the syntax a bit, not the semantic. Sometimes you can win something from a better syntax, most of these visual tools don't as now we have to maintain a larger codebase (a runtime, a custom script interpreter, some graphical interfaces over them...) that expresses at best the same capabilities as pure code.

We gain a bit when we have to iterate over the same kind of logic (because C++ is hard, slow, and so on) but we lose when we have to add completely new functionalities (that require modifications to the "native" runtime and to be propagated through tools).

This is not the kind of "data-driven" computation I'll be talking about and it is an enormous source of complexity.

**Data that drives.**

Data comes in two main flavours, sort of orthogonal to each other: acquisition and simulation. Acquired data is often to expensive to store, and needs to be compressed in some ways. Simulated (generated) data is often expensive to compute, and we can offset that with storage (precomputation).

Things get even more interesting when you chain both i.e. you precompute simulated data and then learn/compress models out of it, or you use acquired data to instruct simulated models, and so on.

Things get even more interesting when you chain both i.e. you precompute simulated data and then learn/compress models out of it, or you use acquired data to instruct simulated models, and so on.

Let's take animation. We have data, lots of it, motion capture is the de-facto standard for videogame animation. Yet, all we do it to clean it up, manually keyframe a bit, then manually chop, split, devise a logic, connect pieces together, build huge graphs dictating when a given clip can transition into another, how two clips can blend together and so on. For hundreds of such clips, states and so forth.

Acquisition gets manually ground into the runtime, and simulation is mostly relegated to minor aesthetic details. Cloth, hair, ragdolls. When you're lucky collisions and reactions to them.

Acquisition gets manually ground into the runtime, and simulation is mostly relegated to minor aesthetic details. Cloth, hair, ragdolls. When you're lucky collisions and reactions to them.

Can we use the original data more? Filter, learn models. If we know what a character should do, then can we search for the most "fitting" data we have automatically, an animation that has a pose that conserves what matters (position, momentum) and goes where we want to go... Yes, it turns out, we can.

Now, this is just an example, and I can't even begin to scratch the surface of the actual techniques, so I won't. If you do animation and this is new to you, start from

Now, this is just an example, and I can't even begin to scratch the surface of the actual techniques, so I won't. If you do animation and this is new to you, start from

[Popovic](http://homes.cs.washington.edu/~zoran/#papers)([continuos character control with low dimensional embeddings](http://graphics.stanford.edu/projects/ccclde/index.htm)is to the date the most advanced of his "motion learned from data" approaches, even if kNN based solutions or synthesis of motion trees might be most practical today) and explore from there.
All of this is not even completely unexplored, AAA titles are shipping with methods that replace hardcoding with data and simulation. An example is the learning-based method employed for the

I had the pleasure of working from many years with the sports group at EA, which surely knows animation and AI very well, shipping what was at the date I think

The work of Simon Clavet (

[animation of crowds in Hitman:Absolution](http://www.gdcvault.com/play/1015315/Crowds-in-Hitman).I had the pleasure of working from many years with the sports group at EA, which surely knows animation and AI very well, shipping what was at the date I think

[one of the very few AAA titles with a completely learning-based AI, Fight Night Round 4](http://www.develop-online.net/press-releases/ea-sports-fight-night-round-4-predicts-knockout-victory-for-manny-pacquiao-over-ricky-hatton/0133219).The work of Simon Clavet (

[responsible for the animation of Assissin's Creed 3](http://vancouver.siggraph.org/2012/10/10/procedurally-animating-assassins-creed-iii/)) is another great example, this time towards the simulation end of the spectrum.
What I'd really wish is to see if we can actually use all the computing power we have to make better games, via a technological revolution. We're going to really enter a "next generation" of gaming if we learn more on what we can do with data. In the end it's computer science, actually all there is to it. Which is both thrilling and scary, it means we have to be better at it, and how much there is to learn.

- Data acquisition: filtering, signal processing, but also understanding what matters which means metrics.
- Animation works with a lot of acquisition. Gameplay acquires data too, telemetry but also some studios experiment with biometrics and other forms of user testing. Rendering is just barely starting with data (e.g. HDR images, probes, BRDF measurements).
- Measures and errors. Still have lots to understand about
[Perception](http://www.amazon.com/Visual-Perception-Computer-Graphics-Perspective/dp/1568814658)and[Psychology](http://www.amazon.com/Art-Visual-Perception-Psychology-Creative/dp/0520243838)(what matters! artists right now are our main guidance, which is not bad, listen to them). Often we don't really know what errors we have in the data, quantitatively. - Simulation,
[Visualization](http://www.amazon.com/Data-Visualization-Principles-Alexandru-Telea/dp/1568813066),[Exploration](http://www.ams.org/notices/201110/rtx111001410p.pdf). - Representation, which is huge, everything really is compression, quite literally as code is compressed data, we know, but the field is huge. Learning really is compression too.
- Symbolic regression.
[Statistical models and classification](http://vimeo.com/70734281). Dimensionality reduction. Compression. - Runtime,
[parallel algorithms](https://www.udacity.com/course/cs344)and[GPUs](http://www.nvidia.ca/object/cuda_home_new.html). - This is what rendering gets done well today, even if mostly on artist-made data.
- Gather (Reduce) / Scatter / Transform (Map)
- For state machines (Animation, AI) a good framework is to think about search and classification. What is the best behaviour in my database for this situation? Given a stage, can I create a classification function that maps to outcomes? And so on.

In the end it's all a play of shifting complexity from authoring to number crunching. We'll see.

## No comments:

Post a Comment