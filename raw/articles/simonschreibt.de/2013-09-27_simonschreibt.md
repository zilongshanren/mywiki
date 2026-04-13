---
title: Simonschreibt.
url: https://simonschreibt.de/gat/world-of-torch-siege-blended-trunks/
author: Simon
published: '2013-09-27'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

I hope you appreciate that i died for this article! *Twice*.

I don’t play [World of Wacraft](http://eu.battle.net/wow/de/) that much and so i use a level 1 hero to investigate the graphics of the game. What can i say? The world is full of aggressive creatures! Grrr! I wish there would be a “ghost” account where you could fly through the world of World of Warcraft without any fighting. ]:)

But now let’s dig to the root of this article! Look at the image below and tell me what you see:

Correct, a bunch of painted polygons (luckily they are forged together to a very beautiful world). But you can see (or can’t see) another detail: **No** hard edges between the trees and the ground. Since computers are able to render a lot of grass, flowers and bushes we can hide sharp polygon edges very well.

At least, if you *don’t* look from above.

In WoW this isn’t a problem since you don’t look very often like this at the game. But there other games out there – and some of them use exactly such a top-down-perspective! So how do they handle this problem (expect from just accepting it)?

I found two very interesting examples which i want to share with you:

On the left you see a tree out of [Dungeon Siege](http://en.wikipedia.org/wiki/Dungeon_Siege) and it’s more or less just a 6-sided cylinder with a wood texture (at this time this was more than enough! I loved the graphic back in 2002)! The interesting part is, that they widened the cylinder at the bottom and faded it out smoothly. So they avoided a hard 6-sided-tree-ground-cut and blended nicely into mother earth.

Even more interesting is the approach to the right. It looks like some grass is covering the bottom of the tree in [Torchlight II](http://www.torchlight2game.com/). But if you take a closer look…

…you’ll see that it’s not grass which covers the tree. The stump itself has some alpha1-cutouts and let you see though!

In my eyes, this is a very nice trick! I mean really…they render less to show more. This is almost philosophic!


![](../../assets/ba0680151067ebbc.png)

[Eric Chadwick](http://ericchadwick.com/)was so nice

[to mention an other interesting approach](http://www.polycount.com/forum/showpost.php?p=1925699&postcount=311)to blend trees with terrain. He used vertex color which he painted on the ground. The result can be seen below (click the link below the picture for high-res version):