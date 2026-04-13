---
title: Simulating UIScrollView in Cocos2D
url: https://etodd.io/2013/11/26/simulating-uiscrollview-in-cocos2d/
published: '2013-11-26'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Simulating UIScrollView in Cocos2D

I wrote this article for the [Sidebolt company blog](http://www.sidebolt.com/simulating-uiscrollview-in-cocos2d/). Reposting it here for your reading pleasure!

We publish our games on both Mac and iOS. Since UIKit is not available on Mac, we have to build all of our UI by hand in Cocos2D. One of the hardest parts to get right was emulating the UIScrollView bouncy scroll formula. Here it is in action:

There are tons of implementations available in nearly every language and framework, but few of them nail all the important properties of the UIKit scroll:

**When the user is touching the screen:** the page should be glued to their finger. Easy enough.

**After the user flicks the screen and lets go:** the page should “glide”, decelerating slowly until it comes to a stop. Most implementations get this half-right because it’s also pretty easy: just multiply the velocity by a decay factor (we use 0.95) every frame. The real pitfall lies in calculating the velocity at the moment the user lets go of the page. Here’s the naive implementation:

```
-(BOOL) ccTouchBegan:(UITouch*)touch withEvent:(UIEvent*)event
{
_lastFrameTouch = [[CCDirector sharedDirector] convertTouchToGL:touch];
_isTouching = true;
}
-(BOOL) ccTouchMoved:(UITouch*)touch withEvent:(UIEvent*)event
{
CGPoint currentTouch = [[CCDirector sharedDirector] convertTouchToGL:touch];
page.position = ccpAdd(page.position, ccp(0, currentTouch.y - _lastFrameTouch.y));
_lastFrameTouch = currentTouch;
}
-(BOOL) ccTouchEnded:(UITouch*)touch withEvent:(UIEvent*)event
{
CGPoint currentTouch = [[CCDirector sharedDirector] convertTouchToGL:touch];
_velocity = currentTouch.y - _lastFrameTouch.y;
_isTouching = false;
}
-(void) update:(ccTime)dt
{
if (!_isTouching)
{
_velocity *= 0.95f;
_page.position = ccpAdd(_page.position, ccp(0, _velocity));
}
}
```


This works most of the time, but you may find that occasionally the page flies off at warp speed after a very light touch. The reason is that while the user is removing their finger from the screen, their fingertrip is actually changing shape. The center of that shape may move very quickly at the exact instant they release their finger, even if the finger as a whole has only moved straight away from the screen. The solution is not to calculate the velocity when the touch is ended, but to filter the velocity continually like so:

```
-(BOOL) ccTouchBegan:(UITouch*)touch withEvent:(UIEvent*)event
{
_lastFrameTouch = [[CCDirector sharedDirector] convertTouchToGL:touch];
_isTouching = true;
}
-(BOOL) ccTouchMoved:(UITouch*)touch withEvent:(UIEvent*)event
{
CGPoint currentTouch = [[CCDirector sharedDirector] convertTouchToGL:touch];
_unfilteredVelocity = currentTouch.y - _lastFrameTouch.y;
_page.position = ccpAdd(_page.position, ccp(0, _unfilteredVelocity));
_lastFrameTouch = currentTouch;
}
-(BOOL) ccTouchEnded:(UITouch*)touch withEvent:(UIEvent*)event
{
_isTouching = false;
}
-(void) update:(ccTime)dt
{
if (_isTouching)
{
const float kFilterAmount = 0.25f;
_velocity = (_velocity * kFilterAmount) + (_unfilteredVelocity * (1.0f - kFilterAmount));
_unfilteredVelocity = 0.0f;
}
else
{
_velocity *= 0.95f;
_page.position = ccpAdd(_page.position, ccp(0, _velocity));
}
}
```


**When the page is gliding and it hits the bottom:** this is where some implementations start to break down. The page should go past the edge and elastically snap back. Many implementations just stop the page immediately, or worse, bounce off the bottom inelastically.

```
-(void) update:(ccTime)dt
{
if (_isTouching)
{
const float kFilterAmount = 0.25f;
_velocity = (_velocity * kFilterAmount) + (_unfilteredVelocity * (1.0f - kFilterAmount));
_unfilteredVelocity = 0.0f;
}
else
{
const float kScrollSnapMaxSpeed = 17.0f;
const float kScrollSnapMaxAcceleration = 2.2f;
const float kScrollSnapBackRatio = 0.1f;
bool decay = true;
// Calculate screen bounds and page bounds
= _page.contentSize;
size.width *= _page.scaleX;
size.height *= _page.scaleY;
CGPoint anchor = _page.anchorPoint;
CGPoint pos = _page.position;
CGPoint min = ccp(pos.x - (size.width * anchor.x), pos.y - (size.height * anchor.y));
CGPoint max = ccp(pos.x + (size.width * (1.0f - anchor.x)), pos.y + (size.height * (1.0f - anchor.y)));
CCNode* p = _page.parent;
CGSize parentSize = p ? p.contentSize : [CCDirector sharedDirector].winSize;
CGRect parentRect = CGRectZero;
parentRect.size.width = MIN(size.width, parentSize.width);
parentRect.size.height = MIN(size.height, parentSize.height);
parentRect.origin.x = 0;
parentRect.origin.y = parentSize.height - parentRect.size.height;
if (min.y > parentRect.origin.y) // We want negative velocity
decay = false;
_velocity = MIN(_velocity, kScrollSnapMaxSpeed);
_velocity += MAX(((min.y - parentRect.origin.y) * -kScrollSnapBackRatio) - _velocity, -kScrollSnapMaxAcceleration);
}
if (max.y < parentRect.origin.y + parentRect.size.height) // We want positive velocity
decay = false;
_velocity = MAX(_velocity, -kScrollSnapMaxSpeed);
_velocity += MIN(((parentRect.origin.y + parentRect.size.height - max.y) * kScrollSnapBackRatio) - _velocity, kScrollSnapMaxAcceleration);
}
if (decay)
_velocity *= 0.95f;
_page.position = ccpAdd(_page.position, ccp(0, _velocity));
}
}
```


**When the user has their finger on the screen and tries to scroll past the edge (overscroll):** a lot of implementations keep the page glued to the user's finger when this happens. It's easy to miss, but UIKit actually slows the scroll down to about 40% of the normal speed.

```
-(BOOL) ccTouchMoved:(UITouch*)touch withEvent:(UIEvent*)event
{
currentTouch = [[CCDirector sharedDirector] convertTouchToGL:touch];
_unfilteredVelocity = currentTouch.y - _lastFrameTouch.y;
const float kOverscrollRatio = 0.4f;
// calculate min, max, and parentSize
if (min.y > 0.0f)
_unfilteredVelocity *= (1.0f - (min.y / parentSize.height)) * kOverscrollRatio;
if (max.y < parentSize.height)
_unfilteredVelocity *= (1.0f - ((parentSize.height - max.y) / parentSize.height)) * kOverscrollRatio;
page.position = ccpAdd(page.position, ccp(0, _unfilteredVelocity));
_lastFrameTouch = currentTouch;
}
```


And that's it! The results speak for themselves. Happy scrolling!