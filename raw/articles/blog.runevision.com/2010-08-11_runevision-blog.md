---
title: runevision blog
url: https://blog.runevision.com/2010/08/
published: '2010-08-11'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

Like [I wrote about a few weeks ago](http://blog.runevision.com/2010/07/eas-agile-enemies-in-platform-game.html) I've been working on pathfinding and AI for the enemies in The Cluster. The AI pathfinding is now reasonably stable and there's a working demo below where you can fight against simple hunting enemies. Right now the enemies always know where the player is; later the knowledge of most enemies will be made less global and more based on local memory.

I've also been working on some new character models and animations. The new animations in particular bring the player avatar and enemies a lot more alive! Even though I'm a complete amateur as an animator, the crude animations I've made still make the character a lot more fun to watch, I think. :)

Here is a simple playable demo of the current state of the game (requires Unity plug-in):

Controls: **Arrows** to run, **Ctrl** to jump, **Alt** to shoot fireballs.

Again, this demo is just a "tech demo" and features no way to win. It extends infinitely to the right. Enemies should be able to chase the player almost everywhere, but they can't pass the checkpoints (the white monuments).

Like I [wrote about before](http://blog.runevision.com/2010/07/eas-agile-enemies-in-platform-game.html), I'm still not sure what gameplay elements would be best at making agile enemies like these the most fun in a platform game. Have a go at the demo above and then let me know if you have some ideas for how to make this gameplay more fun!


*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

I'm taking a break from [pathfinding and AI](http://blog.runevision.com/2010/07/eas-agile-enemies-in-platform-game.html) to go back and talk about the raw level design in The Cluster; More specifically the procedural generation.

The entire world in The Cluster is procedurally generated at runtime, though it is consistent, meaning that the world will be the same every time you play. However, this is strictly a design choice, not a technical limitation, and I'm considering including some kind of bonus areas or similar that will be different every time.

To give you an idea of the current state of the game, here is a simple playable demo (requires Unity plug-in):

Controls: **Arrows** to run, **Ctrl** to jump.

This demo is just a "tech demo" and features no enemies and no way to win. It extends infinitely to the right.

Back in 2007 I [explained the procedural level generation](http://runevision.com/multimedia/cavex/#307) of the game. The game has changed a lot since then - among other things it has turned from a tile based 2D game into a 2.5D game with 3D graphics - but the basic method of generation is still the same.

You can actually see the maze map in-game in the demo above by pressing **2**. Press **1** to hide the world to only see the map. You can zoom a bit out by pressing **Z**, **X** zooms back in, and you can pan around using **WASD**. Press **Esc** to reset the camera.

![](../../assets/2d3f8af1d3cdbecf.png)

A map of the maze that the area is based on.

![](../../assets/a2a90504498e1c58.png)

The map overlayed onto the actual generated area.

![](../../assets/c475f10d5fc9e3d0.png)

The generated area by itself.

One feature not explained in depth on the page linked to above is the placement of locked doors and keys in the game. The game places locked doors and keys in a "perfect way" such that it is always necessary to find all keys and unlock all doors to be able to proceed, and a "deadlock" will never occur, where the key for a door is placed behind that door. The placements are calculated using a simple algorithm I came up with which is based on dividing the area up into a binary tree and then placing keys in leaf nodes and locks in inner nodes in a specific way. Several years after implementing it, I found [this article about "Environment Tree"](http://www.squidi.net/three/entry.php?id=4) at [Squidi.net](http://www.squidi.net/). It's basically the same algorithm, so rather than explaining it myself here, I'll refer to that.

A nice aspect about the algorithm is that it supports placing keys both *sequentially* and *nested*. In the screenshots above, the red door is sequential in the sense that all the following keys and doors are on the far side of the red door, so once you've gone through it, you don't have to go back. The green door, however, is nested. You go through the green door, pick up the blue key, and then go back out the green door in order to proceed. The algorithm doesn't have separate handling of sequential versus nested key and door placements; these are just emergent properties so to speak.

If there's any interest I can cover other aspects of the procedural generation in The Cluster in coming blog posts.


[Maze Raiders](http://runevision.com/multimedia/mazeraiders/) is a two-player game I made together with three other people back in 2004. You need to sit two persons by the same computer to play the game.

![Screenshot: menu screen](../../assets/ea00091ef2b0f7c7.img)


![Screenshot: jungle maze](../../assets/f7b317cfa6f1d590.img)


The objective of the game is to run around in a maze and collect more gold coins than your opponent, and to shoot him and steal his coins. The game sports randomly generated mazes each time you play to keep it fresh. There's two different scenarios - jungle and pyramid. It's classic local two-player fun!

![Screenshot: pyramid maze](../../assets/5418b945d18d8ac7.img)


![Screenshot: status screen](../../assets/430fa1bfe87d4dfa.img)


Though we were all game design novices, we managed to balance the rules to make for a frantic game that just keeps being fun to go back to. When all coins in a maze are collected you have one minute to try to steal coins from your opponent. During this time the player with fewer coins moves faster than the other player. It's just enough that it's not too late to change the tides, and it makes for a panicked final chase before the time runs out, sometimes with the roles switching multiple times.

In 2004 when the game was made there was no indie game movement to speak of so we had nowhere to announce the game - particularly a game of such a small scope. All we could do was submit it to software distribution services like Tucows and FilePlanet. Ha, things sure have changed since then! I thought I'd take this opportunity to put the game online and let others know about it. Enjoy!