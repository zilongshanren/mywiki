---
title: CCMenuItemImage Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_image/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCMenuItem.h](http://www.learn-cocos2d.com/)"

Inherits [CCMenuItemSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_sprite/).

| (id) | -
|

[CCMenuItemImage](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_image/) accepts images as items. The images has 3 different states:

For best results try that all images are of the same size

| - (id) initFromNormalImage: | (NSString *) | value |
||
| selectedImage: | (NSString *) | value2 |
||
| disabledImage: | (NSString *) | value3 |
||
| target: | (id) | r |
||
| selector: | (SEL) | s | ||

initializes a menu item with a normal, selected and disabled image with target/selector

| + (id) itemFromNormalImage: | (NSString *) | value |
||
| selectedImage: | (NSString *) | value2 | ||

creates a menu item with a normal and selected image

| + (id) itemFromNormalImage: | (NSString *) | value |
||
| selectedImage: | (NSString *) | value2 |
||
| disabledImage: | (NSString *) | value3 |
||
| target: | (id) | r |
||
| selector: | (SEL) | s | ||

creates a menu item with a normal,selected and disabled image with target/selector

| + (id) itemFromNormalImage: | (NSString *) | value |
||
| selectedImage: | (NSString *) | value2 |
||
| target: | (id) | r |
||
| selector: | (SEL) | s | ||

creates a menu item with a normal and selected image with target/selector