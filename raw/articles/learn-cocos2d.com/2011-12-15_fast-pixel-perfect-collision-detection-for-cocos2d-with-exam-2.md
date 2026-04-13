---
title: Fast Pixel-Perfect Collision Detection for Cocos2D with Example Code (2/2)
url: http://www.learn-cocos2d.com/2011/12/fast-pixelperfect-collision-detection-cocos2d-code-2of2/
author: Ross says
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This continues and concludes the previous post of the [Fast Pixel-Perfect Collision Detection for Cocos2D with Example Code (1/2)](http://www.learn-cocos2d.com/2011/12/fast-pixelperfect-collision-detection-cocos2d-code-1of2/) article.


#### Testing for pixelMask collision with a rectangle

Testing for an individual point is simple, testing for a rectangle such as the bounding box of another node requires more work. Not just to write the code, but also to run it. And it is limited to nodes which are neither rotated nor scaled.

Unfortunately, [testing collisions with rotated rectangles (oriented bounding boxes) is not trivial](https://en.wikipedia.org/wiki/Bounding_volume#Basic_intersection_checks) even without considering pixelMask collisions. Here’s a [C++ OBB](http://www.flipcode.com/archives/2D_OBB_Intersection.shtml) and a [C# OBB](https://toastymofo.blogspot.com/2010/03/2d-obb-collisions-in-xna_07.html) implementation for OBB collision detection. And that’s just for the bounding boxes, testing each pixel in an oriented pixel mask would likely be prohibitively expensive.

You definitely want to avoid a brute force method that iterates over the entire pixelMask array. Instead, this implementation first creates the intersecting rectangle of the pixelMask node and the other node, then only iterates over the intersection to considerably reduce the number of iterations:

```
-(BOOL) pixelMaskIntersectsRegularNode:(CCNode*)other
{
CGRect intersectRect = [self intersectRectInPixels:self otherNode:other];
// check if any of the flags in the pixelMask are set in intersection
NSUInteger maxX = intersectRect.origin.x + intersectRect.size.width;
NSUInteger maxY = intersectRect.origin.y + intersectRect.size.height;
for (NSUInteger y = intersectRect.origin.y; y < maxY; y++)
{
for (NSUInteger x = intersectRect.origin.x; x < maxX; x++)
{
NSUInteger index = y * pixelMaskWidth + x;
return pixelMask[index];
}
}
return NO;
}
```


It should be noted that we only need to find one pixelMask bit that is set. That means this method could be further optimized in a variety of ways that ensure that a pixel is more likely to be found earlier.

For example it can be argued that closer to the center of the pixelMask the likelihood of a pixelMask bit being set increases. That means depending on the location of the intersectionRect the iteration over the pixelMask could be tweaked to start closer to the center of the pixelMask and work its way outwards. But this optimization depends heavily on the images being used and to some extend how the objects move.

The worst case scenario is that there’s no bit set in the pixelMask for the given intersectRect. Knowing that, one might consider iterating over the pixelMask not BOOL by BOOL but looking up a full 32-Bit NSUInteger (4 BOOL at once) from the pixelMask. If that 32-Bit value is 0, then none of the 4 collision bits can possibly be set, reducing the number of tests and iterations from 4 to 1. Only if the value is greater than 0 you would have to check each individual pixelMask bit. Using a BitArray you could test up to 32 bits at once in a similar fashion.

A quick look at the intersectRectInPixels method reveals that it creates the intersecting rectangle of the two colliding nodes’ bounding boxes. Important to note here is that the origin of the intersecting rectangle must be converted to the first node’s nodeSpace and then converted to pixels to make sure it works with HD images.

```
-(CGRect) intersectRectInPixels:(CCNode*)node otherNode:(CCNode*)other
{
CGRect myBBox = [node boundingBox];
CGRect otherBBox = [other boundingBox];
CGRect intersectRect = CGRectIntersection(myBBox, otherBBox);
// transform the rect to the sprite's space and convert points to pixels
intersectRect.origin = [node convertToNodeSpace:intersectRect.origin];
return CC_RECT_POINTS_TO_PIXELS(intersectRect);
}
```


Being able to pass two nodes to this method allows the intersect rectangle to be calculated for both colliding nodes. This is needed next, when we determine the collision of two possibly intersecting KKPixelMaskSprite.

#### Detecting collision of two KKPixelMaskSprites

It’s only a relatively small step going from pixelMask with rectangle intersection to testing two pixelMasks for intersection (overlap may be a better word here). Again, you do not have to use brute force - it is sufficient to check the overlapping (intersecting) rectangle of the two sprites. Again this test doesn’t work with rotated or scaled rectangles but it’s a drawback that benefits the performance of the test.

```
-(BOOL) pixelMaskIntersectsPixelMaskSprite:(KKPixelMaskSprite*)other
{
CGRect intersectSelf = [self intersectRectInPixels:self otherNode:other];
CGRect intersectOther = [self intersectRectInPixels:other otherNode:self];
NSUInteger originOffsetX = intersectOther.origin.x - intersectSelf.origin.x;
NSUInteger originOffsetY = intersectOther.origin.y - intersectSelf.origin.y;
NSUInteger otherPixelMaskWidth = other.pixelMaskWidth;
BOOL* otherPixelMask = other.pixelMask;
// check if any of the flags in the pixelMask are set in intersection area
NSUInteger maxX = intersectSelf.origin.x + intersectSelf.size.width;
NSUInteger maxY = intersectSelf.origin.y + intersectSelf.size.height;
for (NSUInteger y = intersectSelf.origin.y; y < maxY; y++)
{
for (NSUInteger x = intersectSelf.origin.x; x < maxX; x++)
{
NSUInteger index = y * pixelMaskWidth + x;
if (pixelMask[index])
{
// check if there's a pixel set at the same location
// in the pixelMask of the other sprite
NSUInteger otherX = x + originOffsetX;
NSUInteger otherY = y + originOffsetY;
NSUInteger otherIndex = otherY * otherPixelMaskWidth + otherX;
if (otherPixelMask[otherIndex])
{
return YES;
}
}
}
}
return NO;
}
```


Compared to the previous rectangle test, the intersecting rectangle of the other colliding KKPixelMaskSprite was added and a reference to otherPixelMask along with other cached values in lines 4-9. The gist of the function still performs the same test up until line 22. Instead of returning the first bit that is set in the pixelMask, we have to make sure that this bit is also set in the otherPixelMask.

Since the index into the otherPixelMask can be easily calculated by offsetting it with the intersectOther rectangle’s origin, we only need to generate a new index for the same x,y coordinates but relative to the other KKPixelMaskSprite’s coordinate system. Lines 26 and 27 perform that operation using the pre-calculated originOffset from lines 6 and 7. In essence this offsets the x,y coordinates to the same location within the other sprite’s intersection rectangle. What remains is converting the coordinates to the index and testing if the otherPixelMask bit at that index is also set. If so, we have a collision.![pixelperfectmask](../../../wordpress/wp-content/uploads/pixelperfectmask-300x154.png)


#### Putting the intersection tests together

There’s one method that I left out so far. It’s the public interface method that users of KKPixelMaskSprite will call. It performs several early out tests and also picks the right test to perform based on the class of the other node.

```
-(BOOL) pixelMaskIntersectsNode:(CCNode*)other
{
if (rotation_ != 0.0f || other.rotation != 0.0f ||
self.scale != 1.0f || other.scale != 1.0f)
{
CCLOG(@"either or both nodes are rotated and/or scaled, returning NO!");
return NO;
}
if ([self intersectsNode:other])
{
if ([other isKindOfClass:PixelMaskSpriteClass])
{
KKPixelMaskSprite* maskSprite = (KKPixelMaskSprite*)other;
return [self pixelMaskIntersectsPixelMaskSprite:maskSprite];
}
else
{
return [self pixelMaskIntersectsRegularNode:other];
}
}
return NO;
}
```


I mentioned before that the intersection tests don’t work with rotated or scaled nodes. In this case the method immediately returns NO and logs this to avoid someone becoming frustrated because the tests “don’t always work”. Also to spare me many such questions.

![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)

Of course the intersection tests only make sense if the bounding boxes intersect. The intersectsNode method is a [convenience function that you’ll find in Kobold2D](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_c_c_node_07_kobold_extensions_08/), and in the CCNodeExtensions class added to the project.

The pixelMask against pixelMask test is only performed if the other node is also a KKPixelMaskSprite, in all other cases the rectangle intersecting pixelMask test is performed instead. The PixelMaskSpriteClass variable is a static variable initialized in the init method as [self class] simply because sending the class message every time is a bit wasteful compared to the 4 bytes of additional memory for the PixelMaskSpriteClass variable.

Testing intersection of two sprites, whether KKPixelMaskSprite or not, is as simple as writing:

|
1 |
if ([spriteA pixelMaskIntersectsNode:spriteB]) ... |

#### Pixel Mask Performance: BitArray vs. BOOL array

Now to an interesting question: if the BitArray is able to reduce memory usage to 1/8th (12.5%), is it also faster? Let me reveal this as a graphic obtained by performing the pixelMask vs pixelMask check several hundred thousand times repeatedly, and measuring the total running time:

In other words: it is a tradeoff between memory usage and runtime performance. Pixel mask intersection tests are 27% slower on an iPod 4, and 18% slower on an iPhone 3G when using the BitArray. And just in case you’re wondering: if you were to use a UInt16 or even UInt32 array instead of the BOOL array you’ll see a very minor decrease in performance (less than 5%) but double respectively four times the memory usage.

#### Room for Improvement

While writing the KKPixelMaskSprite class I discovered a lot of room for improvement. I don’t want to spare you the list because it also reveals some shortcomings of the class that I think you should be aware of. If you do implement one of these improvements please share them, and if possible share them under a permissive license such as MIT.

##### Possibly useful improvements, in order of usefulness

- cache pixelMasks, for example in a CCPixelMaskCache singleton, or add them to CCTexture2D
- allow pixel mask creation from spriteframes or spriteframe names
- allow collision tests if sprite is rotated to exactly 90, 180 or 270 degrees
- allow use of non-power of two images for pixelMasks on 1st/2nd generation devices
- allow collisions between SD and HD image sprites

##### Potential optimizations in order of expected effectiveness

- reduce pixelMask size by combining 2×2, 3×3, 4×4, etc pixels into a single bit
- OR: only use SD images for pixelMask, forcing collisions on Retina devices to point boundaries
- optimize iterations by testing UInt32 (4x BOOL) or multiple Bits at once for value > 0
- optimize iterations by starting to iterate from corner closest to center

In particular the optimization to reduce the pixelMask size by combining multiple pixels should prove to be very efficient, and is relatively easy to implement. Most pixel-perfect collisions don’t really need to be pixel-perfect, a close-enough approximation is more than enough for most applications. In particular on Retina devices no player will be able to make out if the not-so-pixel-perfect collisions are accurate only within two, three, or possibly even more pixels. The simplest approach would be to just consider only the SD images for pixel masks, even on Retina devices. The added advantage being that a smaller pixelMask equals fewer iterations and thus quicker collision tests.

#### Download the example project with KKPixelMaskSprite

[This project is also available on my github repository](https://github.com/LearnCocos2D/LearnCocos2D) where I host all of the iDevBlogADay source code.

#### Merry piXmas!

This is my last iDevBlogADay post before Xmas. It’s extra large, extra crispy, covered in chocolate, smells like cinnamon, tastes like apples and walnuts and gravy and cookies and turkey, and is [prohibited in the USA because it contains inedible pixels](https://en.wikipedia.org/wiki/Kinder_Surprise#Prohibition_on_sale_or_import_into_the_United_States) and is a choking hazard for everyone who intends to read it in one go.

In that sense, Merry Xmas everyone! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] LearnCocosTV - Episode 1: How I maed your Kobold Fast Pixel-Perfect Collision Detection for Cocos2D with Example Code (2/2) […]

Have you tested performance relative to physics libraries such as Box2d or Chipmunk? I’d be interested to know - I imagine a lot of people only use them for their collision detection functionality.

This can not be reasonably compared because physics engines don’t do pixel-perfect collision tests, they rely on polygons (shapes) to do the collision testing. And the number of vertices in each shape is often severely limited, for example Box2D allows at most 8 vertices per shape.

Actually, I think that they can be reasonably compared.

Game development techniques are often a trade-off between what is “good” and what is “good enough”.

If adding pixel perfect collisions makes your game better to play, but cuts the framerate in half, many developers will choose the higher framerate and lower collision accuracy.

As such, knowing the performance of collision detection for Box2D would help a developer make an informed choice. Of course you should try to make the comparisons as close as possible and would like be using all those 8 vertices.

You’re correct in principle. But in this instance I would say that the decision has to be made by design. Performance just isn’t crucial to this decision.

For example, pixel-perfect collisions are very accurate but don’t work in any of the sprites is rotated or scaled. Whereas if you consider collision-detection with a physics engine your sprites can be rotated or scaled. And chances are that if you want or have to be using a physics engine anyway, using physics to detect all collisions is simply a requirement.

Steffen, I’m glad you built upon my many-years-old post. In my defense, I did state I posted pseudo-code.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I’m oftentimes purposely vague code-wise, specifically because what really matters is the base concept, and I like people to think through it and come up with their own solutions and implementations.

As far as the usability of the code vs say, a physics engine, it really depends on what you’re doing. I recall that when I posted that idea I was working on a Lemmings-type of clone for iOS (never released), and that entailed real-time deformation of terrain in semi-circular shapes which ended up in a plethora of vertices, that caused both Chipmunk and OpenGL ES to choke quite rapidly (we’re talking 1st gen devices here).

Using this method instead, I simply clipped out the “terrain” texture with a circle, update the collision map, and the only minimal slowdown was reuploading the texture from the CPU to the GPU (which only happened when the terrain was actually modified, not that common of an occurrence).

BTW, adjusting the code to work on rotated or scaled nodes is not that complicated. You would simply have to transform the input point before doing the lookup.

I kept thinking that the next logical step would be a Lemmings-style terrain deformation.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


As for transforming the input point, I did that in the first example. Testing if a point is within a scaled and rotated collision map is a matter of converting the point to the node space. But this fails if you want to test two collision maps against each other, and both may be scaled or rotated. Maybe it’s possible though to first transform the currently analyzed point from one node to world space, and then to the other node’s space, not sure if that will give the correct result.

You would need to apply multiple transforms. It’s all really dependent on needs.

If at some point you need to know precise direction, momentum, inertia or any of those vectors as part of the collision, then you’re probably better off with the physics engine.

Hi Steffen

What if the two sprites to check for collision is on different CCLayers, could your code be updated to handle this also? So that the position of the mask sprites are converted to world space or something in the collision check?

Best regards

Søren

Have you verified that the code fails to report the collisions correctly in this case? Because as far as I understand it, converting coordinates to a node’s space (coordinate system) will take into account (or it simply doesn’t matter) that the node may be a child of one or several other nodes.

Hm is did fail, but it complained about rotated nodes and I first saw that now.. I rotate my sprites a lot sadly![:(](../../../wordpress/wp-includes/images/smilies/frownie.png)


Hi Steffen

I have been using KKPixelMaskSprite successfully with my game (it’s great!), but I have changed my sprites to spriteWithSpriteFrameName… and now I realize that it doesn’t work with sprite frames![:(](../../../wordpress/wp-includes/images/smilies/frownie.png)


I’m going to try to adapt KKPixelMaskSprite to work with sprite frames (I suppose it hasn’t been done). Any clue to start with?

Thanks!!

JARV

Finally I get it working with a small workaround… that is ok for my purpose (of couse, it can be improved)

1.- Create a CCRenderTexture with the size of the sprite.

2.- Change sprite position to 0,0 to visit the CCRenderTexture and then restore its original position:

sprite.anchorPoint = ccp(0,0);

sprite.position = ccp(sprite.offsetPositionInPixels.x*(-1)

,sprite.offsetPositionInPixels.y*(-1));

3.- Create a UIImage with the CCRenderTexture:

UIImage *image = [rt getUIImageFromBuffer];

Now we have an UIImage and we can re-use the code from KKPixelMaskSprite (initWithFile).

Just a final consideration, before call to pixelMaskContainsPoint we have to adjust the point because of the offset:

CGPoint point = ccp(point.x-sprite.offsetPositionInPixels.x,point.y-sprite.offsetPositionInPixels.y);

It works great!!

JARV, that sounds great!

Any chance you could share your final detection code? I am struggling with the same problem.. Thanks in advance!

Hi Steffen,

While your code works fine in the simulator (iOS SDK 5) in the device (iphone4) it hangs in the “Pixel-Perfect Sprite Inersection” test when the Sprite collides to center non-movable sprite. This happens at 70% of the collisions.

Did you had any feedback from users about this problem? Do you have any clue why this happens ?

George

What do you mean by “hang”? Haven’t heard of anything like that but I do know there’s a bug if you mix SD and HD images and try to detect collisions between SD and HD images.

Hi,

Thank you for your reply. When I say “hang” I mean it crashes and the application exits to the system.

I didn’t any chnages to your original code. It just crashes not everytime but very frequently.

I am using XCode4 and firmware 5.01 for my phone.

Hi Steffen,

First of all, I am glad you had this class made. I didn’t want to opt for Physics engine just to check collisions.

KKPixelMaskSprite class works great on iPhone 5.1 simulator. But when I test in iPhone 4, it crashes saying ‘pixelMask index out of bounds’. I believe this happens because, on iPHone 4, Kobold uses hd version of the image. For all the images used, I have hd version available. I also have -ipad and -ipadhd versions. It works on iPad 5.1 simulator too, but not on iPad 3 (The new iPad) and crashes with same error. I am using xCode 4.4.1.

Can you please suggest if it supports images with -hd and -ipadhd extension. I believe the crash is because of this. I am using point system instead of pixel system in Cocos2D.

Thanks in advance!

I think there’s a Retina issue. Mainly because it doesn’t make sense to support Retina images for pixel perfect collision detection, the resolution of standard resolution images is high enough for collisions, and will give the same results in point coordinates anyway. I can’t remember exactly but I think I never had a -hd image in the project. You could try to force it to load the SD version.

Thank you very much.

It is very helpful for me : )))

Hi Steffen.

I use this collision and its perfect, but sometimes the app crashes with this log:

“Terminating app due to uncaught exception NSInternalInconsistencyException, reason: other pixelMask index out of bounds for x,y: 162, 142”

Can you tell me what do I have to do? Or what am I doing wrong?

Thanks

George

I don’t understand the code inside the double loop for testing an intersection with another rect:

NSUInteger maxX = intersectRect.origin.x + intersectRect.size.width;

NSUInteger maxY = intersectRect.origin.y + intersectRect.size.height;

for (NSUInteger y = intersectRect.origin.y; y < maxY; y++)

{

for (NSUInteger x = intersectRect.origin.x; x < maxX; x++)

{

NSUInteger index = y * pixelMaskWidth + x;

return pixelMask[index];

}

}

This will always return either YES or NO on the very first iteration. Shouldn't there be an "if" test like this:

if (pixelMask[index]) return pixelMask[index];

If not, why not?

Thanks for this work !

How to use this with a CCSpriteFrameCache texture?

You would have to limit the check to the region (rect) of the sprite frame, and normalize the region as if it were anchored at 0,0.

This is so great!

Thank you Steffen…