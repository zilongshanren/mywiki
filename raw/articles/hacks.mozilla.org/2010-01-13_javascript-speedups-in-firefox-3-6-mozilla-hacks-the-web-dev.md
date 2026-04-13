---
title: JavaScript speedups in Firefox 3.6 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/01/javascript-speedups-in-firefox-3-6/
author: Alix Franquet
published: '2010-01-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This post was written by David Mandelin who works on Mozilla’s JavaScript team.*

Firefox 3.5 introduced TraceMonkey, our new JavaScript engine that traces loops and JIT compiles them to native (x86/ARM) code. Many JavaScript programs ran 3-4x faster in TraceMonkey compared to Firefox 3. (See our [previous article](http://hacks.mozilla.org/2009/07/tracemonkey-overview/) for technical details.)

For JavaScript performance in Firefox 3.6, we focused on the areas that we thought needed further improvement the most:

- Some JavaScript code was not trace-compiled in Firefox 3.5. Tracing was disabled by default for Firefox UI JavaScript and add-on JavaScript, so those programs did not benefit from tracing. Also, many advanced JavaScript features were not trace-compiled. For Firefox 3.6, we wanted to trace more programs and more JS features.
- Animations coded with JavaScript were often choppy because of garbage collection pauses. We wanted to improve GC performance to make pauses shorter and animations smoother.

In this article, I’ll explain the most important JS performance improvements that come with Firefox 3.6. I’ll focus on listing what kinds of JS code get faster, including sample programs that show the improvements Fx3.6 makes over Fx3.5.

### JIT for Browser UI JavaScript

Firefox runs JavaScript code in one of two contexts:*content* and *chrome* (no relation to Google Chrome). JavaScript that is part of web content runs in a *content* context. JavaScript that is part of the browser UI or browser add-ons runs in a *chrome* context and has extra privileges. For example, chrome JS can alter the main browser UI, but content JS is not allowed to.

The TraceMonkey JIT can be enabled or disabled separately for content and chrome JS using `about:config`

. Because bugs affecting chrome JS are a greater risk for security and reliability, in Firefox 3.5 we chose to disable the JIT for chrome JS by default. After extensive testing, we’ve decide to enable the JIT for chrome JS by default, something we did not have time to fully investigate for Fx3.5. Turning on the JIT for chrome should make the JS behind the Firefox UI and add-ons run faster. This difference is probably not very noticeable for general browser usage, because the UI was designed and coded to perform well with the older JS engines. The difference should be more noticeable for add-ons that do heavy JS computation.

| Option | Fx3.5 Default | Fx3.6 Default |
|---|---|---|
| javascript.options.jit.chrome | false | true |
| javascript.options.jit.content | true | true |

### Garbage Collector Performance

JavaScript is a garbage-collected language, so periodically the JavaScript engine must reclaim unused memory. Our garbage collector (GC) pauses all JavaScript programs while it works. This is fine as long as the pauses are “short”. But if the pauses are even a little too long, they can make animations jerky. Animations need to run at 30-60 frames per second to look smooth, which means it should take no longer than 17-33 ms to render one frame. Thus, GC pauses longer than 40 ms cause jerkiness, while pauses under 10 ms should be almost unnoticeable. In Firefox 3.5, pause times were noticeably long, and JavaScript animations are increasingly common on the web, so reducing pause times was a major goal for JavaScript in Firefox 3.6.

**Demo: GC Pauses and Animation**

**Demo.**

The spinning dial animation shown here illustrates pause times. Besides animating the dial, this demo creates one million 100-character strings per second, so it requires frequent GC. The *frame delay* meter gives the average time between frames in milliseconds. The *estimated GC delay* meter gives the average estimated GC delay, based on the assumption that if a frame has a delay of 1.7 times the average delay or more, then exactly one GC ran during that frame. (This procedure may not be valid for other browsers, so it is not valid for comparing different browsers. Note also that the GC time also depends on other live JavaScript sessions, so for a direct comparison of two browsers, have the same tabs open in each.) On my machine, I get an estimated GC delay of about 80 ms in Fx3.5, but only 30 ms in Fx3.6.

But it’s a lot easier to see the difference by opening the demo in Fx3.5, watching it a bit, and then trying it in Fx3.6.

In Fx3.5, I see frequent pauses and the animation looks noticeably jerky. In Fx3.6, it looks pretty smooth, and it’s hard for me even to tell exactly when the GC is running.

**How Fx3.6 does it better.** We’ve made many improvements to the garbage collector and memory allocator. I want to give a little more technical details on the big two changes that really cut our pause times.

First, we noticed that a large fraction of the pause time was spent calling `free`

to reclaim the unused memory. We can’t do much to make freeing memory faster, but we realized we could do it on a separate thread. In Fx3.6, the main JS thread simply adds unused memory chunks to a queue, and another thread frees them during idle time or on a separate processor. This means machines with 2 or more cores will benefit more from this change. But even when one core, freeing might be delayed to an idle time when it will not affect scripts.

Second, we knew that in Fx3.5 running GC clears out all the native code compiled by the JIT as well as some other caches that speed up JS. The reason is that the tracing JIT and GC did not know about each other, so if the GC ran, it might reclaim objects being used by a compiled trace. The result was that immediately after a GC, JS ran a bit slower as the caches and compiled traces were built back up. This would be experienced as either an extended GC pause or a brief hiccup of slow animation right after the GC pause. In Fx3.6, we taught the GC and the JIT to work together, and now the GC does not clear caches or wipe out native code, so it resumes running normally right after GC.

### Tracing More JavaScript Constructs

In my [article on TraceMonkey](http://hacks.mozilla.org/2009/07/tracemonkey-overview/) for the Fx3.5 release, I noted that certain code constructs, such as the `arguments`

object, were not traced and did not get performance improvements from the JIT. A major goal for JS in Fx3.6 was to trace more stuff, so more programs can run faster. We do trace more stuff now, in particular:

**DOM Properties.**DOM objects are special and harder for the trace compiler to work with. For Fx3.5, we implemented tracing of DOM methods, but not DOM properties. Now we trace DOM properties (and other “native” C++ getters and setters) as well. We still do not trace scripted getters and setters.**Closures.**Fx3.5 traced only a few operations involving closures (by which I mean functions that refer to variables defined in lexically enclosing functions). Fx3.6 can trace more programs that use closures. The main operation that is still not traced yet is creating an anonymous function that modifies closure variables. But calling such a function and actually writing to the closure variables are traced.We now trace most common uses of the`arguments`

.`arguments`

keyword. “Exotic” uses, such as setting elements of`arguments`

, are not traced.We have improved performance when tracing`switch`

.`switch`

statements that use densely packed numeric case labels. These are particularly important for emulators and VMs.

These improvements are particularly important for jQuery and Dromaeo, which heavily use `arguments`

, closures, and the DOM. I suspect many other complex JavaScript applications will also benefit. For example, we recently heard from the author that [this R-tree library](http://stackulator.com/rtree/) performs much better in Fx3.6.

Here is a pair of demos of new things we trace. The first sets a DOM property in a loop. The second calls a **sum** function implemented with `arguments`

I get a speedup of about 2x for both of them in Fx3.6 vs. Fx3.5.

### String and RegExp Improvements

Fx3.6 includes several improvements to string and regular expression performance. For example, the regexp JIT compiler now supports a larger class of regular expressions, including the ever-popular `w+`

. We also made some of our basic operations faster, like `indexOf`

, `match`

, and `search`

. Finally, we made concatenating sequences of several strings inside a function (a common operation in building up HTML or other kinds of textual output) much faster.

*Technical aside on how we made string concatenation faster:* The C++ function that concatenates two strings S1 and S2 does this: Allocate a buffer big enough to hold the result, then copy the characters of S1 and S2 into the buffer. To concatenate more than two strings, as in JS `s + "foo" + t`

, Fx3.5 simply concatenates two at a time from left to right.

Using the Fx3.5 algorithm, to concatenate N strings each of length K, we need to do N-1 memory allocations, and all but one of them are for temporary strings. Worse, the first two input strings are copied N-1 times, the next one is copied N-2 times, and so on. The total number of characters copied is K(N-1)(N+2)/2, which is O(N^2).

Clearly, we can do a lot better. The minimum work we can do is to copy each input string exactly once to the output string, for a total of KN characters copied. Fx3.6 achieves this by detecting sequences of concatenation in JS programs and combining the entire sequence into one operation that uses the optimal algorithm.

Here are a few string benchmarks you can try that are faster in Fx3.6:

### Final Thoughts and Next Steps

We also made a lot of little improvements that don't fit into the big categories above. Most importantly, Adobe, Mozilla, Intel, Sun, and other contributors continue to improve *nanojit*, the compiler back-end used by TraceMonkey. We have improved its use of memory, made trace recording and compiling faster, and also improved the speed of the generated native code. A better *nanojit* gives a boost to all JS that runs in the JIT.

There are two big items that didn't make the cut for Fx3.6, but will be in the next version of Firefox and are already available in nightly builds:

**JITting recursion.**Recursive code, like explicit looping code, is likely to be hot code, so it should be JITted. Nightly builds JIT directly recursive functions. Mutual recursion (g calls f calls g) is not traced yet.**AMD x64 nanojit backend.**Nanojit now has a backend that generates AMD x64 code, which gives the possibility of better performance on that plaform.

And if you try a nightly build, you'll find that many of these demos are already even faster than in Fx3.6!

## 85 comments

fabriceJanuary 13th, 2010 at 10:37Dave MandelinJanuary 13th, 2010 at 18:17Nice TryJanuary 13th, 2010 at 10:47sep332January 13th, 2010 at 10:51ZorkzeroJanuary 13th, 2010 at 11:17Dave MandelinJanuary 13th, 2010 at 18:22ZorkzeroJanuary 14th, 2010 at 07:45Jamie PenneyJanuary 24th, 2010 at 14:16MaxJanuary 24th, 2010 at 15:14Ted MielczarekJanuary 13th, 2010 at 11:42BorisJanuary 13th, 2010 at 12:57TNOJanuary 13th, 2010 at 13:58Alex VincentJanuary 13th, 2010 at 15:14Alix FranquetJanuary 13th, 2010 at 16:13DrazickJanuary 13th, 2010 at 17:16DavidJanuary 13th, 2010 at 17:59QuestionJanuary 13th, 2010 at 22:31TranscontinentalJanuary 14th, 2010 at 00:47GervJanuary 14th, 2010 at 04:10Neil RashbrookJanuary 14th, 2010 at 04:19Ciprian MustiataJanuary 14th, 2010 at 04:32FabJanuary 14th, 2010 at 07:01BorisJanuary 14th, 2010 at 09:07BorisJanuary 14th, 2010 at 09:11Kelly ClowersJanuary 14th, 2010 at 20:02MarkJanuary 16th, 2010 at 07:59RicardoJanuary 16th, 2010 at 12:23nemoJanuary 19th, 2010 at 11:39HansterJanuary 19th, 2010 at 19:39mawryaJanuary 19th, 2010 at 21:56SunJanuary 21st, 2010 at 14:25WiritpolJanuary 21st, 2010 at 20:07mynthonJanuary 22nd, 2010 at 11:59Marko MacekJanuary 23rd, 2010 at 05:08Mark HoltonJanuary 24th, 2010 at 01:23gwenhwyfaerJanuary 24th, 2010 at 06:51gwenhwyfaerJanuary 24th, 2010 at 06:52Jimboooo!January 24th, 2010 at 08:24DavidJanuary 25th, 2010 at 17:38MicJanuary 24th, 2010 at 16:30onurJanuary 25th, 2010 at 12:00DimitrsJanuary 26th, 2010 at 06:50tsphand1January 28th, 2010 at 01:49ChrisJanuary 28th, 2010 at 14:54Vijay RayapatiJanuary 29th, 2010 at 04:10Sasha ChedygovJanuary 30th, 2010 at 14:13FJanuary 30th, 2010 at 08:31defaultJanuary 31st, 2010 at 12:04PascalFebruary 2nd, 2010 at 08:46blehFebruary 2nd, 2010 at 20:35ZiruMarch 1st, 2010 at 11:36rajMarch 15th, 2011 at 05:55nickMay 8th, 2010 at 13:34GaryMay 27th, 2010 at 10:27GaryMay 27th, 2010 at 10:38Christopher BlizzardMay 27th, 2010 at 10:42GaryJune 2nd, 2010 at 07:00Sadiq nasiryJuly 1st, 2010 at 00:07massschneiderJuly 29th, 2010 at 08:15JeffzAugust 28th, 2010 at 14:20JeffzAugust 28th, 2010 at 14:22max jonesOctober 29th, 2010 at 06:32psalmsninetyoneNovember 1st, 2010 at 22:49jhonMarch 17th, 2011 at 13:47BMorrisMarch 23rd, 2011 at 03:58ChrisMarch 30th, 2011 at 17:22