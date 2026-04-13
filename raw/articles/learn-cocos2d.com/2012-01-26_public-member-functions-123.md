---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_menu_item_atlas_font/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCMenuItem.h>`


| id |
|

| id CCMenuItemAtlasFont::initFromString:charMapFile:itemWidth:itemHeight:startCharMap:target:selector: | ( | NSString * | value, |
| [charMapFile] NSString * | charMapFile, |
||
| [itemWidth] int | itemWidth, |
||
| [itemHeight] int | itemHeight, |
||
| [startCharMap] char | startCharMap, |
||
| [target] id | rec, |
||
| [selector] SEL | cb |
||
| ) | ` [virtual]` |

initializes a menu item from a string and atlas with a target/selector

| id CCMenuItemAtlasFont::itemFromString:charMapFile:itemWidth:itemHeight:startCharMap: | ( | NSString * | value, |
| [charMapFile] NSString * | charMapFile, |
||
| [itemWidth] int | itemWidth, |
||
| [itemHeight] int | itemHeight, |
||
| [startCharMap] char | startCharMap |
||
| ) | ` [static, virtual]` |

creates a menu item from a string and atlas with a target/selector

| id CCMenuItemAtlasFont::itemFromString:charMapFile:itemWidth:itemHeight:startCharMap:target:selector: | ( | NSString * | value, |
| [charMapFile] NSString * | charMapFile, |
||
| [itemWidth] int | itemWidth, |
||
| [itemHeight] int | itemHeight, |
||
| [startCharMap] char | startCharMap, |
||
| [target] id | rec, |
||
| [selector] SEL | cb |
||
| ) | ` [static, virtual]` |

creates a menu item from a string and atlas. Use it with MenuItemToggle