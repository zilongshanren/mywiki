---
title: Introducing KoboldTouch
url: http://www.learn-cocos2d.com/2012/10/introducing-koboldtouch/
author: Hartmut says
published: '2012-10-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

For tomorrow’s launch of [KoboldTouch](http://www.learn-cocos2d.com/2012/10/essential-cocos2d-koboldtouch/) I made a quick 6-minute presentation about KoboldTouch and what makes it special.

Not everything made it into the presentation. There’s a couple things that may be worth adding or stressing:


First of all, [ARC](http://developer.apple.com/library/mac/#releasenotes/ObjectiveC/RN-TransitioningToARC/Introduction/Introduction.html). Seriously, if you’re not using ARC today, [right now](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/), you’re doing yourself a [HUGE disservice](http://www.learn-cocos2d.com/2012/06/mythbusting-8-reasons-arc/). KoboldTouch does not only allow you to write ARC code, KT itself is written using ARC. You’ll see how much cleaner code gets when you don’t have to consider release, autorelease or retain anymore.

Secondly, [zeroing weak references](http://www.informit.com/articles/article.aspx?p=1806938&seqNum=13) are a fundamental aspect of KoboldTouch development. It makes it so easy to avoid retain cycles, and it makes a couple things easier for you too. For example, if you forget to unregister a delegate - it doesn’t matter! KT classes providing a delegate property declare the delegate as weak reference, so there won’t be a crash if you don’t unregister, and in fact you don’t have to unregister delegates at all.

Classes that can have multiple delegate will clean up the delegates when a scene change occurs. Again this is to prevent crashes or leaks due to accidentally forgetting to unregister a delegate.

Lastly, zeroing weak references enable KoboldTouch to actually **catch and warn about a memory leak**! If shortly after a scene change the previous scene’s reference hasn’t been nil’ed automatically, KoboldTouch knows that the scene is still in memory for whatever reason. This will raise an exception, and then you know about the leak when it first occurs. It’s a lot easier to figure out and fix the cause for such a leak when you’re still aware of the changes you did most recently.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi,

launch time?

2-3 hours from now. Still uploading files.

I’m so excited! This looks like a very big time saver. While I’m here, I have a quick question. I’m using the newest CocosBuilder (2.1) to help with level construction for a game world that spans far beyond the screenSize, but is not a parallax scroll. I’m also using Kobold. To push the very first scene I need to use [CCBReader sceneWithNodeGraphFromFile:@”..”]. With Kobold, the call to push the initial scene is tucked away in the config.lua. How would I go about initializing the first scene with CCBReader while using Kobold?

You can add this to the AppDelegate’s initializationComplete method. If a scene is already setup and running after this method completes, it will not try to load the scene specified in the config.lua.

Ah, I knew I was missing something. Many thanks.