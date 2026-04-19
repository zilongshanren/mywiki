---
title: runevision blog
url: https://blog.runevision.com/2010/
published: '2010-12-22'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

OMG the 3rd Person Shooter demo I made in the beginning of the year has ended up on popular web games portal [Kongregate](http://www.kongregate.com/). [The game](http://www.kongregate.com/games/joe1017/unity-demo) has had 20,000 plays so far and counting and has a rating of over 4.1 out of 5. I'm totally flattered. :D

**UPDATE:** Kongregate took down the demo after enough other Unity games had been submitted that the demo was not needed to demonstrate Unity anymore.

![](../../assets/84aed0dc7e12d615.img)


I made the demo at work at Unity back in the beginning of 2010 to demonstrate various animation techniques, and I [ended up making it into an actual game](http://blog.runevision.com/2010/02/3rd-person-shooter-unity-demo.html) (albeit a small one). Since then it has been possible to [play it on the Unity website](http://unity3d.com/gallery/live-demos/index.html#3rd-person-shooter). The demo was based on a tech demo that Paulius Liekis and I did for a [presentation about animation techniques](http://unity3d.com/support/resources/unite-presentations/character-animation-tips-amp-tricks) at Unite '09.

So the reason it ended up on Kongregate: Kongregate, which used to host only Flash games, has just announced that [they have opened up for Unity games](http://www.kongregate.com/unity_game_contest) too (and they're having a grand Unity Game Content to kick it off!). They wanted to show their users a simple demonstration of just how great things can be made with Unity, and they picked this Unity demo for that purpose.

So - a little known fact is that I did the voice work for this demo; totally unprofessionally too, but it brings a lot of humor to the game. Reading the [comments](http://www.kongregate.com/games/joe1017/unity-demo/comments?sort=newest) from users on Kongregate, it seems that it's appreciated. :D

A lot of the comments a very positive or out right hilarious. A few examples:

"Takes long to load, but definately worth it. 5/5"

"Wait... This is an actual 3-D game, without lag... And it's not one of those ones with just 3D sprites and whatnot... YES!... YES!... THIS IS DELICIOUS!"

"Cant wait for the sequel Unity demo 2: Better run! and the spin-off game "how do I get behind it?" and don't forget the T.V gameshow "YEAH, Ha Ha, Take THAT!""

"ZOMG!!! love the voice"

"should i pull out my second gun to shoot it with? nooo! why would i do that?"

"lol i love the voice acting :)"

"WOOT! I lost in no fail mode! Robot sploded on my head +)"

"i like the ragdoll physics unity 3d has (this and dead frontier) its fun i killed it on medium ran towards it and BOOM i went flying"

"This. Is. So. Mother. Freaking. Awesome."

"AMAZING Graphics! I Have To Say 5/5 I'm Gonna Devo For This ;)"

"This is actually real?!?! Oh my God the graphics..."

"This game could change the history of kongregate. 3D games Zero lag."

"best graphics on kongregate ever"

"R.I.P. Flash 'Nuff said?"

"BOOOM!sorry that was just my BRAIN exploding from awesome!!!!!!"


I'm famous! Well, except the thing was not posted in my name so nobody will know. Oh well. :P


A new study confirms that procedural animation in a game, such as the [Locomotion System](http://runevision.com/tech/locomotion/) I developed for my Master's Thesis, can improve not only the visual impression of the game, but also increase the overall player engagement significantly.

I was contacted some some ago by Chelsea Hash, a digital media student from the Polytechnic Institute of New York University. She had just finished her own Master's Thesis [Reactive Animation and the Play Experience](http://www.livelydisposition.com/?p=149) which included a social psychology experiment on the affect of dynamic animation systems on the user experience. The semi-procedural animation system used as part of the experiment is based on the Locomotion System I developed. She told me:

The study found that given four versions of a game with the only variation being the avatar visualization and animation system, the semi-procedural animation system consistently had a positive impact on the game experience. Users consistently ranked the procedurally animated version higher and played it for longer. This effect was found to be subtle and often beneath the user's ability to consciously identify the difference.

![](../../assets/f618bd295be91bfd.jpg)

I find this highly interesting! My Master's Thesis and many other technical papers about animation techniques simply take for granted that animation techniques that makes characters more physically situated in the game environment increases player immersion - but this study actually tests this hypothesis, and finds that players become more engaged at a general level as well.

Her Master's Thesis is part of her studies at the Social Game Lab where research is conducted that addresses the subconscious qualities in design that make quality interactions. You can read more about Chelsea's work at her website, [livelydisposition.com](http://www.livelydisposition.com/).

For anyone interested in using this form of dynamic animation in their own games (to enhance player engagement!), the Locomotion System can be used for free in any game authored using [Unity](http://unity3d.com/) - get the [Locomotion System project folder](http://unity3d.com/support/resources/unity-extensions/locomotion-ik) to get started.


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


*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

I've been working on implementing path-finding for The Cluster, the 2.5D platform game I'm developing. Path-finding will let NPCs (enemies, companions, or other characters in the game) be able to find their way around in the world. For example, this will let them be able to chase/follow the player, or flee away from her.

So far I have a simple proof of concept with multiple red NPCs following the player (but not being quite perfect at it yet):

As mentioned before, some aspects of the game have come a long way already, while other are not even touched yet. I have yet to figure out and decide something as basic as what kind of game mechanics I want the game to focus on. I want game mechanics that create a focus on using the environment to one's advantage, and which makes use of the maneuverability of the enemies in an interesting way. But which mechanics can create that form of gameplay? I'm still a novice at game design.

In practically all platform games I've seen, enemies have exceedingly simple movement patterns and a very limited ability to move around in the level. Most often an enemy simply patrols a small path going back and forth or similar. My aim is to develop more engaging enemies that are almost as agile as the player. If anyone knows of existing games that have tackled this problem, I'd like to know!

I want the focus to stay on platforming though and not make it into a combat game. I don't care for twitch or combo based combat, but would prefer a small tactical element instead, using the local environment to one's advantage somehow.

I've thought about the 3 most dominant fighting mechanics in platform games:

**Jumping on enemies' heads**Like in*Mario*or*Sonic***Shooting**(typically horizontally and vertically only) Like in*Commander Keen*or*Cave Story***Melee**(I haven't played a lot of those -*Jak and Daxter*maybe? But that's 3D)

Early tests quickly revealed that jumping on enemies' heads don't work at all with agile enemies that move fast and unpredictably. All games with this mechanic have enemies that move rather slow or at least in a very predictable pattern.

Melee - I'm not sure how that would work well, as you'd have to always approach the enemies closely, which I *think* will make it harder to use the environment in an advantageous way.

Shooting from a distance seems like the best candidate to support the kind of gameplay i want, but I'm still not sure how to model the details of the game mechanics to encourage a play style based more on simple tactics than on head-on confrontation.


*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

I've been working on a platform game on and off in my spare time for a looong time. Working title: **The Cluster**.

It's a [2.5D platform game](http://en.wikipedia.org/wiki/2.5D#3D_games_with_a_two-dimensional_playing_field) with focus on non-linear exploration, set in a big, continuous world. I'm using [Unity](http://unity3d.com/) to develop it.

![](../../assets/4d272c4b7e94d378.png)


![](../../assets/4d272c4b7e94d378.png)

In some respects it has already come a long way (advanced algorithms used to control the world in the game) and in other respects the fundamentals haven't even been decided on yet (the exact gameplay mechanics, story, graphical style...) so it's very much a work in progress.

![](../../assets/1d692696b040ced4.png)


![](../../assets/1d692696b040ced4.png)

I just finished some code that rounds all the corners in the world geometry and it makes it looks way better than it did before! In the image below an area is seen at some distance, and you can see some coins, some springs, some spikes and some enemies. The models are all simple placeholders for now.

![](../../assets/88c202d1629a88cb.png)


![](../../assets/88c202d1629a88cb.png)

I'll continue documenting the progress of The Cluster here, so stay tuned. For some info on the *very* early development when the game was still sprite-based and developed in Delphi Pascal, see [this page](http://runevision.com/multimedia/cavex/) on my website.


I've been spending the last week in San Francisco attending the [Game Developers Conference](http://gdconf.com/) and showing off [Unity](http://unity3d.com/) at our awesome (and very busy) booth.

![](../../assets/5ce1a50b28b18057.img)


### Booth Experiences

The people I've met have been very excited about Unity; both our product in general and about the [new features](http://unity3d.com/unity/coming-soon/unity-3) we'll be releasing in upcoming Unity 3 this summer and which we previewed at the booth. Unlike last year, there were practically no people this year who hadn't heard about Unity some way or another.

### IGF Impressions

The [Independent Games Festival](http://igf.com/) awards show was great. I was especially excited about Danish guys *Playdead* winning no less than two awards for their game [Limbo](http://www.limbogame.org/) and other Danish guys *Press Play* winning an award for their Unity game [Max & the Magic Marker](http://maxandthemagicmarker.com/) for Wii, PC, and Mac. I've had a chance to play both, and they're both excellent games. Coincidentally they're both side-scrolling platform games with a strong puzzle focus, but besides that they're completely different.

### Animation Insights

I only got to see one session this year - [Player Movement and Animation in Drake's Fortune 1 and 2](https://www.cmpevents.com/GD10/a.asp?option=C&V=11&SessID=10429). It was very well presented. Everything was sensible and easy to understand; there was nothing ground-breaking but a lot of useful tips and tricks. With the exception of one thing that was purely done to save memory (flipping animations on the left-right axis), everything they did could be done in Unity without problems. They basically rely on lots of animation blending, some of the animations applying to only part of the skeleton, and some animations being additive; all things that are supported in Unity. They also do some IK fixes, which of course can be done in Unity with scripting.

Their method for making characters standing and moving correctly on uneven surfaces is a little similar to how my [Locomotion System](http://unity3d.com/support/resources/unity-extensions/locomotion-ik) does it, just a bit simpler: They too use raycasts to find the ground height for the feet, then adjust the hip/root height, and then use IK to adjust the legs.

The most interesting thing they did was having a few long animations with random wiggling of the character. By applying this on top of a 1-frame idle animation they get a nice long, varied idle animation, but it means they can have lots of different idle animations that are all just 1 frame long which turn into nice animations when the wiggly-animation is applied on top. They do similar things with walking and running to add variation that can span over a long time but doesn't require much space because it can be reused for many different animations. Perhaps we can add something like that for our new Unity 3 launch demo that we're working on.

### Going Home

It's been a long and hard, awesome week, and I've met lots of great people, but now I also look forward to going home again. I'll be arriving back in Copenhagen on Monday, and once I've recharged a little I'll be continuing working on getting Unity 3 out.


At work I've been working on a Unity demo to demonstrate various animation techniques, and I ended up making it into an actual game (albeit a small one). You can read more about it - and play it! - here:

It's based on a tech demo that Paulius Liekis and I did for a presentation at Unite '09. You can see a video of the presentation here:


This weekend I participated in the [Nordic Game Jam](http://nordicgamejam.org/) - the first and biggest instance of the [Global Game Jam](http://www.globalgamejam.org/) event.

The basic idea is that lots of people meet and split up into small groups that each *make a game in about 40 hours*. That's some seriously intensive game making, which is very exciting and fun (and exhausting). Because the games are so small and quick, there is unlimited room for wild experimentation which would not often be risked in larger scoped games with more serious commitments.

In my group we made [Preschool Theater Director](http://www.globalgamejam.org/2010/preschool-theater-director) - a game where you have to direct a chaotic set of pre-school kids in order to enact Shakespeare's "A Midsummer Night's Dream" on the stage in front of a demanding audience of parents. You can [play it online here](http://runevision.com/multimedia/preschooltheater/) via the Unity browser plug-in.

The game is over quite quickly (if you can remember the names of the children anyway) but the graphics and sound design and general sense of attempting to direct small clueless kids makes it for a funny experience.

[Florian Sänger](http://www.floriansanger.com/) made the graphics, [Bernie Schulenburg](http://bushghost.blogspot.com/) the sound and voices, [Kasper Clemmensen](http://www.myspace.com/lyskurv) produced the music, and [Nils Deneken](http://gutefabrik.com/) contributed with bits here and there though he was busy working on another game at the same time. [Lau Korsgaard](http://dk.linkedin.com/in/laukorsgaard) helped with some initial prototype programming before family commitments took over. After that I was the only programmer on the game which made me somewhat of a bottleneck, but I'm glad we got it into a state where it's fully playable and actually a bit of fun.