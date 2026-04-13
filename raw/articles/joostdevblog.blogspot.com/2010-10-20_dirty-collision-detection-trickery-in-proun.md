---
title: Dirty collision detection trickery in Proun
url: http://joostdevblog.blogspot.com/2010/10/dirty-collision-detection-trickery-in.html
author: Joost van Dongen
published: '2010-10-20'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*Pr0n*instead of

*Proun*. I think this may be due to the dirtiness of some of the coding tricks I used in Proun.

Or

*maybe*it is because these words are written so similarly. No, really, I don't think so.

Anyway, programmers who worked with me might agree that I have pretty radical ideas on what good programming is, especially in comparison to how large console games are usually made. I almost always choose simplicity and understandability over performance, over memory use and often even over amount of work.

Most coding interns need to get used to the idea that sometimes when they consider something done, but there is still a way of structuring it in a better way, I actually make them go back and change their already working code, just to make the code itself better. Since the games at Ronimo are around 100.000 lines of code, keeping the code clean is very important. No way will we find our bugs if such an amount of code is also a mess!

An extreme example of choosing simplicity over performance can be found in the collision detection in

[Proun](http://www.proun-game.com/).

Collision detection in games is usually done per frame. So 60 times per second, all objects are moved a bit and then the game checks whether they collide. This means that the time


This becomes a problem when fast moving objects (e.g. bullets) pass through thin obstacles: in one frame they are on one side of the obstacle, and in the next frame they already passed it.


![](../../assets/f55d964f5002781d.gif)



Common solutions to this problem are to cast a ray between the position at the previous frame and the current position. An alternative is to do sub-steps just for the collision detection and only when moving really fast.


![](../../assets/46ffd48091052a0e.gif)



Both of these solutions share that they would need additional work in the collision detection of vehicles in Proun. When doing the solution with subframes, the collision detection would run at a different framerate from the rest of the game, which increases the complexity of the code. Not dramatically, but it is more complex nevertheless.


For Proun, I implemented a simpler solution:


The result is that even when you race extremely fast (grab a turbo on Impossible difficulty to do that), you still don't move too fast to pass through objects without collision detection detecting this.


Any reasonable programmer would say this is idiotic. So much performance wasted! I even update all obstacle animations at this framerate. Unnecessary! However, Proun's performance is almost entirely in the graphics. The gameplay is very simple and can be processed really quickly, so why would I bother implementing something more efficient and more complex? Doing a lot of gameplay updates per frame is really simple to implement and everything just works. I don't need to add any math for the time-in-between or anything like that, I don't need to think about having different framerates for collision detection and for other gameplay aspects. Any other solution would have made the collision detection code more complex than it is now.


I tested the actual performance impact of this and it turns out that this only impacts the framerate in a relevant way when a really slow processor is combined with a very fast videocard. No one actually has such a combination, so I don't consider that relevant.


So. Simple! Clear!



*between*two frames is completely ignored!This becomes a problem when fast moving objects (e.g. bullets) pass through thin obstacles: in one frame they are on one side of the obstacle, and in the next frame they already passed it.

![](../../assets/f55d964f5002781d.gif)

Common solutions to this problem are to cast a ray between the position at the previous frame and the current position. An alternative is to do sub-steps just for the collision detection and only when moving really fast.

![](../../assets/46ffd48091052a0e.gif)

Both of these solutions share that they would need additional work in the collision detection of vehicles in Proun. When doing the solution with subframes, the collision detection would run at a different framerate from the rest of the game, which increases the complexity of the code. Not dramatically, but it is more complex nevertheless.

For Proun, I implemented a simpler solution:

*all gameplay in Proun runs at a fixed*. Three thousand. Three thousand! The graphics still runs at 60fps, of course (or less if your videocard is too slow).**3000**frames per secondThe result is that even when you race extremely fast (grab a turbo on Impossible difficulty to do that), you still don't move too fast to pass through objects without collision detection detecting this.

Any reasonable programmer would say this is idiotic. So much performance wasted! I even update all obstacle animations at this framerate. Unnecessary! However, Proun's performance is almost entirely in the graphics. The gameplay is very simple and can be processed really quickly, so why would I bother implementing something more efficient and more complex? Doing a lot of gameplay updates per frame is really simple to implement and everything just works. I don't need to add any math for the time-in-between or anything like that, I don't need to think about having different framerates for collision detection and for other gameplay aspects. Any other solution would have made the collision detection code more complex than it is now.

I tested the actual performance impact of this and it turns out that this only impacts the framerate in a relevant way when a really slow processor is combined with a very fast videocard. No one actually has such a combination, so I don't consider that relevant.

So. Simple! Clear!

*(And in fact not dirty at all, so maybe the words*Pr0n*and*Proun*do look pretty similar...)*
Great! For a First Person Shooter I would choose a 60 (or even 30) fps and then shoot the ray between positions for objects moving fast. But for this case, I think yours is the best solution.

ReplyDeleteFor a gun, that would indeed be a better, because the bullets are insanely small. 3000fps collision detection would still be to low for that.


ReplyDeleteA complication in Proun is that the level is sometimes also moving, so I also get more precise collision detection with moving obstacles for free this way. :)

Because the collision objects seem to be all geometric solids why not consider swept-volume calculations? Or even simple ray intersection tests?



ReplyDeleteThat way you can simulate at any framerate and still obtain perfect collision detection.

After all 3000 frames per second isn't fixing the problem, the same fixed-frame collision problem exists, just extremely hard to reproduce (very thin objects, and very high speeds will still glitch!)

The point of the 3000fps decision is not that it is the best solution in terms of results and performance, but that it is the simplest solution to implement, has the smallest chance of resulting in math-bugs and such, and was really quick to make. :)



ReplyDeleteThe problem with swept volumes is that their math is pretty complicated and I would have needed to rewrite my collision-solving code, because you suddenly need to take into account that penetration depth of the swept volume is not the same as the offset that needs to be applied to the vehicle. The same goes for ray-casting, with the added problem that the ray does not represent the entire volume.

As for very thin objects: all objects in Proun are polygon-based, so all collision detection is always against infinitely thin objects. When the speeds are high enough, this will indeed break. However, I know the size of the player's vehicle (which is a sphere volume) and I know the maximum speed that can ever happen in the game, so I can calculate a framerate at which issues can never happen at all.

I had this issue when I made a 2D platformer in Game Maker, but my solution was, rather than checking for a collision at the player's current position, I checked for it as the players position, plus its horizontal and vertical speed values, effectively checking everything one frame ahead.

ReplyDeleteInteresting approach! But does that actually work? If an object goes too fast to detect collision, why would you detect the collision if you check one frame ahead? You still move with the same speed and don't do anything in between frames, right?

ReplyDeleteI think RandomAnimations27's solution is more useful to stop objects from partially "digging" in the thing they are colliding with than to prevent tunelling.




ReplyDeleteAnyway, I've seen somewhere else that the blury effect in your game is what is taking 90% of the system ressources (written elsewhere on your blog) while everything else is taking only 10%.

Apparently, despite having 50 times more physics steps per second, the physics still requires less than 10% of the power of a relatively unimportant eye candy. If that's true, that seems to mean optimisation is sometimes really pointless. (unless this is happening because the eye candy is badly optimised...)

I'm mocking around for fun with a destructible worms-like terrain and movement can be a bit tricky to get right, since the terrain is so formless. I think I'm going to move the character a single pixel at a time with a loop. Since the type of game I'm working with doesn't exactly have the blazing speed of Proun, that should work fine.

Yeah, optimisation sometimes just doesn't matter. Proun's gameplay is super simple and the graphics run on the GPU, so there just isn't anything else the CPU could be doing. There is very little point in optimising CPU things in Proun (including collisions).

Delete