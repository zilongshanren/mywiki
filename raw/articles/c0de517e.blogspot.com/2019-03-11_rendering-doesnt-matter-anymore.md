---
title: Rendering doesn’t matter anymore?
url: http://c0de517e.blogspot.com/2019/03/rendering-doesnt-matter-anymore.html
published: '2019-03-11'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Apologies. I wanted to resist the clickbait title, but I couldn’t find anything much better...

And no, I’m not renouncing my ways as a rendering engineer, I’m not going to work on build systems or anything like that. Nor do I believe that real-time

[rendering has “peaked”](http://c0de517e.blogspot.com/2013/12/shit-people-say-graphics-have-peaked.html)or that our pace and progress in image quality has seen slowdowns. There is still a ton of work to do, and the difference between good and bad graphics can be dramatic...
But what I want to talk about a bit more (I mentioned this

[in my previous post](http://c0de517e.blogspot.com/2019/03/what-i-learned-at-activision.html)) is what matters, and how do we decide that. ROI, perhaps an ugly term, but it gets the job done.**From product.**

I’ve spent most of my now thirteen-old professional career in videogames working on production teams. A.k.a. making games. And lots of games I’ve helped making, I actually average a game per year, even when I was in production, which is quite unusual I guess.

Now, when you are in production, things are relatively simple. Ok, no, they are everything but. What I mean is that is straightforward... Ok, maybe still not the best description.

You start with some sort of rough plan. Hopefully, the creative persons have ideas, they present them to you, and you start making a sketch. What are the risks, things to experiment first, what are tasks that are more well known.

Unless you are bootstrapping an engine from scratch or doing major tech changes, mostly you’ll be asked for a ton of features, things people want. An unreasonable amount of them. Ludicrous.

So you go on and prioritize, estimate, shuffle things until you have some plan that makes sense. It won’t, but we know that, we start working and as things change, we re-adjust that plan, kicking features off the list and moving thinks up the priority...

So you get a gigantic amount of work to do, you get on the ride and off you go, fighting fires as they happen, course-adjusting and bracing yourself for the landing. For the most part. There are some other skills involved here and there, but mostly it’s about steering this huge ship that has both a ton of momentum and the worst controls ever.

Naturally, there isn’t much time to think about philosophical questions and other bullshit like that. In fact, plenty of times the truth is that you start losing control over the priorities, even.

That neat idea of reshuffling your list becomes more like a rough sort, and you don’t even necessarily have time or energy to understand why people who are asking for things need these things...



Production, on a good day.



![]() |

If you go around and look at big enough productions, one pattern you will notice is that people start working without knowing the “why” of things. Which leads, no need to say, to quite sub-optimal solutions. But the production beast is an organic one, it’s unclean, it’s made by people and opinions and blood and sweat.

[Engineering is the art of handling all that and still shipping a great game](http://c0de517e.blogspot.com/2017/10/the-curse-of-success-why-nothing-great.html), and it looks nothing like any idealized version of beauty some programmers might hold dear.**To technology.**

Then you move to some cushy job in some central technology department, right? And now you have a problem. You have time, at least, sometimes.

You might want to work on things that help, or have a chance to help, more than a single product. If you do R&D, you will be doing things that have more risks and unknowns. In general, you aren’t so strongly tied to that list of features people are shuffling around day after day. Even when you are doing the only reasonable thing, which is to be attached to a product, you are not that close, you can’t be as you’re not part of the core team.

This is an opportunity because you can have some time and freedom, but also a huge risk because, in the end, the product is all that matters. Being singularly focused on production is not necessarily the best strategy for great products, because that monster swallows and consumes everything, focused on getting “more”, but straying away too much is the road to masturbatory efforts that can be irrelevant at best, dangerous most often.

So, you start thinking of ROI. What should I do? What’s best? You probably have things from multiple teams that could be done, and you have other things that you can persuade teams they should want...

In my case, being a rendering person, the question boils down to, what matters in rendering? How do I estimate how much a thing weights? When you move from “vfx artists want this particle trail thing and you have to do it tomorrow” to look at things with an iota of horizon, how do you decide?

**Rendering doesn’t matter...**

...like it used to. Once upon a time, rendering made the games. Even more than that, entire genres. Doom, of course, is the obvious example, but there are many. The CD-ROM FMV game era. The hardware sprite and scrolling background fuelled platformers, shooters, and so on.



Chances are your engine won't create the next big videogame genre.



![]() |

Then that ended, we arrived at a point where we had enough computing hardware that videogame genres are not defined by technology anymore. Perhaps this will change with VR/AR but for now let’s ignore them (they’re not hard to ignore either, these days).

But we still had a period where technology could be product defining. Call of Duty running at 60fps on ps3 and 360, for example, was quite unique, and that technical characteristic was instrumental to the product. Today doing a 60fps title is the norm, to ship at 30 is almost a gutsy move...

Rendering is thus restricted in the narrower field of aesthetics. It’s just... graphics. Sad if you think of that, right?

Well of course not! We have an ace up our sleeves, see. It’s true that technology is not genre-defining anymore, but AAA productions are insanely graphic-intensive. We love our computer graphics, and the amount of people dedicated to their care and feed is enormous. Everything is good again in the universe, rendering engineering reigns supreme.

So this is the first order of attack of the ROI problem. There are lots of things that are measurable in people and hours and dollars. These, pretty much, will automatically win over anything else. Let’s put them in the bucket of “really important stuff”.

By the way, when I say “measurable”, I don’t mean you can measure them or that you will. You most definitely will not! What I mean is that you could think of them and have a strong feeling they relate to said measurable quantities...

**Chasing shiny things.**

So I said you can bucket things. Things that are required to ship the game first. Things that help people second. Third, you get all your shiny things, which are, incidentally today what you could call graphics R&D. A good part of the stuff I do!

Should we stop doing that? No, of course I will never admit to that, c'mon.

But more seriously, it obviously can’t be that simple. There will never be an end to thing that “help people”, even if the best possible scenario you can still make progress, nothing is ever perfect. So obviously you will reach a point where some rendering effect trumps a tiny pipeline improvement, at least that is a given!

Moreover, though it is not that computer-graphic techniques, even when they are purely visual, do not help content production. We could point at the obvious trend of physically-based rendering, and how that helped (after a lot of growing pains everyone had to go through) to curb the explosion of hacks and ad-hoc controls that we had to create assets before.

But even smaller things can help artists to get more freedom, say even things like antialiasing, for example, might mean that geometry and other sources of discontinuity can be use more leniently, without transforming the frame in an undecipherable mess.

Not only there are diminishing returns for productivity improvements as for any other things, but the split point between features and productivity is often tricky. We definitely do not wait till everything is perfect before pushing more features out, the production monster wants to be fed.

And we shall never, ever discount the gigantic effects of familiarity, the other big scary monster. It is not worth sacrificing everything to it, but we should respect it. To use a technique well, to master it takes a long time. Changing things, even if entirely for the better, with no drawbacks whatsoever, still implies that we need to pay the (often huge) costs of loss of familiarity.



So? How do you decide? How do you measure? Then again. You do not.

I hope he won’t mind me saying, this is one the paths to enlightenment forced on my by Christer, my former boss. How to put this. He has his tricks, not quite koans... So I learned that when he wasn’t persuaded about the opportunity of something, he would go and ask me to put things in more systematic ways, to try to narrow down that ever elusive “ROI”.

Then one time I think we were even arguing about how he could decide that a given initiative he was supporting would, in the end, be beneficial or the better course compared to another alternative. And he slipped and say that we don’t necessarily have to quantify this ROI thing! Of course, be both immediately caught that, even if we were over the phone he could almost sense my smile, but being the clever man he is, he managed to still be right despite the apparent idiosyncrasy...

The lesson is that we want to keep in mind that ROI thing. Not that we need to necessarily optimize for it and spend too much time chasing it. But we definitely need to keep it in mind, be always scared of the risk of doing irrelevant, or worse, damaging things. Keep ourselves accountable.

**It’s the question, not the answer.**

You might be excused to have thought that I put the question mark in the title, even if it isn’t in the form of a question, because of my poor English. But no, it was a clever thing you see, I actually went back halfway into writing this, and thought about it, and finally changed the punctuation. Only after deciding I would also write this, and feel so meta-clever. And again and ok, let’s stop this recursive loop...

And if I was really good at this, I could have jumped directly to the point and spared you all the blabbing, but I have time on my hands these days so. You’re welcome.

In the end, it is true that certain games should even chase diminishing returns because that’s what you do when you’re up enough. And it’s totally true that you can’t really quantify ROI anyway, so often times you should just do what you want. If someone really thinks something is important, and it’s not offensively bad, there should be space for that. In other words, because we know we are bad at ROI, we should realize that to chase it we should not chase it all the time (surprisingly,

[this is even a concept in optimization algorithms](https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/lehman_ecj11.pdf), by the way).
But! The questions are interesting.

How important shiny things are? Is there a point when state of the art techniques become so complex that they are unfriendly both to either content or programmers integrating/iterating, so much so that they will be used sub-optimally? And simpler solutions would have been actually better instead?

Think for example of something perfectly physically accurate, that can produce perfect images, but that behaves poorly when the inputs are not exact. This is not even such a wild scenario, you can see plenty of PBR games that would have been most likely best off without copy-and-pasting the GGX formulas, just because they now go nuclear with specular and aliasing...



Bloodborne might not be the pinnacle of RTR, but it is imaginative...


![]() |

Even more interesting.

**Is there a point where the attention to graphical perfection actually produces worse graphics?**Could it be, for example, that the efforts required to create worlds that are perfect, truly great quality-wise, comes in the way of creating worlds that have the variety, the artistry, the iteration and look that in the end are most often correlated to what people think of great graphics?
Again. In the end, we should remember that we serve the product. Not photorealism, per se, but the product. We do believe that photorealism is a great tool to create games, and I won’t question that. But still we have to remember that photorealism is not the goal, technology per se is useless. It’s the product, that we work for.

And if I had to guess, I'd say in most products today both end-user image quality and in most cases, performance, are bottlenecked by asset production, not the lack of whatever latest cool rendering trick. In particular by:

- The sheer ability of authoring assets.
**Quantity / Variety.** - The ability of iterating on assets.
**Quality.** - The complexity of technical issues linked to art assets. Which in practice yield sub-optimal decision.
**Performance & Quality.** - And the very fixed granularity of assets and their editing tools, the overall inability of performing large, sweeping art changes. The more an environment is "dressed" (authored) the more it hardens and resist change.
**Art direction.***(and perhaps this also causes an over-reliance on some of the few tools that can do said sweeping changes, namely, post-effects)*

**N.B.**All these

**are**

**rendering**

**problems**! Implementation, research, even hardware innovation. Despite the title, the argument here is not that rendering research in videogames is a waste of time, or beyond diminishing returns. Au contraire! It's more vital than ever, in our times of enormous asset pressure. But we have to think hard about what is useful to the end product.

To make a stupid example. A very smart system to automatically generate rendering meshes from artist data (LODs, materials, instances etc) is probably orders of magnitude more important than say, a post-effect...

## No comments:

Post a Comment