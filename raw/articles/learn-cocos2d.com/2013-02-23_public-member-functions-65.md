---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_atlas_node/
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

`#import <CCAtlasNode.h>`


| (id) | -
|

[CCAtlasNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_atlas_node/) is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) that implements the [CCRGBAProtocol](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/protocol_c_c_r_g_b_a_protocol-p/) and [CCTextureProtocol](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/protocol_c_c_texture_protocol-p/) protocol

It knows how to render a TextureAtlas object. If you are going to render a TextureAtlas consider sub-classing [CCAtlasNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_atlas_node/) (or a subclass of [CCAtlasNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_atlas_node/))

All features from [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) are valid, plus the following features:

| + (id) atlasWithTileFile: | (NSString *) | tile |
|
| tileWidth: | (NSUInteger) | w |
|
| tileHeight: | (NSUInteger) | h |
|
| itemsToRender: | (NSUInteger) | c |
|

| - (id) initWithTileFile: | (NSString *) | tile |
|
| tileWidth: | (NSUInteger) | w |
|
| tileHeight: | (NSUInteger) | h |
|
| itemsToRender: | (NSUInteger) | c |
|

updates the Atlas (indexed vertex array). Shall be overridden in subclasses