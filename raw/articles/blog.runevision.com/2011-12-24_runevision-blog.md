---
title: runevision blog
url: https://blog.runevision.com/2011/
published: '2011-12-24'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

What do you know, it looks like I got 4th place in the AI Challenge!

I began writing an explanation of my bot and you can read [Part I here](http://blog.runevision.com/2011/12/ai-challenge-my-bot-explained-part-i.html) as well as downloading the source code. Right now is holiday time with the family; I'll write up the remainder afterwards. :)


So my ant colony bot is doing rather well in the final AI Challenge tournament. It's ranked around [between 4 and 11](http://aichallenge.org/profile.php?user=9661) depending on when you look.

Reading about some of the strategies used by other bots, I'm surprised mine has performed so well, since it's not really that sophisticated. Well, I'm releasing the source code here. This is in the same state as when I submitted it without further cleanup, so not the most tidy code but not a complete mess either.

Note that the bot behaves completely different depending on whether it's compiled as a DEBUG or a RELEASE build. As a debug build it will look for a file called parameters.txt describing parameters to use for various constants in the code and when executed multiple times it will run with those parameters having different values and keep track of statistics of which parameter values work best. More about that later. As a release build the constants are hard-coded in the code and that's what is used in the actual competition.

The bot have these primary functions:

- Combat logic to evaluate each of 5 possible moves (4 directions plus staying) for each ant. Afterwards each ant has a score for each move.
- Path-finding done using "flood-filling" / breadth-first search from the goal locations. Afterwards each ant has an assigned goal and know which direction to move in to get there.
- Goal handling. This basically adds extra points to one or more of the 5 move scores based on the direction obtained from the path-finding.
- Moves resolution. This resolves which ant has the right to move into which position based roughly on "who needs it the most".

### Path-Finding

The first thing I implemented was path-finding. This was originally done using a [flood-fill / breadth-first search](http://en.wikipedia.org/wiki/Flood_fill) from the goal locations. The default path-finding algorithm choice for computer games is A* but it's not useful for being reused by many agents which is why I used the flood-fill instead. It might also be the same or similar to what is called [collaborative diffusion](http://scalablegamedesign.cs.colorado.edu/wiki/Collaborative_Diffusion) - not entirely sure about that; I only heard about that term after I had implemented my solution.

Initially I simply used a queue for the search. I later switched to a [priority queue](http://en.wikipedia.org/wiki/Priority_queue) so I could us various cost functions for the path-finding. For example, by giving positions occupied by my own ants a higher cost, ant behind them will prefer to go around them instead of just being stuck.

I also implemented support for specifying for a goal the maximum number of ants assigned to it, the maximum distance to search out from the goal, and an initial cost (which gives the goal lower overall priority).

The goals I ended up using are:

- Defense positions around my own hills (1 ant each, no cost, max dist 30)
- Enemy hills (a third of all my ants divided by number of known enemy hills, no cost, no max dist)
- Food (1 ant each, cost equal to 4 dist, no max dist)
- Explore (1 ant for each explore position, cost equal to 25 dist, no max dist)
- Enemy ants (20 ants each, cost equal to 42 dist, max dist 13)

The defense positions are positions immediately around my own hills. 12% of my ants are assigned to defense, divided between my hills if more than one.

Any unassigned ants are assigned to enemy hills as well.

*This post is ending up much longer than I thought so I'm splitting it up. Read on in part II about goal handling and moves resolution.*


The final tournament has begun. Here's some interesting battles [my bot](http://aichallenge.org/profile.php?user=9661) has been in that I've captured on video.

My 5th game where my bot annihilates 8 opponents in an epic battle!

My 6th game where my opponent just won't die (or my massive army is not quite aggressive enough). Also: Dancing!


For the past - hmm, almost 2 months now - I've taken a break from my other hobbies and let myself become distracted by Google's [AI Challenge](http://aichallenge.org) - an Artificial Intelligence (AI) programming contest.

Not for much longer though since the final submission deadline is in 10 hours at the time of writing.

When I [wrote about it a months ago](http://blog.runevision.com/2011/11/ant-colony-google-ai-challenge.html) I'd only been at it for a few weeks but [my bot](http://aichallenge.org/profile.php?user=9661) was already ranked 39th in the world out of 10000+.

Since then I've made a lot of improvements - but so have the other contestants, so the overall level has continuously risen.

Whenever a new version of a bot is uploaded to the content servers, the skill and rank is completely reset, so the bot will have to fight its way all the way back up from the bottom. That can take a few days to a week depending on how high a ranking it can get before it's stabilized.

I last uploaded a bot four days ago. It has gotten up to rank 22 in the world; my highest ranking yet. It's also the top ranked bot in Denmark by a large margin and the 3rd ranked bot written in C#.

When working on improving the bot, it's usually hard to know if some new idea will actually improve the bot or just make it worse without having tested it first. I usually test by running a game with the new version against the old version. However, most changes only make a small difference that will only slightly increase the bot's chances of winning, so it has to be in many games before it's clear if it's better or not. Did it win 4 out of 6 games? Might just be a coincidence due to random luck.

You can see it quickly becomes tiresome to test these things manually. That's why I programmed a simple framework to automatically run many games in a row between the various version of the bot and gather statistics on which versions win the most times. I've often let this run overnight so I have statistics from hundreds of games the next day.

Sometimes, however - sometimes an idea turns out to be a significant improvement. By significant I mean that the new version consistently beat the previous version - as in 10 out of 10 times. Those times when I've managed to make such an improvement have been the most satisfying moments of this competition.

The most interesting improvements have all been related to how the ants handle combat. The way [battle resolution](http://aichallenge.org/specification.php#Battle-Resolution) works in the game follows simple rules but has complex consequences and my understanding of it has increased in stages.

The combat is basically about ants being in majority winning over ants that are in minority. If one red ant is within combat range of one white ant, they both die. But if one red ant is within combat range of two white ants, only the red ant die and both of the white ants survive.

Initially I thought combat was a matter of being cautious. Only move into combat range if you have more ants you can move within range than the opponent has. But it's not that simple. There's various potential outcomes to consider and also an element of gamble. I might write some more about it after the competition has ended if not somebody higher ranking does it first. Not that I'm an expert by any count - I feel like I've only scratched the surface.

Anyway, since I uploaded that last bot four days ago I've made several significant improvements in the combat skillz of my bot, meaning that the newest version I have here totally and consistently kicks the ass of that version I uploaded four days ago. Now I've just uploaded this new version. It will probably be the last unless I get some last-minute epiphany which is not likely by now.

We'll see how it performs in the final tournament.


For the past few weeks I've taken a break from my other hobbies and let myself become distracted by Google's [AI Challenge](http://aichallenge.org).

It's an Artificial Intelligence (AI) programming contest about programming the smartest virtual colony of ants which fight against other colonies for domination.

The matches are played entirely by the submitted programs on online servers and replays of them can be seen online at the website. My matches can be followed [here](http://aichallenge.org/profile.php?user=9661), such as [this one](http://aichallenge.org/visualizer.php?game=117871&user=9661).

As mentioned, I've been at it for a few weeks, and my colony is now the 39th highest ranked world-wide out of several thousands, and the highest ranked in Denmark out of 138. :)

It's quite good fun, so I'll try to make a few more improvements, although I'm beginning to run out of ideas. It's tough competition for sure!

If you know a bit of programming, it's easy to [get started](http://aichallenge.org/quickstart.php), and starter packages are provided for all kinds of different programming languages including Java, C#, Python, C++ and more.

Let me know if you're participating as well!


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


*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

In the last post I wrote about how I've [improved the edges](http://blog.runevision.com/2011/05/eas-sweet-sweet-edges.html) in the environment generation of The Cluster. But the background scenery was basically just parts of the foreground extended far into the distance which was not terribly interesting to look at.

Since then I've implemented generation of more interesting backgrounds with hills and cliffs and forests. The background scenery can be seen in the first half of the video here.

The video shows a green hilly environment and an underground dungeon style environment. There's no enemies in this demo and many objects are still placeholders - the focus is on the terrain itself.

The background is somewhat faint (due to [aerial perspective](http://en.wikipedia.org/wiki/Aerial_perspective)) and blurry and isn't meant to steal the attention away from what's happening in the foreground, but having interesting detail in it can nevertheless add a lot to the overall feel.

Another thing to note in the video is the dynamic camera framing. It zooms the view in and out and places the player nearer the top or bottom of the screen as necessary based on the surroundings. It's something I may go into more detail with in a future post.


I just upgraded from Firefox 3 to 5 and find that my blog is shown without a stylesheet at all. It still works fine in Firefox 3, and latest Chrome and Safari and I assume other browsers too. And the rest of my site still works fine in Firefox 5 too; it's only the blog part that's broken.

**Update:** It appears it was the stylesheet that was not recognized. I had my stylesheet inside an .asp file to be able to execute server-side code in it. That has always worked just fine but it appears to break when the browser is Firefox 5 AND the site linking to the stylesheet is on Google's Blogger service. When the same stylesheet is linked to from the part of my website that's hosted on my own server, it works fine. The stylesheet is hosted on my own server in both cases, so how it can make any difference where the html page is hosted I do not understand. In either case, baking the stylesheet into a static .css file and linking to that instead seems to have fixed the problem.


*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

Last time I posted an update about The Cluster was - 10 months ago!? Well, development hasn't been idle though - far from it! - it's just that I've been working on some refactoring and changes that ended up being rather time-consuming. Some big hurdles are now over and blog updates should hopefully be more regular going forward.

One of the most recent features I've implemented is handling of smoothing and texturing of edges. This has been on my todo-list since forever but I had to switch to a better way of generating meshes before this became feasible.

Consider a generated environment with surfaces that meet each other in sharp edges:

![](../../assets/21b2e05645caeb78.png)


![](../../assets/21b2e05645caeb78.png)

The surfaces look weightless like they're made out of cardboard. No offense to MineCraft, but it's not the look I'm going for. Let's smooth those edges a bit.

![](../../assets/7f413e010d02c024.png)


![](../../assets/7f413e010d02c024.png)

Better. The environment now has a certain weight to it; it feels more solid. But the abrupt edges between surfaces with different textures still makes it seem artificial and less believable (believable not in the sense of realism as I'm not going for that, but in the sense of suspension of disbelief). Let's cover up those abrupt changes in texture.

![](../../assets/7c37bca03e6572cb.png)


![](../../assets/7c37bca03e6572cb.png)

Ahh! With the edges of the textures covered up with natural-looking transitions, the world has finally come alive and is more inviting than ever.

A few more examples of the current look of The Cluster (don't mind those ugly green box stepping platforms and spikes. They're placeholders I haven't yet replaced with something better):

![](../../assets/6d97cd5323332ce4.png)


![](../../assets/6d97cd5323332ce4.png)

![](../../assets/029065542fa6ce15.png)


![](../../assets/029065542fa6ce15.png)

![](../../assets/5fbb18aeb0499a06.png)


![](../../assets/5fbb18aeb0499a06.png)

Most of the textures are made with good old [POV-Ray](http://povray.org/) by the way; the raytracer [I used to work a lot with](http://runevision.com/3d/) back in the days.

The environment is controlled by a neat system of specifying block types, face types, and edge types. Each "cell" in the world (think big voxel) is of a specific block type, for example "Bricks" or "Empty". The procedural generation algorithm fills in the block types of all cells in a generated area prior to constructing the mesh.

A block types specifies the face types it has. For example, this is the data for the Bricks block type (here called EnvironmentData but I should rename that):

![](../../assets/4f9a6c8bf8a61719.png)

All faces here uses the BrickWall face type, except the Up face which uses the Grass face type. Here's the data for the Grass face type:

![](../../assets/a6dea3255a757c53.png)

The face type specifies the material to use for the face surface, as well as edge data for convex, flat, and concave edges. The edge data is used to specify rounding size for an edge as well as the material, width, and UV data for the textured strip that is generated over the edge.

This is an example of an edge texture (diffuse channel):

![](../../assets/88f374eb7c0f6405.png)

This one is of course extremely wasteful, but the system is already set up so multiple edges can be contained in one material; I just need to change my texture so they actually make use of that.

Currently it's not possible to differentiate the different edges of a face but I'll need to add support for that so different edge data can be used for edges that are "along U" and "along V".

When generating geometry an edge is of course shared between two faces. The priority value of an edge is used to settle which of the two faces get to use their edge data for the edge.

When I had to set up the relationships between block types, face types and edge types, that was the first time the data got too unwieldy for me to hard-code directly in the code. Instead I turned to Unity's ScriptableObject, as I wrote a short post about [here](http://blog.runevision.com/2011/05/unitys-scriptableobject-and-threading.html). Using the ScriptableObject means that Unity's Inspector can be used to specify the data, and Unity's serialization system automatically takes care of everything related to storing and loading the data. At some point I'll probably write some custom editor GUI for the data too so it becomes easier to comprehend and get an overview over.

And that's all I have to say about edges!

![](../../assets/1c18d37be6fc82b8.png)


![](../../assets/1c18d37be6fc82b8.png)


I found a pleasant solution to a problem I had in Unity that I thought I'd share. This post is technical in nature and won't be of interest to people who don't use [Unity](http://unity3d.com/).

In my [procedural game](http://blog.runevision.com/search/label/TheCluster) I'm doing a lot of lengthy calculations and I've been looking into doing them in a separate thread in order to easily spread out the calculations over multiple frames. Using co-routines for this was getting overly convoluted, with yield statements and [StartCoroutine()](http://unity3d.com/support/documentation/ScriptReference/MonoBehaviour.StartCoroutine.html) calls sprinkled all over the code-base.

Threading is supported in Unity using the normal .Net (or more specifically Mono) [APIs for threading](http://msdn.microsoft.com/en-us/library/aa645740%28VS.71%29.aspx). However, the Unity API can't be touched in anything else than the main thread, or errors will occur. Luckily the lengthy calculations are mostly self-contained and are not touching the Unity API.

However, the calculations do use some data structures that are stored in the form of [ScriptableObject](http://unity3d.com/support/documentation/ScriptReference/ScriptableObject.html). Using ScriptableObject is the simplest way to store some data in Unity with automatically handled serialization. Also see [Bas' explanation here](http://bassmit.info/?p=68).

The problem?

- Querying the name of a ScriptableObject can't be done outside of the main thread.
- Doing equality comparisons between ScriptableObjects can't be done outside of the main thread. This includes checking if a ScriptableObject is null.

These are things I can't avoid in my code. So instead I came up with this derived class that I now use for all my ScriptableObject needs:

```
using UnityEngine;
public class ThreadFriendlyScriptableObject : ScriptableObject {
// Hide the name property with a public variable of the same name.
// (Also hide this in the Inspector.)
[HideInInspector]
public new string name;
// Set it to be the same as the property was.
// (OnEnable will be called from the main thread so it's ok here.)
void OnEnable () {
name = base.name;
}
// Override equality operators to avoid calls into
// the Unity API when doing comparisons.
public static bool operator == (
ThreadFriendlyScriptableObject a,
ThreadFriendlyScriptableObject b
) {
return object.ReferenceEquals (a, b);
}
public static bool operator != (
ThreadFriendlyScriptableObject a,
ThreadFriendlyScriptableObject b
) {
return !object.ReferenceEquals (a, b);
}
public override bool Equals (System.Object other) {
return object.ReferenceEquals (this, other);
}
// We get a compile warning if we don't override this one too
public override int GetHashCode () {
return base.GetHashCode ();
}
}
```


Everything works great for me using this class. There's a few limitations of course:

- You won't be able to access or modify the actual name of the ScriptableObject. This is not a problem unless you need the name to change.
- You won't get Unity's nice behavior of making a reference to an Object look like it's null if the Object was destroyed. This is only a problem if you plan on destroying the ScriptableObjects at runtime. Since the main function of ScriptableObjects is to be persistent assets, you're not likely to want or need this.

Use at your own risk. :)