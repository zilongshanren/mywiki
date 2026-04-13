---
title: Fast Pixel-Perfect Collision Detection for Cocos2D with Example Code (1/2)
url: http://www.learn-cocos2d.com/2011/12/fast-pixelperfect-collision-detection-cocos2d-code-1of2/
author: Thozzz Says
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Detecting collisions on pixel-perfect boundaries is the holy grail of collision detection in 2D games. As such, it seems like the ideal, if not to say perfect, solution to collision detection in general. Yet, it’s also quite complicated and the straightforward solutions don’t perform very well until you start optimizing the code.

This first post focuses on creating a pixel mask by analyzing the raw image data, as [proposed over 3 years ago by Ernesto Corvi](https://groups.google.com/group/cocos2d-iphone-discuss/msg/41d79413f2ac1339). It’s the fastest solution if you want to test if a point collides with a pixel on an image, which also works for rotated and scaled sprites. However it does take some optimizing to speed up detecting collisions between a bounding box of a node and the pixel mask, or two pixel masks.

The alternative solution is to render the two colliding objects onto a CCRenderTexture, as [developed by Dani and others on the Cocos2D forum](http://www.cocos2d-iphone.org/forum/topic/18522). It is able to detect collisions of arbitrarily rotated and scaled sprites but can be expected to be noticeably slower than a pixel mask. I will discuss this solution in a future iDevBlogADay post.

The results will find their way into

[Kobold2D], to make the solutions readily available to all developers.


#### The Ernesto Corvi Pixel-Perfect CollisionMap Strategy

The [pseudo-code approach posted by Ernesto](https://groups.google.com/group/cocos2d-iphone-discuss/msg/41d79413f2ac1339) involves creating a 32-Bit UIImage from a file and allocating a pixelMask (he calls it collisionMap) buffer to hold the colliding/not colliding states for each pixel in the image. Then its just a matter of iterating over the image pixels, masking out the alpha part to determine if the pixel is fully opaque, and if it is, the collision flag in the pixelMask is set.

This solution has a few needs for improvements. It’s rudimentary code that doesn’t account for Retina displays and -hd images and leaves the pixelMask as upside-down image like the UIImage. It doesn’t allow the user to specify a threshold for the alpha value (0 to 255 range), to be able to consider pixels which aren’t fully opaque. And the code doesn’t provide a solution for testing rectangle intersections of the pixel mask, let alone the intersection of two pixel masks. That’s what this post is about.

#### Introducing KKPixelMaskSprite

KKPixelMaskSprite is a reusable class inheriting from CCSprite that adds the pixelMask and several collision detection methods. By setting the USE_BITARRAY macro to 1 you can change the class to use a BitArray instead. Instead of storing unsigned char (BOOL) types it the BitArray stores bits individually, thus reducing memory consumption to 1/8th (or 12.5%). For example, a 512×512 pixel mask using BOOL (unsigned char) will require 256 KB of memory whereas the same pixel mask as a bit array would only require 32 KB of memory.

I chose to use the

[Bit Manipulation Library from Michael Dipperstein]because it’s released under the[LGPL]license - the same license Cocos2D had used before it adopted the MIT License - and because it provides implementations for both C (used) and C++.

Let’s walk through the code that loads the image and allocates the pixelMask array:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 |
// this ensures that we're loading the -hd asset on Retina devices NSString* fullpath = [CCFileUtils fullPathFromRelativePath:filename]; UIImage* image = [[UIImage alloc] initWithContentsOfFile:fullpath]; // get all the image information we need pixelMaskWidth = image.size.width; pixelMaskHeight = image.size.height; pixelMaskSize = pixelMaskWidth * pixelMaskHeight; // allocate and clear the pixelMask buffer #if USE_BITARRAY pixelMask = BitArrayCreate(pixelMaskSize); BitArrayClearAll(pixelMask); #else pixelMask = malloc(pixelMaskSize * sizeof(BOOL)); memset(pixelMask, 0, pixelMaskSize * sizeof(BOOL)); #endif |

Line 2 ensures that the -hd suffix is appended to the filename, if there’s an HD version of the image available and Retina display is enabled. Lines 6-8 get the image information and the resulting pixelMaskSize, which is simply the number of pixels in the image. Depending on the USE_BITARRAY macro the pixelMask is either declared as **bit_array_t* pixelMask;** (BitArray) or **BOOL* pixelMask;** (BOOL array).

Of note here is that I chose to use the **BOOL** type simply because it’s the native boolean data type in Objective-C. BOOL is a typedef to **unsigned char** so it’s using the same underlying data type as Ernesto’s code. Be aware that **BOOL** and **bool** (note the lowercase) are two different types! The lowercase bool is a 32-Bit integer.

With the pixelMask buffer setup and cleared, we can now scan the image’s pixels and determine if each pixel’s alpha value allows it to be added to the pixelMask or not. For clarity, the USE_BITARRAY macro and BitArray implementation parts are not shown from here on.

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 |
// get the pixel data (more correctly: texels) as 32-Bit unsigned integers CFDataRef imageData = CGDataProviderCopyData(CGImageGetDataProvider(image.CGImage)); const UInt32* imagePixels = (const UInt32*)CFDataGetBytePtr(imageData); UInt32 alphaValue = 0, x = 0, y = pixelMaskHeight - 1; UInt8 alpha = 0; for (NSUInteger i = 0; i < pixelMaskSize; i++) { // ensure that the pixelMask is created in top to bottom orientation NSUInteger index = y * pixelMaskWidth + x; x++; if (x == pixelMaskWidth) { x = 0; y--; } // mask out the colors so that only the alpha value remains (upper 8 bits) alphaValue = imagePixels[i] & 0xff000000; if (alphaValue > 0) { // get the alpha value, then compare alpha with the alpha threshold alpha = (UInt8)(alphaValue >> 24); if (alpha > alphaThreshold) { pixelMask[index] = YES; } } } CFRelease(imageData); imageData = nil; [image release]; image = nil; |

Lines 2-4 gain access to the raw pixel information in the image. This involves using several Core Foundation functions. The UIImage gives you access to the underlying [Quartz CGImage](http://developer.apple.com/library/mac/#documentation/GraphicsImaging/Reference/CGImage/Reference/reference.html) through the **CGImage** property. From the CGImage a [CGDataProvider](http://developer.apple.com/library/ios/#documentation/GraphicsImaging/Reference/CGDataProvider/Reference/reference.html) is created which allows the image’s raw data to be copied to a **CFDataRef**.

CFDataRef is merely a pointer to an internal Core Foundation struct named __CFData. The details of this struct are not exposed to developers but it can be looked up in [CFData.c on opensource.apple.com](http://opensource.apple.com/source/CF/CF-550/CFData.c). The [CFDataGetBytePtr](http://developer.apple.com/library/mac/documentation/CoreFoundation/Reference/CFDataRef/Reference/reference.html#//apple_ref/c/func/CFDataGetBytePtr) function returns a pointer to the bytes stored in the __CFData struct. What remains is simply to cast the pointer to an **UInt32** (a typedef for **unsigned int**) because the UIImage is an image with 32-Bits per pixel (RGBA8888).

What follows in lines 8-30 is a loop that inspects every pixel in the image to determine if that pixel should be added as a collision bit to the pixelMask or not. The first peculiarity starts with lines 11-17 which calculates the index into the pixelMask. By doing so it fixes the issue that UIImage images are upside down by adding bits to the pixelMask buffer in a bottom up manner while iterating over the imagePixels buffer from top to bottom.

In line 20 the alpha part (leftmost 8 bits) of each 32-Bit pixel value is masked out. This sets all the color bits (0-23) to 0 and leaves only the highest bits which contain the 8-Bit alpha value. If alphaValue is 0 the pixel is fully transparent and we can just move on with the next iteration. Otherwise lines 24 to 28 create the **UInt8** (typedef for **unsigned char**) value containing the pixel’s alpha (0 to 255 range) which is then compared with the alphaThreshold. If the test succeeds, the corresponding bit in the pixelMask is set to YES. Finally lines 32-35 perform the necessary cleanup and release the image memory.

A KKPixelMaskSprite can be initialized with spriteWithFile and an optional alphaThreshold value:

|
1 |
spriteB = [KKPixelMaskSprite spriteWithFile:@"imageB.png" alphaThreshold:100]; |

#### Testing for collision of a point in the pixel mask

Testing if a bit at a specified x,y location in the pixel mask is set is computationally inexpensive, if not trivial. It simply requires calculating the index into the array, plus some bounds checks:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 |
-(BOOL) pixelMaskBitAt:(CGPoint)point { // round the point coordinates to the nearest integer int x = (int)(point.x + 0.5f); int y = (int)(point.y + 0.5f); if (x < 0 || y < 0 || x >= pixelMaskWidth || y >= pixelMaskHeight) { return NO; } NSUInteger index = y * pixelMaskWidth + x; return pixelMask[index]; } |

The only special consideration to make is that points can have fractional parts, but we must calculate the index based on integer values (lines 4-5). To allow for natural rounding of a floating point to integer values the simple trick of adding 0.5f is used. This ensures that every fraction value greater than 0.5f is increased to the next higher integer, and since casting to integer simply removes the fractional part, we end up with values of 1.0 to 1.4999 to be rounded down to 1 whereas values from 1.5 to 1.9999 will be rounded up to 2.

The bounds check in line 7 avoids calculating an index that is out of bounds, which might cause the app to crash. In line 12 the pixelMask index is calculated based on the trusted [formula that maps a 2D position onto a 1-dimensional array](http://stackoverflow.com/questions/2151084/map-a-2d-array-onto-a-1d-array-c). Finally the bit at that index is returned. Overall this test uses simple arithmetics and is blazingly fast.

But that’s only one part of the story. The pixelMaskBitAt method is actually a private method of the KKPixelMaskSprite class. As a user of the class you will be sending the pixelMaskContainsPoint message instead. I’ll explain why after the code sample:

|
1 2 3 4 5 6 7 8 9 |
-(BOOL) pixelMaskContainsPoint:(CGPoint)point { // the point coordinates need to be relative to the node's space point = [self convertToNodeSpace:point]; // upscale point to Retina pixels if necessary point = ccpMult(point, CC_CONTENT_SCALE_FACTOR()); return [self pixelMaskBitAt:point]; } |

Since we’re working with Cocos2D, we must consider the possibility that the sprite with the pixel mask is rotated or scaled, or both. The **convertToNodeSpace** method in line 4 takes care of that for us. And it performs another important task by ensuring that the point coordinate is relative to the sprite texture’s origin coordinate (lower left corner). The pixelMask has the width and height of the image, indexing it with screen coordinates (whose origin is at the lower left corner of the screen) would return incorrect results.

Line 6 also makes sure that the point is converted to a pixel coordinate by multiplying it with ![pixelperfecttouch](../../../wordpress/wp-content/uploads/pixelperfecttouch-300x154.png)


**CC_CONTENT_SCALE_FACTOR()**. The content scale factor is 2 on Retina devices with Retina display enabled, otherwise it’s 1. This assumes that if you enable Retina mode and run the app on a Retina device, corresponding -hd images will be provided for all pixel mask sprites.

#### Continue Reading Part 2 …

I had to split this post into two, due to a [PHP limitation](http://www.undermyhat.org/blog/2009/07/sudden-empty-blank-page-for-large-posts-with-wordpress/).

[Please continue with the second post of this article](http://www.learn-cocos2d.com/2011/12/fast-pixelperfect-collision-detection-cocos2d-code-2of2/) to learn how the rectangle intersection and pixelMask with pixelMask collision detection is done.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] Fast Pixel-Perfect Collision Detection for Cocos2D with Example Code (1/2) […]

great…and perfect

[…] KKPixelMaskSprite as described in Fast Pixel-Perfect Collision Detection for Cocos2D […]

Nice tool, thanks for sharing! How would you use this to implement a boundary that sprites can’t touch? I have project that is top-down 2D and the player sprite will move around a map. I’ve got a PNG that has the walls colored red and I’m using your tool to accurately detect collision between the player and the walls. But when I detect a collision, I stop the player form moving any more. How should I allow the player to move away from the boundary once he hits it?

Well, as soon as I asked the question I thought of an idea, and i’d like you opinion on it… its working for me now

CGPoint start = CGPointMake(worldMap.position.x, worldMap.position.y);

CGPoint pnt = CGPointMake(worldMap.position.x + -velocity.x * delta, worldMap.position.y + -velocity.y * delta);

worldMap.position = pnt;

char collision = [coll pixelMaskIntersectsNode:boy];

if (collision) {

worldMap.position = start;

}

My next problem is that I am building my collision map or pixel mask out of a CCLayerPanZoom layer which holds a CCBigImage made of 256×256 pixel tiles. Any suggestions there? Can I create a pixel mask from CCBigImage?

Hi,

Great class! Thanks for posting this. I am having some trouble getting KKPixelMaskSprite to detect a hit when initializing it with a texture as opposed to a sprite…

As a simple test I did the following:

test 1:

- init with

[[KKPixelMaskSprite spriteWithFile:@”Zombie.png”]

- test pixelMaskContainsPoint (x,y)

- it works!!

test 2:

![:(](../../../wordpress/wp-includes/images/smilies/frownie.png)


- create a CCRenderTexture (_zombieTexture)

- create a CCSprite (_zombie)

- visit _zombie to “draw” it to the _zombieTexture

- init with

[[KKPixelMaskSprite spriteWithTexture:_zombieTexture.sprite.texture]

- test pixelMaskContainsPoint (x,y)

- it fails

Any idea as to what might be causing the problem? As far as I can tell everything is identical aside from the init..

Cheers,

-d-

Hmmm I could imagine that the Zombie.png is an SD sprite but if you draw it with CCRenderTexture on a Retina device, the resulting texture will have Retina resolutions. It’s just a hunch though. You might want to try the test with pixel coordinates multiplied by 2 to see if it then returns true. It would not be proof though, just an indication.

Bug in “KKPixelMaskSprite.m” function ‘pixelMaskIntersectsPixelMaskSprite’

Lines 170, 171 Unsigned integer doesn’t allow for potential negative offsets.

was:

170: NSUInteger originOffsetX = intersectOther.origin.x - intersectSelf.origin.x;

171: NSUInteger originOffsetY = intersectOther.origin.y - intersectSelf.origin.y;

fix:

170: NSInteger originOffsetX = intersectOther.origin.x - intersectSelf.origin.x;

171: NSInteger originOffsetY = intersectOther.origin.y - intersectSelf.origin.y;

Jeff.

Is there anyone to part this code to OpenGL ES Textures not Cocos2D?