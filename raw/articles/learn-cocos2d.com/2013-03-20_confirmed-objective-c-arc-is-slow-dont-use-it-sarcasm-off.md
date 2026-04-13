---
title: 'Confirmed: Objective-C ARC is slow. Don�t use it! (sarcasm off)'
url: http://www.learn-cocos2d.com/2013/03/confirmed-arc-slow/
author: Dad says
published: '2013-03-20'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Or so goes the argument](http://stackoverflow.com/questions/12527286/are-there-any-concrete-study-of-the-performance-impact-of-using-arc). Still.

I wish Apple would just pull the plug and completely remove MRC support from LLVM. I’m getting tired, annoyed and sometimes angry when I browse [stackoverflow.com](http://stackoverflow.com/) and frequently find MRC code samples containing one or more blatant memory management issues.

Before I rant any further, **this article is about testing the performance difference of ARC vs MRC code**. I provide some examples, and the [updated performance measurement project](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/Cocos2D-ARC-Performance-Test) I’ve used before for [cocos2d performance analysis](http://www.learn-cocos2d.com/2011/11/depth-ios-cocos2d-performance-analysis-test-project/), and the results of the full run at the bottom. I also split it into both synthetic low-level tests and closer to real-world algorithms to prove not one but two points:

**ARC is generally faster, and ARC can indeed be slower** - but that’s no reason to dismiss it altogether.

#### Measuring & Comparing Objective-C ARC vs MRC performance

Without further ado, here are the results of the low-level MRC vs ARC performance tests, obtained from an iPod touch 5th generation with compiler optimizations enabled (release build):


Times are in nanoseconds. A nanosecond (ns) is one billionth of a second (0.000 000 001 second). One Gigahertz (GHz) equals 1,000,000,000 Hz. One cycle of a 1 GHz CPU takes 1 nanosecond. A game that renders every frame in less than 16,700,000 nanoseconds runs at 60 frames per second. In other words, you can perform close to half a million Objective-C message sends every frame before your framerate drops below 60.


##### ARC vs MRC: Messaging Tests


| Name | Each (ns) |
| ARC: Message Send to Object | 49 |
| MRC: Message Send to Object | 86 |
| ARC: Assign (nonatomic, copy) property | 329 |
| MRC: Assign (nonatomic, copy) property | 331 |

##### ARC vs MRC: Alloc/Init Tests


| Name | Each (ns) |
| ARC: Create Alloc/Init Object | 4.844 |
| MRC: Create Alloc/Init Object | 4.881 |

##### ARC vs MRC: Autorelease Tests


| Name | Each (ns) |
| ARC: Create & Return Autorelease Object | 5.769 |
| ARC: Create Autorelease Object | 5.840 |
| MRC: Create & Return Autorelease Object | 5.843 |
| MRC: Create Autorelease Object | 6.625 |

So the low-level tests are about equal and ARC usually has an advantage. Mainly due to faster autorelease pools and other low-level optimizations. This is why Apple says that ARC is generally faster than MRC.

#### Where ARC can actually be slower

That ARC is faster is not true in every case. Specifically where existing MRC code has already been fine-tuned to provide the best possible performance in regards to memory usage.

This is because in some situations ARC adds additional retain/release messages that are sort of optional under MRC. This happens for example when you send a message to a selector with one or more object (id) parameters. It also happens when you receive a temporary variable from a method - it gets retained and then released even though its lifetime is short and contained. For example:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 |
// this is typical MRC code: { id object = [array objectAtIndex:0]; [object doSomething]; [object doAnotherThing]; } // this is what ARC does (and what is considered best practice under MRC): { id object = [array objectAtIndex:0]; [object retain]; // inserted by ARC [object doSomething]; [object doAnotherThing]; [object release]; // inserted by ARC } |


And again when sending messages to a selector which takes one or more objects as parameters:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 |
// this is typical MRC code: -(void) someMethod:(id)object { [object doSomething]; [object doAnotherThing]; } // this is what ARC does (and what is considered best practice under MRC): -(void) someMethod:(id)object { [object retain]; // inserted by ARC [object doSomething]; [object doAnotherThing]; [object release]; // inserted by ARC } |


The reason why ARC adds these additional retain/release is because above all else ARC ensures correctness. And that code is correct under MRC as well. So why don’t we usually add these additional retain/release in MRC and it still works?

Because most of us aren’t writing multi-threaded applications, and even those who do will probably not understand why they’re treading dangerously close to the edge. In multithreaded applications said object could be released between the doSomething and doAnotherThing calls - thus crashing your app. Granted, it’s rare but when it rears its ugly head, you wish you wouldn’t have to debug it.

This explains why some algorithms run slower under ARC than the same code written in MRC. I took [this Objective-C ARC genetic algorithm](http://ijoshsmith.com/2012/04/08/simple-genetic-algorithm-in-objective-c/) and converted it to MRC to make the comparison. You’ll see in the results that the ARC version is noticably slower than the MRC version mainly because of the additional retain/release:

##### ARC vs MRC: Algorithm Tests


| Name | Each (ns) |
| ARC: Unoptimized Contains String algorithm | 1.696.808 |
| MRC: Unoptimized Contains String algorithm | 1.752.414 |
| MRC: genetic algorithm | 1.134.536.017 |
| ARC: genetic algorithm | 1.579.992.123 |

PS: don’t ask me why the “contains string” algorithm is faster under ARC. It just is.

#### Avoid using ARC for best performance, right?

**No way!
**

Whoever thinks like that hasn’t understood what programming or ARC are all about. First and foremost, you want to write an app and release it without bugs, especially no crashes.

[ARC helps you tremendously](http://stackoverflow.com/a/8760820/201863)with that.

While writing this very little MRC code for the project I had already introduced several leaks, one of which wasn’t even caught by the analyzer. It’s just too damn easy to write incorrect manual reference counting code. And it’s even more code to read and write, too. With ARC I have not had a single leak or other such issue in months! The static analyzer has changed from a tool that I used to run daily to one I run on a monthly basis only to confirm that there are few or no memory management issues.

For beginners MRC is even worse, because not understanding MRC they’ll randomly insert or remove release, retain and autorelease messages until it somehow works. Usually they just shift the problem around or change the nature of it: a crash becomes a leak, a leak becomes a dangling pointer. It makes me want to cry. It makes me want to not help anyone who is still using MRC code for no reason or simply because that’s the default in cocos2d.

That every day thousands of cute kittens have to die because developers are starting new cocos2d projects with MRC templates makes me really sad. I find solace only in knowing that [Kobold2D](http://www.kobold2d.com/) and [KoboldTouch](http://www.learn-cocos2d.com/store/koboldtouch/) help to preserve the imaginary kitten population.

#### Good programmers use ARC!

Spending as little time as possible on any extraneous tasks such as manual memory management and debugging issues because of it is a programmer’s primary concern. Maybe second only to writing readable and maintainable code. Performance is way at the bottom of the priority lists, even for game developers.

If you’re more concerned about performance than code correctness, you’re not doing a good job because you set the wrong priorities. ARC ensures that you get the most out of your time **and** your app’s runtime.

And then any performance difference you can measure between ARC and MRC code in synthetic tests is practically null and void in real world applications. You’re usually doing a lot more elsewhere, like rendering, and often you don’t even have much control over those parts (game engine, foundation, etc). And you always have room for optimization just by writing better code.

The genetic algorithm I picked is such an example. The code repeats a terribly wasteful memory management pattern regardless of whether you’re using ARC or MRC. Refactor or rewrite the essential parts of the code in C, or just optimized Objective-C, and you’ll likely see gains far greater than the difference between ARC and MRC in the test result above.

Finally, typically **less than 5% of your code contributes to 95% of its runtime performance!** It would be downright stupid not to use ARC for the remaining 95%, and hand-tune only the 5% where it’ll make an actual difference in responsiveness, speed or framerate.

#### Final words

Arguing against using ARC because it may be slower in some well-defined situations really makes me wonder one thing: if you’re that concerned about performance, why are you even using Objective-C to begin with?

**Objective-C has been proven to be slower than C countless times already. Your argument is invalid!**

You can certainly make significantly greater performance improvements by rewriting certain performance-critical code to C than you could ever hope to achieve by avoiding ARC and sticking to MRC. Fortunately only very few developers will ever have to consider doing so.

And why are we using Objective-C?

It’s because Objective-C is **easier to use and safer** than plain C! In that sense, using ARC is a logical next step for any Objective-C programmer because it makes your work even easier and your app more stable. And when you do find an actually **noticable** performance difference, compared to one that’s only measurable, you can always **-fno-objc-arc the hell out of that code**.

### Complete Test Results (iPod touch 5G)

This is from a different run, so the values you’ve already seen earlier may differ. Comparing the results gives you an indication of how much of an error range there is in these values.

The results involving cocos2d are not directly comparable to the previous performance tests I did because [the updated performance test project](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/Cocos2D-ARC-Performance-Test) uses cocos2d v2.1 (rc0a), the previous one used cocos2d v1.0.1.

#### ARC vs MRC: Messaging Tests


| Name | Each (ns) |
| ARC: Message Send to Object | 61 |
| MRC: Message Send to Object | 61 |
| ARC: Assign (nonatomic, copy) property | 329 |
| MRC: Assign (nonatomic, copy) property | 330 |

#### ARC vs MRC: Alloc/Init Tests


| Name | Each (ns) |
| ARC: Create Alloc/Init Object | 4.747 |
| MRC: Create Alloc/Init Object | 4.811 |

#### ARC vs MRC: Autorelease Tests


| Name | Each (ns) |
| ARC: Create Autorelease Object | 5.503 |
| ARC: Create & Return Autorelease Object | 5.608 |
| MRC: Create & Return Autorelease Object | 5.612 |
| MRC: Create Autorelease Object | 6.342 |

#### ARC vs MRC: Algorithm Tests


| Name | Each (ns) |
| ARC: Unoptimized Contains String algorithm | 1.691.563 |
| MRC: Unoptimized Contains String algorithm | 1.750.430 |
| MRC: genetic algorithm | 1.144.589.482 |
| ARC: genetic algorithm | 1.559.268.544 |

#### Loading Textures

Time it takes to load and unload the same 1024×1024 texture using a variety of different image file formats, compression and color bit depths.


| Name | Each (ns) |
| PVRTC2.pvr.ccz | 300.497 |
| PVRTC4.pvr.ccz | 306.025 |
| PVRTC2.pvr | 3.752.015 |
| PVRTC4.pvr | 7.255.280 |
| PVRTC2.pvr.gz | 10.308.318 |
| PVRTC4.pvr.gz | 19.612.099 |
| RGBA8888.pvr | 57.411.790 |
| RGBA8888.pvr.ccz | 85.919.379 |
| RGBA8888.png | 98.239.494 |
| RGBA8888.pvr.gz | 100.842.780 |

#### Node Hierarchy (children)

The performance of functions that act on the node hierarchy (children list) depends heavily on the number of children.


| Name | Each (ns) |
| reorderChild w/ 100 Nodes | 258 |
| reorderChild w/ 2,500 Nodes | 258 |
| reorderChild w/ 10 Nodes | 259 |
| reorderChild w/ 500 Nodes | 261 |
| getChildByTag w/ 10 Nodes | 1.188 |
| getChildByTag w/ 100 Nodes | 5.998 |
| addChild with tag | 6.758 |
| removeChildByTag | 16.493 |
| getChildByTag w/ 500 Nodes | 29.022 |
| getChildByTag w/ 2,500 Nodes | 178.572 |

#### Array Tests

Testing Cocos2D’s CCArray performance against regular NSMutableArray.


| Name | Each (ns) |
| CCArray objectAtIndex: | 248 |
| CCArray exchangeObjectAtIndex | 267 |
| NSMutableArray objectAtIndex: | 285 |
| CFArray GetValueAtIndex | 319 |
| CCArray withCapacity addObject: | 385 |
| CCArray addObject: | 385 |
| NSMutableArray insertObject: atIndex:0 | 468 |
| NSMutableArray withCapacity addObject: | 539 |
| NSMutableArray addObject: | 540 |
| CCArray removeLastObject | 734 |
| NSMutableArray removeLastObject | 1.039 |
| CCArray removeObjectAtIndex | 1.546 |
| NSMutableArray removeObjectAtIndex | 1.776 |
| NSMutableArray exchangeObjectAtIndex | 2.069 |
| NSMutableArray insertObject: atIndex:random | 2.709 |
| CCArray insertObject: atIndex:random | 4.479 |
| CCArray insertObject: atIndex:0 | 8.430 |
| NSMutableArray fast enumeration | 9.353 |
| CCArray indexOfObject | 17.732 |
| CCArray containsObject | 17.799 |
| NSMutableArray indexOfObject | 46.535 |
| NSMutableArray containsObject | 47.374 |
| NSMutableArray makeObjectsPerformSelector | 125.084 |
| NSMutableArray makeObjectsPerformSelector withObject | 137.865 |
| CCArray makeObjectsPerformSelector | 138.679 |
| CCArray makeObjectsPerformSelector withObject | 152.657 |
| CCArray fast enumeration | 333.421 |
| CCArray enumeration | 408.957 |
| NSMutableArray enumeration | 450.680 |
| NSMutableArray add/removeObjectsInArray | 1.223.791 |
| CCArray add/removeObjectsInArray | 2.732.601 |

#### Object Creation

These tests tell you how long it takes to allocate memory, initialize the object, and deallocate it. The longer this takes for an object, the higher the chance that doing this during gameplay will negatively affect performance. Note that **these tests do not give any indication whatsoever of the runtime/rendering performance** of these objects.


| Name | Each (ns) |
| NSAutoreleasePool alloc/init/release | 225 |
| NSObject alloc/init/release | 1.868 |
| CCMoveTo alloc/init/release | 2.869 |
| CCSequence alloc/initOne/release | 3.864 |
| CCNode alloc/init/release | 4.663 |
| CCSprite alloc/initWithFile/release | 21.914 |
| CCParticleSystemQuad 25 particles alloc/init/release | 284.135 |
| CCParticleSystemQuad 250 particles alloc/init/release | 675.596 |
| CCLabelBMFont alloc/initWithString/release | 897.208 |
| CCLabelTTF alloc/initWithString/release | 1.385.200 |
| CCTMXTiledMap small alloc/init/release | 6.494.550 |
| CCTMXTiledMap large alloc/init/release | 492.783.615 |
| CCSprite GCD alloc/initWithFile/release | 12.424.037.083 |

#### Messaging / Function Calls

Low-level overhead for calling C++ functions respectively sending Objective-C messages in various ways.


| Name | Each (ns) |
| ObjC class @public variable | 3 |
| C++ cached virtual method call | 11 |
| C++ virtual method call | 11 |
| IMP-cached message send | 11 |
| Objective-C message send | 34 |
| Objective-C performSelector | 115 |
| ObjC class nonatomic property dot notation | 127 |
| ObjC class atomic property dot notation | 141 |
| ObjC class nonatomic property message send | 160 |
| ObjC class atomic property message send | 164 |
| NSInvocation message send | 2.101 |
| Objective-C CCArray message send | 43.796 |
| Objective-C NSArray message send | 43.829 |
| Objective-C NSArray enumerateWithBlock msg send | 70.741 |
| Objective-C NSArray enumerateWithBlock concurrent msg send | 100.265 |
| Objective-C NSArray makeObjectsPerformSelector | 121.572 |
| Objective-C CCArray makeObjectsPerformSelector | 138.597 |

#### Object Comparison

Compare objects with various methods, and testing if it makes any difference if the test fails (mismatch) or succeeds (match).


| Name | Each (ns) |
| NSObject hash | 35 |
| NSObject is not Equal | 50 |
| NSString isEqual | 50 |
| NSString isEqualToString | 50 |
| NSObject isEqual | 52 |
| isMemberOfClass, class cached | 144 |
| is not MemberOfClass, class cached | 144 |
| NSString hash | 148 |
| isMemberOfClass | 199 |
| is not MemberOfClass | 200 |
| isKindOfClass, class cached | 224 |
| is not KindOfClass, class cached | 260 |
| NSString is not EqualToString | 277 |
| NSString is not Equal | 277 |
| isKindOfClass | 278 |
| is not KindOfClass | 338 |

#### Arithmetic Tests

Simple calculations done frequently in an app, using various data types.


| Name | Each (ns) |
| Double square root | -0 |
| Float division with int conversion | -0 |
| Float square root | -0 |
| Double division with int conversion | -0 |
| Integer multiplication | 0 |
| Integer division | 0 |
| Float multiplication | 5 |
| Double multiplication | 9 |
| Float division | 20 |
| Accelerometer Highpass filter | 20 |
| Double division | 33 |

#### Memory Tests

Allocating and releasing memory.


| Name | Each (ns) |
| 16MB malloc/free | -0 |
| 1MB memcpy | 0 |
| 16 byte memcpy | 0 |
| 16 byte malloc/free | 0 |

#### File IO


| Name | Each (ns) |
| Read 16-byte file | 109.127 |
| Read 16MB file | 110.008 |
| Write 16-byte file | 202.430 |
| Write 16MB file | 219.193 |
| Write 16-byte file (atomic) | 359.137 |
| Write 16MB file (atomic) | 362.201 |

#### Miscellaneous Tests


| Name | Each (ns) |
| Zero-second delayed perform | 7 |
| pthread create/join | 158.470 |

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

So the genetics algorithm test is flawed. The reason is that the MRC version is leaking memory and so not doing the same amount of work as the ARC version. Specifically the - (void) populate; method and the mateWithChromosome methods (or the caller of mateWithChromosome) leak.

I strongly suspect that if you fix the memory leaks in the MRC version and you run your timing around an autoreleasepool block inside the run method you’ll find they compare differently. I’d even hazard to guess that ARC will win instead![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Happy to do that, but … where and why exactly should mateWithChromosome leak? It returns an autoreleased object and the caller puts it in an array. Analyzer has no problems with the code, thought that need not mean anything. I also ran instruments to find leaks, none reported there either. It was my suspicion too that there may be leaks - after all that’s the biggest problem with MRC code, but really couldn’t find anything.

Autoreleasepool is already in place, just one method up in the call stack in MRCTests/ARCTests classes, so I can use NSAutoreleasePoll vs @autoreleasepool accordingly.

I’ll try without the random, though I don’t expect any significant difference.

The other thing, of course, is that the genetic algorithm is not deterministic (uses random in the algorithm) so comparing different runs of it is problematic.

So those “extra” retains that ARC puts in aren’t just there for multi-threaded programs. Every single method or function you call can have side effects, and that includes the possibility of releasing an object you have a reference to in a local variable. It happens pretty rarely in practice, but it does happen. To make things worse, because the time between deallocation and dereferencing is very small, it tends to crash very rarely even when it’s wrong. I’ve spent *hours* debugging issues like that in the past, and they tend to be very non-obvious.

One thing I’d disagree with though is that for a beginner, ARC is conceptually pretty good, but it doesn’t “just work”. As a beginner, ARC and GC are going to be “magical”. With GC it’s darned near impossible to make a mistake, but very easy to do so with ARC. I’ve seen people trying to figure out memory leaks with ARC due to a simple retain cycle (especially with blocks), and their bug random flailing is even worse than with MRC. They don’t have any idea what they are doing and just randomly add weak qualifiers and bridged casts until it works. Then they have crashes from dangling pointers, and even less idea what is wrong. Objective-C in general is just not as beginner friendly as something like Python or C#. While people might conceptually understand what a retain cycle is, my experience is that they don’t know what to do about them until they have to deal with them from MRC.

Agree, specifically ARC & blocks can be difficult. Things like retaining self magically behind the scenes due to a block can drive you nuts.

Fortunately most beginners refrain from using blocks because of their inviting (hah!) syntax.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I came to Obj-C a little before ARC was introduced and thought “you honestly want me to do manual ref-counting?” So of course when it was unveiled at WWDC I jumped on it and immediately converted all my code to use it.

At the time I took Apple’s word for the performance benefits, but the time *not* spent during development/debug was more valuable anyway.

Thanks for the evaluation - it’s great to know it actually is equally fast.

(This was coming from C++, where the things like boost/tr1/C++11 shared_ptr + others would stop you from doing manual memory management.)

The ARC code isn’t thread safe either. The object could be de-allocated before the implicit retain call is made. If you share objects between threads, you’re in for a world of hurt unless they’re guarded by locks.

The ole bait and switch. I was virtually yelling this at my screen before I realized you were being facetious.

“Finally, typically less than 5% of your code contributes to 95% of its runtime performance! It would be downright stupid not to use ARC for the remaining 95%, and hand-tune only the 5% where it’ll make an actual difference in responsiveness, speed or framerate.”

Why is there no like button for comments?![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I love ARC and thanks for the article even through you use Jedi mind tricks to get me to read it.

The big takeaway, for me, is this:

CCParticleSystemQuad 25 particles alloc/init/release 284.135

CCParticleSystemQuad 250 particles alloc/init/release 675.596

It’s only 2.4x longer to have 10x the particles allocated, initialised and released.

Thank you. Very useful information throughout this entire piece.

Hello!

As far as I know, you can use __unsafe_unretained or __weak modifiers to avoid ARC automatic retain/release inserts. I have tested this my own using instruments, but can someone ensure this?

Thanks!

The multithreading argument for putting in the extra retain /release pairs in both of your examples is bogus.

The race condition still exists because the object you are retaining could be deallocated by another thread between you getting the references and the retain message being sent.

In the first case, the array and the objects in it could still be deallocated by another thread between lines 10 and 11. In the second case, the object could be deallocated by another thread at any time before the retain.