---
title: CCMenuItemSprite Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_sprite/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCMenuItem.h](http://www.learn-cocos2d.com/)"

Inherits [CCMenuItem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/), and [CCRGBAProtocol-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/).

Inherited by [CCMenuItemImage](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_image/).

| (id) | -
|

[CCMenuItemSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_sprite/) accepts [CCNode<CCRGBAProtocol>](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) objects as items. The images has 3 different states:

| - (id) initFromNormalSprite: | (
|

initializes a menu item with a normal, selected and disabled image with target/selector

| + (id) itemFromNormalSprite: | (
|

creates a menu item with a normal and selected image

| + (id) itemFromNormalSprite: | (
|

creates a menu item with a normal,selected and disabled image with target/selector

| + (id) itemFromNormalSprite: | (
|

creates a menu item with a normal and selected image with target/selector

the image used when the item is disabled

the image used when the item is not selected

the image used when the item is selected