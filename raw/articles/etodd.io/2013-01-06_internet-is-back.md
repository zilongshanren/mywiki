---
title: Internet is Back
url: https://etodd.io/2013/01/06/internet-is-back/
published: '2013-01-06'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Internet is Back

I just got internet back after being without it since before Christmas. It was a tearful reunion, to be sure. Turns out, I was actually more productive than usual without internet. There's a one-word explanation for that, and it rhymes with "edit".

ANYway, here's what got done:

### Analytics

When you finish a play session, you'll see something like this:


I haven't figured out the server side of this system yet, but all it really needs to do is accept plain text file uploads. Once I have the files, it's easy to load them into the editor, yielding data like this:


On the right-hand side, you can see how I can view individual play sessions, or select all of them and filter by event type. For example, if I wanted to see where in the map people most often exited in a fit of rage, I could select all the play sessions, then filter on the "Exit" event.

The player's position at the time of each event is visualized as a colored dot. I normalize the first three bytes of the MD5 hash of the event name and use that as the color.

At the bottom you can see I also record graphs of various properties, like the player's health and ammo. I can also just play back the recorded sessions at up to 10x speed. The analytics data also includes crash logs, so now I can see the circumstances leading up to a crash.

**TL;DR:** The next alpha release should give me a lot more useful information about pacing, difficulty, and bugs.

### Headlamp

I'm working on a pitch-black claustrophobic section of the game. Ancient FPS tradition requires that I implement a flashlight.


Complete with shadows and everything!

### SS-Fail-O

I tried to implement SSAO. This is as far as I got:


Sad sad sad.

### Revamped Player Textures

I know, I'm not a very good 3D artist. I've been getting some complaints about it. I'm trying to go back and re-vamp the player model without throwing away hundreds of hours of work. I've already made one of the easiest improvements, which was to photochop the textures a bit and add normal-mapping.

Here's before and after:

### Laundry List

Here's some other things, because you obviously have nothing better to do!

- I've done a good bit of research and writing for the story in the past few weeks. I feel lucky to have a lot of source material to work from. But oh is it still difficult.
- Pistol handling animations have been cleaned up.
- The camera doesn't clip into the environment anymore (for the most part).
- I keep improving voxel performance. It's pretty smooth at this point. There's one last stubborn piece of code I need to cajole onto another thread though.
- I wrote a very simple state-machine AI for the snake enemy. It's so much more fun now, it feels like an actual game.
- I also applied the AI to a new "floater" NPC which will come into play more later.
- I think the player movement and special ability code is finally starting to settle down. I've narrowed things down to the right number of abilities that keep things simple but also give the player a lot of power. Hopefully it will just be tweaks and bug fixes from here on.
- Speaking of bug fixes, I've squashed probably over fifty bugs since Christmas. Feels good man.

Thanks for reading. Hang in there for the next alpha release!