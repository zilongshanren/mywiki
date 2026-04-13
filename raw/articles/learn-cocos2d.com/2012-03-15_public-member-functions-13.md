---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_pixel_mask_sprite/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <KKPixelMaskSprite.h>`


| id |
|

[KKPixelMaskSprite](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_pixel_mask_sprite/) is a CCSprite that has a pixelMask for pixel-perfect collision detection.

Notable behavior of this class:

These may be fixed at a later time given enough interest.

| id KKPixelMaskSprite::initWithFile:alphaThreshold: | ( | NSString * | filename, |
| [alphaThreshold] UInt8 | alphaThreshold |
||
| ) | ` [virtual]` |

Initializer with filename and alphaThreshold (range 0-255). The alpha value of a pixel must be > alphaThreshold to be added as a collision bit to the pixelMask. Ie alphaThreshold = 255 ensures that only fully opaque pixels are colliding, and alphaThreshold == 0 ensures that all but completely transparent pixels are considered for collision bits.

| BOOL KKPixelMaskSprite::pixelMaskContainsPoint: | ( | CGPoint | point | ) | ` [virtual]` |

Returns YES if the given point (in world/screen coordinates) is on a collision bit that is set to YES in the pixelMask. Returns NO if the point in the pixelMask is not colliding, or if the point lies outside the bounds of the pixelMask.

Note: The [KKPixelMaskSprite](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_pixel_mask_sprite/) may be rotated and/or scaled.

| BOOL KKPixelMaskSprite::pixelMaskIntersectsNode: | ( | CCNode * | other | ) | ` [virtual]` |

Returns YES if the given node intersection contains a pixelMask collision bit. If the node is a non-KKPixelMaskSprite node then the intersection rectangle (if any) will be tested for containing any collision bits and return YES if the other node's boundingBox intersection contains a pixelMask collision. Returns NO if the nodes aren't colliding or if there is no pixelMask collision.

If the other node is of class [KKPixelMaskSprite](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_pixel_mask_sprite/) an accurate pixelMask vs. pixelMask comparison is performed. If the intersection of the two nodes contains a pixelMask collision bit set at the same coordinates, then the two nodes are colliding and YES is returned.

Note: both nodes may NOT be rotated or scaled. This test only works with non-rotated, non-scaled nodes!

| id KKPixelMaskSprite::spriteWithFile: | ( | NSString * | filename | ) | ` [static, virtual]` |

Same as initWithFile but returns an autoreleased instance with alphaThreshold defaulting to 255 (only fully opaque pixels are collision bits).

| id KKPixelMaskSprite::spriteWithFile:alphaThreshold: | ( | NSString * | filename, |
| [alphaThreshold] UInt8 | alphaThreshold |
||
| ) | ` [static, virtual]` |

Same as initWithFile but returns an autoreleased instance.