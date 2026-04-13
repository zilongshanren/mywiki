---
title: Cocos2D got forked …
url: http://www.learn-cocos2d.com/2015/06/cocos2d-forked/
published: '2015-06-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Cocos2D “for iPhone” (as in: Objective-C) now has two forks:

[Cocos2D-ObjC](https://github.com/cocos2d/cocos2d-objc)maintained by Lars Birkemose. This fork builds on v3.4 with a focus on making Cocos2D easier to use for beginners. Its website is[cocos2d-objc.org](http://cocos2d-objc.org/).[Cocos2D-SpriteBuilder](https://github.com/spritebuilder/cocos2d-spritebuilder)maintained by Scott Lembcke and others. This fork is currently at v3.4 also but will soon have a v4 release. Its website is[spritebuilder.com](http://www.spritebuilder.com/).

### How did this happen?

[Scott’s thread](http://forum.spritebuilder.com/t/the-future-of-cocos2d-spritebuilder/) explains it to some degree. There’s more info on the [-ObjC thread](http://forum.cocos2d-objc.org/t/the-new-objc-site/). And the [-ObjC mini roadmap](http://forum.cocos2d-objc.org/t/the-cocos2d-objc-mini-roadmap/17316) provides some more insight.

**Long story short:** Lars and Scott disagree on the direction of Cocos2D. Lars continues with the version 3.4 of Cocos2D before any work on v4 has started. Naturally Cocos2D-SpriteBuilder will soon **be** the previously announced v4.

This happened shortly after Apportable stopped sponsoring the development of new Cocos2D/SpriteBuilder features. For Lars, Cocos2D was becoming this big chunk of support code for SpriteBuilder, and he’s now trying to turn the ship around.

### Double-fork all the way - what does it mean?


To the best of my assessment and what’s been posted, it means that Cocos2D-ObjC is heading towards a Cocos2D as it was in the times of cocos2d-iphone v1 and v2 - not technically but in terms of keeping the core framework plain and simple, with optional features available as add-ons/add-ins or extensions, all code contained within a single Xcode project/target and re-adding the Xcode templates.

Whereas Cocos2D-SpriteBuilder will continue the path of integration with SpriteBuilder. It will also contain the work that has been put into v4, another decluttering and modernizing the core framework, for instance by replacing CCFileUtils and providing a threaded renderer. [Check out the v4 roadmap](https://docs.google.com/document/d/1owIKJQ7ftHM0psddlrunpEwTkunqsBy17wWPv-KUyWM/edit#heading=h.hu07lx31ymvd) but keep in mind that this was an initial plan and does not indicate current development status or plans anymore. Moreover SpriteBuilder itself will continue to be updated.

That said, it seems likely that Cocos2D-ObjC will eventually break away from SpriteBuilder, too.

How you look at this personally will mostly depend on whether you’re a barebones programmer and text wrangler or rather enjoy the benefits of visual editing and getting certain menial tasks taken care of but also taken away from your (immediate) control while not double-questioning every other class’ existence in the project.

### Which one do I choose?

If you like SpriteBuilder or visual editing in general, you go with Cocos2D-SpriteBuilder.

If you like all your project to be code and data under your control, your best bet will be Cocos2D-ObjC at this time.

However with the pending release of Cocos2D-SpriteBuilder v4 you should look into those changes. After all, Cocos2D-SpriteBuilder can be used as a code-only framework, too. The only caveat being that you need SpriteBuilder to create the initial project, and depending on how touchy you are on this subject, you may optionally feel the need to remove certain folders/resources from the project, such as items needed only for Android builds.

I know that causes some bad stomach feeling for some developers. If that’s the case for you, you will probably want to use/support the Cocos2D-ObjC fork.

### What about Apportable?

I’m afraid I can’t say much about it, except for what’s been said already: Apportable no longer pays the CC/SB developers (as in: no longer sponsoring CC/SB), including myself.

Apportable continues to offer the SpriteBuilder Android plugins in the [SpriteBuilder Store](https://store.spritebuilder.com/), and they are about to launch their other project named [Tengu](http://www.tengu.com/).

Note that these two projects are essentially the same technology, except that SB Android is aimed at game developers using CC/SB or porting a CC/SB project whereas Tengu is aimed at UIKit developers launching new projects.

### /me last words

Personally, I’m very grateful having gotten the chance to write [Learn SpriteBuilder](http://www.apress.com/9781484202630) among many other things while doing [my part](https://www.makeschool.com/docs/) for Apportable. But this change in time allotment also gave me a welcome “time off” and the opportunity to start working on [TilemapKit](http://tilemapkit.com/), a tilemap game development framework for Cocos2D and Sprite Kit.

And if you ask me personally where I stand on the issue of two forks, I will say that I’d rather have them spoon. 😀

But seriously, I think both projects have merit and the thing with forks this fresh is whether both can attract a decent following from the start and are henceforth continuously maintained and updated, and actually differ on things that matter to users. Perhaps this forking will even motivate both parties to better their own respective forks. In a way it also doubles the chances for the Objective-C version of Cocos2D to stay meaningful, one fork or the other.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |