---
title: CCAtlasNode Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_atlas_node/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCAtlasNode.h](http://www.learn-cocos2d.com/)"

Inherits [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/), [CCRGBAProtocol-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/), and [CCTextureProtocol-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_texture_protocol-p/).

Inherited by [CCLabelAtlas](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_label_atlas/), and [CCTileMapAtlas](http://www.learn-cocos2d.com/).

| (id) | -
|

[CCAtlasNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_atlas_node/) is a subclass of [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) that implements the [CCRGBAProtocol](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/) and [CCTextureProtocol](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_texture_protocol-p/) protocol

It knows how to render a TextureAtlas object. If you are going to render a TextureAtlas consider subclassing [CCAtlasNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_atlas_node/) (or a subclass of [CCAtlasNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_atlas_node/))

All features from [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) are valid, plus the following features:

| + (id) atlasWithTileFile: | (NSString *) | tile |
||
| tileWidth: | (int) | w |
||
| tileHeight: | (int) | h |
||
| itemsToRender: | (int) | c | ||

| - (id) initWithTileFile: | (NSString *) | tile |
||
| tileWidth: | (int) | w |
||
| tileHeight: | (int) | h |
||
| itemsToRender: | (int) | c | ||

| - (void) updateAtlasValues |

updates the Atlas (indexed vertex array). Shall be overriden in subclasses