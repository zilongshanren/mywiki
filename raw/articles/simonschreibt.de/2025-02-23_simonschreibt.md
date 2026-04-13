---
title: Simonschreibt.
url: https://simonschreibt.de/gat/infinity-nikki-one-way-window/
author: Simon
published: '2025-02-23'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1). [Update 2](https://simonschreibt.de#update2).

I just noticed, that this window can **not** be seen through another window on the other side of the building:

[Infinity Nikki](https://store.epicgames.com/de/p/infinity-nikki-71fc64)

My guess: It’s an optimization to save some polygons.

The back of the wall is most likely **one** huge quad (instead of at least four), but thanks to back-face culling, this quad does not block the view when we look inside the room.

[Infinity Nikki](https://store.epicgames.com/de/p/infinity-nikki-71fc64)

But why can we still see the sun shining into the room? I assume they use only the **front**-faces for the shadow map calculation and with that, the sun ignores the big back-face quad.

By the way, a little info-nugget about a game I worked on (Sacred 2):

For this game, **back**-faces were used for the shadow map calculation (also called “[front-face culling](https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping)“). One artifact of this is, that it’s possible to see small light leaks like this:

A reason for using **back**-faces for the shadow map: it fixes the so-called “peter panning” (read more about it [here](https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping)).

But a new problem arises by using this technique: a common optimization (for top-down games like Sacred 2) of removing the polygons on the **underside** (aka back-faces) of objects doesn’t work anymore since, for example, a tabletop would not cast any shadow.

So we had to make sure that all our tables, bridges, etc. had nice polygons on the underside, even if the player will never see them:

[Sacred 2](https://de.wikipedia.org/wiki/Sacred_2)

Have a nice day! 🌞

Simon

![](https://data.simonschreibt.de/assets/icon_update_01.png)

Just noticed another small optimization in the game. Objects, which are out of view, stop being animated. Wouldn’t be noticeable, except if the shadow (or the sun! Again!) wouldn’t reveal the secret:

[Infinity Nikki](https://store.epicgames.com/de/p/infinity-nikki-71fc64)

Another tidbit: Some NPCs, which are too far off the screen, get their animations disabled as well. **But** this doesn’t seem to be related to the camera frustum, but probably a simple dot product between the camera view vector and the NPC position relative to the camera. I assume that, because when you play in 32:9 you can see some NPCs stop their animation **while they are still on-screen**.

[Infinity Nikki](https://store.epicgames.com/de/p/infinity-nikki-71fc64)

I guess the developer didn’t test this optimization in super wide screen.

![](../../assets/ba0680151067ebbc.png)

For the window backface, I’m wondering if it might be slightly more complicated than a polygon optimization. I mean, if you wanted to reduce the poly count, you would just not render the interiors, right?

My theory: but some games use occlusion culling to hide objects hidden behind larger objects. There are various ways to implement occlusion culling, one of them is to have occlusion volumes manually placed by artists. The issue is that if you can see through the building, then you can’t place an occlusion volume, since it might cull everything rendered through both windows.

The best solution is to have windows only one way, so that occlusion culling still works for objects behind the building, and you can still see inside with windows on every wall. The best of both worlds.

I also think it’s more than a polygon optimisation. It saves on overdraw, and avoids the sorting issues that come with rendering multiple layers of transparency, so there’s multiple benefits to it, with only a slight (and hard to notice) change to ‘accuracy’!