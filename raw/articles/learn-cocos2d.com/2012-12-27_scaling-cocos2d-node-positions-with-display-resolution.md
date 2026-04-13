---
title: Scaling Cocos2D Node Positions with Display Resolution
url: http://www.learn-cocos2d.com/2012/12/scaling-cocos2d-node-positions-display-resolution/
author: KoboldTouch Autoscaling Demo most wanted feature; Learn; Master Cocos
published: '2012-12-27'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Here’s a quick tip on how to design your scenes so that they scale up to higher resolution displays. For example when your app runs on a widescreen iPhone / iPod touch or on an iPad. This article is not about Retina displays, which use the same coordinate system and merely display higher resolution images.

#### Design for the lowest supported resolution

First, design your game to the lowest device/window resolution that your app supports. In most cases this will be the 480×320 points used by the majority of iPhones.

Contrary to images, you always want to scale your designed screen layouts up and never down. This is because upscaled screens will always fit on the device’s display, with more or less additional spacing between the nodes. Downscaling however might cause screen elements to overlap, which is hard to fix if you don’t see the overlap in the resolution you design for.

It’s also easier to make manual changes to upscaled screen layouts than it is for downscaled screen layouts.

#### Calculate the scaling factor

By dividing the current device/window size with the resolution you designed for, you get the scaling factor by which you have to multiply positions. This is a simple wrapper you can use:

|
1 2 3 4 5 6 7 8 9 |
static CGSize designSize = {480, 320}; -(CGPoint) scalePoint:(CGPoint)point { CGSize winSize = [CCDirector sharedDirector].winSize; CGSize scaleFactor = CGSizeMake(winSize.width / designSize.width, winSize.height / designSize.height); return CGPointMake(point.x * scaleFactor.width, point.y * scaleFactor.height); } |


To make a node’s position resolution independent, use the position you would use for a 480×320 screen and scale it up:

|
1 2 |
// centers the sprite, regardless of window size sprite.position = [self scalePoint:CGPointMake(240, 160)]; |


This even works for autorotation. If you use NSNotificationCenter to receive orientation change events, you can use the scalePoint method with the current position to generate the node’s position after the rotation happened. You can try by simply changing the designSize to {320, 480} and setting the app’s default orientation to Portrait.

#### Caveats

Of course it’s entirely up to you what makes sense, which nodes can be scaled and which should not. For example squeezing a landscape app in portrait mode is possible, but it simply won’t make for a good user experience. However scaling HUD elements that should be aligned with one side of the screen so that they automatically stick to the side of the screen (ie widescreen iPhones, iPad) would be a huge timesaver.

If you update your node’s positions manually in order to move them, then you may have to also scale the amount by which the node moves. It’s easy to do by multiplying the movement vector with the same scale factor.

This won’t work well for actions, which may run faster (or sometimes even slower) depending on window size and aspect ratio. But it’ll work with actions nonetheless if you also apply the scale factor to the target position.

Another issue to watch out for is to accidentally scale up a position, and then scale it up again. This can happen if you’re not careful when updating more complex algorithms or dependencies where more than one method updates the node’s position. The best way to avoid that is to ignore scaling until just before the screen is drawn. You could override the draw or visit method (don’t forget to call super) and scale the position:

|
1 |
self.position = [self scalePoint:self.position]; |

After drawing is complete you could then reset the position back to its original by dividing by the scale factor. I’ll leave it up to you to add a convenience method for that. That would make the position scaling completely transparent to your app and you could simply consider all screens to be in the designed for resolution.

#### KoboldTouch

I will be adding a KTAutoscaleController to [KoboldTouch](http://www.learn-cocos2d.com/store/koboldtouch/) soon to make this easier for KT users. This will be a really nice feature to have, and really easy to use:

|
1 2 3 4 5 6 7 |
KTAutoscaleController* autoscaleController = [KTAutoscaleController controller]; autoscaleController.designResolution = CGSizeMake(480.0f, 320.0f); [self addSubController:autoscaleController]; // autoscale this sprite's position depending on window size [autoscaleController autoscaleNode:sprite scaledProperties:KTAutoscalePropertyPosition]; |


Until next year, have an enjoyable year’s end!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] already blogged about scaling node positions with display resolution. This feature is now built into KoboldTouch. Time for a demonstration before I get back to work on […]