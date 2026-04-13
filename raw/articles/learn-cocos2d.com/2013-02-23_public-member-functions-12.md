---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_big_image/
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

holds parts of big image as an idvididual dynamically unloadable tiles. Besides dynamic tiles this node can have normal children, such as CCSprite, layer, etc...

[CCBigImage](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_big_image/) is refactored DynamicTiledLevelNode New Features: 1) Tile-Cutter ( [https://github.com/psineur/Tile-Cutter](https://github.com/psineur/Tile-Cutter) ) instead of Gimp & xcftools 2) Removed unnecessary code, more comments, etc...

Besides Dynamic Mode, when all tiles are loaded in independent thread this node also supports Static Mode (dynamicMode = NO) when all tiles are preloaded and no additional thread is used. However, even in staticMode tiles that aren't visible now in screen rect will be not rendered to increase performance.

LIMITATIONS: CCCamera may be not supported.

| - (id) initWithTilesFile: | (NSString *) | filename |
|
| tilesExtension: | (NSString *) | extension |
|
| tilesZ: | (int) | tilesZ |
|

Inits [CCBigImage](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_big_image/). Designated initializer.

| filename | plist filename from Tile-Cutter. |
| extension | file extension, that will be used for all tiles instead of their extensions that are in plist file. Pass nil to kep original extension from plist file. |
| tilesZ | zOrder, that will be used for all tiles. Usefull when you have other nodes added as children to
|

Load tiles by request in a given rect (in nodes coordinates)

| + (id) nodeWithTilesFile: | (NSString *) | filename |
|
| tilesExtension: | (NSString *) | extension |
|
| tilesZ: | (int) | tilesZ |
|

if YES - then only needed (visible in screen rect) tiles will be loaded at the moment via independent thread if NO - all tiles will be preloaded and no no additional thread will be used This property can be changed at runtime in both directions. On the Mac by default this property is OFF On the iOS devices by default this property is ON

Returns size that describes in what distance beyond each side of the screen tiles should be loaded to avoid holes when levels scrolls fast. By default it's equal to first tile's size.