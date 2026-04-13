---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_sprite/
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

[CCMenuItemSprite](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_sprite/) accepts [CCNode<CCRGBAProtocol>](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) objects as items. The images has 3 different states:

| - (id) initWithNormalSprite: | (
|

initializes a menu item with a normal, selected and disabled image with a block. The block will be "copied".

| - (id) initWithNormalSprite: | (
|

initializes a menu item with a normal, selected and disabled image with target/selector. The "target" won't be retained.

| + (id) itemWithNormalSprite: | (
|

creates a menu item with a normal and selected image

| + (id) itemWithNormalSprite: | (
|

creates a menu item with a normal and selected image with a block. The block will be "copied".

| + (id) itemWithNormalSprite: | (
|

creates a menu item with a normal, selected and disabled image with a block. The block will be "copied".

| + (id) itemWithNormalSprite: | (
|

creates a menu item with a normal, selected and disabled image with target/selector. The "target" won't be retained.

| + (id) itemWithNormalSprite: | (
|

creates a menu item with a normal and selected image with target/selector. The "target" won't be retained.

the image used when the item is disabled

the image used when the item is not selected

the image used when the item is selected