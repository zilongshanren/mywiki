---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_t_m_x_layer/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCTMXLayer.h>`


| (id) | -
|

[CCTMXLayer](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_t_m_x_layer/) represents the TMX layer.

It is a subclass of [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/). By default the tiles are rendered using a [CCTextureAtlas](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_texture_atlas/). If you mofify a tile on runtime, then, that tile will become a [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/), otherwise no [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) objects are created. The benefits of using [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) objects as tiles are:

cocos2d v2.0 doesn't support the cc_vertexz value. Whenever a the cc_vertexz property is found, it will raise an exception.

"value" by default is 0, but you can change it from Tiled by adding the "cc_alpha_func" property to the layer. The value 0 should work for most cases, but if you have tiles that are semi-transparent, then you might want to use a differnt value, like 0.5.

For further information, please see the programming guide:

Tiles can have tile flags for additional properties. At the moment only flip horizontal and flip vertical are used. These bit flags are defined in CCTMXXMLParser.h.

returns the position in points of a given tile coordinate

dealloc the map that contains the tile position from memory. Unless you want to know at runtime the tiles positions, you can safely call this method. If you are going to call [layer tileGIDAt:] then, don't release the map

| - (void) setTileGID: | (uint32_t) | gid |
|
| at: | (CGPoint) | tileCoordinate |
|

sets the tile gid (gid = tile global id) at a given tile coordinate. The Tile GID can be obtained by using the method "tileGIDAt" or by using the TMX editor -> Tileset Mgr +1. If a tile is already placed at that position, then it will be removed.

| - (void) setTileGID: | (uint32_t) | gid |
|
| at: | (CGPoint) | pos |
|
| withFlags: | (ccTMXTileFlags) | flags |
|

sets the tile gid (gid = tile global id) at a given tile coordinate. The Tile GID can be obtained by using the method "tileGIDAt" or by using the TMX editor -> Tileset Mgr +1. If a tile is already placed at that position, then it will be removed.

Use withFlags if the tile flags need to be changed as well

returns the tile ([CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/)) at a given a tile coordinate. The returned [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) will be already added to the [CCTMXLayer](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_t_m_x_layer/). Don't add it again. The [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) can be treated like any other [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/): rotated, scaled, translated, opacity, color, etc. You can remove either by calling:

returns the tile gid at a given tile coordinate. if it returns 0, it means that the tile is empty. This method requires the the tile map has not been previously released (eg. don't call [layer releaseMap])

returns the tile gid at a given tile coordinate. It also returns the tile flags. This method requires the the tile map has not been previously released (eg. don't call [layer releaseMap])

Layer orientation, which is the same as the map orientation

size of the map's tile (could be different from the tile's size)

properties from the layer. They can be added using Tiled