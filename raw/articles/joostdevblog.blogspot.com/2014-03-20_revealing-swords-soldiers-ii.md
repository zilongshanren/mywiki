---
title: Revealing Swords & Soldiers II
url: http://joostdevblog.blogspot.com/2014/03/revealing-swords-soldiers-ii.html
author: Joost van Dongen
published: '2014-03-20'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

We recently announced that we our new game is Swords & Soldiers II. We didn't actually show any real gameplay yet, so today brings an exciting moment: here's what it looks like! It’s beards, mead, sheep, demons, axes, wenches and barbecues! Hope you like it!

This looks really well polished, art especially. Absolutely impressive, a huge leap since Swords & Soldiers...

I've always wondered how do you handle this heavy art style and keep the assets size reasonable. Blurry backgrounds I get, but my png's become size monstrosities very soon regardless. Now, I know you've already posted about the animation process last year, but perhaps you can elaborate about the actual graphics handling? maybe with some words about resolution, scale and pixel density :) oh! and Spritesheets! Also, how do you do Frame-by-Frame animation (for non-particle effects) in the engine? I mean, you obviously don't draw it FBF directly in AE, right?! Is it fully drawn in Photoshop? sounds very time consuming...

The main thing is that we just use enormous amounts of texture space. Our texture budget for Swords & Soldiers 2 is currently 550mb (might even become a bit more). Also, we pack sprite sheets a bit more efficiently than a simple grid, so we eliminate some waste from the difference in height between frames.

As for our animation workflow: all actual animations are made in After Effects, using a combination of frame-to-frame handdrawn animation and deformations. The handdrawn frames are drawn in Photoshop. Some of our artists also use Flash because it is easier than After Effects for completely frame-to-frame animated things like flags or explosions.

This looks really well polished, art especially. Absolutely impressive, a huge leap since Swords & Soldiers...



ReplyDeleteI've always wondered how do you handle this heavy art style and keep the assets size reasonable. Blurry backgrounds I get, but my png's become size monstrosities very soon regardless.

Now, I know you've already posted about the animation process last year, but perhaps you can elaborate about the actual graphics handling? maybe with some words about resolution, scale and pixel density :) oh! and Spritesheets!

Also, how do you do Frame-by-Frame animation (for non-particle effects) in the engine? I mean, you obviously don't draw it FBF directly in AE, right?! Is it fully drawn in Photoshop? sounds very time consuming...

The main thing is that we just use enormous amounts of texture space. Our texture budget for Swords & Soldiers 2 is currently 550mb (might even become a bit more). Also, we pack sprite sheets a bit more efficiently than a simple grid, so we eliminate some waste from the difference in height between frames.


DeleteAs for our animation workflow: all actual animations are made in After Effects, using a combination of frame-to-frame handdrawn animation and deformations. The handdrawn frames are drawn in Photoshop. Some of our artists also use Flash because it is easier than After Effects for completely frame-to-frame animated things like flags or explosions.

Thanks for the reply! I try to keep my mobile targets under 50mb because of the potential players loss, but maybe It's just a personal phobia...




DeleteJoost, those enemy monsters had better be a playable faction. Fell in love as soon as I saw the huge lizard base.

ReplyDeleteOf course, duh! :D

Delete