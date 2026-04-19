---
title: runevision blog
url: https://blog.runevision.com/2011_08_21_archive.html
published: '2011-08-21'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/9d0eb0bafe71df89.png)

The procedural game I'm working on in my spare time, [The Cluster](http://blog.runevision.com/search/label/The%20Cluster), has a focus on non-linear exploration and is set in a big, continuous world. When I've let people play it in its current state they've been happy to roam around at first, but quickly become bewildered from a lack of sense of direction and purpose because they could go so many places but had little idea of what they're supposed to do other than running around aimlessly. That got me thinking about ways to direct the experience better.

In [Part Six of his series on Proceduralism](http://roguelikedeveloper.blogspot.com/2011/08/proceduralism-part-six-architecture.html), Andrew Doull recently wrote:

Populous, Dwarf Fortress, Minecraft and Terraria all cheat procedural generation in two important ways: they allow you to modify the topology of the space and they encourage you to make interesting content in that space to which you become attached. An uninteresting dead end can be transformed into a useful corridor, or lit by a torch to mark that you've 'already been here' or mined for valuable ore. The procedural generation systems they use may make beautiful places, but it is the player's job to change them into interesting spaces.

This sums up the situation pretty well - and if we ignore the building aspect, other games like Spelunky can be added to the list as well. The choice of wording "cheating" can be discussed, but it's certainly a way to circumvent one of the biggest challenges of procedural generation: To make the environment interesting and challenging while still ensuring that it's never impossible to traverse.

### Non-Modifiable Environments that Direct the Player

In traditional games it's in general not possible to add or remove from the environment (i.e. Mario, Sonic, Zelda, Metroid, you name it; almost all games are like that). If the player could just dig or blow up a hole anywhere he wanted, it would ruin the carefully constructed challenge. So these games ensure traversability not by allowing the player to change the environment, but by ensuring that it's traversable from the beginning. And that's not hard to do in manually designed levels. If it's not possible to traverse a location, the designers will find out when testing it and then just change it.

For games that are procedurally generated at runtime, it's not always possible to test any level or environment prior to release because there may be an infinite number of them. The above mentioned games circumvent this problem by simply not giving any guarantee that the environments are traversable, because the player in those games can always dig or explode a hole almost anywhere to create a passage where there wouldn't otherwise be one.

### Non-Modifiable Environments in Procedural Games

So modifiable environment lifts a big burden from the procedural generation problem in those games. However, some people - like me - still like more traditional games a lot where you have to deal with the given environment rather than just being able to dig a hole through it. Games where the experience is a bit more structured and directed instead of relying entirely on the player creating challenges for himself.

Creating procedural environments that do have a traversability guarantee imposes a lot more restrictions on the generation algorithms, and I find it to be an interesting and worthy challenge. My efforts in that direction can be seen in The Cluster, my 2.5D platform game under development with focus on non-linear exploration. (You can read [all the posts about The Cluster here](http://blog.runevision.com/search/label/TheCluster).)

### Spatial Algorithms that Create Structure

So what kinds of algorithms can be used to create environments that structure the game experience and guides the player?

Before talking algorithms, it's useful to look at what structure and guidance techniques are used in games in general, including non-procedural games.

**Linear progression**is the simplest way to structure and guide the player. Simply move on forward; it's the only way to go!**Keys and locks**is a way to break up linear progression, whether it's literal keys and locks like in Commander Keen and Doom, or other variants like switches that causes a door elsewhere to open, a bridge to extend, or a hazard blocking the way to disappear.- Non-linear games often have features of
**unlocking new regions when some threshold is met**, whether it's experience points in RPGs or number of collected stars in Super Mario 64. - Non-linear games may also grant the player new
**abilities that are required for certain parts of the world**. This effectively is also used for unlocking new regions, but at the same time the ability is also used as a normal part of gameplay within those unlocked regions. This is especially popular in games in the Metroidvania genre.

There's many other techniques, but these are sufficient for this discussion.

For linear games, there's no need for algorithms to structure the experience and guide the player, since the structure and guiding is inherit in the linearity itself. Making the game interesting is still a challenge though, so algorithms are needed for that. This comes down to the moment to moment gameplay, and is very dependent on which type of game it is.

*Importantly, making the moment to moment gameplay interesting is needed in any case, no matter if the game is linear or not.*

Simple key and lock puzzles can easily be implemented procedurally. I wrote a bit about it [here](http://blog.runevision.com/2010/08/eas-demo-of-procedural-environment.html) where there's also a playable demo of it, but it's also [described well on Squidi.net](http://www.squidi.net/three/entry.php?id=4).

![](../../assets/9d0eb0bafe71df89.png)

Unlocking parts of the world, whether it's based on collectibles or on gained abilities, should also be more or less simple to implement. I know others have done it already and I'm currently experimenting with algorithms for it myself.

Now, in [his article](http://roguelikedeveloper.blogspot.com/2011/08/proceduralism-part-six-architecture.html), Andrew Doull also wrote:

My procedural spider senses tingle as soon as I see a procedural generation system that uses one of the following two approaches: 1. Mazes (and by extension BSP-trees) 2. Height maps - because I've yet to play a game where I've exclaimed 'Wow, what a great height map' (...) and the pleasure of solving a maze isn't the same as the pain of having to play through one. I've also seen a rise in recent suggestions and several implementations of Metroid-style procedural generation featuring gated lock-and-key puzzles to partition a map, on the assumption that being forced to traverse through a non-linear space looking for a key is some how interesting. This is putting the cart before the horse: Metroid (and Zelda) use this technique to force the player to explore an already interesting (and hand-designed) location, not because looking for a key is itself challenging.

This is missing the point, I think. *Of course* the locations and the moment to moment gameplay in them needs to be interesting. Just like a linear game with no challenges (say, just walking from left to right) would bore you to death, so would a game with a different guiding structure, such as keys and locks, or progressively unlocked regions. But that doesn't mean that those guiding structures have no merit or importance. Indeed, just like they were important in Metroid and Zelda, so they can be in a non-linear procedurally generated game.

They have more merit too than just to "force the player to explore an already interesting location". They serve at least three additional purposes:

- To prevent player confusion and bewilderment at having too many open possibilities, especially in the beginning. An open world where there's access to everything from the start can give a sense of lack of direction or purpose which can be very off-putting - more so for some people than others. This is why most open and "sand-box" games still have clearly defined "main missions" that can be pursued, and certain options, areas, or missions that are not accessible until further into the game.
- To give the player a sense of reward when a new part of the world is unlocked.
- To keep things fresh and interesting by saving some things in the game for later.

To dismiss an interest in such guiding structures as "putting the cart before the horse" only makes sense if some people think that a game can consist of these guding structures alone with no gameplay beyond that. But I'm not sure who ever claimed something like that.

### Room and Corridors versus Mazes

In his article, Andrew also writes:

The most successful (and perhaps only successful) procedurally generated game spaces so far are all based on Rogue, with its simple room and corridor design. With a room and corridor design we get four important features:


- Corridors - which act as natural choke points at each end, and cover if you are in them
- Convex shapes - spaces where you can see everything in the space from everywhere else
- Concave shapes - spaces where some space is hidden from another (more cover)
- Loops - which allow you a safe haven by traversing the loop to recover when chased by enemies of the same speed or slower

But it's obvious that these success criteria are coupled tightly with Rogue-like gameplay and have little relevance to many other types of games.

In any case, I have a hard time seeing how this [room and corridor design](http://roguelikedeveloper.blogspot.com/2007/11/unangband-dungeon-generation-part-two.html) is superior over a design based initially on a maze. The room and corridor design connects rooms in a web that gives very little control over the progression of the player through the area, as far as I can see, since there's an undefined number of ways to get from one point to another.

In contrast, a design based initially on a perfect maze (a maze with no loops) has only one way to get from any point to any other. This means that obstacles or challenges can be strategically placed at positions that the player cannot avoid - in other words it gives actual control over choke points at a global scale if so desired, whereas the room and corridor design may create local choke points, but won't guarantee the player has to pass through them.

The important point here is that mazes can still provide all those other features as well.

**Rooms?**Just place rooms in the beginning before the maze algorithm has run. Rooms could define locations with potential entrances or required entrances, and the maze algorithms will make sure to connect them up (but without forming any loops). I have that feature in my own maze algorithms and use it to place predefined rooms where artifacts are located.**Loops?**After the maze algorithm has run and after required global choke points like locked doors have been chosen and placed, just carve some additional corridors/tunnels, maybe starting from some of the dead ends left by the maze algorithm. When doing so, prevent connecting parts of the maze that are on opposing sides of a global choke point (like a locked door).**Avoiding dead ends?**Dead ends can easily be made non-pointless by placing rewards there (or keys to locked doors), but they can also just be removed in a pass that runs after the maze algorithm that removes any dead ends that haven't been assigned any purpose. The algorithm can also be made to leave a certain number of dead ends in, or give preference to removing long dead ends or short dead ends, depending on what is wanted.

![](../../assets/92b9a716bd23b51d.png)

The important part here is that using a maze algorithm does not imply that the result will look and feel like a maze. It's just an algorithm to get things done, and the useful part is that at one point during the generation there's exactly one way to get from any point to another, although this doesn't have to be the case when the whole generation is completed.