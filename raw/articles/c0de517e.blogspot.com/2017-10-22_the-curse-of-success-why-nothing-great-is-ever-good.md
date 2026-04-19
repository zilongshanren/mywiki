---
title: The curse of success. Why nothing great is ever "good".
url: https://c0de517e.blogspot.com/2017/10/the-curse-of-success-why-nothing-great.html
published: '2017-10-22'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**- The wedding.**

A few weeks ago I flew back to Italy. My best friend was getting married, and I had to be his best man.

![]() |

One night a few days before the wedding we were spending some time together when suddenly he starts getting phone calls from work. Some of the intranet infrastructure in this huge industrial oil and gas site he works in started failing, and even if he is not an IT expert, he happens to be the chief of maintenance for the entire site, and that entails also making sure their server room has everything it needs to keep functioning.

A few months back he commissioned a partial remodel of the room to improve the airflow, as they started experiencing some problems with the cooling efficiency of the air conditioners in the room. Fresh of that experience, immediately a fear dawns on his face: the servers are overheating and that’s why they started experiencing loss of functionality, started with emails.

He sends a technician in the room and his fears were confirmed: none of the four AC units are working, there are more than fifty degrees in the room. Two of them are completely off, the other two have their control panels on but the pumps are not working. To add insult to injury, they didn't receive any notification apparently because the email server was the first to fail.

After instructing the technician to open all windows in the room, it’s decided that he has to go on site to follow the situation. And as I didn’t have much better to do, I followed...

What came after was a night of speculations, experiments, and deductions that you might see in an episode of House M.D., but applied to heavy industrial machinery. Quite interesting to see from the perspective of a software engineer, debugging problems in code is not quite as exciting...

In the end, the problem turned out to be that one of the phases of a tri-phase outlet was missing, and in the end the culprit was found: one cable in the power line went completely bust, possibly due to some slow decay process that has been going on for years, maybe triggered by some slight load imbalance, till in the end an electric arc sparked between two contacts and fried immediately the system.

![]() |

The two units that appeared still to be powered on had their controls wired to the two working phases of the tri-phase, but even for these the pumps would not work because they require all three phases to be present.

4 am, we're back in the car going home and I was asking questions. Why things went the way they did? What could have been done to prevent downtime of an apparently critical piece of IT? Why was that piece of IT even that critical, apparently there was a mirror unit at another location. What is exactly that server room doing? It seems that obviously there would be better ways to handle all that...

And then it dawned on me - this huge industrial site has a ton of moving parts, at any given time there are many ongoing maintenance projects going on, even just monitoring them all is a challenge. Nobody knows everything about everything. Nothing is perfect, lots of things are not even good, in some ways it seems to be barely getting by, in others, it looks fairly sci-fi... You keep the machine going, you pick your battles. Certain things will rot, some stuff will be old and obsolete and wasteful, some other will be state of the art.

Which happens to be exactly how we make videogames. And software in general! I've never been in a game company where there weren't parts of the technology that were bad. Where people didn't have anything to complain about.

Sometimes, or often even, we complain only because we easily accommodate to a given baseline, anything good becomes just the way things are, and anything bad stands out.

But often times we have areas where things are just objectively terrible, old, primitive, cumbersome, slow, wasteful, rotten. And the more successful is the game, the more used is the engine, the bigger and better the end results, the more we risk let some parts fall behind.

**- The best products are not made with the "best" tools in the "best" ways.**

It's easy to understand how this "curse of success" takes place. Production is a monster that devours everything. Ed Catmull and Amy Wallace describe this in chapter seven of the excellent "Creativity Inc." talking of production pressures as the "hungry beast". When you're successful you can't stop, you can't break things and rebuild the world, there's less space for architecture and "proper" engineering.

People want what you're making, so you'll have to make more of it, add features, make things bigger and better; quicky all your resources are drained trying to chase that dragon. On the other hand, the alternative is worse: technology that is perfectly planned, perfectly executed, and perfectly useless.

Engineers and computer scientists are often ill-equipped to deal with this reality. We learn about mathematical truths, hard science, all our education deals with rigorous theoretical foundations, in an almost idealized, Platonic sense of beauty. In this world, there is always a perfect solution to a problem, demonstrably so, and the goal of the engineer is to achieve it.

The trivialities of dealing with people, team, and products are left to human resources or marketing.

Of course, that's completely wrong as there are only two kinds of technology: the kind that serves people, and the useless kind. But this doesn't mean there is no concept of quality in technology either! Not at all! But, we'll have to redefine the concept of "great technology" and "proper" engineering. Not about numbers, features, and algorithms, but about happiness and people: problems solved, results delivered, needs addressed...

![]() |

Great technology then seems not to be defined by how perfect and sparkly clean it is on the inside (even if sometimes that can be a mean for the goal) but by a few things that make it unique, and lots of hard work to keep everything in working order.

If you are very aggressive in prioritizing the end product, inevitably how it's done, the internals, will suffer.


But the alternative is clearly wrong, isn't it? If you prioritize technical concerns over end-user features, you're making something beautiful maybe, but useless. It's gradient diffusion: the farther you are from the output, the more your gradient vanishes.

The product and its needs are the ones that drive the gradient of change the most, the tools that are used to make the product are one step farther, they still need to adapt and be in good shape in order to accomodate the product needs, but the gradient is smaller, and so on, the tools that are made to make the tools for the products have an even smaller gradient until it vanishes and we deal with technology that we don't even care to write or ever change, it's just there for us (e.g. our workstation's OS, Visual Studio internals, what is Mathematica doing when I'm graphing something, how Outlook works etc...)



If you are very aggressive in prioritizing the end product, inevitably how it's done, the internals, will suffer.

But the alternative is clearly wrong, isn't it? If you prioritize technical concerns over end-user features, you're making something beautiful maybe, but useless. It's gradient diffusion: the farther you are from the output, the more your gradient vanishes.

The product and its needs are the ones that drive the gradient of change the most, the tools that are used to make the product are one step farther, they still need to adapt and be in good shape in order to accomodate the product needs, but the gradient is smaller, and so on, the tools that are made to make the tools for the products have an even smaller gradient until it vanishes and we deal with technology that we don't even care to write or ever change, it's just there for us (e.g. our workstation's OS, Visual Studio internals, what is Mathematica doing when I'm graphing something, how Outlook works etc...)

The thing that I happen to say most often nowadays when discussing clever ideas is "nice, but what problem it is solving, in practice, for people, today?".

The role of the engineer should then mostly be to understand what your product needs, what makes a difference, and how to engineer solutions to keep things going, how to prioritize your efforts when there are thousands of things that could be done, very little time to do them, and huge teams of people using your tools and technologies that can't stop making forward progress...

That also explains why in practice we never found a fixed recipe for any complex system: there always are a lot of different ways to reach success: engineering is not about trying to find -the- best solution, but managing the ride towards a good one.

**- Unreasonable solutions to pragmatic goals.**

All this though does not mean that we should be myopic, and just create things by getting precise measures of their effects, and thus optimize for the change that yields the biggest improvement. You can do well, certainly, by aggressively iterating upon your technology, polishing it, climbing the nearest hill. There is value to that, but to be truly excellent one has also to make space for doing crazy things, spending time chasing far-fetched ideas, down avenues that seem at first wasteful.

I myself work in a group that does a lot of research, thus lives by taking risks (if you're not scared, you're not doing research, by definition you're just implementing a solution). And most if not all of the research we do is very hard to correlate to either sales or user engagement. When we are lucky, we can prove some of our stuff saved some time (thus money) for production.

And at one point, one might even need to go explore areas of diminishing returns...

It's what in optimization is called the "exploration versus exploitation" tradeoff: sometimes we have to trust the fact that in order to achieve success we don't have to explicitly seek it, we have to stop explicitly looking at these measures. But that does not mean that the end goal stops to be very pragmatic!

What it means is that sometimes (sometimes) to be truly the best one has to consciously dedicate time to play around, to do things because they are interesting even if we can't prove they will lead anywhere. Know how to tame the production beast.

In practice, it's a tricky balance and a lot of exploration is something that not many teams can realistically achieve (while surviving). Great engineering is also about understanding these tradeoffs and navigating them -consciously-.

## No comments:

Post a Comment