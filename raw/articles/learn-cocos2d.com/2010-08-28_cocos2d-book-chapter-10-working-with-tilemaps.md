---
title: 'cocos2d Book, Chapter 10: Working with Tilemaps'
url: http://www.learn-cocos2d.com/2010/08/1600/
author: Virag
published: '2010-08-28'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 10 - Working with Tilemaps

This chapter dives into the depths of the CCTMXTileMap class and how to create, iterate and modify tilemaps in code, including isometric and hexagonal tilemaps. Of course there will be an introduction to the [Tiled Map Editor](http://www.mapeditor.org/) as its the primary tool to create TMX tilemaps that cocos2d supports.

The chapter 11 will then use this newfound information and I’ll walk you through making a scrolling tilemap game, since simply loading, modifying and displaying a tilemap would just be half the story.

### Summary of working on Chapter 9 - Particle Effects

This chapter was fun. Particle effects are fun indeed. That is, unless you need to tweak them in code only. I did do that an did my best to describe what each CCParticleSystem property does to a visual effect, although some things you’ll have to see for yourself. You’ll find a lot of detailed information on how to setup or simply modify a particle system in code and a couple tips for designing good particle effects.

Of course with ![shootemup-withparticles](../../../wordpress/wp-content/uploads/shootemup-withparticles-300x156.png)


[Particle Designer](http://particledesigner.71squared.com/)everything changes. Designing a cool particle effect suddenly goes from a treadmill to a mesmerizing activity that you can waste countless hours on. If you check Particle Designer’s Online Library you’ll find four of the Particle Effects that I designed and submitted, starting with the “Colorful Burst” effect. Have a look!

Obviously these cool effects needed to go somewhere, so I added them to the Shoot ’em Up game as you can see in the screenshot (the boss just exploded into purple smudge). Along the way you learn how to load the particle effects created by Particle Designer of course.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi,

I recently purchased this book, based on the blurb mentioning hexagonal

tilemaps. I can’t find any reference to code for hexagonal tilemaps that

is like the tutorials for orthogonal or isometric tilemaps. Most of the examples for hexagonal TMX tilemaps is missing something, so it is difficult to use or understand. I am hoping since the blurb mentions it, you might have the code in your manuscript and hopefully post it - I would really love to be able to control my maps as hexagonal designs the same way as the other protocols!

Thanks!

If you are referring to the hexagonal tilemap demo I posted on Indiepinion, that was a test I did a while ago but ran into so many issues that I abandoned it. The built-in support for hex tilemaps in both cocos2d-iphone and Tiled Map Editor are rather limited, therefore I didn’t include this in the book. And my example was far from usable either. I created it primarily to have hex tilemaps with the corner at the top (cocos2d doesn’t support that).

Thanks for replying - I have found several different ways to do this,

but I think I am going to have to go back to an orthogonal map until I have a bit

more experience!

One more Cocos2d tool to add to the fray:

https://itunes.apple.com/app/particle-creator-for-cocos2d/id564925232?mt=8

This is a particle editor for the iPad only.