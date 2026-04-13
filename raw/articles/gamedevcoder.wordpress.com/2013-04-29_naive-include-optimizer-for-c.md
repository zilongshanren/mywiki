---
title: 'Naive #include Optimizer for C++'
url: https://gamedevcoder.wordpress.com/2013/04/29/naive-include-optimizer-for-c/
published: '2013-04-29'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Here’s my simple and really basic utility written in C# that optimizes Visual Studio project by removing redundant #include lines where possible. Why having redundant #includes is so bad? The answer is simple – it can severely slow down the compilation process.

Download: [Source and Binary](https://code.google.com/p/naive-include-optimizer/downloads/list)

Example usage:

NaiveIncludeOptimizer.exe “C:/Program Files (x86)/Microsoft Visual Studio 11.0/Common7/IDE/devenv.exe” “C:/my_project/my_project.sln” “Debug” “C:/my_project/src”

Example output:

Optimizing Main.cpp... Redundant #include External.h Redundant #include Misc.h Optimizing Misc.cpp... Redundant #include Common.h Redundant #include API.h Redundant #include Defines.h DONE!

The way it works is very brute force (hence the “Naive” in the name) meaning it tests every #include individually to see if the solution would still build if it was removed. So, yes, that means larger projects may even take days to process! But in the end it does work (mostly – see below when it doesn’t).

Be careful because it does modify the source code. But while doing so, it always creates a backup copy. Bonus feature is that it is capable of resuming from where it stopped last time.

Also, please note that it only optimizes .cpp files. Optimizing .h files would obviously take a lot longer!

I should also point out that the proper way of doing this would be implementing full blown C++ preprocessor that would include:

* removing redundant #includes

* adding forward declares where possible

* making sure that the actual code generated does not change (my solution may result in some undesired program “optimizations” – e.g. by removing #include “my_new_operators.h” the definition of your new/delete operators might change but the project would still build successfully)

It’s obviously a lot more work but fortunately that’s exactly how Google’s [Include-What-You-Use](https://code.google.com/p/include-what-you-use/) is meant to work. I haven’t tried it but it looks neat.