---
title: The story of the non deterministic Replay
url: https://blog.gemserk.com/2016/09/26/the-story-of-the-non-deterministic-replay/
published: '2016-09-26'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

This is the story of how I discovered my simplified replay system wasn’t so deterministic as I believed because I had an ugly bug, but read the post if you want to know where exactly.

While integrating the lockstep engine on the game I am working on, I decided to do something to save and load replays to be able to easily reproduce some bugs I was experimenting. After I had that done and working, it was pretty awesome to see I can replay the same game multiple times (food for another blog post by the way), however, I thought it could be fun and easy to play them faster, why not.

Since I have a fixed time step logic, it should should be pretty straightforward, simply use a multiplied time and then the fixed timestep logic would do all the work and the game logic shouldn’t notice the change. I decided to give it a try and it worked…. almost, when playing the replays at higher speeds I noticed some visual differences but I wasn’t totally sure (it could be interpolation code).

To verify, I went back to the test project, where I had the [moving box](https://blog.gemserk.com/2016/08/30/lockstep-multiplayer-first-steps/), and test it there, but I needed some way to be sure. Since I have already a way to calculate checksums of the game state, I used that to verify the game states when playing replays at different speeds (from 2x to 16x).

It failed, even though it only failed to validate some frames, *following frames were not necessarily invalid* (this is something important to consider).

![invalid-state](../../assets/e94014748f095980.png)

*Image 1: It shows one of the best tools in the world to check game states when replaying a game.*

So, I was right, I saw some differences, I could be sure that something was happening. The thing was, with only the checksums I couldn’t know what the real difference was. Next step, making something to detect it.

In order to do that, I had to change to start saving (at least for debug) the game state, not only the checksum, and to check differences between stored game states in the replay and the current game state (when replaying the game) when checksum validation fails. It worked too, now I have the exact place where the differences are.

*Image 2: It shows why serializing all the game state in one string is the best thing to do in your life.*

After testing it a bit, I noticed another curious thing, the game validation wasn’t always failing given the same replay and the same speed. That gave me a hint that the problem was probably not related with the game code itself (the moving box).

So, if I played the replay at 1x, it was validated properly. If I played the replay at 8x, it failed, most of the time, but not always. So, it seems there is something related with speed I don’t understand yet.

I decided to test the same replay but with Unity timescale modified, my first test was using 1x for replay but 5x for the timescale, validation failed, then the opposite, 10x for replay but 0.1x for timescale, and it worked well. So the problem seems to be related with my accumulator logic inside the fixed timestep logic?

Some test cycles later, it turns out that, it was indeed a bug in one of the core classes of the engine!

The problem was on my class [LockstepFixedUpdate](https://github.com/acoppes/deterministicgame/commit/7639bf1cabfa1715e6f658dcf25febbab3193135), the first version was overriding the Update() method and performing lockstep logic, it worked ok if only at most one fixed update is processed, but in the case a big delta time arrives, it only process lockstep logic once for the first fixed update and never again.

That means that, in case replay commands were to be processed in frame 3, we are in frame 1 and a big dt of 10 frames arrives, then lockstep logic checks only in frame one and never again until all 10 frames were processed. This bug even bypass the lockstep!

Since I made a test to replicate the bug, it was really easy to fix it, I changed to process the lockstep logic with each fixed step updates and it works fine now, I have high speed replays!! YEAH!!

### Conclusion

In the process of finding this bug I started to expand the engine support and create better tools, this is really important if I want to build something solid over it.

The only way to detect issues as soon as possible is to iterate over the engine as soon as possible and to do that, use cases are needed and games provide the best use cases. In my case, I am using not only the game I am trying to make but also other similar games as references when deciding what I want and how I want to test it, for example, having replays, being able to play the replay at different speeds, being able to save the replays, etc. Also, being able to replicate a bug in a small test case where you can iterate quickly to fix it is super useful.

Detecting (and having) problems like this in a small and simple game gives the idea of the complexity of a medium to big game, all the variables and the difficulties, it is not something to underestimate, so when developers say they couldn’t add multiplayer features to their game because it was really hard to do it, it is not a lie.

I love all of this stuff, even though I understand it is not an easy path.

To complete this post, here is a video showing a prototype of how I load and play a replay which was created by playing with two players in LAN, one was my computer and the other was my phone:

The quote of the day is ‘Fail as much as possible, as soon as possible to avoid failing when it is too late’.

Hope you enjoyed the journey.