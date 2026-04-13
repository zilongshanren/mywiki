---
title: 'Cool KoboldTouch Features: Weak Typing and Controller Sharing'
url: http://www.learn-cocos2d.com/2012/11/koboldtouch-cool-features-weak-typing-controller-sharing/
published: '2012-11-02'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I recorded two insanely great, beautiful, amazing, wonderful (I’ve been watching Steve Jobs’ keynotes recently, it must be rubbing off a bit) feature presentations to explain two cool features in [KoboldTouch](http://www.koboldtouch.com/).

### Weak Typing

Weak typing allows you to create, read and assign variables just by name. You don’t have to declare the variable, just assign a value. No need to change the interface, and works with all KTModel classes.

Access is almost as fast as property access, and the values are mutable thanks to the KTMutableNumber implementation which feels like NSNumber except that it doesn’t create and release new objects every time you need to change a value.

### Controller Sharing


Controller sharing solves the common problem of getting two unrelated objects to communicate with each other. Of course you need references to do that, but where to put them? Hopefully not in a singleton, or else you open the portal to retain cycle/memory leak hell.

KoboldTouch has an elegant, remarkable, amazing (here it is again) solution for this problem: register any controller by (unique) name on the scene ViewController, and then get the controller back by its name or class. No interface changes needed, no retain cycles (as long as you declare any caching ivar/property referencing that foreign controller as weak).

### Outtake

In this short outtake I struggle to get past a certain word… ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)



|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |