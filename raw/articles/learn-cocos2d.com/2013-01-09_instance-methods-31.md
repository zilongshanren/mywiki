---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_sprite/
published: '2013-01-09'
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

`#import <CCSprite.h>`


| (id) | +
|

|

| BOOL |
|

[CCSprite](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_sprite/) is a 2d image ( [http://en.wikipedia.org/wiki/Sprite_(computer_graphics)](https://en.wikipedia.org/wiki/Sprite_(computer_graphics)) )

[CCSprite](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_sprite/) can be created with an image, or with a sub-rectangle of an image.

If the parent or any of its ancestors is a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) then the following features/limitations are valid

If the parent is an standard [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_node/), then [CCSprite](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_sprite/) behaves like any other [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_node/):

The default anchorPoint in [CCSprite](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_sprite/) is (0.5, 0.5).

| - (id) initWithCGImage: | (CGImageRef) | image |
|
| key: | (NSString *) | key |
|

Initializes an sprite with a CGImageRef and a key The key is used by the [CCTextureCache](http://www.learn-cocos2d.com/) to know if a texture was already created with this CGImage. For example, a valid key is: "sprite_frame_01". If key is nil, then a new texture will be created each time by the [CCTextureCache](http://www.learn-cocos2d.com/).

| - (id) initWithFile: | (NSString *) | filename |

Initializes an sprite with an image filename. The rect used will be the size of the image. The offset will be (0,0).

Initializes an sprite with an image filename, and a rect. The offset will be (0,0).

Initializes an sprite with an sprite frame.

| - (id) initWithSpriteFrameName: | (NSString *) | spriteFrameName |

Initializes an sprite with a texture. The rect used will be the size of the texture. The offset will be (0,0).

Initializes an sprite with a texture and a rect in points (unrotated) The offset will be (0,0).

Initializes an sprite with a texture and a rect in points, optionally rotated. The offset will be (0,0). IMPORTANT: This is the designated initializer.

| - (void) setDisplayFrameWithAnimationName: | (NSString *) | animationName |
|
| index: | (int) | frameIndex |
|

| - (void) setTextureRect: | (CGRect) | rect |

| - (void) setVertexRect: | (CGRect) | rect |

set the vertex rect. It will be called internally by setTextureRect. Useful if you want to create 2x images from SD images in Retina Display. Do not call it manually. Use setTextureRect instead.

| + (id) spriteWithCGImage: | (CGImageRef) | image |
|
| key: | (NSString *) | key |
|

Creates an sprite with a CGImageRef and a key. The key is used by the [CCTextureCache](http://www.learn-cocos2d.com/) to know if a texture was already created with this CGImage. For example, a valid key is: "sprite_frame_01". If key is nil, then a new texture will be created each time by the [CCTextureCache](http://www.learn-cocos2d.com/).

| + (id) spriteWithFile: | (NSString *) | filename |

Creates an sprite with an image filename. The rect used will be the size of the image. The offset will be (0,0).

Creates an sprite with an image filename and a rect. The offset will be (0,0).

| + (id) spriteWithSpriteFrameName: | (NSString *) | spriteFrameName |

Creates an sprite with a texture. The rect used will be the size of the texture. The offset will be (0,0).

Creates an sprite with a texture and a rect. The offset will be (0,0).

| - (void) updateTransform |

updates the quad according the the rotation, position, scale values.

|
readwritenonatomicassign |

The index used on the TextureAtlas. Don't modify this value unless you know what you are doing

|
readwritenonatomicassign |

whether or not the Sprite needs to be updated in the Atlas

|
readwritenonatomicassign |

whether or not the sprite is flipped horizontally. It only flips the texture of the sprite, and not the texture of the sprite's children. Also, flipping the texture doesn't alter the anchorPoint. If you want to flip the anchorPoint too, and/or to flip the children too use:

sprite.scaleX *= -1;

|
readwritenonatomicassign |

whether or not the sprite is flipped vertically. It only flips the texture of the sprite, and not the texture of the sprite's children. Also, flipping the texture doesn't alter the anchorPoint. If you want to flip the anchorPoint too, and/or to flip the children too use:

sprite.scaleY *= -1;

|
readnonatomicassign |

offset position in points of the sprite in points. Calculated automatically by editors like Zwoptex.

the quad (tex coords, vertex coords and color) information

|
readnonatomicassign |

returns whether or not the texture rectangle is rotated