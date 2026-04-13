---
title: 're:Creation week #4. New graphics, chests, doors, screen transitions'
url: https://eliasdaler.wordpress.com/2014/08/03/recreation-week-4/
published: '2014-08-03'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Previous weeks**:

This week was totally awesome!

Dmitry has redrawn lots of graphics and the game looks a lot better now.

We’ve also decided to make character proportions more realistic which is also great.

Here’s the graphics comparison

![](../../assets/6ade3770797887ad.png)



I’ve also made invetory system and inventory menu.

![](../../assets/af3e82ce9d87c43d.gif)


It was pretty easy to implement. I created **InventoryComponent** which has **std::vector<std::string>** of item names. When drawing inventory, I get all the important info about the items from scripts by item name. Giving items to player is also easy, it’s just one line in script!

addToInventory(playerId, "DUCK")

Checking if player has item is also easy:

hasItem(playerId, "DUCK")

This function can be called in script so I can check this when player interacts with npcs. Something like that:

-- something in .lua script if(hasItem(playerId, "DUCK") then say("Where did you get that duck"?) end

![](../../assets/ba057d1dc5ff8963.png)


I’ve also made chests.

![](../../assets/afb1808dc0692473.gif)


Chest actually has three states: closed, opening and open

Opening state is important because I can show the item which player gets and then I call “open” function from script which gives some item to player and sets chest in “open” state. It’s also important when loading saved files. I need to set all opened chest states to “open” so player doesn’t get another item or hear opening sound.

Doors are very similar to chests but they have a neat feature which chests don’t. Doors can be automatically opened on some conditions. As you may see in the .gif above, the door opens when player kills the enemy. How does it work? Pretty easy. I have “isOpened” function in script which is called every frame. Something like that:

isOpened = function() if(killedEveryone()) then return true end end

![](../../assets/32eafa1dd3ae9805.gif)


When it returns true, the door goes to “Opening” state and opens.

I was worried that this will slow down the game but it’s actually working pretty fast and the game runs normally.

I’ve also made neat transition effects when player goes to another level.

![](../../assets/7a684e8cab332e3c.gif)



Thanks to guys from SFML forum who helped me achieve this (SFML already had pixelation shader so I didn’t need to write it from scratch)

And that’s all for that week. There’s not a lot left to implement to make a fully playable level! I think it will be ready by the end of this month and I will release the build to hear what people will say about the game. (I’ll probably get lots of critique, but that’s great if it’s constuctive!)

Piekielnie korzystny wpis, polecam ludziom

I don’t speak Polish, can you please translate your commentary into English?

Means: Hell of a favorable entry , I recommend people

Looks great!

Ha-ha, thanks. And that’s two years ago! Check out how it looks now! :D

I will, I’m working my way through the back blog posts. I’m also making a top down rpg and the scripting concepts have been SUPEF useful so far!!

Doh, super*

It looks great! Give me the source code please, I’m learning game development.

Thanks! The game is close sourced, sorry.

LOL at blatant request for source.