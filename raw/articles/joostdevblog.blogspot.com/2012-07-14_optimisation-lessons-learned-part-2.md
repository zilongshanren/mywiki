---
title: Optimisation lessons learned (part 2)
url: http://joostdevblog.blogspot.com/2012/07/optimisation-lessons-learned-part-2.html
author: Joost van Dongen
published: '2012-07-14'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Last week](http://joostdevblog.blogspot.nl/2012/07/optimisation-lessons-learned-part-1.html)I talked about some rather general things that I learned about CPU optimisation, when spending a lot of time improving the framerates of

[Awesomenauts](http://www.awesomenauts.com/),

[Swords & Soldiers](http://www.swordsandsoldiers.com/), and even

[Proun](http://www.proun-game.com/). Today I would like to discuss some more practical examples of what kind of optimisations are to be expected.

Somehow I like talking about optimisation so much that I couldn't fit it all in today's blogpost, so topics around threading and timing will follow next week. Anyway, forward with today's "lessons learned"!

**Giant improvements are possible (at first)**

The key point of my previous blogpost was that you should not worry too much about optimisation early in the project. A fun side-effect of not caring about performance during 'normal' development, is that you are bound to waste a lot of framerate in really obvious ways. So once you fire up the profiler for the first time on a big project, there will always be a couple of huge issues that give giant framerate improvement with very little work.

For example, adding a memory manager to Swords & Soldiers instantly brought the framerate from 10fps to 60fps. That is an extreme example of course, and it only worked this strongly on the Wii (apparently the Wii's default memory manager is really slow compared to other platforms). Still, during the first optimisation rounds, there is bound to always be some low-hanging fruit, ready to be plucked.

The real challenge starts when all the easy optimisations have been done and you still need to find serious framerate improvements. The more you have already done, the more difficult it becomes to do more.

**Big improvements are in structure, not in details**

Before I actually optimised anything, I thought optimisation would be about the details. Faster math using SIMD instructions, preventing L2 cache misses, reducing instruction counts by doing things slightly smarter, those kinds of things. In practice, it turns out that there is much more to win by simply restructuring code.

A nice example of this, is looking for all the turrets in a list of 1,000 level objects. Originally it might make most sense to just iterate over the entire list and check which objects are turrets. However, when this turns out to be done so often that it reduces framerate, it is easy enough to make an extra list with only the turrets. Sometimes I need to check all level objects, so turrets are now in both lists, and when just the turrets are needed, the longer list doesn't need to be traversed any more. Optimisations like this are really simple to do and can have a massive impact on performance.

This is also a nice example of last week's rule that "

*Premature optimisation is the root of all evil*": having the same object in two lists is more easy to break, for example by forgetting to remove the turret from the other list when it is destroyed. In fact, the rare bug with purple screens that sometimes happens in Awesomenauts on console recently turned out to be caused by exactly this! (Note that the situation was extremely timing specific: this only happened when host migration had happened just before a match was won.)

In my experience, it is quite rare to find optimisations that don't make code at least a little bit more complex and more difficult to maintain.

**Platforms have wildly different performance characteristics**

This is quite a funny one. I thought running the same game on different platforms would have roughly the same performance characteristics. However, this turned out to not be the case. I already mentioned that the default memory manager is way slower on the Wii than on any of the other platforms I worked with, making implementing my own memory manager more useful there than elsewhere. Similarly, the copying phase of my multi-threading structure (which I previously discussed

[here](http://joostdevblog.blogspot.nl/2012/03/question-how-to-synchronise-between.html)) takes a significant amount of time on the Playstation 3, but is hardly measurable when I run the exact same code on a PC.

So far I have seen that all the optimisations I have done have improved the framerate on different platforms with wildly differing amounts. They did always improve the performance on all platforms at least a bit, just not with the same amounts. So I think it is really important to try to always profile on the platform that actually has the worst performance problems, so that you can focus on the most important issues.

**Truly low-level optimisations are horribly difficult**

The final lesson that I would like to share today is actually a negative one, and cause for a little bit of shame on my side. I have tried at several occasions, but I have hardly ever been able to achieve measurable framerate improvements with low-level optimisations.

I have read a lot of articles and tutorials about this for various platforms. I tried all kinds of things. To avoid cache misses, I have tried using intrinsics to tell the CPU which memory I would need a little bit later. I have tried avoiding virtual function calls. I have tried several other similar low-level optimisations that are supposedly really useful, but somehow I have never been able to improve the framerate this way. The only measurable result I ever got this way was a 1% improvement by making a set of functions available for inlining (the Playstation 3 compiler does not have Whole Program Optimisation to do this automatically in more complex cases).

Of course, this definitely does not mean that low-level optimisations are impossible, it just means that I consider them a lot more complex to get results with. This also means that it is possible to make a larger project like Awesomenauts run well enough without any low-level optimisations.

We've got a big announcement coming up next week, and next weekend I will be back with the last part of my mini-series on optimisation. Stay tuned!

*(Muhaha, are you curious what we are going to announce? Feel free to speculate in the comments!)*

"A nice example of this, is looking for all the turrets in a list of 1,000 level objects. Originally it might make most sense to just iterate over the entire list and check which objects are turrets"





ReplyDeleteOuch, that just made my brain hurt :(. Well, I guess that just goes to show it's a good thing I'm not in industry. Joking aside, what can we learn from this one?

There are, what, 10 turrets out of 1000 objects? That means checking the entire list has serious overhead versus being able to iterate over just the turrets. But if you do it only once per frame, then the overhead _per frame_ is maybe negligible.

You --I'm going to say 'you', but I guess that means 'somebody at Ronimo'-- ended up changing it. So at some point this got on your radar? Did you end up getting more performance? (You did get more bugs, assuming your initial implementation had no bugs.)

Was it worth it? Could you have known in advance? Should you have done the more complicated solution to begin with? Are you glad that you didn't? I ask this non-rethorically.

See, once you even start to think like that, you're getting ready to go down that road to hell (the one that's paved with good intentions). No, you should NOT have done the more complicated solution to begin with. Yes, that example may have sounded like an obvious place that cycles would have been wasted -- but what he didn't mention in the story are the twenty other places in the code where he did things "the slow way" that turned out to have absolutely no measurable effect on performance.


DeleteIf you do the more complicated solution to begin with, then you have added 20 times more complexity to your code than you needed. Nor can you easily go back and simplify your code, because you don't have any quick way to find out which one of the twenty is the one that you actually needed.

I totally agree with Brian that doing these kinds of things beforehand is a bad idea, because there are so many of them and so many turn out not to matter.





DeleteOften it goes something like this:

1. I need to count the number of active turrets once per frame to see which team is winning. This does not impact performance much, so I do it the simple way.

2. Our AI designer wants to know how many turrets his own team still has and gets a logic block to query that. I reuse the turret-counting function I already had.

3. Our AI designer uses this block 100 times per AI tick (seriously, he does these kinds of things!).

4. The profiler tells me 5% of all the time is spent on counting turrets.

5. I optimise and see that the 5% turns into 0.01%.

The alternative path is that the list was really short when I built the turret counter, so storing turrets separately wasn't of use then. During development the list becomes 100x bigger and no one remembers the turret counting. Then at some point it turns up in the profiler. This really happens: the level objects list in Awesomenauts easily has over 5000 objects per level, and started out with 50 early in development.

So optimisations like this are in my case always based on the profiler and quite often get a 5% or more performance boost. That's a lot for something as simple as this!

An important remark here is that I am quite experienced with performance now, so I know for example that iterating long lists many times per frame is a bad idea, and I have a feeling for what 'long list' and 'many times per frame' mean. So I sometimes fire up the profiler immediately after making something, when I think I am doing something that decreases the framerate immediately.

Very reasonable scenario. So how about the logic block caches the count? Is that what you actually did?

DeleteI didn't cache it just for the logic block. If there is one thing that is really easy to introduce bugs with, than it is caching. When you delete a turret in the middle of a frame, you need to know about all the caches and update them. That is possible, of course, and there are structures to make that less easy to get bugs, but it is pretty complex. At least the separate list of turrets is next to the list of level objects, in the same class. That makes it relatively easy to understand the situation.

DeleteCould you say more about not getting performance from avoiding virtual function calls? Is there something you tried there? It seems to me like this is mostly an architectural aspect that can't easily be hacked into something.



ReplyDeleteThat is, this seems like something where some initial 'optimisation' could actually be important; setting up your architecture so that it uses virtuals all over the place even though it doesn't have to would be (premature?) pessimisation :P.

This assumes virtual function calls actually impact performance. I have heard it suggested that it doesn't actually matter much in most reasonable cases on modern hardware. On the other hand, if I recall correctly, virtual function calls ARE super terrible on PowerPC, that is, Xbox. I think Olaf told me something to that effect at some point.

I strongly disagree with the message in your reply: virtuals are a good thing! They are one of the key aspects of object oriented design and an important way to prevent complex relationships between too many classes. Of course, when they are not needed, adding them randomly is bogus. But using less virtuals because of performance is a really bad idea. Making a good object oriented design for something as complex as Awesomenauts is incredibly difficult already without these kinds of bogus limitations.




DeleteHowever, since so many people told me virtuals were a bad idea, I made sure my inner rendering loop contains few (only spot in the code where I cared for this). It does contain a couple, though, but I know that in practice 98% of the time it calls one specific implementation and the profiler said this took some time. So what I tried that had no effect was doing something like this:

if (object->getType() == RECT)

{

static_cast(object)->doNonVirtualStuff();

}

else

{

object->doVirtualStuff();

}

No measureable performance difference, even when doing this 5000 times per frame. I guess the added complexity spent as much time as the virtual, or maybe virtuals are just cheaper than people say. This was on the PPU of the PS3, by the way.

I'm not saying virtuals are a bad thing. I'm saying virtuals can be a costly thing (though in most cases that won't matter).





DeleteRolling your own runtime method dispatch would probably just be worse. (In your optimisation attempt: more complex code, no better performance.) You're paying for the indirection, not for keyword virtual.

Look, I guess the reason I get hung up on these things is that most of my recent reading on C++ was about the implementation of really low-level stuff like smart pointers. Those really should not lug around big vtables and do runtime dispatch. Most 'non-library' methods just don't called that much, I guess.

That could be fun to know: what's the maximum amount a single method gets called per frame in, say, Awesomenauts? What (kind of) method is it?

It's been mentioned that a lot of code is might surprise you by not begin hot. Do you remember any code surprising you by being hot?

I have no idea how often specific functions are being called. I generally just look at the CPU time percentage in the profiler, not at the number of calls.


DeleteI can't really think of any particular things that surprised me to be slower than expected, actually. In general the really slow things, are spots were lists are traversed too often (usually this should have been maps instead), or where strings are constructed and destructed too often (inside a for-loop, for example).

Joost how do you look at this from a design point of view?




ReplyDeleteFor example you mention you increased fps from 10 to 60 at a certain stage. But if it was at 10 before that would seriously hinder proper playtesting and design. When designing levels or gameplay I continiously play the game. If that doesn't run properly it is almost impossible to do. I'd even say that if the game doesn't run at the desired final fps it limits a designer. Sounds like whining maybe, but I truely believe that.

Also during development of ibb and obb we have showcased the game at many different events. Often last minute requests came in and this sometimes let to not optimal builds at these events. (I still need to figure out a way to deal with this for later projects.)

How do you feel about this? Do you guys build seperate playtest or event builds sometimes?

I totally see your point, and I agree that evolving gameplay when the game is not properly playable is impossible.





DeleteHowever, we have a very simple solution to that. Our engine is set up so that everything looks and plays the exact same on console and PC, and all art and gameplay development is done on PC. Only console-specific things are made on devkits.

The trick now is that with the power of current PC's, if a Playstation 3 runs the game at 10fps, than a €600 PC will easily run it at 60fps (much more, actually). So we can playtest and showcase the game on PC. We have presented Awesomenauts at several consumer events and always just used PCs with console controllers. No problem.

If, however, the performance gets so low that it is unplayable on our development PCs, then we start optimising immediately. Playability is super-important at all times.

As for separate builds for showcasing the game: we always try to make the build for a show one week before, and we extensively test that and fix bugs to make it good enough. We also disable features that we don't want to show or that are too broken. After that, the build for the show is stored en we just continue development as normal. So we rarely have last-minute features at shows, since the risk of a broken build is too big that way. (In practice our planning sometimes goes wrong, of course, but in theory this is a sound plan... ;) )

Thanks, all makes sense : )

DeleteIt's really interesting to know how you optimized your game for PS3. Did you offload PPU by running some logic on SPU? And if yes, what logic exactly? (e.g physics, animations, etc)

ReplyDeleteWe didn't do anything for SPU specifically, since that is a lot of work and research to get that to work well, and those optimisations would probably not benefit the 360 and PC versions without extra work.



DeleteAlso, not everything is a good idea to do on SPUs and most of the work done in our game doesn't lend itself well for SPUs. They are really good at doing massive math, but less at updating our animation system.

The standard PS3 libraries do part of the rendering work and the sound on SPUs, though, so we do have that.