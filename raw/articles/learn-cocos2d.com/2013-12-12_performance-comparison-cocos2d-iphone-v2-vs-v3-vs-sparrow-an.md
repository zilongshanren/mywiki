---
title: 'Performance Comparison: cocos2d-iphone v2 vs v3 vs Sparrow and ARC vs MRC'
url: http://www.learn-cocos2d.com/2013/12/performance-comparison-cocos2diphone-v2-v3-sparrow-arc-mrc/
author: PrimaryFeather says
published: '2013-12-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Daniel Sperl, developer of the Sparrow Framework, recently posted a performance comparison on the Apple Developer forum where [Sparrow ran 2.5 times faster with MRC code](https://devforums.apple.com/thread/208688?start=0&tstart=0) than the version upgraded to ARC.

A curious finding though it seemed very far off from real world observations. Being a synthetic benchmark no less. I decided to do a similar test based on the same code comparing cocos2d v2 and v3.

Fortunately cocos2d-iphone v3 has made a similar switch from MRC (v2.1 and earlier) to ARC (v3 preview). Unfortunately the internals of cocos2d also changed to some extent, for example custom collection classes written in C were replaced by Core Foundation classes. I don’t have a full overview of the changes, but at least [the renderer doesn’t seem to have changed](http://www.learn-cocos2d.com/2013/11/premature-preview-cocos2diphone-v3-preview/) in any significant way. Yet.

So while comparability is good, it’s not like Sparrow where truly the only changes made were converting the code from ARC back to MRC. Take the following benchmark results and comparisons with two grains of salt and pepper on the side.

### ARC vs MRC

The original benchmark done with Sparrow has seen MRC perform 2.5 times better than ARC in a synthetic “draw as many sprites as possible until framerate has dropped consistently below 30 fps” test:

![sparrow_arc_vs_mrc](../../../wordpress/wp-content/uploads/sparrow_arc_vs_mrc.png)



The discussion seemed to reveal that the issue may be a side-effect of Sparrow’s architecture taking a larger-than-usual hit from the switch to ARC due to insertions of extra retain/release. For example passing an object to a method will have ARC insert retain and release for the object even though the object’s lifetime will always exceed the duration of the method.

Cocos2d on the other hand doesn’t pass a lot of objects around during the update loop, so I was hopeful it wouldn’t take as much a performance penalty from ARC as Sparrow did. Turns out to be true:

![Screen Shot 2013-12-12 at 17.03.28](../../../wordpress/wp-content/uploads/Screen-Shot-2013-12-12-at-17.03.28.png)


ARC is in fact slightly faster for iPod touch 5 and iPad 1, while cocos2d-iphone v2.1 (MRC) is 50% faster on iPad 3. I can’t really explain this difference on the Retina iPad, it needs further investigation when cocos2d v3 is more mature.

I can’t even say whether the iPad 3 test is CPU or GPU bound. It may be CPU bound which *might* explain a greater negative impact of ARC. However if that’s true, that’s actually good news, because far more games have performance issues because of fillrate, not because the CPU couldn’t keep up. And there’s a simple optimization to be found in multithreading, given that almost all iOS 7 devices have dual-core CPUs.

Now of course that needs a framework which is capable of multithreading. Sprite Kit + [OpenGW](http://opengameworld.com/). Hint, hint. 😉

### The effect of Batch Drawing

While I was at it I wanted to show how much of a difference batch drawing makes.

![Screen Shot 2013-12-12 at 17.03.39](../../../wordpress/wp-content/uploads/Screen-Shot-2013-12-12-at-17.03.39.png)


Interestingly the gap is far larger on the Retina iPad 3 than for the slower devices. Goes to show that even a much faster device (iPad 3) will render fewer sprites than an older device (iPad 1) that renders batched sprites.

### Cocos2D vs Sparrow

Though the benchmark code I used is based on [Sparrow’s benchmark scene](https://github.com/Gamua/Sparrow-Framework/blob/master/samples/demo/src/Classes/BenchmarkScene.m), it can’t really be compared. I’m doing it anyway. 😉

What you need to know about this comparison is that Sparrow’s benchmark scene renders slightly differently. It allows some of the nodes to be partially outside the screen, which may skew results slightly in its favor.

The iPad versions of Sparrow’s benchmark can’t be compared at all because the results I see are quite different compared to cocos2d. It looks like internally Sparrow uses a fixed-size scene of 960×640 points for all devices, which leaves a small area of the iPad screen cut off. Plus the scaling is different compared to cocos2d, Sparrow’s sprites are about twice as large on iPads. Hence Sparrow’s iPad version of the benchmark produces far lower results than my ported benchmark.

Overall real world performance difference between the two engines doesn’t really matter.

### The Benchmark Code

You’ll find the benchmark projects for cocos2d v2 and v3 in [my github repository](https://github.com/LearnCocos2D/LearnCocos2D).

Look for the projects named **Cocos2D-v2.1-Performance** and **Cocos2D-v3.0-alpha-Performance**.

Side-note: just getting the two benchmark projects work on both Retina and non-Retina, on small and iPad screen sizes took me about 2 hours to get them decently correct. It’s bugs like disappearing menus on Retina, iPad not loading the correct images, labels wildly offset on each device and resolution and the fact that these behaviors change between v2 and v3 make me a very happy Sprite Kit user these days.

### Poll for (future) Sprite Kit users

If you can spare a minute please take this poll, thank you!

Let me know what I should be working on or confirm that what I’m currently working on won’t be for naught … which apparently it isn’t. Good to know. 😉

Also [take the preferred Objective-C render engine poll](http://www.webpollgenerator.com/ViewPoll.php?p=528fc819cacaf) if you haven’t already. Thanks again!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Thanks for porting the benchmark over to Cocos2D, Steffen! Those are really interesting results. That’s good news for Cocos2D that it doesn’t suffer from ARC that much.

That the results of iPod Touch 5G and iPad 1 are so similar while there’s a difference on iPad 3 is a little suspicious, though. I suppose Cocos2D renders all objects in one batch, right? Then you could rule out the fill rate by repeating the benchmark with very small objects — scaling them down to 10%, for example. Have you tried that?

BTW, just for the sake of completeness: Sparrow does not use a fixed-size scene of 960×640 points for all devices — just the benchmark project does. 😉

I noticed a bug in the iPad 3 version. While the v2.1 build used the -hd texture the v3 build did not. Looks like there may be a bug with the -hd suffix, I explicitly set -hd as ipad retina suffix via CCFileUtils but it wasn’t adhered to and the low resolution images was loaded instead.

Though this should have skewed the results *in favor* of v3 it did not, instead v2.1 was faster. In fact the size of the texture on iPad 3 made no difference to begin with.

iPad 3 results with correct (HD) size of benchmark image in cocos2d v3:

cocos2d v3, batched, ARC (using HD image): 8995 (was: 8970)

I re-ran the iPad 3 test with tiny textures (8×8 pixels, Retina). Results:

cocos2d v2.1, batched, MRC: 13678 (was: 12048)

cocos2d v3, batched, ARC: 9115 (was: 8970)

Texture size had a negligible effect on the benchmark results. Cocos2d v3 remains 33% slower on iPad 3 compared with v2.1. Again it’s too early to tell where this is coming from and whether this characteristic will persist in future v3 versions.