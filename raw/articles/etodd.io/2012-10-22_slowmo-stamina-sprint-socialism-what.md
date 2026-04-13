---
title: Slowmo! Stamina! Sprint! Socialism! What?
url: https://etodd.io/2012/10/22/slowmo-stamina-sprint-socialism-what/
published: '2012-10-22'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Slowmo! Stamina! Sprint! Socialism! What?

### Stamina and Sprint

I finally realized that speed is perhaps the most important resource in a Parkour game. Up until now, Lemma hasn't really understood the concept of "faster" and "slower"; you were always going the same speed. Acceleration from a dead stop was almost instantaneous and the Parkour moves didn't change your speed (with the exception of wall-running).

With this in mind, I decreased the acceleration a lot and made all the moves preserve your momentum. To make a longer jump, you'll need a running start. I also put in some simple combos. For example, doing a roll immediately followed by a jump lets you jump a lot farther.

This is where the new sprint ability comes in. Not only does it make you run faster, it also makes every other move more powerful as well. At the moment, you can sprint for about 15 seconds before depleting your stamina. Without sprinting, stamina lasts about 10 minutes. Stamina is recharged by collecting energy pickups that respawn throughout the levels.

Here's a screenshot of the stamina meter and some energy pickups. The edges of the meter turn red when sprinting.

### Slowmo

I'm calling this "slowmo", but there's a lot more to it. This is a new experiment that tries to encourage "flow" by predicting where you will be in a few seconds and building blocks there to help you.

Here's how it works. While mid-air, you hold Shift. The game goes into slow motion and presents you several options in the form of transparent blocks. (Note that slowmo burns stamina almost as fast as sprinting). You release Shift to speed everything back up. Then, if you perform a Parkour move on a transparent block, the block becomes solid (at the cost of more stamina).

Screenshots and text don't do it justice, but I don't have time yet to make a video. Sorry!

This may or may not make it into the final version, but so far it seems to work pretty well. I'll keep polishing it this week and start working on all these enemies I keep promising. I did a ton of other work this week too, but it's mostly boring under-the-hood stuff. I'll let you know when more cool stuff surfaces. Thanks for reading!