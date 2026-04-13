---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer_gradient/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCLayer.h>`


| (id) | -
|

[CCLayerGradient](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer_gradient/) is a subclass of [CCLayerColor](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer_color/) that draws gradients across the background.

All features from [CCLayerColor](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer_color/) are valid, plus the following new features:

Color is interpolated between the startColor and endColor along the given vector (starting at the origin, ending at the terminus). If no vector is supplied, it defaults to (0, -1) -- a fade from top to bottom.

If 'compressedInterpolation' is disabled, you will not see either the start or end color for non-cardinal vectors; a smooth gradient implying both end points will be still be drawn, however.

If ' compressedInterpolation' is enabled (default mode) you will see both the start and end colors of the gradient.

Whether or not the interpolation will be compressed in order to display all the colors of the gradient both in canonical and non canonical vectors Default: YES