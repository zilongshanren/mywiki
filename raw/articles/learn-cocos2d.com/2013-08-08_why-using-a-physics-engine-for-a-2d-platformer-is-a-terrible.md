---
title: Why Using A Physics Engine For A 2D Platformer Is A Terrible Idea
url: http://www.learn-cocos2d.com/2013/08/physics-engine-platformer-terrible-idea/
author: Super Stick Spy New Isometric Look; Kobold Kit says
published: '2013-08-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

For [Kobold Kit](http://koboldkit.com/) (the Sprite Kit game engine) we’re working on **Super Stick Spy**, a 2D platformer game. Like so many others, we started out using the (Box2D) physics engine that’s so neatly integrated in Sprite Kit to get everything up and running quickly.

But we knew full well that for the final product, we’ll have to scrap the physics engine altogether and follow [best practices when it comes to platformer-programming](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/).

Now with the demo version nearing completion (see video) I can tell you in full detail why you don’t want to use a physics engine for a 2D platformer!

### Moving Platform Hell

A moving platform with physics needs to be a dynamic body. Don’t even try moving static bodies, at least in Box2D that will end up in jumpy movement of the body. Though kinematic bodies work better (if available).

The player or other game characters standing on a moving physics body will have the platform slide underneath their feet. The characters won’t magically move along with the platform! And there is no feature in the physics engine that lets you set this up. You have to program it to synchronize character movement with the platform they’re currently standing on, and end the synchronization as soon as a character lifts its feet up from the platform.

Which can be a problem for downward-moving platforms as the player loses contact with the platform every other frame, starts falling, and lands right back on the platform. To put it in Homer’s words: “Doh, doh, doh, doh, doh, doh, doh …”. So you need to make the character stick to the platform, yet allow him to fall off of the ledges and jump, and possibly also allow him to be forced off the ground by normal collision events (projectile impact, platform moving through a tiny crevice).


If the moving platform follows a path but hits an obstacle, it is no longer guaranteed to follow the path exactly. In fact since it is a physics body, any external force acting on it will make it deviate from its preset path - including the player landing on it! This can only be prevented by calculating the position of the platform based on the current path segment’s end points and by considering what percentage of that segment the platform must have traveled based on current time and/or movement speed. Don’t try to do this the simple way with actions or position+velocity integration.

If there is any chance of the platform getting other characters stuck between collisions, like a lift dropping all the way to the floor, you need to prevent this situation. Otherwise the stuck character may be forcefully repositioned by the physics engine. That character could end up in completely blocked space, or on the other side of a blocked door, or on top of the lift or to the sides of it.

### Walking on Sunshine, Not

A common issue with physics engines is that they treat the corners of bounding boxes as just as solid (rigid) as the rest of the bodies’ bounding box. Therefore characters can easily get stuck in areas where differently angled slopes meet. Fortunately Box2D has chain shapes with which this problem can be prevented through specifying “neighbor” points. But this is tedious to setup.

Furthermore, walking along a slope will always have characters with rectangle bounding boxes slide up in the air. Walking up a 30° slope to the left means only the lower left corner of the bounding box will meet with the slope, which leaves the center and bottom right areas of the bounding box high above the ground:

The only way to force a character to walk with his feet on the ground is by purposefully giving the collision shape for the slope a one-tile offset to the right. That of course only works if your tile sizes and player sizes match. Plus it makes designing levels and generating collisions from it so much harder.

In turn, if you move along a slope downwards, the character won’t just slide down on it. The steeper the slope, the more it will “bunny hop” downwards rather than slide. This just doesn’t look good, and it causes issues with other aspects of the game. Say you don’t allow the player to jump in mid air - that then makes jumping while walking down a slope completely unreliable without extra code counteracting against this.

### Tilemap Collisions Ain’t Easy

You’d think that every tilemap tile being a rectangle, you could simulate physics collisions by generating a box for every tile. Nope.

Not only is this incredibly wasteful, both memory wise and runtime performance (collision detection). It will lead to the aforementioned movement problems where moving bodies get stuck on edges. And by edges I mean any two boxes sitting next to each other, forming a seemingly straight line. Yet the character can get stuck trying to move across these boxes.

To properly create physics collision shapes for tilemaps you need to apply contour tracing (Moore algorithm) like the solution I implemented in [KoboldTouch](http://www.koboldtouch.com/). This generates paths forming the contours of a tilemap, and from those paths you can more easily create the necessary chain shapes for smooth movement across even surfaces.

In a custom platformer physics engine you’d simply check each character’s surrounding tiles with CGRectIntersect tests and then determine whether a contact occurs or doesn’t. You essentially analyze and respond to what’s happening in the tilemap collision-wise as the character moves along rather than having to pre-generate the collisions.

The latter creates an interesting problem: if tracing contours and creating physics shapes is costly, how do you open blocked doors for instance? In a physics world, you’d have to add an extra blocking body and subsequently remove it. In custom tilemap collision detection routine you’d simply detect that the previously blocking tile has been replaced with one that isn’t blocking (or removed altogether).

### Physics contact detection is expensive

With a physics engine contact and collision detection just works. This is the good part. You can get going quickly.

However as levels grow in size, complexity and number of interactive objects, the physics engine will slow you down. You may need to put all physics bodies outside the visible screen area to sleep.

And then most contact tests really are just rectangle intersection tests. You can do the same just as well with CGRectIntersect. Especially if you consider you’ll have to write custom contact code anyway for things like slopes.

Just as problematic is how physics engines filter out contacts. You have contact, collision and category bit masks. They’re easy to confuse, so you may end up not being able to pick up powerup items because you forgot to set the flags in both the character and the powerup item correctly. You could as well let all contact events go through, and then look at the contacting object’s types to determine whether to ignore the contact or not. But this wastes the performance enhancing effect of using filters in the first place to prevent unwanted contact events from spamming the system.

With custom, rectangle intersection based collision detection you can typically create an easier to understand and faster contact event system.

### Physics are alwaaa-a-a-ays glit-tch-tch-tch-y

This is just stating the obvious: you can never entirely prevent (or foresee) all possible physics engine glitches. Fortunately these effects are much less pronounced than they used to be, at least in 2D physics engines.

But still, you could end up with stacked bodies never coming to rest. Squeezed bodies tunneling and being repositioned elsewhere from one frame to the other. Joint connections being stretched far beyond reasonable and blocking pathways or worse, “exploding” everything touching them to extreme velocities.

Due to the dynamic nature of physics engines, and the fact that you most certainly didn’t write the physics engine, makes it quite difficult to debug such issues. And it rules out all “offset” type movement because you have no guarantee that the current position is the correct one to begin with.

### There’s got to be a speed limit on everything

Due to the potential glitches but also because of falling bodies accelerating indefinitely, you **have** to put a velocity cap on every moving object. There is hardly a way around it, and hardly an easier way to prevent most glitches or at least soften their impact on gameplay.

Under no circumstances should you allow any body move faster than the speed it could reasonably move at. Otherwise such objects could simply bypass collisions (in science you’d call this effect quantum tunneling).

That means touching and comparing many body’s velocities every frame, before the simulation (world step) occurs. In a custom platformer physics the velocity cap would be an inherent aspect of moving a character in the first place.

### Tweak the hell out of this world

In a physics world, bodies influence each other through collisions. If you change one aspect of one body (ie mass) this will affect other bodies it contacts (ie higher escape velocities). You can not make changes in isolation, you always have to consider that for every physics property you change on one body, all the other potentially interacting bodies will be affected by this change.

In custom platformer physics you usually ignore certain properties based on object types and what not. You don’t actually have to make a crate heavier if you want to make it accelerate downwards faster. You would instead simply change its gravitational factor, but collisions with other objects won’t be influenced unless you purposefully consider the impacting object’s speed.

So a custom platformer physics allows you to selectively apply only the properties that need to be applied in a specific situation. In a physics engine world, you can’t really do that. Building a world with a physics engine is the equivalent of building a house from a deck of cards rather than building one out of Legos.

### Speaking of Movement

Have you played any platformers lately? Do any of those characters jump, walk, run, roll, fall, crawl, etc. like a physics object does?

No. Therefore at least the player’s own movement behavior needs to be severely customized in a physics world. In a way that you may end up taking over every aspect of the player’s movement from the physics engine. And when you do that, but you still have the physics body attached to it, more glitches can occur.

For example when two bodies impact each other, their velocities are used to calculate the outcome of the collision. Now if you move a character manually and end up only updating the position property, the physics body’s velocity may fluctuate every frame because the physics engine keeps trying to accelerate the body in the direction of gravity. That means you could end up with very weird collision behavior.

Fighting these effects gets worse when you want to implement features like wall-sliding or wall-jumps. Or allowing the character while jumping to slide along the ceiling until its upwards velocity runs out - the physics engine’s default behavior will be to stop the character when it hits the ceiling, reset the vertical velocity, and let gravity act on it, instantly pulling it downwards.

Or let’s consider a very simple, very basic yet essential maneuver: landing.

Have you ever seen a platformer player character bounce off of the ground when it lands? I haven’t. It makes for bad gameplay. Again, the “no jumping while in air” issue comes into play here.

Unfortunately, with physics this bouncing behavior is pretty much guaranteed. And it is difficult to circumvent: you have to determine that you’ve actually landed, and then you have to reset the velocities. The difficulty lies not in writing this code, but considering the various circumstances where this ideal scenario breaks. Landing on a moving platform, for example. Or disregarding pickup items because you don’t actually land on them.

Do you want the player to be sliding a little when changing movement direction? Then physics are a fine helper. If not, again you have to write code to force this behavior and consider circumstances where it doesn’t apply. Like for example when you do want to allow the player to change movement in mid-air but not abruptly like on the floor.

This list goes on and on and on …

### Is it too early or too late?

Whenever you write custom code to circumvent physics engine behavior, you not only have to consider when you perform this code in relation to other characters. You also must know when to apply this to the physics body. You always have two choices: before or after the world step.

Which one you use normally doesn’t make any difference. But it can lead to subtle issues like the position of the player following the position of the moving platform with a 1-frame delay. Or it could have your character jitter on the floor, perhaps only after falling from a high ledge.

Normally you will want to feed the physics engine with your custom positions and velocities before doing the world step. But when you use other physics bodies’ positions and velocities in your calculations, they again may be one frame off.

In the worst case you may need to apply changes before the world step, and then verify positions and velocities for plausibility (or simply cap them) after the physics simulation and before the rendering.

### Summary: physics engines vs platformers

Tough love!

Physics are simple enough to get you going, but you quickly get to the point where the physics engine stops being useful and only gets in the way. Depending on what game you are developing, you might get away with it.

For a really well done platformer, a physics engine is out of the question. You’d be too busy to fight it so that the time and effort it takes to create custom platformer collision routines that you’ll actually be able to debug is the preferable option.

To this end we’re currently in the process of removing and replacing physics engine code and behavior from **Super Stick Spy** step by step. Eventually we’ll have an implementation of platformer movement & collision behavior [as explained in this great article](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/) and [others](http://www.wildbunny.co.uk/blog/2011/12/14/how-to-make-a-2d-platform-game-part-2-collision-detection/).

Yet, since we already have the contour tracing code in, we can still use the physics engine for visual effects and dynamic bodies whose movement doesn’t need to adhere to platformer standards (ie items, physics puzzles).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] On related news, you may also be interested in my iDevBlogADay post over at Learn Cocos2D where I give you an insight into the many problems associated with physics engines in a 2D platformer game. […]

According to moving platforms in Box2D, you can make moving objects kinematic and apply linear and/or angular velocity. In this situation all object on such platform are moving properly.

Yes, with the “Kinematic” option, platforms work just as they should. This should be noted.

There are certainly a lot of things to deal with when using a physics engine of any sort. Most of the same problems apply to 3D engines, too. Some of these things can be solved reasonably, though.

What about kinematic bodies? I would use those for moving platforms, as long as you don’t need them to be motor-controlled. They behave similarly to static bodies (they ignore forces), but can move. You would set the velocity directly depending on the game state.

If you’re using a physics engine, you might have to treat your characters more physically than with a traditional approach. Real people do not slide along the ground when they move or else you would certainly expect them to trip over slight protruding edges. My approach is to use high-friction invisible wheels on characters to smooth out their movement over very small obstacles. Then on-ground motion is controlled by setting the motor speed (calculate via desired arc-length per second) of the wheels instead of applying a body-centered force. Wheel suspension can be adjusted so landings are smooth and not bouncy and downward slopes are no problem.

I think collision grouping bit masks are too hard to use and manage. For Box2D in particular, I override the b2ContactFilter::ShouldCollide method for real control over whether collisions should happen for a particular pair of fixtures/bodies at a given time.

I think physics engines have a place in some platformers, definitely not all though. It might be faster and less headache-inducing to write your own platforming physics, but once you get through some of the surprising details of a generic physics engine, you have a good code base and experience for games of other types, too.

p.s. Quantum tunneling doesn’t really depend on the speed of the particle, since there’s a probability of the particle bypassing any finite potential hill regardless of the energy required; it’s a calculable probability wave phenomenon as opposed to a classical particle effect.

Ok, kinematic bodies certainly solve some issues. Unfortunately this is currently not supported by SK.

[…] As previously mentioned, our Super Stick Spy game/starterkit will move to “real” platformer physics, because using a physics engine for a 2D platformer is a terrible idea. […]

I think this article sucks!

Its not true people that physics engines arent good for platform games. Box2d is really good, check out the credits on lots of best sellers apps. for example: “league of evil”, you will see box2d 😉

There are many games named “League of Evil” or quite similar. The popular iOS hit doesn’t have Box2D in its credits.

Well, first edition doesn’t have a credits screen at all (unless there’s one when you complete the game), version 2 only shows 3 names, and there’s nothing on the website or on google indicating they used a physics engine or Box2D. For this title I’d be really surprised if they did use a physics engine, that’s exactly the kind of title that would suffer from relying on a physics engine and not using custom platformer physics.

Limbo uses box2D

http://en.wikipedia.org/wiki/Limbo_(video_game)

I think the article is useful in that it highlights possible difficulties with using a physics engine. However, I used physics in my platformer (wrote my own physics code) and didn’t regret it at all.

Little big planet is a physics based 2.5 D platformer….<.<

Yes, that’s certainly a notable exception. On the other hand it doesn’t really qualify as just being a platformer, it’s more a puzzle and sandbox game.

But speaking of which Limbo definitely falls in the category of a physics-engine platformer.

Solutions using Box2D:

Moving Platform Hell:

Kinematic body

Walking on Sunshine, Not:

Ghost vertices for static ground, rounded player “feet” for dynamic ground

Tilemap Collisions Ain’t Easy:

Ghost vertices

Physics contact detection is expensive:

Collision callbacks (very efficient)

There’s got to be a speed limit on everything:

There is and it’s modifiable in b2Settings

Speaking of Movement:

The two biggest known retro-platformers had realistic physics: Mario and Sonic.

Arguably, most modern platformers have a realistic in-house physics engine or use a 3rd party general-purpose physics engine.

In my opinion, if you plan on making a professional looking game, at this point in time, it would be a good idea to have knowledge of how to apply a physics engine to the task.

Player feet wheels? Ghost vertices? Seems like a lot of work to solve problems that are easily addressed by custom player physics. Even the process of determining if the player is grounded becomes complicated when using a realistic physics engine.

Mario and Sonic didn’t have realistic physics in the slightest. Sonic in particular is a big collection of hardcoded hacks, with four movement modes just to glue the player to walls and ceilings. See http://info.sonicretro.org/Sonic_Physics_Guide for specifics.

Using a solid circle for feet is easy; just create a circle shape and listen for contacts like you would any feet sensor. Ghost vertices are similarly easy to specify; Box2D even provides EdgeChain and EdgeLoop shapes to do it for you (though converting a tilemap to segment chains can be tricky).

Creating your own physics engine and collision engine, even a relatively simple one, would take much longer.

Also, you are arguing against yourself; you say in your first paragraph that doing character physics in a realistic physics engine is “complicated”, but in your second paragraph you state that unrealistic, integer-based engines are “a big collection of hardcoded hacks”.

The goal would not be to create a realistic physics engine but a simplistic one designed for 2D platforming. I fail to see the contradiction in the statements you referenced.

I suggest you check out- and by check out I mean play- the demo for Intrusion 2. The game is probably the most original and ‘ well done’ platform shooter in years. I’m no game designer/programmer/etc, but it seems that it’s well worth the effort of using a physics engine if you can make a game as great as this.

Pity that the game is underrated. If you’re a fan of run and guns, then I can almost guarantee that this game will blow your mind away, and possibly change your outlook on physics based platformers.

And I almost forgot to mention Super Mario 63. It’s fan game that puts mario in a physics based adventure.

Lay aside your prejudices upon fan games. This game, while very slightly buggy, could have been made by nintendo themselves.

Most of these have simple solutions, many of which you would also need to implement in a custom collision engine.

Moving Platform Hell

Kinematic bodies. If your physics engine doesn’t support them then find one that does.

Walking on Sunshine, Not

Just change where you’re drawing the sprites.

Tilemap Collisions Ain’t Easy

There’s a simple solution for this that doesn’t involve edge shapes. Google is your friend.

Physics contact detection is expensive

You don’t seem to understand how a physics engine works.

Physics are alwaaa-a-a-ays glit-tch-tch-tch-y

If you need a lot of bodies on screen, lower the iterations. If you need more accuracy, increase the iterations. Done.

There’s got to be a speed limit on everything

There’s a global settings for this. There’s also way to have bodies with infinite speed. You’d also run into the same issue with a custom collision engine.

Tweak the hell out of this world

You have to tweak the hell out of any world.

Speaking of Movement

Again, you’re mentioning things that are easily fixable or that you would also encounter in a custom collision engine.

Is it too early or too late?

I’ll add that you appear to be misusing the physics engine. You’re not supposed to set the position and velocity directly (unless you’re using a kinematic body).

Nice article, but I got some problem now.

How to make a moveale and collideable object without physics engine,for example the player moved a box and stood on it.

Newer to cocos2dx,thanks for help.

In principle you need a reference to the attached object in the player object. First move the object, which adds the corresponding object movement offset to the player. Then move the player normally. Also requires extra checks to see if the player landed on a “dynamic” object vs “static” background collisions.

Thanks, I’ll try.

“In custom platformer physics you usually ignore certain properties based on object types and what not. You don’t actually have to make a crate heavier if you want to make it accelerate downwards faster.”

Making an object heavier wouldn’t make it accelerate any faster. As the mass of an object increases, so does the force of gravity, and thus acceleration remains constant.

Here’s a neat follow-up to this:

Shovel Knight, hailed as the best modern retro platformer in recent years, mainly for its great gameplay, uses Box2D!

Now, they did actually keep the physics simple: everything consists of boxes, so there are no rounded edges.

But this certainly still showcases what a finely tuned Box2D set up can feel like!

hello Steffen!

with much respect I will have to disagree with you about everything you just wrote in this article. the problems you mentioned are not with Box2d, but simply with you misusing it.

some people in the comments already addressed some of the things I’m about to say, but I still have some things to add:

* Moving Platform Hell:

with kinematic bodies and friction it works perfectly fine. but if you rather do it yourself you can always add a sensor to the the bottom of the character and use the contact events to detect when you attach and detach from a platform and implement your own customized code to stick the character to the platform. I don’t see how detecting it yourself is easier than using a Box2d sensor.

as for a platform following a path - as people already mentioned here use kinematic bodies. and if you want more accuracy you can set the bodies position directly based on the time and state of the moving platform. so I see no issue here.

* Walking on Sunshine, Not:

that’s why you never use box shape for a character. use a capsule shape and tweak the friction.

* Tilemap Collisions Ain’t Easy:

getting stuck between neighbor tiles problem is solved if you use capsule for your characters instead of box.

you suggested one solution there which is nice if your tiles are static. if you want dynamic tiles with efficient collision detection you can always create your own customized shape that checks collision in a better way. anyway not every platformer is tile based.

* Physics contact detection is expensive:

if you find Box2d to slow you down you are doing something wrong. unless you put thousands of entities all together in a small space bouncing around and hitting each other (which I assume you didn’t…), you shouldn’t be worrying about performance. also just because you didn’t understand how to use category masks correctly or forgot how to set your bodies doesn’t mean it’s a bad system. that’s like saying a car sucks because you don’t know how to handle its stick.

* Physics are alwaaa-a-a-ays glit-tch-tch-tch-y:

if you found bugs in Box2d please report them to the authors.

anyway all the glitches you mentioned - are you saying you can implement those things better yourself? are you suggesting that you wrote rigid bodies, joints, collision etc better than box2d? if you did please do share the code with us! but if you didn’t what you are basically saying to the game developer is to give up lots of features they might need because they might be glitchy. that’s not a reason not to use a physics engine. if you don’t like those specific features simply don’t use them.

and I am well familiar with the glitches you mentioned yet I never had them in any of my projects. perhaps you had too few simulator iterations or you did weird things with box2d to cause this. the only glitch I ever had with box2d was the “never resting bodies”, which can be solved very easily with making corpses turn static after, say, 5 seconds they didn’t move too much. its not that big of a deal.

* There’s got to be a speed limit on everything

Devon already answered this perfectly.

* Tweak the hell out of this world

tweaking takes a lot less than writing the whole thing yourself. also an easy way I found to get decent physics - just stick to real life properties. use real life gravity and mass, try to maintain realistic proportions, and its done.

* Speaking of Movement:

you are using it all wrong. you don’t “move” the player, you apply force on its physical body and update the sprite based on the body movement. use friction and bounciness (forgot the property real name :P) to make your character react properly to collision. you can tell box2d you don’t want your character to bounce. its easy. now lets say you suddenly want to create an icy, slippery level. if you wrote your own physical engine you now need to implement a whole new feature. good luck with that. if you used box2d you simply change the friction of the ground. one line of code.

as for things like mid-air jumps etc, these are things you will have to face anyway if you write your own physics. but as I mentioned before: add a sensor to the legs of your character and use the contact callback to know when he is standing on a ground (or anything else) and when he detach from it. this solve so many problems you don’t even know exist yet.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


* Is it too early or too late?:

you said this: “Normally you will want to feed the physics engine with your custom positions and velocities before doing the world step. But when you use other physics bodies’ positions and velocities in your calculations, they again may be one frame off.”.

NO. I can’t possible express how wrong that is! whats the point of a physics simulator if you force your own input every frame and override everything it just calculated?? what are you doing man?? now I understand why you had so many glitches… 😛

* Summary: physics engines vs platformers

I urge you to read some tutorials and give Box2d another try. not just for this game, but for future projects as well. you won’t regret this.

just because you don’t know how to use a technology doesn’t mean its bad. I’m sorry if I sound a little harsh but this post is very misleading and I can actually imagine young developers who read this and think “oh I should write my own physics engine!” while this is a huge mistake that will cost them time and frustration.

Thank you Ness, i agree with all you wrote.

Totally correct! Glad someone beat me to it and wrote these things down.

Box2D is simply one of the most useful tooms in a game developer’s toolbox. And I have created both my own physics engine and several game engines. Box2D solved so many problems I

I made my own physics engine, I couldn’t be happier.

Not to take away from what Box2D can be, for beginners its a great tool and can save you a lot of time, BUT, someone mentioned Mario and Sonic for games that used realistic physics and that’s pure bs (for one they’re not realistic, that’s what we like about them)

If Mario and Sonic were made *from scratch* today, they would not be using an existing physics engine. Once you start breaking the mold of what the physics engine was built for, that’s the time to start debating whether it’s worth using. There’s too many custom platforms and environments in action platformers to justify using an engine. Puzzle platformers can sneak by since they rarely do more then basic movement

In your article you mentioned the walljumping issue with Box2D. Is walljumping possible in Box2D? Yes. Would it be easier to implement in a custom physics engine? If you know what you’re doing, yes. There’s less hurdles to jump through and less to think about if you made the engine yourself, BUT, that’s assuming you made a good engine.

And that’s what this really boils down to. Beginners who can’t see the limitations of using a physics engine should just use one until they themselves decide they don’t like it. The only reason I managed to make a good engine is because I’ve done it a few times in the past, I have experience about how to organize and plan the structure of it

It also depends on what you want to make. I’m making an action platformer, so I need lots of control over slopes, character movement, enemy movement, etc. A game like Limbo doesn’t need that since it basically consists of jumping and moving left/right

Sidenote: I personally found Limbo boring as hell and I wasn’t a fan of the physics. Never quite understood the hype

Mario and Sonic did use realistic physics at the time. Most platformers in those days felt like Shinobu or Megaman: not realistic at all. Interestingly enough, modern Mario and Sonic games also use a physics engine. But that’s somewhat irrelevent as every AAA game these days uses one.