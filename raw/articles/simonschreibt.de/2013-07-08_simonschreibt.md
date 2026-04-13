---
title: Simonschreibt.
url: https://simonschreibt.de/gat/1nsane-carpet-2-repetitive-worlds/
author: Simon
published: '2013-07-08'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Introduction

Forget history! The earth isn’t flat and neither it’s round! It is a **repeating** iteration of itself! … at least for todays topic: the repetitive worlds of [Magic Carpet 2](http://en.wikipedia.org/wiki/Magic_Carpet_2) and [1nsane](http://invictus.com/games/1nsane#).

(If you think this is blasphemy and wanna punish someone, please contact

[amassingham]on

In MC2 you fly on a magic carpet and shoot monsters. In 1nsane you do off-road races. The special detail: you’ll *never* reach a level border! You’re *not* slowed down. Not turned 180°. Not killed. The map just repeats and repeats and repeats…

The mini map of MC2. You can clearly see the repeating map:

The same issue can be seen in [1nsane](http://invictus.com/games/1nsane#) (thx to [bananaft](http://www.youtube.com/user/BananaftRu) for mentioning!) where you also have an endless repeating terrain (watch at the mini map!):

Logically the terrain geometry has to be seamless at the border but besides of that it was (at least for me) really interesting to think about the programmers side of this whole thing a bit more. I’ll trust the comments of the [reddit thread](http://www.reddit.com/r/gamedev/comments/1gi6np/magic_carpet_style_infinite_wrapping_terrain/) to “explain” it.

![]() |
What do you see when you look across the border and what happens when you walk over it?
re-coded something like this and “just” copied the terrain 8x around the map and re-positioned the player as soon as he “tried” to leave his map tile (see left image).This behavior can also be seen perfectly in 1nsane (white arrow in the image below). |

![]() |
With NPCs it gets complicated. For the game logic, every object exists only 1x and only in the central map! If you look at an enemy within your map, all is fine. The enemy position for game logic and rendering is the same.But what’s when you look across the border? Then the position for the game logic and the actually rendered position is different. |
![]() |
Next point: If you only take the central map into account, an enemy movement should look like this. Even if you don’t stare at the enemy. |
![]() |
But if you see this with a “multiple terrain” perspective look across the border, it will look like the enemy runs away from you (to attack you from behind). |
![]() |
When measuring the distance between enemy and player you have to take the map borders into account! Then you’ll see, that’s shorter to just rotate the enemy and walk across the border towards the player. |

You want more? [bananaft](http://www.youtube.com/user/BananaftRu) (he worked on games with this feature) mentioned much more technical difficulties:

- “Physics and collision detection have to deal with fact, that object,

that crossing the border can be in two (or even four) places

simultaneously, and have to collide with other objects from other side.” - “Ai and pathfinding (Bots should see through the border).”
- “Sounds should be properly positioned.”
- “Effects and trails. Just imagine particle emitter crossing the

border, and what you should do to make it properly visible from both

sides?” - When there’s a background like in Insane 2, you shouldn’t use detail objects like trees because this would help the player to notice, that the background never gets nearer (
[watchable in this Youtube video](http://www.youtube.com/watch?feature=player_detailpage&v=EL-A9Sv8Cxk#t=0m39s))

Thx [elecdog](http://www.reddit.com/user/elecdog) (he creates the game [Arcane Worlds](http://ranmantaru.com/games/arcane-worlds) with endless terrain feature) for answering the following question:

- The game logic only knows
*one*instance of every object, but if you would increase the field of view or the view distance – could you actually

see them several times?

**The answer**: Yes. But since it makes no sense, it’s better to optimize it that way, that the FoV & view distance is limited.

Last thoughts

I’m sorry that it got a bit text- & tech-heavy. But i found the whole issue very interesting. *Especially because my brain accepts the trick. It doesn’t say “That’s weird!” it just relaxes and is happy about this huge free world….even when i stumble about the same stuff again and again.*

After some thinking it’s clear why the brain accepts this world-behavior: since our own world is round, the real world behaves exactly the same. The game world ist just a very small sphere. :)

I really like that you don’t have map boundaries. Imagine a Battlefield air to air dogfight without turning around all the time. In the case of Battlefield: if you leave the map…you die.

Last words

I hope you enjoyed this article and if you did, feel free to contact me via [Mail](mailto:simon@simonschreibt.de), [Twitter](https://twitter.com/simonschreibt) or [Facebook](https://www.facebook.com/simonschreibtblog). I would love to hear your opinions, topic-suggestions or just a “Hello!”.

![](../../assets/ba0680151067ebbc.png)

**BmB**mentioned that such repetitive worlds where planned for Battlefield 1942 “but they scrapped it because you were able to shoot yourself in the head with a sniper rifle.” – How cool and crazy at the same time is that? :D Thanks BmB!

Introduction

Forget history! The earth isn’t flat and neither it’s round! It is a **repeating** iteration of itself! … at least for todays topic…

Well, I think this is madness and this is blasphemy!

But, seriously, I would consider repositioning the terrain according to the player position. Always place up to 4 copies of it around the players position (or more copies, if your player can see further). This solves all kinds of problems with multiple positions and what not.

This should work with static terrain. If your map is allowed to change you really need to store the changes somehow and reproduce them upon a visit of this ‘sector’.

This guys here did an almost infinite game-world, without resorting to repeatable patterns: http://www.altdevblogaday.com/2012/04/27/the-difficulties-of-an-infinite-video-game-world/

Really interesting link! Thank you! And of course thank you for your comment :) I also like the design of your blog! Unfortunately i don’t understand the content :D

the easyest solution to repetive terrains is simply tiling the terrain and ignoring that it tiles, so the game happens in the square and you can go outside like forever (but there are no objects to populate the terrain, so its boring to run around outside of the terrain)

Jup that’s right. Delta Force did it like you described, as far as i know.

Infnite square tiling like this is analagous to an unwrapped torus.

http://en.wikipedia.org/wiki/Toroidal_coordinates

So there’s one way of presenting this where all positions are within the same closed space.

But asteroids had this same kind of movement, only the screen was the space you could move about in rather than a larger presentation of it.

1nsane is likely doing the teleport at frame with tiles trick. The terrain could be a calculated set of quads and the mapping just tiles naturally along with the large scale terrain’s UV space.

Thank you for your comment! I’m not sure if i understand the Wikipedia article (too much math) but i’m sure some other readers will. :)

Hi. Check implementation of infinite landscape in Arma series battle simulator. There is air battles over huge map with infinite boundaries. When you leave game map on jet you can permanent fly over infinite landscape and fast get back to game map if turn back.

Wow, thanks for the hint! :) Didn’t know that!

In an interview with Game Informer, Lars Gustavsson reveals that Battlefield 1942 was originally to have infinitely repeating worlds, but they scrapped it because you were able to shoot yourself in the head with a sniper rifle.

https://www.youtube.com/watch?v=4tS74Adi_zs

Thank you for the info! That’s crazy :D I added the video as update to the article: http://simonschreibt.de/gat/1nsane-carpet-2-repetitive-worlds/#update1

I recently somehow landed on your site and bookmarked it because I saw the interesting topics you talk about.

Now I came back and had a closer look and what do I find here: The answer how 1nsane and Insane 2 managed to have repetitve worlds!

I thought about this problem from time to time, but never figured out how you would handle AI and other players.

I’m excited to see what other treasures I’ll find here! :)

Glad to hear! Have fun exploring :)