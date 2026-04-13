---
title: Voxelart Styles in Video Games
url: https://www.gamedeveloper.com/art/voxelart-styles-in-video-games
author: Zach Soares
published: '2019-02-15'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Voxelart Styles in Video Games

A blog post explaining some of the foundational voxelart styles in videogames. This applies to general voxelart as well but it serves to build a better understanding for the form in video games.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

### Voxelart styles in video games

(This article is a rewrite from the original I wrote back in 2015. It has been updated to reflect the times and changes that have occured in the industry since.)


Hi, I’m Zach and I’ve been making voxel art professionally in the games industry for 6 years. I’m writing this piece to talk to you all about the implication of voxel art in video games and where I see that going. Voxels are a rendering method that have existed for a long time, in fact, it was in early competition with polygons as the rendering method for 3d game visualization and well…. we saw how that turned out, polygons won! While polygons have been the way games have grown and evolved artistically, voxel art has slowly started to make a comeback in the medium. A great example of early era voxel art is Shadow Warrior (1997) and Command and Conquer: Tiberian Sun (1999), So this is not to say that it has only recently been used —the last 5–10 years— but only that it wasn’t feasible in the early days due to performance requirements.

Command and Conquer: Tiberian Sun (1999)

In the last 10 years voxel art has started to make a return in the games industry with games like Minecraft (Early alpha release in May of 2009) and 3D-Dot Heroes (November 2009 release). This return has spawned a new wave of developers to create games around the voxel art aesthetic. The reasoning behind this is the growth of hardware limitations along with improved rendering techniques. Thanks to this growth in tech, developers are now able to make games that make full use of voxels. However, you can attribute the artistic growth of the medium to the developers making Voxel Editors. A way to edit voxels outside of the game engine and later passing that over to the game space is extremely important. This impact is the same impact that 2D editing software had on games prior to what they were today (transition of early era pixelart to photorealistic texturing).

Thanks to softwares like Qubicle, MagicaVoxel, Voxelshop and many others, artists have been able to express themselves artistically games using voxels. These tools have the ability to not only export models and pieces as raw voxel objects, they are able to export these models as usable Polygon objects. Now yes, I know earlier I spoke about how voxels and polygons are two different things. I might be contradicting myself at the moment on what is a voxel model but what we’re talking about is voxel art. The art in which voxels are the root or influence. We’ll later touch on some edge case art styles to better identify what i mean.

Voxel art is fascinating as an art form. It can be seen as pixel art in the third dimension or something more akin to low-poly art. It’s best to separate voxels from all others forms of 3d art. This is the only way to really figure out what voxel art is and can be; the same way polygons are separated from 2D illustrations. Pixel art does lend itself to voxels, it does indeed help with the development of the form but it can also restrict the style. Voxels are 3D and thus need to be thought of that way when working with it, otherwise your work will come off as 2-dimensional even if it was being projected in a 3D space.

There are many types of voxel art but I’ll simply list and explain a few below which can be considered “base” styles.

Vector voxel art: See this as the style that uses only 90 degree bends when representing curves. It is a very clean style that is easy to read at varying scales. Crossy Roads uses this style most prominently. This style is most optimal for game devices which have low system requirements. This is why Crossy road looks the way it does. Not only for its artistic expression in its simplicity and abstraction of real life objects/characters, but also due to the hardware limitations posed by smartphones. It is and was always a perfect match.


Crossy Road by Hipster Whale

Pixelated voxels (flat shaded): This style is currently less common but has been done. Utilizing pixel art in its entirety, the artistic pieces done using this style tries its best to represent pixel art in a 3D space. This style has to be flat shaded to be forgiving for its bends. Flat Shaded voxelart also benefits from being able to show all the colors being used due to minimal presence of shadows, therefore the style benefits from vibrant colors. With any form of hard shadows applied the piece and style will be ruined. This is often achieved using raytracing techniques which are often expensive for computers to…compute but is rather lightweight for voxel-tech. This can be seen as the most “pure” form of voxel rendering.


Fugl by Melodive

Voxelnauts by Retro Ronin

Blocky voxels: Boxy voxels are what I would categorise for games in the vein of minecraft. The style is very blocky and looks like the world is made up of cubes, even the characters. It’s a very forgiving style in that it is easy to work with on a technical and artistic level. (this isn’t to say it is easy to execute. It still requires talent and skill to make good looking boxy art). Often this style uses textures on polygonal cubes instead of being made edited in direct voxel editors. This is where a major conflict can arise in what is now defined as “voxel” art. The reason I would still include this category is because it is still recreatable in voxel editors, but more importantly it is a style derived by and inspired by voxel art and so it is worth mentioning. A pure voxel created art piece in the Boxy style might not look as complex as something from Hytale but it is important to note that it -can- be voxel art.


If you follow [THIS](https://medium.com/@Voxels/blocky-voxelart-a-brief-11d3ef9f9724) link I’ll go further into explaining this topic as it encompasses a whole other set of ideas which detract from this article’s main goal.

Minecraft by Mojang

Hytale by Hypixel

Greeble Voxels: This voxel style ignores the rules of bends from vector art and embraces its curves. While it is the most difficult to manage in terms of technical rendering, it can yield interesting results. The use of SSAO here is meant to emphasize the jagged-ness of voxels when built at a higher resolution. Using simpler colors and ignoring manual shading (something often done in pixel art). Applying shading on the model should only be done in-engine as adding your own coloring won’t yield visible results. The style lends itself best to realistic renditions of world objects. Additionally, this style is often brought further in it’s rendering by using PBR (Physical Based Rendering) to create more realistic material effects on the voxel objects in question. You’ll often get a more gritty atmosphere from this style but it’s not to say that you can’t make more cartoony pieces using it.


The greeble style is coincidentally the style that was used in the classic voxel games like Command and Conquer: Tiberian Sun. The game made unit models out of voxels so that they could be destructive and show damage over time. Where previously it was used for gameplay reasons, it can now be used purely for aesthetic which is a nice reward for artists patiently waiting. Be wary however, the work involved in making this style feasible is quite high due to engines not being designed for voxel models which yield unusually high polycounts.

![](../../assets/0cfeb2f24b8a5685.png)

Critical Annihilation by Devoga

Voxel Foliage and Lighting test

These are the four varying forms of voxel art I can distinguish as the variable extremes. They each serve their own purposes and can impact the style, and feel of a game tremendously. What’s very important to note is that to be voxels or voxel art it needs to be perfect at the pixel level. A cube is a cube in the same way a pixel is a pixel. They do not bleed into one another, they do not clip into each other, they are stuck in a grid throughout the creation process. That is the primary constraint for voxel art that needs to be distinguished, although it can be circumvented if you were to make objects individual from one another and later put them together in a 3D modeling software, or engine. To be clear, these are not all the styles that exist for voxel art. I’ve personally made a handful of different looking styles touching on the above and more, but above is what I would consider the 4 circles of voxel styles.

Moments ago I mentioned how the voxel art constraints may be circumvented using external editing tools and game engines. We’ll be elaborating on the techniques which can be used to circumvent these constraints, but nonetheless the base models created are all from voxel editors and therefore should still be considered voxelart.

All the techniques which circumvent previously mentioned constraints revolve around animation.

### Voxelart and Animation

The world of animation in voxelart is a bit in contention for various reasons. One is that there’s a lack of tools that allow for all types of voxelart animation to be possible. Nonetheless, the existing animation styles people are pursuing touches on 3 techniques;

Rigid body animation, Soft-Body animation and frame based animation.

Rigid body animation has to do with creating standard 3d skeletal rigs in any animation tool like blender or maya and then snapping chunks of a voxel model to a given bone. This way a model piece (say, a hand or lower arm) moves along with the bone it’s attached to 1:1 with no warping of the exported mesh.


This technique of voxelart animation presents itself with a lot of visual complexity which can dictate a specific voxelart style output due to things like Z fighting of model textures and mesh clipping.

![](../../assets/05e6bc6795c9f40e.gif)

Elbow joint for a demon king in Last Stand

This is all well and good, it’s the expectation when delving into animation. Your animation style will guide the voxelart style you lead yourself with. I go into further depth about how I developed the aesthetic in the animation below [HERE](https://medium.com/@Voxels/voxel-art-reducing-the-greebles-263cef16b12d).

Model from Last Stand by Zach Soares

It’s important to know that with each style you’ll encounter a new issue, so while the animation technique is the same, the resulting look and feel will be different.

Soft-Body animation is a step further than rigid body animation style. It entails a little more overhead as you need to apply proper weights along the topology of a mesh so the resulting animation is clean. The outcome of an animation here tends feel less “retro” and more modern with game development trends. This given rigging method makes it exponentially harder to deal with if you’re working with certain voxel styles, not because of the animation itself, but due to retopology overhead. It’s not to say this rigging process wouldn’t work with other voxel styles, it’s simply alluding to more complexity in the pipeline before producing a usable end result.


An example of having to retopologise a model to run more efficiently for a game, we’ll take the running knight below.

![](../../assets/9e417c96b59163db.png)

This is what an optimized voxel model looks like when being rigged in Maya. We’ve had to export the model as a traditional 3D format so we can go about editing this otherwise we’d be locking ourselves to the rigid body technique. As you can see we’ve done various edge-loops along the body, arms and legs so we get the right amount of flex throughout the animation. Alternatively, if we were to leave the model unoptimize and in its “raw” voxel output, we’d get the below.

![](../../assets/0e96cd0bbe8e6d3e.png)

This Output will yield the same results, if not smoother bends, but at the expense of your games performance. Unless we can get ourselves a voxelengine which allows the bending of voxel assets (like in the [Atom Engine](https://youtu.be/jItvtnc5hLw?t=105)) we wouldn’t have to concern ourselves with this issue, but it’s best to avoid it in the long run as it’s largely inaccessible. This is the reason for retopologizing and why the Soft-Body rigging technique requires a longer pipeline to get results. For any traditional animator in the games industry, this won’t seem unusual, but for beginners it can be quite daunting.

Bendy Knight by Zach Soares

Frame-Based animation is the most problematic, not because of any artistic complexities or limitations but specifically because there are no existing tools that allow for the form to function effectively. Now, bear with me, there are methods to make this form of animation work using “tools” like plug-ins and extentions within game engines, but as it stands there are no standalone applications comparable to tools like Aseprite or GraphicsGale for voxelart. This roadblock makes frame based voxelart animation very frustrating. It requires an exponential amount of time to execute on a level equal to a pixelart animation and the technical requirements to make it work are still quite heavy. With frame-based animations you’re required to swap every single voxel mesh on a per frame basis in the same way you’d cycle through various frames of a pixelart spritesheet. For every frame, the engine will need to recall a new mesh and then destroy the old one which is not a very enjoyable task.


An old version of MagicaVoxel briefly allowed people to make frame based animations like the one below and it really shows how charming voxelart can be when left to its roots. It feels retro yet new, familiar but fresh. This is what many are striving for and hopefully soon we can encounter some games that use it in its full capacity.

![](../../assets/d803fef0cddc92c6.gif)

Magic Mallet by @Armyoftrolls

I hope you enjoyed this refreshed article on Voxelart Styles in games. Of course this is not ALL the voxelart styles. As previously mentioned, there are many more to be found and many unmentioned, but I consider all of the above as the foundation for what is voxelart and what can help to define a style in the form. As new tools come to light and new games are made, we’ll be able to experience new styles and that something I will always be looking forward to.