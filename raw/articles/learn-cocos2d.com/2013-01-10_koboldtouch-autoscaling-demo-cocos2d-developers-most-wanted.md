---
title: 'KoboldTouch: Autoscaling Demo (cocos2d developers’ most wanted feature)'
url: http://www.learn-cocos2d.com/2013/01/koboldtouch-autoscaling-demo-cocos2d-developers-wanted-feature/
published: '2013-01-10'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I already blogged about [scaling node positions with display resolution](http://www.learn-cocos2d.com/2012/12/scaling-cocos2d-node-positions-display-resolution/). This feature is now built into [KoboldTouch](http://www.koboldtouch.com/). Time for a demonstration before I get back to work on an improved Tilemap renderer:

The cool thing about KoboldTouch autoscaling is that it works transparently. Your nodes will be positioned relative to the design resolution, for example 480×320. The nodes will continue to use the same position on any device! So you just develop these nodes’ positions and their movement as if they were always on a 480×320 device. It’s that simple.

It also works for movement of any kind, be it CCMove* actions or manually updating the position property every frame. Moving nodes continue to move seemlessly even when you rotate the device.


The content size is not scaled for good reason: it wouldn’t look good. Instead depending on the target device cocos2d’s file suffixes kick in (-hd/-ipad/-ipadhd) as usual, provided that you’ve added these assets.

If you’re using move actions as in the demo, you’ll notice that nodes may pick up speed or slow down after rotation due to the fact that cocos2d’s actions use a duration from which they derive movement speed, as opposed to using an actual “points per frame” speed value which is more common in games (and why I recommend not to use move actions for game world objects).


[Please take the KoboldTouch survey]. I highly appreciate your feedback, thank you!

### Most wanted feature?

I call it the most wanted feature because “resolution independent positioning of nodes” came out on top in my cocos2d developer survey:


### Autoscaling Demo Gallery

#### iPhone

#### iPad

#### Retina iPhone, Widescreen

#### Mac OS X, 16:9 Aspect Ratio

### Like this feature?

Then check out [KoboldTouch](http://www.koboldtouch.com/).

### Short Notice

I know I promised a numbers article on KoboldTouch for today. I decided to postpone it to February because upon closer inspection the current stats aren’t too meaningful yet. Most are projections since it’s only been two months. This also leaves me time to run a survey about KoboldTouch.

### One last thing

I already promised KoboldTouch members to write a small example game around new features and document it. The next one will make use of the new Tilemap renderer.

However I think I can do one better: developing an actual, publishable game! The game will be available to KoboldTouch members as a template from day one and over time evolve into a starterkit and a demonstration of KoboldTouch features and code. And most importantly: it’s all about eating my own dogfood.

I realized that building an engine requires a goal that’s more than just features on a checklist. Feedback from members has been invaluable, but there’s nothing more valuable than to actually use the tool (or engine) you’re working on. If the goal is to make a game, a lot more of those pesky details and usability issues in the engine will surface, allowing me to fix or improve KoboldTouch.

The game will pick up the [railroad game idea](http://www.learn-cocos2d.com/2012/07/starting-point-train-game-freeform-tracks/), combine it with the railtrack linedrawing demo (see above) I wrote several months ago, add physics and a randomly generated tilemap world - the rest will be a surprise. Even to us. I teamed up with a former colleague who will do the game design while I’ll focus on programming.

Hint: we both watched [Unstoppable](https://www.imdb.com/title/tt0477080/) recently. So that may have been an influence.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |