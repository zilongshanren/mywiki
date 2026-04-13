---
title: CCAnimate Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_animate/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCActionInterval.h](http://www.learn-cocos2d.com/)"

Inherits [CCActionInterval](http://www.learn-cocos2d.com/).

| (id) | -
|

Animates a sprite given the name of an Animation

creates the action with an Animation and will restore the original frame when the animation is over

creates the action with an Animation

| + (id) actionWithDuration: | (
|

creates an action with a duration, animation and depending of the restoreOriginalFrame, it will restore the original frame or not. The 'delay' parameter of the animation will be overrided by the duration parameter.

initializes the action with an Animation and will restore the original frame when the animtion is over

initializes the action with an Animation

| - (id) initWithDuration: | (
|

initializes an action with a duration, animation and depending of the restoreOriginalFrame, it will restore the original frame or not. The 'delay' parameter of the animation will be overrided by the duration parameter.