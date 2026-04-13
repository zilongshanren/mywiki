---
title: CryptoRl - postmortem
url: https://randomtower.blogspot.com/2015/09/cryptorl-postmortem.html
author: Pubblicato da Marte
published: '2015-09-04'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

My take on roguelikes have a long start... four years ago with a little experiment,

[Goblin Invasion](http://randomtower.blogspot.it/2011/07/goblin-invasion.html). It's not a game and it's not working anymore, but is a start as player and developer to understand these games. What is going on under the hood ?

I've started playing more roguelikes, forget about graphics and think about mechanics: what is cool? How to implement that ? And then Notch (do you remember? Minecraft before Microsoft.. ) develop for

[LudumDare](http://www.ludumdare.com/compo/)

[Prelude of the Chambered](http://randomtower.blogspot.it/2011/09/into-notchs-mind-prelude-of-chambered.html).It's incredible how much you cand do, if you want and in small amount of time!

Then finally some decent roguelike tutorials from

[Trystan](http://randomtower.blogspot.it/2011/09/trystans-rougelike-tutorials.html)!

So I've started to use my library, MarteEngine (see

[Drone Defense](http://randomtower.blogspot.it/2012/11/drone-defense-02.html),

[Fuzzy](http://randomtower.blogspot.it/2011/09/fuzzy-is-out.html)) to develop a little roguelike, here last

[MarteEngine roguelike tutorial](http://randomtower.blogspot.it/2012/05/marte-engine-graphic-rogue-like_23.html).

But.. I was missing the point: understand the basics. So I've created

[CryptoRl](http://randomtower.blogspot.it/2015/08/cryptorl-release-10_28.html), with some limitations on my mind:

- small in scope: 3 type of monsters, 3 items
- few mechanics: attack, get item from ground, use it
- small iterations, develop quickly
- no graphics

**What went right**

- small scope: don't do too much, I have a lot of ideas, but .. keep it simple! (stupid, kiss :P)
- quick iterations: release somenthing, request for feedback, but as developer "see" your project working and growing is rewarding
- use a TODO list, note ideas, but keep organized: first bugs, then TODO and finally IDEAS

**What went wrong**

- interface: I don't like characters only interface, using mouse could help a lot to figure out what is going on!
- animation: many roguelikes demonstrate that today I can develop a game with simple graphics, but few animations can help a LOT

Now it's time to collect ideas and move to a new project!

## No comments:

## Post a Comment