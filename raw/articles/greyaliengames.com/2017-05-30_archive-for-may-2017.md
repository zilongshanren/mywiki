---
title: Archive for May, 2017
url: http://greyaliengames.com/blog/2017/05/
published: '2017-05-30'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

In my [last blog post](http://greyaliengames.com/blog/?p=2503) about [Shadowhand](http://www.shadowhandgame.com), I talked about how some card suits have the added bonus of charging certain weapons faster – a great way to get the advantage over your enemy in a fight through strategic card play.

For this developer diary I’m gong to show another way that we have used suits in the game, as part of another game mechanic.

**Introducing suit locks**

Here’s a reminder once again of the customised suits that we have developed for Shadowhand. Each suit has ten cards, numbered 0-9.

In our previous card game, [Regency Solitaire](http://store.steampowered.com/app/351090/Regency_Solitaire/), we introduced a mechanic called a Regal Lock, where removing a royal card (J, Q or K) was necessary to unlock certain cards on the play field. We thought this was a fun mechanic, and it allowed us to create some quite interesting and challenging levels.

This time around we have lost J, Q and K but we have more suits to play around with. This time some cards on the play field have a Suit Lock, which is only removed when a target number of cards of that suit have been matched. We can choose any number we like to vary the challenge. This lock shown in play takes nine oak cards to unlock! Don’t fear, we will run our automated game test on every level to check that they are actually possible to complete. But in some cases, it will a significant achievement to get that last card.

Mechanics such as training that unlocks weapon charging matched by suit, and the suit locks shown in this post add many layers of strategy. The core gameplay is based on a solitaire variant, which is already a strategy game.

We aim to give players something new by coupling RPG battles to card play rather than dice rolls. Gradually adding layers of mechanics and a huge array of character choices and mini deck-building opportunities will mean that there are as many types of strategy to beat Shadowhand as there are players.