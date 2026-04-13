---
title: To multiply with delta time or not to multiply with delta time?
url: http://www.learn-cocos2d.com/2013/10/game-engine-multiply-delta-time-or-not/
author: Colin Humber says
published: '2013-10-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Don’t multiply velocity/position changes with delta time! End of story.

Okay, not quite. There’s a rationale that goes with it. And there are situations where applying delta time is important, if not required - but probably not in the way you’ve been taught by tutorials and fellow developers.

This is important stuff because applying delta time wrongly makes for a bad game experience.

### What is this delta time thing anyway?

If you integrate velocity to a node’s position every frame, you have the option to multiply that velocity with the delta time passed in the update: method. Delta time is simply the time difference between the previous and the current frame.

Actually that is not entirely accurate - delta time is the time difference between the last and current execution of the update: method. This usually occurs every frame, but doesn’t have to be. On a scheduled selector that runs every second, the delta time is - tadaa - one second.

Okay, not even that is accurate. On a scheduled selector that runs every second, delta time is at least one second. It could be slightly more. This can depend on the resolution of the timer and how well one second divides with the time allocated to render a frame, or (as you’ll see later) whether time delta was calculated with the same means as the screen refresh rate.

### What does multiplying with delta time do?

The effect of (not) multiplying a node’s velocity with delta time is as follows, assuming that 60 fps is the maximum achievable framerate as on iOS:

- Don’t multiply with time delta: the node slows down as the framerate drops below 60 fps.
- Multiply with time delta: the node moves the same distance regardless of the framerate.

Multiplying with delta time is often referred to as “framerate independent” (updates, movement, gameplay, etc). In contrast not multiplying with time delta is often called “framerate dependent” (updates, movement, gameplay, etc).

Unfortunately, framerate independent updates are said to be “important” and often taught by fellow game developers without actually teaching the implications, drawbacks and situations where you don’t want to apply delta time. Here’s one key point to take away early:

**Applying delta time only makes a difference when the framerate drops below 60 fps.**

If your game always runs at 60 fps there’s absolutely no point to multiply with time delta. If time delta is only used to combat the effect of short-lasting framerate drops, possibly introduced by system events, you’re doing it wrong.

In this case, and most others too, you’re almost always better off not applying delta time on iOS. And if you do, there’s a whole set of things to consider, including the architecture of both the game and the engine.

### Understanding locked framerates and vertical synchronization

The maximum screen update frequency on iOS devices is 60 Hz (aka 60 fps). An iPhone/iPad device will never render more than 60 images per second. Unlike desktop computers there’s no user setting that can unlock the framerate to go as high as game and device allow.

iOS devices use [vertical synchronization](https://en.wikipedia.org/wiki/Vertical_synchronization#Vertical_synchronization) to update the screen contents at a fixed interval. Put simply, while the screen content’s are updated the contents will not change half-way during a screen refresh. Any updates (ie rendering) occurs between two screen refreshes. This prevents the [screen tearing effect](https://en.wikipedia.org/wiki/Screen_tearing).

Vertical synchronization has another effect: if the engine can’t prepare a framebuffer for display within 0.0166.. seconds (60 Hz) then the device renders the old framebuffer once more, thus skipping a frame. The engine then has to prepare the framebuffer within another 0.0166.. seconds. If this cycle continues the result is a framerate of 30 fps, as the framebuffer is updated only for every other screen refresh cycle.

This means the only framerates possible on an iOS device are framerates resulting from integer numbers divided by the screen refresh rate (60 Hz). The CADisplayLink [frameInterval](https://developer.apple.com/library/ios/documentation/QuartzCore/Reference/CADisplayLink_ClassRef/Reference/Reference.html#//apple_ref/occ/instp/CADisplayLink/frameInterval) property is an integer, not a float, for this very reason.

Thus **on iOS devices you can only ever have these discrete framerates**:

- 60 / 1 =
**60 fps**(delta time: 0.0166.. seconds) - 60 / 2 =
**30 fps**(delta time: 0.0333.. seconds) - 60 / 3 =
**20 fps**(delta time: 0.05 seconds) - 60 / 4 =
**15 fps**(delta time: 0.0666.. seconds) - 60 / 5 =
**12 fps**(delta time: 0.0833.. seconds) - 60 / 6 =
**10 fps**(delta time: 0.1 seconds)

### But my game runs at ~45 fps!

Yes, it doesn’t.

Most framerate counters, and cocos2d’s is no exception, display the **average framerate** over a number of updates. By default at 60 fps cocos2d takes the average of the last 6 frames, ie the counter is updated every 0.1 seconds.

What the fps counter displays as 45 fps is in reality a game that constantly fluctuates between 30 and 60 fps. One frame takes less than 0.0166.. seconds the complete, the next takes a little longer. Repeat ad infinitum and take the average and you get 45 fps.

But **this isn’t the update rate at which your game is running! **It runs at 60 fps one frame, and 30 fps the next. Meaning in one update the delta time will be 0.0166.. and at another it will be 0.0333…

### Delta time may not be exactly 0.0166..

If you log the delta time of a cocos2d-iphone game running at 60 fps you get fluctuating values like these:

|
1 2 3 4 5 6 7 8 |
deltaTime = 0.016574 deltaTime = 0.017026 deltaTime = 0.016425 deltaTime = 0.016939 deltaTime = 0.016299 deltaTime = 0.016665 deltaTime = 0.017033 deltaTime = 0.016618 |

This is a particular issue with cocos2d because it does not use the CADisplayLink duration property. Instead it relies on system timers to calculate the time difference. As a result, cocos2d’s delta time is merely an approximation and ever-so-slightly disconnected from the actual refresh rate. Other game engines may or may not have the same issue.

So in cocos2d games you will inevitably have subtle frame-over-frame variations when multiplying with delta time. This leads to nodes not moving 100% exactly at the same speed frame over frame, but the speed may be 99% in one frame, 101% in another to catch up.

By and large this will not be noticeable, but if you ever wondered why cocos2d delta-time movements don’t look super-smooth, this may be it.

### Allowing the game to slow down is preferable

An iOS device is a gaming console, from a technical perspective. Yes, it does run on a multitasking OS but so do modern consoles.

**Given the fact that your game can only ever run at 60 or 30 fps, your very first goal should be to make damn sure your game always runs at 60 fps (or 30 fps)!**

Yes, system events can cause a sudden drop in framerate. But in such a case, do you want the user to see fewer updates of the game but continue at the same pace, or would you rather have the game slow down?

Say the framerate drops exactly at the moment when the player aligns at the tile edge to make a jump at the very last instance. If the game suddenly slows down, he’ll probably still make the jump. If the framerate drops but the game continues at the same pace, the player’s entity may have moved beyond the tile’s boundaries in the next frame - the player can’t and didn’t make the jump.

There’s a reason why 99% of arcade (2D) console games don’t bother multiplying with time delta. You’ll see almost all of them slow down in congested situations. This is particularly true if you remember the older console games, from NES to Mega Drive. The jump’n runs and shoot’em ups back in the day all slowed down rather than skipping frames.

I’ll explain in the desktop games paragraph below why this is a little different today.

### Negative side-effects of applying delta time

At 30 fps with applied delta time you’re skipping every other frame, respectively you’re advancing your game objects by twice the distance. That may be acceptable, though it will not be a pleasant experience for the player if the game frequently drops to 30 fps and then goes back up to 60 fps. You get a very unsteady framerate and feel.

At 20 fps game objects advance by three times their normal distance, four times at 15 fps and 6 times at 10 fps. So if one game object moves with a speed of 5 points per second along the x axis then at 20 fps you’ll only see it at discrete points 0,15, 30, 45, 60. At 10 fps you’ll see it at 0, 30, 60. Eventually you’ll have to allow the game to slow down, otherwise it will become unfair to the player.

Unfortunately the nature of most hiccups caused by system events is that they eat up all the CPU power in a very short burst. So if a system event comes in, what happens isn’t that your game drops from 60 to 30 fps for an entire second - it’s more likely that your game drops from 60 fps to below 10 fps (or no frames at all!) for just a couple frames.

Say your game is skipping one tenth of a second (10 frames) due to a system event. What happens to your game object moving along the x axis? One frame it was at point 30, the next frame it’s at point 80. This is a huge distance! So huge in fact that it can be an issue that introduces severe bugs like tunnelling through collisions and being able to enter (and never leave) inaccessible areas of the game!

**Multiplying with time delta becomes useless AND dangerous if the framerate drops too low!**

So you always have to safeguard framerate independent updates against very low framerates. In fact below 30 fps the framerate independent update very quickly loses its appeal. And if you then consider you get to have only 60 or 30 fps on iOS - what little good use remains of applying time delta is rendered moot.

At the same time your code complexity grows because you’re not only going to have to multiply with time delta, you will also have to lock time delta to never be greater than a certain threshold, say 0.05 for 20 fps.

### The better solution for 31-59 fps games: lock the framerate to 30 fps

Yes, we all want our games to run as fast as possible. But let’s face it: not all games need 60 fps, and many games that can’t achieve a steady 60 fps are better played at a constant 30 fps.

Especially when in-between framerates are an illusion, as on iOS. Any game that runs at a framerate above 30 but below 60 is actually fluctuating more or less randomly between 60 fps and 30 fps. This can make the experience worse for the player since the game runs at 60 fps for a moment, only to continue at 30 fps for a while, then going back up, then coming down again. Repeat ad infinitum.

Put simply:** Framerates between 31 and 59 fps need to be considered inacceptable! **

You either run at a steady 60 fps and do all the necessary analysis and optimizations on the slowest supported devices to achieve this goal, or you lock the framerate to the next lower integral which would be 30 fps. No moaning and complaining will help you - suck it up or drop it down!

Those close-to-60-fps framerates can be particularly nasty. If you get 55 fps that actually means that every 6th frame doesn’t complete in 0.01666.. seconds. Or worse, that every 12th frame 3 entire frames are skipped. The good news is: you have a pretty good chance at isolating the cause and optimizing it. In particular if you know you’re doing something every n frames and this aligns with an increased delta time in the next frame.

Usually a constant framerate is perceived better, perhaps even smoother than one that is consistently switching between 60 and 30 fps or one where every tenth of a second 2 or more frames are skipped. Because the moment when you get a couple 60 fps frames everything feels super-smooth, which is then interrupted by moments where it doesn’t feel smooth at all. Users notice this difference more than they might with a constant but lower framerate.

Try it yourself. Set CCDirector’s animationInterval to 1/30 if your game is in the 35-50 fps area. Do a test: same version of the game, one unlocked the other locked to 30 fps. Give it to friends and ask them (without explaining the technical difference) which version they like better, which one feels smoother, which one they’d rather play.

PS: don’t try to cheat, you have to set director’s animationInterval to one of the supported framerates (1 divided by 60, 30, 20, 15, 12, 10) of CADisplayLink - otherwise (and at worst, I haven’t checked what cocos2d really does) you could be updating the world 3 times for every two frames, or vice versa.

### Problems with framerate-dependent updates

Framerate dependency isn’t without issues, too.

All is fine at 60 fps. As soon as a frame is missed however, the game slows down to half its normal speed - if only for a single frame.

Like with skipping frames, there is a sudden change in motion. But this time when dropping from 60 to 30 fps the game runs at half the normal speed. This is very obvious, even to games that on average run at 50-55 fps because it means the game is running 10% slower on average.

What I said in the previous paragraph is even more true for framerate-dependent updates: if you can’t achieve 60 fps all the time, it’ll be better to lock the framerate to 30 fps. But now this change midway in development will affect your entire game - locking the framerate to 30 fps means the game written for 60 fps consistently runs at half its normal speed!

So when you make that decision, you will have to double all of your “speed” values to make the game run at the same speed as before. If you decide to drop down to 30 fps it’ll be a little more work for a framerate-dependent game - unless you planned for it by neatly tugging away all gameplay relevant data in a central file so you can easily x2 all the values (or add *2 to the calculations you’re hopefully doing in one central place). But compared to the issues with framerate-independent updates, framerate-dependency isn’t as bad.

Even today, **framerate-dependent gameplay is the de facto standard for 2D games on gaming devices with a locked refresh rate** (meaning: vertical synchronization is always enabled).

The only viable alternative in use today is a fixed-timestep game world with a view that interpolates the world’s state by applying time delta but without changing the world’s state. This is ..

### What desktop (and all “professional”) games do

Basically every desktop computer game must use the framerate-independent approach because the users themselves may disable vertical synchronization through graphics driver tools. But they aren’t using it the way it is taught to iOS developers!

Most moderately complex games employ a game simulation module that is updated at a fixed rate regardless of the framerate. This game simulation is completely separated from the visual side of things, just like [OpenGW](http://opengameworld.com/). Many games can do away with a 30 Hz or even a 10 Hz update rate of the game simulation. The delta time is only applied to the visuals.

What happens is as follows: the game world is updated once every tenth of a second and rendered to the screen in the same frame. The visual side then (linearly) interpolates the current game object’s positions by multiplying their velocity with the delta time for the next 5 frames, until in the 6th frame the game world is updated once more.

It’s as if the game objects continued to move in the same direction at the same speed for one tenth of a second while the game simulation’s state doesn’t change one bit (literally) during that time.

This works very well if the game world updates are fast enough for a given type of game. For example an RTS can do away with 10 Hz updates but a first-person shooter ought to use at least 30 Hz if not more. You can even have split-timing, where positions and weapons are integrated at 60 Hz but auxiliary (possibly expensive) modules like AI and physics are only updated at a 10 Hz rate.

It’s not a coincidence that this approach lends itself well to networked multiplayer games with client-side predictions. The “prediction” aspect isn’t more than simply continuing to apply a remote object’s position and velocity until an updated set of position and velocity is received. Some multiplayer games optimize by keeping a list of previous positions and velocities of remote objects over a period of time in order to more accurately predict and interpolate continuous non-linear movements (ie walking in circles).

By updating the game world at a fixed rate, and only interpolating the view, all of the “tunnelling through collisions” issues can’t happen. Instead you may see an entity’s view slide into or even through a collision, only to be reset a fraction of a second later because the world simulation keeps updating at a constant rate.

You may have seen this effect when bumping into collisions or other players in a “technically less competent” multiplayer game or in high lag situations - the objects seem to be penetrating but frequently reset to their “last known” position.

Furthermore, if the framerate drops below the update rate of the world simulation, the game would automatically slow down if the world simulation’s update is done in the rendering loop, as would normally be the case. So if a single frame takes a very long time to render then the world simulation will also only update once.

We can express this in pseudo-code, note how the automatic framerate-dependent update mode at below 30 Hz does not even need to be expressed explicitly - it is implicit because at framerates below 30 Hz currentTime will be greater than the next world update time:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 |
-(void) gameLoop:(NSTimeInterval)currentTime { if (currentTime >= nextGameWorldUpdateTime) { // game world updates at a fixed 30 Hz (30 times per second) // with fps below 30 fps this block will run every frame nextGameWorldUpdateTime = currentTime + (1.0 / 30.0); [gameWorld simulate]; [renderer drawWorld:gameWorld]; lastTime = currentTime; } else { // update view by interpolating with delta since last world update [renderer drawWorld:gameWorld delta:currentTime - lastTime]; } } |

### Recommendation: don’t apply delta time!

You really only have two valid options:

- Simple approach: don’t apply delta time, allow the game to slow down. This works particularly well on all devices with a locked refresh rate. This should be the standard model for iOS games, and in particular where there’s no separation between view and model.
- Model-View approach: update game world with fixed time step and interpolate view in frames where the world didn’t update. This is mandatory for desktop and multiplayer games, and best practice for any game.

PS: [OpenGW](http://opengameworld.com/) will help you in designing a world model detached from the view.

Applying delta time to both view and game objects is really a bad idea because it will create inconsistencies (if not serious bugs) in your game simulation while not giving users a tangible benefit.

It is more frustrating to miss a jump because you couldn’t possibly know that the next frame the player would no longer be standing on the edge of the tile than compared to maybe missing a jump because the timing suddenly slowed down - but at least then you still have the chance to react!

In 3D games that picture changes, since we’re now “in the world” and slowing down the world breaks the suspension of disbelief more than a low framerate. Though 3D games that don’t employ the Model-View architecture are very rare. Unfortunately the same can not be said about 2D games.

So in general it’s better to allow a 2D/side view/topdown view game to slow down rather than to keep running at the same speed regardless of how much of it is displayed on screen. The opposite is true for 3D games with a 1st/2nd/3rd person perspective but those are almost requiring a model-view architecture to begin with.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I’m curious what brought you to this conclusion. In your Learn cocos2d book in chapter 6 you recommend multiplying by the delta time to ensure the game runs smoothly independent of the frame rate. I don’t disagree with the article, but I’m just wondering what precipitated this when your book says something to the contrary.

Thanks

In a nutshell: more experience. 😉

I did not give this topic much attention until recently. Then I wondered why I came to avoid delta time multiplication. I used it before, but in our first game we just capped delta time multiplication down to 20 or 15 fps to avoid the physics engine from making too significant “jumps”.

Fair enough! I finished reading your Cocos2d book awhile back and am diving into SpriteKit now and wanted to make sure I had all my ducks in a row.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Thanks for this post, How would you lock the framerate to 30 fps in Sprite Kit?

SKView has a frameInterval property, if I understand correctly that throttles how often update: messages are sent to the scene (so it doesn’t necessarily cap frame rate, just how often the scene’s update message gets sent).

I think this theory falls down in gameplay practice.

Imagine a player’s character, let’s call him Mario, is heading towards a ledge, and at that ledge the player needs to jump at just the right time to get to the other side, or he’ll miss the distance required by jumping too early.

If the game slows down right before the jump, for a couple of frames, by your non-delta approach you’re suggesting the player has time to adjust their jump pressing moment so as to still make the jump.

But I don’t think there’s many players could make this kind of adjustment, largely because they’ve committed to when they’re going to press the jump button well prior to this moment, based on their understanding of the pace and timing of Mario towards the ideal jump point.

In other words, regardless of skittish changes to Mario’s progress, they’re already committed to a touch time for the jump, and now going to miss the jump because you’ve not used delta time and Mario’s two frames back from where they’ve anticipated he’d be based on the other framers they’ve been observing of Mario’s rate of movement towards the jump point.

The best possible example of this kind of anticipation by the player might be the old Olympics games.

Take the very first animation of the Long Jump here, by way of example:

http://www.youtube.com/watch?v=TKRkIMgFAfE

If there’s a frame rate hiccup caused by the operating system during the lead up to the jump, of any sort, without DeltaTime you’re asking the player to adjust to that hiccup. Who do you think can do that?

But now, let’s ask a really important question… if a frame rate hiccup occurs at or around the ideal time for the jump, what does iOS do with regards sensing the touch time of the player? Is it “off” due to the system hiccup or is there something at such a level of priority in the touch detection system that regardless of other events the time of the touch is grabbed accurately?

At its lowest level it boils down to either having a little more time to perform the jump (no delta time applied), or simply missing the jump because the next frame has the player forward past the ledge.

Yes it’s difficult if timing is messed up, but not impossible as in the situation with applied delta time. That’s the key difference. It will rarely pan out exactly this way, but the possibility alone is enough to try and avoid it.

Before this I added delta time to my platformer in SpriteKit. When my map loads I get a spike in the framerate and i fall through the floor, is this because I used delta time for objects and view?

Apple use delta time like this in their example:

Is this just to update the view?

Hard to say from here because the actual update happens in updateWithTimeSinceLastUpdate. It depends where and how they use the delta time.

This was very enlightening! Thanks a bunch!

Great aricle, thanks. I read on another blog, this approach based off Microsoft’s XNA framework… If a given draw call takes a bit too long, it will call update repeatedly until it “catches up”. Here’s an adaption written in Swift…

var lastTime: CFTimeInterval = 0.0

override func update(currentTime: CFTimeInterval) {

if (lastTime == 0.0) { lastTime = currentTime }

var accumulatedFrames = round((currentTime - lastTime) * 60.0) // assume updates at 60hz and catch up if we drop below that

lastTime = currentTime // for the next update

// update the world as many times needed to “catch up”

while (accumulatedFrames > 0) {

updateMyWorld()

accumulatedFrames-

}

}

…thoughts?

I wouldn’t do that because it creates exactly the situation that players don’t want: the simulation suddenly skipping a couple frames forward without them being able to react to it. Whether you feed delta time into a step function, or call the step function several times if delta has become too high, is essentially the same thing expressed differently.