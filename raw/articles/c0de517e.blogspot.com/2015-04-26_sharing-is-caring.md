---
title: Sharing is caring
url: http://c0de517e.blogspot.com/2015/04/sharing-is-caring.html
published: '2015-04-26'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Knowledge > Code.**

Code is cheap, code needs to be simple. Knowledge is expensive, so it makes lots of sense to share it. But, how do we share knowledge in our industry?



Nearly all you really see today is the following: a product ships, people wrap it up, and some good souls start writing presentations and notes which are then shared either internally or externally in conferences, papers and blogs.

This is convenient both because at the end of production people have more time on their hands for such activities, and because it's easier to get company approval for sharing externally after the product shipped.

What I want to show here are some alternative modalities and what they can be used for.

**Showing without telling.**

Nowadays an increasingly lost art, bragging has been the

[foundation of the](http://www.hardcoregaming101.net/demoscene/demoscene.htm)[demo-scene](http://thecreatorsproject.vice.com/blog/idemoscene-the-art-of-the-algorithmsi-looks-at-the-history-of-a-digital-subculture). Showing that something is possible, teasing others into a competition can be quite powerful.
![]() |

[Stash/TBL](http://www.pouet.net/prod.php?which=3)
One of the worst conditions we sometimes put ourselves into is to stop imagining that things are possible. It's a curse that comes especially as a side-effect of experience, we become better at doing a certain thing consistently and predictably, but it can come at the cost of not daring trying crazy ideas.

Just knowing that someone did somehow achieve a given effect can be very powerful, it unlocks our minds from being stuck into negative thinking.



*I always use as an example*

[Crytek's SSAO](http://en.wikipedia.org/wiki/Screen_space_ambient_occlusion)in the first Crysis title, which was brought to my attention by an artist with a great "eye" while playing the game in the company I was working at the time. I immediately started thinking how realtime AO was possible, and the same day I quickly created a shader by modifying code from[relief mapping](http://www.inf.ufrgs.br/~comba/papers/2005/rtrm-i3d05.pdf)which came close to what it was the actual technique (albeit as you can imagine much slower as it was actually ray marching the z-Buffer).
This is particularly useful if we want to incentive others into coming up with different solutions, engage their minds. It's also easy: it can be done early, it doesn't take much work and it doesn't come with the same IP issues as sharing your solution.

**Open problems.**

If you have some experience in this field, you have to assume we are still making lots of large mistakes. Year after year we learned that our colors were all wrong (

[2007: the importance of being linear](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch24.html)), that our normals didn't mean what we thought ([2008: care and feeding of normal vectors](http://blog.selfshadow.com/publications/blending-in-detail/)) and that they didn't mipmap the way we did ([2010: lean mapping](http://blog.selfshadow.com/2011/07/22/specular-showdown/)), that[area lights are fundamental](http://blog.selfshadow.com/publications/s2013-shading-course/karis/s2013_pbs_epic_slides.pdf), that specular highlights have a tail and so on...
Actually you should know of

[many errors](http://c0de517e.blogspot.ca/2015/03/being-more-wrong-parallax-corrected.html)you are making right now even, probably some that are known but you were too lazy to fix, some you know you are handwaving away without strong error bounds, and many more you don't suspect yet;[The](http://www.cs.princeton.edu/courses/archive/fall10/cos526/papers/zimmerman98.pdf)[rendering equation](http://www.rorydriscoll.com/2008/08/24/lighting-the-rendering-equation/)is beautifully hard to solve.
![]() |

[The rendering equation](http://www.dca.fee.unicamp.br/~leopini/DISCIPLINAS/IA725/ia725-12010/kajiya-SIG86-p143.pdf)
We can't fix a problem we don't know is there, and I'm sure a lot of people have found valuable problems in their work that the rest of our community have overlooked. Yet it's lucky if we find an honest account of open problems as further research suggestions at the end of a publication.

Sharing problems is again a great way of creating discussion, engaging minds, and again easier to do than sharing full solutions, but even internally in a company it's hard to find such examples, people underestimate the importance of this information and sometimes our egos come into play even subconsciously we think we have to find a solution ourselves before we can present.

Hilbert





[knew](http://aleph0.clarku.edu/~djoyce/hilbert/problems.html)[better](http://www.ams.org/notices/200007/fea-grattan.pdf). Johan Andersson did[something](http://bps10.idav.ucdavis.edu/talks/02-andersson_5MajorChallenges_BPS_SIGGRAPH2010.pdf)[along these](http://bps12.idav.ucdavis.edu/talks/02_johanAndersson_5MajorChallenges_bps2012.pdf)lines for the realtime rendering community, but even if EA has easily the best[infrastructure](http://www.slideshare.net/e2conf/fes17-fu)and dedication to knowledge sharing I've ever seen discussion about open problems was uncommon (at least in my experience).
Establishing a new sharing pattern is hard, requires active dedication before it becomes part of a culture, and has to be

[rewarded](http://www.reliableplant.com/Read/522/reliability-failure).**The journey is the destination.**

It's truly silly to explore an

[unknown landscape](http://c0de517e.blogspot.ca/2015/03/design-optimization-landscape.html)and mark only a single point of interest. We would map the entire journey, noting intersections, roads we didn't take, and ones we took and had to backtrack from. Even algorithms[know](http://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo)[better](http://en.wikipedia.org/wiki/Tabu_search).
Hoarding information is cheap and useful, keeping notes as one works is something that in various forms everybody does, the only thing that is needed is to be mindful in saving progress through times, snapshots.


The main hurdle we face is really ego and expectations, I think. I've seen many people having problems sharing, even internally, work that is not yet "perfect" or thinking that certain information is not "worth" presenting.

The main hurdle we face is really ego and expectations, I think. I've seen many people having problems sharing, even internally, work that is not yet "perfect" or thinking that certain information is not "worth" presenting.

![]() |

Michelangelo's unfinished sculptures are

[fascinating](http://www.mu.nl/uk/exhibitions/past/the-sculpture-factory).
Few people share work-in-progress of technical ideas in scientific fields, even when we do share information on the finished product, it's just not something we are used to see.


Internally it's easy and wise to share work-in-progress, and you really want people's ideas to come to you early in your work, not after you already wrote thousands of lines of code, just to find someone had a smarter solution or worse, already had code for the same thing, or was working at it at the same time.

Internally it's easy and wise to share work-in-progress, and you really want people's ideas to come to you early in your work, not after you already wrote thousands of lines of code, just to find someone had a smarter solution or worse, already had code for the same thing, or was working at it at the same time.

Externally it's still great to tell about the project's history, what hurdles were found, what things were left unexplored. Often reading papers, with some experience, one can get the impression that certain things were needed to circumvent untold issues of what would otherwise seem to be more straightforward solutions.

Is it wise to let people wonder about these things, potentially exploring avenues that were already be found to not be productive? And on the other side sometimes documenting these avenues explicitly might make others have ideas on how to surpass a given hurdle in a different way. Also consider different people have different

[objectives and tradeoffs](http://en.wikipedia.org/wiki/Pareto_efficiency)...

**The value of failure.**

If you do research,

[you fail](http://www.bbc.com/news/technology-25880738). That is almost the definition of research work (and the reason for

[fast](http://toplap.org/)

[iteration](http://ecorner.stanford.edu/authorMaterialInfo.html?mid=686)), if you're not allowed to fail you're in production, not inventing something new. The important thing is to learn, and thus as we are learning, we can share.

*Vice-versa, if your ideas are always or often great and useful, then probably you're not pushing yourself hard enough (not that it is necessarily a bad thing - often we have to do the things that we exactly know how to do, but that's not research).*

When doing research do we spend most time implementing good solutions or dealing with mistakes? Failing is important, it means we are taking risks, exploring off the beaten path, it should be rewarded, but that doesn't mean there is an incredible value for people to encounter the same pitfalls over and over again.

Yet, failures don't have any space in our discussions. We hide them, as having found that a path is not viable is not a great information to share.

Even worse really, most ideas are not really entirely "bad". They might not work right now, or in the precise context they were formulated, but often we have failures on ideas that were truly worth exploring, and didn't pan out just because of some ephemeral contingencies.

Moreover this is again a kind of sharing that can be "easier", usually a company legal department has to be involved when we share our findings from shipped products, but fewer people would object if we talk about things that never shipped and never even -worked-.

Lastly, even when we communicate about things that actually do work, we should always document failure cases and downsides. This is really a no-brainer, it should be a requirement in any serious publication, it's just dishonest not to do so, and nothing is worst than having to implement a technique just to find all its issues that the author did not care to document.

*P.S. Eric Haines a few days ago shared his view on sharing code as part of research projects. I couldn't agree more, so*

[I'll link it here](http://www.realtimerendering.com/blog/why-not/).*The only remark I'd like to add is that while I agree that code doesn't even need to be easy to build to be useful, it is something that should be given priority to if possible.*

*Having code that is easy to build is better than having pretty code, or even code that builds "prettily". Be extremely pragmatic.*

*I don't care if I have to manually edit some directories or download specific versions of libraries in specific directories, but I do hate if your "clean" build system wants me to install N binary dependencies just to spit a simple Visual Studio .sln you could have provided to begin with, because it means I probably won't have the patience to look at it...*

## 4 comments:

Thanks for this post. I particularly like the principle of "seeing is believing", that just proving something is possible breaks us out of our preconceptions. That's one thing I love about graphics - assumptions change.


The "if you're not failing, you're not doing research" is a good point. It's tough, though, to get anyone to publish, "boy, this sure didn't work" results. Even blogging about them sounds a bit depressing, though I agree it'd be useful, something for others to build on.

Eric, thanks for the comment.



About the "seeing is believing" - that can be interesting in many ways. Internally and Externally at a company/organization it can be interesting time to time to just organize challenges, asking people to beat records, the demoscene is a good example of innovation fueled by that.

About publishing failures. Some would say that already happens, just they are not described as such :) But more seriously, I don't expect anytime soon to have a journal of almost-working ideas, but there isn't only academia and even there, journals are not the only mean academia can communicate...

The types of people who reinvent software will do so with or without sample source code.



Academic types have the stupidest excuses not to share code, and sometimes it's the university tempting them to go commercial (GTA 4's Euphoria; Mixamo) which - while beneficial for the standalone product - is a pattern norm that creates meta-level issues like a drained software community of dysfunctional individuals, paywalls and garbage app stores full to the brim (Steam), and an industry norm of looking toward monopoly tech companies because of the cultural hegemony they possess (AAA video games and movies and the computer graphics industry; what is normal and widely culturally relevant at any time). Whatever's possible for a tech CEO at the drop of a hat is impossible for the most hardworking individual to ever obtain (The Spectacle) - and we are talking major, addictive messaging being delivered to society on a weekly basis. Horror aside, it's corruption, though not as crystal clear as GamerGate. Academics and programmers alike have a propensity to either not grasp these issues or repress them when they feel powerless by themselves.

Many people object when I post something radical like this, especially in popular places that can now ban you for bursting their bubble. They want to know why. The answer is simple - in any place considered big enough to pose wide open questions about the world -- that's the place the truth is supposed to go.

Anon: I've read your text twice and I don't get what are you saying, how that's relevant to my post and thus why are you saying it here.

I do ramble and rant a lot on this blog but I don't expect the same in the comments :)

Post a Comment