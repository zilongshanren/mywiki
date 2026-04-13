---
title: Failed/fixed leashing in Proun
url: http://joostdevblog.blogspot.com/2010/09/failedfixed-leashing-in-proun.html
author: Joost van Dongen
published: '2010-09-05'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In track 2 in

[Proun](http://www.proun-game.com), at the end of the lap there is a tunnel. There are obstacles in this tunnel and the player needs to avoid them, like this big yellow circle thingie:

![](../../assets/23fb1754bfa962aa.jpg)

Oddly, during playtests, I saw that about one in four players would rotate

*towards*the obstacles, instead of avoiding them. Really strange, because in every other part of that track they immediately understood where they needed to go.

Then one of my testing victims (Marlies Barends, accidentally also the creator of

[this awesome animation](http://www.youtube.com/watch?v=2O9atzRAULQ)) explained to me what was going wrong: the obstacle that you need to avoid has a bright colour, while the tunnel is a dull grey. Also known as: bad leashing!

The solution is simple: I put the light behind the obstacle instead of in front of it. Now the obstacle is in shadow and the tunnel behind it is brightly lit:

![](../../assets/4b2ad05ea482d499.jpg)

I haven't tested this on real dogs yet, but I expect them to know where to fetch the stick now! :)

## No comments:

## Post a Comment