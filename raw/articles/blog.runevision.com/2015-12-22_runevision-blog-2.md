---
title: runevision blog
url: https://blog.runevision.com/2015/12/
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