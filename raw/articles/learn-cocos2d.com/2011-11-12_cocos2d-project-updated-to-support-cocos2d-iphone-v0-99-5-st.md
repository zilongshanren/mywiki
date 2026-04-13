---
title: Cocos2D-Project updated to support Cocos2D-iPhone v0.99.5 stable
url: http://www.learn-cocos2d.com/2011/01/cocos2dproject-updated-support-cocos2diphone-v0995-stable/
author: Snake says
published: '2011-11-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I almost forgot about the [Cocos2D-Project on github](https://github.com/GamingHorror/cocos2d-project). While it works flawlessly with the latest v0.99.5 stable release of Cocos2D, it was still bundled with only the RC1 (release candidate). So I’ve updated the cocos2d version in the repository.

### In case you don’t know what Cocos2D-Project is:

Cocos2D-Project is a great way to start any Cocos2D-iPhone based project.

It eases up- and downgrading the Cocos2D game engine at any time. It includes additional source code as well as multiple targets and build configurations for Ad Hoc & App Store distribution (creates the necessary IPA/ZIP files) and debugging of memory leaks and related issues.

Cocos2D-Project is free, open-source, uses the MIT License and comes already bundled with the cocos2d-iphone version that it currently works with “out of the box”.

It’s not affiliated with or endorsed by [cocos2d-iphone.org](http://cocos2d-iphone.org/) and Ricardo Quesada. You will get support for Cocos2D-Project on [Cocos2D Central](http://cocos2d-central.com/).

### Future updates

With the help of others, the Cocos2D-Project development has taken on a life of its own. The current work in progress is much more than a simple Xcode project referencing just the Cocos2D game engine. I’m looking forward to announce a big update in a couple weeks. Stay tuned.

|
|

I used the old template , it seems to be working fine. But one thing is that how could I disable Cocos2d’s debug output (like alloc and release) in debug mode?

there’s a macro defined in Build Settings: COCOS2D_DEBUG=1

if you change it to 0 it will disable all logging, eg the CCLOG macro won’t print anything to the console anymore