---
title: Is true hacking dead? What we lost.
url: https://c0de517e.blogspot.com/2019/12/is-true-hacking-dead-what-we-lost.html
published: '2019-12-01'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

All of these I've been enjoying, even if some need to be taken with more of a grain of salt than others, and from most I've gained one or two interesting perspectives.

Hackers, in particular, struck some chords that are dear to me. Besides the history and the various personalities, some of which I didn't know of, one thing resonated: the hands-on, pragmatic, a-political nature of early hacking.

And no, before we keep going, I don't mean that we should not be political in our actions, today. We are social animals and we should care about society and politics, in fact, it would seem to me that the only reason, at least if one is to take the book at its word, why early hacking was a-political is because hackers were fairly despicable a-social people.

But, it is interesting, because one could make the case that nowadays we live in a world where ideologies trump pragmatic realities, and perhaps we should understand why and take a step back.

What did hackers want? Access to computing. Computers were fascinating, mesmerizing and scarce. It wasn't a matter of software licenses, nobody cared about pieces of paper (or locked doors even), we wanted to be able to touch and tinker with the machine.

And everything was made to be tinker friendly in a golden age of computer hackerism, were kids like me could put sprites on a home television set by reading the c64 manual and playing with basic.

Nobody cared that the machine was not opensource, that the basic interpreter was licensed from Microsoft.

It was truly a huge movement, if we think about it for a second, even its tools were all about immediacy, graphics as a mean of direct feedback, live-coding.

We had one megahertz CPUs (in my times) working with size (not speed!) optimized interpreters.

Even at the ideological level, the goal was for everyone to have access, with systems like Lisp and even more clearly Smalltalk which were designed explicitly with the idea that the user was a tinkerer, always able to stop the world, inspect the inner workings, make some changes, and keep going.

We almost didn't have graphics, but it was in a way the golden age of graphics because people were mesmerized by the possibilities, especially excited about having immediate feedback loops, direct manipulation, fast iteration.

![]() |

["The Early History of Smalltalk"](http://worrydream.com/EarlyHistoryOfSmalltalk/)We lost all of this, basically all. We live in a time where it's impossible not to interface with a computer, computing is cheap and immensely powerful, yet it's nearly impossible to understand and contribute to it.

It is particularly interesting how we used to have the holy grail of live-coding on computers that shouldn't have been able to afford it, while today even the newest, fanciest languages focus primarily in being able to gobble up millions of lines of code in various modules while making iteration increasingly inefficient.

Not having direct access, the ability to stop the machine, list the code, modify and resume, was almost unthinkable. Not having an easily accessible programming language on your machine was unthinkable.

Today what was once a given, sounds in most contexts like science fiction. QBasic is in many ways still an environment that can teach people many lessons...

And again, what I find especially remarkable is that we had so much abstraction and immediacy on machines that shouldn't have been able to afford it. The 80ies were a sort of golden era for interpreters and VMs.

We went the IBM way, and we probably didn't realize it. All that we do today is built for structured teams of thousands of engineers. We prioritize big batch development over individual productivity.

That's probably why we still have textual source (great for git and merging) over more expressive formats or even the old idea of serializing the entire state of a VM (again lisp, smalltalk) which sacrifices merging entirely to make hotpatching (dynamic software updates) trivial.

![]() |

[TempleOS](http://www.codersnotes.com/notes/a-constructive-look-at-templeos/),a.k.a. what the Raspberry Pi should have been.

Now, to a degree this is entirely reasonable, when something becomes commoditized it's just another thing to be used, it loses its appeal.

We buy cars and go to mechanics, right? We don't know how to peek inside the engines anymore...

But what is striking to me is how that ideology is completely lost as well, replaced with one that prioritizes theoretical freedoms over actual ones.

We replaced the Commodore 64, which was entirely closed, proprietary yet hackable, with a linux-based monstrosity like the Raspberry-Pi, which is mostly opensource from what I understand (on the software side of things), yet might as well just be booting Windows and the vast majority of its uses would remain identical.

It's a cheap and fun toy for programmers, sure, but it mostly (entirely?) fails at making computation more accessible, which was its original goal.

In general, it feels like hacking is today dogmatic instead of pragmatic. Surely if everything was open-source... or distributed... or blockchain-based, immutable and lock-free with a pinch of functional programming... written this or this other way, then we would have a better, enlightened society.

And it's not a joke, it's not an entirely a fringe phenomenon, there are vast arrays of engineers that are honestly invested in trying to change the world, but honestly think that solutions are to be found in the technical infrastructure of things.

[(by the way - wanna see something weird?)](https://breakermag.com/heres-the-dark-enlightenment-explainer-you-never-wanted/)

Perhaps we didn't truly graduate from our a-social tendencies, perhaps we're true to form in thinking that the machine and technology are more interesting than people, and groups, and culture...

Whatever the causes, we have software and hardware systems that strive to be entirely open, yet time and again are closed ones that are more accessible in practice, that really drive social revolutions.

Linux didn't change the desktop, nor the way software is made.

Look at my industry. Videogames. What did make games tinkerable? Liberated individual creativity, art, even the ability to make a living?

Steam, the Apple app store, Microsoft XBLIG, Youtube, Twitch, Spotify, Patreon... Unity, Pico8, Dreams passing through Minecraft and Roblox and the game modding community... Not the blockchain, not linux or torrents and so on.

Even the Demoscene, one of the last bastions of true hackerism, is completely uninterested in the ideology of software licenses and contracts.

![]() |

[Pico-8](https://www.youtube.com/watch?v=87jfTIWosBw)And ironically, probably by utter coincidence, but ironically indeed, all the new power brokers of this era, the Facebooks and Amazons, the Googles and Twitters and so on, fully embrace opensource stacks, hundreds of millions lines of codes powering the AIs, the networks of today.

The new IBMs do know very well that lines of code are for the most part worthless, but people and communities aren't, so it's a no brainer to opensource more if in change one gets more people involved in a project, and more engineers hired...

In the end, probably licenses don't mean much. And perhaps technology doesn't either. How we design our human-computer (and human-to-human) interfaces does. And if we don't start thinking about people and think that some lines of code or a contract can change the world, we'll be stuck in not understanding why we keep failing.

*See also: This inspiring keynote by Andy Van Dam*

## 11 comments:

You might be interested in this: https://write.as/simone-robutti/work-notebooks-against-hackerism-pt

"It wasn't a matter of software licenses, nobody cared about pieces of paper (or locked doors even), we wanted to be able to touch and tinker with the machine. [...] Even the Demoscene, one of the last bastions of true hackerism, is completely uninterested in the ideology of software licenses and contracts."


I'm not sure what your point is here - is caring about licenses good or bad then?

I liked the article, it gives me some prospective on the way I've been feeling about technology lately.


Why is the Raspberry Pi a monstrosity?

Ged - the Raspberry Pi is in many ways great, I have one that I use, and it helped create a new industry. But its original goal (if you talk to the founder) was to be sort of a c64, a tool for people to learn and tinker, to make computation accessible, and I think in that it completely fails, because it thinks that access is about a cheap box with linux on it, and it really isn't... The problem is that current systems are inscrutable, not inaccessible, and providing a full linux distro on a SoC board does not help at all... If you wanted to tinker with linux, you already could, in the end it turned out to be a very successful toy mostly because it's cheap and nerds that already know about programming etc buy it for fun, which is ok, but completely off-target. What would have helped? Well, there are lots of incredibly well designed STEM systems out there - unfortunately all of them are proprietary.



Gargaj - Hello! I don't see the contradiction? I was saying that the OG hackers were not interested basically in the stuff the FSF and GPL etc do, but just on direct manipulation of computers, pressing buttons to do things. And then I said that the demoscene is one of the few areas where that spirit survives, and in a similar way people only care about making things, they don't care about opening up their code or working only on certain systems etc. Same in the indie game scene TBH, which is heart-warming and mostly fueled by Unity.

To all - I'm sorry if my blog is a bit messy, it always have been - it's my scratchpad. I hope it provides some points of thought for some, but I don't pretend it's well, really well written. That said, two comments were not really constructive so they had to go.

Thanks for the post. People should write more in this style. A lot of things now are too technical and although it's all good stuff sometimes you feel that something is missing.

Will have a look, thanks.

I also learned hacking on the C64. But how many hacked the C64, and how many just played with it? If you compare this to today, is it so much different from what happens with the Raspi? Ok, the Raspi does not give you raw access to the total hardware; for that you can get one of a myriad of microcontroller-based computers like TI's Launchpad. OTOH, the question is if such an environment is really attractive for many in the potential audience today.


As for licenses and openness, compare the Raspi to the iPhone and the Playstation; which is more hackable?

I don't see the contradiction? I was saying that the OG hackers were not interested basically in the stuff the FSF and GPL etc do, but just on direct manipulation of computers, pressing buttons to do things. And then I said that the demoscene is one of the few areas where that spirit survives, and in a similar way people only care about making things, they don't care about opening up their code or working only on certain systems etc.I guess your wording was confusing; the way I read your sentence "Even the Demoscene, one of the last bastions of true hackerism, is completely uninterested in the ideology of software licenses and contracts", especially with the addition of "even", it sounded to me like you're saying that "true hackerism" and "the ideology of software licenses and contracts" should be on the same page, and that the scene is failing to be true hackers because of that; like somehow the scene

would betrue hackerismif it wasn't forthe lack of interest in licenses.If that's not you meant than okay, I guess I just misunderstood :)

I've always had this annoying feeling that the Sinclair ZX Spectrum I started on in early 90ies, then the MS-DOS, Win3.1 and further, System 7-MacOS9 were all more hackable and open to tinkering by

users and power-usersthan Linux and all the other *nixes (which I also used a lot), even if anyone was saying the exact opposite. Any curious soul could do a bunch of pretty significant stuff on the Spectrum and I can clearly remember when I saw ResEdit on a Classic Mac for the first time. Maybe the actual lack of diversity of tools and programming languages was a benefit.@Gargaj hey there! The way I get it, is that FSF, GPL, etc. was meant to fuel hackerism, but paradoxaly hasn't. For example, the demoscene, where we actually hack up stuff, but don't care much about open source.

Now if I had to theorize about it I'd say that the pragmatist hacker won't care about licenses at all. And will share ideas more than code. (Heck in the early demoscene the last thing one would do WAS sharing code!)

Anyway, I see a seemingly direct incompatibility between a-politic hackers and licences. However, as tinkerers get older and more serious, it's normal to start thinking about legal terms. It gave us things like Doom and Quake where code went open-source and modding was encouraged. Modding which was probably the equivalent of a C64 for a whole generation of aspiring game makers.

Post a Comment