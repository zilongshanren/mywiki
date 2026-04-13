---
title: 'New School Blues Dev. Diary #7: Flash Puppets'
url: https://www.gamedeveloper.com/art/new-school-blues-dev-diary-7-flash-puppets
author: Yoyo Bolo
published: '2013-01-24'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# New School Blues Dev. Diary #7: Flash Puppets

Originally posted on November 6th, 2012, this developer diary entry examines Flash puppets and cut-out style animation. Artist and animator Jonathan Phillips walks us through with in-game art.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

### Developer Diary #7: Flash Puppets

Last week I took you through my process for designing the “New School Blues” characters. This week I’ll talk about how I created the artwork that will actually appear in the game. Since NSB is a graphic adventure game I will need to create a lot of artwork very quickly. I need to draw all of the backgrounds and fill them with props and set dressing, the items that the player will pick up, all of the characters from both the front and the side, the user interface elements, and create animations for all of the characters.

![](../../assets/1e46222b6a3c54cf.png)


Here’s a few stills of Boy New Kid in action


Traditional frame-by-frame animation is a very time intensive process, but there are other techniques that can be used to create animation much more quickly. One such technique is called “cut-out animation”, which makes use of a puppet that can be reposed for every frame of the animation, rather than creating an all new drawing for each frame. Here’s an [example](http://www.youtube.com/watch?v=LMpXUd_kesA).

By an incredible stroke of good fortune (and definitely not because it has been firmly embedded as the industry standard for creating web graphics and animation for nearly a decade) we chose to build our game using Adobe Flash, which just so happens to be tailored toward creating cut-out style animation.

![](../../assets/20c8228596c81fb5.png)


The many pieces that make up a Flash puppet


You start by splitting the character into several pieces that can be moved independantly to create virtually whatever pose you might need. This approach is not without its own problems however. At each joint, as the limb bends the outline tends to break and cause jagged points to jut out. There are ways to combat this, like making all of the lines a single width, but that is less than ideal and creates a very flat looking drawing. You can also tediously tweak and fiddle with the lines around each and every joint until they are all just right. Or you can just get rid of the lines completely, and use all of the time you just saved to do the actual animating part.

![](../../assets/616b85fef5a36c30.png)


Having lines along the edges of your pieces can cause problems


That first clip was from Terry Gilliam of Monty Python fame. For a closer look at that process [click here](http://www.youtube.com/watch?v=xs7WaL44_Iw) to see a great video that showcases how this style of animation is done.