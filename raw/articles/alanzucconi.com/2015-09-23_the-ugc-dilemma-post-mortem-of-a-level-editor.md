---
title: 'The UGC Dilemma: post-mortem of a level editor'
url: https://www.alanzucconi.com/2015/09/23/the-ugc-dilemma-post-mortem-of-a-level-editor/
author: Alan Zucconi
published: '2015-09-23'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

It is undeniable that *user generated content* is getting more and more relevant for games. When a player has the power to create their own content , they engage with the game in a completely new way. But if you’re a developer, you should know that creating a proper level editor can be even more time consuming that creating the game itself. Giving players the chance to create content is not enough: it *has* to be fun. On top of that, level editors need to be intuitive, or players won’t be able to use them properly. The best solution is a trade off between giving players the power to create whatever they want, and the need to simplify it.

![500px-Puzzle_Creator_initial_view](../../assets/53234c2213b72179.png)

A perfect example of this is Valve’s [Puzzle Creator](http://theportalwiki.com/wiki/Puzzle_Creator), which beautifully captures the essence of Portal’s gameplay. There is no space for scripting or custom events, making most of the original levels from Portal impossible to replicate. Valve has made a very clear design choice: they add constraints, but in a way that guide players’ creativity.

This post go through some of the challenged I encountered while working on the level editor for [0RBITALIS](http://store.steampowered.com/app/278440), and how I solved them. I will show in the second part how the editor actually works.

#### The style of the editor

[0RBITALIS](http://store.steampowered.com/app/278440) is a gravity simulator disguised as a puzzle game. It is not surprising that since its very first release, players asked for a level editor. [0RBITALIS](http://store.steampowered.com/app/278440) has a very unique style, and the entire game contains little (if any) text at all. I wanted the level editor to be based on the same logic, with as little text as possible. I also wanted something different: the game heavily uses red and black, and this was the perfect chance to show something completely different, yet still coherent.

![e3abe8f6fc9fcd718e722fac9cb57deb](../../assets/183442e3b8c5675b.gif)

In a game about gravity, being able to understand how planets will move is essential. Unfortunately it turns out that a single screenshot from the game doesn’t give many clues on how objects are moving. This encouraged me to design the editor in a way that made orbital mechanics obvious even with just a glance. I added links between gravitationally bounded bodies, and drawn orbits using a dashed line. Every dash takes exactly a second to be covered by the planet, giving visual clues about the orbital speed and direction.

#### Designing the controls

![3](../../assets/3389a2355cbb448d.png)

The biggest challenge has been designing a set of tools which allowed players to manipulate planets (and their orbits) without any text or traditional menu. I decided to go with handles: they stick out of planets, and players can drag them to alter their solar system (see picture). There is no indication about what they do, but this is in line with the style of the game: everything in [0RBITALIS](http://store.steampowered.com/app/278440) has to be a discovery, and I want players to try and play with the interface.

#### Limitations and constraints

Despite its minimalistic aesthetic, [0RBITALIS](http://store.steampowered.com/app/278440) has quite a lot of content. It was pretty much clear that bringing it all to the editor would have been a real challenge. I decided to include enough content to allow players to create interesting levels. But at the same time, I skimmed most of the eye candies and the minor features, making the editor much more intuitive and easy to use. Some of the features which I decided to skim from the editor are: elliptical and Lissajous orbits; comets, pulsars, teleports, nebulae; enemies and missiles; destructible planets; coloured planets and stars; scanning and landing missions and, finally, scripted events.

There is another important limitation which I decided to turn into a feature: the mass of an object depends only on its size. This allowed me to condense asteroids, planets, gas giants and stars into a single object. Conceptually, they are the same thing: the only difference is their mass. It takes only a glance to realise how massive objects are, just by looking at their size.

When you are working on a game there is always a trade off between the amount of work you put into it, and the money it will make. I believe that removing those features was the right choice; implementing them is a time investment which I believe I would have not recouped easily.

### Part 2: How the editor works

You can access the editor from the title screen of [0RBITALIS](http://store.steampowered.com/app/278440). The first screen will show a list of your previously created levels. You can select each one individually to edit it, or creating an entirely new one.

When working on a level, it will appear as a blueprint. There are three classes of objects available: planets, stars and probes. When a planet is orbiting a star, an arrow will link them. Orbital paths are also drawn with a dotted line. In the editor, the mass of an object is always proportional to its size. I tested this style both on new and experienced players: they all understood the editor correctly, providing they knew how the game works.

#### Move an object

![rotate](../../assets/099d71b543e2864d.gif)

You can move every object just by dragging it to the position you want. This will automatically determine their initial angle and orbital distance when the level starts. If other objects are orbiting the planet you’re moving, they relative angle and position will be preserved.

#### Make an orbit

![link](../../assets/a7a84c0b5a1c7bf3.gif)

Objects that are not connected to anything are called *stationary*. They will not move when the game starts. If you want them to orbit around a planet or a star, you have to drag the down arrow onto it. You can only orbit around objects which are highlighted in red. You can drag the arrow onto the body itself to make it stationary again.

#### Change the orbital speed

![duration](../../assets/2d8efbc878a972be.gif)

You can change the time it takes for an object to complete is orbit using its *speed arrow. *This determines the speed of the object, which is visualised by its orbit. Each arc represent a second: the more arcs, the slower it is. You can invert the orbital speed, to make your object orbiting clockwise or anticlockwise.

#### Change the mass

![resize_probe](../../assets/238612052168e066.gif)

Planets and star are actually the same object in [0RBITALIS](http://store.steampowered.com/app/278440). What it changes is their mass. You can use the *mass handler* to change the mass of an object. This will affect both its size and the way it is rendered. Small objects are asteroids, they then become rock planets, gas giants and finally stars. You can also invert the direction of the mass handler, giving planets and probes a negative mass. Negative gravity will repel standard probes, but attract anti-probes.

#### Creating a new object

![new](../../assets/03d09220a3e0f45e.gif)

On the top right corner of the screen there are two buttons. The first one create a new celestial body (a planet or a star), the second a new probe (that thing you launch). Object are positioned randomly, but you can drag them to the position you want.

#### Destroy an object

![delete](../../assets/b3052842080b3043.gif)

To destroy an object, simply drag it into the top left corner. If something is attached to it, it will be destroyed as well. Every level should always at least one probe; you cannot delete an orbital tree if this would leave you with no probes.

#### How to play user generated levels

Once saved, levels are available in the [Steam Workshop](http://steamcommunity.com/app/278440/workshop/). If you find a level you like, click on the “Subscribe” button and it will be available in the in-game “Workshop” screen. These are some of my favourite levels so far…

### Conclusion

Designing the editor for [0RBITALIS](http://store.steampowered.com/app/278440) was a real challenge; overall, I am very pleased with the result and I believe making it was the right choice. Level editors can be very hard not just to create but also to integrate with Steam. Before embarking on such a quest, make sure that what you are doing meets the players needs and expectations. Not every game requires a level editor. And even for the ones who do, it does not automatically means it will increase their revenue. Depending on the type of game you have, you should also be careful about what users are creating: this wasn’t a problem for [0RBITALIS](http://store.steampowered.com/app/278440), but many games have a [Time To Penis](http://www.urbandictionary.com/define.php?term=TTP) which is less than a minute.

## Leave a Reply Cancel reply