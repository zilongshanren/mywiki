---
title: Archive for October, 2017
url: http://greyaliengames.com/blog/2017/10/
published: '2017-10-24'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

Click [here to wishlist](http://store.steampowered.com/app/427490/Shadowhand/) Shadowhand on Steam!

We’ve been working on two major things since the last update, and a few other things. Here’s the lowdown!

**New Enemies**

We added enemies into the second half of the game, which was a BIG task. For almost a year we’ve been sitting on the art for the remaining enemies because we knew it was going to take a while and there were a bunch of other things that needed doing more urgently.

Anyway finally they’ve all been edited and plugged into the game!

First Jake uses Photoshop to fixes errors in the source psd files. He check the poses, hands, weapons, outlines, transparency and other stuff. Then he plugs them into a master enemies psd file and scales and positions them to be consistent.

Then those images are exported and loaded into the game and offsets are calculated for enemy strikes on the player and vice versa, and gun smoke particles are added where relevant.

The following enemies were added:

– Soldier with pistol (a variant of a previous enemy)

– Art(hur)

– Gamekeeper (see screenshot above)

– Marsh Man Lance/Percy (2 versions)

– Marsh Woman Gwen

– Marsh Woman Guin

– Merl

– Ostler Joe (2 versions)

– Revenue Boss

– Revenue Man1

– Revenue Man2

– Lady Spry (2 versions)

– Shipwreck Sue

– A secret enemy

Enemies have between 3-5 stances and now there are over 200 enemy images in the game! (see image below)

**Enemy Properties**

Once the enemy graphics were in the game we made a giant spreadsheet of all of the enemies (see snippet above) in order to assign them properties such as health, defense, stealth, gold, special defenses, gear etc.

However, they all still need to be tested and balanced using the automated AI duelling system, which will be done soon.

**New Save System**

Another big change was that there’s now a new save system that basically records two different states: the state at the start of the chapter and the state mid-chapter.

This way if players fail a chapter and retry, or quit a chapter, the state can be reset back to the start of the chapter. The mid-chapter state is just the most recent save that gets loaded if the player shuts down the game mid-chapter OR if they retry a hand, perhaps due to losing a duel.

It was weirdly complex and took a long time to get right, and it’s a departure from the way that Regency Solitaire handles chapter/hand progress, but it was needed due to having an inventory system that can change mid-chapter.

**Chapter Cards**

Now that the enemies are done we were able to finalise the text and character images for the chapter cards (see image for Chapter 10 above)

These look pretty cool and we are pleased with how they turned out. Here’s another one…

**Misc stuff**

As per usual we did a bunch of other minor stuff including:

– Added a Play/Equip panel before puzzle hands so that players can swap out active/passive abilties.

– Fixed a bug with restarting a hand not rolling back some chapter stats for the current hand.

– Made mirrored throwing knife and rat particle effects for when they are used on the player.

– Added separate x offset for bombs hitting enemies so it doesn’t have to be the same as gun impact x.

– Enter and Space can be used to activate the Retry button on Level End screen if there’s no Next/Loot button.

– Added second blood splat/pow to pitchfork because it has two prongs.

– Made special weapon cards for the Ostler’s various punches.

– Made special weapon card for Whip Lady’s pistol.

– If there are two crates on a level the 2nd one doesn’t fade in! FIXED.

– Set music for all new enemies.

– Edited chapter names and shop message text.

OK that’s it for now. We’ll try and upload a video soon. We are getting there!