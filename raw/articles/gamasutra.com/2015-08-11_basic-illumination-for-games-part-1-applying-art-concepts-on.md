---
title: 'Basic Illumination for Games, Part 1: Applying art concepts on interactive
  media'
url: https://www.gamedeveloper.com/art/basic-illumination-for-games-part-1-applying-art-concepts-on-interactive-media
author: Jorge Veloso
published: '2015-08-11'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Basic Illumination for Games, Part 1: Applying art concepts on interactive media

This articles explores the basic anatomy of visual information, reviews the famous 3-point lighting technique used in film and photography, and provides examples of how it translates to interactive media, mainly in abstract and side-scrolling games.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

With Global Illumination now taking the default seat in game engines from Unreal to Unity, the technological status quo of development raises the bar higher than ever. This is, of course, AWESOME… in some ways. It allows indie artists to achieve a graphical fidelity that can keep up with current AAA games. This also means they have more tools available to create unique aesthetics that would have been technologically impossible otherwise. But, as always, this can also lead to overconfidence when dealing with the fundamentals of what these technologies were designed for.

I’m writing this article to remind the basics of illumination and to examine how they’re applied on games. This article is aimed mainly at newcomers, developers with no artistic background, and to artists without developer background that wish to see how basic concepts translate to interactive media… or just to people who want to refresh these concepts and take a new look at them! :)

### The purpose of Illumination

Light in videogames usually serves a simple purpose: to give players enough visual information for them to play. Unless visibility is being used as a game mechanic (Unfinished Swan, Silent Hill, Five Nights at Freddy’s, etc.), gameplay elements should always be properly illuminated. It is one of those things that should remain unnoticed by the player. And as most things that remain unnoticed, it has to work perfectly!

We could talk for days about every aspect of what makes attractive illumination, but today we’re going to focus on what makes it functional.

### Anatomy of visual information: Shapes and Borders

To be considered functional, illumination must provide 2 important pieces of information to the player:


Borders: the very basic visual element that must be provided in order to interact with any object (in real life or videogames). Border defines the limits of where objects begin and where they end.


When you were little, you may have been scared of shadows in your room at night. These shadows would fuse with the light coming from your window and other things in your room, causing the illusion of monsters, creatures or otherworldly beasts (or clowns, terrible, terrible clowns!). In partial darkness, such as a dim lit room, borders are usually hard to see, while certain shapes remain visible. This makes your imagination define these shapes into something new, but unreal. A mop next to stacked pillows could easily become Cthulhu in your mind!

Shapes: The next element in visual priority is depth. Think about this: if 2 black objects with square borders were to be placed back-to-back, their silhouettes would fuse, making a rectangle and thus distorting the player’s perception of the object. This is the case of hand puppet shadows.


![](https://fbcdn-sphotos-g-a.akamaihd.net/hphotos-ak-xaf1/v/t1.0-9/11825006_10153259045808025_5763538142320564968_n.jpg?oh=04ea1a762ed57d0f48c24b4a4056f4e7&oe=564D8008&__gda__=1446410172_bf91d4a82e70ffded34fda5e58025d69&width=1280&auto=webp&quality=80&disable=upscale)


The element of depth is not something inherent to 3D. It’s also a very basic element in handling 2D games. You can see its effect in many versions of Tetris:

![](https://scontent-mia1-1.xx.fbcdn.net/hphotos-xtf1/v/t1.0-9/11870900_10153259047553025_938395817906090126_n.jpg?oh=f90188df896d48af92b92f4db5e3f486&oe=563F9582&width=1280&auto=webp&quality=80&disable=upscale)


It is actually easier to make out the Russian text than trying to figure out which pieces were placed at the bottom.

![](https://scontent-mia1-1.xx.fbcdn.net/hphotos-xft1/v/t1.0-9/11880573_10153259063643025_2173435640562743137_n.jpg?oh=90507b23902e9c41979e523b6bb030b0&oe=563AFD80&width=1280&auto=webp&quality=80&disable=upscale)


![](https://fbcdn-sphotos-b-a.akamaihd.net/hphotos-ak-xpf1/v/t1.0-9/11880573_10153259063648025_1344387442410980907_n.jpg?oh=fe76d2ef964d6c09ee482733f9ab1c76&oe=563B82CB&__gda__=1448072628_2d8de191c4a8735260d7440983d610fd&width=1280&auto=webp&quality=80&disable=upscale)


Ok, this is better! Now every brick has a clearly defined border and shape! This is closer to becoming fully functional…until we go through the colorblind test, where it… ugh. But hey! We’re making progress, at least now we can distinguish each individual brick!

![](https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-xft1/v/t1.0-9/11880573_10153259063653025_5316325294993772947_n.jpg?oh=7e4c5d305bf720b661b9de480f95e339&oe=567F8368&__gda__=1447368602_bfddd07b9ecdacb7d707d691d9e7b6dc&width=1280&auto=webp&quality=80&disable=upscale)


Wow... this is a smart use of shapes! You’ll see that beyond the borders, each block is different depending on the piece it belongs to. Even without colors, you no longer see shapes fusing with each other, and you can properly identify pieces even when they are cluttered.

So, now that we’ve seen how borders and shapes work, let’s get hands on illumination!

What we adopted from photography and movies: the 3 point lighting!

This is the most simplified way to explain illumination! In every given scene, objects and environments should be illuminated by more than one light, as usually one light will not be enough to define every object’s border and shape. The minimum number of lights that can used to define an object is 3, as triangulating light around any 3D object will almost certainly give you enough information about its borders and shapes. This works using 3 lights for 3 different purposes:

Key Light: This light is the main light of your object/scene. It is usually (but not always) the brightest of the 3. It can be placed with relative freedom (preferably within the 180 degrees in front of the camera), as the other 2 lights’ position will depend on the placement of the Key Light.


![](https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-xfp1/v/t1.0-9/11825006_10153259045813025_3791312812805107441_n.jpg?oh=db01124928094996fa6cfe63bd4c260d&oe=564521B7&__gda__=1447998418_b25d66c6fc96e94cfbab1f040a731c86&width=1280&auto=webp&quality=80&disable=upscale)


Fill Light: The purpose of this light is to demonstrate volume. This is the light that defines shape. As such, it should affect the most surface space possible. It is usually placed within 90 degrees from the position of the Key Light.


![](https://scontent-mia1-1.xx.fbcdn.net/hphotos-xaf1/v/t1.0-9/11825006_10153259045828025_1744961852553414777_n.jpg?oh=bf637398247d6668ba7ca10251246ce6&oe=5682F9AC&width=1280&auto=webp&quality=80&disable=upscale)


Rim Light: This light is used to define borders. It is usually the least visible one, as it will always be illuminating an object from behind. It is usually placed somewhere around 180 degrees from the Key Light.


![](https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-xfp1/v/t1.0-9/11825006_10153259045823025_2953508765467633478_n.jpg?oh=fa5a213007ae358a7d5ab6b03f9a5cdd&oe=564A216E&__gda__=1447497227_d695979712a7f48178352d497a62fd98&width=1280&auto=webp&quality=80&disable=upscale)


So, if we were to see a scene from the top, the diagram would look something like this:

![](https://fbcdn-sphotos-g-a.akamaihd.net/hphotos-ak-xpa1/v/t1.0-9/11825006_10153259045818025_8048340984003761354_n.jpg?oh=1b501f9ad0860bb577c17a290c61c050&oe=56426EE4&__gda__=1447779314_5a269113745e6c87580448d562f6b323&width=1280&auto=webp&quality=80&disable=upscale)


This technique is widely used in photography and film (it was actually created by them), as it requires the least quantity of lights to generate optimal, visually informative compositions. If you watch a film or check out posters and promotional artwork, this technique will kind of hit you in the face (actually, take a little break and search for your favorite movie posters!):

![](https://scontent-mia1-1.xx.fbcdn.net/hphotos-xfp1/v/t1.0-9/p206x206/11870900_10153259047558025_5661289340213398652_n.jpg?oh=9a9f7135681027a0f4127c126aed1421&oe=564DC821&width=1280&auto=webp&quality=80&disable=upscale)


So, now that we see how 3-point lighting works, let’s see how we can apply it on videogames.

The first thing to notice is that this works perfectly when the output is a still image or a non-interactive video. In Games, however, we have a problem: Both camera and player are usually in the control of someone else. So, let’s see how we can translate this to abstract and side-scrolling games:

In abstract games we saw the example of Tetris. Everything regarding borders and shapes in these type of games relies on how you render the “pieces” or “blocks” you use to build it, as most times camera is fixed, regardless of the player’s movement.

In side-scrolling games, however, this takes a more complex twist. There are many ways to approach 3-point lighting, yet the one I’ve found more useful is this:

First, divide the scenery in 3 areas:

-The Foreground: Whatever elements lie in front of the character.

-The Midground: Where the action takes place. This is where you’ll find most interactive elements, and where your character will spend most of her/his time.

-The Background: Whatever lies behind the character.

You can have 8 layers of parallax if it’s a 2D game, or you could have more than 3 “grounds” if your assets are 3D. Still, separate them in the 3 areas above.

Then, assign each light to one of the areas. For example, this is a scene from Systole, a game I’m currently working on:

![](https://scontent-mia1-1.xx.fbcdn.net/hphotos-xfp1/v/t1.0-9/11870900_10153259047538025_7759955027341724329_n.jpg?oh=8a5b15a812af9c51cfac13ad4e314b98&oe=5640185A&width=1280&auto=webp&quality=80&disable=upscale)


And here’s how each light was assigned:

![](https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-xft1/t31.0-8/11838645_10153259047543025_7565557339167892439_o.jpg?width=1280&auto=webp&quality=80&disable=upscale)


You’ll see that the Key Light (placed at Midground) will illuminate both the midground and the background, but does little to illuminate the foreground, as it remains backlit. The Fill Light, (placed at foreground) will give volume to the shapes in the foreground and midground, but leave the background somewhat unattended. Finally, the Rim Light is placed at the background, and stretches all the way to the foreground elements. This way I make sure every object is defined by their borders, but only the midground is affected by all 3 lights at once.

Depending on which layer you assign each light to, you can create different illumination dynamics to play with. In this case, for example, we needed a light dynamic that could properly light the scene, but at the same time obscuring objects in the foreground and background, as we didn’t want to give players too much visual information that could confuse them.

In this scene, most of the foreground elements’ borders are defined not by light, instead they’re defined by the contrast they create against the well-lit Midground. And by making sure the Fill Light doesn’t stretch over to the background, we can give a sense of volume to the most immediate objects without giving unnecessary shape information on background elements.

Can get a bit complex, huh?

Well, not really. As long as you keep in mind the purpose of each of these 3 lights, you can play with them however you want to create very different results. For example, Limbo takes an extreme approach to this. If you see any screenshot of the game (there’s one below), you’ll quickly notice that every light source is pushed into the background. It actually IS the background. The Fill Light in this game only serves to illuminate fog and mist… yes, it doesn’t even illuminate physical objects! But by doing so, it creates the depth players need in order to distinguish elements in the background from elements in the midground, so they don’t get confused and try to step on a tree branch placed in the background.

![](https://scontent-mia1-1.xx.fbcdn.net/hphotos-xpf1/v/t1.0-9/p206x206/11870900_10153259047548025_4574088659363126230_n.jpg?oh=a2e9bae2056dc5661e7dd79078fc97da&oe=5637D17F&width=1280&auto=webp&quality=80&disable=upscale)


We’ll leave it at this point for now. Next week, we’ll be taking a look at replicating the 3-point lighting concepts in 3rd person games, and the role that color temperature plays in its successful implementation.

The scene I used as an example for this article is from SYSTOLE, a side-scrolling game currently Live on Kickstarter. During the course of this month, we'll be posting a weekly “tutorial/making of” video where we’ll be showing the process of making an enemy from conception to production, modeling, texturing, animation and coding. We’ll be posting the videos at:

So, that's it for today! hope you enjoyed this article and learned something from it! see you next week! :)