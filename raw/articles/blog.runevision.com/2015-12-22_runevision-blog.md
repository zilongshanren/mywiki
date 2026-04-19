---
title: runevision blog
url: https://blog.runevision.com/2015/
published: '2015-12-22'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

[design](https://blog.runevision.com/search/label/design),

[game design](https://blog.runevision.com/search/label/game%20design),

[game development](https://blog.runevision.com/search/label/game%20development),

[graphics](https://blog.runevision.com/search/label/graphics),

[procedural](https://blog.runevision.com/search/label/procedural),

[TheCluster](https://blog.runevision.com/search/label/TheCluster),

[unity](https://blog.runevision.com/search/label/unity),

[usability](https://blog.runevision.com/search/label/usability)

The Cluster is an exploration game I've been developing in my spare time for some time. You can see [all posts about it here](http://blog.runevision.com/search/label/TheCluster). It looks like I didn't write any posts about it for all of 2015, yet I've been far from idle.

[By the end of 2014](http://blog.runevision.com/2014/12/the-cluster-2014-retrospective.html) I had done some ground work for fleshing out the structure of the world regions, but the game still didn't provide visible purpose and direction for the player.

My goal for 2015 was to get The Cluster in a state where it worked as a real game and I could hand it over to people to play it without needing instructions from me. Did The Cluster reach this goal in 2015? Yes and no.

![](../../assets/487b85981c6d67d8.png)


![](../../assets/487b85981c6d67d8.png)

I made a big to-do list with all the items needed to be done for this to work. (As always, the list was revised continuously.) I did manage to implement all these things so that the game in theory should be meaningfully playable. I consider that in itself a success and big milestone.

However, I performed a few play tests in the fall, and it revealed some issues. This was not really unexpected. I've developed games and play tested them before, and it always reveals issues and shows that things that were designed to be clearly understandable are not necessarily so. I don't consider this a failure as such - when I decided on my goal for 2015 I didn't make room for extensive iteration based on play test findings. I did manage to address some of the issues already - others will need to be addressed in 2016.

On the plus side, several players I had playing the game had a good time with it once they got into it with a little bit of help from me. In two instances they continued playing for much longer than I would have expected, and in one instance a play-tester completed clearing an entire region, which takes several hours. I think only a minority of players can get that engaged with the game in its current state, but it was still highly encouraging to see.

### Essentials

Some boring but important stuff just had to be done. A main menu. A pause menu. Fading to black during loading and showing a progress bar. (I found out that estimating progress for procedural generation can be surprisingly tricky and involved. I now have a lot more understanding for unreliable progress bars in general.) Also, upgrading to Unity 5 and fixing some shaders etc.

![](../../assets/3b0b6f5a2dd978f7.png)


![](../../assets/3b0b6f5a2dd978f7.png)

### Enemy combat

I had AI path-finding working long ago, but never wrapped up the AIs into fully functional enemies. In 2015 I implemented enemy bases in the world to give the enemies a place to spawn from and patrol around.

![](../../assets/0ab71a93b1be8bc6.png)


![](../../assets/0ab71a93b1be8bc6.png)

Enemy combat also entailed implementing health systems for player and enemies (with time-based healing for the player), implementing player death and reloading of state, and having the enemies be destroyed when the player enters certain safe zones.

For the combat I decided to return to a combat approach I used long ago where both player and enemies can hold only one piece of ammo at a time (a firestone). Once thrown, player or enemies have to look for a new firestone to pick up before they can attack again. This facilitates a gameplay alternating between attacking and evading. I noticed that the game [Feist](https://playfeist.net/) uses a similar approach (though the [old version of my game](http://runevision.com/multimedia/cavex/) that used this approach is much older than Feist).

![](../../assets/aac7c63f5cba1eed.png)


![](../../assets/aac7c63f5cba1eed.png)

I decided to begin to use behaviour trees for the high-level control of enemies. This included patrolling between points by default, spotting the player on sight, pursuing the player, but look for firestones on the ground to use as ammo if not already carrying one. Then returning to patrolling if having lost sight of the player for too long. Even AI logic as simple as this turned out to have quite some complexities and edge cases to handle.

### Conveying the world structure

The other big task on my list after enemy combat was making the world structure comprehensible and functional to the player.

Worlds in The Cluster are divided into large regions. One region has a central village and multiple shrines. All of those function as safe zones that instantly destroys enemies when entered and saves the progress. In addition, a region has multiple artefact locations that are initially unknown and must be found and activated by the player. This basic structure was already in place by the end of 2014, but not yet communicated to the player in any way.

I've done my share of game design but I'm still not super experienced as a game designer. It took a lot of pondering and iteration to figure out how to effectively communicate everything that's needed to the player, and even then it's still far from perfect. In the end I've used several different ways to communicate the world structure that work in conjunction:

- Supporting it through the game mechanics.
- In-world as part of how the world looks.
- In meta communication, such as a map screen.
- Through text explanations / dialogue.

### Supporting world structure through game mechanics

There are a number of game mechanics that are designed to support the world structure.

The artefacts that are hidden around the region can be discovered by chance by exploring randomly, but this can take quite a while and requires self-direction and determination that not all players have. To provide more of a direction, I introduced a mechanic that the shrines can reveal the approximate location of the nearest undiscovered artefact. This gives the player a smaller area to go towards and then search within.

![](../../assets/ae96374cf4fde4c3.png)


![](../../assets/ae96374cf4fde4c3.png)

In order to sustain most of the mystery for as long as possible, a new approximate artefact location can't be revealed until the existing one has been found. This also helps giving the player a single clear goal, they are still free to explore elsewhere if desired.

Once an artefact is found, a shortcut in the form of a travel tube can be used to quickly get back to a more central place in the region. Initially the tube exit would be close to a shrine, but the player might subsequently miss the shrine and be aimless about where to go next. Based on early play tests, I changed the tubes to lead directly back to a shrine. This way the player can immediately choose to have a new approximate artefact location revealed.

![](../../assets/43f93dd3f3975f38.png)


![](../../assets/43f93dd3f3975f38.png)

### World structure communicated in-world

I got the idea to create in-world road signs that point towards nearby locations in the region, such as the village and the various shrines. This both concretely provides directions for the player and increases immersion.

Particularly for a procedurally generated world, the signage can also help reinforce the notion that there is structure and reason to the world as opposed to it being entirely random as can be a preconception about procedurally generated worlds.

![](../../assets/b8cad008df4a0317.png)


![](../../assets/b8cad008df4a0317.png)

This entailed generating names for the locations and figuring out which structures to store them in. The signs can point to locations which are far outside the range of the world that is currently loaded at the max planning level. As such, the names of locations need to be generated as part of the overall region planning rather than as part of the more detailed but shorter range planning of individual places.

Next, I needed to make key locations look their part. I'm not a modeller, but I created some simple placeholder models and structures which at least can give the idea of a village and shrines.

![](../../assets/656c6614bfee681a.png)


![](../../assets/656c6614bfee681a.png)

![](../../assets/328a0cd1c04a1f50.png)


![](../../assets/328a0cd1c04a1f50.png)

### Improved map screen

I had created a detailed map for the game long ago, but that didn't effectively communicate the larger overall structure of a region.

To remedy this I created a new map that shows the region structure. I've gone a bit back and forth between how the two maps integrate, but eventually I've concluded that combining them in one view produces too much confusing simultaneous information, so they are now mostly separate, with the map screen transitioning between the two as the player zooms in or out.

Here's examples of the detail-map and the region-map:

![](../../assets/1daafb01ad8ce2dc.png)


![](../../assets/1daafb01ad8ce2dc.png)

![](../../assets/7f5dadb754969d94.png)


![](../../assets/7f5dadb754969d94.png)

Apart from the map itself, I also added icons to the map to indicate the various locations as well as the position of the player. Certain locations in the game can be known but not yet discovered. This mean the approximate location is known but not the exact position. These locations are marked with a question-mark in the icon and a dotted circle around it to indicate the area in which to search for the location.

![](../../assets/a2c452944a77d12d.png)


![](../../assets/a2c452944a77d12d.png)

Part of the work was also to keep track of discovered locations in the save system.

### Dialogue system

Communicating structure and purpose through in-world signage and the map screen was not sufficient, so I started implementing a dialogue system in order to let characters in the game be able to explain things.

![](../../assets/9950e5be30dc2096.png)


![](../../assets/9950e5be30dc2096.png)

This too proved to be quite involved. Besides the system to just display text on screen in a nice way, there also needed to be a whole supporting system for controlling which dialogues should be shown where, depending on which kind of world state.

This can be complex enough for a manually designed game. For a procedural game, it's an additional concern how to design the code to place one-off dialogue triggers in among procedural algorithms that are used to generate hundreds of different places, without the code becoming cluttered in undesirable ways.

### What's next?

I hope to get The Cluster into a state where it's fully playable without any instructions in the first quarter of 2016.

After that I want to expand on the gameplay to make it more engaging and more varied.

As part of that I anticipate that I may need to revert the graphics in the game to a simpler look for a while. I've had a certain satisfaction from developing the gameplay and graphics of the game in parallel, since having something nice to look at is very satisfying to accomplish. However, now that I'll need to ramp up rapid development of more gameplay elements, having to make new gameplay gizmos match the same level of graphics will slow down the iteration process. For that reason I'll probably make the game have more of a prototype look for a while, where I can develop new gameplay with little or no time spent on graphics and looks.

Nevertheless, even with a much simpler look, I still want to retain some level of atmosphere, since one of the things I want to implement is more variety in moods. This is in extension to the game jam project [A Study in Composition](http://blog.runevision.com/2015/11/a-study-in-composition.html) I worked on this year.

If you are interested in being a play tester for early builds of The Cluster, let me know. I can't say when I will start the next round of play testing, but I'm building up a list of people I can contact once the time is right. Play testing may involve talking and screen-sharing over e.g. Skype since I'll need to be able to observe the play session.

If you want to follow the development of the Cluster you can follow [The Cluster on Twitter](https://twitter.com/TheClusterGame) or follow [myself](https://twitter.com/runevision).


[A Study in Composition](https://blog.runevision.com/search/label/A%20Study%20in%20Composition),

[demo](https://blog.runevision.com/search/label/demo),

[design](https://blog.runevision.com/search/label/design),

[game development](https://blog.runevision.com/search/label/game%20development),

[graphics](https://blog.runevision.com/search/label/graphics),

[procedural](https://blog.runevision.com/search/label/procedural),

[unity](https://blog.runevision.com/search/label/unity),

[video](https://blog.runevision.com/search/label/video)

Two weeks ago I participated in [Exile Game Jam](http://www.exile.dk/) - a cosy jam located remotely an hour's drive outside of Copenhagen. There was a suggested theme of "non-game" this year.

This was partially overlapping with the online [Procedural Generation Jam](http://itch.io/jam/procjam) (#procjam) which ran throughout last week with the simple theme of "Make something that makes something".

I wanted to make a combined entry for both jams. My idea was to create procedural landscapes with a focus on evoking a wide variety of moods with simple means. I formed a team with Morten Nobel-Jørgensen and got an offer to help with soundscapes from Andreas Frostholm, and we got to work.

You can download the final result here: [A Study in Composition at itch.io](http://runevision.itch.io/a-study-in-composition). You can also watch a video of it here:

Furthermore we decided to make the source code open source under the MIT license. You can see and download the [Unity project folder at GitHub](https://github.com/mortennobel/A-Study-in-Composition).

### Motivation

The motivation of the project was primarily to learn about how to create evocative and striking landscapes with simple means, particularly by creating harmonic and expressive color palettes. The name "A Study in Composition" is meant to convey this [in a similar sense as it's used in classical art](https://en.wikipedia.org/wiki/Study_%28art%29).

![](../../assets/7c7ae4fea45858b5.png)


![](../../assets/7c7ae4fea45858b5.png)

### Making the demo

Each scene consists of just a flat plane and a distribution of trees, all of it with simple colors without textures. Additionally there is a light source, variable fog amount, and sometimes a star-field. The trees are procedurally generated using L-systems and are distributed in many different ways using multiple noise functions.

#### Tree generation

Morten had created procedural trees with L-systems for previous work that we could make use of in this project. This was a huge head-start. During the project he worked on improvements such as support for leaves, a simple wind effect, and improvements to the algorithm.

#### Distribution of trees

We use a continuous noise function to distribute the trees. The function is evaluated twice - once at low frequency and once at higher frequency - and the values (between 0 and 1) are multiplied together. Simply put, this creates large clumps consisting of smaller clumps.

![](../../assets/d459339d243ac088.png)


![](../../assets/d459339d243ac088.png)

The resulting function is still between 0 and 1. For each position in a grid, we evaluate the function. The the function value is greater than a certain threshold, we place a tree.

The threshold value is different from scene to scene. We also add a random value to the threshold for each tree placement to make the edges of the clumps of trees more fuzzy. This randomness amount is also different from scene to scene. The result can create anything from dense forests to sparse savannas, and within a single scene, trees are not uniformly placed but clumps nicely in groups.

#### Color palettes

An important element of evoking different moods despite the simple means is in the color selection. First an initial color is chosen. This is done is HSV color space, where hue, saturation, and value are all values between 0 and 1. (The Value in HSV means brightness; not to be confused with lightness.)

A palette is created from the initial color by creating either a pair of complementary colors from it, or a color triad. The initial color determines the saturation and value of all the colors in the palette. This is a simple way to make the palette look consistent and harmonic.

![](../../assets/7006c091975d3adf.png)


![](../../assets/7006c091975d3adf.png)

Some extra color variations are created, and each scene element is then assigned a color from this palette. Each element knows its "normal" color and will attempt to choose a color from the palette similar to that. This will often result in natural landscapes with green grass, blue sky, brown branches, and green to red leaves. Sometimes though, nothing close to those colors will be available in the palette, and the result may be more surrealistic.

One thing I found during development was that palettes with low value (brightness) and high saturation always seemed to look bad. While I don't know for sure, my theory is that it's related to night vision. In our demo, a dark palette makes everything darker, including the sky, so it's synonymous with a darker light level, meaning dusk, overcast, or night time environments. In low-light environments, the color vision ability of the human eye becomes less effective, and the night vision ability - which is in gray-scale only - plays a larger role. So I think there's an expectation that low light environments don't have saturated colors, since our color vision is mostly out of play.

![](../../assets/df04eec2092a5c4c.png)

In any case, to avoid the unpleasant looking saturated dark colors, we simply multiplied the value (brightness) onto the saturation.

#### Soundscapes

Two thirds into the development, we showed the demo to Andreas who were making sounds for other jam projects too. In a short amount of time he managed to bang out soundscapes that added a lot of atmosphere to the demo while having zero constraints on how they should be played. The multiple pieces of sound files had different length but were each either non-rhythmical or only sporadically rhythmic, and they could be played on top of each other randomly and still sound good. The result is not always harmonic, but it intentionally uses the disharmony to create hypnotic soundscapes that interweaves between beautiful calm and eerie.

The sound files sounded fine all just playing simultaneously at the same value, but I added some extra variety by randomly adjusting the volume levels.

#### Cinematography

During development of the demo, I got tired of walking around manually using a first-person view, and pressing a button to change the environment. It seemed unnecessary to what we were doing, so we decided to make the camera movement and scene changes automatic instead. Non-games were encouraged and fully accepted in the two jams respectively anyway.

For camera movement we initially had a camera zooming fast by the trees, but following a tip from Tim Garbos to slow it down a lot made the scenes come much more to their right. Late in the process we settled on some variations of camera movement: Successive shots would vary between moving the camera forward or panning sideways left or right. It would also vary between being position at eye height (most common) or above the trees for a grander overview (more seldom).

We experimented with different ways of fading between shots. A cross-fade was impractical due to the need to have two scenes active at the same time, but we tried fading to black or white. Frequent fading detracted from the experience though. In the end we used no-frill cuts, but had every third cut be bridged by a dramatic cut to black inspired by the [opening to Vanilla Sky](https://www.youtube.com/watch?v=kagVPRjH0lE). I joked that we should win the award for pretentiousness if the jam had one.

Some tweaks were made after the Exile Jam was over, while ProcJam was still running. I made the groups of three scenes in between black cuts thematically coherent by keeping certain variables constant between them. While most variables are randomized in every new scene, the palette saturation and value, the fog amount, and the camera movement mode is only changed when a "black cut" happens. This lets you experience small variations of a theme with the black cuts resetting the senses in between changes to new themes.

### Future work

While there is a lot of ways the demo could be expanded and improved, we don't have any future work planned for this demo in itself. For me, I'm going to use what I've learned about creating variety in environments for my own other procedural projects.

We've also made [the source code for this demo available](https://github.com/mortennobel/A-Study-in-Composition) and if you do anything with it, we'd love to hear about it!


Procedural generation has gotten a lot more popular since my interest in it started 10 years ago. Today most game developers and even many gamers know what it means in broad terms.

In this piece I want to highlight fundamental differences between three approaches to procedural world generation: The simulation approach, the functional approach and the planning approach. The approaches are not only algorithmically very different but are also suitable for different types of games and gameplay. Here's a breakdown and analysis, with lovingly hand-drawn - err, *mouse*-drawn - illustrations.

### The three approaches

**The simulation approach** attempts to create an environment by simulating the processes that creates it. Terrain erosion, vegetation distribution based on plants competing over sunlight and nutrients, fluid dynamics, fire propagation and genetic algorithms all fall under this approach. Simulation approaches are not always based on reality. For example cellular automata simulations can be used to create nice cave patterns even though this is not mimicking how caves are formed in reality. The defining trait of simulations is that it's a process with calculation steps that are repeated many times in order to reach the end result.

![](../../assets/a95a227766db5875.png)


![](../../assets/a95a227766db5875.png)

**The functional approach** deals only with the desired end result and attempts to approximate it directly with a mathematical function. For height field based terrain, this could be using a Perlin Noise function, a fractal function, or any combination of many different functions to determine the height for a given coordinate. Similar functions (but for 3D coordinates) can be used for voxel terrain. For vegetation, mathematical functions can be used to determine the probabilities for various types of plants to appear at a given spot.

![](../../assets/0cc5adeedc787de8.png)


![](../../assets/0cc5adeedc787de8.png)

**The planning approach** doesn't primarily try to mimic nature at all, but instead plans out an area according to level design principles. For a terrain it might create a mountain range that can only be passed in a specific spot, or it could carve out a cave which contains a key inside that unlocks a vital door elsewhere. For vegetation it might create dense trees that block the player from taking an unwanted shortcut, or it might place plants and flowers in specific spots to try to create a certain emotion or feel related to that spot.

![](../../assets/0ad6548364b58fd2.png)


![](../../assets/0ad6548364b58fd2.png)

We'll get back to the planning approach in a bit. For now, let's compare the simulation and functional approaches.

### Context or no context

An important distinction of the functional approach is that the value at a given coordinate can be evaluated without regard for neighboring points. This is both a strength and a weakness.

The strength is that the generation is simpler and that it can more easily be divided up into smaller parts that don't rely on each other. No arrays need to be used for the generation except to store the end result and this means lower memory requirements.

For games with a pseudo-infinite world, such as Minecraft and No Man's Sky, the lack of dependencies on neighboring points (at least for terrain generation) is important. Since the world is generated in chunks on the fly, a point may need to be evaluated without the neighboring points being available yet, because they are in a different chunk that doesn't exist at this point in time.

![](../../assets/96dd426c155ed2dc.png)


![](../../assets/96dd426c155ed2dc.png)

The weakness of the functional approach is that certain things can just not be calculated meaningfully without context. For example, consider a river that flows from a source and downwards wherever the terrain goes down the steepest. Given a mathematical function that defines a terrain, it's not generally possible to determine where the river would flow without considering the terrain at many different points at once. Similarly, it's not possible to calculate how light and shadow propagates in a space without having the context of the surrounding geometry available.

There are ways to get around these limitations by mixing functional techniques with simulation techniques. Once a pass of functional calculations have run, a different pass of simulation can run on top, which has does context information. For game worlds that are not generated all at once - and that includes all pseudo-infinite worlds - this has to be handled very carefully to work correctly.

One example is calculation of lighting in Minecraft. The terrain is calculated fully functionally (with user-created modifications on top). After that, the lighting is simulated with proper context information about the terrain. However, the fact that the lighting simulation needs context means that lighting near the edge of a chunk needs terrain data from the neighboring chunk in order to be simulated. How far out can a change in geometry affect the lighting? 2 blocks? 10 blocks? 100 blocks? This, along with the block size of chunks, affects how many neighboring chunks must have been "geometry calculated" before a given chunk can be "lighting simulated".

It just so happens that chunks in Minecraft are 16x16 (vertically they take up the entire world height), while lighting propagates only 15 blocks. This conveniently means that only the 8 neighboring chunks need to be geometry calculated in order for sufficient lighting context to be available for a chunk. This is very likely not to be a coincidence. Having light propagate further than the size of one chunk would have had large negative consequences for the performance.

![](../../assets/62301816f00bdcd1.png)


![](../../assets/62301816f00bdcd1.png)

*(Disclaimer: My explanation of lighting in Minecraft is based on a few facts combined with speculation on my part. I can't guarantee it actually works the way I describe but it's entirely conceivable.)*

Other types of simulation can not as easily be limited to a specific range. One option here is to just ignore the simulation for chunks or parts of the world that haven't been generated yet, and just simulates the best they can with the information generated so far. Maybe a river only begins flowing once the player gets close enough to its source that the chunk containing the source is generated, and that's okay. But for other games where any rivers present should appear to have always been there and not just suddenly begin flowing based on player location, it can be a tricky or impossible problem to solve.

### Topology and traversability

Consider for a moment a game with a player character that can not dig holes or build structures (except maybe at very specific spots). It could be Zelda, Grand Theft Auto, Mario, Half-Life, Metroid or really most other games. What would it mean if there was a hole too deep to jump out of? A gap too wide to jump over? Or a tall wall with a vital objective on the other side but no way to get past it? Basically you would be stuck. It would be game breaking.

![](../../assets/a95a142de86cc937.png)


![](../../assets/a95a142de86cc937.png)

Games like Minecraft would have tons of these stuck situations if it wasn't for the ability to dig and build. But in the majority of games - games where the player can generally not modify the environment much - the level design needs to guarantee that you won't get physically stuck with no means to progress.

These games need to guarantee that the topology is such that it can be traversed by the player, so that all locations can be reached that needs to be reached.

Here's the kicker: Neither the simulation nor the functional approach can make such guarantees. (Well except in boring cases; for example if the world is so flat and without obstructions that the player can go in any direction at any time.)

Let's say we uneven terrain with caves. The simulation and functional approaches can easily be used to create interesting terrain of this type, but very little can be guaranteed about it. Maybe it creates some cliffs, but you don't know if you can get to the top, or if it's too steep all the way around. Or maybe it creates a cave underground, but you don't actually know if it's connected to the surface or not.

![](../../assets/8627b263ed218eb9.png)


![](../../assets/8627b263ed218eb9.png)

For the functional approach, this is because it evaluates every point without context - and topology cannot be determined without context. Again, the exception is terrain where it's trivial to get to any point, but that's not useful for directed, non-sandbox gameplay. The point is that it's virtually impossible to create a mathematical function that creates interesting level/world design where it's non-trivial to reach a given goal location, yet still guaranteed to be possible. Maybe it's doable - and if so that would be highly interesting - but I've yet to have seen it pulled off in practice.

For the simulation approach, the context is usually available, but simulation is not concerned with making guarantees about topology or traversability, just like there are no such guarantees in nature. If a simulation algorithm did make such guarantees, it would really at least partially be a planning algorithm instead.

The planning approach then is the one that can make these guarantees. In fact, much of the planning in planning algorithms is typically centered around ensuring such guarantees.

If you have read articles describing procedural generation for rogue-like games, they typically describe how multiple rooms are placed on the map, and an algorithm ensures that they are all connected with passages. Maybe certain rooms are guaranteed to only be reachable via one passage. More advanced ones may have keys for locked doors, and need to ensure that a key for a locked door is not placed behind the locked door, and similar.

![](../../assets/1f9915c69ac8e63e.png)


![](../../assets/1f9915c69ac8e63e.png)

Most games with planning algorithms take place in sequences of maps with limited size, which each are generated all at once. It's trickier, though absolutely possible, to use the planning approach on pseudo-infinite worlds generated on the fly in chunks. It typically requires planning at several scopes, with a large-scale planning algorithm handling the overall design of the world. This algorithm can then delegate responsibility of the more fine grained planning to algorithms creating the individual chunks. Often, each chunk is given certain criteria it must meet in order to fit into the overall plan. There can be an arbitrary number of such layers of responsibility.

I'm not aware of any shipped games that are pseudo-infinite and use the planning approach - let me know if you do! My own game in development, [The Cluster](http://blog.runevision.com/search/label/TheCluster), uses this approach, and I write about various aspects of the generation and design on [my blog](http://blog.runevision.com/).

### Generation approaches and effects on gameplay

We have discussed how the simulation and functional generation approaches cannot make guarantees about topology and traversability. What this means is that they are essentially mostly suited for games with sandbox gameplay, for example where the player can dig and/or builds anywhere in order to make non-traversable environments traversable. Often these games also don't have any specific locations that must be reached, with the goals being loosely defined or completely absent.

More traditional "directed" games have carefully constructed level design that can be traversed without freely modifying the environment. For these games certain guarantees must be made. For this to be done procedurally, a planning approach must be used.

We have also discussed the implications for pseudo-infinite games that are generated in chunks on the fly. For these games the functional approach has very advantageous properties in that it doesn't require context. The simulation approach can be used only to a very limited extent, while the planning approach can be used fine, but needs very careful division of responsibility between different generation algorithms at different layers of scope or abstraction.

### Mixing and matching

While a procedural game typically has one approach that dominates its generation strategy, there's no problem in mixing and matching the different approaches. For example, a game might use a planning approach for the overall level design, use a bit of simulation to enhance aesthetic properties of the terrain that doesn't affect traversability, and then use a functional approach to place vegetation.

![](../../assets/6df06008ba744ef5.png)


![](../../assets/6df06008ba744ef5.png)

The dominating approach could be said to be the one that affects gameplay the most, and specifically determines how the player can move around in the world and achieve objectives. For anything that doesn't affect gameplay directly, or only in aesthetic ways, the choice of approach is more of an open question.

I hope this article has been helpful in giving insight into various approaches to use for procedural world generation, either for analyzing other games or for use in designing your own. If you have great examples of games using the various approaches to good effect, let me know!


If you're creating anything procedural, you're almost guaranteed to come in need of random numbers at one point. And if you want to be able to produce the same result more than once, you'll need the random numbers to be repeatable.

In this article we'll use level/world generation in games as example use cases, but the lessons are applicable to many other things, such as procedural textures, models, music, etc. They are however not meant for applications with very strict requirements, such as cryptography.

Why would you want to repeat the same result more than once?

**Ability to revisit the same level/world.**For example a certain level/world can be created from a specific*seed*. If the same seed is used again, you will get the same level/world again. You can for example[do this in Minecraft](http://www.minecraftseeds.info/).**Persistent world that's generated on the fly.**If you have a world that's generated on the fly as the player moves around in it, you may want locations to remain the same the first and subsequent times the player visit those locations (like in Minecraft, the upcoming game No Man's Sky, and others), rather than being different each time as if driven by dream logic.**Same world for everyone.**Maybe you want your game world to be the same for everyone who play it, exactly as if it wasn't procedurally generated.[This is for example the case](http://www.vg247.com/2014/12/04/the-goal-of-no-mans-sky-is-to-reach-the-centre-of-the-galaxy/)in No Man's Sky. This is essentially the same as the ability to revisit the same level/world mentioned above, except that the same seed is always used.

We've mentioned the word *seed* a few times. A seed can be a number, text string, or other data that's used as input in order to get a random output. The defining trait for a seed is that the same seed will always produce the same output, but even the slightest change in the seed can produce a completely different output.

In this article we'll look into two different ways to produce random numbers - random number generators and random hash functions - and reasons for using one or the other. The things I know about this are hard earned and don't seem to be readily available elsewhere, so I thought it would be in order to write it down and share it.

### Random number generators

The most common way to produce random numbers is using a random number generator (or RNG for short). Many programming languages have RNG classes or methods included, and they have the word "random" in their name, so it's the obvious go-to approach to get started with random numbers.

A random number generator produces a sequence of random numbers based on an initial seed. In object-oriented languages, a random number generator is typically an object that is initialized with a seed. A method on that object can then be repeatedly called to produce random numbers.

![](../../assets/968af841bdc499f3.png)


![](../../assets/968af841bdc499f3.png)

The code in C# could look like this:

```
Random randomSequence = new Random(12345);
int randomNumber1 = randomSequence.Next();
int randomNumber2 = randomSequence.Next();
int randomNumber3 = randomSequence.Next();
```


In this case we're getting random integer values between 0 and the maximum possible integer value (2147483647), but it's trivial to convert this to a random integer in a specific range, or a random floating point number between 0 and 1 or similar. Often methods are provided that do this out of the box.

Here's an image with the first 65536 numbers generated by the Random class in C# from the seed 0. Each random number is represented as a pixel with a brightness between 0 (black) and 1 (white).

![](../../assets/3333931fe6db28dd.png)


![](../../assets/3333931fe6db28dd.png)

It's important to understand here that you cannot get the third random number without first getting the first and second one. This is not just an oversight in the implementation. In its very nature, an RNG generates each random number using the previous random number as part of the calculation. Hence we talk about a random *sequence*.

![](../../assets/d0aadf2abbdba8f8.png)


![](../../assets/d0aadf2abbdba8f8.png)

This means that RNGs are great if you need a bunch of random numbers one after the other, but if you need to be able to get a specific random number (say, the 26th random number from the sequence), then you're out of luck. Well, you could call Next() 26 times and use the last number but this is a very bad idea.

#### Why would I want a specific random number from the sequence?

If you generate everything at once, you probably don't need specific random numbers from a sequence, or at least I can't think of a reason. However, if you generate things bit by bit on the fly, then you do.

For example, say you have three sections in your world: A, B, and C. The player starts in section A, so section A is generated using 100 random numbers. Then the player proceeds to section B which is generated using 100 different numbers. The generated section A is destroyed at the same time to free up memory. The player proceeds to section C which is 100 yet different numbers and section B is destroyed.

However, if the player now go back to section B again, it should be generated with the same 100 random numbers as it was the first time in order for the section to look the same.

#### Can't I just use random number generators with different seed values?

No! This is a very common misconception about RNGs. The fact is that while the different numbers in the same sequence are random in relation to each other, the same indexed numbers from different sequences are not random in relation to each other, even if it may look like it at first glance.

![](../../assets/1a209f08196d497c.png)


![](../../assets/1a209f08196d497c.png)

So if you have 100 sequences and take the first number from each, those numbers will not be random in relation to each other. And it won't be any better if you take the 10th, 100th, 1000th number from each sequence.

At this point some people will be skeptical, and that's fine. You can also look at this [Stack Overflow question about RNG for procedural content](http://stackoverflow.com/questions/167735/fast-pseudo-random-number-generator-for-procedural-content) if that's more trustworthy. But for something a bit more fun and informative, let's do some experiments and look at the results.

Let's look at the numbers generated from the same sequence for reference and compare with numbers created by getting the first number in of each of 65536 sequences created from the seeds 0 to 65535.

![](../../assets/da6fa0265df00c02.png)


![](../../assets/da6fa0265df00c02.png)

Though the pattern is rather uniformly distributed, it isn't quite random. In fact, I've shown the output of a purely linear function for comparison, and it's apparent that using numbers from subsequent seeds is barely any better than just using a linear function.

Still, is it almost random though? Is it *good enough*?

At this point it can be a good idea to introduce better ways to measure randomness since the naked eye is not very reliable. Why not? Isn't it enough that the output *looks* random enough?

Well yes, in the end our goal is simply that things look sufficiently random. But the random number output can look very different depending on how it's used. Your generation algorithms may transform the random values in all kinds of ways that will reveal clear patterns that are hidden when just inspecting the values listed in a simple sequence.

An alternative way to inspect the random output is to create 2D coordinates from pairs of the random numbers and plot those coordinates into an image. The more coordinates land on the same pixel, the brighter that pixel gets.

Let's take a look at such a coordinate plot for both a random numbers in the same sequence and for random numbers created from individual sequences with different seeds. Oh and let's throw in the linear function too.

![](../../assets/3dccd0a618d5bea2.png)


![](../../assets/3dccd0a618d5bea2.png)

Perhaps surprisingly, when creating coordinates from random numbers from different seeds, the coordinates are all plotted into thin lines rather than being anything near uniformly distributed. This is again just like for a linear function.

Imagine you created coordinates from random numbers in order to plant trees on a terrain. Now all your trees would be planted in a straight line with the remaining terrain being empty!

We can conclude that random number generators are only useful if you don't need to access the numbers in a specific order. If you do, then you might want to look into random hash functions.

### Random hash functions

In general a hash function is any function that can be used to map data of arbitrary size to data of fixed size, with slight differences in input data producing very big differences in output data.

For procedural generation, typical use cases are to provide one or more integer numbers as input and get a random number as output. For example, for large worlds where only parts are generated at a time, a typical need is to get a random number associated with an input vector (such as a location in the world), and this random number should always be the same given the same input. Unlike random number generators (RNGs) there is no *sequence* - you can get the random numbers in any order you like.

![](../../assets/4b873a234db940fc.png)


![](../../assets/4b873a234db940fc.png)

The code in C# could look like this - note that you can get the numbers in any order you like:

```
RandomHash randomHashObject = new RandomHash(12345);
int randomNumber2 = randomHashObject.GetHash(2);
int randomNumber3 = randomHashObject.GetHash(3);
int randomNumber1 = randomHashObject.GetHash(1);
```


The hash function may also take multiple inputs, which mean you can get a random number for a given 2D or 3D coordinate:

```
RandomHash randomHashObject = new RandomHash(12345);
randomNumberGrid[20, 40] = randomHashObject.GetHash(20, 40);
randomNumberGrid[21, 40] = randomHashObject.GetHash(21, 40);
randomNumberGrid[20, 41] = randomHashObject.GetHash(20, 41);
randomNumberGrid[21, 41] = randomHashObject.GetHash(21, 41);
```


Procedural generation is not the typical use of hash functions, and not all hash functions are well suited for procedural generation, as they may either not have sufficiently random distribution, or be unnecessarily expensive.

One use of hash functions is as part of the implementation of data structures such as dictionaries. These are often fast but not random at all, since they are not meant for randomness but just for making algorithms perform efficiently.

Another use of hash function is for cryptography. These are often very random, but are also slow, since the requirements for cryptographically strong hash functions is much higher than for values that just looks random.

Our goal for procedural generation purposes is a random hash function that looks random but is also efficient, meaning that it's not slower than it needs to be. Chances are there's not a suitable one built into your programming language of choice, and that you'll need to find one to include in your project.

I've tested a few different hash functions based on recommendations and information from various corners of the Internet. I've selected three of those for comparison here.

**PcgHash**: I got this hash function from Adam Smith in a[discussion on Google Groups](https://groups.google.com/d/msg/proceduralcontent/AuvxuA1xqmE/T8t88r2rfUcJ)forum on Procedural Content Generation. Adam proposed that with a little skill, it's not too hard to create your own random hash function and offered his PcgHash code snippet as an example.**MD5**: This may be one of the most well-known hash functions. It's also of cryptographic strength and more expensive than it needs to be for our purposes. On top of that, we typically just need a 32-bit int as return value, while MD5 returns a much larger hash value, most of which we'd just be throwing away. Nevertheless it's worth including for comparison.**xxHash**: This is a high-performing modern non-cryptographic hash function that has both very nice random properties and great performance.

Apart from generating the noise sequence images and coordinate plots, I've also tested with a randomness testing suite called [ENT - A Pseudorandom Number Sequence Test Program](http://www.fourmilab.ch/random/). I've included select ENT stats in the images as well as a stat I devised myself with I call the Diagonals Deviation. The latter looks at sums of diagonal lines of pixels from the coordinate plot and measures the standard deviation of these sums.

Here's the results from the three hash functions:

![](../../assets/13e2f1b0af31b75f.png)


![](../../assets/13e2f1b0af31b75f.png)

PcgHash stands out in that while it appears very random in the noise images of sequential random values, the coordinate plot reveals clear patterns, which means it doesn't hold up well to simple transformations. I conclude from this that rolling your own random hash function is hard and should probably be left to the experts.

MD5 and xxHash seem to have very comparable random properties, and out of those, xxHash is around 50 times faster.

xxHash also has the advantage that although it's not an RNG, it still has the concept of a seed, which is not the case for all hash functions. Being able to specify a seed has clear advantages for procedural generation, since you can use different seeds for different random properties of entities, grid cells, or similar, and then just use the entity index / cell coordinate as input for the hash function as-is. Crucially, with xxHash, the numbers from differently seeded sequences are random in relation to each other (see Appendix 2 for more details).

#### Hash implementations optimized for procedural generation

In my investigations of hash functions it has become clear that while it's good to choose a hash function that's high-performing in general-purpose hash benchmarks, it's crucial for performance to optimize it to procedural generation needs rather than just using the hash function as-is.

There are two important optimizations:

**Avoid conversions between integers and bytes.**Most general-purpose hash functions take a byte array as input and return an integer or some bytes as the hash value. However, some of the high-performing ones convert the input bytes to integers since they operate on integers internally. Since it's most common for procedural generation to get a hash based on integer input values, the conversion to bytes is completely pointless. Refactoring the reliance on bytes away can triple the performance while leaving the output 100% identical.**Implement no-loop methods that take just one or a few inputs.**Most general-purpose hash functions take input data of variable length in the form of an array. This is useful for procedural generation too, but the most common uses are probably to get a hash based on just 1, 2 or 3 input integers. Creating optimized methods that take a fixed number of integers rather than an array can eliminate the need for a loop in the hash function, and this can dramatically improve the performance (by around 4x-5x in my tests). I'm not an expert on low level optimization, but the dramatic difference could be caused by either implicit branching in the for loop or by the need to allocate an array.

My current recommendation for a hash function is to use an implementation of xxHash that's optimized for procedural generation. See Appendix C for details on why.

You can get [my implementations of xxHash and other hash functions on sourcehut](https://hg.sr.ht/~runevision/random-numbers-testing/browse/Assets/Implementations/HashFunctions). They are written in C# but shouldn't be too hard to port to other languages.

Besides the optimizations I also added extra methods to get the output as an integer number in a specified range or as a floating point number in a specified range, which are typical needs in procedural generation.

Note: At the time of writing I only added a single integer input optimization to xxHash and MurmurHash3. I'll add optimized overloads for two and three integer inputs too when I get time.

### Combining hash functions and RNGs

Random hash functions and random number generators can also be combined. A sensible approach is to use random number generators with different seeds, but where the seeds have been passed through a random hash function rather than being used directly.

Imagine you have a large maze world, possibly nearly infinite. The world has a large scale grid where each grid cell is a maze. As the player moves around in the world, mazes are generated in the grid cells surrounding the player.

In this case you'll want each maze to always be generated the same way every time it's visited, so the random numbers needed for that need to be able to be produced independently from previously generated numbers.

However, mazes are always generated one whole maze at a time, so there's no need to have control over the order of the individual random numbers used for one maze.

The ideal approach here is to use a random hash function to create a seed for a maze based on the coordinate of the grid cell of the maze, and then use this seed for a random number generator sequence of random numbers.

![](../../assets/3b397acf523e75e3.png)


![](../../assets/3b397acf523e75e3.png)

The C# code could look like this:

```
RandomHash randomHashObject = new RandomHash(12345);
int mazeSeed = randomHashObject.GetHash(cellCoord.x, cellCoord.y);
Random randomSequence = new Random(mazeSeed);
int randomNumber1 = randomSequence.Next();
int randomNumber2 = randomSequence.Next();
int randomNumber3 = randomSequence.Next();
```


### Conclusions

If you need control over the order of querying random numbers, use a suitable random hash function (such as xxHash) in an implementation that's optimized for procedural generation.

If you just need to get a bunch of random numbers and the order doesn't matter, the simplest way is to use a random number generator such as the System.Random class in C#. In order for all the numbers to be random in relation to each other, either only a single sequence (initialized with one seed) should be used, or if multiple seeds are used they should be passed through a random hash function (such as xxHash) first.

The source code for the random numbers testing framework referred to in this article, as well as a variety of RNGs and hash functions, is [available on sourcehut](https://hg.sr.ht/~runevision/random-numbers-testing/).

### Appendix A: A note on continuous noise

For certain things you'll want to be able to query noise values that are continuous, meaning that input values near each other produce output values that are also near each other. Typical uses are for terrains or textures.

These requirements are completely different from the ones discussed in this article. For continuous noise, look into Perlin Noise - or better -

Simplex Noise.

However, be aware that these are *only* suitable for continuous noise. Querying continuous noise functions just to get random numbers unrelated to other random numbers will produce poor results since it's not what these algorithms are optimized for. For example, I've found that querying a Simplex Noise function at integer positions will return 0 for every third input!

Additionally, continuous noise functions usually use floating point numbers in their calculations, which have worse stability and precision the further you get from the origin.

### Appendix B: More test results for seed and input values

I've heard various misconceptions over the years and I'll try to address a few more of them here.

#### Isn't it best to use a large number for the seed?

No, I haven't seen anything that indicates that. If you look at the test images throughout this article, there's no difference between the results for low or high seed values.

#### Don't random number generators take a few numbers to "get going"?

No. Again, if you look at the test images, you can see that the sequences of random values follow the same pattern from start (upper left corner and proceeding one line after the other) to end.

In the image below I've tested the 0th number in 65535 sequences as well as the 100th number in those same sequences. As can be seen, there's no apparent significant difference in the (lack of) quality of the randomness.

![](../../assets/60c70de5df5e86b9.png)


![](../../assets/60c70de5df5e86b9.png)

#### Doesn't some RNGs, such as Java's, have better randomness between numbers from differently seeded sequences?

Maybe a tiny bit better, but not nearly enough. Unlike the Random class in C#, the Random class in Java doesn't use the provided seed as-is, but shuffles the bits a bit before storing the seed.

The resulting numbers from different sequences may be a tiny bit more random looking, and we can see from the test stats that the Serial Correlation is much better. However, it's clear in the coordinates plot that the numbers still collapse to a single line when used for coordinates.

![](../../assets/b33f52b8b5b8011e.png)


![](../../assets/b33f52b8b5b8011e.png)

That said, there's no reason why a RNG couldn't apply a high-quality random hash function to the seed before using it. In fact it seems like a very good idea to do so, with no downsides I can think of. It's just that popular RNG implementations that I'm aware of don't do that, so you'll have to do it yourself as described previously.

#### How come it's fine to use different seeds for random hash functions when it isn't for RNGs?

There's no intrinsic reason, but hash functions such as xxHash and MurmurHash3 treat the seed value similar to the inputs, meaning that it essentially applies a high quality random hash function to the seed, so to speak. Because it's implemented that way, it's safe to use the Nth number from differently seeded random hash objects.

![](../../assets/03360c0fbe3f6ad6.png)


![](../../assets/03360c0fbe3f6ad6.png)

### Appendix C: Comparison of more hash functions

In the original version of this article I compared PcgHash, MD5, and MurmurHash3 and recommended using MurmurHash3.

MurmurHash3 has excellent randomness properties and very decent speed. The author implemented it in parallel with a framework for testing hash functions called [SMHasher](http://code.google.com/p/smhasher/) which has become a widely used framework for that purpose.

I also looked at this [Stack Overflow question about good hash functions for uniqueness and speed](http://programmers.stackexchange.com/questions/49550/which-hashing-algorithm-is-best-for-uniqueness-and-speed) which compares a lot more hash functions and seems to paint an equally favorable picture of MurmurHash.

After publishing the article I got recommendations from Aras Pranckevičius to look into xxHash and from Nathan Reed to look into Wang Hash which [he's written about here](http://www.reedbeta.com/blog/2013/01/12/quick-and-easy-gpu-random-numbers-in-d3d11/).

xxHash is a hash function which apparently beats MurmurHash on its own turf by scoring as high on quality in the SMHasher testing framework while having significantly better performance. Read more about [xxHash on its Google Code page](https://code.google.com/p/xxhash/).

In my initial implementation of it, after I had removed byte conversions, it was slighter faster than MurmurHash3, though not nearly as much faster as shown in the SMHasher results.

I also implemented WangHash. The quality proved to be insufficient since it showed clear patterns in the coordinate plot, but it was over five times faster than xxHash. I tried implementing a "WangDoubleHash" where its result is fed to itself, and that had fine quality in my tests while still being over three times faster than xxHash.

![](../../assets/23b7b04dedb15559.png)


![](../../assets/23b7b04dedb15559.png)

However, since WangHash (and WangDoubleHash) takes only a single integer as input, it struck me that I should implement single input versions of xxHash and MurmurHash3 as well to see if that might improve performance. And it turned out to improve performance dramatically (around 4-5 times faster). So much in fact that xxHash was now faster than WangDoubleHash.

![](../../assets/6cf1de0ab67bdcb5.png)


![](../../assets/6cf1de0ab67bdcb5.png)

As for quality, my [own test framework](https://hg.sr.ht/~runevision/random-numbers-testing/) reveals fairly obvious flaws, but is not nearly as sophisticated as the [SMHasher](http://code.google.com/p/smhasher/) test framework, so a hash function that scores high there can be assumed to be a better seal of quality for randomness properties than just looking fine in my own tests. In general I would say that passing the tests in my test framework may be sufficient for procedural generation purposes, but since xxHash (in its optimized version) is the fastest hash function passing my own tests anyway, it's a no-brainer to just use that.

You can get [my implementations of xxHash and other hash functions on sourcehut](https://hg.sr.ht/~runevision/random-numbers-testing/browse/Assets/Implementations/HashFunctions). They are written in C# but shouldn't be too hard to port to other languages.