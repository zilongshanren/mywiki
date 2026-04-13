---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture_atlas/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCTextureAtlas.h>`


| id |
|

A class that implements a Texture Atlas. Supported features: The atlas file can be a PVRTC, PNG or any other fomrat supported by Texture2D Quads can be udpated in runtime Quads can be added in runtime Quads can be removed in runtime Quads can be re-ordered in runtime The TextureAtlas capacity can be increased or decreased in runtime OpenGL component: V3F, C4B, T2F. The quads are rendered using an OpenGL ES VBO. To render the quads using an interleaved vertex array list, you should modify the [ccConfig.h](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/cc_config_8h/) file

| void CCTextureAtlas::drawNumberOfQuads: | ( | NSUInteger | n | ) | ` [virtual]` |

draws n quads n can't be greater than the capacity of the Atlas

| void CCTextureAtlas::drawNumberOfQuads:fromIndex: | ( | NSUInteger | n, |
| [fromIndex] NSUInteger | start |
||
| ) | ` [virtual]` |

draws n quads from an index (offset). n + start can't be greater than the capacity of the atlas

| void CCTextureAtlas::drawQuads | ( | ) | ` [virtual]` |

draws all the Atlas's Quads

| id CCTextureAtlas::initWithFile:capacity: | ( | NSString * | file, |
| [capacity] NSUInteger | capacity |
||
| ) | ` [virtual]` |

initializes a TextureAtlas with a filename and with a certain capacity for Quads. The TextureAtlas capacity can be increased in runtime.

WARNING: Do not reinitialize the TextureAtlas because it will leak memory (issue #706)

| id CCTextureAtlas::initWithTexture:capacity: | ( |
|

` [virtual]`

initializes a TextureAtlas with a previously initialized Texture2D object, and with an initial capacity for Quads. The TextureAtlas capacity can be increased in runtime.

WARNING: Do not reinitialize the TextureAtlas because it will leak memory (issue #706)

| void CCTextureAtlas::insertQuad:atIndex: | ( |
|

` [virtual]`

Inserts a Quad (texture, vertex and color) at a certain index index must be between 0 and the atlas capacity - 1

| void CCTextureAtlas::insertQuadFromIndex:atIndex: | ( | NSUInteger | fromIndex, |
| [atIndex] NSUInteger | newIndex |
||
| ) | ` [virtual]` |

Removes the quad that is located at a certain index and inserts it at a new index This operation is faster than removing and inserting in a quad in 2 different steps

| void CCTextureAtlas::removeAllQuads | ( | ) | ` [virtual]` |

removes all Quads. The TextureAtlas capacity remains untouched. No memory is freed. The total number of quads to be drawn will be 0

| void CCTextureAtlas::removeQuadAtIndex: | ( | NSUInteger | index | ) | ` [virtual]` |

removes a quad at a given index number. The capacity remains the same, but the total number of quads to be drawn is reduced in 1

| BOOL CCTextureAtlas::resizeCapacity: | ( | NSUInteger | n | ) | ` [virtual]` |

resize the capacity of the [CCTextureAtlas](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture_atlas/). The new capacity can be lower or higher than the current one It returns YES if the resize was successful. If it fails to resize the capacity it will return NO with a new capacity of 0.

| id CCTextureAtlas::textureAtlasWithFile:capacity: | ( | NSString * | file, |
| [capacity] NSUInteger | capacity |
||
| ) | ` [static, virtual]` |

creates a TextureAtlas with an filename and with an initial capacity for Quads. The TextureAtlas capacity can be increased in runtime.

| id CCTextureAtlas::textureAtlasWithTexture:capacity: | ( |
|

` [static, virtual]`

creates a TextureAtlas with a previously initialized Texture2D object, and with an initial capacity for n Quads. The TextureAtlas capacity can be increased in runtime.

| void CCTextureAtlas::updateQuad:atIndex: | ( |
|

` [virtual]`

updates a Quad (texture, vertex and color) at a certain index index must be between 0 and the atlas capacity - 1

NSUInteger CCTextureAtlas::capacity` [read, assign]` |

quantity of quads that can be stored with the current texture atlas size

NSUInteger CCTextureAtlas::totalQuads` [read, assign]` |

quantity of quads that are going to be drawn