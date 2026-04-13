---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/cocos2d-iphone/html/interface_c_c_texture_atlas/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
1.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCTextureAtlas.h>`


| (id) | -
|

A class that implements a Texture Atlas. Supported features: The atlas file can be a PVRTC, PNG or any other fomrat supported by Texture2D Quads can be udpated in runtime Quads can be added in runtime Quads can be removed in runtime Quads can be re-ordered in runtime The TextureAtlas capacity can be increased or decreased in runtime OpenGL component: V3F, C4B, T2F. The quads are rendered using an OpenGL ES VBO. To render the quads using an interleaved vertex array list, you should modify the [ccConfig.h](http://www.learn-cocos2d.com/) file

draws n quads n can't be greater than the capacity of the Atlas

draws n quads from an index (offset). n + start can't be greater than the capacity of the atlas

| - (void) fillWithEmptyQuadsFromIndex: | (NSUInteger) | index |
|
| amount: | (NSUInteger) | amount |
|

| - (id) initWithFile: | (NSString *) | file |
|
| capacity: | (NSUInteger) | capacity |
|

initializes a TextureAtlas with a filename and with a certain capacity for Quads. The TextureAtlas capacity can be increased in runtime.

WARNING: Do not reinitialize the TextureAtlas because it will leak memory (issue #706)

initializes a TextureAtlas with a previously initialized Texture2D object, and with an initial capacity for Quads. The TextureAtlas capacity can be increased in runtime.

WARNING: Do not reinitialize the TextureAtlas because it will leak memory (issue #706)

Inserts a Quad (texture, vertex and color) at a certain index index must be between 0 and the atlas capacity - 1

| - (void) insertQuadFromIndex: | (NSUInteger) | fromIndex |
|
| atIndex: | (NSUInteger) | newIndex |
|

Removes the quad that is located at a certain index and inserts it at a new index This operation is faster than removing and inserting in a quad in 2 different steps

| - (void) insertQuads: | (
|

Inserts a c array of quads at a given index index must be between 0 and the atlas capacity - 1 this method doesn't enlarge the array when amount + index > totalQuads

| - (void) insertQuadsFromIndex: | (NSUInteger) | oldIndex |
|
| amount: | (NSUInteger) | amount |
|
| atIndex: | (NSUInteger) | newIndex |
|

Inserts a amount of quads from oldIndex at newIndex, while moving quads at newIndex - oldIndex back accordingly

| - (void) moveQuadsFromIndex: | (NSUInteger) | index |
|
| to: | (NSUInteger) | newIndex |
|

removes all Quads. The TextureAtlas capacity remains untouched. No memory is freed. The total number of quads to be drawn will be 0

removes a quad at a given index number. The capacity remains the same, but the total number of quads to be drawn is reduced in 1

| - (void) removeQuadsAtIndex: | (NSUInteger) | index |
|
| amount: | (NSUInteger) | amount |
|

removes a amount of quads starting from index

resize the capacity of the [CCTextureAtlas](http://www.learn-cocos2d.com/api-ref/latest/cocos2d-iphone/html/interface_c_c_texture_atlas/). The new capacity can be lower or higher than the current one It returns YES if the resize was successful. If it fails to resize the capacity it will return NO with a new capacity of 0.

| + (id) textureAtlasWithFile: | (NSString *) | file |
|
| capacity: | (NSUInteger) | capacity |
|

creates a TextureAtlas with an filename and with an initial capacity for Quads. The TextureAtlas capacity can be increased in runtime.

creates a TextureAtlas with a previously initialized Texture2D object, and with an initial capacity for n Quads. The TextureAtlas capacity can be increased in runtime.

updates a Quad (texture, vertex and color) at a certain index index must be between 0 and the atlas capacity - 1

quantity of quads that can be stored with the current texture atlas size