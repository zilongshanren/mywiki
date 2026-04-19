---
title: Mine your Data!
url: https://c0de517e.blogspot.com/2011/04/mine-your-data.html
published: '2011-04-03'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Some simple ideas:

- Add to your bug tracking two compulsory fields to be filled (choosing from a list) when closing a bug: where it was found (AI, Rendering, Loading etc...) and what caused it (Incorrect API usage, corner case not handled, memory stomp, wrong algorithm, variable not properly initialized, invariants not enforced and so on). Soon you'll see what parts require rewriting, what need unit testing, automated tests and so on.
- Give testers a build connected to a sampling profiler. Sample. Diff the profiled function list with the list of functions in your symbols file. Voila', cheap coverage analysis. Now we know which code to delete!
- Install automatic time tracking tools, like this
[one](http://www.procrastitracker.com/#). Anonymously gather data about your project (be nice). At the end, you'll know how much time was spent in which area (much better than measuring the number of changes or check-ins or so). So we'll know which things are better to be moved into a scripting language, or into a dynamically loadable module! - It's also a good idea to keep track of the CPU time of some key processes, like your compiler, linker, the time your VCS spends in networking operations and so on. Unfortunately I don't know any program that does that on windows and I ended up writing a simple one a year ago to prove we were spending too much time waiting for linking.
- Do you have a in-game telemetry? Are you not using it internally on testers machines to gather data (memory usage, FPS and so on). Shame on you!

## No comments:

Post a Comment