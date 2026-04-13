---
title: What means “Game Ready Substance”?
url: https://www.gamedeveloper.com/art/what-means-game-ready-substance-
author: Giuseppe De Francesco
published: '2013-06-08'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# What means “Game Ready Substance”?

Allegorithmic substance support in game engines is becoming quite common as we see them supported in the two main engines: Unity and UE4. But are the substances game-ready?

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](http://www.dftgames.com/wp-content/uploads/2013/06/substancescreen-131964_250x250.png?width=1280&auto=webp&quality=80&disable=upscale)


We see a lot of Allegorithmic substances on Unity Asset Store, starting with the famous Bitmap To Material (B2M), but are them Game Ready? Not quite! There are a few questions to ask here, and the main one is: how much time takes a substance to generate the maps? This is the very main question because you have to decide if you can use the substance dynamically or not. A substance that takes half a second (or even more) to generate the maps is unlikely to be used dynamically because of the lag between the change made by code (i.e. to show blood on a wall) and the moment in time the player actually sees it. And what about the time that would pass between the level loaded and the level properly displayed? If you have tens of substances applied to your environment and they are set to be dynamic (generated at runtime) the result will be like this: the user loads the level and looks at a blue & white panorama that in a few seconds gets properly textured: a horrible experience!

So basically, Allegorithmic substances are great, but they are not always “Game Ready”. Most of the time you cannot use a substance dynamically because it’s too slow. This is why for our games we design each dynamic substance to be really minimalistic, carrying only the very essential parameters so that they can be actually modified at runtime without having to tell the user that the game needs at least an Intel i7 to run correctly.

We are in the process of publishing a lot of Game Ready substances, designed for being dynamic. We do have also some other that you want to use checking the box to generate the map at the build time instead. We are also defining a colour coding for the substance presentation art to allow our customers to know by the first look which substance is designed to be dynamic and which are not.