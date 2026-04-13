---
title: CCAnimationCache Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_animation_cache/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[CCAnimationCache.h](/)"


[List of all members.](/)


## Detailed Description

Singleton that manages the Animations. It saves in a cache the animations. You should use this class if you want to save your animations in a cache.

Before v0.99.5, the recommend way was to save them on the [CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/). Since v0.99.5, you should use this class instead.

**Since:**- v0.99.5


## Member Function Documentation

| - (void) addAnimation: |
|
([CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) *) |
*animation* |
| name: |
|
(NSString *) |
*name* | |
|
|
| | |

Returns a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) that was previously added. If the name is not found it will return nil. You should retain the returned copy if you are going to use it.

| + (void) purgeSharedAnimationCache |
|
|
|
|

Purges the cache. It releases all the [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) objects and the shared instance.

| - (void) removeAnimationByName: |
|
(NSString *) |
*name* |
|
|

Retruns ths shared instance of the Animation cache


The documentation for this class was generated from the following file: