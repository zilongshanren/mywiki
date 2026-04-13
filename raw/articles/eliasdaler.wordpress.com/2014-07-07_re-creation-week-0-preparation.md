---
title: 're:Creation Week #0: Preparation'
url: https://eliasdaler.wordpress.com/2014/07/07/week-0-preparation/
published: '2014-07-07'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This week I don’t think I’ve accomplished something really huge, because I’ve decided to finally rest after month of studying hard. But now I can work almost full-time so lots of changes will come, I guess.

But still, I’ve managed to develop some cool stuff.

# Game

This isn’t really first week I’m programming this game. I’ve spent some month on engine and level editor, but this is the week I’m starting to see the game itself!

It’s called **re:Creation**. It’s oldschool top-down action rpg where you play as undead knight who wants to seek revenge for his death and free people from evil wizard who used trapped demon’s soul as the power source for 800 years. Here’s what was implemented:


## Runtime script reloading

Well, this thing is actually amazing and useful. I can now reload scripts when the game is running. That means that I can change lots of things without the need to recompile or restart the game. I think this will save me lots of hours.

[http://gfycat.com/FlakyExemplaryAmethystsunbird](http://gfycat.com/FlakyExemplaryAmethystsunbird)

**Advanced script support and dialogues**

![](../../assets/7c9b7a00191aa561.gif)

Witch can heal the player now

This one is actually one of the most impressive things I’ve ever done, I think. I was using Lua as configuration language most of the time, but I can use even more now.

I’ve spent some time messing around with different Lua/C++ libraries and I think [LuaBridge](https://github.com/vinniefalco/LuaBridge) is the best. I think I’ll rewrite [third part of my Lua/C++ tutorial](https://eliasdaler.wordpress.com/2013/11/30/lua_and_cpp_pt3/) which will show how to use it.

My game uses entity/component/system and each entity can be accessed by integer id. Here’s how I can get health value of some entity:

// in C++ std::shared_ptr<Entity> e = entityManager->getEntity(entityId); HealthComponent* hc = e->get<HealthComponent>() int health = hc->getHp();

Yeah, this is quite verbose. I didn’t want to translate it 1:1 to Lua, because it would be much easier to have some wrapper function, which only needs entity id to get its health value. It will be easier and safer to use it this way

// C++ int getHealth(int entityId) { std::shared_ptr<Entity> e = entityManager->getEntity(entityId); HealthComponent* hc = e->get<HealthComponent>() int health = hc->getHp(); return health; }

Of course, error checking can be done to improve function safety:

int getHealth(int entityId) { std::shared_ptr<Entity> e = getEntity(entityId); if(e) { HealthComponent* hc = e->get<HealthComponent>(); if(hc) { return hc->getHealth(); } } return -1; // entity not found or doesn't have HealthComponent }

Let’s get to something more practical. I’ll show how witch in the gif above is scripted

I have **witch.lua** script which has a structure like this

Witch = { ... -- some components InteractionComponent = { interactionRect = { -16, 32, 64, 32 }, interact = function (firstId, secondId) maxHp = getMaxHp(secondId) if (getHp(secondId) < maxHp) then say("Let me help you, stranger.") setHp(secondId, maxHp) else say("Come back when you are\nwounded.") end end } }

I can get “interact” function and don’t even need to harcode witch’s behaviour! This is so cool!

Ah, and I’ve also added lots of error checking which is something that takes a lot of time but isn’t seen by many. If you misspell some name of a function, you get an error and the game ignores it.

![](../../assets/4b53a05d6387e7b4.png)


## Improved level editor

Added snapping to grid and help menu. Nothing very special

![](../../assets/4e83aa92d0497a44.png)


Well, that’s it for this week. I’ll try to work very hard this week (I hope I won’t be interrupted too often) and will post the next update in a week!

# Other

Read a cool book. [“Game Project Complete”](http://www.amazon.com/dp/B00INF6MGA) by [Thomas Schwarzl](http://www.amazon.com/Thomas-Schwarzl/e/B00HWFIYQS/ref=ntt_athr_dp_pel_1). Very motivational and useful. Makes me want to become more disciplined. I cannot recommend this book enough. :)

I am also reading [“Peopleware: Productive Projects and Teams”](http://www.amazon.com/Peopleware-Productive-Projects-Teams-3rd-ebook/dp/B00DY5A8X2/) by [Tom DeMarco](http://www.amazon.com/Tom-DeMarco/e/B000AP7OPO/ref=ntt_athr_dp_pel_1) and [Tim Lister](http://www.amazon.com/s/ref=ntt_athr_dp_sr_2?_encoding=UTF8&field-author=Tim%20Lister&search-alias=digital-text&sort=relevancerank). It’s a really great book about human errors in IT and why managers fail to control projects efficiently.

I also recommend you to watch [this awesome talk](http://youtu.be/L7EGIt3-WUQ) by Jeff Atwood. The most important points for me were “**Embrace the suck**” and “**Do it public**“. Well, as you can see (look at this post!), I do these things. Nice.

![](../../assets/399c98fa589d1956.gif)


Great job! This is a cool looking project! How did you accomplish the in-game script refresh? That is incredibly impressive.

Thanks a lot!

Well, there’s nothing special about it. I just reconstuct each entity again from the script calling it one more time :)

Very nice :)