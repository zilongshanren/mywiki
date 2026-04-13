---
title: Simonschreibt.
url: https://simonschreibt.de/gat/sims-4-mirrors/
author: Simon
published: '2025-03-28'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

[Overview](https://simonschreibt.de#overview) | [Technical Details](https://simonschreibt.de#details) | [Bonus](https://simonschreibt.de#bonus)

# Overview

This article does not contain a revolutionary discovery, but some observations about mirrors that may not be entirely obvious to people who never implemented them into a game.

Sims 4 offers mirrors which actually work! For that, the game needs to render the room **another time** for **each** mirror in the scene. Of course, this is expensive.

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

Nice optimization: From far away, the mirror is actually **not** reflecting anything! It shows a static texture until we zoom in closer. Then the static texture fades out and makes space for the actual reflection.

Before you ask: No, [infinity mirrors](https://en.wikipedia.org/wiki/Infinity_mirror) are not possible:

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

Anyway, what I actually wanted to show is the next video, where we can observe efficient culling within the “mirror verse”.

To prepare you for this video: When I attach my profiling tool, for some reason the rendering **glitches**! The floor is missing, and the mirrored room is rendered **on top**. This allows us to see the **whole** **mirrored **room (not only the tiny part we can observe through the mirror surface)!

I love how efficient the culling works. All characters and objects get culled quickly. Even the display of the laptop! I know, it’s nothing special, but I love looking at stuff like this! 💘

# Technical Details

Here are some more technical details about the rendering process of mirrors:

As mentioned, the game renders the room **again**, for each mirror. Below is what I could find out with my profiling tool. After rendering a depth buffer (and also a shadow map), the scene is rendered as usual and afterward come the mirrors one by one.

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

The first chunk (923) is **another** mirror which is close by but out of the view.

To sort out, which mirror should display which room, the game seems to use **stencil buffers** (which are basically black/white masks). In my capture with three mirrors, I discovered three stencil buffers:

The stencil ref starts at **2** because there was **another** mirror close by when I was capturing the three visible in the scene.

I can’t prove, how exactly it works in Sims 4, but I assume it’s very similar to what is shown in [this Unity tutorial](https://youtu.be/y-SEiDTbszk&t=973):

- Render each
**mirror surface**into its own stencil buffer (or into the same but with different IDs?). - Collect all visible geometries for each mirror individually in order to render them, but only where the stencil mask of the respective mirror allows it.

# Bonus

## Bonus Observation #1

In Sims 4, you can hide the **interior** walls to better see what’s going on in your house. But the mirrors still render them and ignore this “no wall” view mode:

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

## Bonus Observation #2

If we look at a Sim taking a shower, we can see that the pixelation effect and the water particles from the shower itself are also reflected in the mirror:

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

If we look at the same scene with my “glitch” being active, we can observe something interesting: The sim is only pixelated **within the mirror area**, as are the particles (water/steam from the shower). I assume that they are also limited to the above-mentioned stencil mask.

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

## Bonus Observation #3

I could **not** reproduce this funny glitch (the video is 10 years old). I assume it was an optimization in the animation system, and maybe it’s fixed by now. But I still wanted to show this video just because it’s funny:

[Sims 4 Mirror Glitch](https://youtu.be/6rEmnRiST4I?si=0TrrcfhdYIHlSkkt)

## Bonus Example

[Marina](https://bsky.app/profile/parinamais.bsky.social) just implemented a mirror in her game and shared some nice insights on my [Discord](https://discord.simonschreibt.de/).

“For the player, it’s a camera + a render target, that target is a simple quad with a script that follows the player on the horizontal axis, and there’s also a stencil mask on the mirror, so the quad only appears when it’s in front of it.”


Like in Sims, we can see a wall in the mirror which is actually not there from our perspective (otherwise it would block the camera). How was it done?

“The environment is a simple texture on the mirror object itself!”


I hope you liked this little adventure into the world of mirrors!

Simon 🌞