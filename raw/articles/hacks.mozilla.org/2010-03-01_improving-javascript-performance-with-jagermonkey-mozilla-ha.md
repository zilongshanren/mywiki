---
title: improving JavaScript performance with JägerMonkey – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2010/03/improving-javascript-performance-with-jagermonkey/
author: Christopher Blizzard
published: '2010-03-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In August 2008, Mozilla introduced [TraceMonkey](http://weblogs.mozillazine.org/roadmap/archives/2008/08/tracemonkey_javascript_lightsp.html). The new engine, which we shipped in Firefox 3.5, heralded a new era of performance to build the next generation of web browsers and web applications. Just after the introduction of our new engine Google introduced V8 with Chrome. Apple also introduced their own engine to use in Safari, and even Opera has a new engine that they’ve introduced with their latest browser beta.

As a direct result of these new engines we’ve started to see new types of applications start to emerge. People experimenting with [bringing Processing to the web](http://processingjs.org/), people experimenting with [real-time audio manipulation](http://vocamus.net/dave/?p=974), [games](http://benfirshman.com/projects/jsnes/) and many other things. (For some good examples have a look at our list of [Canvas demos](http://hacks.mozilla.org/category/canvas/).)

We’ve learned two things at Mozilla about how our JavaScript engine interacts with these new applications:

- That the approach that we’ve taken with tracing tends to interact poorly with certain styles of code. (That NES game example above, for example, tends to perform very badly in our engine – it’s essentially a giant switch statement.)
- That when we’re able to “stay on trace” (more on this later) TraceMonkey wins against every other engine.

Mozilla’s engine is fundamentally different than every other engine: everyone else uses what’s called a “method-based JIT”. That is, they take all incoming JS code, compile it to machine code and then execute it. Firefox uses a “tracing JIT.” We interpret all incoming JS code and record as we’re interpreting it. When we detect a hot path, we turn that into machine code and then execute that inner part. (For more [background on tracing, see this post on hacks from last year](http://hacks.mozilla.org/2009/07/tracemonkey-overview/).)

The downside of the tracing JIT is that we have to switch back and forth between the interpreter and the machine code whenever we reach certain conditions. When we have to jump back from machine code to the interpreter this is what we call being “knocked off trace.” The interpreter is, of course, much slower than running native machine code. And it turns out that happens a lot – more than anyone expected.

So what we’re doing in our 2nd generation engine is to combine the best elements of both approaches:

- We’re using some chunks of the WebKit JS engine and building a full-method JIT to execute JavaScript code. This should get us fast baseline JS performance like the other engines. And most important, it will be consistent – no more jumping on and off trace and spending a huge amount of time in interpreted code.
- We’ll be bolting our tracing engine into the back of that machine code to generate super-fast code for inner loops. This means that we’ll be able to still have the advantages of a tracing engine with the consistency of the method-based JIT.

This work is still in the super-early stages, to the point where it’s not even worth demoing, but we thought it would be worth posting about so people understand the basics of what’s going on.

You can find more information about this on [David Mandelin](http://blog.mozilla.com/dmandelin/2010/02/26/starting-jagermonkey/)‘s and [David Anderson](http://www.bailopan.net/blog/?p=683)‘s weblogs as well as the [project page for the the new engine](https://wiki.mozilla.org/JaegerMonkey).

## 25 comments

Natanael LMarch 1st, 2010 at 14:33YMarch 1st, 2010 at 14:47JulianMarch 1st, 2010 at 14:53Christopher BlizzardMarch 1st, 2010 at 14:43Robert StuartMarch 1st, 2010 at 15:18KlausMarch 1st, 2010 at 15:43Markus PoppMarch 1st, 2010 at 16:34Chris AinsleyMarch 1st, 2010 at 18:23WulfTheSaxonMarch 1st, 2010 at 19:29PhilMarch 2nd, 2010 at 02:22BWRicMarch 2nd, 2010 at 03:17Christopher BlizzardMarch 2nd, 2010 at 14:20Magne AnderssonMarch 7th, 2010 at 04:27Magne AnderssonMarch 7th, 2010 at 04:29mARK tWAINMarch 3rd, 2010 at 08:26jojoMay 7th, 2011 at 14:20Sarah SpicerMay 29th, 2011 at 10:10louisremiMay 30th, 2011 at 02:54Pablo CuadradoJune 15th, 2011 at 13:12