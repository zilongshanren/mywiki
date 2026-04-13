---
title: Archive for September, 2017
url: http://greyaliengames.com/blog/2017/09/
published: '2017-09-25'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

Click [here to wishlist](http://store.steampowered.com/app/427490/Shadowhand/) Shadowhand on Steam!

Since the last post we’ve mostly been designing and implementing some new lock and key types for the game. That’s gone well and they are nearly done – more on that below. But we’ve also done a bunch of other things.

**Balancing Ability Card Charges**

The image above shows all the active and passive abilities available in Shadowhand. The active ones require charging by removing playing cards from the tableau before they can be used.

The required charge varies from 40 to 70 which basically means somewhere between one and two hands of cards. I spent a while working out their relative strengths before setting these values. If you boost your willpower chracter stat you can make them charge faster, which can definitely come in handy.

**Character Stats**

Speaking of character stats (see image above), I also spent some time evaluating the relative effectiveness of our game’s unusual list of character stats and then balancing them. These stats don’t directly affect combat like most RPGs, they affect the cards instead.

I’ll still need to run some tests on the active/passive abilities and the character stats later on to check that my balancing guesstimates are OK.

**Gold crate**

A recent small addition to the game is to have a gold crate which is hidden under cards. It won’t occur very often but will be a nice treat when it’s found.

**New story/goal items**

The main bulk of last week’s work was designing story/goal items to uncover under cards, and some new locks and keys to add flavour to the game (more on locks and keys below). The wanted posted above is an example of a story/goal item. The story/goal items occur on specific chapters and are mostly related to the plot except for a special bonus item…

![LockKeyPlaceholder](../../assets/4358e27c3adf0fc3.jpg)


*The image above contains placeholder art*

**New keys and Locks**

Some of the new locks and keys are related to the plot and only occur on specific chapters, but others have been designed to be resued on several chapters such as the lantern and dark card, and the torch and gunpowder barrel.

Notice that we’ve also added some large locks to the mix. These will cover lots of cards and so will force the player to complete one half of the tableau first before they can proceed. Also we can hide cool things under them like crates of gold, potions, bombs and story/goal items.

**Misc stuff**

Here’s all the other stuff we got done:

– Reviewed the story to make sure it all makes sense.

– Added support to game and level editor for new lock/key types.

– Plugged all the new story/goal items into the game and coded goals for them.

– Wrote found item messages for the new story/goal items.

– Set placeholder goals for all the chapters in the game. I’ll balance these later.

– Plugged all the new lock/key types into the game and made them work except for particle effects.

– Added in placeholder sounds for new lock/key types. Probably most of them will be final.

– Coded lantern with overlay glow under mouse pointer when carrying lantern.

– Added particle effect for using lantern on dark card.

– Changed Prosperity stat to a chance to double gold award from under card piles.

– Made sure retrying or quitting a training chapter removes the training.

– Fixed a rare bug with using Charging Stallion on last card in a duel layout. Found by a beta tester!

– Changed the way “new” stars work on inventory tabs. They now clear as soon as the tab is viewed even if you haven’t checked out all the new items on that tab.

– Made new weapon base cards with “damage” label on them to make it clearer.

– Added page up/down to level editor to cycle through levels linearly.