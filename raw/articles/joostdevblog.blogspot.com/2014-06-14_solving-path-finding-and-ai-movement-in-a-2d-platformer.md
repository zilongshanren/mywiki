---
title: Solving path finding and AI movement in a 2D platformer
url: http://joostdevblog.blogspot.com/2014/06/solving-path-finding-and-movement-in-2d.html
author: Joost van Dongen
published: '2014-06-14'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com), we started with the most complex part: how to do path finding and movement? When people think of path finding, they usually think of A*. This well-known standard algorithm indeed solves the finding of the path, and in games like an RTS that is all there is to it, since the path can easily be traversed. In a platformer however the step after the finding of the path is much more complex: doing actual movement over the path. Awesomenauts features a ton of different platforming mechanics, like jumps, double jumps, flying, hovering, hopping and air control. We also have moving platforms and the player can upgrade his jump height. How should an AI know which jumps it can make, how to time the jump, how much air control is needed? This turned out to be big challenge!

Since there are so many potential subtleties in platforming movement, my first thought was that handling it in our behaviour trees might not be doable at all. Behaviour trees are good at making decisions, but might not be as good at doing subtle controls during a jump. Add to that that the AIs only execute their behaviour trees 10 times per second because of performance limitations, and I expected trouble.

![](../../assets/ce4ff39499355cfb.jpg)

The solution I came up with was to record tons of gameplay by real players and generate playable path segments from this. By recording not just the player's position but also his exact button presses, I figured we could get enough information to replicate real movement with precise control. Player movement would be split into short bits for moving from one platform to another. The game could then stitch these together to generate specific paths for going from A to B.

To perform movement this way, the behaviour tree would choose where it wants to go and then executes a special block that takes control and fully automatically handles the movement towards the goal. Very much like playing back a replay of segments of a players' previous movement. The behaviour tree could of course stop execution of such movement at any given time to engage in combat, which would again be controlled entirely by the behaviour tree.

While the above sounds interesting and workable, the devil is in the details. We would have to write recording and playback code, plus a complex algorithm to analyse the recorded movement and turn that into segments. But it doesn't end there. There were six character classes at the time, each with their own movement mechanics. They could buy upgrades that make them walk faster and jump higher. There are moving platforms that mean that certain jumps are only achievable in combination with certain timing of the platform position. All of these variations increase the complexity of the algorithms needed, and the amount of sample recordings needed to make it work. Then their would need to be a way to stich segments together for playback: momentum is not lost instantly, so going into a jump while previously going to the left is not the same as when going into that same jump while previously going to the right.

The final blow to this plan was that the levels were constantly changing during development. Every change would mean rerecording and reprocessing the movement data.

These problems together made this solution feel just too complicated and too much work to implement. I can still imagine it might have worked really well, but not within the scope of a small indie team building an already too complex and too large multiplayer game. We needed a simpler approach, not something like this.

Looking for a better solution we started experimenting. Programmer Bart Knuiman did an internship at

[Ronimo](http://www.ronimo-games.com)at the time and his internship topic was AI, so he started experimenting with this. He made a small level that included platforming, but that did not need path finding because there were no walls or gaps. Bart's goal with this level was to make a Lonestar AI that was challenging and fun to play against, using only our existing behaviour tree systems. Impressively, he managed to make something quite good from scratch in less than a week. Most Ronimo team members lost their first battle against this AI and took a couple of minutes to find the loopholes and oversights one needed to abuse to win. For such a short development time that was a really good result, so we concluded that for movement and combat, the behaviour trees were good enough after all.

![](../../assets/eae86baeef4d9240.gif)

The only thing really impossible with the systems we had back then was path finding in complex levels. We designed a system for this and Bart built this as well. The important choice we made here was to split path finding and movement into a

*local solver*and a

*global solver*. I didn't know that terminology back then, but someone told me later that it was a common thing with an official name. For finding the global route towards the goal we used path finding nodes and standard A* to figure out which route to take over them. The nodes are spaced relatively far from each other and the local solver figures out how to get to the next node.

![](../../assets/561bad5910b4bb8c.jpg)

The local solver differs per character class and can use the unique properties of that type of character. A jumping character presses the jump button to get up, while one with a jetpack just pushes the stick upwards. The basics of a local solver are pretty simply, but in practice handling all the complexities of platforming is a lot more difficult, yet still doable.

![](../../assets/18c9c7b6d6f59036.gif)

The complex recording system outlined at the start of this post was incredibly complex, while the solution with the local and global solvers is so much simpler. The reason it could be so simple is that although platforming mechanics in Awesomenauts are diverse, they are rarely complex: no pixel-precise wall jumps or air control are needed like in Super Meat Boy, and moving platforms don't move all that fast so getting on to them doesn't require super precise timing. These properties simplify the problem enough that creating a local solver in AI is quite doable.

One aspect that I haven't mentioned yet is how we get the path finding graph. How do we generate the nodes and edges that A* needs to find a route from A to B? The answer is quite simple: our designers place them by hand. Awesomenauts has only four levels and a level needs well below one hundred path finding nodes, so this is quite doable.

![](../../assets/d432f34fbb6e649b.jpg)

While placing the pathfinding we need to take the different movement mechanics into account. Some characters can jump higher than others, and Yuri can even fly. Each class has his own local solver to handle its own movement mechanics, but how do we handle this in the global solver? How do we handle that some paths are only traversable by some characters? Here the solution is also straightforward: any edge we place in the path finding graph can list included or excluded classes. When running A* we just ignore any edges that are not for the current character type. This was originally mostly needed for flyer Yuri: all other classes were similar enough that they could use the same path finding edges.

A similar problem is that falling down from a high platform is possible even if it is too high to jump towards, and jumppads can also only be used in one direction. These things are easy to include in the path finding graph by making those edges only traversable in one direction.

Creating the path finding graph by hand has a couple of added benefits. The first is that we can exclude routes that may work but are too difficult for the local solver to traverse, or are not desirable to use (they might be too dangerous for example). Placing the nodes and edges by hand adds some control to make the movement look sensible. Another nicety is that we can add markers to nodes. The AI can use these markers to decide where it wants to go. For example, an AI can ask the global solver for a route towards "FrontTurretTop" or towards "HealthpackBottom".

The path finding nodes were placed by our designers and they also built the final AIs for the bots. Jasper had made the skirmish AIs for

[Swords & Soldiers](http://www.swordsandsoldiers.com)and he also designed the bot behaviours for Awesomenauts.

Awesomenauts launched with only six classes and only four of them had a bot AI. Since then many more characters were added, but they also never received bot AIs. Now that modders are making AIs for those we will probably have to update the edges to take things like Swiggins' low jump and the hopping flight of Vinnie & Spike into account.

To me the most interesting aspect of pathfinding in Awesomenauts is that after prototyping we ended up with a much simpler solution than originally expected. This is a good reminder that whenever we think about building something complex or something that is too much work, we should spent some time prototyping simpler solutions, hoping one of them might work.

*PS. The AI tools for Awesomenauts have been released for modders in patch 2.5. Modders and interested developers can try them out, including our pretty spectacular AI debugging tools. They are free to use for non-commercial use, check the included license file for more details. Visit our*

Very interesting read :)

ReplyDeleteI always look forward to your new blog posts!

eye-opening!

ReplyDelete