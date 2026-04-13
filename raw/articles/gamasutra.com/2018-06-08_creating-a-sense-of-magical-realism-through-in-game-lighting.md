---
title: Creating a sense of magical realism through in-game lighting
url: https://www.gamedeveloper.com/art/creating-a-sense-of-magical-realism-through-in-game-lighting
author: Jack Yarwood
published: '2018-06-08'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Lighting is an often underused and underappreciated tool in the game developer’s tool kit.

In addition to its (very good) function of making your game visible and readable by the player, lighting can be manipulated to evoke a specific atmosphere or draw particular attention to a level’s design.

For this reason [Midnight Hub](https://www.midnighthub.com), the Malmo-based indie studio behind [Lake Ridden](https://store.steampowered.com/app/696530/Lake_Ridden/), aimed to take full advantage of lighting while working on the puzzle-exploration game.

Rather than simply using lighting to illuminate a scene, the team wanted to evoke a sense of magical realism, purposefully lighting each scene to accentuate the length and shape of shadows as well as draw the player deeper into the story and its mysterious forest setting.

The premise of Lake Ridden is simple: you play as a girl named Marie who is looking for her younger sister. She’s gone missing while on a camping trip in the woods, and it's up to you to explore your surroundings for clues on how to find her.

Playing from a first-person perspective, you're tasked with solving puzzles found throughout the different areas to advance and illuminate light sources, which in turn keep track of where you’ve already been. But, as you explore deeper into the woods, you’ll soon realize that there is more to the environment than first appeared. Something supernatural is afoot.


## "You never want to just place a light somewhere [randomly], you want to [say] 'What can we do to make this area interesting with this light?'"


## Settling on an art direction

One of the biggest problems during the development of Lake Ridden was the amount of time and resources the team had to make the game. While coming up with the art direction, the team were conscious of how time-intensive a realistic aesthetic would be and therefore decided against it, choosing to go with a more stylized look inspired by games like Among the Sleep and Firewatch.

“We realized that if we were going to finish this game we should just do somewhat semi-realistic textures, and maybe paint them a little bit, and then do the stylized feeling with the atmosphere, and the fog, and the lighting, and so on,” explains [Erik Nilsson](https://ean.artstation.com), the art director on the game.

![](../../assets/b114fad31f9634db.img)


The look they strived for with the lighting and environmental effects was something they termed “Hollywood realism”, where the contrast between light and shadow is purposefully dramatic or exaggerated to evoke a particular atmosphere. You can see this in the quite pronounced volumetric light shafts in the daytime scenes and in the interior shadows.

## Using reference material for guidance

The team looked at tons of reference material to achieve this tone, including real world photography and stills from Hollywood movies such as the cinematography of Andrew Lesnie (The Lord of the Rings) and John Alcott (The Shining).

![](../../assets/d108daabb455c38e.img)


This helped them decide how to render particular objects in the game’s world and how many highlights an item should have. They then used their own plug-ins to tweak the saturation and balance colors in the environment when tinting the light, giving the day scenes a warmer overall look and a blue tone to the game’s nights.

“I think [more designers] should look a lot at movies,” says Nilsson. “Look how they are lighting things, because nothing is an accident. Everything is planned. If you have a light, try to get the most out of it, because a shadow is great for breaking up a texture and making it look more interesting.” He adds, “You never want to just place a light somewhere [randomly], you want to [say] 'What can we do to make this area interesting with this light?'”

## Tackling the natural lighting

You see this approach on display early on in the game, when you come across a campsite bathed in moonlight. This clearly communicates to the player that this is the next area of importance, contrasting significantly against the dark forest environment.

![](../../assets/5e9b94db8773d4e8.img)


“We wanted to create these light islands, where if you walk through the path, you can almost always tell where you’re going from this light island space up ahead,” Nilsson explains. “It’s like, “Okay, here’s the next breadcrumb.” It should be light enough that you can explore a bit if you want to, but usually it is [only] the important parts that are lit up.”

This technique is used throughout, such as later when you happen across a stone ruin in the garden swarming with fireflies. Not only is it a functional way of leading the player through a level, it also carries a thematic importance in the plot.

At times the light takes on the form of ghost lights, similar to will-o’-the-wisps from European folklore that were said to lead travelers astray. The game has you follow these moving blue lights throughout a forest to locate certain puzzles in a move that gradually introduces the player to the presence of the more magical elements.

## Using light sources as markers

It isn’t just natural lighting that is important for the level design however. While exploring the manor and the garden locations, you will also often come across static light sources, including lanterns and candles. These are usually placed close to puzzles, key items, and along paths, and can be lit to keep track of where you’ve already been or to simply illuminate the environment and get a better sense of your surroundings.


## "We started out with a flashlight, but it was a lot more fun just to light things [ourselves]...going around with a flashlight everywhere, you’re not only going to destroy the level design, but also the atmosphere."


The decision to add light sources had the benefit of allowing the developer to keep control of the lighting and the mood of each setting, while still giving the player some level of interaction within the scene.

But this wasn’t always the plan.

“We started out with a flashlight, but it was a lot more fun just to light things [ourselves],” explains Nilsson. “If you have a stationary light, you can decide where the light sources are going to be and how things are seen. Whereas going around with a flashlight everywhere, you’re not only going to destroy the level design, but also the atmosphere.”

Exploring the environments for the first time in Lake Ridden, these static lights are important for slowly dispelling the mystery of the game’s world, with the player able to gradually reveal a scene through careful exploration and interaction with the objects around them. It heightens the atmosphere and sells you on the idea that you are the first person to visit the setting in a long time.

## Dynamic over baked lighting

It should be mentioned, though, that the Midnight Hub’s approach to lighting wasn’t without its technical problems. The game was supposed to be lit using baked lighting, which is often a low-cost approach as light and shadows are pre-computed using lightmaps. However, Unity’s lighting system seemed unsuited to the large open environment of the game, meaning they couldn’t get the shadow baking to work properly. It would either be of a low quality or crash the game.

![](../../assets/7bba72d19da535de.img)


The compromise was using dynamic lighting instead. Although, allowing players to light up individual light sources around the world proved taxing on the game’s performance. Johan Bernhardsson, the project director, therefore had to rewrite his own personalized lighting system, to ensure that light and shadows would turn off at a certain distance. This helped maintain performance and ensured that the gameplay didn’t slow down to a crawl if the player lit all the available light sources in a level.

“The main reason [we did this] was because the original lights that are in Unity are pretty good if you want to bake everything, but since we had an open-world area we had some real big problems getting the baking to work,” explains Nilsson. “It just didn’t like the scale of the game. We tried to do real-time outside and baking inside and that didn’t work either.”

![](../../assets/550c2c572b7a154c.img)


Lake Ridden demonstrates just how effective a tool lighting can be. It is not only used to sell the player on the supernatural nature of the game, but to carefully lead the player through the world. I ask Nilsson how challenging it was to get the lighting right for the game.

“We have internal jokes about how much of a pain in the ass the fog and the light has been,” says Nilsson. “I think we have like learned of what not to do for the next project, but yeah, it has been a big thing to get right because it does so much for the atmosphere to get those two things right.” He highlights having to use their own dynamic lighting as one of the biggest lessons they learned. “It’s definitely been a real uphill struggle.”