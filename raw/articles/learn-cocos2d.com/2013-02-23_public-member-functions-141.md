---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_image/
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

[CCMenuItemImage](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_image/) accepts images as items. The images has 3 different states:

For best results try that all images are of the same size

| - (id) initWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|
| disabledImage: | (NSString *) | value3 |
|
| block: | (id sender) | block |
|

initializes a menu item with a normal, selected and disabled image with a block. The block will be "copied".

| - (id) initWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|
| disabledImage: | (NSString *) | value3 |
|
| target: | (id) | r |
|
| selector: | (SEL) | s |
|

initializes a menu item with a normal, selected and disabled image with target/selector. The "target" won't be retained.

| + (id) itemWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|

creates a menu item with a normal and selected image

| + (id) itemWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|
| block: | (id sender) | block |
|

creates a menu item with a normal and selected image with a block. The block will be "copied".

| + (id) itemWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|
| disabledImage: | (NSString *) | value3 |
|

creates a menu item with a normal, selected and disabled image

| + (id) itemWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|
| disabledImage: | (NSString *) | value3 |
|
| block: | (id sender) | block |
|

creates a menu item with a normal, selected and disabled image with a block. The block will be "copied".

| + (id) itemWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|
| disabledImage: | (NSString *) | value3 |
|
| target: | (id) | r |
|
| selector: | (SEL) | s |
|

creates a menu item with a normal, selected and disabled image with target/selector. The "target" won't be retained.

| + (id) itemWithNormalImage: | (NSString *) | value |
|
| selectedImage: | (NSString *) | value2 |
|
| target: | (id) | r |
|
| selector: | (SEL) | s |
|

creates a menu item with a normal and selected image with target/selector

sets the sprite frame for the disabled image

sets the sprite frame for the selected image