---
title: Re:creation dev log. October 2014. Halloween, ghosts and scripts!
url: https://eliasdaler.wordpress.com/2014/10/30/recreation-dev-log-october-2014/
published: '2014-10-30'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Happy Halloween, everybody! **Re:creation** is about undeads and I think its theme fits well with Halloween. It fits even more if I add some pumpkins and scarecrows!

![](../../assets/94f12e6b5214d6e8.png)



I started to work on the City of Undead. This will be a central hub in the game where you meet many important characters and rest after wandering around dangerous places full of humans who’ll try to kill you to get experience points.

The statue in the center is dedicated to the yet unnamed hero from the North who once tried to protect undead after he realized their peacefulness. He spread his message around the North but was killed by the men who still viewed undeads as things for killing and free work force.

I’ll write about other characters soon.

![](../../assets/6a2a15648087e0c7.png)


Here are some other things on which I worked this month.

## Arrows

![](../../assets/3ea31edbea14918d.gif)


This was harder to implement than I thought. But it let me understand how useful and convenient entity/system/component model is!

Let’s look at the arrow. This is what it has:

- Position – PositionComponent
- Sprite – GraphicsComponent
- Velocity – MovementComponent
- Collision – CollisionComponent
- Damage – DamageComponent

So, I didn’t need to add any components to make arrows! Neat.

Let’s look at the collision logics. When the arrow collides with something, a Lua function named **collide** gets called.

This function has two parameters – the first is arrow entity id, the second is an id of an entity with which the arrow collided.

Here’s how the Lua function looks:

collide = function(this, second) if(getCollisionType(second) == "solid") then -- arrow hit something solid like a wall or a static object playSound("res/sounds/arrow_hit.wav"); setState(this, "ArrowStuckState") end if(not isParent(second, this) and -- don't hit self hasHp(second) and getState(second) ~= "DieState") then -- hit an enemy playSound("res/sounds/arrow_hit.wav"); killEntity(this) -- destroy the arrow end end

Note: every function in this script is actually a C++ function. So ,for example, when I call **hasHp** function from Lua the corresponding function in C++ gets called and returns a boolean:

inline bool hasHp(int entityId) { std::shared_ptr e = game_system.em->getEntity(entityId); if (e) { HealthComponent* hc = e->get(); if (hc) { return true; } } return false; // doesn't have HealthComponent }

This is great because a person who writes scripts doesn’t have to know about components and how to get the needed information from them.

I do know how components work, of course (that’s because I’ve programmed them, duh)… but hey, I don’t want to write the same code over and over!

What is **ArrowStuckState**?

An arrow goes into this state when it hits something solid. It becomes stuck in this object, its appearence is changed a bit, its speed is reduced to zero and the arrow gets removed after certain amount of time.

![](../../assets/09abe25f5fd405f1.gif)


What about tiles? Some of them are solid, but tiles are not entities so collide function doesn’t work there. No problem, I just added **collideWithLevel** function which takes a **tile id** instead of an **entity id** and works pretty much similar with a few exceptions.

And that’s it! This is all I had to do. Few lines of C++ code, some Lua scripting – it’s all it takes. (Oh, and art. But it wasn’t very difficult).

I wonder how many hours will entity/component/system save me in the future. I’ll write about things like this to show how cool ECS is. I wish there were more articles about it.

## Worked on the main gameplay mechanic

In **Re:creation** you can turn into enemies and use their abilities to progress through the game. But you can’t get too far away from your own body, so you have to unlock the paths for yourself to progress. I’ve implemented neat selection using your ghost form (not to be confused with **Ghost Mode** which is used for testing!). Here’s how it looks!

![](../../assets/725dd8048ea71ae0.gif)


## Ghost mode

![](../../assets/955b7aab644002f7.gif)


This is one of the most convenient things for testing levels. Press “**G**” to turn into a ghost. Player can pass through everything and moves a lot faster. This is done by setting size of collision bounding box to (0,0) so ghost cannot collide with anything.

I can quickly go to any part of the level using that mode. Neat!

## Cornering

This is one of the things which are almost always unnoticed if improved correctly. It prevents you or other moving objects from getting stuck around the corners because their collision bounding box intersects slightly with the other object’s bounding box.

![](../../assets/a00aa0b25de06bc2.gif)


See? The player gets a little push moving him to the right, so he can go up.

Here’s how I’ve implemented it.

I use SAT for AABB’s for collision checking and resolution. I get intersection 2D vector which shows me how much one object intersects with another. By moving one object by the lowest coordinate of this vector (x or y) I can easily resolve the collision. [You can read about this method here](http://codeblog.shawson.co.uk/8-week-game-competition/how-i-tackled-collision-detection/) and [here](http://www.metanetsoftware.com/technique/tutorialA.html).

Look at the picture below. The character moves up, but he’s stuck, because he slightly intersects with the gray box.

![](../../assets/923702a3ba7d10f9.png)


In the situation like this, intersectionDepth.x will be small compared to the character’s width. So when we resolve the collision by changing his y coordinate, we also move him to the right with the character’s speed until he can go up again. You can easily figure out another situations yourself.

## What’s next?

I have lots of plans for the next month. I want to finish the first playable level, polish it and release the first public build to get some feedback! I don’t have many features left to program, so it’s mostly about art, level design and story writing. These are the things I’m not very experienced with, so it’s going to be hard!

So, this month will probably bring lots of cool updates, so subscribe to my blog or [twitter](https://twitter.com/eliasdaler) so you don’t miss them!