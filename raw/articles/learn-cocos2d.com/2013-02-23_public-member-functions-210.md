---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_tile_map_atlas/
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

`#import <CCTileMapAtlas.h>`


| (id) | -
|

[CCTileMapAtlas](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_tile_map_atlas/) is a subclass of [CCAtlasNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_atlas_node/).

It knows how to render a map based of tiles. The tiles must be in a .PNG format while the map must be a .TGA file.

For more information regarding the format, please see this post: [http://www.cocos2d-iphone.org/archives/27](http://www.cocos2d-iphone.org/archives/27)

All features from [CCAtlasNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_atlas_node/) are valid in [CCTileMapAtlas](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_tile_map_atlas/)

IMPORTANT: This class is deprecated. It is maintained for compatibility reasons only. You SHOULD not use this class. Instead, use the newer TMX file format: [CCTMXTiledMap](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_t_m_x_tiled_map/)

| - (id) initWithTileFile: | (NSString *) | tile |
|
| mapFile: | (NSString *) | map |
|
| tileWidth: | (int) | w |
|
| tileHeight: | (int) | h |
|

initializes a CCTileMap with a tile file (atlas) with a map file and the width and height of each tile in points. The file will be loaded using the TextureMgr.

sets a tile at position x,y. For the moment only channel R is used

returns a tile from position x,y. For the moment only channel R is used

| + (id) tileMapAtlasWithTileFile: | (NSString *) | tile |
|
| mapFile: | (NSString *) | map |
|
| tileWidth: | (int) | w |
|
| tileHeight: | (int) | h |
|

creates a CCTileMap with a tile file (atlas) with a map file and the width and height of each tile in points. The tile file will be loaded using the TextureMgr.