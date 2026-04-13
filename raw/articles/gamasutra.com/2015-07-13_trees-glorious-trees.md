---
title: Trees, Glorious Trees!
url: https://www.gamedeveloper.com/art/trees-glorious-trees-
author: Dave Beck
published: '2015-07-13'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Trees, Glorious Trees!

A short blog about the importance of trees in American history and the process behind making them for my historical game, Tombeaux.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

As I've mentioned before, [Tombeaux ](http://paverson.itch.io/tombeaux)has a main narrator character who we hear reading journal entries throughout the game experience. But there is a group that I would argue upstages our narrator, and that (as you probably guessed by the title) is the trees. Before the [St. Croix](https://en.wikipedia.org/wiki/St._Croix_River_(Wisconsin%E2%80%93Minnesota)) was a river of recreation for fishing, canoeing, and speedboating like it is now, it was a river of pine, acting as one of the nation's busiest highways for timber in the mid to late 1800's. During this time, non-logging boats were lucky to get up the river at all, due to the waterway being clogged full of floating logs (or even worse, a logjam that stopped everything in its path). Since the St. Croix directly connects with the Mississippi, and it had what seemed to be an unlimited supply of tall and straight trees growing along its edges, it was a resource ripe for the picking (or chopping...sorry).

![Pinus_strobus_trees Pinus_strobus_trees](../../assets/814624ce74913e87.jpg)


L: group of Pinus strobus, R: distribution map of tree (images via wikipedia)

While Tombeaux is not entirely about the logging industry, it definitely does take the player on a journey to see what it might have been like both before and after the timber harvest. Because of this, I wanted to set the stage by creating an old growth forest, with the main silvan feature being that of [Pinus strobus](https://en.wikipedia.org/wiki/Pinus_strobus), or the eastern white pine. These old growth forests of white pines are nearly impossible to find now, as only 1% remain in North America due to logging in the late 19th and early 20th centuries. This type of pine is the tallest tree found in the eastern (and northeastern/midwest) United States and Canada. With a mature white pine living well past 200 years old, reaching heights of well over 150 feet (while keeping a very straight trunk), and a diameter of 3-4 feet, they were particularly attractive to lumber barons.

![pinus_strobus_moodboard pinus_strobus_moodboard](../../assets/161645676919b37f.jpg)


Mood Board for reference

After doing some visual research, both online and in person ([last post I wrote about my trip to northern Wisconsin, in which I did some bark texture reconnaissance](https://tombeauxgame.wordpress.com/2015/07/09/research/)), it was time to dive in to creating this giant beast of the forest, including the many iterations that it might take, such as sawed-off stumps, beaver-chewed stubs, and dead (needle-less) versions (both standing and downed). Additionally, I wanted to make sure I was creating an environment that felt both native and diverse, filled with other types of trees such as oak and birch. At a later date, I plan to return to the detail meshes and plants, to create native species such as wild celery (an underwater type of river weed/grass), wild rice, ferns, and wildflowers.

![speedtree_whitepine speedtree_whitepine](../../assets/173076e4c0b63ac4.png)


One iteration of an eastern white pine, inside SpeedTree

Once I compiled a small mood board, I set out to learn and use a new program that I had been itching to try, called [SpeedTree](http://www.speedtree.com/). It is an industry standard tree and foliage creator for both movies and games, and now that it is naturally [integrated into Unity 5 and Unreal 4](http://www.speedtree.com/video-game-development.php), we will most likely continue to see a great deal of high quality natural environments in the coming years from both indies and AAA companies. One way to use their tech is by paying and downloading high-quality, pre-made tree assets from their store (but what's the fun in that?!). Another, more creative way is by paying a [$19 per month subscription fee ](https://store.speedtree.com/)to use their modeling/creation software. As a point of reference, two months of paying for the software is actually cheaper than the $39 price tag for a single tree from their store!). Since it is my goal to create as much in my game as possible from scratch, I decided to download the software and start making assets myself.

![stumps stumps](../../assets/b9a78de8eec8cb2b.jpg)


2 Stumps and 1 Gnawed Beaver Tree in SpeedTree

![bare_tree bare_tree](../../assets/2d0dff7b7d432be1.jpg)


Bare (Dead) White Pine in Speedtree w/ Bark Detail

Simply put, SpeedTree is my new favorite software. One can quickly and easily create natural assets for a game, using an intuitive, node-based interface that tries to mimic how a tree is naturally constructed. Starting with a trunk, and then adding elements such as roots, branches, and leaves provides for a very smooth workflow. Everything is highly customizable as well, with integrated wind effects, collision capsules, seamless branching, randomizers, break points for branches or trunks, and automatic billboard and LOD (level of detail) creation upon export to Unity. Once I created a base white pine tree, I was quickly able to create many iterations by simply removing leaves (bare tree) and breaking and capping trees (stumps). I didn't even use many of their features, and hope to dive deeper into the program when I use it to create plants and other detail foliage. Again, I can't say enough about how much this program has helped my environment-heavy project achieve a great look.

![LOD_unity LOD_unity](../../assets/9d9cddf6e578123b.jpg)


LOD transition feature in Unity (LOD 0 on left w/ 9K tris, LOD 2 on right w/ 2K tris)

Once you bring a SpeedTree asset into the Unity engine, it offers other great options for you to tweak. With the LOD's that were auto-created/exported by SpeedTree, you can adjust them to your liking in the engine, so that it seamlessly transfers to a billboard at the distance you set. I really like the fact that you can also drag and drop the trees into the scene as objects or prefabs. Since these also have the LOD settings, you could put a hero tree (a hi-poly, hi-detailed tree) in your scene without having to worry about relying on Unity's finnicky terrain. With that said, I painted most of my trees on the terrain, as it makes it much easier when you have a large amount of assets to place and randomize.

![tombeaux_5 tombeaux_5](../../assets/7f4edfaa852bcaeb.png)


Here there be beavers...and downed trees...the perfect natural barrier!

Due to my game being on a river, it is important that I have some invisible walls that will stop the player from continuing up and down the river at their leisure. Implementing barriers correctly is tricky, as you don't want the barrier to scream "HEY, I'M AN INVISIBLE WALL PUT THERE BY A GAME DESIGNER WHO DIDN'T REALLY CARE ABOUT YOUR IMMERSIVE EXPERIENCE THAT MUCH!" (sorry, it is one of my biggest pet-peeves in games). While natural-looking barriers are great, you also don't want it to be mistaken for just another stick or bush in the game that one thinks they can walk over. I try to put some purpose behind the walls when possible, which is where things like downed trees, beaver dams, and beaver-gnawed stubs come in to play (plus, it's always a great way to show off some of your hard work in a more up-close view!).

![tombeaux_2 tombeaux_2](../../assets/3d7ebdf18e104b68.png)


The view from directly outside the cabin door

While the exterior river scene is hardly complete, I'm happy with the progress I've made in the past few days on the tree elements. So far, I've created and placed four iterations of the white pine, three of the birch, and two of the oak. Additionally, I have three white pine stumps, three gnawed-beaver stubs, and three downed trees. Once I give the same attention to the plants and detail rocks (they are all currently the low-quality placeholder plants that Unity provides), spend some time on the lighting (it is just a single real-time directional light w/ default skybox at the moment), and add some environmental effects like haze and fog, the river will hopefully start to look more like it did 200 years ago.

This post was originally found at [https://tombeauxgame.wordpress.com/](http://tombeauxgame.wordpress.com/)

![tombeaux_3 tombeaux_3](../../assets/6bb434066f6b851a.png)


Looking up to the cabin from the river (underneath a couple towering pinus strobus)