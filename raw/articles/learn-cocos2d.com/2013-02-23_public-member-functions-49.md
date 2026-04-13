---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_menu_item_font/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-mac
2.1
Improved Cocos2D API Reference (Mac OS X version) for www.kobold2d.com developers
|

`#import <CCMenuItem.h>`


| (id) | -
|

| - (id) initWithString: | (NSString *) | value |
|
| block: | (id sender) | block |
|

initializes a menu item from a string with the specified block. The block will be "copied".

| - (id) initWithString: | (NSString *) | value |
|
| target: | (id) | r |
|
| selector: | (SEL) | s |
|

initializes a menu item from a string with a target/selector The "target" won't be retained.

creates a menu item from a string with the specified block. The block will be "copied".

creates a menu item from a string with a target/selector. The "target" won't be retained.