---
title: Klingons Do Not Release Software
url: http://hacksoflife.blogspot.com/2019/10/klingons-do-not-release-software.html
author: Benjamin Supnik
published: '2019-10-29'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Brent Simmons on



This comes from the fundamentally reusable nature of software. We see this with X-Plane. We have decent estimates for how long aircraft will take to build because each aircraft, while different from the others in terms of its aerodynamics, look, texturing, modeling, is the same in terms of the


On the software side, we do everything exactly once. Once we rewrite the entire rendering engine to run under Vulkan, we will never do that again, because we will have Vulkan support, and coding it twice would be silly.


Almost every software feature ends up like this - the feature is fundamentally novel compared to the last one because you don't need a second copy of code.


Brent finishes up the article with this:



This reminded me of the old nerd joke:



I think Brent's definition is right, as long as we recognize that "ready" is a dynamic term that can change based on market conditions and the better understanding of what you really need to ship that you get from implementation. If your app figures out it's ready before you do, you might have Klingon software on your hands.

[ETAs for software releases](https://inessential.com/2019/10/28/no_etas):This is all just to say that app-making is nothing like building a house. It’s more like building the first house ever in the history of houses, with a pile of rusty nails and your bare hands, in a non-stop tornado.He put this at the end of the article, but I think it's the most important lesson here: it's hard to estimate how long a coding task will take because every coding task that you undertake that is worth something to your business is the very first time your business has made anything like that task.

This comes from the fundamentally reusable nature of software. We see this with X-Plane. We have decent estimates for how long aircraft will take to build because each aircraft, while different from the others in terms of its aerodynamics, look, texturing, modeling, is the same in terms of the

*kind*of tasks: 3-d modeling, UV mapping, animation, etc.On the software side, we do everything exactly once. Once we rewrite the entire rendering engine to run under Vulkan, we will never do that again, because we will have Vulkan support, and coding it twice would be silly.

Almost every software feature ends up like this - the feature is fundamentally novel compared to the last one because you don't need a second copy of code.

Brent finishes up the article with this:

The only reason anything ever ships is because people just keep working until it’s ready.But this is only half-true. Code also ships when the scope of the project is reduced to the things you have already finished. And I think this is important to remember because reducing scope is the one thing that actually reduces ship times.

This reminded me of the old nerd joke:

Klingons do not release software. Klingon software escapes, leaving a bloody trail of design engineers and quality assurance testers in its wake.On a big, unwieldy, messy release with seat-of-the-pants project management, that's a pretty good description of what happens - at some point the overwhelming business force of needing to ship dominates what's left in the todo pile and the software smashes through the wall, Kool-Aid style and gives the users a big "Oh Yeah!"

I think Brent's definition is right, as long as we recognize that "ready" is a dynamic term that can change based on market conditions and the better understanding of what you really need to ship that you get from implementation. If your app figures out it's ready before you do, you might have Klingon software on your hands.

## No comments:

## Post a Comment