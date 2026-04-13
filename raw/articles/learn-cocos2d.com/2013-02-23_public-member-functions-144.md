---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_toggle/
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

A [CCMenuItemToggle](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_toggle/) A simple container class that "toggles" its inner items The inner itmes can be any MenuItem

| - (id) initWithItems: | (NSArray *) | arrayOfItems |
|
| block: | (id) | block |
|

initializes a menu item from a list of items with a block. The block will be "copied".

creates a menu item from a list of items and executes the given block when the item is selected. The block will be "copied".

| + (id) itemWithTarget: | (id) | target |
|
| selector: | (SEL) | selector |
|
| items: | (
|

creates a menu item from a list of items with a target/selector

NSMutableArray that contains the subitems. You can add/remove items in runtime, and you can replace the array with a new one.