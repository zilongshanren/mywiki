---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_animation_cache/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCAnimationCache.h>`


| void |
|

Singleton that manages the Animations. It saves in a cache the animations. You should use this class if you want to save your animations in a cache.

Before v0.99.5, the recommend way was to save them on the [CCSprite](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite/). Since v0.99.5, you should use this class instead.

| void CCAnimationCache::purgeSharedAnimationCache | ( | ) | ` [static, virtual]` |

| void CCAnimationCache::removeAnimationByName: | ( | NSString * | name | ) | ` [virtual]` |

Retruns ths shared instance of the Animation cache