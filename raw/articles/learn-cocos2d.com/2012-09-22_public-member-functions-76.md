---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_menu_item_atlas_font/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.0
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCMenuItem.h>`


| (id) | -
|

| - (id) initWithString: | (NSString *) | value |
|
| charMapFile: | (NSString *) | charMapFile |
|
| itemWidth: | (int) | itemWidth |
|
| itemHeight: | (int) | itemHeight |
|
| startCharMap: | (char) | startCharMap |
|
| block: | (id sender) | block |
|

initializes a menu item from a string and atlas with a block. The block will be "copied".

| - (id) initWithString: | (NSString *) | value |
|
| charMapFile: | (NSString *) | charMapFile |
|
| itemWidth: | (int) | itemWidth |
|
| itemHeight: | (int) | itemHeight |
|
| startCharMap: | (char) | startCharMap |
|
| target: | (id) | target |
|
| selector: | (SEL) | selector |
|

initializes a menu item from a string and atlas with a target/selector. The "target" won't be retained.

| + (id) itemWithString: | (NSString *) | value |
|
| charMapFile: | (NSString *) | charMapFile |
|
| itemWidth: | (int) | itemWidth |
|
| itemHeight: | (int) | itemHeight |
|
| startCharMap: | (char) | startCharMap |
|

creates a menu item from a string and atlas with a target/selector

| + (id) itemWithString: | (NSString *) | value |
|
| charMapFile: | (NSString *) | charMapFile |
|
| itemWidth: | (int) | itemWidth |
|
| itemHeight: | (int) | itemHeight |
|
| startCharMap: | (char) | startCharMap |
|
| block: | (id sender) | block |
|

| + (id) itemWithString: | (NSString *) | value |
|
| charMapFile: | (NSString *) | charMapFile |
|
| itemWidth: | (int) | itemWidth |
|
| itemHeight: | (int) | itemHeight |
|
| startCharMap: | (char) | startCharMap |
|
| target: | (id) | target |
|
| selector: | (SEL) | selector |
|