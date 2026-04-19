---
title: runevision blog
url: https://blog.runevision.com/2016/
published: '2016-12-04'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I've spend the past few days at [Exile](http://www.exile.dk/) (like a game jam but not a jam this year). I've envisioned having a whip in [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple) for a long time, and at Exile I began developing this whip mechanic.

In the main game, the whip is meant to be just one element in the gameplay, aiding in puzzles, like being able to grab and switch levers from a distance, and grabbing objects to pull towards you. However, for now I started out making a little self-contained game based just around the whip, so that I could focus on getting the feel right first.

At the end of Exile I had "whipped up" a little game I might call "Eye of the Temple - Whip Arena". Here's a video of the gameplay:

![](../../assets/47655e798835830a.jpg)

Implementing the whip physics was rather tricky. I've ended up with something that doesn't work quite like a real-world whip - you can't really make it do a crack in mid-air - but feels very responsive in its own way. The sound and haptics is based directly on the simulation, and I found it quite satisfying to use.

Now I'm wondering if I should take a little break from developing the full Eye of the Temple game and try to get this little arena game (which is much smaller in scope) finished and released first. I wonder if it's something people might be interested in? It definitely got positive reactions and feedback at Exile.

I'm thinking it would work well as an infinite game with high scores. There's not yet any fail condition though - I'm trying to think what might work well for that. I also need to implement some kind of bonuses and multipliers in the scoring probably.

As a side note - after spending several days prototyping and implementing this whip mechanic at Exile, I ended up with quite sore shoulders from whipping so much. ;)

If you have a Vive and would like to be an early tester of Whip Arena, let me know.


I've been working on a VR game for the past months. It's called Eye of the Temple and it's a Vive game quite unlike any other.

Here's a pre-alpha trailer for it!

![](../../assets/118366bbaa194a5c.jpg)

That's the first time I've made a trailer by the way. Quite challenging but also fun! It's got some placeholder models in it and it's made from playtest footage rather than clips made specifically for this trailer, but I tried to make the best of what I got.

Eye of the Temple is currently at an early stage in development.

Speaking of placeholder models, I'm just beginning now to look into working with contractors to have some nice art created for the game. If you know of any skilled concept artists or 3d modelers who'd like to design ancient contraptions for a game like this, let me know!

I previously worked on the game jam game [Chrysalis Pyramid](https://runevision.itch.io/chrysalis-pyramid). Eye of the Temple is based on a similar core mechanic, but expands upon it in scope and variety, and is completely rewritten and redesigned from scratch. The goal is a commercial release in 2017.

Playtesting so far has been very promising and it's a lot of fun developing the game. Follow the development here and [on Twitter](https://twitter.com/runevision), and let me know what you think!


The Cluster is an exploration platformer game I've been developing in my spare time for some time. You can see all posts about it [here](http://blog.runevision.com/search/label/TheCluster).

As of the time being, I've put development of The Cluster on hold indefinitely.

![](../../assets/b8cad008df4a0317.png)


![](../../assets/b8cad008df4a0317.png)

### Burdens

After having worked on the game for more than ten years (!) I finally came to the conclusion that the overall design and constraints in the game is making it very hard for me to finish it, while also holding me back from trying out a lot of otherwise interesting ideas.

- The game is procedural and the same every time you play, which makes it super important to guarantee you can't get stuck.
- There is gravity and no ability to fly, which means you will get stuck unless the algorithms are carefully designed to make it impossible. It has to be more or less mathematically provable.
- The AI enemies can follow you practically everywhere, which means every obstacle needs to be coded to also be usable by AI.
- The world is constructed from a rather large-scale grid which makes things like large ramps and hills impossible (just a bit boring).
- The third-person perspective require art and animation resources for avatar and enemies.
- The side-scrolling format makes it hard to wordlessly attract the player to interesting things in the far distance, because only the immediate environment can be seen. This creates more of a reliance on maps and narratives to explain the reasoning for seeking out those far away things, and that plays against the procedural nature of the game.

Now, none of those things are impossible to overcome, and I did have a playable demo at the end of 2015 that worked under all of those constraints. But the game is not yet nearly varied enough, and every new feature is very tough to pull off under the burden of all those constraints.

### Focusing on my strengths

I've switched focus to working on projects that I hope both play more to my strengths, and should be possible to pull off in a shorter time frame.

- First-person perspective without jumping, so no fiddly physics.
- No humanoid characters, which decreases the demands for art, animation and "behaviors".
- No ambition of a story (some of my favorite games don't have one anyway).

This frees me up to focus more exclusively on making interesting environments, which is what I'm most passionate about.

The good news is that the time has not been entirely wasted. For one, I've learned a LOT. And for another I've developed several pieces of substantive tech that are fully reusable in my future projects.

Speaking of future projects, I'm working on a few already.

One is [The Big Forest](http://blog.runevision.com/2016/05/the-big-forest.html), though I'm not actively working on it right now. The focus here is to create nice, interesting and varied environments with very simple gameplay on top. I want it to me my own favorite walking simulator. In its current early stage it's already one of the best virtual forest experiences I've had.

The project I'm actively working on is a VR game for Vive that I've tweeted a little bit about and will soon announce properly here on the blog.

Stay tuned!


I've been continuing my work on the procedural terrain project I wrote about [here](http://blog.runevision.com/2016/03/note-on-creating-natural-paths-in.html). I added grass, trees and footstep sounds (crucial!) and it's beginning to really come together as a nice forest to spend some time in.

I made a video of it here. Enjoy!

If you want to learn more about it, have a look at this thread on the [procedural generation subreddit](https://www.reddit.com/r/proceduralgeneration/comments/4hb3on/the_big_forest_my_try_at_procedural_infinite/).

![](../../assets/c071d552fa2aeea6.png)


![](../../assets/c071d552fa2aeea6.png)


[article](https://blog.runevision.com/search/label/article),

[demo](https://blog.runevision.com/search/label/demo),

[design](https://blog.runevision.com/search/label/design),

[game design](https://blog.runevision.com/search/label/game%20design),

[game development](https://blog.runevision.com/search/label/game%20development),

[procedural](https://blog.runevision.com/search/label/procedural),

[PuzzleGraph](https://blog.runevision.com/search/label/PuzzleGraph),

[unity](https://blog.runevision.com/search/label/unity),

[usability](https://blog.runevision.com/search/label/usability),

[video](https://blog.runevision.com/search/label/video)

In the beginning of 2014 I was interested in procedurally generating computer games puzzles with typical elements like toggles, gates that can be triggered to open, boxes or boulders that can be moved onto pressure plates, etc. Many games contain elements like these and I took inspiration in particular from the game *Lara Croft and the Guardian of Light*.

To better understand these puzzles, and understand what makes a puzzle interesting or boring, I started creating a tool for analyzing and visualizing the state space of the puzzle. In the Procedural Content Generation mailing list I discussed the approach [here](https://groups.google.com/d/msg/proceduralcontent/bFTkuSv2EUE/_UkWMWw5oKUJ).I've worked on it on and off since, and while I still don't have an algorithm for procedurally generating the puzzles, the tool itself is interesting in its own right. It's called PuzzleGraph and I've just released it for free.

![](../../assets/f90ebc95f410a97f.png)


![](../../assets/f90ebc95f410a97f.png)

You can setup and connect puzzle elements like gates, toggles, pressure plates and boulders, and see the state space of the puzzle visualized, including solution paths, dead ends and fail states.

If you make some puzzles with PuzzleGraph, I'd love to see them!

The best demonstration is this video I made. If you already saw the video, skip down a bit for some new info and announcements.


Pathfinding is not just for finding paths for AI agents/NPCs and similar. It’s also for procedurally *creating* paths.

![](../../assets/4059287d27e666af.png)

While working on path creation for a procedural terrain, I had the problem that the generated paths would keep having too steep sections, like this:

![](../../assets/768bece780b66933.png)


![](../../assets/768bece780b66933.png)

It was too steep and also didn’t look natural at all. I kept increasing the cost multiplier for slopes, but it didn’t help.

Then it hit me: My function just penalized the vertical distance, but it didn’t make any difference if this vertical distance came gradually or all at once.

So in fact, my cost function wasn’t trying to avoid steepness - rather it was trying to make a path where the altitude changes *monotonically*. It would do everything it could to avoid the path first going up and then down again.

But I didn’t care if the path went a *little* up and down, as long as it wasn’t too steep at any point. To achieve this behavior, I needed to penalize steep slopes more than linearly, for example by squaring it.

This has the effect of penalizing abrupt changes in altitude and reward gradual changes.

And sure enough, after the change the generated paths avoided steepness and looked much more like what humans would create.

![](../../assets/4059287d27e666af.png)


![](../../assets/4059287d27e666af.png)

Tweaking pathfinding cost functions is one of those odd little things that I really enjoy. Seeing a little change in a formula imbue a generated creation with what could be mistaken for human design is really fascinating and fun!

### Further notes

The observation-turned-blog-post in its original form ended there, but I've compiled some further notes for those who want to dig into the details.

#### Pathfinding method

Let me tell about the method I use for the pathfinding, since I was asked about this. I won't do an introduction to pathfinding in general here but assume understanding of the principles of performing pathfinding using an algorithm like *A** or similar on a *graph* of *nodes* connected by *edges*.

Such a graph can be represented in many ways. Sometimes it's a data structure with explicit data representing all the nodes and edges and how they're connected. Other times it can just be a grid (like a 2D array) and each cell is implicitly connected to the neighboring cells - maybe the 4 or 8 neighbors, depending on whether diagonal connections are used.

It doesn't really matter, and a pathfinding algorithm can typically easily be modified to work with one or the other. Apart from giving it a start node and goal node, the important part is that you can tell the algorithm:

- Which other nodes are a node connected to?
- What is the real or estimated cost of getting from one node to another?

You might have data for this stored in advance or you might calculate the answers on the fly when asked.

For the terrain pathfinding I do the latter. In fact, there is neither an explicit graph, nor any 2D array. There is no data structure at all for the pathfinding to happen inside. Instead, it's all implicit, based solely on coordinates. I tell the pathfinder what the start and end coordinates are, and there's a function for getting "neighbor coordinates" to a given coordinate. There's also a function for getting the cost of getting from one coordinate to another, as you saw earlier.

This may sound completely free-form and magical at first, but there still is a structure that must be adhered to. You must imagine a grid structure and ensure the coordinates always fall within this grid. In my case it's a plain quadratic cell grid where each cell has a size of 5. So the start coordinate, goal coordinate, and every provided neighbor coordinate must always have x and y values that are multiples of 5. You also shouldn't use floating-point numbers for this, since they can produce floating point precision errors, and even the slightest imprecision can cause the pathfinding to completely fail.

I wanted my paths to be able to have a natural, non-jagged look, so I wanted edges to come in 16 directions instead of the basic 8. The 8 additional directions are achieved by going two cells out and one to the side. This provided me with an interesting choice of whether the 8 other directions should also go two cells out, or just one.

![](../../assets/2733ebe6618cc4dd.png)


![](../../assets/2733ebe6618cc4dd.png)

In theory the second option can be weird, since if you need to move just one cell the path have to first side-step by two cells. But in practice both seems to work fine. The first images in this post were made with the first option but I later decided to use the second to avoid the path having very small-scale zig-zags.

#### Effects of different parameter values

I got asked on the proceduralgeneration sub-reddit:

How rapidly does the path change as you increase the power from 1.0 to 2.0? What happens if you go past 2.0? Does the path eventually have to spiral around the mountain or something?

I had actually been content just using the values I had found which seemed to work well enough, but now that I'd been asked, of course I wanted to find the answers too! I tried doing the pathfinding with the power values 1.5, 2.0 and 3.0 and with the multiplier values 1, 2, 3, 4, 5, 6, 7, 10, 15, 20, and 25. I had moved the multiplier inside the power function since the original version of the code, so those multipliers are multiplied onto the steepness before the resulting value is raised to the given power. Here's a table of the results.

![](../../assets/a199502691439e59.png)


![](../../assets/a199502691439e59.png)

Some notes on the result.

Overall the common theme is that the results range from straight and boring to wildly tortuous. At the extreme end, the path begins to create loops - something that should be impossible with path-finding. However, the edges I use in the path-finding can cross each other. This means that they can appear to loop even though they never pass through the same points from the perspective of the path-finding. They only begin to do this once the path-finding is so extremely sensitive to tiny changes in altitude that the small difference in altitude between one of two crossing edges is enough for it to exploit it to loop around. I should say that I only sample the altitude at the end-points of each edge, which appears to be fully sufficient except in the extreme cases like this.

Note that there are very similar occurrences across the different power values. For example, multiplier 10 at power 1.5 looks just like multiplier 6 at power 3.0, and multiplier 7 at power 2.0 looks just like multiplier 5 at power 3.0. Does this mean that any result you can get with one power value, you can also get with another? That there exists a transformation that means they're mathematically equivalent? No, I don't believe so. It feels like there's subtle differences. For example, the progression of paths with power value 3 begins to do loops before it begins to take a major detour, while for power value 2, the loops only start happening after it has begun doing a large detour. The differences are very subtle though and hard to put the finger on exactly.

One thing that's tempting to look for is qualitative differences, such as some paths doing many small zig-zags and others doing larger swoops. However, I think that's a red herring. The algorithms doesn't measure sharpness of turns or frequency of turns in any way and shouldn't be able to tell one from the other. I think that the seeming qualitative differences are thus up to unpredictable aspects of how the path-finding interacts with the terrain height function that sometimes just happen to produce one result or the other. To answer it in terms of the original question: If the terrain was perfectly conical, a path from the base to the top might equally well form a spiral, a zig-zag pattern, or any other combination of left-winding and right-winding sections.

My own pragmatic takeaway from this is that sticking with just a power value of 2 seems fine and I'd then use multiplier values between 3 and 15 depending on how straight or tortuous I want the path to be.

### Perspectives

These generated paths were a proof-of-concept for a new project I'm working on and I'm sure I'll learn more as I go along. For example, already I'm learning some things about approaches for flattening the terrain around the paths which I may share at a later point when I'm a bit more sure of my findings. For now, I hope you found this useful!

### 2024 update: Code available

I've now released a framework called [LayerProcGen](https://github.com/runevision/LayerProcGen) as open source, and one of the sample scenes generates natural paths using the technique described in this article. So a fully functional implementation is now available for study and use.