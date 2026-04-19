---
title: Tell the internet that you're not a moron...
url: https://c0de517e.blogspot.com/2011/03/tell-internet-that-youre-not-moron.html
published: '2011-03-07'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

...because it will assume you are. Especially if you work on a franchise iteration and you change anything.

Fight Night Champion went from 60fps to 30fps. The most generous reaction among professional reviewers is that it was a step back done in order to have better lighting and graphics. Most of the general internet public (or the part of it that is vocal, on the forums and comment sections of websites) just took it as a downgrade impacting both graphics and gameplay.

Screenshot stolen from:




Of course nothing of this is true. Fight Night Round 4 was already a game with very highly rated graphics, there would have been no need to impact the fluidity of the gameplay in order to have even better lighting.

![]() |

[http://imagequalitymatters.blogspot.com/2011/02/tech-analysis-fight-night-champion-back.html](http://imagequalitymatters.blogspot.com/2011/02/tech-analysis-fight-night-champion-back.html)
![]() |

The lighting was designed from day zero to be able to run at 60fps, going to 30 in gameplay does not really bring us much as the worst-case performance scenario were the non-interactive sequences, that were 30fps in Round 4 too.

At a given point during pre-production, we started building tests for 30fps gameplay, first videos in after-effects (adding motion blur via optical flow), then after these proved to be interesting we went for a prototype in game and blind testing.

Most of our testers and producers likes the gameplay of the 30fps with motionblur version better than the 60fps one. Note that the game itself still runs at 60 (120hz for the physics). Even our users think the same, most did notice that now the punches "feel" more powerful and the game more "cinematic".

The motion blur implementation itself is extremely good, blurring correctly out of the skinned characters silhouettes. To the point that when in some early screenshots we photoshopped in the blur effect, we were not really able to achieve an as good effect as the real in game one.

Still, when you release the technical details that no one really understands, people just assume that you're a moron and they know better. They like the feeling of the new game better, but they hate the 30fps rating... This is just an example, but it happens all the time for many feature that you change.

Bottom line? Change things, but be bold about them and take responsibility. Show what you've done and why, show people that you're not a moron, that you tried everything they are thinking to do plus more and made some choices for some real, solid reasons. Otherwise internet will just assume you're a moron...


P.S. This is just my view as a developer that cares about quality and makes choices in order to maximize quality. To say the truth I don't think that quality matters to a company per se. What it matters is the kind of qualities that sell. That's to say, you can do all the blind testing in the world and be 100% sure that a given choice is the best quality wise, then you go out and people just don't buy it, not always quality sells, some time the worst choice is the most popular (and by popular I mean in sales, not in the internet chatter, I.E. see how much

P.S. This is just my view as a developer that cares about quality and makes choices in order to maximize quality. To say the truth I don't think that quality matters to a company per se. What it matters is the kind of qualities that sell. That's to say, you can do all the blind testing in the world and be 100% sure that a given choice is the best quality wise, then you go out and people just don't buy it, not always quality sells, some time the worst choice is the most popular (and by popular I mean in sales, not in the internet chatter, I.E. see how much

## 21 comments:

For a game that already provided 60Hz feedback to the user, I'm frankly quite surprised why so many people thought internally that halving the frequency of visual feedback was a good idea. It's a fighting game, for goodness' sakes. Visual feedback is crucial for reaction/timing for the player.

Read what I wrote. If you still think you know better, read it again.


P.S. the visual feedback is measured by its latency from the input, not the rendering frequency. I can render at 2000000fps, then have a 2 seconds buffer between the input and gameplay, and still the game will have a 2 seconds lag, quite obviously.

That's okay, I assume the internet is a moron (especially the bits that are vocal about changes in games, as you mention), so we're even on that score.

Almost the same thing as with the C++ discussion. People come in swinging, mostly based on their emotional knee-jerk reactions without ever stopping to consider the ratifications for their opinions, or bothering to listen differing views. I think it's got everything to do with a cognitive bias called Illusory Superiority.


Personally I don't care about the FPS as long as the gameplay feels fluid and fun (and I'm not viewing a slideshow). Fight Night happens to be a series that renewed my faith in that genre of games. It looks and feels awesome and is fun to play. Kudos to the makers.

When it comes to the denizens of the Internet who like to talk about graphics, they tend to latch onto any numbers they get. Because everyone knows that if some number is higher then it's better, right?


Framerate obviously gets this treatment, and for the past few years it's been resolution as well. If any console game comes in below the 1280x720 mark, it's automatically worse looking than any game that hits that res and the programmers who work on it are all incompetent and/or lazy.

I'm sorry that you've been demoralized by the internet.





This is quite the interesting outcome of user testing your game at 30hz.

It correlates with many complaints around the tv/movie industry of the "Soap opera effect", in which the between-frame interpolation of 30hz (video tape framerate, which soap operas were recorded at hence the name) and 24hz (movie frame rate) differs so much that people complain about it.

I wonder if this is due to the fact that either 1) viewers are used to the interpolation of 24hz movies and expect that to be the norm subconsciously, or 2) Movies are conveniently at a 'sweet spot' for human vision, in that it aligns well with our natural rate of processing images.

I would bet a guess that if the framerate was dropped to 24hz, people would like it just a hair better than the 30hz one. Closer to film is the industry trend, right?

I respect you for going with the decisions from your playtesters. If they favored the change, of course you should stick to it. Maybe it works fine for your particular game. But for games in general, I disagree with the claim that lower framerate does not matter.


I think it matters because the visual framerate decides how fast you can react. This is more important in some games than others. It doesn't matter if your game logic and user input can detect 1000 button presses per second if the game renders at 30 fps.

The player is limited by the slowest part of the system.It can be network latency, direct user input, render frequency or the frequency of the game loop. If a part of the system is slower than the others, it can not be remedied by the other systems. In my opinion, this is why it makes the most sense to render at a higher or equal frequency compared to the game loop or input polling. Everything else is just lost potential.

Mads: again and again and again. Frequency != Latency. FREQUENCY IS NOT LATENCY.




So yes in general FPS are meaningless from a reactiveness standpoint.

Of course the minimum latency would be achieved in a 60fps game that goes from the pad input to the screen with no buffer, but in general the fact a game is at 60 does not mean it will have a lower latency than a game that goes at 30.

I'll say it again: _FREQUENCY_ _IS_ _NOT_ _LATENCY_

NickC: Demoralized by the internet? I? No, that won't happen.



The "soap opera effect", I wonder if that's only a problem with cheap the temporal resampling, I wonder if the same would be noticeable using optical flow... Anyway it's a bit of a different issue because there you are resampling...

Also the outcome of our testing is not soooooo suprising: http://www.insomniacgames.com/blogcast/blog/mike_acton/1503082

Honest mistake, I didn't mean network latency obviously, but the number of updates sent per second over the network.



I'm very aware that the internal frequency a game runs at doesn't directly reflect the latency in the system. For my example, I obviously disregarded that the system does any buffering.

So again to be clear, assuming that there is little to no buffering, the overall system is limited to the subsystem with the lowest frequency. Do we still disagree?

Mads: if there is no buffering othet than the gpu ring buffet, we agree, 60 will be more responsive. Now go and try to find a game that runs at 60 with no buffers. I date to say you never shipped an AAA game this gen...

But still, isn't 1/fps the lower bound of latency?





Consider this sequence of events:

t=0ms a frame is rendered

t=5ms the physics/game/whatever engine spits out an event

At 60fps, the user is notified at about t=16ms, at 30fps the user is notified at about t=33ms. Isn't this worse?

Or the numbers are such that computations take so much more than rendering to make this argument irrelevant?

I am not a game developer, so I don't know the orders of magnitude involved (especially, I am wondering what is the reaction time of the player).

To clarify: I am not asking to question your decision in the development of your game, I am genuinely curious of what the numbers are for a modern game on modern hardware.

1/fps is indeed the lower bound. But knowing the lower bound is meaningless really. Do in practice games achieve their lower bounds? Nah, it's an exercise left to the reader to see why we could and do have usually a few frames of latency (hints: controller inputs and grammars; why the gpu is always at least one frame behind the cpu? Why does it need to buffer?)

So, why does the game engine run at 60 Hz? (And the physics at 120 Hz?)



Who cares if you determined the position of the ball at instant 1,2,3 and 4 if what you can show is just instant 4?

Am I to assume that you use the extra points so that the player actions can be applied between frames? Isn't it a bit unfair to the player that (s)he has to mentally extrapolate the situation of the next frame without knowing that other events could have happened in the mean time? Or is this considered part of the game?

Anon: Because that provides a lower latency, of course!





Now there are some technical details that I don't want to talk about (and it's not only lazyness but also a matter of non-disclosure) but your reasoning is silly.

It's not that you show things at "instant" 4 as there is not an "instant" 4. There is input, then gameplay, then rendering, and you want to minimize the lag. The input let's say might get your pad state at time 0.1, game can compute the output at time 0.2, render can finish at time 0.5 and you get a 0.1-0.5 = 0.4 latency.

If the "game" part runs slower, you add more latency, right? Plus you can do other things, for example you might want to poll the input at 10000hz to detect some very slight movements and dunno, average or recognize a move or whatever. Then the game can run at 100hz because it wants to be very accurate at updating objects in small steps and dunno, recognize precisely collisions and physics response. Then the render can go at 30fps because that's what your game needs, you tested it and it looks and plays great.

Hope this helps.

" Isn't it a bit unfair to the player that (s)he has to mentally extrapolate the situation of the next frame without knowing that other events could have happened in the mean time?"



Not really, people do it all the time (imagine trying to catch a thrown ball, for example).

Based on your knowledge of the system you can make very accurate educated guesses as to what is likely to happen in the next half a second.

Quite interesting point.


I'm wondering how the game engine design is affected by latency requirements, in particular multi-threading issues.

Biagio: it can and it should be.

"Of course nothing of this is true"







it IS true, no doubt about that - not even arguing.

30 fps is 100% okay for me but you can't deny 60 fps is an improvement over 30 fps just because 1.000s of people don't think so.

i agree other parts are more important (input lag, physics) but there's just no way going from 60 to 30 isn't a downgrade.

another topic would be 'good' 30 fps versus GT5-ish 60 fps (massive tearing and framedrops all over the place)

in that case i understand any developers and gamers to prefer the stable 30 fps :)

Going from 60 to 30 is a downgrade, but that would have been plain stupid. We evaluated 30 with motion blur to 60 without, knowing that we could achieve both easily. We compared the two things side by side and we preferred 30 with motion blur. How is a better thing (at least to the eyes of the people that had the opportunity to test it agains he alternative) be considered a "downgrade"?

Post a Comment