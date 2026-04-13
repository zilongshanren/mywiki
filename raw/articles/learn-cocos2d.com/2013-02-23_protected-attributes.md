---
title: Protected Attributes
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_layer_pan_zoom/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone-extensions
0.2
Cocos2D Extensions API Reference (iOS version) for www.kobold2d.com developers
|

|

represents the layer that can be scrolled and zoomed with one or two fingers.

Distance from bottom edge of panBoundsRect that defines bottom autoscrolling zone in frame mode. Default is 100.0f

Distance from left edge of panBoundsRect that defines left autoscrolling zone in frame mode. Default is 100.0f

The maximum scale level, will change scale if needed automatically. Default is 3.0f

Maximum speed for autosrolling in frame mode Default is 1000.0f

The max distance in points that touch can be dragged before click. If traveled distance is greater then click message will not be sent to the delegate. Default is 15.0f

The minimum scale level, will change scale if needed automatically. Default is 0.5f

Minimum speed for autosrolling in frame mode Default is 100.0f

Describes layer's mode. Defult is kCCLayerPanZoomModeSheet

Rectangle that is used to determine bounds of scrolling area in parent coordinates. Set it to CGRectNull to enable infinite scrolling. Default is CGRectNull

Distance from right edge of panBoundsRect that defines right autoscrolling zone in frame mode. Default is 100.0f

Ratio for rubber effect. Describes the proportion of the panBoundsRect size, that layer can be moved outside from panBoundsRect border. So 0.0f means that layer can't be moved outside from bounds (rubber effect is Off) and 1.0f means that layer can be moved panBoundsRect.size.width far from left/right borders & panBoundsRect.size.height from top/bottom borders. Default is 0.5f. Limitations: only sheet mode is supported.

Time (in seconds) to recover layer position and scale after moving out from panBoundsRect due to rubber effect. Default is 0.2f.

Distance from top edge of panBoundsRect that defines top autoscrolling zone in frame mode. Default is 100.0f