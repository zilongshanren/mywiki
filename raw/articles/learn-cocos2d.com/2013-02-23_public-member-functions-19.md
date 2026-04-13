---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_h_k_t_m_x_layer/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone-extensions
0.2
Cocos2D Extensions API Reference (iOS version) for www.kobold2d.com developers
|

| (id) | -
|

| - (id) initWithTilesetInfo: | (CCTMXTilesetInfo *) | tilesetInfo |
|
| layerInfo: | (CCTMXLayerInfo *) | layerInfo |
|
| mapInfo: | (CCTMXMapInfo *) | mapInfo |
|

| + (id) layerWithTilesetInfo: | (CCTMXTilesetInfo *) | tilesetInfo |
|
| layerInfo: | (CCTMXLayerInfo *) | layerInfo |
|
| mapInfo: | (CCTMXMapInfo *) | mapInfo |
|

returns the position in pixels of a given tile coordinate

| - (void) setTileGID: | (unsigned int) | gid |
|
| at: | (CGPoint) | tileCoordinate |
|

sets the tile gid (gid = tile global id) at a given tile coordinate. The Tile GID can be obtained by using the method "tileGIDAt" or by using the TMX editor -> Tileset Mgr +1. If a tile is already placed at that position, then it will be replaced.

returns the tile gid at a given tile coordinate. if it returns 0, it means that the tile is empty.

Layer orientation, which is the same as the map orientation

size of the map's tile (could be differnt from the tile's size)

properties from the layer. They can be added using Tiled