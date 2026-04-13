---
title: iPhone Performance Killers
url: http://www.learn-cocos2d.com/2011/03/iphone-performance-killers/
author: Dad says
published: '2011-03-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Have a look at the following code, and then answer these questions before reading on:

- Which function will run faster?
- What will be the framerate for each function when run 100 times per frame on an iPhone 3G?
- Will wrapping the 100 calls to function1 in an NSAutoreleasePool show any difference?

[cc lang=”ObjC” height=”465″]

-(void) function1

{

CGPoint pos = [self position];

id x = [NSNumber numberWithFloat:pos.x];

id y = [NSNumber numberWithFloat:pos.y];

id objects = [NSArray arrayWithObjects:x, y, nil];

id keys = [NSArray arrayWithObjects:@”x”, @”y”, nil];

id dict = [NSDictionary dictionaryWithObjects:objects forKeys:keys];

dict; // avoid compiler warning, is a noop

}

-(void) function2

{

CGPoint pos = [self position];

id x = [[NSNumber alloc] initWithFloat:pos.x];

id y = [[NSNumber alloc] initWithFloat:pos.y];

id objects = [[NSArray alloc] initWithObjects:x, y, nil];

id keys = [[NSArray alloc] initWithObjects:@”x”, @”y”, nil];

id dict = [[NSDictionary alloc] initWithObjects:objects forKeys:keys];

[x release];

[y release];

[objects release];

[keys release];

[dict release];

}

[/cc]

### The Answers

- Which function will run faster?
**Answer:**function1 - What will be the framerate for each function when run 100 times per frame on an iPhone 3G?
**Answer:**27 fps for function1 and 24 fps for function2. - Will wrapping the 100 calls to function1 in an NSAutoreleasePool show any difference?
**Answer:**no, but memory of temporary objects is released immediately.

Needless to say, on an iPod (4th Generation) and an iPad these tests all run at 60 fps and give no indication whatsoever that the performance on an iPhone 3G would suffer this much (and neither does the Simulator, of course). All the more reason to test early and often on older devices.

#### To autorelease or not?

Common wisdom may tell you that alloc/release is faster than autorelease. Even Apple recommends avoiding autorelease, right?

Not quite, because this is often misunderstood: Apple recommends to avoid autorelease but only for functions which create a lot of temporary objects and because of the constrained memory - not because it’s slow or even dangerous - [autorelease is not dangerous](http://stackoverflow.com/questions/613583/why-is-autorelease-especially-dangerous-expensive-for-iphone-applications).

Since memory is so constrained on 1st and 2nd generation iOS devices, it’s best to release that memory as soon as possible and don’t leave it allocated for longer than necessary. To achieve this, you can choose to do two things in this case: use alloc/release or [enclose the loop in an NSAutoreleasePool](http://stackoverflow.com/questions/65427/how-does-the-nsautoreleasepool-autorelease-pool-work). The latter option is preferred since it will release the memory right away, and not some time later. And autorelease is generally preferable because you will never, ever forget to send a release message to an object - which means it’ll be leaked and forever use up memory.

You can write well-performing, even better-performing code by using autorelease and using NSAutoreleasePool around tight loops creating many temporary autorelease objects.

#### Innocent looking code kills framerate

Did you expect that creating 100 rather simple NSDictionary instances each frame would drag the framerate down to around 24-27 fps? Me neither. I knew the code wasn’t going to be blazing fast, but I never expected it to have such an impact. However, it can be optimized somewhat since I’m unnecessarily creating two NSArray instances to hold the keys and values respectively before using them to create the NSDictionary. In fact we can get rid of them by using dictionaryWithObjectsAndKeys and doing this in a single step:

[cc lang=”ObjC”]

-(void) function1Optimized

{

CGPoint pos = [self position];

id x = [NSNumber numberWithFloat:pos.x];

id y = [NSNumber numberWithFloat:pos.y];

id dict = [NSDictionary dictionaryWithObjectsAndKeys:x, @”x”, y, @”y”, nil];

dict; // avoid compiler warning, is a noop

}

[/cc]

Sometimes it helps to look around what other ways there are to run the same code. In terms of performance this is an order of a magnitude faster and now clocks in at 42 fps. Still not good enough for realtime rendering obviously but an improvement of over 50% by cutting two NSArray allocations is a very simple and effective optimization.

Just as a general guideline, when I get rid of the two NSNumber instances and simply pass empty strings for x and y the framerate went back up to 60 fps. Of course that’s over-optimizing to the point where the code doesn’t work anymore. It just goes to show how expensive the creation of NSDictionary and NSArray are, as is wrapping simple types in NSNumber or NSValue objects.

If you can avoid allocation and temporary objects, avoid it. If you can’t, at least avoid creating temporary objects every frame. Re-use objects as much as possible. Unfortunately, that’s not an option for NSNumber objects since you can’t change the value of a NSNumber instance.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Allocating memory hundreds of times during the core game loop is always going to hurt performance. Pre-allocate memory wherever possible. Even just doing one big allocation at the start of each loop will be faster than lots of little ones during the loop (though allocating outside the loop and re-using is even better, of course).

Even in the optimized version you are talking about:

- method call to get position

- 2x : memory allocation, init method call, set float method call, assign float values, etc.

- memory allocation (Dict, + its internal Arrays etc with multiple method calls), four retain calls to add the two objects and two keys to the dictionary.

-

at minimum (probably much more). And you’re doing that 100 times each 1/60th of a second, or 6000 times a second? ouch!

Why use NSNumbers and NSDictionary for this? Unless you are storing a bunch of other stuff in the dictionaries, using it for only two known constant keys and their values seems unnecessary. A pre-allocated array of simple x,y structs would be dramatically faster. Likely you are using those floats at some point and are having to pull them out of the NSNumbers and then deallocate the NSNumbers.

If you had an array of structs that was pre-allocated and a marker to know where the “next” slot to use was, this would only involve:

- method call to get the point

- two float assignments

- increment slot marker (int).

quite a bit fewer operations to perform and no memory allocations == way faster!

obviously, the context may not permit this, but it’s worth remembering that ObjectiveC allows C code in cases where you don’t need the abstraction and convenience of OOP and _do_ need performance.

The reason here is that this is the way how Wax treats Lua tables internally as NSDictionary and numbers as NSNumber.

The function timings cannot really be compared, because function1 has not yet released it’s objects. function2 is measuring the speed of allocation and deallocation, whereas function1’s objects will not be deallocated until the autorelease pool is drained (causing a slow down later on in execution).

Arrr …. of course, good point! I should have used a local NSAutoreleasePool for the test.