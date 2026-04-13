---
title: CCMenuItemLabel Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_label/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCMenuItem.h](http://www.learn-cocos2d.com/)"

Inherits [CCMenuItem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/), and [CCRGBAProtocol-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/).

Inherited by [CCMenuItemAtlasFont](http://www.learn-cocos2d.com/), and [CCMenuItemFont](http://www.learn-cocos2d.com/).

| (id) | -
|

An abstract class for "label" [CCMenuItemLabel](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_label/) items Any [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) that supports the [CCLabelProtocol](http://www.learn-cocos2d.com/) protocol can be added. Supported nodes:

| - (void) setIsEnabled: | (BOOL) | enabled |

| - (void) setString: | (NSString *) | label |

sets a new string to the inner label