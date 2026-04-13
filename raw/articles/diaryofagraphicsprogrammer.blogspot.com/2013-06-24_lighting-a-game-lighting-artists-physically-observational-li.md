---
title: Lighting a Game / Lighting Artists / Physically / Observational Lighting models
  / Bounce Lighting
url: http://diaryofagraphicsprogrammer.blogspot.com/2013/06/lighting-game-lighting-artists.html
author: Wolfgang Engel
published: '2013-06-24'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Here is a way on how modern game engines can light scenes. I was just describing this in a forum post: the idea is following what the CG movie industry is doing. Placing real-time lights happens similar to CG movies. In CG movies we have thousands of lights and in games we have now dozens or most of the time 100+ lights in scenes. Compared to switching from observational to physical lighting models, this makes the biggest difference. Then each of those lights can also cast bounce lighting which is another switch for the artist.
So in essence artists can place lots of lights, switch on / off shadows on each light and switch on / off real-time GI on each light. The light / shadow part was already possible on XBOX 360 / PS3 but now on the next-gen consoles we also have bounce lighting per light. That gives lighting artists a wide range of options to light scenes.
A lighting setup like this would be overkill in a game like Blackfoot Blade, where you fly in a helicopter high above ground. We have only a few dozen real-time lights on screen without shadows (each rocket casts a light, the machine gun of the helicopter, even the projectiles from the tanks and the flair). The game runs also on tablets.
With any ground based game like an open-world game, lots of lights makes a huge difference to light corners and the environment. It is one of those "better than real" options that lighting artists like.
My point is comparing the switch from observational to physically based lighting models with switching from a few lights to lots of lights. The later gives you much more "bang for the buck", so you want to do this first. Any scene in shadows will not look much better with a physically based lighting model if you only use one or a few light sources but with lots of lights you can make it look "better than real".

## No comments:

Post a Comment