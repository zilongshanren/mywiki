---
title: Fast Paths
url: http://hacksoflife.blogspot.com/2010/01/fast-paths.html
author: Benjamin Supnik
published: '2010-01-14'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

- When
*designing*an API, you might ask: how do we prevent a slow-down in the fastest possible path? - When
*implementing*an API, you might ask: how does this affect overall performance?

A well optimized OpenGL client program would not do this:

`glEnable(GL_TEXTURE_2D);`

glDrawArrays(GL_TRIANGLES, 0, 51);

glEnable(GL_TEXTURE_2D);

glDrawArrays(GL_TRIANGLES, 108, 51);



The second enable of texturing is totally unneeded. The clever programmer would optimize this away. But what does the OpenGL implementation do? We have two choices:- Check the texture enable state before doing a glEnable. In the case where the programmer didn't optimize, this saves an expensive texture state change, and in the case where the programmer did optimize, it is an unnecessary comparison, probably of one bit.
- Do not check - always do the enable. In the case where the programmer didn't optimize, the program is slow; in the case where the programmer did optimize, we deliver the fastest path.

(In a real program, detecting duplicate state change is very difficult, since code flow can be dynamic. For example, in X-Plane we draw only what is on screen. Since the model that was drawn just before your model will change with camera angle, the state of OpenGL just before we draw will vary a lot.)

From my perspective as a developer who tries to write really fast code, I don't care which one a library writer chooses, as long as the library clearly declares

*what*is fast and what is not.

This was the motivation behind the "datarefs" APIs in the X-Plane SDK: a dataref is an opaque handle to a data source, and we have two sets of operations:

- "Finding" the dataref, where the link is made from the permanent string identifier to the opaque handle. This operation is officially "slow" and client code is expected to take steps to avoid finding datarefs more than necessary, in performance critical locations, in loops, etc. (Secretly finding was linear time for a while and is now log time, so it was never
*that*slow. ) - Reading/writing the dataref, where data is transferred. This operation is officially "fast"; Sandy and I keep a close eye on how much code happens inside the dataref read/write path and forgo heavy validation. The motivation here is: we're not going to penalize well-written performance-critical plugins with validation on every write because other plugins are badly written. Instead the failure case is indeterminate behavior, including but not limited to program termination. (I'm not ruling out
[nasal demons](http://catb.org/jargon/html/N/nasal-demons.html)either!)

A simple example: case statements. Case statements have this nasty behavior that they will "flow through" to the next statement if break is not included. 99% of the time, this is a programmer error, and it would be nice (most of the time) if the language disallowed it. But then we would lose this fast path:

`switch(some_thingie) {`

case MODE_A:

do_some_stuff();

case MODE_B:

do_shared_behavior();

}


In this case, where we want specialized behavior and then common behavior in mode A, but only the common behavior in mode B, flow-through lets us write ever so slightly more optimal code.If this seems totally silly now, in a world where optimizers regularly take our entire program, break them down into subatomic particles, and then reconstitute them as chicken nuggets, we have to remember that C was designed in the 70s on machines where the compiler barely could run on the machine due to memory constraints; if the programmer didn't write C to produce optimal code, there wasn't going to be any optimal code.

Nice article, but the statement "we want specialized behavior and then common behavior in mode B, but only the common behavior in mode A" has A and B reversed.

ReplyDeleteFixed, thanks Judge.

ReplyDelete