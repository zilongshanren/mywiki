---
title: Learn & Master Cocos2D for iPhone Game Dev
url: http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/14127-how-much-memory-ram-is-available-on-the-iphoneipodipad/
author: Max says
published: '2010-10-13'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[FAQ: cocos2d for iPhone](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/): How much memory (RAM) is available on the iPhone/iPod/iPad?

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**Note:**please do not share direct download links to PDF files, the download links expire after a couple minutes!

As of May 2010 there are two device classes in terms of how much memory (RAM) they have installed.

**iPhone/iPod 1st & 2nd generation: 128 MB RAM****iPhone 3GS, iPod 3rd generation & iPad: 256 MB RAM**

The iPhone OS itself takes a large chunk from the memory so what you see as available memory is a lot less than the installed memory. Moreover the amount of available memory fluctuates and depends on the software installed on the device and in future (with iPhone OS 4) even which background tasks are running.

There's a general consensus among iPhone developers that you can get at the very most 35 MB of available memory on a 128 MB device. However, this best-case scenario is hardly ever seen. If you want to be relatively certain to avoid any memory warnings from the iPhone **on a 128 MB device** then **expect no more than 20-25 MB to be available** to your app. If you use around and above 25 MB of memory your app is likely going to receive memory warnings, at which point you should be able to free some more memory, otherwise your app may simply be closed by the iPhone OS.

On the 256 MB device class things are a lot better. The most available memory you can get on an iPhone 3GS or iPad is around 115-125 MB. You may start receiving memory warnings at around 90-100 MB so **for the best experience keep your memory usage below 90 MB on a 256 MB device** - that's still around 4 times more available memory than on the 128 MB devices.

If you want to be able to see the available memory on your device programmatically, check out my [free source code collection](http://www.learn-cocos2d.com/knowledge-base/free-source-code/). There's a utility class with which you can get the available amount of free memory on your device. I actually hacked cocos2d's CCDirector so that it would show me the available memory instead of the framerate.

Enlightening post. Thanks!

And, of course, I have a few question


- everything is relative, but for common code is better to use NSString, NSArray (and pay the cost of creating new objects) or the mutable ones? Which can be the parameters to choose between each one?

- I am wondering if the new iPhone 4.0′s greater performance will be an issue. Games that run smoothly in iPhone 1st and 2nd generation devices will probably run too fast?

Hi Max,

i doubt the NSMutable* datasets are performance killers. I haven’t made any tests but i’m pretty sure that if you don’t change them at all they’ll probably perform just as good as the non-mutable ones. Now, once you *do* need to change the arrays or strings it’s good to have them mutable so that stuff is taken care for you behind the scenes. On the other hand, if you know that you’ll only be creating the items once but never re-order, remove or add others then use the non-mutable ones. For me it’s a matter of use case rather than performance.

Games won’t run faster on newer devices. cocos2d’s CCDirector makes sure of that. You do get better framerates of course but not faster gameplay. That holds true for all modern game engines.