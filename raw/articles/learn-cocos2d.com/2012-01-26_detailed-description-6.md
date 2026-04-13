---
title: Detailed Description
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_scene/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCScene.h>`


[CCScene](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_scene/) is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_node/) that is used only as an abstract concept.

[CCScene](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_scene/) an [CCNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_node/) are almost identical with the difference that [CCScene](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_scene/) has it's anchor point (by default) at the center of the screen.

For the moment [CCScene](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_scene/) has no other logic than that, but in future releases it might have additional logic.

It is a good practice to use and [CCScene](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_scene/) as the parent of all your nodes.