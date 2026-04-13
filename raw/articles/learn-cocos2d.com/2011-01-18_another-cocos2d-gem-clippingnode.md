---
title: 'Another Cocos2D gem: ClippingNode'
url: http://www.learn-cocos2d.com/2011/01/cocos2d-gem-clippingnode/
author: Søren Krogh Neigaard says
published: '2011-01-18'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I needed a way to clip the contents of a node to a specific area of the screen. The goal was to create a scrollable list of items and clipping the items at the top and bottom as they are being scrolled up and down on the screen. The list is of course longer than the screen is high. While you can achieve the same effect by drawing a sprite on top of the scrolling view, I was looking for a cleaner, more flexible and faster solution.

That’s where the glScissor command comes into play. Unfortunately the coordinates are always assuming portrait mode, so you have to rotate them to be able to use Cocos2D coordinates with glScissor. I did some research and found the [solution for transforming glScissor coordinates](http://www.cocos2d-iphone.org/forum/topic/3993) but the rest of that code is too verbose (eg 9 lines instead of the 3 lines needed to transform the Landscape coordinates) and inefficient by needlessly transforming the coordinates every frame.

So I ended up making my own subclass of CCNode called ClippingNode whose children are only drawn within the clippingRegion CGRect (it’s in points). It takes into consideration device rotation and only adjusts the coordinates when either the device rotation changes (name:UIDeviceOrientationDidChangeNotification) or whenever the clippingRegion is updated. In addition the node sets its position at the lower left corner of the clipping region with the contentSize set to the clippingRegion size. By doing so children of the ClippingNode can access the clipping region without having to know that the parent is a ClippingNode class.

To use the ClippingNode, simply add it to your scene hierarchy, then add all other nodes (sprites, labels, etc.) which you want to clip to the ClippingNode. The ClippingNode children will only be drawn with whatever parts are inside the clippingRegion. All other nodes which you do not want to clip you just add to the scene hierarchy as usual. You can of course use two ClippingNodes side-by-side, for example to create a splitscreen view.

##### ClippingNode.h

[cc lang=”objc”]

#import

#import “cocos2d.h”

/** Restricts (clips) drawing of all children to a specific region. */

@interface ClippingNode : CCNode

{

CGRect clippingRegionInNodeCoordinates;

CGRect clippingRegion;

}

@property (nonatomic) CGRect clippingRegion;

@end

[/cc]

##### ClippingNode.m

```
#import "ClippingNode.h"
@interface ClippingNode (PrivateMethods)
-(void) deviceOrientationChanged:(NSNotification*)notification;
@end
@implementation ClippingNode
-(id) init
{
if ((self = [super init]))
{
// register for device orientation change events
[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(deviceOrientationChanged:)
name:UIDeviceOrientationDidChangeNotification object:nil];
}
return self;
}
-(void) dealloc
{
[[NSNotificationCenter defaultCenter] removeObserver:self name:UIDeviceOrientationDidChangeNotification object:nil];
[super dealloc];
}
-(CGRect) clippingRegion
{
return clippingRegionInNodeCoordinates;
}
-(void) setClippingRegion:(CGRect)region
{
// keep the original region coordinates in case the user wants them back unchanged
clippingRegionInNodeCoordinates = region;
self.position = clippingRegionInNodeCoordinates.origin;
self.contentSize = clippingRegionInNodeCoordinates.size;
CCDirector* director = [CCDirector sharedDirector];
CGSize screenSize = [director winSize];
// glScissor requires the coordinates to be rotated to portrait mode
switch (director.deviceOrientation)
{
default:
case kCCDeviceOrientationPortrait:
// do nothing, coords are already correct
break;
case kCCDeviceOrientationPortraitUpsideDown:
region.origin.x = screenSize.width - region.size.width - region.origin.x;
region.origin.y = screenSize.height - region.size.height - region.origin.y;
break;
case kCCDeviceOrientationLandscapeLeft:
region.origin = CGPointMake(region.origin.y, screenSize.width - region.size.width - region.origin.x);
region.size = CGSizeMake(region.size.height, region.size.width);
break;
case kCCDeviceOrientationLandscapeRight:
region.origin = CGPointMake(screenSize.height - region.size.height - region.origin.y, region.origin.x);
region.size = CGSizeMake(region.size.height, region.size.width);
break;
}
// convert to retina coordinates if needed
region = CC_RECT_POINTS_TO_PIXELS(region);
// respect scaling
clippingRegion = CGRectMake(region.origin.x * scaleX_, region.origin.y * scaleY_,
region.size.width * scaleX_, region.size.height * scaleY_);
}
-(void) setScale:(float)newScale
{
[super setScale:newScale];
// re-adjust the clipping region according to the current scale factor
[self setClippingRegion:clippingRegionInNodeCoordinates];
}
-(void) deviceOrientationChanged:(NSNotification*)notification
{
// re-adjust the clipping region according to the current orientation
[self setClippingRegion:clippingRegionInNodeCoordinates];
}
-(void) visit
{
glPushMatrix();
glEnable(GL_SCISSOR_TEST);
glScissor(clippingRegion.origin.x + positionInPixels_.x, clippingRegion.origin.y + positionInPixels_.y,
clippingRegion.size.width, clippingRegion.size.height);
[super visit];
glDisable(GL_SCISSOR_TEST);
glPopMatrix();
}
@end
```


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen,

Any idea why the clipping area of the ClippingNode is smaller (it seems to have the same height but less width) if I enable CC_ENABLE_GL_STATE_CACHE in the ccConfig.h in Kobold2D 2.0.4? I would like to try and run with that cache on, but the ClippingNode does not work right when it is on.

Thank you

Søren

Sorry, no idea. I don’t know what the state cache does but I assume it may use the wrong transformation for the clipping node. Maybe if you look where the macro is used you can find some way to either disable the state cache for the clipping node, or reset the cache before the clipping node is drawn?

Hi,

I have a weird problem when I set the clipping region in init of my ClippingNode subclass it sets the clipping as I’d expect but when I update it later the child view disappears. Any idea why?

Cheers!

Hi

Unfortunately the above code does not even compile in COCOS2D v2. The CCNode variable positionInPixels_ no longer exists and the property director.deviceOrientation no longer exists. So do you know how to fix the code above for COCOS2D V2?

Thanks

Well, after digging into this a bit, I also see that the low level OpenGL code changed dramatically when moving to COCOS2D v2, so you can’t use glPushMatrix and glPopMatrix. So this code appears to be completely broken for COCOS2D v2.

I found the solution for COCOS2D V2 here:

http://www.cocos2d-iphone.org/forum/topic/32102

Thanks Marc for pointing out the solution, helped me greatly!

If it’s of any use, I have created a public repo on GitHub for this.

https://github.com/njt1982/ClippingNode

This version compiles against 2.x and is ARC compatible.

Any Forks or Pull Requests will be appreciated!

And thanks to Steffan for the original work - this is absolutely brilliant!

Thanks, but my work is hardly original. It’s built mainly from scraps found on the cocos2d-iphone forum.