---
title: Archive for July, 2017
url: http://greyaliengames.com/blog/2017/07/
published: '2017-07-31'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

**Weapon Modifiers**

I’ve had a busy couple of days adding some neat features to the game.

First I added the ability to show a modifier e.g. +2 as part of the weapon card name (see screenshot above). This means that there can be more powerful versions of weapons found earlier in the game. I also added the same ability to Grog Bombs because they deal a fixed amount of fire damage and later in the game the player will need more powerful ones.

This turned out to be quite a big task because I had baked the card names onto the card graphics (I was going to change to dynamically drawing them if we ever localise the game). However, now that I needed to display +X next to the name I basically had to re-export all the weapon and gear cards in both small and large format which was 136 exports!

I also needed to create a special new small font to draw the card name. It’s no good scaling down a larger font as it just looks bad, it’s always better to export a font at the exact size it’s planned to be used in-game for clarity.

**Inventory Stacking**

I coded gear stacking so that the player’s various bombs and potions can be stacked in the inventory instead of taking up zillions of inventory slots. The quantity the player has “in stock” is shown on the bottom right of the card on both the small and large versions.

Coding the stacking was a bit complex as it had to handle taking one off the top of the stack and allowing it to be equipped in one of the player’s 3 gear slots and vice versa.

Furthermore I decided to auto-sort the inventory as well so that the weapons/outfit/gear/ability tabs are always sorted in a sensible order. However, new items will still appear in the top left of the inventory tab (and be marked with a new icon) so that players can check them out. This is basically what Dark Souls and the latest Zelda does, so it should be OK 🙂