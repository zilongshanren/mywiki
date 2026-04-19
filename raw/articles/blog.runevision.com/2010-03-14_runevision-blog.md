---
title: runevision blog
url: https://blog.runevision.com/2010/03/
published: '2010-03-14'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I've been spending the last week in San Francisco attending the [Game Developers Conference](http://gdconf.com/) and showing off [Unity](http://unity3d.com/) at our awesome (and very busy) booth.

![](../../assets/5ce1a50b28b18057.img)


### Booth Experiences

The people I've met have been very excited about Unity; both our product in general and about the [new features](http://unity3d.com/unity/coming-soon/unity-3) we'll be releasing in upcoming Unity 3 this summer and which we previewed at the booth. Unlike last year, there were practically no people this year who hadn't heard about Unity some way or another.

### IGF Impressions

The [Independent Games Festival](http://igf.com/) awards show was great. I was especially excited about Danish guys *Playdead* winning no less than two awards for their game [Limbo](http://www.limbogame.org/) and other Danish guys *Press Play* winning an award for their Unity game [Max & the Magic Marker](http://maxandthemagicmarker.com/) for Wii, PC, and Mac. I've had a chance to play both, and they're both excellent games. Coincidentally they're both side-scrolling platform games with a strong puzzle focus, but besides that they're completely different.

### Animation Insights

I only got to see one session this year - [Player Movement and Animation in Drake's Fortune 1 and 2](https://www.cmpevents.com/GD10/a.asp?option=C&V=11&SessID=10429). It was very well presented. Everything was sensible and easy to understand; there was nothing ground-breaking but a lot of useful tips and tricks. With the exception of one thing that was purely done to save memory (flipping animations on the left-right axis), everything they did could be done in Unity without problems. They basically rely on lots of animation blending, some of the animations applying to only part of the skeleton, and some animations being additive; all things that are supported in Unity. They also do some IK fixes, which of course can be done in Unity with scripting.

Their method for making characters standing and moving correctly on uneven surfaces is a little similar to how my [Locomotion System](http://unity3d.com/support/resources/unity-extensions/locomotion-ik) does it, just a bit simpler: They too use raycasts to find the ground height for the feet, then adjust the hip/root height, and then use IK to adjust the legs.

The most interesting thing they did was having a few long animations with random wiggling of the character. By applying this on top of a 1-frame idle animation they get a nice long, varied idle animation, but it means they can have lots of different idle animations that are all just 1 frame long which turn into nice animations when the wiggly-animation is applied on top. They do similar things with walking and running to add variation that can span over a long time but doesn't require much space because it can be reused for many different animations. Perhaps we can add something like that for our new Unity 3 launch demo that we're working on.

### Going Home

It's been a long and hard, awesome week, and I've met lots of great people, but now I also look forward to going home again. I'll be arriving back in Copenhagen on Monday, and once I've recharged a little I'll be continuing working on getting Unity 3 out.