---
title: Archive for May, 2013
url: http://greyaliengames.com/blog/2013/05/
published: '2013-05-21'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

Basically I’ve mostly been doing one thing since the last update. It’s just that it’s quite a complicated thing 🙂

**Here’s what I’ve done:**

– Read in the xml animation file for Earth and got it working. The original game has a complex animation system that can handle way more than most normal animation systems. I’ve had to write code to read and interpret the xml file and make it work with my sprite engine. This was not easy and there’s still a lot to do.

– Read in the xml sprite files for Earth and got it working. Each sprite, which I’m calling a “game object”, can be made up of several animated sprites, or even several other game objects. This was also pretty complex especially when some parts of a game object control other parts of a game object!

– I made a test screen to show the animations and sprites that I’ve read in. This has proved very useful and I’ve made a video about it (see below).

– Finally I made code to create individual “instances” (that’s a programming term) of a game object using a template that has been read in from the sprite xml file. The in-game aliens are now instances based on a template and you can see that they animate and blink in the video I made.

**Video!**

This is my first developer video diary. In it I show of the game a little bit and then talk about the test screen I made to test animations and game objects (sprites).

I Hope you enjoy it!

**Next up**

– Keep going with the xml interpretation code. There’s still a lot to do such as making the aliens move around, making them fire, making the player ship animate as it moves, making particle effects for firing etc. All of this is controlled via the vast xml files that Cas and Chaz (the original developers) made. So I’ve got my work cut out for me!