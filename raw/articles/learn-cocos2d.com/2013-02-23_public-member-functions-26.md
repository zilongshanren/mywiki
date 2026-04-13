---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/protocol_t_m_x_generator_delegate-p/
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

| (NSString *) | -
|

Returns layer setup information based on the name passed. Keys listed in "Layer Setup Info Keys" section above.

Returns all layer names as an array of NSStrings. Order of array items returned here determine the heirarchy.

Returns map setup parameters and properties. Keys listed in the "Map Setup Info Keys" section above. Number values can be strings or NSNumbers.

Returns the names of all the object groups as NSStrings. It's ok to return nil if don't need objects.

Returns object group information based on the name passed. Keys listed in "Objects Group Setup Info Keys" section above.

| - (NSArray*) propertiesForObjectWithName: | (NSString *) | name |
|
| inGroupWithName: | (NSString *) | groupName |
|
` [optional]` |

Returns the optional properties for a given object in a given group. Keys are listed in "Single Object Setup Info Keys" section above.

Returns the properties for a given tileset.

| - (NSString*) tilePropertyForLayer: | (NSString *) | layerName |
|
| tileSetName: | (NSString *) | tileSetName |
|
| X: | (int) | x |
|
| Y: | (int) | y |
|

Returns a uniquely identifying value for the key returned in the method keyForTileIdentificationForLayer: If the value is not found, the tile gets set to the minimum GID.

| - (int) tileRotationForLayer: | (NSString *) | layerName |
|
| X: | (int) | x |
|
| Y: | (int) | y |
|
` [optional]` |

Returns a rotation value (no rotation if this method doesn't exist) for the specified tile name and tile.

Returns tileset setup information based on the name. Keys listed in "Tileset Setup Info Keys" section above.

Returns the name of the tileset (only one right now) for the layer.