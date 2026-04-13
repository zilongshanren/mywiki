---
title: CCMenuItemToggle Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_toggle/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCMenuItem.h](http://www.learn-cocos2d.com/)"

Inherits [CCMenuItem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/), and [CCRGBAProtocol-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/).

| (id) | -
|

A [CCMenuItemToggle](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_toggle/) A simple container class that "toggles" it's inner items The inner itmes can be any MenuItem

initializes a menu item from a list of items with a target selector

| + (id) itemWithTarget: | (id) | t |
||
| selector: | (SEL) | s |
||
| items: | (
|

creates a menu item from a list of items with a target/selector

- (NSUInteger) selectedIndex` [read, write, assign]` |

returns the selected item

- (NSMutableArray*) subItems` [read, write, retain]` |

NSMutableArray that contains the subitems. You can add/remove items in runtime, and you can replace the array with a new one.