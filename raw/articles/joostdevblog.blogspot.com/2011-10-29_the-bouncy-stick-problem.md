---
title: The Bouncy Stick Problem
url: http://joostdevblog.blogspot.com/2011/10/bouncy-stick-problem.html
author: Joost van Dongen
published: '2011-10-29'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)has really fast controls: if you push the stick in a direction, your character immediately faces in that direction. Many games have smoothing animations in between, making the game look more realistic, and adding a bit more weight to the character's movement. However, this also slows down the game a bit and adds some delay to your input, since the character isn't immediately doing what you tell it to. For Awesomenauts we chose to have really quick controls and not do those in-between animations too much.

![](../../assets/d33550f659c68c44.jpg)

However, we discovered an interesting problem with reacting so quickly. It turned out that quite often, when a player walked to the right and then let go of the stick, he ended up facing to the

*left*. Even though he was pressing right. Depending on the controller and the way the player handled the stick, this may never happen, or happen 30% of the times. When this happened it was quite annoying, especially when it happened in the shop: the player would accidentally buy a different item than he wanted once in a while.

So we investigated this issue and my colleague Machiel (of

[Paper Cakes](http://www.papercakes.nl/)fame) discovered what was happening: whenever you let go of the stick, it bounces back to its centre position. But the spring that causes this bounce is so strong, that the stick actually bounces

*beyond*the centre position for a very short amount of time. This GIF animation shows what I am talking about:

![](../../assets/a6c21af4bf24e633.gif)

Note that this doesn't only happen on the Playstation's controller: it also happens on the Xbox 360 controller.

So this explains why the player sometimes ends up looking in the wrong direction: for just one frame, the stick bounces back beyond the neutral position. Awesomenauts reacts to input so quickly, that this results in the player immediately turning around. In slower games, this would not be a problem, but in Awesomenauts, it is.

So I made some measurements on the exact output that the stick is giving each frame. In some cases when you let go of the stick, it just springs back to the neutral position. In other cases, it indeed bounces beyond that.

![](../../assets/ac82426459b8ea8e.gif)

This doesn't always happen, though. So why is that? As you can see in the measurement, the spring back happens extremely quickly, usually within one frame. My guess is that the bounce beyond neutral actually always happens, but is so fast that it often happens in between two frames. So I can't always measure it and thus the game quite often isn't influenced by this bounce.

![](../../assets/7aef006ae191bbf2.gif)

I tried this a lot of times, and it turns out that the stick can bounce quite extremely. When in the neutral stick position, the stick has position 0. All the way to the left is -1 and all the way to the right equals 1. Now when I let go with the stick all the way to the right (1), I have seen it bounce back to as far as -0.72 before getting back to 0. So that bounce is almost entirely to the left! This greatly depends on the controller, though: it seems like the bounce becomes worse when the controller is older, so apparently it increases with use.

**The solution**

So, how to solve this? The first thing that comes to mind is to increase the deadzone: ignore small stick input and hope the bounce falls within the deadzone and thus isn't used. However, since I sometimes measured a bounce of up to 0.72, I would have to increase the deadzone to almost the entire range of the stick, which means the game would only react to stick input when the stick is entirely to the right or left. Not cool.

Another solution also seemed reasonable: since the bounce happens for only one frame, an easy solution would be to ignore input that takes only one frame. However, the game cannot know this until one frame later. So to ignore single-frame input, I would have to introduce a one-frame delay in handling the player's controls. That sucks, because it takes away a little bit from the instant controls that make Awesomenauts play so well.

Now if you look at the graphs, you can see that the user never moves the stick all the way to the right in a single frame: he takes several frames to do this, even on 30fps. Users think they react instantly, but in practice they usually take around 0.1 seconds to move the stick in a certain direction. I tried this a lot and even when I tried to move the stick extremely fast, I am still only very rarely able to move the stick all the way to the right in a single frame. During normal use, this never seems to happen.

The evil bounce, however, always happens practically within a single frame. It is much faster than any real user input. So Machiel came up with a solution that uses this. I implemented his solution and it which works great:

*When the change in the stick's position is bigger than 1.05, ignore it for one frame.**

This eliminates all the bounces that I have seen. And in my measurements, it practically never ignores or delays actual real player input. When the player moves from neutral to all the way to the right, that is a movement from 0 to 1. That is smaller than 1.05, and thus always used immediately. When the user moves all the way from the left to the right, so from -1 to 1, then he takes several frames for this. So the movement per frame is still less than 1.05, and is thus not ignored.

So, I implemented this, and we have not been able to reproduce the Bouncy Stick Problem in Awesomenauts ever since. Win! :)

*

*Edit: As Ben suggested in the comments below this post, it is probably best to use stick position 0 when the output is large, since using the previous frame adds some delay to stopping walking.*

Couldn't you make that threshold dependent on the previous (-1,1) value too? It won't bounce as much when you have it at at -0,5 and release. I understand that people might be inclined to have it near -1/1 in Awesomenauts, but for other things, you never know.

ReplyDeleteInteresting point, I think that would probably indeed be an improvement! :)


ReplyDeleteHowever, I don't think the difference would ever have effect in a real situation, because my current solution already picks out the bounces practically perfectly.

But gamers may be a better quickdraw than you or anyone you know are. You should avoid hampering them ofcourse, and while improbable, it is possible :) Just mentioning as an academic train of thought.

ReplyDeleteSaying that you are implying someone has reflexes fast enough to move the stick from left to right in less that .066 seconds which seems impossible but hey, I could be proved wrong. Regardless, I believe Joost came up with a very intuitive approach on how to solve the problem that will solve the problem for all.

ReplyDeleteSurely your solution will result in 1 frame too many at the extreme position? What I'd do is something like this:



ReplyDeleteif(abs(previous) > threshold && sign(previous) != sign(current))

{ current = 0; }

A tiny change from yours I know, but if you're going for super-responsiveness (which I totally applaud, and is something programmers should focus on more!), then perhaps this would work better.

a really interesting article. These kinds of bugs can be really hard to pin down - it would have taken me a very long time to look beyond the code and at the controller! The graphs are great too.



ReplyDeleteI like other peoples solutions also but my position is that the solution chosen works and was tested, so why look for further solutions?

Joost, it's really good reading blog content on Awesomenauts. In my past experience, blogging on projects I am working on can be hard to get permission for, especially when there are other parties such as clients to consider, it can be a very 'closed door' affair. I am really curious about your set up as you blog about stuff from your professional life and also have your own projects on the side. Does this work ok or cause any issues?

@Ben: Good point, going back to neutral already for that one frame is probably a better solution! :)


ReplyDelete@Dan: I am co-founder and lead programmer at Ronimo Games, so I don't have a boss who tells me what I can and cannot say: I am that boss myself. ;) We do have 7 co-founders, though, and we often work with publishers and consoles, which all add limitations, but in general there is a lot of stuff I can talk about. :)

Joost, as a player and observer only and someone not at all involved in development or troubleshooting, I found this article extremely interesting! I love these small, yet common, issues that arise from tech and human usage. And I love that you find a very effective, human-centered way of solving it!


ReplyDeleteReminds me of how cars are designed with a specific amount of "bounce" in mind so as to replicate the same frequency of the sine-wave motion of walking, so that the bounce isn't noticeable in a car!

I think using stickValue = (previous + current)/2 would also be a correct solution.

ReplyDelete@Deniz: That would work to eliminate the overshoot but if applied constantly would also introduce lag, since it's just general smoothing. The solution needs to be checking for the specific case, I think.

ReplyDelete