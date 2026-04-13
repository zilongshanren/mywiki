---
title: Migration
url: https://blog.gemserk.com/migration/
published: '2011-10-06'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

-
-
1 2 3 4 5 6 7

When simplifying the world in a grid and started thinking in terms of textures, it was easier to apply different kind of image algorithms like drawing a filled circle or a line which were really useful when optimizing. There are even more image operations that could be used for the game logic and rendering. SC2 has a lot of information in terms of textures, not only the player's vision, and they provide an <a href="https://www.youtube.com/watch?time_continue=1&v=-fKUyT14G-8">API to access it and it is being used for machine learning experiments.</a> I am still working on more features and I plan to try some optimization experiments like using c# job system. I am really excited about that one but I first have to transform my code to make it work. I would love to write about that experiment.


-
-
-
1 2 3 4 5 6 7

It was used to build different kind of games/prototypes and even a full game like the <a href="https://blog.gemserk.com/2013/01/05/clash-of-the-olympians-for-android/">Clash of the Olympians</a> for mobile devices, and it worked pretty well. <h1>What about now?</h1> Right now we are not using any of this in Unity. However we never lost interest nor feith in ECS, and there are starting to appear new solutions over Unity in the last years that caught our attention. <a href="https://github.com/sschmid/Entitas-CSharp">Entitas</a> is one of them. The Unity team is working towards this path too as shown in this <a href="https://www.youtube.com/watch?v=tGmnZdY5Y-E">video</a>. Someone who din't want to wait started <a href="https://github.com/Spy-Shifty/BrokenBricksECS">implementing that solution</a> in his own way. We've also watched some Unite and GDC talks about using this approach in big games and some of them even have a Scripting layer too, which is awesome since, in some way, it validates we weren't so wrong ;). I am exited to try ECS approach again in the near future. I believe it could be a really good foundation for multiplayer games and that is something I'm really interested in doing at some point in my life.


-
-
-
1 2 3 4 5

There is a Unity Unite talk named "<span id="eow-title" class="watch-title" dir="ltr" title="Unite Europe 2017 - Squeezing Unity: Tips for raising performance"><a href="https://www.youtube.com/watch?v=_wxitgdx-UI&list=PLX2vGYjWbI0Rzo8D-vUCFVb_hHGxXWd9j&index=9">Unite Europe 2017 - Squeezing Unity: Tips for raising performance</a>" by <a href="https://www.linkedin.com/in/idundore">Ian Dundore </a></span>about things you can do in your game to improve Unity performance by explaining how Unity works behind the scenes. Update: I just noted (when I was about to complete the post) there is another talk by Ian from Unite 2016 named "<a href="https://www.youtube.com/watch?v=n-oZa4Fb12U"><span id="eow-title" class="watch-title" dir="ltr" title="Unite 2016 - Let's Talk (Content) Optimization">Unite 2016 - Let's Talk (Content) Optimization</span></a>", which has other good tips as well.

-
1 2 3 4 5 6 7

There is a Unity Unite talk named "<span id="eow-title" class="watch-title" dir="ltr" title="Unite Europe 2017 - Squeezing Unity: Tips for raising performance"><a href="https://www.youtube.com/watch?v=_wxitgdx-UI&list=PLX2vGYjWbI0Rzo8D-vUCFVb_hHGxXWd9j&index=9">Unite Europe 2017 - Squeezing Unity: Tips for raising performance</a>" by <a href="https://www.linkedin.com/in/idundore">Ian Dundore </a></span>about things you can do in your game to improve Unity performance by explaining how Unity works behind the scenes. Update: I just noted (when I was about to complete the post) there is another talk by Ian from Unite 2016 named "<a href="https://www.youtube.com/watch?v=n-oZa4Fb12U"><span id="eow-title" class="watch-title" dir="ltr" title="Unite 2016 - Let's Talk (Content) Optimization">Unite 2016 - Let's Talk (Content) Optimization</span></a>", which has other good tips as well. There are two techniques to improve Unity UI performance we use at work they didn’t mention in the video and we want to share them in this blog post. One of them is using <a href="https://docs.unity3d.com/Manual/class-CanvasGroup.html">CanvasGroup</a> component and the other one is using <a href="https://docs.unity3d.com/ScriptReference/UI.RectMask2D.html">RectMask2D</a>.


-
-
-
1 2 3 4 5 6 7

The theme of this LD was <a href="https://ldjam.com/events/ludum-dare/38">"A small world"</a> and our game was <a href="https://arielsan.itch.io/pigs-mayhem-in-space">Pigs Mayhem in Space</a>: https://www.youtube.com/watch?v=8prOyQeyCnE After iterating over a thousand ideas (yeah, I like to exaggerate, they were only 999) the first day, we ended up with a 3d, turn by turn game where you have to use projectiles and physics to kill the other players (like Worms). This is one of the first concept:


-
-
-
1 2 3 4 5 6 7

Obviously, by taking a look at the game mods/maps available it is clear that you could build entire games over the SC2 engine, but I wanted to see the basics, how to define and control the game logic. As a side note, I love RTS games since I was a child, I played a lot of Dune 2 and Warcraft 1. I remember playing with the editors of <a href="https://www.youtube.com/watch?v=nRe39UyYFjU">Command & Conquer</a> and <a href="https://www.youtube.com/watch?v=1C_m682LRsw">Warcraft 2</a> also, it was really cool, so much power ;) and fun. With one of my brothers, each one had to make a map and the other had to play and beat it (we did the same with Doom and Duke Nukem 3d editors). <h1>SC2 Editor</h1> SC2 maps are built with Triggers which are composed by Events, Conditions and Actions to define parts of the game logic. There are a lot of other elements as well that I will talk a bit after explaining the basics.


-
-
-
1 2 3 4 5 6 7

To complete this post, here is a video showing a prototype of how I load and play a replay which was created by playing with two players in LAN, one was my computer and the other was my phone: https://www.youtube.com/watch?v=ofHoUhypED0 The quote of the day is 'Fail as much as possible, as soon as possible to avoid failing when it is too late'.


-
-
-
1 2 3 4 5 6 7

Here is a video explaining and showing the game: https://www.youtube.com/watch?v=_hNxfiXmeAE <h3>Analysis</h3>

-
1 2 3 4 5 6

And here is a really fun video of the game to finish the post: https://www.youtube.com/watch?v=xk_q3Zv_5w8


-
-
-
1 2 3 4 5 6 7

I keep making prototypes about what I talk in the <a href="http://blog.gemserk.com/2011/10/06/modifying-textures-using-libgdx-pixmap-in-runtime/">previous post</a>, in this case I made an example of how to interact between the game entities (the bombs in the video) and the Pixmap data (the platform of the video) by adding some kind of basic collision detection checking the Pixmap's pixels with alpha value different from zero. I only wanted to share the a video showing the experiment: https://www.youtube.com/watch?v=PUK-s4kW1ug As always, hope you like it. Probably more information on next posts.


-
-
-
1 2 3 4 5 6 7

The next video shows how I am using the Pixmap class of <a href="http://code.google.com/p/libgdx/">libGDX</a> library to modify textures dynamically. https://www.youtube.com/watch?v=SibDf_2LLvQ In the previous video there are two textures, they start with the same pixmap data. Then I start to paint and erase pixels from each texture to show how the pixmap operations works over the two pixmaps. Finally, I start rotating both textures and then paint and erase stuff again, to show how I am transforming from game world coordinates to each pixmap coordinates.


-