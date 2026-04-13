---
title: How is this Game Rendered?
url: https://www.gamedeveloper.com/art/how-is-this-game-rendered-
author: Game Developer
published: '2020-08-07'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Horror in the Museum

Recently, I made a small, experimental game called [Horror in the Museum](https://schmidt-workshops.itch.io/the-horror-in-the-museum) and submitted it to [#LowRezJam](https://www.indiedb.com/tags/LowRezJam) over on itch.io. The main requirement of that game jam is for games to be limited to 64 x 64 pixels. Here is a screenshot from Horror at the Museum game as it appears there:![Screenshot of Horror in the Museum - Here we see a submarine on display Screenshot of Horror in the Museum - Here we see a submarine on display](https://media.indiedb.com/images/members/4/3827/3826399/profile/Screenshot_005.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Submarine

I started this game with a very simple idea in mind. I wanted to come up with a different way to render a 3D level. I'm going to share the techniques and thought process behind it here.

Vector Graphics:

As a bit of background information, you should know that I am working on another much larger, more complex game called

[Paradox Vector](https://schmidt-workshops.itch.io/paradox-vector). That game uses 3D line draw commands to emulate the vector graphics games of the early 1980's. I wrote about how I was able to use this process to draw 3D objects in

[this article](https://www.indiedb.com/games/paradox-vector/tutorials/making-a-modern-vector-graphics-game). It is my feeling that vector graphics are a source for real artistic potential that has remained untapped for the past few decades, since raster graphics effectively took over the video game scene back then.

Paradox Vector attempts to look like those early arcade games, but it also tries to create a more complex world than any vector graphics games were able to.

![Screenshot of Paradox Vector Screenshot of Paradox Vector](../../assets/8593810e96f2254e.jpg)

A Different Approach to Vector Graphics:

Horror in the Museum does not look like a vector graphics game at all, but it actually is. Allow me to explain. Instead of using vector lines to draw the outlines or shapes of game objects, as I do in Paradox Vector, I decided to use them to define the space between objects, the negative space.

The green "fog" you are seeing is not typical 3D fog but actually a large number of straight lines that are drawn each frame, in a pattern around the player's camera. They extend in all directions, some being roughly parallel to the player's view, while others perpendicular, and still others traversing the player's view at various angles.

Here's what the game looks like at its full resolution...![Horror in the Museum at full resolution - nothing creepy is lurking behind the shark display! Horror in the Museum at full resolution - nothing creepy is lurking behind the shark display!](../../assets/b747724ea759d8b2.jpg)


This is not some kind of 2D filter placed over the image, but the 3D lines themselves. As the camera sees further, it can see more of these lines in the distance, and the "fog" therefore gets brighter, as more lines overlap one another. The dark shapes stand out as they effectively hide any lines that would be drawn through or behind them.

Originally I had lines drawing all at right angles to one another. This created a grid-like effect which I found very interesting. It definitely provided a different feeling, but it looked too calm and organized for a horror game. I later added lots of different angles to the lines, and also caused the lines to switch directions randomly, to create the flashing, strobe effect. However, for the sake of thoroughness, here's what it looked like when the lines were all perpendicular and static...![Perpendicular vector lines Perpendicular vector lines](../../assets/c8409c574a5ad349.jpg)


I think this is something with a lot of potential. I would like to explore it further, but perhaps in a different game.![Sky and water shaders Sky and water shaders](../../assets/ff9c198e5275e77d.jpg)


Some things like the sky and reflective water are done with the standard, built-in rendering tools that come with any 3D engine. Those have nothing to do with the 3D lines.

Why 64 x 64?

I reduced the screen resolution to 64 x 64 pixels just to be able to submit this to [LowRezJam](https://itch.io/jam/lowrezjam-2020). So, while the scenes are created with vector lines, the game's camera filter ends up converting it into a low resolution pixel game. It reduces the resolution and gives the impression of some kind of scratched film effect.

![Animated gif of Horror in the Museum Animated gif of Horror in the Museum](../../assets/cfaccbf53b4787bd.gif)


Why Am I Doing This?

Working on Paradox Vector made me realize the [vast potential of vector graphics](https://www.indiedb.com/games/paradox-vector/news/vector-graphics-the-new-retro) in terms of offering new ways of generating imagery. I just think it's something that has not been deeply explored since the 1980s, and I think it has a lot of untapped possibilities. I would love to see other game developers taking up this idea to explore it further.

In this case, I feel like the experiment was a success. I used vector graphics to create a different way of rendering a 3D scene. I was surprised that it ended up looking so much like the standard 3D fog, but it also has its own distinct look and feel. Ultimately, I feel I accomplished what I had set out to do. I hope to hear any thoughts or feedback you might have about this method, or about my other games. I am also happy to answer any questions you may have.