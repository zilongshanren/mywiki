---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCMenuItem.h>`


| (id) | -
|

[CCMenuItem](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item/) base class

Subclass [CCMenuItem](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item/) (or any subclass) to create your custom [CCMenuItem](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item/) objects.

| - (id) initWithTarget: | (id) | target |
|
| selector: | (SEL) | selector |
|

| + (id) itemWithTarget: | (id) | target |
|
| selector: | (SEL) | selector |
|

Sets the block that is called when the item is tapped. The block will be "copied".

| - (void) setTarget: | (id) | target |
|
| selector: | (SEL) | selector |
|

Sets the target and selector that is called when the item is tapped. target/selector will be implemented using blocks. "target" won't be retained.

If enabled, it releases the block at cleanup time.