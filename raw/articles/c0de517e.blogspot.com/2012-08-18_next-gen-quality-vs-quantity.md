---
title: 'Next-gen: Quality vs Quantity'
url: https://c0de517e.blogspot.com/2012/08/next-gen-quality-vs-quantity.html
published: '2012-08-18'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Pixar's Luxo JR, 1986.

Is this rendered "offline"? Would we mistake this frame as something our realtime engines are capable of? We can go any number of years in the past and look at offline outputs for movies and shorts, up to the very beginnings of computer graphics, and still recognize a gap between videogames and movie productions. How comes?

It's a matter of quality. Siggraph ended last week and

[Johan Andersson delivered yet again](http://www.slideshare.net/DICEStudio/new-13912730)a clear, precise and technically superb presentation on what are the key challanges of realtime rendering. And yet again at number one he identified "cinematic quality" as the priority.
Now of course at a technical level, this implies research on antialiasing solutions (Have you ever noticed how -some games- do look incredible by just bumping up on

[PC the sampling rate](http://www.google.ca/search?hl=en&safe=off&q=mass+effect+ogssaa&bav=on.2,or.r_gc.r_pw.r_cp.&biw=543&bih=653&um=1&ie=UTF-8&tbm=isch&source=og&sa=N&tab=wi&ei=jkMwUIKxBKizigKLn4GwBQ#biv=i%7C3;d%7CfqXXOBospWUX1M:)?), spatially and temporally. His presentation is great so if you haven't read it yet, stop reading right now and fetch that first (and be sure also to follow the links and references he included).
But, I would argue there is more to it than our technical limitations, it is an attitude and a way of working. When creating a realtime rendering experience we are always constrained by our hardware and human resources. We have to make compromises, all the time, and one fundamental compromise we make is between quantity and quality. Should we add or refine?

This is indeed a very fundamental tradeoff, we don't encounter it only in rendering but all across our production and in all activities beyond the videogame industry as well. Isn't it the same compromise that lends to code rot and technical debt in our software? I would dare to make a comparison between Apple and other companies, but that's probably not the best and I could end up having to remove too many comments... Leica versus Canon?

Ok, going back on track, are we doing our best job at this compromise? When we add a visual feature to our rendering, how conscious are we of where it falls on the quality versus quantity line? Is quality even really considered as a target, or do we still reason in terms of features on the "back of the box"?

Of course if you ask that question, everybody would indeed say that quality is their focus. Quality sounds good as a word, it's the same as "workflows" and "tools" and "iteration", everybody wants to have these things, especially if the come for free. We have a "great" team, so quality is a given, right?

Have you ever finished a task for a rendering feature, and it works in game. And it's considered "done"? Or gets tested by an artist, it doesn't crash, it's understood, done? When does quality ever enter this process? I won't rant on otherwise I'll spend half of the post just talking about similar things and companies that value their tools by assigning the most junior programmers to the task and such horrors that really deserve their own space another time.

Do we really know what matters anyways? It is easier for everyone really to go for the quantity, add another feature, it looks like progress, it's easy to track on the schedule, it's easy to show in a trailer, caption and tell the world, we spent money in this new thing, regardless of how it feels. Next-generation HDR and bloom, rings a bell? Crank the parameters to a million and show your work...

Great rendering technology is not supposed to be seen, without trying to be romantic, it should be "felt". The moment you're capable of identifiying rendering techniques in an image, and not layers visual elements in the image (i.e. volume, texture, silouhette, shadows) we already have failed somehow.

If you can't do it well, don't do it at all. I think about

[Toy Story](http://www.imdb.com/title/tt0114709/)and how Pixar chose not to make a story with organic creatures, believing they could not yet deliver that level of complexity. And then of Crysis 2, a great game, with stable graphics (one of the first things I noticed, almost defect free), that I bought and finished.
I make this example often really, because it's such a popular game that most especially renderers have played, which does something peculiar, it fades your LODs pretty aggressively, especially it seems on small detail objects, like rocks on the ground which dissolve into nothing after a few meters. And to me that's surprising, in such a well crafted game, why does it has to show me that rock and then fade it? I can see it, I can see the trick, and I don't want to. I can live without the rock, I would not complain about it not being there, but now I can see it dissolving, I can see the render tech.

The truth is, from my experience at least, we are still far from understanding what makes great realtime visuals. Not only how to manage them, how to produce them and how technically how to solve these problems but also exactly what matters and what doesn't. So you see (and I'm making that up, right now I'm not thinking at one specific title) games with yellow skin highlights and glowing cyan sky that spent time into a dubious water simulation at a scale where it won't anyways be sold as right.

And then when it's all done and badly, we layer on top thick pass of bloom (possibly temporally unstable) and vignette and tinting and lensflares that would make Instagram blush, and we call it done.

In part it's a lack of education, we're a naive, young industry that only now is transitioning into a mature craft with fierce competition and we often just lack the right skills in a team. In part, it's truly a dark art with a lot of unknowns, far from being a science.

Do I really need that? Could I bake that other? What approximation of this is the most reasonable? If you're lucky, you work closely with artists, and great artists and art directors, with the right workflows and somehow magic happens. And some companies do seem to deliver this magic consistently. But as an industry? We're far. Both in practice and in theory, as


There are people saying that rendering is less relevant, or even "solved" (which is crazy, as it's far to be solved even offline, even in theory). That behavior and motion are the next big challenges (and undeniably, they are becoming crucial, and if you have some time read this three, in increasing order of complexity:

[I wrote some time ago](http://c0de517e.blogspot.ca/2011/10/open-questions.html).There are people saying that rendering is less relevant, or even "solved" (which is crazy, as it's far to be solved even offline, even in theory). That behavior and motion are the next big challenges (and undeniably, they are becoming crucial, and if you have some time read this three, in increasing order of complexity:

[motion graphs](http://research.cs.wisc.edu/graphics/Papers/Gleicher/Mocap/mograph.pdf),[motion fields](http://grail.cs.washington.edu/projects/motion-fields/)and[their successor](http://www.stanford.edu/%7Esvlevine/papers/ccclde.pdf)) but we are still far not only from photorealism but from proper understanding and application of the techniques we have, and from proper understanding of how to manage the creative process and how to achieve predictable levels of quality. We probably have more techniques and technical knowledge than experience and "visual taste".
I truly suspect that if we were to start an engine from the basics, forward rendering and mostly baked, a sprinkle of stable CSM shadows and a directional light, and stretch it to quality, we would already have enough tasks to figure out inputs (Textures? What resolution, what filtering. Compressed how? Normals? What are these? Specular? Occlusions?), materials (Specular and prefiltering? Fresnel, how? With Blinn? Diffuse, how? What matters, what does not work...), outputs (Antialiasing, HDR, Tonemapping*, Exposure... there are books written on tone mapping alone) and what matters were (Perception, A/B testing, biometrics? Eye tracking? LODs how etc...) to keep a rendering team busy for a couple of game cycles, write some research papers in the process and create the best visual experience of any generation...


-



-

***Note:**It took way too long and a few articles in books to get this whole gamma/degamma thing to a "mainstream" level. Let's not wait another ten years to get the idea that HDR needs to be**PROPERLY**tonemapped to make any sense. And by HDR I don't mean an HDR framebuffer in post, even if you write just to a LDR 8bit target, you can still do it in the shader, right? Right? Ok. If you don't know what I'm talking about, go and read and USE
## No comments:

Post a Comment