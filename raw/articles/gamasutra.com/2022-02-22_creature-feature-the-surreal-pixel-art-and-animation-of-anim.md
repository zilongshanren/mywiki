---
title: 'Creature feature: The surreal pixel art and animation of Animal Well'
url: https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well
author: Chris Kerr
published: '2022-02-22'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Creature feature: The surreal pixel art and animation of Animal Well

'I like to try to guide the player into thinking they fully understand something, and then reveal that they don't.'

![Key artwork for Animal Well Key artwork for Animal Well](../../assets/5dfc579aba3111bf.png)

There's something both unnatural and irresistible about [Animal Well](https://www.playstation.com/en-us/games/animal-well/). The surreal title hangs in the void like the lure of a patient anglerfish, pulling you in with the promise of fantastical adventure before turning the world on its head.

In the dense, pixel art labyrinth that spilled from the mind of sole developer Billy Basso there is beauty and danger in equal measure. Environments pulsate and glow with an otherworldly verve, bursting into life as players attempt to unlock the secrets of the unfamiliar puzzle box they now inhabit. But there are terrors lurking in the dark. Creatures of unknown intent wondering how best to deal with the interloper fumbling through their forsaken domain.

When I first locked eyes on the indie title [during the recent PS Indies showcase](https://www.youtube.com/watch?v=X4i5CMOliF0), I was taken by how much detail and flavor had been crammed into its pixel art world. There's no doubting the versatility of the aesthetic at this point, but Animal Well's combination of lucid animation and fizzing visuals delivers something that feels raw and evocative.

Drunk on that beguiling, heady cocktail, I caught up with Basso to learn how he's using an engine made entirely from scratch to breathe life into his freakish, enthralling, and slightly terrifying adventure.

Game Developer: How did you develop and hone your animation techniques to make the denizens of Animal Well so brilliantly unsettling?

Billy Basso: The animation techniques in Animal Well were sort of developed alongside the game's engine. I have every sprite in the game on one giant sprite sheet, and very early on, I was manually defining them all by entering the UV coordinates straight into C++ code. So animations at that point were very basic, and sprite strips were just drawn directly on the sheet in photoshop. Since then I've added the ability to ingest data from Aseprite, which is the program I currently use to do traditional 2D animation. I've also added a lot of functionality for particle effects and procedurally drawing geometry. Usually when I'm animating a character I use a mix of all those things. Also, early on, I structured the engine so all the gameplay code is in it's own DLL, and it can be recompiled at any time, while the game is running. So a lot of animation gets created in a tight iteration loop of "creative coding."

As far as making them unsettling, I think the procedural aspects play a big part in that. I think having code drive animations often makes things look uncanny. For instance with the Ghost Cat in the trailer, all the limbs are animated independently through code, along with multiple segments for the body. They are all following their own slightly different paths as the creature follows the player, causing the body to stretch and bend in very unnatural ways. I try to have as many things be dynamic like that. I'm also a programmer by trade, so doing things this way feels most natural for me. There are also a bunch of popular Animation Tips that I've been actively avoiding using. Things like squash and stretch, and screen shake. I see almost every indie game using these to make things look exciting and fun. I've been trying to challenge myself to make animations expressive in different ways.

![AW1.gif AW1.gif](../../assets/0fe2dd26319fc8dc.gif)

You built Animal Well's engine from scratch to explore new pixel art styles and rendering techniques. What were some of the challenges of creating your own engine, and how did you look to push it into uncharted territory?

Over the years I've found programming to be most enjoyable when I'm building my own systems and learning how things work at a more fundamental level. The times where I wasn't happy were when I was debugging an issue related to a third party library, or working around a bug in an engine I couldn't fix. While I was working at various studios where we used Unreal and Unity I would have toy game engines I would work on in my spare time. Animal Well started with one of these. I wanted to see what the bare essentials were for making a 2D platformer, and all aspects of the engine were not developed until I absolutely needed them. This has kept the process consistently enjoyable for me, which I think is crucial on very long form projects.

The biggest challenge of working this way, however, would probably be that I more often have to context switch from developing technology and trying to use it creatively. There have been a lot of times where I'm just trying to make a new character for the game, and I wish my engine could do a particular thing. This will then lead to a week-long detour where I am just developing a new system instead of content. However, over time, the frequency and duration of these interruptions has decreased, as I've accumulated more tools.

As far as pushing into uncharted territory, I've been trying to use techniques that wouldn't work well for pixel art in other engines. I have a fluid sim that is constantly running on a layer for water and smoke effects. I can draw sprites into it the same way I draw anything else. I'm using normal maps for the background art along with a ton of dynamic lighting stuff. Early on, the game truly did look like an NES game, but I've been layering on more and more rendering systems over time. I am always trying to raise the overall quality of the visuals, so I expect the game will look different still, once it's finally done.

![](../../assets/5b4615f7a613daef.img)


More broadly speaking, what are some of the benefits and pitfalls of working with pixel art? What appeals to you about the aesthetic?

I view pixel art as a style that is sort of native to the medium of video games. Most screens are fundamentally made up of a grid of pixels, and you have to do a lot of extra work to hide that fact. Pixel art embraces it instead. A lot of people think the main point of modern pixel art is to create nostalgia for older games, and Animal Well certainly has some of that. But I think there are also a lot of other good timeless qualities about it. In the same way people appreciate tile mosaics, it is satisfying seeing a form be abstracted, and more open to interpretation. I think limitations encourage creativity.

From a technical standpoint, if you are targeting a 3840x2160 (4K) screen, but you only want to render low res pixel art graphics (in Animal Well's case 320x180) you can use 144x more computing power to render each pixel. This opens the door for a huge range of exotic graphics techniques not used anywhere in games. So instead of just strictly adhering to the limitations of old hardware, I'm trying to explore new styles that use all this horsepower, but still feel cohesive and look like pixel art.

As far as drawing the pixel art itself, I think it is very fun. Each pixel matters so much, and placing them all correctly feels like a puzzle sometimes. Moving a character's eye up or down one pixel can completely change their personality.

![AW2.gif AW2.gif](../../assets/136a5eabfd12d52e.gif)

I caught the latest trailer and was absolutely transfixed (and admittedly a little freaked out) by the Ghost Cat that seems to be hounding the player character. Could you break down your process for creating some of the larger creatures in Animal Well?

Each of the larger creatures in the game usually simmer in my mind for a few months before I actually start implementing them. For the chameleon, I thought it would be cool to have an enemy that uses camouflage to disguise itself as a statue. The first few times you encounter it, it is harmless and appears inanimate. However eventually while walking past it, it will reveal its true form, and it will start trying to eat you. It's personality is just kinda animalistic. There's no malicious intent. It just views you purely as a food source. Other animals will have other motives, and you'll have to figure that out as you play.

![](../../assets/62be3862ae280fb9.img)


When I'm actually ready to implement it, I start taking notes about how it will behave and write down what animation states it might have. I'll ask myself questions like what will the room look like where you encounter it? What does the player need to do to get past it? After that, I will do a rough pass of their art and animations in Aseprite. Once I sort of like how it looks, I will create a new Entity type in my engine and code up a state machine to drive the animations I drew. At this point I will start playing with it a lot, and adding particle effects and other little details, like having the eyes track the player's position. I will go through a bunch of iterations like this. Once I am happy with how it looks and plays, I will record some sound effects, and hook those up.

![Animal_Well3.png Animal_Well3.png](../../assets/eee65b87ddb473d1.img)


I've got to level with you. I find the way Ghost Cat drifts across the screen like some gangly, slinking spectre incredibly disturbing. It's brilliant. Can you explain how you designed and animated that character specifically?

I was actually trying to draw a Ghost Dog, but almost everyone has interpreted it as a cat -- including Shuhei Yoshida, who I would never dare correct! I kinda like that though, making something that is more of an open-text. It is fun seeing people have different interpretations.

As for the Ghost Cat-Dog design, up until that point, the game establishes that all enemies reset when you leave a screen and come back. As a player, you always feel safe knowing you only need to reach the end of the screen to escape something. I wanted to make an enemy that surprised the player and broke that rule. I think one of the scariest designs in horror games is the invincible nemesis character that stalks you across the map. I'm thinking of Mr X from RE2, the Alien from Alien: Isolation, or even Phanto from Super Mario Brothers 2. In Animal Well's case, seeing something come from off screen, feels very invasive and wrong.

As for the design, I wanted to make something that moved somewhat slowly, wasn't too hard to avoid, but would just wear you down and prevent you from relaxing. Also I don't feel too bad about inflicting this on the player, since there are ways to avoid summoning it, and it's supposed to feel like you're being haunted! I drew it with a smile to give it what I felt, looked like a little bit of a sadistic personality. But also, it is a dog, so maybe it is just trying to play.

![AW3.gif AW3.gif](../../assets/07637e3bb90f6392.gif)

I also want to touch on the surreal world ofAnimal Well.What philosophies informed your approach to world design, and how are you attempting to ensure each environment will resonate with players?

One of the main goals I have when designing Animal Well's world is creating a feeling of mystery and discovery. I like to try to guide the player into thinking they fully understand something, and then reveal that they don't. Trying to make the familiar suddenly seem unfamiliar. A Lot of things on screen are obscured by darkness, so any black tile could be hiding something. It's also important to me that the entire map be tightly packed and contiguous, with no long elevators or teleporting. If there's a gap in the map, there's a good chance something is hidden there. I'm trying to make the world as dense and detailed as I can, so finding something new is always meaningful. For puzzles that are more challenging, I always leave the player with other things to do, so they don't feel like progress is completely blocked.

I am conscious of how many things I am dangling in front of the player at any given time. It can be fun to tease a player with a door that is locked from the other side. But, it can be overwhelming to walk into a room, and see six doors connecting to different areas. In cases where I need to do this, I will make some of them completely hidden. Like maybe you have to blow up a wall to create a shortcut back. I will also disguise future interactable objects as set dressing, until you have the tools/knowledge to interact with them. There's the knowns, the known unknowns, and the unknown unknowns (to quote famous game designer, Donald Rumsfeld).

Sometimes I also experiment with making the rules and mechanics of the game a puzzle you need to figure out in their own right. A lot of times, the possibility space of things the player can try isn't actually that big. Instead of immediately telling them what they are supposed to do, I let them just discover it through experimentation. Most of the time, this doesn't take them any longer than an explicit tutorial would, and it makes them feel way smarter and more present in the world.