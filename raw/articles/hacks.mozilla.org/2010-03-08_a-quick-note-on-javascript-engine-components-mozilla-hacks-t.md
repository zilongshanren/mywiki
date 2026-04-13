---
title: a quick note on JavaScript engine components – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2010/03/a-quick-note-on-javascript-engine-components/
author: Christopher Blizzard
published: '2010-03-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There have been a bunch of posts about the [JägerMonkey (JM) post](http://hacks.mozilla.org/2010/03/improving-javascript-performance-with-jagermonkey/) that we made the other day, some of which get things subtly wrong about the pieces of technology that are being used as part of Mozilla’s JM work. So here’s the super-quick overview of what we’re using, what the various parts do and where they came from:

1. **SpiderMonkey.**This is Mozilla’s core JavaScript Interpreter. This engine takes raw JavaScript and turns it into an intermediate bytecode. That bytecode is then interpreted. SpiderMonkey was responsible for all JavaScript handling in Firefox 3 and earlier. We continue to make improvements to this engine, as it’s still the basis for a lot of work that we did in Firefox 3.5, 3.6 and later releases as well.

2. **Tracing.** Tracing was added before Firefox 3.5 and was responsible for much of the big jump that we made in performance. (Although some of that was because we also improved the underlying SpiderMonkey engine as well.)

This is what we do to trace:

- Monitor interpreted JavaScript code during execution looking for code paths that are used more than once.
- When we find a piece of code that’s used more than once, optimize that code.
- Take that optimized representation and assemble it to machine code and execute it.

What we’ve found since Firefox 3.5 is that when we’re in full tracing mode, we’re really really fast. We’re slow when we have to “fall back” to SpiderMonkey and interpret + record.

One difficult part of tracing is generating code that runs fast. This is done by a piece of code called **Nanojit**. Nanojit is a piece of code that was originally part of the **Tamarin** project. Mozilla isn’t using most of Tamarin for two reasons: 1. we’re not shipping ECMAScript 4 and 2. the interpreted part of Tamarin was much slower than SpiderMonkey. For Firefox 3.5 we took the best part – Nanojit – and bolted it to the back of SpiderMonkey instead.

Nanojit does two things: it takes a high-level representation of JavaScript and does optimization. It also includes an assembler to take that optimized representation and generate native code for machine-level execution.

Mozilla and Adobe continue to collaborate on Nanojit. Adobe uses Nanojit as part of their ActionScript VM.

3. **Nitro Assembler.** This is a piece of code that we’re taking from Apple’s version of webkit that generates native code for execution. The Nitro Assembler is very different than Nanojit. While Nanojit takes a high-level representation, does optimization and then generates code all the Nitro Assembler does is generate code. So it’s complex, low-level code, but it doesn’t do the same set of things that Nanojit does.

We’re using the Nitro assembler (along with a lot of other new code) to basically build what everyone else has – compiled JavaScript – and then we’re going to do what we did with Firefox 3.5 – bolt tracing onto the back of that. So we’ll hopefully have the best of all worlds: SpiderMonkey generating native code to execute like the other VMs with the ability to go onto trace for tight inner loops for even more performance.

I hope this helps to explain what bits of technology we’re using and how they fit into the overall picture of Firefox’s JS performance.

## 33 comments

soumynanoMarch 8th, 2010 at 15:08Magne AnderssonMarch 8th, 2010 at 15:12BorisMarch 8th, 2010 at 15:33Magne AnderssonMarch 8th, 2010 at 16:02DrazickMarch 8th, 2010 at 16:01AnonymousMarch 8th, 2010 at 16:04BorisMarch 8th, 2010 at 16:13Magne AnderssonMarch 8th, 2010 at 17:04SloboMarch 8th, 2010 at 16:21BorisMarch 8th, 2010 at 17:56PaulMarch 8th, 2010 at 20:34Richard BarrellJuly 15th, 2010 at 03:26jpvincentMarch 9th, 2010 at 02:07Mark Lee SmithMarch 9th, 2010 at 02:23chrisMarch 9th, 2010 at 07:53JuhaMarch 9th, 2010 at 08:29TristanMarch 9th, 2010 at 11:14BorisMarch 9th, 2010 at 14:47BorisMarch 9th, 2010 at 14:58njnMarch 9th, 2010 at 19:45bobMarch 10th, 2010 at 05:05JunebugMarch 10th, 2010 at 08:31DanMarch 10th, 2010 at 18:44AndrewMarch 10th, 2010 at 18:47OskarMarch 10th, 2010 at 19:22BorisMarch 10th, 2010 at 20:14Erik HarrisonMarch 10th, 2010 at 23:17Brandon jonesMarch 13th, 2010 at 15:17njnMarch 14th, 2010 at 21:32BorisMarch 15th, 2010 at 06:33StifuMarch 16th, 2010 at 07:04DissertationsJune 12th, 2011 at 02:43