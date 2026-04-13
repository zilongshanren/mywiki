---
title: CCSpriteFrameCache Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite_frame_cache/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCSpriteFrameCache.h](http://www.learn-cocos2d.com/)"

| (void) | -
|

Singleton that handles the loading of the sprite frames. It saves in a cache the sprite frames.

Adds an sprite frame with a given name. If the name already exists, then the contents of the old name will be replaced with the new one.

| - (void) addSpriteFramesWithDictionary: | (NSDictionary *) | dictionary |
||
| texture: | (
|

Adds multiple Sprite Frames with a dictionary. The texture will be associated with the created sprite frames.

| - (void) addSpriteFramesWithFile: | (NSString *) | plist |

Adds multiple Sprite Frames from a plist file. A texture will be loaded automatically. The texture name will composed by replacing the .plist suffix with .png If you want to use another texture, you should use the addSpriteFramesWithFile:texture method.

Adds multiple Sprite Frames from a plist file. The texture will be associated with the created sprite frames.

| - (void) addSpriteFramesWithFile: | (NSString *) | plist |
||
| textureFile: | (NSString *) | textureFileName | ||

Adds multiple Sprite Frames from a plist file. The texture will be associated with the created sprite frames.

Creates an sprite with the name of an sprite frame. The created sprite will contain the texture, rect and offset of the sprite frame. It returns an autorelease object.

| + (void) purgeSharedSpriteFrameCache |

Purges the cache. It releases all the Sprite Frames and the retained instance.

| - (void) removeSpriteFrameByName: | (NSString *) | name |

Deletes an sprite frame from the sprite frame cache.

| - (void) removeSpriteFrames |

Purges the dictionary of loaded sprite frames. Call this method if you receive the "Memory Warning". In the short term: it will free some resources preventing your app from being killed. In the medium term: it will allocate more resources. In the long term: it will be the same.

| - (void) removeSpriteFramesFromDictionary: | (NSDictionary *) | dictionary |

Removes multiple Sprite Frames from NSDictionary.

| - (void) removeSpriteFramesFromFile: | (NSString *) | plist |

Removes multiple Sprite Frames from a plist file. Sprite Frames stored in this file will be removed. It is convinient to call this method when a specific texture needs to be removed.

Removes all Sprite Frames associated with the specified textures. It is convinient to call this method when a specific texture needs to be removed.

| - (void) removeUnusedSpriteFrames |

Removes unused sprite frames. Sprite Frames that have a retain count of 1 will be deleted. It is convinient to call this method after when starting a new Scene.

Retruns ths shared instance of the Sprite Frame cache

Returns an Sprite Frame that was previously added. If the name is not found it will return nil. You should retain the returned copy if you are going to use it.