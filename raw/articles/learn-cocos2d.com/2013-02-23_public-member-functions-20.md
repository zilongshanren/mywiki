---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_h_k_t_m_x_tiled_map/
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

`#import <HKTMXTiledMap.h>`


| (id) | -
|

Possible oritentations of the TMX map Orthogonal orientation Hexagonal orientation Isometric orientation CCTMXTiledMap knows how to parse and render a TMX map.

It adds support for the TMX tiled map format used by [http://www.mapeditor.org](http://www.mapeditor.org/) It supports isometric, hexagonal and orthogonal tiles. It also supports object groups, objects, and properties.

Features:

Limitations:

Technical description: Each layer is created using an CCTMXLayer (subclass of CCSpriteSheet). If you have 5 layers, then 5 CCTMXLayer will be created, unless the layer visibility is off. In that case, the layer won't be created at all. You can obtain the layers (CCTMXLayer objects) at runtime by:

Each object group is created using a CCTMXObjectGroup which is a subclass of NSMutableArray. You can obtain the object groups at runtime by:

Each object is a CCTMXObject.

Each property is stored as a key-value pair in an NSMutableDictionary. You can obtain the properties at runtime by:

[map propertyNamed: name_of_the_property]; [layer propertyNamed: name_of_the_property]; [objectGroup propertyNamed: name_of_the_property]; [object propertyNamed: name_of_the_property];

return the TMXObjectGroup for the secific group