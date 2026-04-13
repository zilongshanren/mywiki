---
title: Combining 2D and 3D in Blightbound's VFX
url: http://joostdevblog.blogspot.com/2020/11/combining-2d-and-3d-in-blightbounds-vfx.html
author: Joost van Dongen
published: '2020-11-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

An important focus during development of [Blightbound](https://www.blightbound.com/) is that we we wanted to achieve a 2D look but have 3D movement and a 3D camera. A particular challenge are special effects: we had tons of [experience with 2D special effects](http://joostdevblog.blogspot.com/2016/09/creating-crisper-special-effects-with.html), but now the special effects also needed to communicate depth. For example, how far does that area-of-effect damage reach exactly? In this blogpost I will show a number of tricks we used to combine 2D and 3D in the Blightbound VFX.

This blogpost is based on an conversation I had with [Ronimo](http://www.ronimo-games.com/) VFX artist Kees Klop. Unfortunately Kees won’t be staying at Ronimo: for budget reasons we can’t keep him on after November. So, if you’re looking for a stellar VFX artist, be sure to send him a message on his [Art Station](https://www.artstation.com/smearkees) or [email](mailto:KeesKlop97@hotmail.com).

Let’s start by having a look at the Gravity Well skill that some of the mages have. This is a spell that draws in all the enemies near it, making for an excellent combo with area-of-effect attacks by the Mage’s teammates. Like many of the VFX in Blightbound, this effect combines several types of geometry. Here's what it looks like, and a breakdown of some of its elements.

*A video of the Gravity Well effect in-game and in our animation editor.*

![](../../assets/cc055e6c6e584943.jpg)

![](../../assets/3e72ae73cf649f8c.gif)

The next effect I would like to discuss is the Deck of Daggers skill that some rogues have. Several knives are thrown, and those that hit get stuck in the enemy for a while, causing damage over time. These knives are rotated out of the enemy's plane to add depth. It's a subtle effect, but having many of such subtle 3D effects in the game in total adds a lot of depth to the 2D drawings.

*The Deck of Daggers effect or, as Triss would say it: "I'm a fan of knives!"*

Also, our animation tech helps here: since Blightbound plays skeletal animation in real-time (as opposed to rendering it down to spritesheets as we previously did), objects like these knives can really stick to a body part and move along with it. While that's an obvious option to have on 3D characters, it's a lot less common to be able to do this with 2D animation without using a rather stiff animation technique. Our animation workflow however is a topic for a separate, future blogpost.

One of the most screen-filling effects in the game is the victory at the end of a dungeon, after defeating the dungeon's boss. Here we see a combination of many elements, including one that's not used often in our special effects because it's so all-encompassing: colour grading. The colours of the whole scene get changed during this effect.

*The victory effect in-game and in our animation editor. Blight (a corrupting mist) is an important theme in Blightbound. Since this effect marks the end of a successful run, it sucks in and dissolves a lot of mist.*

![](../../assets/ed37869fc2ba4dd5.gif)

*Many special effects in Blightbound are made 3D by overlapping flat planes under various angles.*

![](../../assets/3f0abccbbd71da81.gif)

*A lot of the visual effects also feature bits of frame-to-frame animation. Many of those were made by Ronimo while many others were taken from the*

[RTFX Generator](https://videohive.net/item/rtfx-generator-440-fx-pack/19563523)pack, including this particular one.The warrior's Warcry ability shows another technique for combining 2D and 3D. Warcry is an area of effect ability that buffs teammates. Since the range of the ability is very important, the starting point here is a circle on the ground. However, that's very flat and becomes less readable when sticking through things like grass or small stones. So to make the effect more 3D, a vertical cylinder with an animating swirl is added.

*The Warcry skill in-game and in our editors.*

![](../../assets/0ba2834a725f7ed4.gif)

*Here's a little teaser: update 0.5 (coming this November) adds the new Tamed Wolf sword to Blightbound. A special perk of this sword is that when the warrior uses his shield, his teammates are also shielded. This effect visually overlaps with the Warcry skill. As you can see here, this shield effect makes the verticallity above the circle even stronger.*

On to the assassin's Chakram ability! This is a large projectile that flies, hangs still for a while and then comes back. Unlike most other projectiles it's visible long enough that it's much more than just a flash. Also, it deals damage in an area of a meter or two, so it's quite large.

*The Chakram skill in Blightbound.*

The Chakram is a horizontally flying circular thingy. With the relatively low camera of Blightbound it was seen under too extreme an angle, making it look too flat. We didn't want to turn it into a 3D model though since we wanted to maintain the 2D, handpainted feel of the graphics. The solution is simple: the Chakram is tilted towards the camera a bit. This is subtle enough that it feels like the Chakram is horizontal, but it adds just enough angle that it looks a lot less flat. This is a technique that we use a lot in Blightbound.

![](../../assets/6b256b67e6e4b443.jpg)

![](../../assets/8f84d1e4b8f664fb.gif)

*While the main graphic of the Chakram is entirely flat, it's made more spatial by animating the pitch and adding particles and swooshes that move out of the plane.*

The special effects shown in this blogpost were all made by Kees Klop, whose work I wanted to celebrate today. However, he is not the only special effects artist who worked on Blightbound: [Koen Gabriëls](https://vimeo.com/46219758) and [Luuk van Leeuwen](https://www.artstation.com/scytha) also made a lot of VFX. Koen did most of the early work of establishing the style for the Blightbound effects. Currently Koen and his intern [Ayrthon van de Klippe](https://www.artstation.com/ayrthonvdklippe) are working on making VFX for upcoming Blightbound updates.

Finding the right combination of 2D and 3D in the VFX for Blightbound was quite a search during early development of Blightbound. Our artists ended up combining a lot of different techniques, including hand-drawn art, frame-to-frame animations, meshes, particles, intersecting planes, screen distortions and even colour grading. I think the end result works really well in-game: it looks good, fits the style and communicates the gameplay well.

Thanks for posting this, very insightful!

ReplyDelete