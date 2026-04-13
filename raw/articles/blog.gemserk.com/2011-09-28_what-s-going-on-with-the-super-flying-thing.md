---
title: What's going on with the Super Flying Thing?
url: https://blog.gemserk.com/2011/09/28/whats-going-on-with-the-super-flying-thing/
published: '2011-09-28'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

On the last weeks I was a bit distracted working on [Vampire Runner](https://blog.gemserk.com/games/vampirerunner) and with [Mad Jetpack](https://blog.gemserk.com/2011/09/27/a-game-prototype-mad-jetpack/) so I ended up kinda leaving Super Flying Thing abandoned, I also have some doubts about which features to work on so I preferred to dedicate time on other projects while deciding what to do with the game.

Super Flying Thing is really fun to me, I love the concept but right now the game could be a bit boring and I want to improve that, not so sure how, but I want to try some ideas I have in mind.

### About levels

The main idea of the game is you have to master your flying skills and for that you have to try and fail a lot of times. For that reason, I want to modify the levels to be smaller and harder but not frustrating since you can quickly try again and again.

Random levels are now generated using pre generated tiles (I want to talk about this in a dedicated post), so they are a bit more interesting, however they don’t transmit the idea of try and fail a lot of times yet, so I have to work a bit on level generation.

### About game modes

The practice mode will be removed since you can practice in both challenge and random modes. However, for starters I want to add a Tutorial where you can test the controls and learn how to play to mitigate the change I plan to do over the levels.

Also, we want to try an Endless mode where you have to go as far as you can, playing through different challenges each time harder and harder.

### About content

On some levels there are lasers, moving obstacles and even portals. Despite I love all this stuff, I will probably remove them until I see how they really fit in the game.

Stars will be probably removed as well since they don’t contribute nothing to the game for now. Again, this will be probably temporary until it fits in the game.

### About game objective

On normal game mode, the main objective will remain the same, travel from one planet to the other. However, I want to add a second objective to add challenge factor to the game, something to make the player want to try again the same level several times. One possibility is to add some kind of local competition, for example, improve the time to reach the destination planet, play against your best time, or something like this. Going further with that possibility, maybe publish that replay/best score online and compete with others.

We have to dig further in this subject since it can contribute with re playability factor.

### About controls

Now that we fixed the game behaving different on different devices I will rip off the AxisController and the TiltController and probably one more, and leave only the original one plus maybe some other.

The original control was modified a bit in order to let the player control the ship better based on how new levels are going to be.

### Conclusion

That’s all for now, the idea of this post is to let you know that I want to to continue this game.

Hope you liked it, even if it has nothing interesting.