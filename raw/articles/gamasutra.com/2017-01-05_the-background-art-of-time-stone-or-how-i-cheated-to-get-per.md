---
title: The Background Art of Time Stone OR How I cheated to get perspective right
url: https://www.gamedeveloper.com/art/the-background-art-of-time-stone-or-how-i-cheated-to-get-perspective-right
author: Stuart Lilford
published: '2017-01-05'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# The Background Art of Time Stone OR How I cheated to get perspective right

Producing backgrounds for adventure games can be tough work especially to novice artists like myself. With my indie point-and-click adventure game Time Stone, I tried a new approach which allowed me to "cheat" in order to get my perspective right.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

I wrote this just after the release of my adventure game Time Stone, which you can download on [gamejolt](http://gamejolt.com/games/time-stone/18955) or [itch.io](https://scared-square-games.itch.io/time-stone)

I don't feel like I'm very good at art. I mean, I get by okay, people tell me they dig the artwork in my games, but when I look at the art I can just tell it isn’t that good. People say that as a designer, you’re your own worst critic and maybe that’s true, but I don’t really think about things like colour pallets, perspective, shading etc and I feel that my artwork suffers for it. I have a basic understanding of it all, but don't spend the time to put it into practice. I saw this as a weakness when I was developing my point-and-click adventure games [Entrapment](http://gamejolt.com/games/entrapment/24537) and [Time Stone](http://gamejolt.com/games/time-stone/18955).

One of these things that I’ve managed to find a way around for, a cheat if you will, is with perspective. Yeah, sure you can sketch something out on paper or in Photoshop or whatever and have vanishing points for perspective and then create your background based on that perspective adding in objects to the room and such, but what if you do all that and it still doesn’t look right to you? This happened with me quite frequently when creating backgrounds for Entrapment (which was one of the things I mentioned in my Entrapment Post-mortem). I would create a rough draft of the room using vanishing points and perspective and place a character sprite in it and it just wouldn’t look right. Especially if you moved the character around the room and the scale would look all wrong. Then I would have to start from scratch with new vanishing points/horizon lines which was really frustrating.

![](../../assets/dadfd1930532376d.png)


For Time Stone, I tried something different. I thought, instead of messing around with all that perspective stuff, why don’t I just create my scene in 3D? That way I can move the camera around to get the right angle and my perspective will always be right. I can also move objects around when I please to change the composition without compromising the perspective like it would in Photoshop. So I did just that. [Google SketchUp](http://www.sketchup.com/) is free and simple to learn if you’ve never used 3D modelling tools before. You can use it to create really simple 3D scenes using an effective toolset, but the best thing about it by far is components. Components are basically, a collection of 3D models that people have already made and shared so that anyone else can download and use them in their 3D scene. Need a bed? There’s a ton that people have made. What about a bookcase? Yup, got that too. But you would think it would be difficult to find more obscure things like a giant birdcage, cauldron or a crystal ball? What? They have those too? Of course, they have just about any object you could think of, from random items of furniture to whole buildings! Even a football stadium (which I actually needed for a previous project)!

![](http://www.scaredsquare.com/Blog/Articles/TheBackgroundArtofTimeStone/001.png?width=640&auto=webp&quality=80&disable=upscale)


Now I’m not saying that you need to find the exact item that you need for your game, you’re just using this to get the right perspective. For example, the bed in the scene above is different to the bed which was drawn for the background in Time Stone. I simply used it as a base when painting the bed in, in order to get the correct perspective for it. You also can’t rely on the lighting from the Google Sketchup image as you may have light sources in different locations. You need to think about this carefully when you are painting over the objects from your 3D scene.

![beds beds](http://www.scaredsquare.com/wp-content/uploads/2014/08/beds.png?width=527&auto=webp&quality=80&disable=upscale)


Once you have created your room and added in all of the key objects for your game then you can set up the camera and export an image of the current camera view. This would work from any perspective. Side on, top down, some weird perspective from an awkward angle if you’re going for a certain style. For Time Stone, I chose a side on view of the Professor’s house. Below is the final camera view used or the background in Time Stone:

![](http://scaredsquare.com/Blog/Articles/TheBackgroundArtofTimeStone/002.png?width=612&auto=webp&quality=80&disable=upscale)


It contains all of the essential items from the room. Any object that would warrant me needing to get the perspective right for it such as the bed, the table, the fridge, the bird cage, etc. But notice that I didn’t bother with the paintings on the walls or the tapestries. These were added in later using the existing objects within the room as a guide for the perspective. The reason for this is that I know enough about perspective in order to draw these items myself. I also included a handy scale model, so that the character art and background art would look correct in terms of scale. The only thing I wish I had done is adding in foreground features. Maybe next time.

After that it was simply a matter of painting over the scene to create the background for Time Stone. This Gif shows roughly the steps taken.

![](http://scaredsquare.com/Blog/Articles/TheBackgroundArtofTimeStone/BackgroundSteps.gif?width=416&auto=webp&quality=80&disable=upscale)


1. The base image, before I started to paint over it.

2. I blocked out most of the colour and detail for major objects

3. Coloured in the rest of the image

4. Added in some smaller objects for detail

5. More detail

6. Lighting and shadow (also made some changes to a few objects).

Some things missing from the background are the objects. This is anything that needs to move/animate in the game. For example the book case, the main door and the blanket over the cage are missing. These won’t have been painted as part of the background as they would have to move and so there obviously needs to be something behind them. These were done on separate layers to appear in front of the background.

Something that is easy to forget is to make sure you remember your interface. That’s what the black space was for at the bottom of all of the images. You need to think ahead and figure out if your interface is going to take up any of the screen. You don’t want to waste your time and effort and creating an awesome part to your background only to cover it up with the UI.

![](http://scaredsquare.com/Games/TimeStone/Images/Screenshots/Screenshot290913.png?width=640&auto=webp&quality=80&disable=upscale)


There you have it! A few insights into how I created the artwork for Time Stone. So if like me, you have trouble getting the perspective right on your adventure game backgrounds (or artwork in general), then try out this method. It was a much more efficient method than the one I used for Entrapment and although it might be “cheating” in terms of not learning how to create a correct perspective, it gets me the results I want and who knows, using this method a few more times may help me learn a thing or two about perspective and scale