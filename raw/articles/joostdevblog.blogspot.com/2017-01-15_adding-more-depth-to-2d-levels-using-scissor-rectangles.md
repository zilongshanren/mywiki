---
title: Adding more depth to 2D levels using scissor rectangles
url: http://joostdevblog.blogspot.com/2017/01/adding-more-depth-to-2d-levels-using.html
author: Joost van Dongen
published: '2017-01-15'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](https://www.awesomenauts.com/)and

[Swords & Soldiers 2](http://www.swordsandsoldiers2.com/)our artists often struggled with how to create more depth. All those background elements from one area would slide into view in other parts of the level, limiting how deep the backgrounds could be. For the Starstorm level in Awesomenauts I've added a trick to our editors that solves this problem: scissor rectangles. It's a neat little trick that not only makes Starstorm have backgrounds with much more depth, but also makes rendering them a lot more efficient. So let's have a look: what's the problem exactly, and how do scissor rectangles solve it?

In a purely 2D game like Awesomenauts there's no real perspective: backgrounds are just a lot of 2D textures. As the camera moves all those layers move at different speeds to suggest depth. Traditionally in games that's called

*parallaxing*. From a technical perspective that's basically all there is to 'perspective' and 'distance' in a game like Awesomenauts.

However, this simple idea of objects following the camera creates a big problem. An object that is really far away hardly moves on the screen when the camera moves. The mountain in front of you in the far distance? Walk 10 meters to the left and it's still in front of you. Walk 100 meters to the left and it's still in front of you. It's so far away that it's basically always in front of you. That's realistic and as intended, but what if two rooms in your level should have different objects in them? If the rooms are really deep (like for example a factory hall) then the objects in the back of one room will be visible in the other.

![](../../assets/65e5f032c6f183b4.jpg)

In a 3D game the solution to this is simple: just put a wall in between these two rooms. But this is not a 3D engine. This is a purely 2D engine and walls that go into the distance are not supported. Heck, we don't even have a z-buffer to figure out what parts would be in front of or behind that wall! Also, what if we don't want a wall? What if we want to suggest really deep spaces but don't want to put endless walls into the distance in between them?

The solution our artists used in older Awesomenauts maps is that such deep rooms can't be close to each other. For example, in Ribbit IV the top part of the level is a lush jungle that continues far into the background. Originally my colleague Ralph also added deep caves in the bottom part of the map, but parts from the jungle became visible in the caves, and vice versa. So Ralph made the caves less deep. The jungle parts are still rendered behind the caves, but because the caves have a solid wall close to the camera the jungle isn't visible there anymore.

![](../../assets/7a1597b9e2ca824f.jpg)

Not only is this very limiting for our artists, it's also a huge waste of performance: it causes a lot of overdraw. 'Overdraw' is when several objects are rendered on top of each other. The more objects are rendered on top of each other, the higher the overdraw is and the worse the framerate gets. Sometimes that's needed to get a certain effect, like when having lots of overlapping smoke particles. But here it's a waste: the jungle isn't even visible, so why render it? High overdraw is the number one performance drain in Awesomenauts, so not doing this would be quite wonderful. (For more on overdraw have a look at this post:

[Optimising Special Effects In Awesomenauts](http://joostdevblog.blogspot.nl/2013/02/optimising-special-effects-in.html).)

![](../../assets/582b46ab55f271d5.jpg)

I had been thinking about this problem for a while, mostly coming up with solutions that were quite a lot of work to build, when one day I realised that videocards have a very simple feature that solves exactly this problem: scissor rectangles! The basic idea of a scissor rectangle is that when rendering an object, you tell the videocard to only render the parts of it that are within a certain area on the screen: the scissor rectangle. Everything else is cut off. It's like a mask in Photoshop, but in-game.

![](../../assets/ffa261417d1ef395.jpg)

Scissor rectangles are a very simple and very limited feature. They only do rectangles that are aligned with the screen. So you can't have a rotated rectangle, or a shape that's more complex than a rectangle. If you want any of that you'll need to resort to more involved tech, like the stencil buffer, which isn't efficient to recreate differently for each object rendered. I was looking for something simpler, something that could be changed for each object rendered without causing a performance hit. Scissor rectangles provide exactly that.

![](../../assets/abd48168c23fa189.jpg)

The next question is how to integrate scissor rectangles with our tools: how can an artist easily define which objects are cut off by which scissor rectangle? I chose to link scissor rectangles to our animation system. An 'animation' in the RoniTech (our internal engine) is simply just a bunch of objects that might be animated, so a part of a level can also be an 'animation'. I made it so that each animation can have a custom scissor rectangle, placed by the artist. The resulting workflow is that a level artist creates a room or area in the animation editor, adds a scissor rectangle and then puts the entire 'animation' in the level. It's an easy and fast workflow.

Our levels are mostly decorated by my colleague Ralph, using art drawn by Gijs. On the Starstorm map Ralph used scissor rectangles extensively for the first time and I love the result: he put a lot of depth and detail in the backgrounds and the framerate is higher than on other maps because the scissor rectangles reduce overdraw. Here's a short demo video:

For any programmers that read this, here are some implementation details I've encountered. Feel free to skip this list if you're not a programmer. ;)

- The videocard wants to know about scissor rectangles in screen coordinates, while the way we use them means our tools place them in world space. To use scissor rectangles this way you'll need to convert the coordinates yourself before sending them to the GPU.
- If you accidentaly swap the top and bottom of the scissor rectangle then everything will still work fine on AMD and NVidia GPUs, but on some Intel GPUs the objects will disappear altogether.
- It's not allowed to define scissor rectangles that are partially or entirely outside the screen, so be sure the cap them to the edges of the screen.
- The relevant functions in OpenGL are
*glEnable(GL_SCISSOR_TEST)*and*glScissor()* - DirectX 9:
*SetRenderState(D3DRS_SCISSORTESTENABLE, TRUE)*and*SetScissorRect()* - There are equivalent functions that we use on Xbox One and Playstation 4. I haven't checked on mobile but I expect scissor rectangles are a standard feature on practically all videocards.

![](../../assets/c9281707639da414.jpg)

So there you have it: scissor rectangles! Not only did they enable our level artists to make deeper, richer levels, but they also improved performance by reducing overdraw and were quick and easy to add to our engine.

If you want to give your artists even more control to optimize renderable areas, use Clipper: http://www.angusj.com/delphi/clipper.php

ReplyDeleteAh yeah Clipper, we actually had a look at that one for a procedural thingy, but it turned out to not do specifically the thing we were looking for at the time.

DeleteYeah, the increase of quality in Starstorm really makes it look stunning! Scissor rectangles make me look forward to seeing more maps in the future!

ReplyDelete