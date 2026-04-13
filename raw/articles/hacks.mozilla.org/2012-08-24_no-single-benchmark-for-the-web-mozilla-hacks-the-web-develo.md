---
title: No Single Benchmark for the Web – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/08/no-single-benchmark-for-the-web/
author: Alon Zakai
published: '2012-08-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Google released a new JavaScript benchmark a few days ago called ** Octane**. New benchmarks are always welcome, as they push browsers to new levels of performance in new areas. I was particularly pleased to see the inclusion of

[pdf.js](https://mozillalabs.com/pdfjs/), which unlike most benchmarks is real-world code, as well as the

[GB Emulator](https://github.com/grantgalitz/GameBoy-Online)which is a very interesting type of performance-intensive code. However, every benchmark suite has limitations, and it is worth keeping that in mind, especially given the new benchmark’s title in the announcement and in the

[project page](http://code.google.com/p/octane-benchmark/)as “The JavaScript Benchmark Suite for the Modern Web” – which is a high goal to set for a single benchmark.

Now, every benchmark must pick some code to run out of all the possible code out there, and picking representative code is very hard. So it is always understandable that benchmarks are never 100% representative of the code that exists and is important. However, even taking that into account, I have concerns with some of the code selected to appear in Octane: There are better versions of two of the five new benchmarks, and performance on those better versions is very different than the versions that do appear in Octane.

**Benchmarking black boxes**

One of the new benchmarks in Octane is “Mandreel”, which is the Bullet physics engine compiled by [Mandreel](http://www.mandreel.com/), a C++ to JS compiler. Bullet is definitely interesting code to include in a benchmark. However the choice of Mandreel’s port is problematic. One issue is that Mandreel is a closed-source compiler, a black box, making it hard to learn from it what kind of code is efficient and what should be optimized. We just have a generated code dump, which, as a commercial product, would cost money for anyone to reproduce those results with modifications to the original C++ being run or a different codebase. We also do not have the source code compiled for this particular benchmark: Bullet itself is open source, but we don’t know the specific version compiled here, nor do we have the benchmark driver code that uses Bullet, both of which would be necessary to reproduce these results using another compiler.

An alternative could have been to use Bullet compiled by [Emscripten](http://emscripten.org/), an open source compiler that similarly compiles C++ to JS (disclaimer: I am an Emscripten dev). Aside from being open, Emscripten also has a [port of Bullet](https://github.com/kripken/ammo.js/) (a demo can be seen [here](http://syntensity.com/static/ammo.html)) that can interact in a natural way with regular JS, making it usable in normal web games and not just compiled ones, unlike Mandreel’s port. This is another reason for preferring the Emscripten port of Bullet instead.

**Is Mandreel representative of the web?**

The motivation Google gives for including Mandreel in Octane is that Mandreel is “used in countless web-based games.” It seems that Mandreel is primarily used in the Chrome Web Store (CWS) and less outside in the normal web. The quoted description above is technically accurate: Mandreel games in the CWS are indeed “web-based” (written in JS+HTML+WebGL) even if they are not actually “on the web”, where by “on the web” I mean outside of the walled garden of the CWS and in the normal web that all browsers can access. And it makes perfect sense that Google cares about the performance of code that runs in the CWS, since Google runs and profits from that store. But it does call into question the title of the Octane benchmark as “The JavaScript Benchmark Suite for the Modern Web.”

**Performance of generated code is highly variable**

With that said, it is still fair to say that compiler-generated code is increasing in importance on the web, so some benchmark must be chosen to represent it. The question is how much the specific benchmark chosen represents compiled code in general. On the one hand the compiled output of Mandreel and Emscripten is quite similar: both use large typed arrays, the same [Relooper algorithm](http://dl.acm.org/citation.cfm?doid=2048147.2048224), etc., so we could expect performance to be similar. That doesn’t seem to always be the case, though. When we compare Bullet compiled by Mandreel with Bullet compiled by Emscripten – I made a benchmark of that a while back, it’s available [here](http://kripken.github.com/misc-js-benchmarks/bullet/) – then on my MacBook pro, Chrome is **1.5x slower** than Firefox on the Emscripten version (that is, Chrome takes 1.5 times as long to execute in this case), but **1.5x faster** on the Mandreel version that Google chose to include in Octane (that is, Chrome receives a score 1.5 times larger in this case). (I tested with Chrome Dev, which is the latest version available on Linux, and Firefox Aurora which is the best parallel to it. If you run the tests yourself, note that in the Emscripten version smaller numbers are better while the opposite is true in the Octane version.)

(An aside, not only does Chrome have trouble running the Emscripten version quickly, but that benchmark also exposes a bug in Chrome where the tab consistently crashes when the benchmark is reloaded – possibly a dupe of [this open issue](http://code.google.com/p/chromium/issues/detail?id=141021). A serious problem of that nature, that does not happen on the Mandreel-compiled version, could indicate that the two were optimized differently as a result of having received different amounts of focus by developers.)

Another issue with the Mandreel benchmark is the name. Calling it Mandreel implies it represents all Mandreel-generated code, but there can be huge differences in performance depending on what C/C++ code is compiled, even with a single compiler. For example, Chrome can be 10-15x slower than Firefox on some Emscripten-compiled benchmarks ([example 1](http://code.google.com/p/v8/issues/detail?id=2223), [example 2](http://code.google.com/p/v8/issues/detail?id=2097)) while on others it is quite speedy ([example](https://bugzilla.mozilla.org/show_bug.cgi?id=681062)). So calling the benchmark “Mandreel-Bullet” would have been better, to indicate it is just one Mandreel-compiled codebase, which cannot represent all compiled code.

**Box2DWeb is not the best port of Box2D**

“Box2DWeb” is another new benchmark in Octane, in which a specific port of Box2D to JavaScript is run, namely Box2DWeb. However, as seen [here](http://blog.j15r.com/2011/12/for-those-unfamiliar-with-it-box2d-is.html) (see also [this](http://mozakai.blogspot.com/2012/02/box2djs-box2d-on-web-is-getting-faster.html)), Box2DWeb is significantly slower than other ports of Box2D to the web, specifically Mandreel and Emscripten’s ports from the original C++ that Box2D is written in. Now, you can justify excluding the Mandreel version because it cannot be used as a library from normal JS (just as with Bullet before), but the Emscripten-compiled one does not have that limitation and can be found [here](https://github.com/kripken/box2d.js/). (Demos can be seen [here](http://syntensity.com/static/box2d.html) and [here](http://syntensity.com/static/box2d_80.html).)

Another reason for preferring the Emscripten version is that it uses Box2D 2.2, whereas Box2DWeb uses the older Box2D 2.1. Compiling the C++ code directly lets the Emscripten port stay up to date with the latest upstream features and improvements far more easily.

It is possible that Google surveyed websites and found that the slower Box2DWeb was more popular, although I have no idea whether that was the case, but if so that would partially justify preferring the slower version. However, even if that were true, I would argue that it would be better to use the Emscripten version because as mentioned earlier it is faster and more up to date. Another factor to consider is that the version included in Octane will get attention and likely an increase in adoption, which makes it all the more important to select the one that is best for the web.

I put up a benchmark of Emscripten-compiled Box2D [here](http://kripken.github.com/misc-js-benchmarks/box2d/), and on my machine Chrome is **3x**** slower** than Firefox on that benchmark, but **1.6x**** faster** on the version Google chose to include in Octane. This is a similar situation to what we saw earlier with the Mandreel/Bullet benchmark and it raises the same questions about how representative a single benchmark can be.

**Summary**

As mentioned at the beginning, all benchmarks are imperfect. And the fact that the specific code samples in Octane are ones that Chrome runs well does not mean the code was chosen for that reason: The opposite causation is far more likely, that Google chose to focus on optimizing those and in time made Chrome fast on them. And that is how things properly work – you pick something to optimize for, and then optimize for it.

However, in 2 of the 5 new benchmarks in Octane there are good reasons for preferring alternative, better versions of those two benchmarks as we saw before. Now, it is possible that when Google started to optimize for Octane, the better options were not yet available – I don’t know when Google started that effort – but the fact that better alternatives exist in the present makes substantial parts of Octane appear less relevant today. Of course, if performance on the better versions was not much different than the Octane versions then this would not matter, but as we saw there were in fact significant differences when comparing browsers on those versions: One browser could be significantly better on one version of the same benchmark but significantly slower on another.

What all of this shows is that there cannot be a single benchmark for the modern web. There are simply too many kinds of code, and even when we focus on one of them, different benchmarks of that particular task can behave very differently.

With that said, we shouldn’t be overly skeptical: Benchmarks are useful. We need benchmarks to drive us forward, and Octane is an interesting new benchmark that, even with the problems mentioned above, does contain good ideas and is worth focusing on. But we should always be aware of the limitations of any single benchmark, especially when a single benchmark claims to represent the entire modern web.


## 11 comments

Isaac GouyAugust 25th, 2012 at 07:59WebUserAugust 25th, 2012 at 18:21Brendan EichAugust 27th, 2012 at 14:29Tom Schuster (@evilpies)August 29th, 2012 at 10:15Brendan EichAugust 29th, 2012 at 10:24NinjaWarrior1976August 27th, 2012 at 08:29Alon ZakaiAugust 27th, 2012 at 09:47Tom ColwillNovember 22nd, 2012 at 14:52azakaiNovember 23rd, 2012 at 04:04Alon ZakaiAugust 29th, 2012 at 14:31Mark CodyAugust 29th, 2012 at 14:55