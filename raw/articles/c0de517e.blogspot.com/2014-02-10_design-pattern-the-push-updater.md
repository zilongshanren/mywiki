---
title: 'Design Pattern: The Push Updater'
url: http://c0de517e.blogspot.com/2014/02/design-pattern-push-updater.html
published: '2014-02-10'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just kidding.

Let me tell you a story instead. Near the end of



[Space Marines](http://en.wikipedia.org/wiki/Warhammer_40,000:_Space_Marine)we were, as it often happens at these stages, scrambling to find the extra few frames per second needed for shipping (I maintain that a project should be shippable from start to the end, or close, but I digress).
Now, as I did such a good job (...) at optimizing the GPU side of things it came to a point where the CPU was our bottleneck, and on rendering we mostly were bound by the numbers of material changes we could do per frame (quite a common scenario). Turns out that we couldn't afford our texture indirections, that is, to traverse per each material the pointers that led to our texture classes which in turn contained pointers to the actual hardware textures (or well, graphics API textures). Bad.



Most of the trashing happened in distant objects, so one of the solutions we tried was to collapse the number of materials needed in LODs. We thought of a couple of ways in which artists could specify replacement materials for given ones in an object, collapsing the number of unique materials needed to draw an LOD (thus making the process easier than manual editing of the LODs). Unfortunately it would have required some changes in the editor which were too late to do. We tried something alongside of the idea of baking textures to vertex colors in the distance (a very wise thing actually) but again time was too short for that. Multithreading the draw thread was too risky as well (and on consoles we were already saturating the memory BW so we wouldn't get any better by doing that).



In the end we managed to find a decent balance sorting stuff smartly, asking for a lot of elbow grease from the artists (sorry) and doing lots of other rearrangements of the data structures (splitting by access, removing some handles and so on), we ended up shipping a solid 30fps and were quite happy.



A decent trick is to cache the frequently-accessed parts of an indirection, together with a global counter that signals when any of the objects of that kind changed and a local copy of the counter. If you saw no changes (local copy of the counter equals global) you can avoid following the indirection and use the local cache instead... This can get more complex by having a small number of counters instead of just one, hashing the objects into buckets somehow, or keeping a full record of the changes that happened and have a way for an object to see if its indirection was in the list of changed things... We did some smart stuff, but that was still a sore point. Indirections. These bastards.

So, wrapping up the project we went to the drawing board and started tinkering and writing down plans for the next revision of the engine. We estimated that without these indirections we could push 40% more objects each frame. But why do you have these to begin with? Well, the bottom line is that you often want to update some data that is shared among objects. In case of the textures the indirection served our reference counting system which was used to load and unload them, hot-swapping during development and streaming in-game.



Here comes the "push pattern" to the rescue. The idea is simple, instead of going through an indirection to fetch the updated data, create an object (you can call it UpdateManager and create it with a Factory and maybe template it with some policies, if that's what turns you on) that will store the locations of all the copies of a piece of data (sort of like a database version of a garbage collector), so every time you need to make a copy or destroy a copy you register this fact. Now if create/destroy/updates are infrequent compared to accesses, having copies all around instead of indirections will significantly speed up the runtime, while you can still do global updates via the manager by



**poking the new data in all the registered locations**.
A nifty thing is that the manager could even sort the updates to be propagated by memory location, thus pushing many updates at once with potentially less misses. This is basically what we do in some subsystems in an implicit way. Think about culling for example, if you have some bounding volumes which contain an array of pointers to objects, and as these bounding volumes are found visible you append the pointers to a visible object list, you're "pushing" an (implicit) message that said objects were found visibile...

## No comments:

Post a Comment