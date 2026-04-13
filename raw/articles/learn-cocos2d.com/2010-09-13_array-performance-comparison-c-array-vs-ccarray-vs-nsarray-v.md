---
title: 'Array Performance Comparison: C-Array vs CCArray vs NSArray vs NSMutableArray'
url: http://www.learn-cocos2d.com/2010/09/array-performance-comparison-carray-ccarray-nsarray-nsmutablearray/
author: MartinH says
published: '2010-09-13'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

When [TechnoKinetics](https://twitter.com/TechnoKinetics) mentioned on Twitter he was annoyed with cocos2d, I wanted to know why. It turns out it was the change away from NSMutableArray to CCArray in cocos2d which required him to update his codebase after he upgraded to the latest cocos2d version. He called it a “seemingly insignificant” change. At the time CCArray was introduced I didn’t think much about it but now I wondered, how significant or insignificant is it?

As far as I looked, there were only vague results published and the [cocos2d forum thread](http://www.cocos2d-iphone.org/forum/topic/6793) ends with Pearapps asking for a performance test, so I believe there are no CCArray performance test results available. The conversation also lead me to this [NSArray vs. C-Array performance comparison](http://memo.tv/nsarray_vs_c_array_performance_comparison). To my dismay, it is comparing apples with oranges, as the NSArray had to wrap and unwrap the floating point values into NSNumber objects, so the results are terribly skewed in favor of the C-Array. Since this article was referred to in the CCArray cocos2d forum thread, it made me skeptical about the initial performance tests putting ccArray (the C implementation which is wrapped by CCArray, mind the case) at 3.7 times faster, or just plain text “very very faster”. I’m an engineer and not a believer, such “much faster” statements always make me very skeptical (how much is “very”?). I thought I should put in some time to generate some actual numbers.

### Test Setup

I decided to take parts of [Mehmet Akten](http://www.msavisuals.com/about)‘s array test code (eg. measuring the time), then use all available array types in a way that is most common to cocos2d: storing pointers. I wanted to do a little more real-world-ish test. Internally cocos2d uses CCArray to store the children of a node, which are pointers. Without the boxing & unboxing of NSNumber we can better compare the results of how the individual array types perform. So I [derived my own testing project](https://www.learn-cocos2d.com/wordpress/wp-content/uploads/ArraySpeedTest.zip) to figure out how fast read access is between a C-Array, CCArray, NSMutableArray and NSArray by looping over each element in the array, retrieving the element (a CCLabel) and changing its tag property, just to give the loop something to do. I’m wary of the compiler possibly over-optimizing the loop if it doesn’t do anything. I’m also wary of any caches (whichever the iOS devices may or may not have) affecting the test, so I made sure that the item count (50,000) was large enough to not fit into any caches.

Code that is measured for **for** loops:

|
1 2 3 4 5 |
for(int i=0; i<NumItems; i++) { CCNode* node = [c2Array objectAtIndex:i]; node.tag = i; } |

Using fast enumeration:

|
1 2 3 4 5 |
int i = 0; for (CCNode* node in nsMutArray) { node.tag = i++; } |

Using **CCARRAY_FOREACH** fast enumeration:

|
1 2 3 4 5 6 |
int i = 0; CCNode* node; CCARRAY_FOREACH(c2Array, node) { node.tag = i++; } |

### Sequential Read Performance

The results: a mere 10% read access performance increase for CCArray compared to NSMutableArray when using a **for** loop (2nd and 3rd column from the right in the chart below). And a tiny, negligible improvement when using the **CCARRAY_FOREACH** keyword compared to NS(Mutable)Array’s fast enumerator **for(CCNode* node in array)** to iterate over the array. Both these results are in the same ballpark with the C-Array, and I was pleasantly surprised to see the CCArray and NS(Mutable)Array all perform basically the same as the C-Array when using fast enumeration, with CCArray just a tiny fraction faster - exactly the same performance as a pure C-Array.

The test did also reveal an interesting effect I hadn’t expected: the NSArray’s read access performance without fast enumeration is noticeably slower than NSMutableArray. It really shouldn’t be slower, but NSArray consistently performed around 70% slower than NSMutableArray when using a **for** loop. I have no explanation for this anomaly. And with fast enumeration both are exactly the same speed-wise.

The Y axis is in milliseconds:

These results indicate that you do not need to use a C-Array over NSMutableArray or CCArray when the array is fixed in size and only read from. If you’re only concerned about access speed, and you use the fast enumerator respectively **CCARRAY_FOREACH**, you can use CCArray, NSArray, NSMutableArray and a C-Array interchangeably. The performance difference is indeed insignificant. There’s a lot of other things you can do to improve your game’s performance before you should start considering which type of array to use. But for a fixed-size array, NSArray is definetely the worst choice.

Things change of course if you need to store primitive data types like float, int, double. In that case, the C-Array will win hands down against its competitors because it doesn’t need to wrap primitive data types in a NSNumber object. But in the other cases, when you store actual pointers, by all means use the convenience collections available to you and benefit from bounds checks and a better interface to set, retrieve and iterate over objects. In this read access test, CCArray only has an advantage if you’re using a regular **for** loop to iterate over the elements (see the last 3 columns in the chart above). But at most it’s just 10% faster than NSMutableArray, that’s still negligible, especially if you consider the time spent running whatever code within the loop.

### Add, Insert & Remove Performance

I also wanted to find out how much of an improvement CCArray is over NSMutableArray for adding and removing objects. It causes the array to expand or shrink as the number of objects increase and decrease, which creates an additional and sometimes significant overhead. That’s where CCArray should shine. Here’s the test setup:

Add object to end of array:

|
1 2 3 4 |
for(int i=0; i<NumItems; i++) { [nsMutArray addObject:label]; } |

Insert object at first position (shifting the remaining part of the array back by 1):

|
1 2 3 4 |
for(int i=0; i<NumItems; i++) { [nsMutArray insertObject:label atIndex:0]; } |

Remove last object:

|
1 2 3 4 |
for(int i=0; i<NumItems; i++) { [nsMutArray removeObjectAtIndex:NumItems - i - 1]; } |

Remove object at index 0 (first position):

|
1 2 3 4 |
for(int i=0; i<NumItems; i++) { [nsMutArray removeObjectAtIndex:0]; } |

The initial finding was promising, the CCArray is 40% to 50% faster than NSMutableArray for the addObject and removeObjectAtIndex:last operations (meaning: to add or remove and item at the last position in the array) on my iPhone 3G. On the iPad as native application, the difference is even more significant with CCArray being 8 times faster than NSMutableArray for the addObject operation, and 2.2 times faster for the removeAtIndex:last operation. That’s great news!

But then came the shock when I tried insertObject:AtIndex:0 and removeObjectAtIndex:0 … I thought my iPhone had locked up and crashed, but alas CCArray is just dead slow in these cases! And by dead slow I mean: broken. Over 200 times slower, even on the iPad. Unless I made a grave mistake in my test (which I don’t see), it’s very likely a bug in the CCArray implementation. Or a design flaw. In any case, something isn’t right when it takes CCArray 53 seconds to insert or remove an object at the first index when NSMutableArray only needs 0.2 seconds to perform the same operations. If you rely on the removeAtIndex and insertAtIndex methods you should refrain from using CCArray until this problem is fixed. As far as I can tell, cocos2d rarely uses these methods internally so this issue shouldn’t have a measurable impact on cocos2d’s overall performance.

**Update:** [@manucorporat](https://twitter.com/manucorporat) has [already fixed this CCArray performance issue](https://github.com/manucorporat/cocos2d-iphone/commit/9740711dc45060ae912b7a36c95a1ed98cd8c79d) (within minutes!!), it should be integrated in a new cocos2d build soon. I’ll update the performance test results soon.

**Update #2:** Apparently the fix was not all encompassing. It was faster on the iPad but just about 8 times, but still at least 13 times slower than NSMutableArray. On my iPhone 3G the results were worse and went down to a factor of 360. It’s being worked on. Stay tuned.


Note that this diagram is not to scale! If it were, you wouldn’t be able to make out the blue bars for NSMutableArray!

All tests were done on an iPhone 3G running iOS 4.1 with a release build of cocos2d v0.99.5 beta. The results for iPad were only glanced at to check for relative differences, see text above. All results are in milliseconds, averaged over several runs (3-5) with an iteration count of 50,000. The read speed tests were run individually, not in sequence, because running all read speed tests in sequence caused slightly different results depending on the order in which the tests were run. For example, the slower speed of NSArray was less pronounced if the tests ran in sequence.

Feel free to download my [ArraySpeedTest.zip ](https://www.learn-cocos2d.com/wordpress/wp-content/uploads/ArraySpeedTest.zip)project and try to reproduce the results. Only run the tests on a device and in release builds to get comparable numbers. Let me know if you find flaws in the test setup. I’m also interested to hear if the relative speeds vary on other devices.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Thanks for sharing these results and your project! I used the project as a base to do some benchmarking on my own. I wanted to know how much slower it is to have a math helper function in a helper object vs writing the code directly where the calculation is needed vs using static __inline__ functions.

here is what was calculated 100000 times for 2 points and the result saved into an array:

static __inline__ float tcGetDirectionFromPointToPoint(CGPoint point1, CGPoint point2)

{

float angle = CC_RADIANS_TO_DEGREES(atan2(point2.x-point1.x, point2.y-point1.y));

if (angle < 0) angle += 360;

return angle;

}

the code for the method packed into an object or the variant of writing the code directly into my test loop was identical of course.

and here is the result:

2010-09-22 02:32:38.991 ArraySpeedTest[195:307] math test 1: math helper object

2010-09-22 02:32:39.083 ArraySpeedTest[195:307] 80.2 milliseconds

2010-09-22 02:32:39.094 ArraySpeedTest[195:307] math test 2: no function call

2010-09-22 02:32:39.147 ArraySpeedTest[195:307] 41.9 milliseconds

2010-09-22 02:32:39.157 ArraySpeedTest[195:307] math test 3: static inline function

2010-09-22 02:32:39.211 ArraySpeedTest[195:307] 42.4 milliseconds

2010-09-22 02:32:39.221 ArraySpeedTest[195:307] math test 1: math helper object

2010-09-22 02:32:39.310 ArraySpeedTest[195:307] 78.1 milliseconds

2010-09-22 02:32:39.321 ArraySpeedTest[195:307] math test 2: no function call

2010-09-22 02:32:39.374 ArraySpeedTest[195:307] 41.9 milliseconds

2010-09-22 02:32:39.384 ArraySpeedTest[195:307] math test 3: static inline function

2010-09-22 02:32:39.438 ArraySpeedTest[195:307] 42.6 milliseconds

2010-09-22 02:32:39.448 ArraySpeedTest[195:307] math test 1: math helper object

2010-09-22 02:32:39.539 ArraySpeedTest[195:307] 79.7 milliseconds

2010-09-22 02:32:39.549 ArraySpeedTest[195:307] math test 2: no function call

2010-09-22 02:32:39.602 ArraySpeedTest[195:307] 41.9 milliseconds

2010-09-22 02:32:39.612 ArraySpeedTest[195:307] math test 3: static inline function

2010-09-22 02:32:39.666 ArraySpeedTest[195:307] 42.6 milliseconds

2010-09-22 02:32:39.676 ArraySpeedTest[195:307] math test 1: math helper object

2010-09-22 02:32:39.766 ArraySpeedTest[195:307] 78.3 milliseconds

2010-09-22 02:32:39.776 ArraySpeedTest[195:307] math test 2: no function call

2010-09-22 02:32:39.829 ArraySpeedTest[195:307] 41.8 milliseconds

2010-09-22 02:32:39.840 ArraySpeedTest[195:307] math test 3: static inline function

2010-09-22 02:32:39.895 ArraySpeedTest[195:307] 44.2 milliseconds

2010-09-22 02:32:39.905 ArraySpeedTest[195:307] math test 1: math helper object

2010-09-22 02:32:39.995 ArraySpeedTest[195:307] 79.6 milliseconds

2010-09-22 02:32:40.006 ArraySpeedTest[195:307] math test 2: no function call

2010-09-22 02:32:40.059 ArraySpeedTest[195:307] 41.8 milliseconds

2010-09-22 02:32:40.070 ArraySpeedTest[195:307] math test 3: static inline function

2010-09-22 02:32:40.123 ArraySpeedTest[195:307] 42.6 milliseconds

seems like the overhead of putting those things into an object instead of using that static inline function (I don't even know the right term for this) could get significant if you do things like this extremely often on every frame of a game e.g.. I hope this was interesting for someone and makes any sense.

Thanks for sharing that! I assume the Helper function was something like +(float) calcResults:(CGPoint)pt1 ?

Meaning a Objective-C static method. There’s some overhead associated with message passing which probably causes this overhead. If you even do a Helper* helper = [[Helper alloc] initWithPoint:(CGPoint)pt]; and then [Helper release] that would be more significant overhead.

No problem :). The helper function was one from your linedrawing game starter kit. I just changed the calculation to what I posted above. The call is made like [MathHelper getDirectionFromPoint:point1 toPoint:point2]. There is no alloc or dealloc going on. Would be interesting though, how much longer that would take. Maybe I’ll test it out of couriosity, even though it makes absolutely no sense to use it like that ;).

This is good stuff. As I noted on twitter, it would be very interesting to compare using CFMutableArray with nil retain & release functions. If the retain/release were _actually_ the performance problem, as stated, then this would be a _much_ better approach to fixing it, in my opinion. the NSArray and CFArray classes are very smart (see: http://ridiculousfish.com/blog/archives/2005/12/23/array/ ) and it’s unlikely that any replacement is going to be a generally good.

That said, it’s possible that for Cocos2d we know something that allows us to make a situationally optimal implementation (never more than 100 items in the array or something like that); but I’d want too see actual data proving it was dramatically better before I created a new key core class like this and I’d want LOTS of unit tests over a wide range of input data and use patterns to be sure it was as robust as what it is replacing.

Yap, including selfmade data collections into the core of a game engine is a decision that should not be made lightly. The whole reason I found out about this performance issue was because I was quite frankly furious because there was no substantial and reproducable performance data provided, yet assumptions were running wild.

At that point I thought: am I going to just believe it, or am I going to verify it because I prefer to *know*?

[…] common use case.) Now, there is some contention about the speed of ccArray in cocos2d. For example, this post argues that it’s unfair to count the NSNumber wrapping time against NSMutableArray. Well, […]

[…] been over a year since I last compared the performance of CCArray with NSArray and NSMutableArray. While doing these tests I found that CCArray’s insertObjectAtIndex and removeObjectAtIndex […]

The second to last test, removeObjectAtIndex, isnt really interesting because CCarray remakes the array while nsmutablearray does not. What I would be really curious to see is how CCArrays’s fastRemoveObjectAtIndex stacks up against these. It sacrifices order for speed by moving the last object into the spot of the deleted object.

I purposefully left that out because this method violates the idea of an array’s elements remaining in the order they were added to it, unless you explicitly insert or swap elements. In cocos2d using this method can have undesired side effects, like changing the order in which nodes are drawn. This is the kind of optimization I frown upon having in a public API, meaning one that creates (not so obvious) side-effects in favor of speed. I worry that posting better performance results for this method might drive people to use it without fully understanding the consequences. And who does, really? I ran into an issue that cost me 2 hours of my time because I was using this method and it changed the order in which the nodes were updated.