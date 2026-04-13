---
title: 'Let there be light: Demo of CCLightNode in Cocos2D-Swift v3.4'
url: http://www.learn-cocos2d.com/2015/01/light-demo-cclightnode-cocos2dswift-v34/
author: Brani says
published: '2015-01-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I thought I’ll give you a demo of the upcoming CCLightNode visual effect that will be available in Cocos2D-Swift v3.4, which comes bundled with the upcoming SpriteBuilder v1.4 (available on the [Mac App Store](https://itunes.apple.com/app/spritebuilder/id784912885) soon, [v1.4 beta is available for download](http://spritebuilder.com/beta)).

### Introducing CCEffect

You may have already heard about the [other shader effects first introduced with Cocos2D-Swift v3.2](http://www.spritebuilder.com/blog/crystals). Below is the Crystals example app, in particular it demonstrates the glass (reflection/refraction) effects:

Pretty neat stuff. More effects have been added in Cocos2D-Swift v3.3. Now with v3.4 around the corner, the CCLightNode and accompanying effects will shine their highly configurable lights on upcoming apps.

### Introducing Lighting via CCLightNode

For the most part, the demo was put together entirely in SpriteBuilder:

It only took a little bit of code to add a light node that you can drag around when touching the screen. I chose to use Swift for this example, if only to highlight that yes, you can use use 100% Swift to make your SpriteBuilder + Cocos2D apps if you wish.


|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 |
import Foundation class MainScene: CCNode { var touchLight : CCNode! func didLoadFromCCB() { self.userInteractionEnabled = true } override func touchBegan(touch: CCTouch!, withEvent event: CCTouchEvent!) { touchLight.visible = true touchLight.position = touch.locationInNode(self) } override func touchMoved(touch: CCTouch!, withEvent event: CCTouchEvent!) { touchLight.position = touch.locationInNode(self) } override func touchEnded(touch: CCTouch!, withEvent event: CCTouchEvent!) { touchLight.visible = false } override func touchCancelled(touch: CCTouch!, withEvent event: CCTouchEvent!) { touchLight.visible = false } } |


Note that in the current beta you still have to enable “experimental effects” by going into ccConfig.h and changing this macro to the value 1:

|
1 |
#define CC_EFFECTS_EXPERIMENTAL 1 |

The result looks pretty neat:

Keep in mind that lighting is a performance-intensive task. I recorded the above video using an iPod touch 5G, a device you can consider low-end these days, hence the performance isn’t super-smooth (22.5 fps).

You should be able to use more active lights if you target the higher end devices. Plus I was using a beta version, so there may be room for optimizations.

In any case the iOS Simulator can not be used to test lighting, even for a single light node its software renderer is just far too slow (less than 10 fps).

### Demo Project

I’ve uploaded the fully functional [SpriteBuilder Lighting Demo Project on Github](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/LightingDemo.spritebuilder). You don’t need SpriteBuilder to run it, just open the .xcodeproj.

Enjoy!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen,

Thanks for the ligthing demo.

The project does not work for me after git clone:

FIRST PROBLEM:

GIT does not contain “Publish-iOS” directory, so even you wrote the project works in Xcode without SpriteBuilder (Version: 1.4.9), it’s not true. One needs to open SpriteBuilder and publish the project.

SECOND PROBLEM:

“Images.png” is missing. I do not know SB well, but it is not publishing d24_by_olracadejup-d4ohe4u_0.png properly. I did a workaround - copied d24_by_olracadejup-d4ohe4u_0.png as Images.png and added it into the project.

The result does not look like yours, but the lights are showing and touch works as well.

Maybe you could have a look and fix it, when you have time.

Regards

Brani