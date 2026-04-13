---
title: 6 software tools I use to make Game Art without being an artist
url: https://www.gamedeveloper.com/art/6-software-tools-i-use-to-make-game-art-without-being-an-artist
author: Mich Nannings
published: '2020-07-31'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# 6 software tools I use to make Game Art without being an artist

Being a programmer doesn’t stop me from making game art assets. If you go for a minimalism style and use good colors that fit well together you can make a game look good. I will show you the programs I use and the games I used it for.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Being a programmer doesn’t stop me from making game art assets. If you go for a minimalism style and use good colors that fit well together you can make a game look good. I will show you the programs I use and the games I used it for.

With only simple shapes like rectangles and triangles, you can come a long way. A successful indie game that utilizes minimalism is [Thomas Was Alone](https://store.steampowered.com/app/220780/Thomas_Was_Alone/). The game proofs that you don’t need to be good at art to make a game that a lot of players will enjoy. If you go for a style this simple almost all paint tools are sufficient. Gimp is free and open-source. By using simple art you focus on making the gameplay great. By incorporating a minimalist style and picking a good color scheme you can make a scene that is nice to look at but also fast to make. If you need help with finding a color scheme, sites like [colormind](http://colormind.io/) can help you out by generating colors that are complementary to each other. By adding juice to your game like screen shake, particles, sound effects, and tweening your characters and game menus players don’t care that your game doesn’t have graphics on par with Crysis.

For [Super Blue Boy Planet](https://store.steampowered.com/app/560260/Super_Blue_Boy_Planet/) I used Photoshop and Pixel Edit. Photoshop is great for doing almost everything but for pixel games and especially animations I rather use a dedicated sprite app. Photoshop does come with a frame to frame animator but to turn your animations into a sprite sheet you need customs [scripts](https://github.com/bogdanrybak/spritesheet-generator). Using a dedicated pixel art tool like [Aseprite ](https://www.aseprite.org/)is also much cheaper than Photoshop or if you are using a Game Maker the built-in sprite editor has all the features you need.

With this Voxel Editor, I made all the objects (the player, enemies, etc) that are visible in my game, [Voxel Bot](https://store.steampowered.com/app/1095370/Voxel_Bot/). Voxel-based models are just objects that consist of tiny blocks like Lego. Another way to see it is as pixel art as it was 3D. You start with a canvas and you just start placing cubes on cubes as if you are playing Minecraft. A very successful game that is made with Qubicle is [Crossy Road](https://www.crossyroad.com/). While I like this program there is another free alternative called [MagicaVoxel](https://www.voxelmade.com/magicavoxel/). This free editor is open source and actively maintained so I recommend checking this one out for sure.

This is a Unity specific plugin I use for all my 3D games. If you are already profound with Blender or other 3D programs you may stick with those but if you’re going for a simpler art style or just want to prototype levels then ProBuilder is great. For [Cube Mission](https://store.steampowered.com/app/1008740/Cube_Mission/) I was going for a world made out of cubes so I only needed the basic features of a 3D modeling tool. ProBuilder supports extruding, mirroring, vertex coloring, etc. to make all kinds of models. The thing I think is the best of all is that everything is in the editor so you don’t need to export your models from your 3D program to your Unity project.

In the past, it was called Adobe Flash but the program itself has not changed much except html5 export besides flash player exports. This program is widely used for thousands of flash games on the internet. You could make just the whole game including the code in Animate (coding in ActionScript) if you want to, but I only use the drawing tools. A pro of using vector over pixel art is that you can scale it as big as you want without seeing a degradation in quality. If you want to scale a pixel sprite you have to multiply everything by 2 or else you will see weird artifacts. For [Tricky Cat](https://store.steampowered.com/app/1042330/Tricky_Cat/), I went for a simple vector look and I used a very cheap drawing tablet to make everything. After exporting the cat png I used the Unity 2D animation package to rig the cat. Attaching the bones on different parts of the sprite. This is a very fast way of doing the walking and jump poses instead of frame by frame-based animations.

These are all of the programs I recently used. In the end, it’s not about the tools you use but the creativity and time you put into your projects.