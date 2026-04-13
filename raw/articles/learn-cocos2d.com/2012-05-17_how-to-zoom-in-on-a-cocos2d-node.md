---
title: How to Zoom In on a Cocos2D Node
url: http://www.learn-cocos2d.com/2012/05/zoom-cocos2d-node/
author: DeMan says
published: '2012-05-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![iOS Simulator - iPhone - iOS 5.1 (9B176) 2](../../../wordpress/wp-content/uploads/iOS-Simulator-iPhone-iOS-5.1-9B176-2-300x154.png)


Time to add another project to my github repository. This time I’m answering the frequently asked question (in some form or another) how to zoom in on a particular node. For example zooming in on the player when he dies.

That’s not as trivial as it sounds, but you can make it easy if you follow some guidelines.

First, you want to put all nodes that should be affected by the zoom in the same layer. Then you should avoid changing the position or anchorpoint of the layer - if you still want to change the position of the layer I suggest to add this layer into another, toplevel layer and then only change the position of the toplevel layer. Use the cocos2d node hierarchy to your advantage. And don’t use the CCCamera.

The behavior of this example project is best observed with your own eyes. You can [get the ZoomInOnMe project on github](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/Cocos2D-ZoomInOnMe).


#### Scaling the Layer to Zoom In/Out

Every couple seconds the zoomInOnPlayer method gets executed. It simply uses CCScaleTo actions to zoom the layer in and out. It also sets the isZooming flag for the duration of the zoom, and resets the layer’s position at the end because it may be slightly off due to rounding errors.

So really there’s nothing special here, the meat is in the update method.

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 |
-(void) zoomInOnPlayer:(ccTime)delta { // just to be sure no other actions interfere [self stopAllActions]; isZooming = YES; id zoomIn = [CCScaleTo actionWithDuration:3.0f scale:kZoomInFactor]; id zoomOut = [CCScaleTo actionWithDuration:2.0f scale:1.0f]; id reset = [CCCallBlock actionWithBlock:^{ CCLOG(@"zoom in/out complete"); isZooming = NO; self.position = CGPointZero; [self scheduleOnce:@selector(zoomInOnPlayer:) delay:CCRANDOM_0_1() * 2.0f + 2.0f]; }]; id sequence = [CCSequence actions:zoomIn, zoomOut, reset, nil]; [self runAction:sequence]; } |

#### Moving the Layer so it centers in on a node

![iOS Simulator - iPhone - iOS 5.1 (9B176)](../../../wordpress/wp-content/uploads/iOS-Simulator-iPhone-iOS-5.1-9B176-300x154.png)


There’s a scheduled update method which adjusts the position of the layer every frame, if it is in zoom mode. The layer centers on its anchorPoint when zooming in/out, and that happens to be at the center of the screen. Hence the offsetToCenter point which gives us the distance from the screen center to the current player position. This offset is then multiplied by the current scale factor of the layer (self.scale).

Unfortunately that’s not quite enough. If that were all you did you would have the layer centered on the player’s position just fine, but it will be an instant snap and not a gradual movement. But if that’s all you want, you can comment out line 13 and you’re done.

To have the layer smoothly hone in on its target over time, line 13 is needed. There’s a global kZoomInFactor which is the final zoom factor. You have to determine that up-front, or store it in an instance variable if you want to be able to change the zoom in factor. By subtracting the scale from the zoom factor and then dividing the result by zoom factor minus one, you get a multiplier which gradually goes towards 0 the greater the layer’s scale gets.

Multiply the factor with offsetToCenter and then subtract it from the layer’s position causes the layer to gradually move towards the targeted node. The reason for that is actually line 12, where you multiply the offset from the screen center to the player position with scale. The problem is that scale does not start at 0 but is usually 1. So you’ll already be adding 1 times the offset to the layer’s position. You could also change line 12 to multiply with (self.scale - 1) but that would cause the zoom in to never quite center in on the targeted node.

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 |
-(void) update:(ccTime)delta { … if (isZooming) { CGSize screenSize = [CCDirector sharedDirector].winSize; CGPoint screenCenter = CGPointMake(screenSize.width * 0.5f, screenSize.height * 0.5f); CGPoint offsetToCenter = ccpSub(screenCenter, player.position); self.position = ccpMult(offsetToCenter, self.scale); self.position = ccpSub(self.position, ccpMult(offsetToCenter, (kZoomInFactor - self.scale) / (kZoomInFactor - 1.0f))); } } |

Feel free to play with these calculations. If you like to extend on this, then a generalized solution for zooming in on nodes, even taking the layer’s current position into account, would be very much appreciated.

Note: the code should also work with CCScene instead of CCLayer, but it may or may not work with other nodes due to the relative anchor point setting used by CCScene and CCLayer. Let me know if you were able to successfully implement this on a CCTMXLayer for example.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

The above code works great.

Is there a way to keep the background image the same size? So when you zoom into your player the background appears to be the same size and does not move.

Thanks

Add the background image to a different layer or the scene itself, that ought to work.

Steffen - I’m always amazed by your contributions to the dev community, I’ve learned a ton from your stuff.

But I’m stumped with a problem - I’m trying to use the code above on a side scroller game, and I can’t figure out how to make it work when the layer has been positioned to the left (or any position other than 0,0). I need to have the zoom to a location to the far right of the screen (a sprite is located off screen at 2000,200), from a layer starting position of (-400, 0).

I’ve tried changing the screenCenter.x by the offset of the layer, but that doesn’t seem to work - or I’m doing it wrong.

Any change you could give me some clues? Thanks in advance!