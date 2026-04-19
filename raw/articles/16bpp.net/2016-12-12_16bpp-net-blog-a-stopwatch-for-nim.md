---
title: '16BPP.net: Blog / A Stopwatch for Nim'
url: https://16bpp.net/blog/post/a-stopwatch-for-nim
published: '2016-12-12'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

As I mentioned in the previous post, I've been playing around with the [Nim language](http://nim-lang.org/) for a little less than a month now. So far I really like it and have used it for messing with computer graphics. I like to record how long things take to compute so I set out to look for a Timer of sorts. I was a little surprised to find out that it didn't have a built-in timing/benchmarking mechanism (like C# has with the [Stopwatch class](https://msdn.microsoft.com/en-us/library/system.diagnostics.stopwatch(v=vs.110).aspx)). There was [a package made available by rbmz](https://github.com/rbmz/stopwatch) under the name of `stopwatch`

that did some very basic stuff for me, but I was still unsatisfied. [So I decided to do a fork of it and made all of the changes that I wanted.](https://gitlab.com/define-private-public/stopwatch)

There were two main things that I changed. the `clock`

object was renamed to `Stopwatch`

, and the `Stopwatch`

can now record multiple laps. What I mean by "laps," is that you can now start and stop the `Stopwatch`

multiple times and it will remember those timings for you. Some other minor additions include methods to convert nanoseconds over to milli- and microseconds. To see everything that was added [check the source code here](https://gitlab.com/define-private-public/stopwatch/blob/master/stopwatch.nim), everything should be documented and easy to follow (there isn't much).

If you want to grab the package, it's up on nimble as `stopwatch`

. Yes, [one of the maintainers was nice enough to let me hijack the original package name](https://github.com/nim-lang/packages/pull/437). Here are some code samples (ripped from the README) that show you how to use this package:



[You can find the repo here.](https://gitlab.com/define-private-public/stopwatch) If you have any requests or find any bugs please tell me.