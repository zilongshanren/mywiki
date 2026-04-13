---
title: A basic analysis of Clash Royale multiplayer solution
url: https://blog.gemserk.com/2016/09/05/analyzing-clash-royale-multiplayer-solution/
published: '2016-09-05'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

The idea of this post is to analyze in a superficial way the multiplayer solution behind [Clash Royale](https://clashroyale.com/). Before starting the analysis, you must know that I don’t have previous experience making multiplayer games, I am just learning, and all the analysis done here is just a theory.

So, you surely know about Clash Royale but in case you don’t, it is an online multiplayer 1v1 RTS game where the first player to destroy the other’s towers win. To do so, they play cards which transforms into units that advance and attack enemy towers, structures that spawn units or attack enemy units or special powers which can be used to perform damage, among other things. Cards cost energy that regenerates over time (to a maximum). I recommend it since it is a great game, and it is really really polished in every detail (including multiplayer).

Here is a video explaining and showing the game:

### Analysis

Since the game is very competitive, they probably have an authoritative server to validate player actions to avoid cheating. For example, a Player could say “I played card X” to the server, the server has to validate the player had that card in hand to use it, and enough energy.

In each game there could be several units at the same time (like 30 units in the worst case), also, there are tons of games being played at the same time. In order to make the game run over mobile networks and to support all those games, with all those units at the same time, they have to reduce the bandwidth to the minimum.

One strategy could be to compress the data sent, other could be to send data not so frequent and to interpolate to be as smooth as possible. However, considering that each unit has a position, looking direction, target, health, animation frame, among other stuff, that could still be a lot of data. I am guessing here that they follow another approach like a synchronized simulation of the game in each client and, since it is not so CPU heavy, every mobile device nowadays (game was released March 2016) shouldn’t have problems running the game logic.

Another thing that made me think about synchronized simulation was that every player action is not performed instantly, it has a small delay or a cast time. That could be a design choice but I believe it considers the fact that actions must be synchronized between players and having a delay allows them to do that.

If they are simulating in the client, they have to control the simulation to be deterministic or they must have some way to fix the game state if it was desynchronized at some point.

If I remember correctly, they follow an approach that the game never stops, players could be disconnected for a while and then reconnect and continue playing, they just lose part of the game (couldn’t perform actions). That could be used also for player desynchronization. Don’t know the resynchronization strategy but maybe the server sends game state snapshot and the player continues from there.

They even have game replays, so I am guessing that simulating the game in each device could help in reducing the cost of watching a replay even though they could replay it in a server if they want since they probably have tons of servers :).

### Conclusion

My guess is that the game has a client/server architecture where both the server and the client simulate the game synchronously. The server is in charge of validating player actions and responsible of deciding the real game state in case of desynchronization.

As I said at the beginning of the blog post, this is a superficial analysis based on my current knowledge. If I wanted to perform a deeper analysis I could have follow another approach like doing some [reverse engineering](http://blog.nfi.io/2016/03/28/clash-royale-protocol-dissection/) over the game connections to validate some of my guesses but that wasn’t the blog post purpose.

And here is a really fun video of the game to finish the post: