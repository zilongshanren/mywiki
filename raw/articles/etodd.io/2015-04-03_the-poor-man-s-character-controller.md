---
title: The Poor Man's Character Controller
url: https://etodd.io/2015/04/03/poor-mans-character-controller/
published: '2015-04-03'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# The Poor Man's Character Controller

Let's say that, like so many of us, you want to make a surreal voxel-based first-person parkour game. You're trying to figure out a production schedule. What will take the longest? Graphics? Sound? Level design? I bet it will be the character controller. And I bet it will take 4½ years. Why?

- In running/jumping games, player movement is paramount. It takes forever to nail the right feeling.
- Each game is a unique snowflake. You will not find an article explaining how to design the controls for your specific game. You're flying blind.

That said, each game offers a few transferrable bits of wisdom. Here's my story.

### Make a character

You're a programmer, but one time you were able to suppress the gag reflex
while using [GIMP](http://gimp.org), so you're pretty much an
artist too. You can draw a player character.

![](../../assets/cf929b1ea4129c71.jpg)


![](../../assets/cf929b1ea4129c71.jpg)

That's certainly... a drawing. So the player is an anthropomorphized cylinder?
Well, we've seen [worse](https://en.wikipedia.org/wiki/Thomas_Was_Alone).

If this character has any flaw, it's that he's too exciting and interesting.
Can you make him a little more boring and generic? What if you use
[MakeHuman](http://www.makehuman.org/)? It literally generates human
characters from a template.

![](../../assets/ec662f817f60359f.png)


![](../../assets/ec662f817f60359f.png)

Much better. But there's just one problem: this is a first-person game, so when players look down, they can see their own nose:

![](../../assets/809589343fb1faaa.png)


![](../../assets/809589343fb1faaa.png)

Also, the "pectoral musculature" slider is a tad high, and players are getting confused about their gender.

You end up switching to a female character. Because why not?

Now for the nose problem. You can't remove the entire head, because a headless shadow might be somewhat disconcerting. What if you just remove the face?

![](../../assets/3d98d0d9adeaabb5.jpg)


![](../../assets/3d98d0d9adeaabb5.jpg)

(Eventually you revamp the model, hire an animator, and use separate models, one sans head, for the first-person view and shadow renderer. But none of that is entertaining.)

### Make it move

You're using a great physics engine (seriously, [it's quite good](http://www.bepuphysics.com/))
that comes with a simple character controller. It looks like this:

![](../../assets/e349c02e1f17841a.png)


![](../../assets/e349c02e1f17841a.png)

The character is a cylinder floating above the ground, supported by a single raycast. This way, the cylinder can clear a small obstacle, and once the raycast hits it, the whole apparatus jumps on top.

Since the game world is made of voxels, you quickly run into this problem:![](../../assets/8dfde2fdca9d45c4.png)


![](../../assets/8dfde2fdca9d45c4.png)

Tons of players get stuck this way in your first alpha release. Rather than spend time on an elegant solution, you brute-force it:

![](../../assets/590fb50b26c84d26.png)


![](../../assets/590fb50b26c84d26.png)

Despite this, people still get stuck. You resort to a collision handler that actually pushes the character away from anything that could cause problems. You also interpolate the vertical position to smooth out the camera when traversing uneven voxels:

![](../../assets/6d5f831f57a91c95.png)


![](../../assets/6d5f831f57a91c95.png)

### Make it unrealistic

In an attempt to model reality accurately, the game has no air control at this
point. When you originally made this decision, you somehow forgot that the game
is about an *imaginary cube world*.

Thankfully, after listening to player feedback, you have a change of heart. In the real world, traceurs have many control dimensions (namely, their muscles) that enable precise jumps. Video games have exactly one button. Air control is only fair.

### Make it fun

Since parkour is about momentum, you want the character to take several seconds to reach max speed. Which is fine, except that low acceleration makes small adjustments difficult. The first step takes forever, and the character feels like a semi truck.

Your solution uses different accelerations depending on the current speed. The final speed curve looks like this:

![](../../assets/70ba96fc483b6908.png)


![](../../assets/70ba96fc483b6908.png)

This solves half the problem, but players can still use the mouse to quickly whip the camera around 90+ degrees, which resets their speed back to zero.

You experiment with a few hacks, but eventually settle on a solution using the
[dot product](http://mathworld.wolfram.com/DotProduct.html). It's
basically a measure of the angle between two vectors multiplied by their
magnitude. (Here's a quick [interactive demo](http://et1337.github.io/shaders/#/42/1).)

You use a dot product to find out how much side-to-side momentum the character has. If they're facing perpendicular to the direction of their momentum, the dot product will be large. You use that to increase the acceleration. Long story short, turning no longer burns momentum.

### Make it slippery

There are other ways to lose momentum, like running into a brick wall. You try to mitigate this with low friction physics materials, but angling yourself into a wall will always slow you down:

You are inspired by a [blog post](http://mikebithell.tumblr.com/post/83244226608/aaa-game-control-in-an-indies-evening)
by Mike Bithell on this topic. You use three raycasts and some [cross product magic](https://github.com/et1337/Lemma/commit/ef84bed75d92fc042c6e7636403913ee9deb142c#diff-dc327dde1a6c651c144c14e700a2854fR492)
to figure out a velocity that will slide along the wall.

Later on, you discover another annoyance. Your [wonderful voxel engine](https://etodd.io/2015/02/18/the-poor-mans-voxel-engine/) sometimes
helpfully constructs voxels like this:

![](../../assets/94a7d00607eb13ea.png)


![](../../assets/94a7d00607eb13ea.png)

There's a seam between the two adjacent blocks due to [floating point error](http://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html).
When the character moves flush with the wall and tries to jump upward, it hits
the seam and immediately stops.

The solution is brain-dead simple: change the cylinder to a capsule. Yes, it really does take you 4 years to figure this out.

### Make it forgiving

At first, players just don't understand the movement mechanics. They think they can't get from point A to point B, until you tap them on the shoulder and explain they have to do XYZ. You suspect this is because your tutorial is actually a placebo at this point.

Eventually, the tutorial gets pretty good. Everyone understands the movement capabilities, and they can figure out which moves to use. But now they have a new problem: they fail in the twitchy execution and timing details of their plans.

The worst culprit is a single infamous jump in the tutorial. It tries to teach players how to grab ledges because it's too long to cross with a normal jump.

![](../../assets/94add627207c5db5.png)


![](../../assets/94add627207c5db5.png)

Players fail two or three times before you tell them to "button-mash", which helps them nail the timing through sheer brute-force. Interestingly, as soon as they make this one jump, they have no trouble completing future jumps without button-mashing. For a while, you arrogantly conclude that people are just stupid.

Part of the problem is still the tutorial: you ask players to make a leap of faith and perform a move they've never seen before. They have no idea what the character will do or how long it will take. So you add another, earlier tutorial that lets players try out the ledge grab in a safe space.

But the frustration of perfect timing remains. The solution is two-fold:

- Let players jump for a split second after they walk off an edge.
- Let them hold buttons instead of tapping at the right moment.

![](../../assets/3c4b6db954ea9c01.png)


![](../../assets/3c4b6db954ea9c01.png)

To the surprise of no one but you, this makes the game a lot less frustrating and a lot more fun.

### Make it look good

Over the course of development, you stumble on a few animation tricks. With enough nifty procedural animation, maybe people won't notice your shoddy weight painting and texture work!

- Attach the camera position to the character's head bone, but use a separate root bone to control camera rotation. This eliminates weird rotations when blending between animations.
- Speaking of which, use a quadratic curve to blend between animations rather than straight linear.
- Also, don't use
[linear matrix interpolation](https://etodd.io/assets/DefenselessVerifiableBluefintuna.mp4). Instead use[quaternion interpolation](https://etodd.io/assets/WelltodoPleasedAvocet.mp4). - Remember the dot product from earlier, for calculating side-to-side momentum? Use that to make the character and camera lean when turning at speed.
- Run the character bone transforms through filters for nice effects like tilting the character's head when looking up and down.
- Plant the character's feet and play a little foot-shuffling animation when turning in place.

(For a much more eloquent and in-depth look at procedural animation, check out
[David Rosen's GDC talk](http://www.gdcvault.com/play/1020583/Animation-Bootcamp-An-Indie-Approach).)

### Conclusion

![](../../assets/b219898f9c405a68.jpg)


![](../../assets/b219898f9c405a68.jpg)

Budget an extraordinary amount of time for your character controller. Make it
special and unique. And if you're me, prepare to be *wrong* most of the
time.

[Lemma](http://lemmagame.com) is set to release in May. The entire
game engine is [on GitHub](https://github.com/et1337/Lemma). If you
enjoyed this article, try these:

[The Poor Man's Postmortem - Lemma](https://etodd.io/2015/06/25/poor-mans-postmortem-lemma/)[The Poor Man's Voxel Engine](https://etodd.io/2015/02/18/the-poor-mans-voxel-engine/)[The Poor Man's Dialogue Tree](https://etodd.io/2014/05/16/the-poor-mans-dialogue-tree/)[The Poor Man's Gameplay Analytics](https://etodd.io/2014/02/19/the-poor-mans-gameplay-analytics/)

Thanks for reading!