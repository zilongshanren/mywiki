---
title: Further deets
url: https://etodd.io/2010/12/28/further-deets/
published: '2010-12-28'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Further deets

Okay, it's time to shed some light on this project.

First off, my goal is to release on Xbox and, if possible, Steam (if not, I'll be looking at other online stores). I figure these are the two largest, most practical target markets. The release price will be between $1 and $5, with 100% of the proceeds going to charity (more on this later...).

There are two main themes I want to nail in this game. The first is giving the player freedom to alter the game world; to literally change the world geometry by performing sweet parkour moves (jumps, flips, slides, etc.). The idea is, to create a wall, you simply jump into mid-air and perform a wall jump ![dropship](../../assets/278bdae7a08fd6ef.jpg)


*as if the wall was there*, and poof, it's there. Need to get through that annoying concrete barrier? No problem, slide right through it like it's butter.

The second theme is learning. The story I've developed so far focuses on the main character's journey from the ordinary to the extraordinary. I want the player to mirror this journey, by mastering the different combos and moves as they are unlocked. I think this will greatly help people attach emotionally to the main character.

To make things even more interesting, the player will have to battle the level itself to win the game. By that I mean, parts of it will come flying off, collect into autonomous entities, and attack the player. Or maybe help him, who knows. The possibilities are endless!

Now on to some technical details and progress reports. As some of you know, I was able to get the build you saw in the last YouTube video running on an Xbox, but I ran into some serious performance problems. Namely, the CLR version that runs on Xbox has horrendous floating-point performance, which seems to render most physics engines useless for more than a hundred or so blocks. Obviously, I'm going to need more than that. I debated writing my own engine, which could take advantage of the cubic nature of the levels and make a lot of optimizations, but decided it wasn't worth it. I think I'm going to write some flocking algorithms or just geometric functions to emulate the complex behavior exhibited in the last tech demo. Plus, that way I'll have more control over the cubes' movement.

So what has been accomplished since the last tech demo? Here's a run-down:

- Split-screen support with multiple players
- Keyboard and Xbox controls are interchangeable, and the controls and available moves are much better (still very much under construction though)
- Multiple types of blocks (so far, just destructible and indestructible blocks)
- Texturing! I successfully twisted the arm of the Blender-FBX-XNA content pipeline into giving me normal maps and diffuse textures. The environment shader automatically calculates UV coordinates based on the position of each pixel in space, which means textures are seamless between adjacent cubes.
- Hardware instancing (the entire level is now rendered in two draw calls!)
- Sound! You can now place ambient sounds throughout the level, and there are a few basic sounds already bound to player actions, like jumping.
- Some HUH-YUGE improvements to the editor, including an abstracted editing interface. It's easy to write new editable classes, and it's easy for users to pick up. The level geometry is now stored in binary, while the object mark-up is human readable. I also added support for variable brush radius, which means it's now very easy to create organic geometry (see the background of the first screenshot).

So that's what I've been up to. This project is just now starting to take off, and I can't wait to see the result. Watch this space for more updates!

What I'm working on now:

- Tweaking the controls and fleshing out new combos.
- Simple global illumination. I'm thinking of doing some quick density queries on the level geometry, then dumping the results in an 8-bit 128x128x128 volumetric texture, which I can then sample in the environment shader. Hopefully the texture filtering will smooth it out enough to look good. Or at least, better than Minecraft's lighting.