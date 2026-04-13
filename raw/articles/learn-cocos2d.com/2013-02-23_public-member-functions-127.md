---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_atlas/
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

`#import <CCLabelAtlas.h>`


| (id) | -
|

[CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_atlas/) is a subclass of [CCAtlasNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_atlas_node/).

It can be as a replacement of CCLabel since it is MUCH faster.

[CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_atlas/) versus CCLabel:

A more flexible class is [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_b_m_font/). It supports variable width characters and it also has a nice editor.

| - (id) initWithString: | (NSString *) | string |
|
| charMapFile: | (NSString *) | charmapfile |
|
| itemWidth: | (NSUInteger) | w |
|
| itemHeight: | (NSUInteger) | h |
|
| startCharMap: | (NSUInteger) | firstElement |
|

| - (id) initWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fontFile |
|

| + (id) labelWithString: | (NSString *) | string |
|
| charMapFile: | (NSString *) | charmapfile |
|
| itemWidth: | (NSUInteger) | w |
|
| itemHeight: | (NSUInteger) | h |
|
| startCharMap: | (NSUInteger) | firstElement |
|

| + (id) labelWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fontFile |
|