---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions-mac/html/interface_t_m_x_generator/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

| BOOL |
|

generates a single TMX map with multiple layers. Keep in mind this won't build a world for you, it will just create a TMX file based on data it's fed.

| BOOL TMXGenerator::generateAndSaveTMXMap: | ( | NSError ** | error | ) | ` [virtual]` |

Call this to generate your map & save it to filepath, provided by delegate. Returns NO and an error if the map isn't generated, otherwise returns YES.

| error | Pass NULL if you don't want error description. |

| NSDictionary* TMXGenerator::layerNamed:width:height:data:visible: | ( | NSString * | layerName, |
| [width] int | width, |
||
| [height] int | height, |
||
| [data] NSData * | binaryLayerData, |
||
| [visible] BOOL | isVisible |
||
| ) | ` [static, virtual]` |

Prepare layer setup info with given size in tiles, some additional data and visibilaty. (See TMXGeneratorTestLayer for how-to.

| NSDictionary* TMXGenerator::makeObjectWithName:type:x:y:width:height:properties: | ( | NSString * | name, |
| [type] NSString * | type, |
||
| [x] int | x, |
||
| [y] int | y, |
||
| [width] int | width, |
||
| [height] int | height, |
||
| [properties] NSDictionary * | properties |
||
| ) | ` [static, virtual]` |

Prepare single object with given name, type, position, size & properties dictionary. (See TMXGeneratorTestLayer for how-to.

| NSDictionary* TMXGenerator::tileSetWithImage:named:width:height:tileSpacing: | ( | NSString * | imgName, |
| [named] NSString * | name, |
||
| [width] int | width, |
||
| [height] int | height, |
||
| [tileSpacing] int | spacing |
||
| ) | ` [static, virtual]` |

Prepares tileset setup info with image filename, tileset name, size of tiles & spacing between them. (See TMXGeneratorTestLayer for how-to.)